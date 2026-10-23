import json
import os
from typing import Union, Dict
from pathlib import Path
from base_shopping_tool import BaseShoppingTool, register_tool

# Province aliases for normalization, including various spellings and abbreviations
PROVINCE_ALIASES = {
    'beijing': ['beijing', 'bj', '北京'],
    'shanghai': ['shanghai', 'sh', '上海'],
    'tianjin': ['tianjin', 'tj', '天津'],
    'chongqing': ['chongqing', 'cq', '重庆'],
    'hebei': ['hebei', 'ji', '河北'],
    'shanxi': ['shanxi', 'jin', '山西'],
    'liaoning': ['liaoning', 'liao', '辽宁'],
    'jilin': ['jilin', 'ji_ln', '吉林'],  # Avoid confusion with hebei
    'heilongjiang': ['heilongjiang', 'hei', '黑龙江'],
    'jiangsu': ['jiangsu', 'su', '江苏'],
    'zhejiang': ['zhejiang', 'zhe', '浙江'],
    'anhui': ['anhui', 'wan', '安徽'],
    'fujian': ['fujian', 'min', '福建'],
    'jiangxi': ['jiangxi', 'gan', '江西'],
    'shandong': ['shandong', 'lu', '山东'],
    'henan': ['henan', 'yu', '河南'],
    'hubei': ['hubei', 'e', '湖北'],
    'hunan': ['hunan', 'xiang', '湖南'],
    'guangdong': ['guangdong', 'yue', 'gd', '广东'],
    'hainan': ['hainan', 'qiong', '海南'],
    'sichuan': ['sichuan', 'chuan', 'shu', '四川'],
    'guizhou': ['guizhou', 'qian', 'gui_gz', '贵州'],  # Avoid confusion with guangxi
    'yunnan': ['yunnan', 'yun', 'dian', '云南'],
    'shaanxi': ['shaanxi', 'shan', 'qin', '陕西'],  # shǎnxī
    'gansu': ['gansu', 'gan_gs', '甘肃'],  # Avoid confusion with jiangxi
    'qinghai': ['qinghai', 'qing', '青海'],
    'inner mongolia': ['inner mongolia', 'neimenggu', 'meng', '内蒙古'],
    'guangxi': ['guangxi', 'gui', '广西'],
    'tibet': ['tibet', 'xizang', 'zang', '西藏'],
    'ningxia': ['ningxia', 'ning', '宁夏'],
    'xinjiang': ['xinjiang', 'xin', '新疆'],
    'hongkong': ['hongkong', 'hk', 'xianggang', '香港'],
    'macau': ['macau', 'mo', 'aomen', '澳门'],
    'taiwan': ['taiwan', 'tw', '台湾']
}

