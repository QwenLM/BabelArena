import json
import re
from typing import Union, Dict, List
from pathlib import Path
from base_shopping_tool import BaseShoppingTool, register_tool

# List of valid coupons
VALID_COUPONS = [
    "Cross-store: ¥30 off every ¥300",
    "Cross-store: ¥60 off every ¥500",
    "Cross-store: ¥120 off every ¥900",
    "Cross-store: ¥200 off every ¥1,200",
    "Cross-store: ¥300 off every ¥1,500",
    "Same-brand: ¥25 off every ¥200",
    "Same-brand: ¥60 off every ¥400",
    "Same-brand: ¥180 off every ¥1,000",
    "Same-brand: ¥300 off every ¥1,200",
    "VIP: ¥200 off every ¥1,000",
]


@register_tool('delete_coupon_from_cart')
class DeleteCouponFromCartTool(BaseShoppingTool):
    """
    Tool to remove coupons from cart. Updates cart total after removing coupons.
    """

    LANG_FIELDS = {
        'en': {
            'coupon_name_required': "coupon_name is required",
            'quantity_positive': "quantity must be a positive number",
            'invalid_coupon_name': lambda coupon_name, valid_coupons_str: f"Invalid coupon name: '{coupon_name}'. Valid coupons are: {valid_coupons_str}",
            'coupon_not_in_cart': lambda coupon_name: f"Coupon not in cart: '{coupon_name}'",
            'insufficient_coupon_in_cart': lambda cart_count, coupon_name, quantity: f"Insufficient coupon quantity in cart: Cart has {cart_count} of '{coupon_name}', cannot remove {quantity}",
            'save_cart_failed': lambda err: f"Failed to save cart: {err}",
        },
        'zh': {
            'coupon_name_required': "缺少 coupon_name 参数",
            'quantity_positive': "quantity 必须为正数",
            'invalid_coupon_name': lambda coupon_name, valid_coupons_str: f"无效的优惠券名称：'{coupon_name}'。可用优惠券：{valid_coupons_str}",
            'coupon_not_in_cart': lambda coupon_name: f"购物车中不存在该优惠券：'{coupon_name}'",
            'insufficient_coupon_in_cart': lambda cart_count, coupon_name, quantity: f"购物车中优惠券数量不足：当前有 {cart_count} 张 '{coupon_name}'，无法移除 {quantity} 张",
            'save_cart_failed': lambda err: f"购物车保存失败：{err}",
        },
    }

    def __init__(self, cfg: Dict = None):
        super().__init__(cfg)
        self.cart_data: Dict = {}

        # Default cart path relative to this file
        default_cart_path = Path(__file__).parent.parent / 'database' / 'case_0' / 'cart.json'
        if self.cfg and 'database_path' in self.cfg and self.cfg['database_path']:
            cart_path = Path(self.cfg['database_path']) / 'cart.json'
        else:
            cart_path = default_cart_path

        self.cart_path = cart_path
        self._load_cart(cart_path)

    def _load_cart(self, path: Path):
        """Load cart data from JSON file."""
        default_cart = {
            "items": [],
            "used_coupons": [],
            "summary": {"total_items_count": 0, "total_price": 0.0},
        }
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    self.cart_data = default_cart
                    return

                data = json.loads(content)
                if isinstance(data, dict):
                    self.cart_data = data
                    if 'items' not in self.cart_data:
                        self.cart_data['items'] = []
                    if 'used_coupons' not in self.cart_data:
                        self.cart_data['used_coupons'] = []
                    if 'summary' not in self.cart_data:
                        self.cart_data['summary'] = {
                            "total_items_count": len(self.cart_data.get('items', [])),
                            "total_price": 0.0
                        }
                else:
                    self.cart_data = default_cart
        except FileNotFoundError:
            self.cart_data = default_cart
        except (json.JSONDecodeError, Exception):
            self.cart_data = default_cart

    def _save_cart(self):
        """Save cart data to file."""
        with open(self.cart_path, 'w', encoding='utf-8') as f:
            json.dump(self.cart_data, f, ensure_ascii=False, indent=4)

    def _parse_coupon(self, coupon_name: str):
        """
        Parse coupon string and extract the discount amount.
        Example: "Cross-store: ¥30 off every ¥300" -> 30.0
        """
        pattern = r'¥([\d,]+)\s+off\s+every\s+¥([\d,]+)'
        match = re.search(pattern, coupon_name)
        if not match:
            return None

        discount_str = match.group(1).replace(',', '')
        try:
            discount = float(discount_str)
            return discount
        except ValueError:
            return None

    def _calculate_base_total(self) -> float:
        """Calculate the base total price of the cart (without coupon discounts)."""
        items = self.cart_data.get('items', [])
        total = 0.0
        for item in items:
            # Support both price and items_price field names
            price = float(item.get('price') or item.get('items_price', 0.0))
            quantity = int(item.get('quantity', 0))
            total += price * quantity
        return round(total, 2)

    def _calculate_total_discount(self, used_coupons: List[Dict]) -> float:
        """Calculate the total discount amount from all used coupons."""
        total_discount = 0.0
        for coupon in used_coupons:
            # Support two data structures:
            # 1. {coupon_name: quantity} - dict, key is the coupon name
            # 2. {"coupon_name": coupon_name, "quantity": quantity} - dict with coupon_name field
            if isinstance(coupon, dict):
                coupon_name = None
                quantity = 0
                # New format: {coupon_name: quantity}
                if len(coupon) == 1:
                    coupon_name = list(coupon.keys())[0]
                    quantity = int(coupon.get(coupon_name, 0))
                # Old format: {"coupon_name": ..., "quantity": ...}
                elif 'coupon_name' in coupon:
                    coupon_name = coupon.get('coupon_name', '')
                    quantity = int(coupon.get('quantity', 0))
                if coupon_name:
                    discount = self._parse_coupon(coupon_name)
                    if discount is not None:
                        total_discount += discount * quantity
        return round(total_discount, 2)

    def _update_summary(self):
        """Update cart summary statistics including coupon discounts."""
        items = self.cart_data.get('items', [])
        total_items_count = sum(item.get('quantity', 0) for item in items)
        base_total = self._calculate_base_total()
        used_coupons = self.cart_data.get('used_coupons', [])
        total_discount = self._calculate_total_discount(used_coupons)
        final_price = max(0.0, base_total - total_discount)
        if 'summary' not in self.cart_data:
            self.cart_data['summary'] = {}
        self.cart_data['summary']['total_items_count'] = total_items_count
        self.cart_data['summary']['total_price'] = round(final_price, 2)

    def _cleanup_zero_quantity_coupons(self):
        """Remove coupons with quantity 0 from the cart."""
        used_coupons = self.cart_data.get('used_coupons', [])
        cleaned_coupons = []
        for coupon in used_coupons:
            if isinstance(coupon, dict):
                # New format: {coupon_name: quantity}
                if len(coupon) == 1:
                    coupon_name = list(coupon.keys())[0]
                    quantity = int(coupon.get(coupon_name, 0))
                    if quantity > 0:
                        cleaned_coupons.append(coupon)
                # Old format: {"coupon_name": ..., "quantity": ...}
                elif 'coupon_name' in coupon:
                    quantity = int(coupon.get('quantity', 0))
                    if quantity > 0:
                        cleaned_coupons.append(coupon)
        self.cart_data['used_coupons'] = cleaned_coupons

    def call(self, params: Union[str, dict], **kwargs) -> str:
        """
        Remove coupon from cart.
        Args:
            - coupon_name: Coupon name (required)
            - quantity: Quantity to remove (optional, default: 1)
        """
        self._load_cart(self.cart_path)
        try:
            params_dict = self._verify_json_format_args(params)
        except ValueError as e:
            return self.format_result_as_json({"error": str(e)})

        coupon_name = params_dict.get('coupon_name')
        quantity = params_dict.get('quantity', 1)

        if not coupon_name:
            return self.format_result_as_json({
                "error": self.fields['coupon_name_required'],
            })

        if not isinstance(quantity, (int, float)) or quantity <= 0:
            return self.format_result_as_json({
                "error": self.fields['quantity_positive'],
            })

        if coupon_name not in VALID_COUPONS:
            return self.format_result_as_json({
                "error": self.fields['invalid_coupon_name'](coupon_name, ', '.join(VALID_COUPONS)),
            })

        quantity = int(quantity)
        used_coupons = self.cart_data.get('used_coupons', [])
        coupon_found = False
        current_quantity = 0
        coupon_index = -1

        for idx, coupon in enumerate(used_coupons):
            if isinstance(coupon, dict):
                # New format: {coupon_name: quantity}
                if len(coupon) == 1:
                    existing_coupon_name = list(coupon.keys())[0]
                    if existing_coupon_name == coupon_name:
                        coupon_found = True
                        coupon_index = idx
                        current_quantity = int(coupon.get(coupon_name, 0))
                        break
                # Old format: {"coupon_name": ..., "quantity": ...}
                elif 'coupon_name' in coupon:
                    if coupon.get('coupon_name') == coupon_name:
                        coupon_found = True
                        coupon_index = idx
                        current_quantity = int(coupon.get('quantity', 0))
                        break

        if not coupon_found:
            return self.format_result_as_json({
                "error": self.fields['coupon_not_in_cart'](coupon_name),
            })

        if current_quantity < quantity:
            return self.format_result_as_json({
                "error": self.fields['insufficient_coupon_in_cart'](current_quantity, coupon_name, quantity),
            })

        new_quantity = current_quantity - quantity

        if new_quantity == 0:
            used_coupons.pop(coupon_index)
        else:
            coupon = used_coupons[coupon_index]
            if len(coupon) == 1:
                coupon_name_key = list(coupon.keys())[0]
                coupon[coupon_name_key] = new_quantity
            elif 'coupon_name' in coupon:
                coupon['quantity'] = new_quantity

        self.cart_data['used_coupons'] = used_coupons
        self._cleanup_zero_quantity_coupons()
        self._update_summary()

        try:
            self._save_cart()
        except Exception as e:
            return self.format_result_as_json({
                "error": self.fields['save_cart_failed'](str(e)),
            })

        return self.format_result_as_json(self.cart_data)