# Per-language transliterations of canonical Chinese province names, scraped from
# the per-language v3 DBs (`database_level{N}_<code>/`). Pre-normalized: lowercased
# and whitespace-stripped so they line up with `_normalize_province` preprocessing.
# Covers the 23 provinces that actually appear as user destinations or product
# shipping_info.origin across L1/L2/L3. Without these the tool fails on 42-68%
# of `calculate_transport_time` calls for the 16 non-Latin / non-Chinese langs
# (plus Vietnamese which renders e.g. "Quảng Đông"), because the localized DBs
# transliterate place names but the tool itself only understands Latin + Chinese.
LOCALIZED_PROVINCE_ALIASES = {
    'anhui': ['anhuy', 'аньхой', 'אנהוי', 'آنهوي', 'आनहुई', 'ਅਨਹੂਈ', 'அன்ஹுய்', 'అన్హుయ్', 'อันฮุย', 'ອານຮຸຍ', 'အန်းဟွေ', 'អានហ៊ូយ', '안후이'],
    'beijing': ['bắckinh', 'pekin', 'pekín', 'pékin', 'бейжің', 'пекин', 'пекін', "בייג'ינג", 'بكين', 'बीजिंग', 'ਬੀਜਿੰਗ', 'ਬੇਜਿੰਗ', 'பீஜிங்', 'பெய்ஜிங்', 'బీజింగ్', 'ปักกิ่ง', 'ປັກກິ່ງ', 'ပေကျင်း', 'ប៉េកាំង', '베이징'],
    'chongqing': ['trùngkhánh', 'çongking', 'чунцин', 'чунцын', "צ'ונגצ'ינג", 'تشونغتشينغ', 'चोंगकिंग', 'ਚੋਂਗਕਿੰਗ', 'சோங்கிங்', 'చోంగ్‌కింగ్', 'ฉงชิ่ง', 'ຊົງຊິງ', 'ချုံကင်း', 'ឆុងឈីង', '重慶', '충칭'],
    'fujian': ['phúckiến', 'фуцзянь', "פוג'יין", 'فوجيان', 'फ़ुजियान', 'ਫੁਜਿਆਨ', 'ஃபுஜியான்', 'ఫుజియాన్', 'ฝูเจี้ยน', 'ຝູຈ້ຽນ', 'ဖူကျန်း', 'ហ្វូជៀន', '복건'],
    'guangdong': ['quảngđông', 'гуандун', 'גואנגדונג', 'غوانغدونغ', 'गुआंगडोंग', 'ਗੁਆਂਗਡੋਂਗ', 'குவாங்டாங்', 'గ్వాంగ్డాంగ్', 'กวางตุ้ง', 'ກວາງຕຸ້ງ', 'ကွမ်တုံ', 'ក្វាងទុង', '広東', '광동'],
    'guangxi': ['quảngtây', 'гуанси', 'гуансі', 'גואנגשי', 'قوانغشي', 'गुआंग्शी', 'ਗੁਆਂਗਸੀ', 'குவாங்சி', 'గ్వాంగ్జీ', 'กว่างซี', 'ກວາງຊີ', 'ကွမ်စီ', 'ក្វាងស៊ី', '広西', '광시'],
    'guizhou': ['quýchâu', 'гуйчжоу', "גויז'ו", 'قويتشو', 'गुइझोउ', 'ਗੁਇਝੋਉ', 'குயிசோ우', 'గుయిజౌ', 'กุ้ยโจว', 'ກວ້ຍໂຈວ', 'ကွေဇိုး', 'ក្វៃចូវ', '貴州', '구이저우'],
    'hainan': ['hảinam', 'хайнань', 'היינאן', 'هاينان', 'हैनान', 'ਹਾਈਨਾਨ', 'ஹைனான்', 'హైనాన్', 'ไห่หนาน', 'ໄຫນານ', 'ဟိုင်နန်', 'ហៃណាន', '하이난'],
    'hebei': ['hàbắc', 'хэбэй', 'הביי', 'خبي', 'हेबेई', 'ਹੇਬੇਈ', 'ஹெபெய்', 'హెబీ', 'เหอเป่ย', 'ເຫີເບຍ', 'ဟေဘေ', 'ហឺប៉ី', '허베이'],
    'heilongjiang': ['hắclonggiang', 'хэйлунцзян', "היילונגג'יאנג", 'هيلونغجيانغ', 'हेलोंगजियांग', 'ਹੇਇਲੋਂਗਜਿਆਂਗ', 'ஹெய்லோங்ஜியாங்', 'హైలాంగ్జియాంగ్', 'เฮยหลงเจียง', 'ເຮຍລົງຈຽງ', 'ဟဲလိုင်ဂျီယန်း', 'ហែលុងជាំង', '黒竜江', '헤이룽장'],
    'henan': ['hànam', 'хэнань', 'הנאן', 'خنان', 'हेनान', 'ਹੇਨਾਨ', 'ஹெனான்', 'హెనాన్', 'เหอหนาน', 'ເຫີນານ', 'ဟဲနန်', 'ហឺណាន', '허난'],
    'hubei': ['hồbắc', 'хубэй', 'הוביי', 'هوبي', 'हूबेई', 'ਹੁਬੇਈ', 'ஹுபெய்', 'హుబే', 'หูเป่ย', 'ຫູເບຍ', 'ဟူဘေ', 'ហ៊ូប៉ី', '후베이'],
    'hunan': ['hồnam', 'хунань', 'הונאן', 'هونان', 'हूनान', 'ਹੁਨਾਨ', 'ஹுனான்', 'హునాన్', 'หูหนาน', 'ຫູນານ', 'ဟူနန်', 'ហ៊ូណាន', '후난'],
    'jiangsu': ['giangtô', 'цзянсу', "ג'יאנגסו", 'جيانغسو', 'जियांगसू', 'ਜਿਆਂਗਸੂ', 'ஜியாங்சு', 'జియాంగ్సు', 'เจียงซู', 'ຈ້ຽງຊູ', 'ဂျန်းစူး', 'ជាំងស៊ូ', '江蘇', '강소'],
    'liaoning': ['liêuninh', 'ляанін', 'ляонин', 'ליאונינג', 'لياونينغ', 'लियाओनिंग', 'ਲਿਆਓਨਿੰਗ', 'லியாவோனிங்', 'లియానింగ్', 'เหลียวหนิง', 'ເລຍວນິງ', 'လီယာိုနင်း', 'លៀអូនីង', '遼寧', '랴오닝'],
    # NOTE: shaanxi and shanxi share some transliterations (hindi 'शांक्सी', korean
    # '산시'). We bias those toward shanxi (more common) since the existing alias
    # map already disambiguates shaanxi with 'qin'/'shan'. shaanxi-only forms here.
    'shaanxi': ['thiểmtây', 'шэньси', 'шэньсі', 'שאאנשי', 'شنشي', 'ਸ਼ਾਨਸ਼ੀ', 'ஷாஅன்சி', 'షాన్షీ', 'ส่านซี', 'ຊານຊີ', 'ရှန်အန်စီ', '陝西'],
    'shandong': ['sơnđông', 'шаньдун', 'שאנדונג', 'شاندونغ', 'शानदोंग', 'ਸ਼ਾਂਦੋਂਗ', 'ஷாண்டோங்', 'షాండాంగ్', 'ซานตง', 'ຊານຕົງ', 'ရှန်တုံ', 'សានតុង', '山東', '산둥'],
    'shanghai': ['shanghái', 'thượnghải', 'şanghay', 'шанхай', 'שאנגחאי', 'שנגחאי', 'شنغهاي', 'शंघाई', 'ਸ਼ੰਘਾਈ', 'ஷாங்காய்', 'షాంఘై', 'เซี่ยงไฮ้', 'ຊັງຫາຍ', 'ຊຽງໄຮ້', 'ရှန်ဟိုင်း', 'សៀងហៃ', '상하이'],
    'shanxi': ['sơntây', 'шаньси', 'шаньсі', 'שאנשי', 'شانشي', 'शांक्सी', 'ਸ਼ਾਂਸ਼ੀ', 'ஷான்சி', 'షాన్సీ', 'ซานซี', 'ຊານຊິ', 'ရှန်စီ', 'សានស៊ី', '산시'],
    'sichuan': ['tứxuyên', 'сычуань', "סצ'ואן", 'سيتشوان', 'सिचुआन', 'ਸਿਚੁਆਨ', 'சிச்சுவான்', 'సిచువాన్', 'เสฉวน', 'ສີຈວນ', 'စီချွန်း', 'ស៊ីឆួង', '쓰촨'],
    'tianjin': ['thiêntân', 'тяньцзинь', 'цяньцзінь', "טיינג'ין", 'تيانجين', 'तियानजिन', 'ਤਿਆਨਜਿਨ', 'தியான்ஜின்', 'టియాన్‌జిన్', 'เทียนจิน', 'ທຽນຈິນ', 'တိန်ကျင်း', 'ទៀនជិន', '천진'],
    'yunnan': ['vânnam', 'юньнань', 'יונאן', 'يونان', 'युन्नान', 'ਯੁਨਾਨ', 'யுன்னான்', 'యున్నాన్', 'ยูนนาน', 'ຢຸນນານ', 'ယူနန်', 'យូណាន', '雲南', '윈난'],
    'zhejiang': ['chiếtgiang', 'чжэцзян', "ג'ג'יאנג", 'تشجيانغ', 'झेजियांग', 'ਝੇਜਿਆਂਗ', 'ஜெஜியாங்', 'జెజియాంగ్', 'เจ้อเจียง', 'ເຈີ້ຈຽງ', 'ဇဲ့ကျောင်း', 'ចឺជៀង', '절강'],
}

# Reverse mapping from alias to standard name (Latin + Chinese + per-language transliterations)
PROVINCE_NORMALIZATION_MAP = {
    alias: std_name for std_name, aliases in PROVINCE_ALIASES.items() for alias in aliases
}
for std_name, extra_aliases in LOCALIZED_PROVINCE_ALIASES.items():
    for alias in extra_aliases:
        # Don't overwrite an alias that already resolves to a different province
        # (this protects the hand-tuned shanxi/shaanxi disambiguation above).
        if alias not in PROVINCE_NORMALIZATION_MAP:
            PROVINCE_NORMALIZATION_MAP[alias] = std_name

# Region code mapping for each normalized province
REGION_MAP = {
    'beijing': 'NC', 'tianjin': 'NC', 'hebei': 'NC', 'shanxi': 'NC', 'inner mongolia': 'NC',
    'liaoning': 'NE', 'jilin': 'NE', 'heilongjiang': 'NE',
    'shanghai': 'EC', 'jiangsu': 'EC', 'zhejiang': 'EC', 'anhui': 'EC', 'fujian': 'EC', 'jiangxi': 'EC', 'shandong': 'EC',
    'henan': 'CC', 'hubei': 'CC', 'hunan': 'CC',
    'guangdong': 'SC', 'guangxi': 'SC', 'hainan': 'SC', 'hongkong': 'SC', 'macau': 'SC', 'taiwan': 'SC',
    'sichuan': 'SW', 'chongqing': 'SW', 'guizhou': 'SW', 'yunnan': 'SW', 'tibet': 'SW',
    'shaanxi': 'NW', 'gansu': 'NW', 'qinghai': 'NW', 'ningxia': 'NW', 'xinjiang': 'NW',
}

# Region-to-region base delivery days
BASE_REGION_TIME = {
    'NC': {'NC': 1, 'NE': 2, 'EC': 2, 'CC': 2, 'SC': 3, 'SW': 3, 'NW': 3},
    'NE': {'NC': 2, 'NE': 1, 'EC': 3, 'CC': 3, 'SC': 4, 'SW': 4, 'NW': 4},
    'EC': {'NC': 2, 'NE': 3, 'EC': 1, 'CC': 2, 'SC': 2, 'SW': 3, 'NW': 4},
    'CC': {'NC': 2, 'NE': 3, 'EC': 2, 'CC': 1, 'SC': 2, 'SW': 2, 'NW': 3},
    'SC': {'NC': 3, 'NE': 4, 'EC': 2, 'CC': 2, 'SC': 1, 'SW': 3, 'NW': 4},
    'SW': {'NC': 3, 'NE': 4, 'EC': 3, 'CC': 2, 'SC': 3, 'SW': 1, 'NW': 3},
    'NW': {'NC': 3, 'NE': 4, 'EC': 4, 'CC': 3, 'SC': 4, 'SW': 3, 'NW': 1},
}

# Provider-specific delivery day modifiers
PROVIDER_MODIFIERS = {
    'sf express': -2, 'sf': -2,
    'jd logistics': -1, 'jd': -1,
    'yto express': 1, 'yto': 0,
    'zto express': 1, 'zto': 0,
    'sto express': 1, 'sto': 0,
    'yunda express': 1, 'yunda': 0,
    'cainiao': 1,
    'china post': 2,
    'ems': 0,
    'deppon express': 0, 'deppon': 0,
    'default': 0
}

@register_tool('calculate_transport_time')
class CalculateTransportTimeTool(BaseShoppingTool):
    """
    Tool to estimate logistics delivery time between origin and destination provinces for a product.
    - Uses a hardcoded matrix of base days between regional districts.
    - Applies modifiers for delivery providers.
    - Final result is never less than 1 day.
    """

    LANG_FIELDS = {
        'en': {
            'product_not_found': lambda product_id: f"Product with ID '{product_id}' not found.",
            'shipping_origin_not_found': lambda product_id: f"Shipping origin not found for product '{product_id}'.",
            'cannot_determine_province': lambda address: f"Could not determine a valid province from origin address: '{address}'.",
            'cannot_determine_destination_province': lambda address: f"Could not determine a valid province from destination address: '{address}'.",
            'valid_province_required': "Please provide a valid Chinese province name.",
            'cannot_map_to_region': "Could not map provinces to geographical regions.",
        },
        'zh': {
            'product_not_found': lambda product_id: f"未找到 ID 为 '{product_id}' 的商品。",
            'shipping_origin_not_found': lambda product_id: f"商品 '{product_id}' 未设置发货地址。",
            'cannot_determine_province': lambda address: f"无法从发货地址 '{address}' 中识别出有效的省份。",
            'cannot_determine_destination_province': lambda address: f"无法从收货地址 '{address}' 中识别出有效的省份。",
            'valid_province_required': "请提供有效的中国省份名称。",
            'cannot_map_to_region': "无法将省份映射到地理区域。",
        },
    }

    def __init__(self, cfg: Dict = None):
        super().__init__(cfg)
        self.products_map: Dict[str, Dict] = {}
        default_db_path = os.path.join(
            os.path.dirname(__file__), '..', 'database', 'case_0', 'products.jsonl'
        )

        if self.cfg and 'database_path' in self.cfg and self.cfg['database_path']:
            db_path = Path(self.cfg['database_path']) / 'products.jsonl'
        else:
            db_path = default_db_path

        self._load_database(db_path)
        self.REGION_MAP = REGION_MAP
        self.BASE_REGION_TIME = BASE_REGION_TIME
        self.PROVIDER_MODIFIERS = PROVIDER_MODIFIERS
        self.PROVINCE_NORMALIZATION_MAP = PROVINCE_NORMALIZATION_MAP

    def _load_database(self, path: str):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        product = json.loads(line)
                        self.products_map[product['product_id']] = product
        except FileNotFoundError:
            pass
        except Exception:
            pass

    def _normalize_province(self, address_str: str) -> str:
        """Standardize input address string and map to normalized province name."""
        if not address_str:
            return None
        processed_str = (
            address_str.lower()
            .replace(' ', '')
            .replace('province', '')
            .replace('city', '')
        )
        if processed_str in self.PROVINCE_NORMALIZATION_MAP:
            return self.PROVINCE_NORMALIZATION_MAP[processed_str]
        for alias, std_name in self.PROVINCE_NORMALIZATION_MAP.items():
            if alias in processed_str:
                return std_name
        return None

    def call(self, params: Union[str, dict], **kwargs) -> str:
        try:
            params_dict = self._verify_json_format_args(params)
        except ValueError as e:
            return self.format_result_as_json({"error": str(e)})

        product_id = params_dict.get('product_id')
        destination_address = params_dict.get('destination_address')
        product = self.products_map.get(product_id)
        if not product:
            return self.format_result_as_json({"error": self.fields['product_not_found'](product_id)})

        shipping_info = product.get('shipping_info', {})
        origin_address = shipping_info.get('origin')
        provider = shipping_info.get('provider', 'default').lower()

        if not origin_address:
            return self.format_result_as_json({"error": self.fields['shipping_origin_not_found'](product_id)})

        origin_province = self._normalize_province(origin_address)
        destination_province = self._normalize_province(destination_address)

        if not origin_province:
            return self.format_result_as_json({"error": self.fields['cannot_determine_province'](origin_address)})
        if not destination_province:
            return self.format_result_as_json({"error": f"{self.fields['cannot_determine_destination_province'](destination_address)} {self.fields['valid_province_required']}"})

        origin_region = self.REGION_MAP.get(origin_province)
        dest_region = self.REGION_MAP.get(destination_province)

        if not origin_region or not dest_region:
            return self.format_result_as_json({"error": self.fields['cannot_map_to_region']})

        base_days = self.BASE_REGION_TIME[origin_region][dest_region]

        remote_provinces = ['tibet', 'xinjiang', 'qinghai', 'inner mongolia']
        if origin_province in remote_provinces or destination_province in remote_provinces:
            base_days += 2
            print(
                f"[Info] Special remote province detected: "
                f"{origin_province if origin_province in remote_provinces else destination_province}; extra delivery days applied."
            )

        modifier = self.PROVIDER_MODIFIERS.get(provider, self.PROVIDER_MODIFIERS['default'])
        estimated_days = base_days + modifier
        final_days = max(1, estimated_days)

        result = {
            "product_id": product_id,
            "origin": origin_address,
            "destination": destination_address,
            "estimated_delivery_days": final_days
        }

        return self.format_result_as_json(result)