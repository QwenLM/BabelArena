"""Tool schema definitions for the instore domain.

This file contains the descriptions and mappings for all tools decorated with @is_tool
in the InstoreTools class.
"""

from typing import Dict, Any
from vita.utils.schema_utils import create_tool_schema_manager

# Tool descriptions extracted from tools.py - Chinese version
TOOL_DESCRIPTIONS_ZH = {
    "instore_shop_search_recommend": {
        "description": "在到店场景下，用户（需求模糊，没明确表达具体套餐｜没有明确表达具体商家），需要结合用户个人喜好和商家标签等信息，推荐多个商家",
        "preconditions": "处于到店场景，获取商家相关的关键词",
        "postconditions": "返回商家列表，引导用户选择确定商家，商家确定后需要用户选择并确定套餐",
        "args": {
            "keywords": "描述商家的关键词"
        },
        "returns": "结构化输出的商家信息",
        "tool_type": "READ"
    },
    
    "instore_product_search_recommend": {
        "description": "在到店场景下，可以根据用户表达抽取出描述套餐的关键词，搜索或推荐多个套餐",
        "preconditions": "处于到店场景，套餐相关的关键词",
        "postconditions": "返回套餐列表，引导用户选择套餐并创建订单",
        "args": {
            "keywords": "描述套餐的关键词"
        },
        "returns": "结构化输出的套餐信息",
        "tool_type": "READ"
    },
    
    "create_instore_product_order": {
        "description": "到店订单提交",
        "preconditions": "处于到店场景，确定唯一一个店家id和一个或多个商品id",
        "postconditions": "返回订单信息（包含order_id），询问用户是否支付订单",
        "args": {
            "user_id": "用户id",
            "shop_id": "商家id",
            "product_id": "套餐id",
            "quantity": "数量"
        },
        "returns": "订单信息",
        "tool_type": "WRITE"
    },
    
    "pay_instore_order": {
        "description": "在到店场景下，上文有订单信息，用户表达支付完成，或者重新支付完成",
        "preconditions": "处于到店场景，用户表达完成支付操作，订单创建完成并进入支付环节｜用户表示重新支付",
        "postconditions": "返回支付结果信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "输出支付结果信息",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_order": {
        "description": "用户取消订单，或者用户取消支付。禁止对处于已取消状态的订单再次取消。",
        "preconditions": "处于到店场景，查询订单状态，确保订单状态为非cancelled",
        "postconditions": "返回取消订单结果信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "输出取消订单结果信息",
        "tool_type": "WRITE"
    },
    
    "instore_book": {
        "description": "座位预定 - 在选定商家后预定物理座位/桌位",
        "preconditions": "处于到店场景，确定唯一一个商家id，商家支持座位预定服务",
        "postconditions": "返回座位预定信息（包含book_id），如需要支付订座费，询问用户是否支付",
        "args": {
            "user_id": "用户id",
            "shop_id": "商家id",
            "time": "座位预定时间 格式: %Y-%m-%d %H:%M:%S",
            "customer_count": "座位预定人数，默认为1人"
        },
        "returns": "座位预定信息",
        "tool_type": "WRITE"
    },
    
    "pay_instore_book": {
        "description": "到店座位预定支付",
        "preconditions": "处于到店场景，确定唯一一个订座id",
        "postconditions": "返回支付结果信息",
        "args": {
            "book_id": "订座id"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_book": {
        "description": "到店取消订座",
        "preconditions": "处于到店场景，确定唯一一个订座id",
        "postconditions": "返回取消订座结果信息",
        "args": {
            "book_id": "订座id"
        },
        "returns": "取消订座结果信息",
        "tool_type": "WRITE"
    },
    
    "instore_reservation": {
        "description": "服务预约 - 在选定商家后预约服务时间点",
        "preconditions": "处于到店场景，确定唯一一个商家id，商家支持服务预约",
        "postconditions": "返回服务预约信息（包含reservation_id），通知用户按照约定时间到商家接受服务",
        "args": {
            "user_id": "用户id",
            "shop_id": "商家id",
            "time": "服务预约时间 格式: %Y-%m-%d %H:%M:%S",
            "customer_count": "服务预约人数，默认为1人"
        },
        "returns": "服务预约信息",
        "tool_type": "WRITE"
    },
    
    "instore_modify_reservation": {
        "description": "到店场景对查询到的预约消费信息进行修改",
        "preconditions": "处于到店场景，查询用户待修改预约消费订单，确定唯一一个reservation_id，用户修改预约消费的时间、人数",
        "postconditions": "输出修改后预约消费信息，通知用户按照约定时间到商家消费",
        "args": {
            "reservation_id": "预约消费id",
            "time": "修改后的预约消费时间 正确格式为 %Y-%m-%d %H:%M:%S",
            "customer_count": "修改后的预约消费人数"
        },
        "returns": "修改后的预约信息",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_reservation": {
        "description": "到店预约消费取消",
        "preconditions": "处于到店场景，确定唯一一个预约消费id",
        "postconditions": "返回取消预约消费结果信息",
        "args": {
            "reservation_id": "预约消费id"
        },
        "returns": "取消预约消费结果信息",
        "tool_type": "WRITE"
    },
    
    "get_instore_orders": {
        "description": "获取指定用户所有到店订单",
        "preconditions": "处于到店场景，需要查看所有到店订单",
        "postconditions": "返回所有到店订单的详细信息",
        "args": {
            "user_id": "用户id"
        },
        "returns": "当前用户所有到店订单的详细信息",
        "tool_type": "READ"
    },
    
    "get_instore_reservations": {
        "description": "获取指定用户所有到店预约消费",
        "preconditions": "处于到店场景，需要查看所有到店预约消费",
        "postconditions": "返回所有到店预约消费的详细信息",
        "args": {
            "user_id": "用户id"
        },
        "returns": "当前用户所有到店预约消费的详细信息",
        "tool_type": "READ"
    },
    
    "get_instore_books": {
        "description": "获取指定用户所有到店座位预定",
        "preconditions": "处于到店场景，需要查看所有到店座位预定",
        "postconditions": "返回所有到店座位预定的详细信息",
        "args": {
            "user_id": "用户id"
        },
        "returns": "当前用户所有到店座位预定的详细信息",
        "tool_type": "READ"
    },
    
    "search_instore_book": {
        "description": "查询用户的座位预定信息，当book_id为None时，返回用户所有座位预定，当book_id不为None时，返回指定座位预定",
        "preconditions": "处于到店场景，当book_id为None时，返回用户所有座位预定，当book_id不为None时，返回指定座位预定",
        "postconditions": "返回座位预定信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户id",
            "book_id": "座位预定id，可选参数，默认为None"
        },
        "returns": "座位预定信息，多个座位预定用换行符分隔",
        "tool_type": "READ"
    },
    
    "search_instore_reservation": {
        "description": "查询用户的预约消费信息",
        "preconditions": "处于到店场景，当reservation_id为None时，返回用户所有预约消费，当reservation_id不为None时，返回指定预约消费",
        "postconditions": "返回预约消费信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户id",
            "reservation_id": "预约消费id，可选参数，默认为None"
        },
        "returns": "预约消费信息，多个预约用换行符分隔",
        "tool_type": "READ"
    }
}

# Tool descriptions extracted from tools.py - English version
TOOL_DESCRIPTIONS_EN = {
    "instore_shop_search_recommend": {
        "description": "In instore consumption scenario, when user needs are vague (no clear expression of specific packages or specific merchants), need to recommend multiple merchants based on user preferences and merchant tags",
        "preconditions": "In instore consumption scenario, get merchant-related keywords",
        "postconditions": "Return merchant list, guide user to select and confirm merchant, after merchant is confirmed user needs to select and confirm package",
        "args": {
            "keywords": "Keywords describing merchants"
        },
        "returns": "Structured merchant information output",
        "tool_type": "READ"
    },
    
    "instore_product_search_recommend": {
        "description": "In instore scenario, can extract keywords describing packages from user expressions, search or recommend multiple packages",
        "preconditions": "In instore scenario, package-related keywords",
        "postconditions": "Return package list, guide user to select package and create order",
        "args": {
            "keywords": "Keywords describing packages"
        },
        "returns": "Structured package information output",
        "tool_type": "READ"
    },
    
    "create_instore_product_order": {
        "description": "Submit instore order",
        "preconditions": "In instore scenario, determine unique merchant id and one or more product ids",
        "postconditions": "Return order information (including order_id), ask user to confirm payment",
        "args": {
            "user_id": "User id",
            "shop_id": "Merchant id",
            "product_id": "Package id",
            "quantity": "Quantity"
        },
        "returns": "Order information",
        "tool_type": "WRITE"
    },
    
    "pay_instore_order": {
        "description": "In instore scenario, with order information above, user expresses payment completion or re-payment completion",
        "preconditions": "In instore scenario, user expresses completion of payment operation, order creation completed and enters payment phase | user indicates re-payment",
        "postconditions": "Return payment result information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Payment result information output",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_order": {
        "description": "User cancels order or user cancels payment. Prohibited from canceling orders that are already in cancelled status.",
        "preconditions": "In instore scenario, query order status, ensure order status is not cancelled",
        "postconditions": "Return order cancellation result information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Order cancellation result information output",
        "tool_type": "WRITE"
    },
    
    "instore_book": {
        "description": "Seat reservation - Reserve physical seats/tables after selecting merchant",
        "preconditions": "In instore scenario, determine unique merchant id, merchant supports seat reservation service",
        "postconditions": "Return seat reservation information (including book_id), if seat reservation fee is required, ask user to confirm payment",
        "args": {
            "user_id": "User id",
            "shop_id": "Merchant id",
            "time": "Seat reservation time format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Seat reservation customer count, default is 1 person"
        },
        "returns": "Seat reservation information",
        "tool_type": "WRITE"
    },
    
    "pay_instore_book": {
        "description": "Instore seat reservation payment",
        "preconditions": "In instore scenario, determine unique seat reservation id",
        "postconditions": "Return payment result information",
        "args": {
            "book_id": "Seat reservation id"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_book": {
        "description": "Cancel instore seat reservation",
        "preconditions": "In instore scenario, determine unique seat reservation id",
        "postconditions": "Return seat reservation cancellation result information",
        "args": {
            "book_id": "Seat reservation id"
        },
        "returns": "Seat reservation cancellation result information",
        "tool_type": "WRITE"
    },
    
    "instore_reservation": {
        "description": "Service reservation - Reserve service time after selecting merchant",
        "preconditions": "In instore scenario, determine unique merchant id, merchant supports reservation service",
        "postconditions": "Return reservation information (including reservation_id), notify user to arrive at merchant at agreed time to receive service",
        "args": {
            "user_id": "User id",
            "shop_id": "Merchant id",
            "time": "Service reservation time format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Service reservation customer count, default is 1 person"
        },
        "returns": "Service reservation information",
        "tool_type": "WRITE"
    },
    
    "instore_modify_reservation": {
        "description": "Modify instore reservation consumption information",
        "preconditions": "In instore scenario, query user's pending modification reservation consumption orders, determine unique reservation_id, user modifies reservation consumption time and customer count",
        "postconditions": "Output modified reservation consumption information, notify user to arrive at merchant at agreed time for consumption",
        "args": {
            "reservation_id": "Reservation id",
            "time": "New reservation consumption time format: %Y-%m-%d %H:%M:%S",
            "customer_count": "New reservation consumption customer count"
        },
        "returns": "Modified reservation consumption information",
        "tool_type": "WRITE"
    },
    
    "instore_cancel_reservation": {
        "description": "Cancel instore reservation consumption",
        "preconditions": "In instore scenario, determine unique reservation consumption id",
        "postconditions": "Return reservation consumption cancellation result information",
        "args": {
            "reservation_id": "Reservation consumption id"
        },
        "returns": "Reservation consumption cancellation result information",
        "tool_type": "WRITE"
    },
    
    "get_instore_orders": {
        "description": "Get all instore orders for specified user",
        "preconditions": "In instore scenario, need to view all instore orders",
        "postconditions": "Return detailed information of all instore orders",
        "args": {
            "user_id": "User id"
        },
        "returns": "Detailed information of all instore orders for current user",
        "tool_type": "READ"
    },
    
    "get_instore_reservations": {
        "description": "Get all instore reservation consumption for specified user",
        "preconditions": "In instore scenario, need to view all instore reservation consumption",
        "postconditions": "Return detailed information of all instore reservation consumption",
        "args": {
            "user_id": "User id"
        },
        "returns": "Detailed information of all instore reservation consumption for current user",
        "tool_type": "READ"
    },
    
    "get_instore_books": {
        "description": "Get all instore seat reservations for specified user",
        "preconditions": "In instore scenario, need to view all instore seat reservations",
        "postconditions": "Return detailed information of all instore seat reservations",
        "args": {
            "user_id": "User id"
        },
        "returns": "Detailed information of all instore seat reservations for current user",
        "tool_type": "READ"
    },
    
    "search_instore_book": {
        "description": "Query user's seat reservation information, when book_id is None, return all user seat reservations, when book_id is not None, return specified seat reservation",
        "preconditions": "In instore scenario, when book_id is None, return all user seat reservations, when book_id is not None, return specified seat reservation",
        "postconditions": "Return seat reservation information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User id",
            "book_id": "Seat reservation id, optional parameter, default is None"
        },
        "returns": "Seat reservation information, multiple seat reservations separated by newlines",
        "tool_type": "READ"
    },
    
    "search_instore_reservation": {
        "description": "Query user's reservation consumption information",
        "preconditions": "In instore scenario, when reservation_id is None, return all user reservation consumption, when reservation_id is not None, return specified reservation consumption",
        "postconditions": "Return reservation consumption information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User id",
            "reservation_id": "Reservation consumption id, optional parameter, default is None"
        },
        "returns": "Reservation consumption information, multiple reservations separated by newlines",
        "tool_type": "READ"
    }
}

# Tool descriptions - Telugu version
TOOL_DESCRIPTIONS_TE = {
    "instore_shop_search_recommend": {
        "description": "స్టోర్ సందర్భంలో, వినియోగదారు (అవసరాలు అస్పష్టంగా ఉన్నాయి, నిర్దిష్ట ప్యాకేజీని స్పష్టంగా పేర్కొనలేదు | నిర్దిష్ట మర్చంట్‌ను స్పష్టంగా పేర్కొనలేదు), వినియోగదారు వ్యక్తిగత ఇష్టాలు మరియు మర్చంట్ ట్యాగ్‌లు వంటి సమాచారాన్ని కలిపి, అనేక మర్చంట్‌లను సిఫార్సు చేయాలి",
        "preconditions": "స్టోర్ సందర్భంలో ఉండండి, మర్చంట్‌కు సంబంధించిన కీవర్డ్‌లను పొందండి",
        "postconditions": "మర్చంట్ జాబితాను తిరిగి ఇవ్వండి, వినియోగదారును మర్చంట్‌ను ఎంచుకుని నిర్ధారించమని గైడ్ చేయండి, మర్చంట్ నిర్ధారించిన తర్వాత వినియోగదారు ప్యాకేజీని ఎంచుకుని నిర్ధారించాలి",
        "args": {
            "keywords": "మర్చంట్‌ను వర్ణించే కీవర్డ్‌లు"
        },
        "returns": "నిర్మాణాత్మకంగా అవుట్‌పుట్ చేయబడిన మర్చంట్ సమాచారం",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "స్టోర్ సందర్భంలో, వినియోగదారు వ్యక్తీకరణ ఆధారంగా ప్యాకేజీలను వర్ణించే కీవర్డ్‌లను సేకరించి, అనేక ప్యాకేజీలను శోధించవచ్చు లేదా సిఫార్సు చేయవచ్చు",
        "preconditions": "స్టోర్ సందర్భంలో ఉండాలి, ప్యాకేజీకి సంబంధించిన కీవర్డ్‌లు",
        "postconditions": "ప్యాకేజీ జాబితాను తిరిగి ఇవ్వండి, వినియోగదారును ప్యాకేజీ ఎంచుకోవడానికి మరియు ఆర్డర్ సృష్టించడానికి మార్గనిర్దేశం చేయండి",
        "args": {
            "keywords": "ప్యాకేజీని వర్ణించే కీవర్డ్‌లు"
        },
        "returns": "నిర్మాణాత్మకంగా అవుట్‌పుట్ చేయబడిన ప్యాకేజీ సమాచారం",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "స్టోర్ ఆర్డర్ సమర్పణ",
        "preconditions": "స్టోర్ సందర్భంలో ఉండి, ఒక ప్రత్యేకమైన షాప్ ఐడీ మరియు ఒకటి లేదా అంతకంటే ఎక్కువ ఉత్పత్తి ఐడీలను నిర్ధారించండి",
        "postconditions": "ఆర్డర్ సమాచారాన్ని తిరిగి ఇవ్వండి (ఆర్డర్_ఐడీతో సహా), వినియోగదారు ఆర్డర్ చెల్లించాలా అని అడగండి",
        "args": {
            "user_id": "వినియోగదారు ఐడీ",
            "shop_id": "షాప్ ఐడీ",
            "product_id": "ప్యాకేజీ ఐడీ",
            "quantity": "పరిమాణం"
        },
        "returns": "ఆర్డర్ సమాచారం",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "దుకాణ సందర్భంలో, పైభాగంలో ఆర్డర్ సమాచారం ఉంటుంది, వినియోగదారుడు చెల్లింపు పూర్తయిందని లేదా మళ్లీ చెల్లింపు పూర్తయిందని వ్యక్తం చేస్తారు.",
        "preconditions": "దుకాణ సందర్భంలో ఉండాలి, వినియోగదారుడు చెల్లింపు పూర్తయిందని తెలియజేయాలి, ఆర్డర్ సృష్టించబడి చెల్లింపు దశలోకి వెళ్ళి ఉండాలి｜వినియోగదారుడు మళ్లీ చెల్లింపు చేస్తున్నట్లు సూచించాలి.",
        "postconditions": "చెల్లింపు ఫలిత సమాచారాన్ని తిరిగి ఇస్తుంది.",
        "args": {
            "order_id": "ఆర్డర్ ఐడి"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారాన్ని అవుట్‌పుట్ చేస్తుంది.",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "వినియోగదారు ఆర్డర్‌ను రద్దు చేయడం లేదా చెల్లింపును రద్దు చేయడం. ఇప్పటికే రద్దు చేయబడిన ఆర్డర్‌ను మళ్లీ రద్దు చేయకూడదు.",
        "preconditions": "స్టోర్ సందర్భంలో ఉండాలి, ఆర్డర్ స్థితిని తనిఖీ చేయాలి, ఆర్డర్ స్థితి రద్దు చేయబడలేదని నిర్ధారించుకోండి.",
        "postconditions": "ఆర్డర్ రద్దు ఫలిత సమాచారాన్ని తిరిగి ఇవ్వండి.",
        "args": {
            "order_id": "ఆర్డర్ ఐడి"
        },
        "returns": "ఆర్డర్ రద్దు ఫలిత సమాచారాన్ని అందించండి.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "సీటు రిజర్వేషన్ - ఎంచుకున్న మర్చంట్ తర్వాత భౌతిక సీట్లు/టేబుల్స్ బుక్ చేయండి",
        "preconditions": "దుకాణ సందర్భంలో ఉండాలి, ఒక ప్రత్యేకమైన మర్చంట్ ఐడి నిర్ధారించబడాలి, మర్చంట్ సీటు రిజర్వేషన్ సేవను అందించాలి",
        "postconditions": "సీటు రిజర్వేషన్ వివరాలను తిరిగి ఇవ్వండి (book_id కలిగి ఉంటుంది), ఒకవేళ బుకింగ్ రుసుము చెల్లించాల్సి వస్తే, వినియోగదారు చెల్లిస్తారా అని అడగండి",
        "args": {
            "user_id": "వినియోగదారు ఐడి",
            "shop_id": "మర్చంట్ ఐడి",
            "time": "సీటు రిజర్వేషన్ సమయం ఫార్మాట్: %Y-%m-%d %H:%M:%S",
            "customer_count": "సీటు రిజర్వేషన్ చేసే వ్యక్తుల సంఖ్య, డిఫాల్ట్‌గా 1 వ్యక్తి"
        },
        "returns": "సీటు రిజర్వేషన్ సమాచారం",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "స్టోర్ సీట్ బుకింగ్ చెల్లింపు",
        "preconditions": "స్టోర్‌కు వచ్చిన సందర్భంలో, ఒక ప్రత్యేక బుకింగ్ ఐడీని నిర్ధారించండి",
        "postconditions": "చెల్లింపు ఫలిత సమాచారాన్ని రిటర్న్ చేస్తుంది",
        "args": {
            "book_id": "బుకింగ్ ఐడీ"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "స్టోర్‌లో రిజర్వేషన్ రద్దు చేయడం",
        "preconditions": "స్టోర్‌కు వచ్చిన సందర్భంలో, ఒక ప్రత్యేకమైన రిజర్వేషన్ ఐడీని నిర్ధారించండి",
        "postconditions": "రిజర్వేషన్ రద్దు ఫలిత సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "book_id": "రిజర్వేషన్ ఐడీ"
        },
        "returns": "రిజర్వేషన్ రద్దు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "సేవ అపాయింట్‌మెంట్ - ఎంచుకున్న వ్యాపారి తర్వాత సేవ సమయాన్ని షెడ్యూల్ చేయండి",
        "preconditions": "స్టోర్‌కు వచ్చిన సందర్భంలో ఉండాలి, ఒక ప్రత్యేకమైన వ్యాపారి ఐడీని నిర్ధారించాలి, వ్యాపారి సేవ అపాయింట్‌మెంట్‌కు మద్దతు ఇవ్వాలి",
        "postconditions": "సేవ అపాయింట్‌మెంట్ సమాచారాన్ని తిరిగి ఇవ్వండి (reservation_id కలిగి), అంగీకరించిన సమయానికి సేవ పొందడానికి వ్యాపారి వద్దకు వెళ్లాలని వినియోగదారునికి తెలియజేయండి",
        "args": {
            "user_id": "వినియోగదారు ఐడీ",
            "shop_id": "వ్యాపారి ఐడీ",
            "time": "సేవ అపాయింట్‌మెంట్ సమయం ఫార్మాట్: %Y-%m-%d %H:%M:%S",
            "customer_count": "సేవ అపాయింట్‌మెంట్ చేసుకునే వ్యక్తుల సంఖ్య, డిఫాల్ట్‌గా 1 వ్యక్తి"
        },
        "returns": "సేవ అపాయింట్‌మెంట్ సమాచారం",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "స్టోర్ సందర్భంలో క్వెరీ చేయబడిన రిజర్వేషన్ వినియోగ సమాచారాన్ని సవరించండి",
        "preconditions": "స్టోర్ సందర్భంలో ఉండండి, సవరించాల్సిన వినియోగదారు రిజర్వేషన్ ఆర్డర్‌ను క్వెరీ చేయండి, ఒక ప్రత్యేకమైన reservation_id ని నిర్ధారించండి, వినియోగదారు రిజర్వేషన్ వినియోగ సమయం మరియు వ్యక్తుల సంఖ్యను సవరిస్తారు",
        "postconditions": "సవరించిన రిజర్వేషన్ వినియోగ సమాచారాన్ని అవుట్‌పుట్ చేయండి, అంగీకరించిన సమయంలో వ్యాపారానికి వినియోగించడానికి వినియోగదారుకు తెలియజేయండి",
        "args": {
            "reservation_id": "రిజర్వేషన్ వినియోగ ఐడి",
            "time": "సవరించిన రిజర్వేషన్ వినియోగ సమయం సరైన ఫార్మాట్ %Y-%m-%d %H:%M:%S",
            "customer_count": "సవరించిన రిజర్వేషన్ వినియోగదారుల సంఖ్య"
        },
        "returns": "సవరించిన రిజర్వేషన్ సమాచారం",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "స్టోర్ సందర్శన రిజర్వేషన్ రద్దు",
        "preconditions": "స్టోర్ సందర్శన సందర్భంలో ఉండి, ఒక ప్రత్యేకమైన రిజర్వేషన్ ఐడిని గుర్తించండి",
        "postconditions": "రిజర్వేషన్ రద్దు ఫలిత సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "reservation_id": "రిజర్వేషన్ ఐడి"
        },
        "returns": "రిజర్వేషన్ రద్దు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "నిర్దిష్ట వినియోగదారుని అన్ని స్టోర్ విజిట్ ఆర్డర్లను పొందండి",
        "preconditions": "స్టోర్ విజిట్ సందర్భంలో ఉన్నప్పుడు, అన్ని స్టోర్ విజిట్ ఆర్డర్లను వీక్షించాల్సిన అవసరం ఉన్నప్పుడు",
        "postconditions": "అన్ని స్టోర్ విజిట్ ఆర్డర్ల వివరణాత్మక సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "user_id": "వినియోగదారుని ఐడి"
        },
        "returns": "ప్రస్తుత వినియోగదారుని అన్ని స్టోర్ విజిట్ ఆర్డర్ల వివరణాత్మక సమాచారం",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "నిర్దిష్ట వినియోగదారు యొక్క అన్ని స్టోర్ విజిట్ అపాయింట్‌మెంట్ వినియోగాలను పొందండి",
        "preconditions": "స్టోర్ విజిట్ సందర్భంలో ఉన్నప్పుడు, అన్ని స్టోర్ విజిట్ అపాయింట్‌మెంట్ వినియోగాలను చూడాల్సిన అవసరం ఉన్నప్పుడు",
        "postconditions": "అన్ని స్టోర్ విజిట్ అపాయింట్‌మెంట్ వినియోగాల వివరణాత్మక సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "user_id": "వినియోగదారు ఐడి"
        },
        "returns": "ప్రస్తుత వినియోగదారు యొక్క అన్ని స్టోర్ విజిట్ అపాయింట్‌మెంట్ వినియోగాల వివరణాత్మక సమాచారం",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "నిర్దిష్ట వినియోగదారుని అన్ని స్టోర్ సీట్ రిజర్వేషన్లను పొందండి",
        "preconditions": "స్టోర్ సందర్భంలో ఉన్నప్పుడు, అన్ని స్టోర్ సీట్ రిజర్వేషన్లను చూడాల్సిన అవసరం ఉంది",
        "postconditions": "అన్ని స్టోర్ సీట్ రిజర్వేషన్ల వివరణాత్మక సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "user_id": "వినియోగదారుని ఐడి"
        },
        "returns": "ప్రస్తుత వినియోగదారుని అన్ని స్టోర్ సీట్ రిజర్వేషన్ల వివరణాత్మక సమాచారం",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "వినియోగదారు సీటు రిజర్వేషన్ సమాచారాన్ని విచారించండి. book_id None అయినప్పుడు, వినియోగదారుని అన్ని సీటు రిజర్వేషన్లను తిరిగి ఇవ్వండి; book_id None కానప్పుడు, నిర్దిష్ట సీటు రిజర్వేషన్‌ను తిరిగి ఇవ్వండి.",
        "preconditions": "స్టోర్‌కు వచ్చిన సందర్భంలో, book_id None అయినప్పుడు, వినియోగదారుని అన్ని సీటు రిజర్వేషన్లను తిరిగి ఇవ్వండి; book_id None కానప్పుడు, నిర్దిష్ట సీటు రిజర్వేషన్‌ను తిరిగి ఇవ్వండి.",
        "postconditions": "సీటు రిజర్వేషన్ సమాచారాన్ని తిరిగి ఇవ్వండి, తర్వాత సవరణ లేదా రద్దు చేయడానికి వీలుగా.",
        "args": {
            "user_id": "వినియోగదారుని ఐడి",
            "book_id": "సీటు రిజర్వేషన్ ఐడి, ఐచ్ఛిక పారామితి, డిఫాల్ట్‌గా None"
        },
        "returns": "సీటు రిజర్వేషన్ సమాచారం, అనేక సీటు రిజర్వేషన్లు న్యూలైన్‌తో వేరు చేయబడతాయి",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "వినియోగదారు యొక్క రిజర్వేషన్ వినియోగ సమాచారాన్ని విచారించండి",
        "preconditions": "దుకాణ సందర్భంలో ఉన్నప్పుడు, reservation_id None అయితే, వినియోగదారు యొక్క అన్ని రిజర్వేషన్ వినియోగాలను తిరిగి ఇస్తుంది; reservation_id None కాకపోతే, నిర్దిష్ట రిజర్వేషన్ వినియోగాన్ని తిరిగి ఇస్తుంది",
        "postconditions": "రిజర్వేషన్ వినియోగ సమాచారాన్ని తిరిగి ఇస్తుంది, తరువాత సవరణ లేదా రద్దు చేసుకోవడానికి వీలు కల్పిస్తుంది",
        "args": {
            "user_id": "వినియోగదారు ఐడి",
            "reservation_id": "రిజర్వేషన్ వినియోగ ఐడి, ఐచ్ఛిక పారామితి, డిఫాల్ట్ విలువ None"
        },
        "returns": "రిజర్వేషన్ వినియోగ సమాచారం, అనేక రిజర్వేషన్లు న్యూలైన్ క్యారెక్టర్లతో వేరు చేయబడతాయి",
        "tool_type": "READ"
    },
}

# Tool descriptions - Tamil version
TOOL_DESCRIPTIONS_TA = {
    "instore_shop_search_recommend": {
        "description": "கடைக்கு வரும் சூழலில், பயனரின் தேவைகள் தெளிவாக இல்லாதபோது (குறிப்பிட்ட தொகுப்பு அல்லது வணிகர் பற்றி தெளிவாகக் கூறாமல்), பயனரின் தனிப்பட்ட விருப்பங்கள் மற்றும் வணிகர் குறிச்சொற்கள் போன்ற தகவல்களை அடிப்படையாகக் கொண்டு பல வணிகர்களை பரிந்துரைக்க வேண்டும்.",
        "preconditions": "கடைக்கு வரும் சூழலில் இருத்தல், வணிகர் சார்ந்த முக்கிய வார்த்தைகளைப் பெறுதல்.",
        "postconditions": "வணிகர் பட்டியலைத் திருப்பி அனுப்பு, பயனரை வணிகரைத் தேர்ந்தெடுத்து உறுதிப்படுத்த வழிநடத்து, வணிகர் உறுதிப்படுத்தப்பட்ட பிறகு பயனர் தொகுப்பைத் தேர்ந்தெடுத்து உறுதிப்படுத்த வேண்டும்.",
        "args": {
            "keywords": "வணிகரை விவரிக்கும் முக்கிய வார்த்தைகள்"
        },
        "returns": "கட்டமைக்கப்பட்ட வெளியீடான வணிகர் தகவல்",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "கடைக்கு வரும் சூழலில், பயனர் கூற்றின் அடிப்படையில் தொகுப்புகளை விவரிக்கும் முக்கிய சொற்களை பிரித்தெடுத்து, பல தொகுப்புகளை தேடலாம் அல்லது பரிந்துரைக்கலாம்",
        "preconditions": "கடைக்கு வரும் சூழலில் இருத்தல், தொகுப்பு சார்ந்த முக்கிய சொற்கள்",
        "postconditions": "தொகுப்பு பட்டியலை திரும்ப அளித்தல், பயனரை தொகுப்பை தேர்ந்தெடுத்து ஆர்டர் உருவாக்க வழிநடத்துதல்",
        "args": {
            "keywords": "தொகுப்பை விவரிக்கும் முக்கிய சொற்கள்"
        },
        "returns": "கட்டமைக்கப்பட்ட வெளியீடாக தொகுப்பு தகவல்",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "கடையில் ஆர்டர் சமர்ப்பித்தல்",
        "preconditions": "கடை சூழலில் இருத்தல், தனித்துவமான கடை ஐடி மற்றும் ஒன்று அல்லது அதற்கு மேற்பட்ட பொருள் ஐடிக்களை உறுதி செய்தல்",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அனுப்பு (order_id உட்பட), பயனர் ஆர்டரை செலுத்த விரும்புகிறாரா எனக் கேட்கவும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "shop_id": "கடை ஐடி",
            "product_id": "தொகுப்பு ஐடி",
            "quantity": "எண்ணிக்கை"
        },
        "returns": "ஆர்டர் தகவல்",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "கடைக்கு வரும் சூழலில், முந்தைய உரையாடலில் ஆர்டர் தகவல் உள்ளது, பயனர் கட்டணம் செலுத்தி முடித்ததாக அல்லது மீண்டும் கட்டணம் செலுத்தி முடித்ததாக தெரிவிக்கிறார்",
        "preconditions": "கடைக்கு வரும் சூழலில் இருத்தல், பயனர் கட்டணம் செலுத்தி முடித்ததாக தெரிவித்தல், ஆர்டர் உருவாக்கப்பட்டு கட்டணம் செலுத்தும் நிலையில் இருத்தல்｜பயனர் மீண்டும் கட்டணம் செலுத்துவதாக தெரிவித்தல்",
        "postconditions": "கட்டண முடிவு தகவலைத் திருப்பி அனுப்புகிறது",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "கட்டண முடிவு தகவலை வெளியிடுகிறது",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "பயனர் ஆர்டரை ரத்து செய்கிறார், அல்லது பயனர் கட்டணத்தை ரத்து செய்கிறார். ஏற்கனவே ரத்து செய்யப்பட்ட நிலையில் உள்ள ஆர்டரை மீண்டும் ரத்து செய்வது தடைசெய்யப்பட்டுள்ளது.",
        "preconditions": "கடையை அடைந்த சூழலில், ஆர்டர் நிலையை விசாரிக்கவும், ஆர்டர் நிலை ரத்து செய்யப்படவில்லை என்பதை உறுதி செய்யவும்.",
        "postconditions": "ஆர்டர் ரத்து செய்வதற்கான முடிவு தகவலைத் திருப்பி அனுப்பவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் ரத்து செய்வதற்கான முடிவு தகவலை வெளியிடவும்",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "இருக்கை முன்பதிவு - தேர்ந்தெடுக்கப்பட்ட வணிகரிடம் நேரடி இருக்கை/மேசையை முன்பதிவு செய்யவும்",
        "preconditions": "கடையில் இருக்கும் சூழலில், தனித்துவமான வணிகர் ஐடியை உறுதி செய்யவும், வணிகர் இருக்கை முன்பதிவு சேவையை ஆதரிக்கிறார்",
        "postconditions": "இருக்கை முன்பதிவு தகவலைத் திருப்பி அனுப்பவும் (book_id உட்பட), இருக்கை முன்பதிவு கட்டணம் செலுத்த வேண்டியிருந்தால், பயனரிடம் செலுத்த வேண்டுமா என்று கேட்கவும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "shop_id": "வணிகர் ஐடி",
            "time": "இருக்கை முன்பதிவு நேரம் வடிவம்: %Y-%m-%d %H:%M:%S",
            "customer_count": "இருக்கை முன்பதிவு செய்யும் நபர்களின் எண்ணிக்கை, இயல்பாக 1 நபர்"
        },
        "returns": "இருக்கை முன்பதிவு தகவல்",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "கடையில் இருக்கை முன்பதிவு கட்டணம் செலுத்துதல்",
        "preconditions": "கடை சூழலில், தனித்துவமான முன்பதிவு ஐடியை உறுதிப்படுத்தவும்",
        "postconditions": "கட்டணம் செலுத்திய முடிவு தகவலைத் திருப்பி அனுப்பும்",
        "args": {
            "book_id": "முன்பதிவு ஐடி"
        },
        "returns": "கட்டணம் செலுத்திய முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "கடையில் இருக்கை முன்பதிவை ரத்து செய்தல்",
        "preconditions": "கடைக்கு வந்த சூழலில், தனித்துவமான இருக்கை முன்பதிவு ஐடியை உறுதி செய்யவும்",
        "postconditions": "இருக்கை முன்பதிவை ரத்து செய்ததற்கான முடிவு தகவலைத் திருப்பி அனுப்பும்",
        "args": {
            "book_id": "இருக்கை முன்பதிவு ஐடி"
        },
        "returns": "இருக்கை முன்பதிவை ரத்து செய்ததற்கான முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "சேவை முன்பதிவு - தேர்ந்தெடுக்கப்பட்ட விற்பனையாளருக்குப் பிறகு சேவை நேரத்தை முன்பதிவு செய்யவும்",
        "preconditions": "கடையை அடையும் சூழலில் இருத்தல், தனித்துவமான விற்பனையாளர் ஐடியை உறுதி செய்தல், விற்பனையாளர் சேவை முன்பதிவை ஆதரிக்கிறார்",
        "postconditions": "சேவை முன்பதிவு தகவலைத் திருப்பி அனுப்பவும் (reservation_id உள்ளிட்ட), ஒப்பந்த நேரத்தில் சேவையைப் பெற விற்பனையாளருக்குச் செல்ல பயனரை அறிவிக்கவும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "shop_id": "விற்பனையாளர் ஐடி",
            "time": "சேவை முன்பதிவு நேரம் வடிவம்: %Y-%m-%d %H:%M:%S",
            "customer_count": "சேவை முன்பதிவு நபர்கள் எண்ணிக்கை, இயல்பாக 1 நபர்"
        },
        "returns": "சேவை முன்பதிவு தகவல்",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "கடைக்கு வருகை தரும் சூழலில் விசாரிக்கப்பட்ட முன்பதிவு நுகர்வு தகவலை மாற்றவும்",
        "preconditions": "கடைக்கு வருகை தரும் சூழலில் இருக்க வேண்டும், பயனர் மாற்ற விரும்பும் முன்பதிவு நுகர்வு ஆர்டரை விசாரிக்க வேண்டும், தனித்துவமான reservation_id ஐ உறுதி செய்ய வேண்டும், பயனர் முன்பதிவு நுகர்வு நேரம் மற்றும் நபர்களின் எண்ணிக்கையை மாற்ற வேண்டும்",
        "postconditions": "மாற்றப்பட்ட முன்பதிவு நுகர்வு தகவலை வழங்கவும், ஒப்பந்த நேரத்தின்படி வணிக நிலையத்திற்கு நுகர்வு செய்ய பயனருக்கு அறிவிக்கவும்",
        "args": {
            "reservation_id": "முன்பதிவு நுகர்வு ஐடி",
            "time": "மாற்றப்பட்ட முன்பதிவு நுகர்வு நேரம் சரியான வடிவம் %Y-%m-%d %H:%M:%S",
            "customer_count": "மாற்றப்பட்ட முன்பதிவு நுகர்வு நபர்களின் எண்ணிக்கை"
        },
        "returns": "மாற்றப்பட்ட முன்பதிவு தகவல்",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "கடையில் முன்பதிவு செய்த நுகர்வை ரத்து செய்தல்",
        "preconditions": "கடை வருகை சூழலில் இருத்தல், தனித்துவமான முன்பதிவு நுகர்வு ஐடியை உறுதி செய்தல்",
        "postconditions": "முன்பதிவு நுகர்வு ரத்து முடிவு தகவலைத் திருப்பி அனுப்பு",
        "args": {
            "reservation_id": "முன்பதிவு நுகர்வு ஐடி"
        },
        "returns": "முன்பதிவு நுகர்வு ரத்து முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "குறிப்பிட்ட பயனரின் அனைத்து கடை வருகை ஆர்டர்களைப் பெறுக",
        "preconditions": "கடை வருகை சூழலில் இருக்கும் போது, அனைத்து கடை வருகை ஆர்டர்களையும் பார்க்க வேண்டும்",
        "postconditions": "அனைத்து கடை வருகை ஆர்டர்களின் விரிவான தகவல்களைத் திருப்பி அனுப்புக",
        "args": {
            "user_id": "பயனர் ஐடி"
        },
        "returns": "தற்போதைய பயனரின் அனைத்து கடை வருகை ஆர்டர்களின் விரிவான தகவல்கள்",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "குறிப்பிட்ட பயனரின் அனைத்து கடை வருகை முன்பதிவு நுகர்வுகளையும் பெறுக",
        "preconditions": "கடை வருகை சூழலில் இருக்கும் போது, அனைத்து கடை வருகை முன்பதிவு நுகர்வுகளையும் பார்க்க வேண்டும்",
        "postconditions": "அனைத்து கடை வருகை முன்பதிவு நுகர்வுகளின் விரிவான விவரங்களைத் திருப்பி அனுப்புக",
        "args": {
            "user_id": "பயனர் அடையாளம்"
        },
        "returns": "தற்போதைய பயனரின் அனைத்து கடை வருகை முன்பதிவு நுகர்வுகளின் விரிவான விவரங்கள்",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "குறிப்பிட்ட பயனரின் அனைத்து கடையில் இருக்கை முன்பதிவுகளைப் பெறுக",
        "preconditions": "கடையில் உள்ள சூழலில், அனைத்து கடையில் இருக்கை முன்பதிவுகளையும் பார்க்க வேண்டும்",
        "postconditions": "அனைத்து கடையில் இருக்கை முன்பதிவுகளின் விரிவான தகவல்களைத் திருப்பி அனுப்புக",
        "args": {
            "user_id": "பயனர் ஐடி"
        },
        "returns": "தற்போதைய பயனரின் அனைத்து கடையில் இருக்கை முன்பதிவுகளின் விரிவான தகவல்கள்",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "பயனரின் இருக்கை முன்பதிவு தகவலை விசாரிக்கவும். book_id None ஆக இருந்தால், பயனரின் அனைத்து இருக்கை முன்பதிவுகளையும் திரும்ப அளிக்கவும். book_id None இல்லையெனில், குறிப்பிட்ட இருக்கை முன்பதிவைத் திரும்ப அளிக்கவும்.",
        "preconditions": "கடையை அடைந்த சூழலில் இருக்க வேண்டும். book_id None ஆக இருந்தால், பயனரின் அனைத்து இருக்கை முன்பதிவுகளையும் திரும்ப அளிக்கவும். book_id None இல்லையெனில், குறிப்பிட்ட இருக்கை முன்பதிவைத் திரும்ப அளிக்கவும்.",
        "postconditions": "இருக்கை முன்பதிவு தகவலைத் திரும்ப அளிக்கிறது, பின்னர் மாற்றம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்.",
        "args": {
            "user_id": "பயனர் ஐடி",
            "book_id": "இருக்கை முன்பதிவு ஐடி, விருப்பமான அளவுரு, இயல்புநிலை None."
        },
        "returns": "இருக்கை முன்பதிவு தகவல், பல இருக்கை முன்பதிவுகள் புதிய வரி குறியீடு மூலம் பிரிக்கப்படும்.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "பயனரின் முன்பதிவு நுகர்வு தகவலை விசாரிக்கவும்",
        "preconditions": "கடையில் இருக்கும் சூழலில், reservation_id None ஆக இருந்தால், பயனரின் அனைத்து முன்பதிவு நுகர்வுகளையும் திருப்பி அனுப்பவும், reservation_id None அல்லாததாக இருந்தால், குறிப்பிட்ட முன்பதிவு நுகர்வைத் திருப்பி அனுப்பவும்",
        "postconditions": "முன்பதிவு நுகர்வு தகவலைத் திருப்பி அனுப்பவும், பின்னர் திருத்தம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "reservation_id": "முன்பதிவு நுகர்வு ஐடி, விருப்பமான அளவுரு, இயல்புநிலை None"
        },
        "returns": "முன்பதிவு நுகர்வு தகவல், பல முன்பதிவுகள் புதிய வரிக்குறியீட்டால் பிரிக்கப்படும்",
        "tool_type": "READ"
    },
}

# Tool descriptions - Lao version
TOOL_DESCRIPTIONS_LO = {
    "instore_shop_search_recommend": {
        "description": "ໃນສະຖານະການມາຮ້ານ, ຜູ້ໃຊ້ (ຄວາມຕ້ອງການບໍ່ຊັດເຈນ, ບໍ່ໄດ້ລະບຸຊຸດສະເພາະ ຫຼື ບໍ່ໄດ້ລະບຸຮ້ານຄ້າສະເພາະ), ຕ້ອງປະສານຄວາມມັກສ່ວນຕົວຂອງຜູ້ໃຊ້ ແລະ ແທັກຂອງຮ້ານຄ້າ ແລະ ຂໍ້ມູນອື່ນໆ ເພື່ອແນະນຳຫຼາຍຮ້ານຄ້າ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮ້ານ, ດຶງຂໍ້ມູນຄຳສຳຄັນທີ່ກ່ຽວຂ້ອງກັບຮ້ານຄ້າ",
        "postconditions": "ສົ່ງຄືນລາຍການຮ້ານຄ້າ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກ ແລະ ຢືນຢັນຮ້ານຄ້າ, ຫຼັງຈາກຢືນຢັນຮ້ານຄ້າແລ້ວ ຜູ້ໃຊ້ຕ້ອງເລືອກ ແລະ ຢືນຢັນຊຸດ",
        "args": {
            "keywords": "ຄຳສຳຄັນທີ່ອະທິບາຍກ່ຽວກັບຮ້ານຄ້າ"
        },
        "returns": "ຂໍ້ມູນຮ້ານຄ້າທີ່ສົ່ງອອກແບບໂຄງສ້າງ",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "ໃນສະຖານະການມາຮອດຮ້ານ, ສາມາດດຶງເອົາຄຳສຳຄັນທີ່ອະທິບາຍກ່ຽວກັບຊຸດອາຫານອອກຈາກຄຳເວົ້າຂອງຜູ້ໃຊ້, ເພື່ອຄົ້ນຫາ ຫຼື ແນະນຳຊຸດອາຫານຫຼາຍຊຸດ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຄຳສຳຄັນທີ່ກ່ຽວຂ້ອງກັບຊຸດອາຫານ",
        "postconditions": "ສົ່ງຄືນລາຍການຊຸດອາຫານ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກຊຸດອາຫານ ແລະ ສ້າງຄຳສັ່ງຊື້",
        "args": {
            "keywords": "ຄຳສຳຄັນທີ່ອະທິບາຍຊຸດອາຫານ"
        },
        "returns": "ຂໍ້ມູນຊຸດອາຫານທີ່ສົ່ງອອກແບບໂຄງສ້າງ",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "ການສົ່ງຄໍາສັ່ງຊື້ສິນຄ້າຢູ່ຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການຢູ່ຮ້ານ, ກໍານົດໄອດີຮ້ານຄ້າໜຶ່ງແຫ່ງ ແລະ ໄອດີສິນຄ້າໜຶ່ງ ຫຼື ຫຼາຍຢ່າງ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຄໍາສັ່ງຊື້ (ລວມທັງ order_id), ຖາມຜູ້ໃຊ້ວ່າຈະຊໍາລະຄ່າຄໍາສັ່ງຊື້ຫຼືບໍ່",
        "args": {
            "user_id": "ໄອດີຜູ້ໃຊ້",
            "shop_id": "ໄອດີຮ້ານຄ້າ",
            "product_id": "ໄອດີຊຸດສິນຄ້າ",
            "quantity": "ຈໍານວນ"
        },
        "returns": "ຂໍ້ມູນຄໍາສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "ໃນສະຖານະການຢູ່ຮ້ານ, ມີຂໍ້ມູນຄຳສັ່ງຢູ່ໃນບໍລິບົດກ່ອນໜ້າ, ຜູ້ໃຊ້ລະບຸວ່າຊຳລະເງິນສຳເລັດ, ຫຼື ຊຳລະເງິນຄືນໃໝ່ສຳເລັດ",
        "preconditions": "ຢູ່ໃນສະຖານະການຢູ່ຮ້ານ, ຜູ້ໃຊ້ສະແດງວ່າໄດ້ດຳເນີນການຊຳລະເງິນສຳເລັດ, ຄຳສັ່ງຖືກສ້າງສຳເລັດແລະເຂົ້າສູ່ຂັ້ນຕອນຊຳລະເງິນ｜ຜູ້ໃຊ້ລະບຸວ່າຕ້ອງການຊຳລະເງິນຄືນໃໝ່",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງ"
        },
        "returns": "ສະແດງຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄຳສັ່ງຊື້ ຫຼື ຍົກເລີກການຊຳລະເງິນ. ຫ້າມດຳເນີນການຍົກເລີກຄຳສັ່ງຊື້ທີ່ຖືກຍົກເລີກແລ້ວອີກຄັ້ງ.",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ກວດສອບສະຖານະຄຳສັ່ງຊື້, ຮັບປະກັນວ່າສະຖານະຄຳສັ່ງຊື້ບໍ່ແມ່ນຖືກຍົກເລີກ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຍົກເລີກຄຳສັ່ງຊື້",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງຊື້"
        },
        "returns": "ສະແດງຜົນຂໍ້ມູນຜົນການຍົກເລີກຄຳສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "ການຈອງທີ່ນັ່ງ - ຈອງທີ່ນັ່ງ/ໂຕະທາງກາຍະພາບຫຼັງຈາກເລືອກຮ້ານຄ້າ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮ້ານ, ກຳນົດໄອດີຮ້ານຄ້າໃຫ້ຊັດເຈນ, ຮ້ານຄ້າຮອງຮັບບໍລິການຈອງທີ່ນັ່ງ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນການຈອງທີ່ນັ່ງ (ລວມມີ book_id), ຖ້າຕ້ອງຈ່າຍຄ່າຈອງ, ຖາມຜູ້ໃຊ້ວ່າຈະຈ່າຍຫຼືບໍ່",
        "args": {
            "user_id": "ໄອດີຜູ້ໃຊ້",
            "shop_id": "ໄອດີຮ້ານຄ້າ",
            "time": "ເວລາຈອງທີ່ນັ່ງ ຮູບແບບ: %Y-%m-%d %H:%M:%S",
            "customer_count": "ຈຳນວນຄົນຈອງທີ່ນັ່ງ, ຄ່າເລີ່ມຕົ້ນແມ່ນ 1 ຄົນ"
        },
        "returns": "ຂໍ້ມູນການຈອງທີ່ນັ່ງ",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "ການຊໍາລະເງິນສໍາລັບການຈອງທີ່ນັ່ງຢູ່ຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຢືນຢັນໄອດີການຈອງທີ່ນັ່ງທີ່ເປັນເອກະລັກ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຊໍາລະເງິນ",
        "args": {
            "book_id": "ໄອດີການຈອງທີ່ນັ່ງ"
        },
        "returns": "ຂໍ້ມູນຜົນການຊໍາລະເງິນ",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "ຍົກເລີກການຈອງເມື່ອມາຮອດຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຢືນຢັນໄອດີການຈອງທີ່ເປັນເອກະລັກ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຍົກເລີກການຈອງ",
        "args": {
            "book_id": "ໄອດີການຈອງ"
        },
        "returns": "ຂໍ້ມູນຜົນການຍົກເລີກການຈອງ",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "ການນັດໝາຍບໍລິການ - ນັດໝາຍເວລາບໍລິການຫຼັງຈາກເລືອກຮ້ານຄ້າ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮ້ານ, ຢືນຢັນໄອດີຮ້ານຄ້າທີ່ຊັດເຈນ, ຮ້ານຄ້າຮອງຮັບການນັດໝາຍບໍລິການ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນການນັດໝາຍບໍລິການ (ລວມມີ reservation_id), ແຈ້ງໃຫ້ຜູ້ໃຊ້ໄປຮ້ານຄ້າຕາມເວລາທີ່ຕົກລົງເພື່ອຮັບບໍລິການ",
        "args": {
            "user_id": "ໄອດີຜູ້ໃຊ້",
            "shop_id": "ໄອດີຮ້ານຄ້າ",
            "time": "ເວລານັດໝາຍບໍລິການ ຮູບແບບ: %Y-%m-%d %H:%M:%S",
            "customer_count": "ຈຳນວນຄົນນັດໝາຍບໍລິການ, ຄ່າເລີ່ມຕົ້ນແມ່ນ 1 ຄົນ"
        },
        "returns": "ຂໍ້ມູນການນັດໝາຍບໍລິການ",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "ການແກ້ໄຂຂໍ້ມູນການຈອງບໍລິໂພກທີ່ຄົ້ນຫາໄດ້ໃນສະຖານະການມາຮອດຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຄົ້ນຫາໃບສັ່ງຈອງບໍລິໂພກຂອງຜູ້ໃຊ້ທີ່ລໍຖ້າການແກ້ໄຂ, ກຳນົດ reservation_id ທີ່ມີຄ່າດຽວ, ຜູ້ໃຊ້ແກ້ໄຂເວລາ ແລະ ຈຳນວນຄົນຂອງການຈອງບໍລິໂພກ",
        "postconditions": "ສະແດງຂໍ້ມູນການຈອງບໍລິໂພກຫຼັງຈາກແກ້ໄຂ, ແຈ້ງເຕືອນຜູ້ໃຊ້ໃຫ້ມາບໍລິໂພກທີ່ຮ້ານຕາມເວລາທີ່ຕົກລົງກັນ",
        "args": {
            "reservation_id": "ລະຫັດການຈອງບໍລິໂພກ",
            "time": "ເວລາການຈອງບໍລິໂພກຫຼັງຈາກແກ້ໄຂ ຮູບແບບທີ່ຖືກຕ້ອງແມ່ນ %Y-%m-%d %H:%M:%S",
            "customer_count": "ຈຳນວນຄົນການຈອງບໍລິໂພກຫຼັງຈາກແກ້ໄຂ"
        },
        "returns": "ຂໍ້ມູນການຈອງຫຼັງຈາກແກ້ໄຂ",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ການຍົກເລີກການຈອງບໍລິໂພກໃນຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການໃນຮ້ານ, ກຳນົດໄອດີການຈອງບໍລິໂພກໃຫ້ໄດ້ຢ່າງຊັດເຈນພຽງອັນດຽວ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຍົກເລີກການຈອງບໍລິໂພກ",
        "args": {
            "reservation_id": "ໄອດີການຈອງບໍລິໂພກ"
        },
        "returns": "ຂໍ້ມູນຜົນການຍົກເລີກການຈອງບໍລິໂພກ",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "ດຶງຂໍ້ມູນຄຳສັ່ງຊື້ທັງໝົດຂອງຜູ້ໃຊ້ທີ່ກຳນົດໄວ້ທີ່ມາຮອດຮ້ານ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຕ້ອງການເບິ່ງຄຳສັ່ງຊື້ທັງໝົດທີ່ມາຮອດຮ້ານ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຄຳສັ່ງຊື້ທັງໝົດທີ່ມາຮອດຮ້ານ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງຄຳສັ່ງຊື້ທັງໝົດທີ່ມາຮອດຮ້ານຂອງຜູ້ໃຊ້ປະຈຸບັນ",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "ດຶງຂໍ້ມູນລາຍການບໍລິໂພກຈາກການນັດໝາຍມາຮ້ານທັງໝົດຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮ້ານ, ຕ້ອງການເບິ່ງລາຍການບໍລິໂພກຈາກການນັດໝາຍມາຮ້ານທັງໝົດ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງລາຍການບໍລິໂພກຈາກການນັດໝາຍມາຮ້ານທັງໝົດ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງລາຍການບໍລິໂພກຈາກການນັດໝາຍມາຮ້ານທັງໝົດຂອງຜູ້ໃຊ້ປະຈຸບັນ",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "ກູ້ຂໍ້ມູນການຈອງທີ່ນັ່ງໃນຮ້ານທັງໝົດຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮ້ານ, ຕ້ອງການເບິ່ງການຈອງທີ່ນັ່ງໃນຮ້ານທັງໝົດ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງການຈອງທີ່ນັ່ງໃນຮ້ານທັງໝົດ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງການຈອງທີ່ນັ່ງໃນຮ້ານທັງໝົດຂອງຜູ້ໃຊ້ປະຈຸບັນ",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "ສືບຄົ້ນຂໍ້ມູນການຈອງທີ່ນັ່ງຂອງຜູ້ໃຊ້, ຖ້າ book_id ເປັນ None ຈະສົ່ງຄືນການຈອງທີ່ນັ່ງທັງໝົດຂອງຜູ້ໃຊ້, ຖ້າ book_id ບໍ່ແມ່ນ None ຈະສົ່ງຄືນການຈອງທີ່ນັ່ງທີ່ລະບຸ",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ຖ້າ book_id ເປັນ None ຈະສົ່ງຄືນການຈອງທີ່ນັ່ງທັງໝົດຂອງຜູ້ໃຊ້, ຖ້າ book_id ບໍ່ແມ່ນ None ຈະສົ່ງຄືນການຈອງທີ່ນັ່ງທີ່ລະບຸ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນການຈອງທີ່ນັ່ງ, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "book_id": "ລະຫັດການຈອງທີ່ນັ່ງ, ພາຣາມິເຕີເສີມ, ຄ່າເລີ່ມຕົ້ນແມ່ນ None"
        },
        "returns": "ຂໍ້ມູນການຈອງທີ່ນັ່ງ, ການຈອງທີ່ນັ່ງຫຼາຍອັນແຍກກັນດ້ວຍເສັ້ນໃໝ່",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "ສືບຄົ້ນຂໍ້ມູນການບໍລິໂພກການຈອງຂອງຜູ້ໃຊ້",
        "preconditions": "ຢູ່ໃນສະຖານະການມາຮອດຮ້ານ, ເມື່ອ reservation_id ເປັນ None, ຈະສົ່ງຄືນການບໍລິໂພກການຈອງທັງໝົດຂອງຜູ້ໃຊ້, ເມື່ອ reservation_id ບໍ່ແມ່ນ None, ຈະສົ່ງຄືນການບໍລິໂພກການຈອງທີ່ລະບຸ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນການບໍລິໂພກການຈອງ, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "reservation_id": "ລະຫັດການບໍລິໂພກການຈອງ, ພາຣາມິເຕີເສີມ, ຄ່າເລີ່ມຕົ້ນແມ່ນ None"
        },
        "returns": "ຂໍ້ມູນການບໍລິໂພກການຈອງ, ການຈອງຫຼາຍອັນແຍກກັນດ້ວຍຕົວອັກສອນຂັ້ນບັນທັດໃໝ່",
        "tool_type": "READ"
    },
}

# Tool descriptions - Burmese version
TOOL_DESCRIPTIONS_MY = {
    "instore_shop_search_recommend": {
        "description": "ဆိုင်တွင်းဝန်ဆောင်မှု ပေးသည့်နေရာတွင် အသုံးပြုသူများ (လိုအပ်ချက် မရှင်းလင်းဘဲ သီးသန့်ပက်ကေ့ဂ် သို့မဟုတ် သီးသန့်ဆိုင်ကို ရှင်းရှင်းလင်းလင်း မဖော်ပြထားသော) အသုံးပြုသူ၏ ကိုယ်ပိုင်နှစ်သက်မှုများနှင့် ဆိုင်အမှတ်အသားများ စသည့် အချက်အလက်များကို ပေါင်းစပ်ကာ ဆိုင်အများအပြားကို အကြံပြုရန် လိုအပ်သည်။",
        "preconditions": "ဆိုင်တွင်းဝန်ဆောင်မှု ပေးသည့်နေရာတွင် ရှိနေပြီး ဆိုင်နှင့် သက်ဆိုင်သော သော့ချက်စာလုံးများကို ရယူထားသည်။",
        "postconditions": "ဆိုင်စာရင်းကို ပြန်လည်ပေးပို့ကာ အသုံးပြုသူအား ဆိုင်ကို ရွေးချယ်အတည်ပြုရန် လမ်းညွှန်သည်၊ ဆိုင် အတည်ပြုပြီးနောက် အသုံးပြုသူသည် ပက်ကေ့ဂ်ကို ရွေးချယ်ပြီး အတည်ပြုရန် လိုအပ်သည်။",
        "args": {
            "keywords": "ဆိုင်ကို ဖော်ပြသည့် သော့ချက်စာလုံးများ"
        },
        "returns": "ဆိုင်အချက်အလက်များကို စနစ်တကျ ဖွဲ့စည်းထားသော ထွက်ရှိမှု",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "ဆိုင်တွင်းရောက်ရှိနေသည့် အခြေအနေတွင် အသုံးပြုသူ၏ ပြောကြားချက်မှ အစုံလိုက်ကို ဖော်ပြသည့် သော့ချက်စာလုံးများကို ထုတ်ယူနိုင်ပြီး အစုံလိုက်များကို ရှာဖွေခြင်း သို့မဟုတ် အကြံပြုခြင်း ပြုလုပ်နိုင်သည်။",
        "preconditions": "ဆိုင်တွင်းရောက်ရှိနေသည့် အခြေအနေ၊ အစုံလိုက်နှင့် သက်ဆိုင်သည့် သော့ချက်စာလုံးများ",
        "postconditions": "အစုံလိုက် စာရင်းကို ပြန်လည်ပေးပို့ပြီး အသုံးပြုသူအား အစုံလိုက်ကို ရွေးချယ်ရန်နှင့် အော်ဒါပြုလုပ်ရန် လမ်းညွှန်သည်။",
        "args": {
            "keywords": "အစုံလိုက်ကို ဖော်ပြသည့် သော့ချက်စာလုံးများ"
        },
        "returns": "ဖွဲ့စည်းပုံအလိုက် ထုတ်ပေးသည့် အစုံလိုက် အချက်အလက်များ",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "ဆိုင်သို့လာရောက်အော်ဒါတင်သွင်းခြင်း",
        "preconditions": "ဆိုင်သို့လာရောက်သည့်အခြေအနေတွင်ရှိနေပြီး၊ ဆိုင်အိုင်ဒီတစ်ခုတည်းနှင့် ကုန်ပစ္စည်းအိုင်ဒီတစ်ခု သို့မဟုတ် တစ်ခုထက်ပိုသောအိုင်ဒီများကို အတည်ပြုထားရမည်။",
        "postconditions": "အော်ဒါအချက်အလက်များကို ပြန်လည်ပေးပို့မည် (order_id ပါဝင်သည်)၊ အသုံးပြုသူအား အော်ဒါကို ငွေချေမလားဟု မေးမြန်းမည်။",
        "args": {
            "user_id": "အသုံးပြုသူအိုင်ဒီ",
            "shop_id": "ဆိုင်အိုင်ဒီ",
            "product_id": "ပါကေးအိုင်ဒီ",
            "quantity": "အရေအတွက်"
        },
        "returns": "အော်ဒါအချက်အလက်များ",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "ဆိုင်တွင်းဝန်ဆောင်မှု အခြေအနေတွင်၊ အထက်တွင် အော်ဒါအချက်အလက်များရှိနေပြီး၊ အသုံးပြုသူက ငွေပေးချေမှု ပြီးဆုံးကြောင်း သို့မဟုတ် ပြန်လည်ငွေပေးချေမှု ပြီးဆုံးကြောင်း ပြောကြားသည့်အခါ",
        "preconditions": "ဆိုင်တွင်းဝန်ဆောင်မှု အခြေအနေတွင် ဖြစ်ရမည်၊ အသုံးပြုသူက ငွေပေးချေမှု လုပ်ဆောင်ချက် ပြီးဆုံးကြောင်း ပြောကြားသည်၊ အော်ဒါ ဖန်တီးပြီးဖြစ်ကာ ငွေပေးချေမှုအဆင့်သို့ ရောက်ရှိနေသည်｜အသုံးပြုသူက ပြန်လည်ငွေပေးချေကြောင်း ပြောကြားသည်",
        "postconditions": "ငွေပေးချေမှု ရလဒ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "order_id": "အော်ဒါအမှတ်"
        },
        "returns": "ငွေပေးချေမှု ရလဒ်အချက်အလက်ကို ထုတ်ပေးသည်",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "အသုံးပြုသူက အော်ဒါကို ပယ်ဖျက်ခြင်း သို့မဟုတ် ငွေပေးချေမှုကို ပယ်ဖျက်ခြင်း။ ပယ်ဖျက်ပြီးသား အနေအထားရှိ အော်ဒါများကို ထပ်မံပယ်ဖျက်ခွင့်မရှိပါ။",
        "preconditions": "ဆိုင်လာရောက်သည့် အခြေအနေတွင်၊ အော်ဒါအနေအထားကို စစ်ဆေးပြီး အော်ဒါအနေအထားသည် ပယ်ဖျက်ထားခြင်း မဟုတ်ကြောင်း သေချာစေရန်။",
        "postconditions": "အော်ဒါပယ်ဖျက်မှု ရလဒ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "အော်ဒါပယ်ဖျက်မှု ရလဒ်အချက်အလက်ကို ထုတ်ပေးသည်။",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "ထိုင်ခုံ ကြိုမှာခြင်း - ရွေးချယ်ထားသော ဆိုင်တွင် ရုပ်ပိုင်းဆိုင်ရာ ထိုင်ခုံ/စားပွဲကို ကြိုမှာခြင်း",
        "preconditions": "ဆိုင်သို့ ရောက်ရှိသည့် အခြေအနေတွင် ရှိနေရမည်၊ ဆိုင်အိုင်ဒီ တစ်ခုတည်းကို သေချာစွာ သတ်မှတ်ထားရမည်၊ ဆိုင်က ထိုင်ခုံ ကြိုမှာဝန်ဆောင်မှုကို ပံ့ပိုးပေးထားရမည်",
        "postconditions": "ထိုင်ခုံ ကြိုမှာအချက်အလက်ကို ပြန်လည်ပေးပို့မည် (book_id ပါဝင်သည်)၊ ထိုင်ခုံ ကြိုခကြေး ပေးသွင်းရန် လိုအပ်ပါက အသုံးပြုသူအား ပေးသွင်းမည် ဟုတ်မဟုတ် မေးမြန်းမည်",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "shop_id": "ဆိုင် အိုင်ဒီ",
            "time": "ထိုင်ခုံ ကြိုမှာသည့် အချိန် ပုံစံ - %Y-%m-%d %H:%M:%S",
            "customer_count": "ထိုင်ခုံ ကြိုမှာသည့် လူဦးရေ၊ ပုံမှန်အားဖြင့် ၁ ဦး"
        },
        "returns": "ထိုင်ခုံ ကြိုမှာအချက်အလက်",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "ဆိုင်တွင် ထိုင်ခုံကြိုမှာမှုအတွက် ငွေချေခြင်း",
        "preconditions": "ဆိုင်တွင်ရှိနေသော အခြေအနေဖြစ်ပြီး ထိုင်ခုံကြိုမှာမှု အိုင်ဒီတစ်ခုတည်းကို အတည်ပြုထားရမည်",
        "postconditions": "ငွေချေမှု ရလဒ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "book_id": "ထိုင်ခုံကြိုမှာမှု အိုင်ဒီ"
        },
        "returns": "ငွေချေမှု ရလဒ်အချက်အလက်",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "ဆိုင်သို့ရောက်ရှိချိန် ချိန်းဆိုမှုပယ်ဖျားခြင်း",
        "preconditions": "ဆိုင်သို့ရောက်ရှိသည့် အခြေအနေတွင်ရှိပြီး ထူးခြားသော ချိန်းဆိုမှု အိုင်ဒီကို သေချာစွာ သတ်မှတ်ထားရမည်",
        "postconditions": "ချိန်းဆိုမှုပယ်ဖျားခြင်း ရလဒ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "book_id": "ချိန်းဆိုမှု အိုင်ဒီ"
        },
        "returns": "ချိန်းဆိုမှုပယ်ဖျားခြင်း ရလဒ်အချက်အလက်",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "ဝန်ဆောင်မှု ကြိုတင်မှာကြားခြင်း - ကုန်သည်ကို ရွေးချယ်ပြီးနောက် ဝန်ဆောင်မှု အချိန်ကို ကြိုတင်မှာကြားခြင်း",
        "preconditions": "ဆိုင်သို့ ရောက်ရှိသည့် အခြေအနေတွင်၊ တစ်ခုတည်းသော ကုန်သည် အိုင်ဒီကို အတည်ပြုရမည်၊ ကုန်သည်သည် ဝန်ဆောင်မှု ကြိုတင်မှာကြားခြင်းကို ပံ့ပိုးပေးသည်",
        "postconditions": "ဝန်ဆောင်မှု ကြိုတင်မှာကြားခြင်း အချက်အလက်ကို ပြန်လည်ပေးပို့သည် (reservation_id ပါဝင်သည်)၊ သဘောတူညီထားသော အချိန်တွင် ဝန်ဆောင်မှု လက်ခံရယူရန် ကုန်သည်ထံ သွားရောက်ရန် အသုံးပြုသူကို အကြောင်းကြားသည်",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "shop_id": "ကုန်သည် အိုင်ဒီ",
            "time": "ဝန်ဆောင်မှု ကြိုတင်မှာကြားသည့် အချိန် ပုံစံ - %Y-%m-%d %H:%M:%S",
            "customer_count": "ဝန်ဆောင်မှု ကြိုတင်မှာကြားသည့် လူဦးရေ၊ ပုံမှန်အားဖြင့် ၁ ဦး"
        },
        "returns": "ဝန်ဆောင်မှု ကြိုတင်မှာကြားခြင်း အချက်အလက်",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "ဆိုင်သို့ရောက်ရှိသော အခြေအနေတွင် ရှာဖွေတွေ့ရှိထားသည့် ကြိုတင်မှာယူမှု အချက်အလက်များကို ပြင်ဆင်ခြင်း",
        "preconditions": "ဆိုင်သို့ရောက်ရှိသော အခြေအနေတွင် ရှိနေပြီး၊ ပြင်ဆင်ရန်လိုအပ်သော အသုံးပြုသူ၏ ကြိုတင်မှာယူမှု အော်ဒါကို ရှာဖွေကာ၊ တစ်ခုတည်းသော reservation_id ကို သေချာစွာ သတ်မှတ်ပြီး၊ အသုံးပြုသူက ကြိုတင်မှာယူမှု အချိန်နှင့် လူဦးရေကို ပြင်ဆင်သည်",
        "postconditions": "ပြင်ဆင်ပြီးသော ကြိုတင်မှာယူမှု အချက်အလက်များကို ထုတ်ပေးပြီး၊ သဘောတူညီထားသော အချိန်အတိုင်း ဆိုင်သို့ သွားရောက် အသုံးပြုရန် အသုံးပြုသူအား အကြောင်းကြားသည်",
        "args": {
            "reservation_id": "ကြိုတင်မှာယူမှု အိုင်ဒီ",
            "time": "ပြင်ဆင်ပြီးသော ကြိုတင်မှာယူမှု အချိန်၊ မှန်ကန်သော ပုံစံမှာ %Y-%m-%d %H:%M:%S ဖြစ်သည်",
            "customer_count": "ပြင်ဆင်ပြီးသော ကြိုတင်မှာယူမှု လူဦးရေ"
        },
        "returns": "ပြင်ဆင်ပြီးသော ကြိုတင်မှာယူမှု အချက်အလက်",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ဆိုင်တွင် ကြိုတင်မှာကြားထားသော ဝန်ဆောင်မှုကို ပယ်ဖျားခြင်း",
        "preconditions": "ဆိုင်တွင် ရောက်ရှိနေသည့် အခြေအနေဖြစ်ပြီး ထူးခြားသော ကြိုတင်မှာကြားထားသော ဝန်ဆောင်မှု အိုင်ဒီကို သတ်မှတ်ထားရမည်",
        "postconditions": "ကြိုတင်မှာကြားထားသော ဝန်ဆောင်မှုကို ပယ်ဖျားခြင်း ရလဒ် အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "reservation_id": "ကြိုတင်မှာကြားထားသော ဝန်ဆောင်မှု အိုင်ဒီ"
        },
        "returns": "ကြိုတင်မှာကြားထားသော ဝန်ဆောင်မှုကို ပယ်ဖျားခြင်း ရလဒ် အချက်အလက်",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "သတ်မှတ်အသုံးပြုသူ၏ ဆိုင်လာရောက်မှု အော်ဒါအားလုံးကို ရယူရန်",
        "preconditions": "ဆိုင်လာရောက်မှု အခြေအနေတွင် ရှိနေပြီး ဆိုင်လာရောက်မှု အော်ဒါအားလုံးကို ကြည့်ရှုရန် လိုအပ်သောအခါ",
        "postconditions": "ဆိုင်လာရောက်မှု အော်ဒါအားလုံး၏ အသေးစိတ် အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "user_id": "အသုံးပြုသူ အမှတ်"
        },
        "returns": "လက်ရှိအသုံးပြုသူ၏ ဆိုင်လာရောက်မှု အော်ဒါအားလုံး၏ အသေးစိတ် အချက်အလက်များ",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ ဆိုင်လာရောက် ကြိုတင်မှာကြားမှု ကုန်သုံးမှုအားလုံးကို ရယူခြင်း",
        "preconditions": "ဆိုင်လာရောက်ခြင်း ဆိုင်ရာ အခြေအနေတွင် ရှိနေပြီး ဆိုင်လာရောက် ကြိုတင်မှာကြားမှု ကုန်သုံးမှုအားလုံးကို ကြည့်ရှုရန် လိုအပ်သည်",
        "postconditions": "ဆိုင်လာရောက် ကြိုတင်မှာကြားမှု ကုန်သုံးမှုအားလုံး၏ အသေးစိတ် အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "လက်ရှိအသုံးပြုသူ၏ ဆိုင်လာရောက် ကြိုတင်မှာကြားမှု ကုန်သုံးမှုအားလုံး၏ အသေးစိတ် အချက်အလက်များ",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ ဆိုင်တွင် စားသုံးရန် ထိုင်ခုံ ကြိုတင်မှာကြားမှု အားလုံးကို ရယူခြင်း",
        "preconditions": "ဆိုင်တွင် စားသုံးမှု ပုံစံတွင် ရှိနေပြီး ဆိုင်တွင် စားသုံးရန် ထိုင်ခုံ ကြိုတင်မှာကြားမှု အားလုံးကို ကြည့်ရှုရန် လိုအပ်သည်",
        "postconditions": "ဆိုင်တွင် စားသုံးရန် ထိုင်ခုံ ကြိုတင်မှာကြားမှု အားလုံး၏ အသေးစိတ် အချက်အလက်များကို ပြန်လည် ပေးပို့သည်",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "လက်ရှိ အသုံးပြုသူ၏ ဆိုင်တွင် စားသုံးရန် ထိုင်ခုံ ကြိုတင်မှာကြားမှု အားလုံး၏ အသေးစိတ် အချက်အလက်များ",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "အသုံးပြုသူ၏ နေရာကြိုမှာမှု အချက်အလက်ကို စစ်ဆေးရန်၊ book_id သည် None ဖြစ်ပါက အသုံးပြုသူ၏ နေရာကြိုမှာမှုအားလုံးကို ပြန်လည်ပေးပို့မည်၊ book_id သည် None မဟုတ်ပါက သတ်မှတ်ထားသော နေရာကြိုမှာမှုကို ပြန်လည်ပေးပို့မည်။",
        "preconditions": "ဆိုင်သို့ရောက်ရှိသော အခြေအနေတွင်၊ book_id သည် None ဖြစ်ပါက အသုံးပြုသူ၏ နေရာကြိုမှာမှုအားလုံးကို ပြန်လည်ပေးပို့မည်၊ book_id သည် None မဟုတ်ပါက သတ်မှတ်ထားသော နေရာကြိုမှာမှုကို ပြန်လည်ပေးပို့မည်။",
        "postconditions": "နေရာကြိုမှာမှု အချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်းအတွက် အဆင်ပြေစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "book_id": "နေရာကြိုမှာမှု အိုင်ဒီ၊ ရွေးချယ်စရာ ပါရာမီတာ၊ ပုံသေမှာ None ဖြစ်သည်"
        },
        "returns": "နေရာကြိုမှာမှု အချက်အလက်၊ နေရာကြိုမှာမှုများစွာကို မျဉ်းအသစ်စာသားဖြင့် ခွဲခြားထားသည်။",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "အသုံးပြုသူ၏ ကြိုတင်မှာကြားထားသည့် သုံးစွဲမှု အချက်အလက်များကို စစ်ဆေးရန်",
        "preconditions": "ဆိုင်သို့ ရောက်ရှိနေသည့် အခြေအနေတွင် ဖြစ်သည်။ reservation_id သည် None ဖြစ်ပါက အသုံးပြုသူ၏ ကြိုတင်မှာကြားထားသည့် သုံးစွဲမှု အားလုံးကို ပြန်လည်ပေးပို့ပြီး၊ reservation_id သည် None မဟုတ်ပါက သတ်မှတ်ထားသော ကြိုတင်မှာကြားမှုကို ပြန်လည်ပေးပို့သည်။",
        "postconditions": "ကြိုတင်မှာကြားထားသည့် သုံးစွဲမှု အချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး၊ နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်း ပြုလုပ်ရန် လွယ်ကူစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "reservation_id": "ကြိုတင်မှာကြားထားသည့် သုံးစွဲမှု အိုင်ဒီ၊ ရွေးချယ်စရာ ပါရာမီတာ၊ ပုံသေတန်ဖိုးမှာ None ဖြစ်သည်။"
        },
        "returns": "ကြိုတင်မှာကြားထားသည့် သုံးစွဲမှု အချက်အလက်၊ ကြိုတင်မှာကြားမှု တစ်ခုထက်ပိုပါက မျဉ်းသစ်ဖြင့် ခွဲခြားထားသည်။",
        "tool_type": "READ"
    },
}

# Tool descriptions - Khmer version
TOOL_DESCRIPTIONS_KM = {
    "instore_shop_search_recommend": {
        "description": "ក្នុងស្ថានភាពមកដល់ហាង អ្នកប្រើប្រាស់ (តម្រូវការមិនច្បាស់លាស់ មិនបានបញ្ជាក់ជាក់លាក់អំពីកញ្ចប់ ឬមិនបានបញ្ជាក់អាជីវកម្មជាក់លាក់) ត្រូវការផ្សំចំណង់ចំណូលចិត្តផ្ទាល់ខ្លួន និងស្លាកសញ្ញាអាជីវកម្មជាដើម ដើម្បីណែនាំអាជីវកម្មជាច្រើន។",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពមកដល់ហាង ទទួលបានពាក្យគន្លឹះដែលពាក់ព័ន្ធនឹងអាជីវកម្ម។",
        "postconditions": "ត្រឡប់បញ្ជីអាជីវកម្ម ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើស និងកំណត់អាជីវកម្ម បន្ទាប់ពីកំណត់អាជីវកម្មរួច អ្នកប្រើប្រាស់ត្រូវជ្រើសរើស និងកំណត់កញ្ចប់។",
        "args": {
            "keywords": "ពាក្យគន្លឹះដែលពិពណ៌នាអំពីអាជីវកម្ម។"
        },
        "returns": "ព័ត៌មានអាជីវកម្មដែលបានបង្ហាញជាលក្ខណៈរចនាសម្ព័ន្ធ។",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "ក្នុងបរិបទនៅហាង អាចដកស្រង់ពាក្យគន្លឹះដែលពិពណ៌នាអំពីកញ្ចប់ ផ្អែកលើការសម្តែងរបស់អ្នកប្រើប្រាស់ ដើម្បីស្វែងរក ឬណែនាំកញ្ចប់ជាច្រើន",
        "preconditions": "ស្ថិតក្នុងបរិបទនៅហាង ពាក្យគន្លឹះទាក់ទងនឹងកញ្ចប់",
        "postconditions": "ត្រឡប់បញ្ជីកញ្ចប់ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសកញ្ចប់ និងបង្កើតការកុម្ម៉ង់",
        "args": {
            "keywords": "ពាក្យគន្លឹះដែលពិពណ៌នាអំពីកញ្ចប់"
        },
        "returns": "ព័ត៌មានកញ្ចប់ដែលបានបង្ហាញជាលក្ខណៈរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "ការដាក់បញ្ជាទិញនៅហាង",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពនៅហាង កំណត់លេខសម្គាល់ហាងតែមួយ និងលេខសម្គាល់ផលិតផលមួយ ឬច្រើន",
        "postconditions": "ត្រឡប់ព័ត៌មានបញ្ជាទិញ (រួមមាន order_id) សួរអ្នកប្រើប្រាស់ថាតើចង់ទូទាត់បញ្ជាទិញឬអត់",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "shop_id": "លេខសម្គាល់ហាង",
            "product_id": "លេខសម្គាល់ឈុត",
            "quantity": "ចំនួន"
        },
        "returns": "ព័ត៌មានបញ្ជាទិញ",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "នៅក្នុងស្ថានភាពនៅហាង មានព័ត៌មានការកុម្ម៉ង់នៅខាងលើ អ្នកប្រើប្រាស់បញ្ជាក់ថាបានបង់ប្រាក់រួច ឬបានបង់ប្រាក់ឡើងវិញរួច",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពនៅហាង អ្នកប្រើប្រាស់បញ្ជាក់ថាបានបញ្ចប់ការបង់ប្រាក់ ការកុម្ម៉ង់ត្រូវបានបង្កើតរួច និងចូលដំណាក់កាលបង់ប្រាក់｜អ្នកប្រើប្រាស់បញ្ជាក់ថាចង់បង់ប្រាក់ឡើងវិញ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលការបង់ប្រាក់",
        "args": {
            "order_id": "លេខសម្គាល់ការកុម្ម៉ង់"
        },
        "returns": "បង្ហាញព័ត៌មានលទ្ធផលការបង់ប្រាក់",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកម្មង់ ឬលុបចោលការទូទាត់។ ហាមឃាត់ការលុបចោលការកម្មង់ដែលស្ថិតក្នុងស្ថានភាពបានលុបចោលរួចហើយម្តងទៀត។",
        "preconditions": "ក្នុងស្ថានភាពមកដល់ហាង ត្រូវពិនិត្យមើលស្ថានភាពការកម្មង់ ធានាថាស្ថានភាពការកម្មង់មិនត្រូវបានលុបចោល",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលនៃការលុបចោលការកម្មង់",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "បង្ហាញព័ត៌មានលទ្ធផលនៃការលុបចោលការកម្មង់",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "ការកក់កន្លែងអង្គុយ - កក់កន្លែងអង្គុយ ឬតុជាក់លាក់ បន្ទាប់ពីជ្រើសរើសហាង",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពមកដល់ហាង បញ្ជាក់លេខសម្គាល់ហាងតែមួយគត់ ហាងគាំទ្រសេវាកម្មកក់កន្លែងអង្គុយ",
        "postconditions": "ត្រឡប់ព័ត៌មានកក់កន្លែងអង្គុយ (រួមមាន book_id) ប្រសិនបើត្រូវការបង់ថ្លៃកក់ សួរអ្នកប្រើប្រាស់ថាតើត្រូវបង់ដែរឬទេ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "shop_id": "លេខសម្គាល់ហាង",
            "time": "ពេលវេលាកក់កន្លែងអង្គុយ ទម្រង់៖ %Y-%m-%d %H:%M:%S",
            "customer_count": "ចំនួនអ្នកកក់កន្លែងអង្គុយ លំនាំដើម 1 នាក់"
        },
        "returns": "ព័ត៌មានកក់កន្លែងអង្គុយ",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "ការទូទាត់ការកក់កន្លែងអង្គុយនៅហាង",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពនៅហាង ត្រូវកំណត់លេខសម្គាល់ការកក់កន្លែងអង្គុយតែមួយ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលការទូទាត់",
        "args": {
            "book_id": "លេខសម្គាល់ការកក់កន្លែងអង្គុយ"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "លុបចោលការកក់នៅហាង",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពដល់ហាង បញ្ជាក់លេខសម្គាល់ការកក់តែមួយគត់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលការលុបចោលការកក់",
        "args": {
            "book_id": "លេខសម្គាល់ការកក់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការលុបចោលការកក់",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "ការកក់សេវា - កក់ម៉ោងសេវាកម្មបន្ទាប់ពីជ្រើសរើសហាង",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពមកដល់ហាង កំណត់លេខសម្គាល់ហាងតែមួយគត់ ហាងគាំទ្រការកក់សេវា",
        "postconditions": "ត្រឡប់ព័ត៌មានការកក់សេវា (រួមមាន reservation_id) ជូនដំណឹងដល់អ្នកប្រើប្រាស់ឱ្យមកហាងតាមពេលវេលាកំណត់ដើម្បីទទួលសេវា",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "shop_id": "លេខសម្គាល់ហាង",
            "time": "ពេលវេលាកក់សេវា ទម្រង់: %Y-%m-%d %H:%M:%S",
            "customer_count": "ចំនួនអ្នកកក់សេវា លំនាំដើមគឺ 1 នាក់"
        },
        "returns": "ព័ត៌មានការកក់សេវា",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "កែសម្រួលព័ត៌មានការកក់ទទួលទានដែលបានស្វែងរកនៅក្នុងស្ថានភាពមកដល់ហាង",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពមកដល់ហាង ស្វែងរកពាក្យសុំកក់ទទួលទានរបស់អ្នកប្រើប្រាស់ដែលត្រូវកែសម្រួល កំណត់ reservation_id តែមួយគត់ អ្នកប្រើប្រាស់កែសម្រួលម៉ោង និងចំនួនអ្នកសម្រាប់ការកក់ទទួលទាន",
        "postconditions": "បង្ហាញព័ត៌មានការកក់ទទួលទានដែលបានកែសម្រួល ជូនដំណឹងដល់អ្នកប្រើប្រាស់ឱ្យមកទទួលទាននៅហាងតាមម៉ោងដែលបានកំណត់",
        "args": {
            "reservation_id": "លេខសម្គាល់ការកក់ទទួលទាន",
            "time": "ម៉ោងកក់ទទួលទានដែលបានកែសម្រួល ទម្រង់ត្រឹមត្រូវគឺ %Y-%m-%d %H:%M:%S",
            "customer_count": "ចំនួនអ្នកកក់ទទួលទានដែលបានកែសម្រួល"
        },
        "returns": "ព័ត៌មានការកក់ដែលបានកែសម្រួល",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ការលុបចោលការកក់សម្រាប់ការប្រើប្រាស់នៅកន្លែង",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពនៅកន្លែង កំណត់អត្តសញ្ញាណការកក់សម្រាប់ការប្រើប្រាស់តែមួយគត់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលនៃការលុបចោលការកក់សម្រាប់ការប្រើប្រាស់",
        "args": {
            "reservation_id": "អត្តសញ្ញាណការកក់សម្រាប់ការប្រើប្រាស់"
        },
        "returns": "ព័ត៌មានលទ្ធផលនៃការលុបចោលការកក់សម្រាប់ការប្រើប្រាស់",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "ទទួលបានការកម្មង់ទាំងអស់ដែលមកដល់ហាងរបស់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពមកដល់ហាង ត្រូវការមើលការកម្មង់ទាំងអស់ដែលមកដល់ហាង",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកម្មង់ទាំងអស់ដែលមកដល់ហាង",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការកម្មង់ទាំងអស់ដែលមកដល់ហាងរបស់អ្នកប្រើប្រាស់បច្ចុប្បន្ន",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "ទទួលបានការប្រើប្រាស់សេវាកម្មតាមការកក់ចូលហាងទាំងអស់របស់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "preconditions": "ស្ថិតក្នុងបរិបទចូលហាង ត្រូវការមើលការប្រើប្រាស់សេវាកម្មតាមការកក់ចូលហាងទាំងអស់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការប្រើប្រាស់សេវាកម្មតាមការកក់ចូលហាងទាំងអស់",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការប្រើប្រាស់សេវាកម្មតាមការកក់ចូលហាងទាំងអស់របស់អ្នកប្រើប្រាស់បច្ចុប្បន្ន",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "ទទួលបានការកក់កន្លែងអង្គុយនៅហាងទាំងអស់សម្រាប់អ្នកប្រើប្រាស់ជាក់លាក់",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពនៅហាង ត្រូវការមើលការកក់កន្លែងអង្គុយនៅហាងទាំងអស់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកក់កន្លែងអង្គុយនៅហាងទាំងអស់",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការកក់កន្លែងអង្គុយនៅហាងទាំងអស់សម្រាប់អ្នកប្រើប្រាស់បច្ចុប្បន្ន",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "ស្វែងរកព័ត៌មានការកក់កន្លែងអង្គុយរបស់អ្នកប្រើប្រាស់ នៅពេល book_id ស្មើនឹង None ត្រឡប់ការកក់កន្លែងអង្គុយទាំងអស់របស់អ្នកប្រើប្រាស់ នៅពេល book_id មិនស្មើនឹង None ត្រឡប់ការកក់កន្លែងអង្គុយដែលបានកំណត់",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពមកដល់ហាង នៅពេល book_id ស្មើនឹង None ត្រឡប់ការកក់កន្លែងអង្គុយទាំងអស់របស់អ្នកប្រើប្រាស់ នៅពេល book_id មិនស្មើនឹង None ត្រឡប់ការកក់កន្លែងអង្គុយដែលបានកំណត់",
        "postconditions": "ត្រឡប់ព័ត៌មានការកក់កន្លែងអង្គុយ ដើម្បីងាយស្រួលក្នុងការកែប្រែ ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "អត្តសញ្ញាណអ្នកប្រើប្រាស់",
            "book_id": "អត្តសញ្ញាណការកក់កន្លែងអង្គុយ ប៉ារ៉ាម៉ែត្រជម្រើស តម្លៃលំនាំដើមគឺ None"
        },
        "returns": "ព័ត៌មានការកក់កន្លែងអង្គុយ ការកក់កន្លែងអង្គុយច្រើនត្រូវបានបំបែកដោយនិមិត្តសញ្ញាបន្ទាត់ថ្មី",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "ស្វែងរកព័ត៌មានស្តីពីការកក់ និងការប្រើប្រាស់របស់អ្នកប្រើប្រាស់",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពមកដល់ហាង នៅពេលដែល reservation_id គឺ None ត្រឡប់មកវិញនូវការកក់ និងការប្រើប្រាស់ទាំងអស់របស់អ្នកប្រើប្រាស់ នៅពេលដែល reservation_id មិនមែនជា None ត្រឡប់មកវិញនូវការកក់ និងការប្រើប្រាស់ជាក់លាក់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានស្តីពីការកក់ និងការប្រើប្រាស់ ដើម្បីងាយស្រួលក្នុងការកែប្រែ ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "អត្តសញ្ញាណអ្នកប្រើប្រាស់",
            "reservation_id": "អត្តសញ្ញាណការកក់ និងការប្រើប្រាស់ ប៉ារ៉ាម៉ែត្រជម្រើស តម្លៃលំនាំដើមគឺ None"
        },
        "returns": "ព័ត៌មានស្តីពីការកក់ និងការប្រើប្រាស់ ការកក់ច្រើនត្រូវបានបំបែកដោយនិមិត្តសញ្ញាបន្ទាត់ថ្មី",
        "tool_type": "READ"
    },
}

# Tool descriptions - Kazakh version
TOOL_DESCRIPTIONS_KK = {
    "instore_shop_search_recommend": {
        "description": "Орынға бару сценарийінде пайдаланушының қажеттіліктері бұлыңғыр болса (нақты пакетті немесе нақты мекемені нақты көрсетпеген), пайдаланушының жеке қалаулары мен мекеме белгілері сияқты ақпаратты біріктіре отырып, бірнеше мекемені ұсыну қажет.",
        "preconditions": "Орынға бару сценарийінде болу, мекемеге қатысты кілт сөздерді алу",
        "postconditions": "Мекемелер тізімін қайтару, пайдаланушыны мекемені таңдауға және бекітуге бағыттау, мекеме бекітілген соң пайдаланушы пакетті таңдап, растауы тиіс",
        "args": {
            "keywords": "Мекемені сипаттайтын кілт сөздер"
        },
        "returns": "Мекеме ақпаратының құрылымдалған шығысы",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Дүкенге келу сценарийінде пайдаланушының сөздерінен пакетті сипаттайтын кілт сөздерді алып, бірнеше пакетті іздеуге немесе ұсынуға болады",
        "preconditions": "Дүкенге келу сценарийінде болу, пакетке қатысты кілт сөздер",
        "postconditions": "Пакеттер тізімін қайтару, пайдаланушыны пакетті таңдауға және тапсырыс жасауға бағыттау",
        "args": {
            "keywords": "Пакетті сипаттайтын кілт сөздер"
        },
        "returns": "Пакет ақпаратының құрылымдалған шығысы",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Дүкенге келу тапсырысын жіберу",
        "preconditions": "Дүкенге келу сценарийінде болу, бірегей дүкен идентификаторын және бір немесе бірнеше тауар идентификаторын анықтау",
        "postconditions": "Тапсырыс ақпаратын қайтару (order_id қамтиды), пайдаланушыдан тапсырысты төлеуді сұрау",
        "args": {
            "user_id": "Пайдаланушы идентификаторы",
            "shop_id": "Дүкен идентификаторы",
            "product_id": "Жиынтық идентификаторы",
            "quantity": "Саны"
        },
        "returns": "Тапсырыс ақпараты",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Дүкенге келу сценарийінде, контексте тапсырыс ақпараты бар, пайдаланушы төлемді аяқтағанын немесе қайта төлемді аяқтағанын хабарлайды",
        "preconditions": "Дүкенге келу сценарийінде, пайдаланушы төлем операциясын аяқтағанын білдіреді, тапсырыс жасалып, төлем кезеңіне өтті｜пайдаланушы қайта төлемді көрсетеді",
        "postconditions": "Төлем нәтижесі туралы ақпаратты қайтарады",
        "args": {
            "order_id": "Тапсырыс id-сы"
        },
        "returns": "Төлем нәтижесі туралы ақпаратты шығарады",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Пайдаланушы тапсырысты немесе төлемді жоққа шығарады. Жоққа шығарылған күйдегі тапсырысты қайта жоққа шығаруға тыйым салынады.",
        "preconditions": "Дүкенге келу сценарийінде тапсырыс күйін тексеру және тапсырыс күйінің 'cancelled' емес екеніне көз жеткізу.",
        "postconditions": "Тапсырысты жоққа шығару нәтижесі туралы ақпаратты қайтару.",
        "args": {
            "order_id": "Тапсырыс идентификаторы"
        },
        "returns": "Тапсырысты жоққа шығару нәтижесі туралы ақпаратты шығару.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Орын брондау - таңдалған мекемеден кейін нақты орынды/үстелді брондау",
        "preconditions": "Мекемеге бару сценарийінде, бірегей мекеме ID анықталған және мекеме орын брондау қызметін қолдайды",
        "postconditions": "Орын брондау ақпаратын қайтару (book_id қамтылған), егер брондау ақысын төлеу қажет болса, пайдаланушыдан төлеуді сұрау",
        "args": {
            "user_id": "Пайдаланушы ID",
            "shop_id": "Мекеме ID",
            "time": "Орын брондау уақыты Форматы: %Y-%m-%d %H:%M:%S",
            "customer_count": "Орын брондауға арналған адам саны, әдепкі бойынша 1 адам"
        },
        "returns": "Орын брондау ақпараты",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Мекемеге барып орын брондау үшін төлем жасау",
        "preconditions": "Мекемеге бару жағдайында болу және бірегей брондау идентификаторын анықтау",
        "postconditions": "Төлем нәтижесі туралы ақпаратты қайтару",
        "args": {
            "book_id": "Брондау идентификаторы"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Орынға келгенде брондауды жою",
        "preconditions": "Орынға келу жағдайында, бірегей брондау ID-сын анықтау",
        "postconditions": "Брондауды жою нәтижесі туралы ақпаратты қайтару",
        "args": {
            "book_id": "Брондау ID-сы"
        },
        "returns": "Брондауды жою нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Қызметке жазылу - Таңдалған дүкеннен кейін қызмет уақытын белгілеу",
        "preconditions": "Дүкенге бару сценарийінде, бірегей дүкен id анықталған, дүкен қызметке жазылуды қолдайды",
        "postconditions": "Қызметке жазылу ақпаратын қайтару (reservation_id қамтиды), пайдаланушыға келісілген уақытта қызмет алу үшін дүкенге бару туралы хабарлау",
        "args": {
            "user_id": "Пайдаланушы id",
            "shop_id": "Дүкен id",
            "time": "Қызметке жазылу уақыты Форматы: %Y-%m-%d %H:%M:%S",
            "customer_count": "Қызметке жазылу адам саны, әдепкі бойынша 1 адам"
        },
        "returns": "Қызметке жазылу ақпараты",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Дүкенге келу сценарийінде табылған брондау ақпаратын өзгерту",
        "preconditions": "Дүкенге келу сценарийінде болу, пайдаланушының өзгертуге тиіс брондау тапсырысын сұрау, бірегей reservation_id анықтау, пайдаланушы брондау уақыты мен қонақ санын өзгертеді",
        "postconditions": "Өзгертілген брондау ақпаратын шығару, пайдаланушыға келісілген уақытта дүкенге келу туралы хабарлау",
        "args": {
            "reservation_id": "Брондау идентификаторы",
            "time": "Өзгертілген брондау уақыты, дұрыс пішімі %Y-%m-%d %H:%M:%S",
            "customer_count": "Өзгертілген қонақ саны"
        },
        "returns": "Өзгертілген брондау ақпараты",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Дүкенге келу бойынша брондауды жою",
        "preconditions": "Дүкенге келу жағдайында, брондау тапсырысының бірегей ID-сын анықтау",
        "postconditions": "Брондауды жою нәтижесі туралы ақпарат қайтарылады",
        "args": {
            "reservation_id": "Брондау тапсырысының ID-сы"
        },
        "returns": "Брондауды жою нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Белгіленген пайдаланушының барлық дүкенге келу тапсырыстарын алу",
        "preconditions": "Дүкенге келу сценарийінде болу, барлық дүкенге келу тапсырыстарын қарау қажет",
        "postconditions": "Барлық дүкенге келу тапсырыстарының толық ақпаратын қайтару",
        "args": {
            "user_id": "Пайдаланушы идентификаторы"
        },
        "returns": "Ағымдағы пайдаланушының барлық дүкенге келу тапсырыстарының толық ақпараты",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Көрсетілген пайдаланушының дүкенге келу бойынша барлық алдын ала жазылған тұтыну деректерін алу",
        "preconditions": "Дүкенге келу сценарийінде болу, дүкенге келу бойынша барлық алдын ала жазылған тұтыну деректерін қарау қажет",
        "postconditions": "Дүкенге келу бойынша барлық алдын ала жазылған тұтыну деректерінің толық ақпаратын қайтару",
        "args": {
            "user_id": "Пайдаланушы идентификаторы"
        },
        "returns": "Ағымдағы пайдаланушының дүкенге келу бойынша барлық алдын ала жазылған тұтыну деректерінің толық ақпараты",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Көрсетілген пайдаланушының барлық дүкенге келу орындықтарын брондауын алу",
        "preconditions": "Дүкенге келу сценарийінде болу, барлық дүкенге келу орындықтарын брондауды көру қажет",
        "postconditions": "Барлық дүкенге келу орындықтарын брондаудың толық ақпаратын қайтару",
        "args": {
            "user_id": "Пайдаланушы идентификаторы"
        },
        "returns": "Ағымдағы пайдаланушының барлық дүкенге келу орындықтарын брондаудың толық ақпараты",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Пайдаланушының орын брондау ақпаратын сұрау. Егер book_id мәні None болса, пайдаланушының барлық орын брондаулары қайтарылады; егер book_id мәні None болмаса, белгіленген орын брондауы қайтарылады.",
        "preconditions": "Мекемеге келу сценарийінде. Егер book_id мәні None болса, пайдаланушының барлық орын брондаулары қайтарылады; егер book_id мәні None болмаса, белгіленген орын брондауы қайтарылады.",
        "postconditions": "Орын брондау ақпараты қайтарылады, кейінірек өзгерту немесе жою үшін ыңғайлы.",
        "args": {
            "user_id": "Пайдаланушы идентификаторы",
            "book_id": "Орын брондау идентификаторы, міндетті емес параметр, әдепкі мәні None"
        },
        "returns": "Орын брондау ақпараты, бірнеше орын брондауы жаңа жол таңбасымен бөлінген.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Пайдаланушының брондау және тұтыну ақпаратын сұрау",
        "preconditions": "Дүкенге келу сценарийінде. Егер reservation_id мәні None болса, пайдаланушының барлық брондау және тұтыну ақпараты қайтарылады; егер reservation_id мәні None болмаса, нақты бір брондау ақпараты қайтарылады.",
        "postconditions": "Брондау және тұтыну ақпаратын қайтарады, бұл кейінірек өзгерту немесе болдырмау үшін қолайлы.",
        "args": {
            "user_id": "Пайдаланушы ID-сы",
            "reservation_id": "Брондау және тұтыну ID-сы, қосымша параметр, әдепкі мәні None."
        },
        "returns": "Брондау және тұтыну ақпараты, бірнеше брондау жол ажыратқышымен бөлінген.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Punjabi version
TOOL_DESCRIPTIONS_PA = {
    "instore_shop_search_recommend": {
        "description": "ਸਟੋਰ 'ਤੇ ਜਾਣ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਵਰਤੋਂਕਾਰ (ਲੋੜਾਂ ਅਸਪਸ਼ਟ ਹਨ, ਖਾਸ ਪੈਕੇਜ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਜ਼ਾਹਰ ਨਹੀਂ ਕੀਤਾ | ਖਾਸ ਵਿਕਰੇਤਾ ਸਪਸ਼ਟ ਤੌਰ 'ਤੇ ਜ਼ਾਹਰ ਨਹੀਂ ਕੀਤਾ), ਵਰਤੋਂਕਾਰ ਦੀਆਂ ਨਿੱਜੀ ਪਸੰਦਾਂ ਅਤੇ ਵਿਕਰੇਤਾ ਟੈਗਾਂ ਵਰਗੀ ਜਾਣਕਾਰੀ ਦੇ ਆਧਾਰ 'ਤੇ, ਕਈ ਵਿਕਰੇਤਾਵਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰਨ ਦੀ ਲੋੜ ਹੈ",
        "preconditions": "ਸਟੋਰ 'ਤੇ ਜਾਣ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਵਿਕਰੇਤਾਵਾਂ ਨਾਲ ਸਬੰਧਤ ਕੀਵਰਡ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਵਿਕਰੇਤਾਵਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਵਰਤੋਂਕਾਰ ਨੂੰ ਵਿਕਰੇਤਾ ਚੁਣਨ ਅਤੇ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ, ਵਿਕਰੇਤਾ ਦੀ ਪੁਸ਼ਟੀ ਹੋਣ ਤੋਂ ਬਾਅਦ ਵਰਤੋਂਕਾਰ ਨੂੰ ਪੈਕੇਜ ਚੁਣਨ ਅਤੇ ਪੁਸ਼ਟੀ ਕਰਨ ਦੀ ਲੋੜ ਹੈ",
        "args": {
            "keywords": "ਵਿਕਰੇਤਾ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਕੀਵਰਡ"
        },
        "returns": "ਢਾਂਚਾਗਤ ਆਉਟਪੁਟ ਵਿਕਰੇਤਾ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਦੇ ਕਥਨ ਦੇ ਆਧਾਰ 'ਤੇ ਪੈਕੇਜ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ ਕੱਢੇ ਜਾ ਸਕਦੇ ਹਨ, ਅਤੇ ਕਈ ਪੈਕੇਜਾਂ ਦੀ ਖੋਜ ਜਾਂ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾ ਸਕਦੀ ਹੈ।",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਪੈਕੇਜ ਨਾਲ ਸਬੰਧਤ ਮੁੱਖ ਸ਼ਬਦ",
        "postconditions": "ਪੈਕੇਜਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਪੈਕੇਜ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਬਣਾਉਣ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ",
        "args": {
            "keywords": "ਪੈਕੇਜ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ"
        },
        "returns": "ਢਾਂਚਾਗਤ ਆਉਟਪੁੱਟ ਪੈਕੇਜ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "ਦੁਕਾਨ ਆਰਡਰ ਸਬਮਿਟ ਕਰਨਾ",
        "preconditions": "ਦੁਕਾਨ ਦੇ ਸਥਾਨ 'ਤੇ, ਇੱਕ ਵਿਲੱਖਣ ਦੁਕਾਨ ਆਈਡੀ ਅਤੇ ਇੱਕ ਜਾਂ ਇੱਕ ਤੋਂ ਵੱਧ ਉਤਪਾਦ ਆਈਡੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ।",
        "postconditions": "ਆਰਡਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ (order_id ਸਮੇਤ), ਉਪਭੋਗਤਾ ਨੂੰ ਪੁੱਛੋ ਕਿ ਕੀ ਉਹ ਆਰਡਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹਨ।",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ",
            "shop_id": "ਦੁਕਾਨ ਆਈਡੀ",
            "product_id": "ਪੈਕੇਜ ਆਈਡੀ",
            "quantity": "ਮਾਤਰਾ"
        },
        "returns": "ਆਰਡਰ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਜਾਣਕਾਰੀ ਹੈ, ਉਪਭੋਗਤਾ ਭੁਗਤਾਨ ਪੂਰਾ ਹੋਣ ਜਾਂ ਮੁੜ ਭੁਗਤਾਨ ਪੂਰਾ ਹੋਣ ਦਾ ਇਸ਼ਾਰਾ ਕਰਦਾ ਹੈ।",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਭੁਗਤਾਨ ਕਾਰਵਾਈ ਪੂਰੀ ਕਰਨ ਦਾ ਪ੍ਰਗਟਾਵਾ ਕਰਦਾ ਹੈ, ਆਰਡਰ ਬਣਾਇਆ ਗਿਆ ਹੈ ਅਤੇ ਭੁਗਤਾਨ ਪੜਾਅ ਵਿੱਚ ਦਾਖਲ ਹੋ ਗਿਆ ਹੈ | ਉਪਭੋਗਤਾ ਮੁੜ ਭੁਗਤਾਨ ਦਾ ਇਸ਼ਾਰਾ ਕਰਦਾ ਹੈ।",
        "postconditions": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਆਉਟਪੁਟ ਕਰੋ।",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਆਰਡਰ ਰੱਦ ਕਰਦਾ ਹੈ, ਜਾਂ ਵਰਤੋਂਕਾਰ ਭੁਗਤਾਨ ਰੱਦ ਕਰਦਾ ਹੈ। ਪਹਿਲਾਂ ਹੀ ਰੱਦ ਕੀਤੇ ਗਏ ਆਰਡਰ ਨੂੰ ਦੁਬਾਰਾ ਰੱਦ ਕਰਨਾ ਮਨ੍ਹਾ ਹੈ।",
        "preconditions": "ਸਟੋਰ ਆਗਮਨ ਸਥਿਤੀ ਵਿੱਚ, ਆਰਡਰ ਸਥਿਤੀ ਦੀ ਜਾਂਚ ਕਰੋ, ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਆਰਡਰ ਸਥਿਤੀ 'cancelled' ਨਹੀਂ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੀ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੀ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਆਉਟਪੁੱਟ ਕਰੋ।",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "ਸੀਟ ਬੁਕਿੰਗ - ਚੁਣੇ ਗਏ ਸਟੋਰ ਤੋਂ ਬਾਅਦ ਭੌਤਿਕ ਸੀਟ/ਟੇਬਲ ਬੁੱਕ ਕਰੋ",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਇੱਕ ਵਿਲੱਖਣ ਸਟੋਰ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕਰੋ, ਸਟੋਰ ਸੀਟ ਬੁਕਿੰਗ ਸੇਵਾਵਾਂ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ",
        "postconditions": "ਸੀਟ ਬੁਕਿੰਗ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ (book_id ਸਮੇਤ), ਜੇਕਰ ਬੁਕਿੰਗ ਫੀਸ ਦਾ ਭੁਗਤਾਨ ਕਰਨ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਉਪਭੋਗਤਾ ਨੂੰ ਪੁੱਛੋ ਕਿ ਕੀ ਉਹ ਭੁਗਤਾਨ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹਨ",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ",
            "shop_id": "ਸਟੋਰ ਆਈਡੀ",
            "time": "ਸੀਟ ਬੁਕਿੰਗ ਸਮਾਂ ਫਾਰਮੈਟ: %Y-%m-%d %H:%M:%S",
            "customer_count": "ਸੀਟ ਬੁਕਿੰਗ ਲਈ ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ, ਮੂਲ ਰੂਪ ਵਿੱਚ 1 ਵਿਅਕਤੀ"
        },
        "returns": "ਸੀਟ ਬੁਕਿੰਗ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "ਸਟੋਰ 'ਤੇ ਸੀਟ ਰਿਜ਼ਰਵੇਸ਼ਨ ਭੁਗਤਾਨ",
        "preconditions": "ਸਟੋਰ ਮਾਹੌਲ ਵਿੱਚ, ਇੱਕ ਵਿਲੱਖਣ ਬੁਕਿੰਗ ਆਈਡੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ",
        "postconditions": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "book_id": "ਬੁਕਿੰਗ ਆਈਡੀ"
        },
        "returns": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "ਦੁਕਾਨ 'ਤੇ ਬੁਕਿੰਗ ਰੱਦ ਕਰਨਾ",
        "preconditions": "ਦੁਕਾਨ 'ਤੇ ਹਾਜ਼ਰ ਹੋਣ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਇੱਕ ਅਨੋਖੀ ਬੁਕਿੰਗ ਆਈਡੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ",
        "postconditions": "ਬੁਕਿੰਗ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "book_id": "ਬੁਕਿੰਗ ਆਈਡੀ"
        },
        "returns": "ਬੁਕਿੰਗ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ - ਚੁਣੇ ਗਏ ਸਟੋਰ ਤੋਂ ਬਾਅਦ ਸੇਵਾ ਦਾ ਸਮਾਂ ਬੁੱਕ ਕਰੋ",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਇੱਕ ਵਿਲੱਖਣ ਸਟੋਰ ID ਦੀ ਪਛਾਣ ਕਰੋ, ਸਟੋਰ ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ",
        "postconditions": "ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ (reservation_id ਸਮੇਤ), ਵਰਤੋਂਕਾਰ ਨੂੰ ਸਹਿਮਤ ਸਮੇਂ 'ਤੇ ਸੇਵਾ ਲੈਣ ਲਈ ਸਟੋਰ ਜਾਣ ਬਾਰੇ ਸੂਚਿਤ ਕਰੋ",
        "args": {
            "user_id": "ਵਰਤੋਂਕਾਰ ID",
            "shop_id": "ਸਟੋਰ ID",
            "time": "ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ ਸਮਾਂ ਫਾਰਮੈਟ: %Y-%m-%d %H:%M:%S",
            "customer_count": "ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ ਲਈ ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ, ਮੂਲ ਰੂਪ ਵਿੱਚ 1 ਵਿਅਕਤੀ"
        },
        "returns": "ਸੇਵਾ ਅਪਾਇੰਟਮੈਂਟ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "ਦੁਕਾਨ 'ਤੇ ਪਹੁੰਚਣ ਦੀ ਸਥਿਤੀ ਵਿੱਚ ਖੋਜੀ ਗਈ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਜਾਣਕਾਰੀ ਨੂੰ ਸੋਧੋ",
        "preconditions": "ਦੁਕਾਨ 'ਤੇ ਪਹੁੰਚਣ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਦੇ ਸੋਧਣ ਯੋਗ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਆਰਡਰ ਦੀ ਖੋਜ ਕਰੋ, ਇੱਕ ਅਨੋਖਾ reservation_id ਨਿਰਧਾਰਤ ਕਰੋ, ਉਪਭੋਗਤਾ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਦਾ ਸਮਾਂ ਅਤੇ ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ ਸੋਧਦਾ ਹੈ",
        "postconditions": "ਸੋਧੀ ਗਈ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਜਾਣਕਾਰੀ ਆਉਟਪੁਟ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਸਹਿਮਤ ਸਮੇਂ ਅਨੁਸਾਰ ਵਪਾਰੀ ਕੋਲ ਖਪਤ ਕਰਨ ਲਈ ਸੂਚਿਤ ਕਰੋ",
        "args": {
            "reservation_id": "ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਆਈਡੀ",
            "time": "ਸੋਧਿਆ ਗਿਆ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਸਮਾਂ ਸਹੀ ਫਾਰਮੈਟ %Y-%m-%d %H:%M:%S ਹੈ",
            "customer_count": "ਸੋਧਿਆ ਗਿਆ ਰਿਜ਼ਰਵੇਸ਼ਨ ਖਪਤ ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ"
        },
        "returns": "ਸੋਧੀ ਗਈ ਰਿਜ਼ਰਵੇਸ਼ਨ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ਸਟੋਰ 'ਤੇ ਬੁਕਿੰਗ ਰੱਦ ਕਰੋ",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਇੱਕ ਵਿਲੱਖਣ ਬੁਕਿੰਗ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕਰੋ",
        "postconditions": "ਬੁਕਿੰਗ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "reservation_id": "ਬੁਕਿੰਗ ਆਈਡੀ"
        },
        "returns": "ਬੁਕਿੰਗ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "ਨਿਰਧਾਰਤ ਉਪਭੋਗਤਾ ਦੇ ਸਾਰੇ ਸਟੋਰ ਆਰਡਰ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਸਥਿਤੀ ਵਿੱਚ, ਸਾਰੇ ਸਟੋਰ ਆਰਡਰਾਂ ਨੂੰ ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ",
        "postconditions": "ਸਾਰੇ ਸਟੋਰ ਆਰਡਰਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ"
        },
        "returns": "ਮੌਜੂਦਾ ਉਪਭੋਗਤਾ ਦੇ ਸਾਰੇ ਸਟੋਰ ਆਰਡਰਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "ਨਿਰਧਾਰਤ ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਸਟੋਰ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤਾਂ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਸਟੋਰ ਵਿਜ਼ਿਟ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਸਾਰੀਆਂ ਸਟੋਰ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤਾਂ ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ",
        "postconditions": "ਸਾਰੀਆਂ ਸਟੋਰ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ"
        },
        "returns": "ਮੌਜੂਦਾ ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਸਟੋਰ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "ਨਿਰਧਾਰਤ ਉਪਭੋਗਤਾ ਲਈ ਸਾਰੀਆਂ ਦੁਕਾਨ ਸੀਟ ਰਿਜ਼ਰਵੇਸ਼ਨ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਦੁਕਾਨ ਦੇ ਮਾਹੌਲ ਵਿੱਚ, ਸਾਰੀਆਂ ਦੁਕਾਨ ਸੀਟ ਰਿਜ਼ਰਵੇਸ਼ਨਾਂ ਨੂੰ ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ",
        "postconditions": "ਸਾਰੀਆਂ ਦੁਕਾਨ ਸੀਟ ਰਿਜ਼ਰਵੇਸ਼ਨਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰਦਾ ਹੈ",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ"
        },
        "returns": "ਮੌਜੂਦਾ ਉਪਭੋਗਤਾ ਲਈ ਸਾਰੀਆਂ ਦੁਕਾਨ ਸੀਟ ਰਿਜ਼ਰਵੇਸ਼ਨਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "ਵਰਤੋਂਕਾਰ ਦੀ ਸੀਟ ਬੁਕਿੰਗ ਜਾਣਕਾਰੀ ਦੀ ਜਾਂਚ ਕਰੋ, ਜਦੋਂ book_id None ਹੋਵੇ ਤਾਂ ਵਰਤੋਂਕਾਰ ਦੀਆਂ ਸਾਰੀਆਂ ਸੀਟ ਬੁਕਿੰਗਾਂ ਵਾਪਸ ਕਰੋ, ਜਦੋਂ book_id None ਨਾ ਹੋਵੇ ਤਾਂ ਨਿਰਧਾਰਤ ਸੀਟ ਬੁਕਿੰਗ ਵਾਪਸ ਕਰੋ।",
        "preconditions": "ਸਟੋਰ ਆਗਮਨ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਜਦੋਂ book_id None ਹੋਵੇ ਤਾਂ ਵਰਤੋਂਕਾਰ ਦੀਆਂ ਸਾਰੀਆਂ ਸੀਟ ਬੁਕਿੰਗਾਂ ਵਾਪਸ ਕਰੋ, ਜਦੋਂ book_id None ਨਾ ਹੋਵੇ ਤਾਂ ਨਿਰਧਾਰਤ ਸੀਟ ਬੁਕਿੰਗ ਵਾਪਸ ਕਰੋ।",
        "postconditions": "ਸੀਟ ਬੁਕਿੰਗ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ/ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ ਹੈ।",
        "args": {
            "user_id": "ਵਰਤੋਂਕਾਰ id",
            "book_id": "ਸੀਟ ਬੁਕਿੰਗ id, ਵੈਕਲਪਿਕ ਪੈਰਾਮੀਟਰ, ਮੂਲ ਰੂਪ ਵਿੱਚ None"
        },
        "returns": "ਸੀਟ ਬੁਕਿੰਗ ਜਾਣਕਾਰੀ, ਕਈ ਸੀਟ ਬੁਕਿੰਗਾਂ ਨੂੰ ਨਵੀਂ ਲਾਈਨ ਨਾਲ ਵੱਖ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "ਉਪਭੋਗਤਾ ਦੀ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤ ਜਾਣਕਾਰੀ ਦੀ ਜਾਂਚ ਕਰੋ",
        "preconditions": "ਦੁਕਾਨ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਜਦੋਂ reservation_id None ਹੁੰਦਾ ਹੈ, ਤਾਂ ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤਾਂ ਵਾਪਸ ਕਰੋ, ਜਦੋਂ reservation_id None ਨਹੀਂ ਹੁੰਦਾ, ਤਾਂ ਨਿਰਧਾਰਤ ਅਪਾਇੰਟਮੈਂਟ ਖਪਤ ਵਾਪਸ ਕਰੋ।",
        "postconditions": "ਅਪਾਇੰਟਮੈਂਟ ਖਪਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ ਜਾਂ ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ ਹੈ।",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ id",
            "reservation_id": "ਅਪਾਇੰਟਮੈਂਟ ਖਪਤ id, ਵੈਕਲਪਿਕ ਪੈਰਾਮੀਟਰ, ਮੂਲ ਰੂਪ ਵਿੱਚ None"
        },
        "returns": "ਅਪਾਇੰਟਮੈਂਟ ਖਪਤ ਜਾਣਕਾਰੀ, ਕਈ ਅਪਾਇੰਟਮੈਂਟ ਨੂੰ ਨਵੀਂ ਲਾਈਨ ਨਾਲ ਵੱਖ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "tool_type": "READ"
    },
}

# Tool descriptions - Belarusian version
TOOL_DESCRIPTIONS_BE = {
    "instore_shop_search_recommend": {
        "description": "У сцэнарыі наведвання, калі карыстальнік (размытыя запыты, не выказаў дакладна канкрэтны пакет | не выказаў дакладна канкрэтны заклад), трэба, спалучаючы асабістыя перавагі карыстальніка і інфармацыю аб тэгах закладаў, рэкамендаваць некалькі закладаў",
        "preconditions": "У сцэнарыі наведвання, атрыманне ключавых слоў, звязаных з закладамі",
        "postconditions": "Вяртаецца спіс закладаў, карыстальніка накіроўваюць на выбар і пацвярджэнне заклада; пасля пацвярджэння заклада карыстальнік павінен выбраць і пацвердзіць пакет паслуг",
        "args": {
            "keywords": "Ключавыя словы, якія апісваюць заклад"
        },
        "returns": "Структураваная інфармацыя аб закладзе",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "У сцэнарыі візіту ў краму можна вылучыць ключавыя словы, якія апісваюць наборы, на аснове выказванняў карыстальніка, каб шукаць або рэкамендаваць некалькі набораў",
        "preconditions": "Знаходжанне ў сцэнарыі візіту ў краму, ключавыя словы, звязаныя з наборамі",
        "postconditions": "Вяртае спіс набораў, накіроўвае карыстальніка на выбар набору і стварэнне замовы",
        "args": {
            "keywords": "Ключавыя словы, якія апісваюць набор"
        },
        "returns": "Структураваная інфармацыя аб наборах",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Афармленне замовы ў краме",
        "preconditions": "У сцэнарыі візіту ў краму, вызначаны ўнікальны ідэнтыфікатар крамы і адзін або некалькі ідэнтыфікатараў тавараў",
        "postconditions": "Вяртае інфармацыю пра заказ (уключаючы order_id), пытае карыстальніка, ці жадае ён аплаціць заказ",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "shop_id": "Ідэнтыфікатар крамы",
            "product_id": "Ідэнтыфікатар набора",
            "quantity": "Колькасць"
        },
        "returns": "Інфармацыя пра заказ",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "У сцэнарыі візіту ў краму, калі ў кантэксце ёсць інфармацыя пра заказ, карыстальнік паведамляе пра завяршэнне аплаты або паўторную аплату",
        "preconditions": "Сцэнарый візіту ў краму, карыстальнік паведамляе пра завяршэнне аплаты, заказ створаны і знаходзіцца на этапе аплаты｜Карыстальнік паведамляе пра паўторную аплату",
        "postconditions": "Вяртае інфармацыю пра вынік аплаты",
        "args": {
            "order_id": "Ідэнтыфікатар заказа"
        },
        "returns": "Выводзіць інфармацыю пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Карыстальнік скасоўвае заказ або аплату. Забаронена паўторна скасоўваць заказ, які ўжо знаходзіцца ў скасаваным стане.",
        "preconditions": "У сцэнарыі візіту ў краму, праверыць статус заказу, пераканацца, што статус заказу не cancelled",
        "postconditions": "Вярнуць інфармацыю пра вынік скасавання заказу",
        "args": {
            "order_id": "ID заказу"
        },
        "returns": "Вывесці інфармацыю пра вынік скасавання заказу",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Браніраванне месцаў - браніраванне фізічных месцаў/сталоў пасля выбару канкрэтнай крамы",
        "preconditions": "Сцэнарый візіту ў краму, вызначаны адзіны ідэнтыфікатар крамы, крама падтрымлівае паслугу браніравання месцаў",
        "postconditions": "Вяртае інфармацыю аб браніраванні месца (уключаючы book_id); калі патрабуецца аплата за браніраванне, запытаць карыстальніка, ці жадае ён апліціць",
        "args": {
            "user_id": "ідэнтыфікатар карыстальніка",
            "shop_id": "ідэнтыфікатар крамы",
            "time": "час браніравання месца фармат: %Y-%m-%d %H:%M:%S",
            "customer_count": "колькасць асоб для браніравання месца, па змаўчанні 1 асоба"
        },
        "returns": "інфармацыя аб браніраванні месца",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Аплата браніравання месца ў установе",
        "preconditions": "Сцэнарый знаходжання ў установе, вызначаны ўнікальны ідэнтыфікатар браніравання",
        "postconditions": "Вяртае інфармацыю пра вынік аплаты",
        "args": {
            "book_id": "Ідэнтыфікатар браніравання месца"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Адмена браніравання па прыбыцці",
        "preconditions": "Сцэнарый прыбыцця, вызначаны ўнікальны ідэнтыфікатар браніравання",
        "postconditions": "Вяртае інфармацыю пра вынік адмены браніравання",
        "args": {
            "book_id": "ідэнтыфікатар браніравання"
        },
        "returns": "Інфармацыя пра вынік адмены браніравання",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Браніраванне паслуг - запіс на час паслугі пасля выбару канкрэтнай крамы",
        "preconditions": "Сцэнарый візіту ў краму, вызначаны адзіны ідэнтыфікатар крамы, крама падтрымлівае браніраванне паслуг",
        "postconditions": "Вяртае інфармацыю аб браніраванні паслугі (уключаючы reservation_id), паведамляе карыстальніку аб неабходнасці з'явіцца ў краму ў узгоднены час для атрымання паслугі",
        "args": {
            "user_id": "ідэнтыфікатар карыстальніка",
            "shop_id": "ідэнтыфікатар крамы",
            "time": "час браніравання паслугі, фармат: %Y-%m-%d %H:%M:%S",
            "customer_count": "колькасць асоб для браніравання паслугі, па змаўчанні 1 асоба"
        },
        "returns": "інфармацыя аб браніраванні паслугі",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Змена інфармацыі аб браніраванні спажывання, знойдзенай у сцэнарыі прыбыцця ў краму",
        "preconditions": "Сцэнарый прыбыцця ў краму, пошук заказа на браніраванне спажывання карыстальніка, які патрабуе змены, вызначэнне ўнікальнага reservation_id, змена карыстальнікам часу і колькасці асоб для браніравання спажывання",
        "postconditions": "Вывад інфармацыі аб змененым браніраванні спажывання, апавяшчэнне карыстальніка аб візіце ў краму для спажывання ў узгоднены час",
        "args": {
            "reservation_id": "Ідэнтыфікатар браніравання спажывання",
            "time": "Час браніравання спажывання пасля змены, правільны фармат %Y-%m-%d %H:%M:%S",
            "customer_count": "Колькасць асоб для браніравання спажывання пасля змены"
        },
        "returns": "Змененая інфармацыя аб браніраванні",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Адмена запісу на паслугу ў краме",
        "preconditions": "У сцэнарыі візіту ў краму, вызначаны ўнікальны ідэнтыфікатар запісу на паслугу",
        "postconditions": "Вяртае інфармацыю пра вынік адмены запісу на паслугу",
        "args": {
            "reservation_id": "Ідэнтыфікатар запісу на паслугу"
        },
        "returns": "Інфармацыя пра вынік адмены запісу на паслугу",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Атрымаць усе заказы ў краме для ўказанага карыстальніка",
        "preconditions": "У сцэнарыі наведвання крамы, калі неабходна праглядзець усе заказы ў краме",
        "postconditions": "Вяртае падрабязную інфармацыю пра ўсе заказы ў краме",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка"
        },
        "returns": "Падрабязная інфармацыя пра ўсе заказы ў краме для бягучага карыстальніка",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Атрымаць усе запісы аб спажыванні па папярэднім запісе на наведванне крамы для ўказанага карыстальніка",
        "preconditions": "У сцэнарыі наведвання крамы, калі неабходна праглядзець усе запісы аб спажыванні па папярэднім запісе ў краме",
        "postconditions": "Вяртае падрабязную інфармацыю пра ўсе запісы аб спажыванні па папярэднім запісе на наведванне крамы",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка"
        },
        "returns": "Падрабязная інфармацыя пра ўсе запісы аб спажыванні па папярэднім запісе на наведванне крамы для бягучага карыстальніка",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Атрымаць усе браніраванні месцаў у зале для вызначанага карыстальніка",
        "preconditions": "Знаходзіцца ў сцэнарыі візіту ў залу, неабходна праглядзець усе браніраванні месцаў у зале",
        "postconditions": "Вяртае падрабязную інфармацыю пра ўсе браніраванні месцаў у зале",
        "args": {
            "user_id": "ID карыстальніка"
        },
        "returns": "Падрабязная інфармацыя пра ўсе браніраванні месцаў у зале для бягучага карыстальніка",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Запыт інфармацыі аб браніраванні месцаў карыстальніка. Калі book_id роўны None, вяртаюцца ўсе браніраванні месцаў карыстальніка. Калі book_id не роўны None, вяртаецца канкрэтнае браніраванне месца.",
        "preconditions": "Сцэнарый прыбыцця ў заклад. Калі book_id роўны None, вяртаюцца ўсе браніраванні месцаў карыстальніка. Калі book_id не роўны None, вяртаецца канкрэтнае браніраванне месца.",
        "postconditions": "Вяртае інфармацыю аб браніраванні месцаў для зручнасці наступнага змянення або скасавання.",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "book_id": "Ідэнтыфікатар браніравання месца, неабавязковы параметр, па змаўчанні None"
        },
        "returns": "Інфармацыя аб браніраванні месцаў; некалькі браніраванняў раздзяляюцца сімвалам новага радка.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Запыт інфармацыі пра браніраванне і спажыванне карыстальніка",
        "preconditions": "У сцэнарыі візіту ў заклад: калі reservation_id роўны None, вяртаецца ўсё браніраванне і спажыванне карыстальніка; калі reservation_id не роўны None, вяртаецца канкрэтнае браніраванне і спажыванне",
        "postconditions": "Вяртае інфармацыю пра браніраванне і спажыванне, каб пазней можна было яе змяніць або скасаваць",
        "args": {
            "user_id": "ID карыстальніка",
            "reservation_id": "ID браніравання і спажывання, неабавязковы параметр, па змаўчанні None"
        },
        "returns": "Інфармацыя пра браніраванне і спажыванне, некалькі запісаў падзелены сімвалам новага радка",
        "tool_type": "READ"
    },
}

# Tool descriptions - Malay version
TOOL_DESCRIPTIONS_MS = {
    "instore_shop_search_recommend": {
        "description": "Dalam senario di kedai, pengguna (keperluan kabur, tidak menyatakan pakej spesifik | tidak menyatakan merchant spesifik), perlu menggabungkan kegemaran peribadi pengguna dan tag merchant serta maklumat lain, untuk mencadangkan beberapa merchant.",
        "preconditions": "Berada dalam senario di kedai, dapatkan kata kunci berkaitan merchant.",
        "postconditions": "Kembalikan senarai merchant, bimbing pengguna untuk memilih dan mengesahkan merchant, setelah merchant disahkan, pengguna perlu memilih dan mengesahkan pakej.",
        "args": {
            "keywords": "Kata kunci yang menggambarkan merchant."
        },
        "returns": "Maklumat merchant yang dikeluarkan secara berstruktur.",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Dalam senario kedatangan ke kedai, kata kunci yang menerangkan pakej boleh diekstrak berdasarkan ungkapan pengguna untuk mencari atau mengesyorkan berbilang pakej",
        "preconditions": "Berada dalam senario kedatangan ke kedai, kata kunci berkaitan pakej",
        "postconditions": "Memulangkan senarai pakej, membimbing pengguna memilih pakej dan mencipta pesanan",
        "args": {
            "keywords": "Kata kunci yang menerangkan pakej"
        },
        "returns": "Maklumat pakej yang dikeluarkan secara berstruktur",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Penyerahan pesanan kedai",
        "preconditions": "Berada dalam senario kedai, pastikan ID kedai yang unik dan satu atau lebih ID produk",
        "postconditions": "Kembalikan maklumat pesanan (termasuk order_id), tanya pengguna sama ada ingin membayar pesanan",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID kedai",
            "product_id": "ID pakej",
            "quantity": "Kuantiti"
        },
        "returns": "Maklumat pesanan",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Dalam senario di kedai, maklumat pesanan wujud dalam konteks sebelumnya, pengguna menyatakan pembayaran telah selesai, atau pembayaran semula telah selesai",
        "preconditions": "Berada dalam senario di kedai, pengguna menyatakan operasi pembayaran telah selesai, pesanan telah dicipta dan memasuki peringkat pembayaran | pengguna menyatakan pembayaran semula",
        "postconditions": "Memulangkan maklumat hasil pembayaran",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Mengeluarkan maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Pengguna membatalkan pesanan, atau pengguna membatalkan pembayaran. Dilarang membatalkan pesanan yang sudah berstatus dibatalkan.",
        "preconditions": "Berada dalam senario kedai, semak status pesanan, pastikan status pesanan bukan dibatalkan",
        "postconditions": "Memulangkan maklumat hasil pembatalan pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Mengeluarkan maklumat hasil pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Tempahan Tempat Duduk - Tempah tempat duduk atau meja fizikal setelah memilih merchant",
        "preconditions": "Berada dalam senario tiba di kedai, ID merchant unik telah ditentukan, merchant menyokong perkhidmatan tempahan tempat duduk",
        "postconditions": "Memulangkan maklumat tempahan tempat duduk (termasuk book_id), jika perlu membayar yuran tempahan, tanya pengguna sama ada ingin membayar",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID merchant",
            "time": "Masa tempahan tempat duduk Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Bilangan orang untuk tempahan tempat duduk, secara lalai adalah 1 orang"
        },
        "returns": "Maklumat tempahan tempat duduk",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Pembayaran tempahan tempat duduk di kedai",
        "preconditions": "Berada dalam senario di kedai, tentukan ID tempahan yang unik",
        "postconditions": "Memulangkan maklumat hasil pembayaran",
        "args": {
            "book_id": "ID tempahan tempat duduk"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Membatalkan tempahan apabila tiba di kedai",
        "preconditions": "Berada dalam senario tiba di kedai, tentukan ID tempahan yang unik",
        "postconditions": "Memulangkan maklumat hasil pembatalan tempahan",
        "args": {
            "book_id": "ID tempahan"
        },
        "returns": "Maklumat hasil pembatalan tempahan",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Tempahan Perkhidmatan - Tempah masa perkhidmatan setelah memilih kedai",
        "preconditions": "Berada dalam senario kunjungan kedai, ID kedai unik telah ditentukan, kedai menyokong tempahan perkhidmatan",
        "postconditions": "Memulangkan maklumat tempahan perkhidmatan (termasuk reservation_id), memaklumkan pengguna untuk hadir ke kedai mengikut masa yang dipersetujui untuk menerima perkhidmatan",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID kedai",
            "time": "Masa tempahan perkhidmatan Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Bilangan orang untuk tempahan perkhidmatan, lalai adalah 1 orang"
        },
        "returns": "Maklumat tempahan perkhidmatan",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Mengubah suai maklumat tempahan penggunaan yang disemak dalam senario kedatangan ke kedai",
        "preconditions": "Berada dalam senario kedatangan ke kedai, semak pesanan tempahan penggunaan pengguna yang hendak diubah suai, tentukan satu reservation_id yang unik, pengguna mengubah suai masa dan bilangan pelanggan untuk tempahan penggunaan",
        "postconditions": "Keluarkan maklumat tempahan penggunaan yang telah diubah suai, maklumkan pengguna untuk hadir ke merchant mengikut masa yang dipersetujui",
        "args": {
            "reservation_id": "ID tempahan penggunaan",
            "time": "Masa tempahan penggunaan yang telah diubah suai. Format yang betul ialah %Y-%m-%d %H:%M:%S",
            "customer_count": "Bilangan pelanggan untuk tempahan penggunaan yang telah diubah suai"
        },
        "returns": "Maklumat tempahan yang telah diubah suai",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Pembatalan tempahan penggunaan di kedai",
        "preconditions": "Berada dalam senario kedai, tentukan ID penggunaan tempahan yang unik",
        "postconditions": "Memulangkan maklumat hasil pembatalan tempahan penggunaan",
        "args": {
            "reservation_id": "ID penggunaan tempahan"
        },
        "returns": "Maklumat hasil pembatalan tempahan penggunaan",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Dapatkan semua pesanan kedatangan ke kedai untuk pengguna yang ditentukan",
        "preconditions": "Berada dalam senario kedatangan ke kedai, perlu melihat semua pesanan kedatangan ke kedai",
        "postconditions": "Memulangkan maklumat terperinci untuk semua pesanan kedatangan ke kedai",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Maklumat terperinci untuk semua pesanan kedatangan ke kedai pengguna semasa",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Dapatkan semua transaksi tempahan kehadiran di kedai untuk pengguna tertentu",
        "preconditions": "Berada dalam senario kehadiran di kedai, perlu melihat semua transaksi tempahan kehadiran di kedai",
        "postconditions": "Memulangkan maklumat terperinci bagi semua transaksi tempahan kehadiran di kedai",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Maklumat terperinci bagi semua transaksi tempahan kehadiran di kedai untuk pengguna semasa",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Dapatkan semua tempahan tempat duduk di kedai untuk pengguna tertentu",
        "preconditions": "Berada dalam senario di kedai, perlu melihat semua tempahan tempat duduk di kedai",
        "postconditions": "Memulangkan maklumat terperinci bagi semua tempahan tempat duduk di kedai",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Maklumat terperinci bagi semua tempahan tempat duduk di kedai untuk pengguna semasa",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Dapatkan maklumat tempahan tempat duduk pengguna. Apabila book_id ialah None, kembalikan semua tempahan tempat duduk pengguna. Apabila book_id bukan None, kembalikan tempahan tempat duduk yang ditentukan.",
        "preconditions": "Dalam senario kedatangan di kedai. Apabila book_id ialah None, kembalikan semua tempahan tempat duduk pengguna. Apabila book_id bukan None, kembalikan tempahan tempat duduk yang ditentukan.",
        "postconditions": "Kembalikan maklumat tempahan tempat duduk untuk memudahkan pengubahsuaian atau pembatalan selepas ini.",
        "args": {
            "user_id": "ID pengguna",
            "book_id": "ID tempahan tempat duduk, parameter pilihan, lalai ialah None"
        },
        "returns": "Maklumat tempahan tempat duduk, beberapa tempahan tempat duduk dipisahkan oleh aksara baris baru",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Semak maklumat transaksi tempahan pengguna",
        "preconditions": "Berlaku dalam senario kedatangan ke kedai. Apabila reservation_id ialah None, kembalikan semua transaksi tempahan pengguna; apabila reservation_id bukan None, kembalikan transaksi tempahan yang ditentukan.",
        "postconditions": "Mengembalikan maklumat transaksi tempahan, memudahkan pengubahsuaian atau pembatalan selepas itu.",
        "args": {
            "user_id": "ID pengguna",
            "reservation_id": "ID transaksi tempahan, parameter pilihan, nilai lalai ialah None"
        },
        "returns": "Maklumat transaksi tempahan, beberapa tempahan dipisahkan oleh aksara baris baru",
        "tool_type": "READ"
    },
}

# Tool descriptions - Vietnamese version
TOOL_DESCRIPTIONS_VI = {
    "instore_shop_search_recommend": {
        "description": "Trong kịch bản đến cửa hàng, khi người dùng (nhu cầu mơ hồ, chưa nêu rõ gói cụ thể | chưa nêu rõ cửa hàng cụ thể), cần kết hợp sở thích cá nhân của người dùng và các thông tin như nhãn cửa hàng để đề xuất nhiều cửa hàng",
        "preconditions": "Đang trong kịch bản đến cửa hàng, lấy được các từ khóa liên quan đến cửa hàng",
        "postconditions": "Trả về danh sách cửa hàng, hướng dẫn người dùng lựa chọn và xác nhận cửa hàng, sau khi cửa hàng được xác nhận, người dùng cần chọn và xác nhận gói",
        "args": {
            "keywords": "Các từ khóa mô tả cửa hàng"
        },
        "returns": "Thông tin cửa hàng được xuất ra có cấu trúc",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Trong kịch bản tại cửa hàng, có thể trích xuất các từ khóa mô tả gói combo từ biểu đạt của người dùng để tìm kiếm hoặc đề xuất nhiều gói combo.",
        "preconditions": "Đang trong kịch bản tại cửa hàng, có từ khóa liên quan đến gói combo.",
        "postconditions": "Trả về danh sách gói combo, hướng dẫn người dùng chọn gói combo và tạo đơn hàng.",
        "args": {
            "keywords": "Các từ khóa mô tả gói combo."
        },
        "returns": "Thông tin gói combo được xuất ra có cấu trúc.",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Gửi đơn hàng tại cửa hàng",
        "preconditions": "Trong ngữ cảnh tại cửa hàng, xác định một id cửa hàng duy nhất và một hoặc nhiều id sản phẩm",
        "postconditions": "Trả về thông tin đơn hàng (bao gồm order_id), hỏi người dùng có muốn thanh toán đơn hàng không",
        "args": {
            "user_id": "id người dùng",
            "shop_id": "id cửa hàng",
            "product_id": "id gói combo",
            "quantity": "Số lượng"
        },
        "returns": "Thông tin đơn hàng",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Trong bối cảnh tại cửa hàng, thông tin đơn hàng đã có trong ngữ cảnh trước, người dùng biểu thị đã hoàn tất thanh toán hoặc đã thanh toán lại",
        "preconditions": "Đang trong bối cảnh tại cửa hàng, người dùng biểu thị đã hoàn tất thao tác thanh toán, đơn hàng đã được tạo và chuyển sang giai đoạn thanh toán｜Người dùng biểu thị thanh toán lại",
        "postconditions": "Trả về thông tin kết quả thanh toán",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Xuất ra thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Người dùng hủy đơn hàng hoặc hủy thanh toán. Không được phép hủy lại đơn hàng đã ở trạng thái đã hủy.",
        "preconditions": "Trong kịch bản tại cửa hàng, truy vấn trạng thái đơn hàng, đảm bảo trạng thái đơn hàng không phải là đã hủy",
        "postconditions": "Trả về thông tin kết quả hủy đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Xuất thông tin kết quả hủy đơn hàng",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Đặt bàn - Đặt chỗ ngồi/bàn vật lý sau khi chọn nhà hàng",
        "preconditions": "Đang trong kịch bản đến cửa hàng, xác định duy nhất một ID nhà hàng, nhà hàng hỗ trợ dịch vụ đặt bàn",
        "postconditions": "Trả về thông tin đặt bàn (bao gồm book_id), nếu cần thanh toán phí đặt chỗ, hỏi người dùng có thanh toán không",
        "args": {
            "user_id": "ID người dùng",
            "shop_id": "ID nhà hàng",
            "time": "Thời gian đặt bàn Định dạng: %Y-%m-%d %H:%M:%S",
            "customer_count": "Số người đặt bàn, mặc định là 1 người"
        },
        "returns": "Thông tin đặt bàn",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Thanh toán đặt chỗ ngồi tại cửa hàng",
        "preconditions": "Đang trong ngữ cảnh đến cửa hàng, xác định duy nhất một ID đặt chỗ",
        "postconditions": "Trả về thông tin kết quả thanh toán",
        "args": {
            "book_id": "ID đặt chỗ"
        },
        "returns": "Thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Hủy đặt bàn tại cửa hàng",
        "preconditions": "Đang trong ngữ cảnh tại cửa hàng, xác định duy nhất một ID đặt bàn",
        "postconditions": "Trả về thông tin kết quả hủy đặt bàn",
        "args": {
            "book_id": "ID đặt bàn"
        },
        "returns": "Thông tin kết quả hủy đặt bàn",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Đặt lịch hẹn dịch vụ - Đặt thời điểm dịch vụ sau khi chọn cửa hàng",
        "preconditions": "Đang trong bối cảnh đến cửa hàng, xác định duy nhất một id cửa hàng, cửa hàng hỗ trợ đặt lịch hẹn dịch vụ",
        "postconditions": "Trả về thông tin đặt lịch hẹn dịch vụ (bao gồm reservation_id), thông báo cho người dùng đến cửa hàng để nhận dịch vụ theo thời gian đã hẹn",
        "args": {
            "user_id": "id người dùng",
            "shop_id": "id cửa hàng",
            "time": "Thời gian đặt lịch hẹn dịch vụ, định dạng: %Y-%m-%d %H:%M:%S",
            "customer_count": "Số người đặt lịch hẹn dịch vụ, mặc định là 1 người"
        },
        "returns": "Thông tin đặt lịch hẹn dịch vụ",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Sửa đổi thông tin đặt chỗ tiêu dùng đã truy vấn trong kịch bản đến cửa hàng",
        "preconditions": "Đang trong kịch bản đến cửa hàng, truy vấn đơn đặt chỗ tiêu dùng cần sửa đổi của người dùng, xác định một reservation_id duy nhất, người dùng sửa đổi thời gian và số lượng người cho việc đặt chỗ tiêu dùng",
        "postconditions": "Xuất thông tin đặt chỗ tiêu dùng đã sửa đổi, thông báo cho người dùng đến cửa hàng tiêu dùng theo thời gian đã hẹn",
        "args": {
            "reservation_id": "ID đặt chỗ tiêu dùng",
            "time": "Thời gian đặt chỗ tiêu dùng đã sửa đổi, định dạng đúng là %Y-%m-%d %H:%M:%S",
            "customer_count": "Số lượng người đặt chỗ tiêu dùng đã sửa đổi"
        },
        "returns": "Thông tin đặt chỗ đã sửa đổi",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Hủy đặt hẹn tiêu dùng tại cửa hàng",
        "preconditions": "Đang trong kịch bản tại cửa hàng, xác định duy nhất một ID đặt hẹn tiêu dùng",
        "postconditions": "Trả về thông tin kết quả hủy đặt hẹn tiêu dùng",
        "args": {
            "reservation_id": "ID đặt hẹn tiêu dùng"
        },
        "returns": "Thông tin kết quả hủy đặt hẹn tiêu dùng",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Lấy tất cả đơn hàng tại cửa hàng của người dùng được chỉ định",
        "preconditions": "Đang trong ngữ cảnh tại cửa hàng, cần xem tất cả đơn hàng tại cửa hàng",
        "postconditions": "Trả về thông tin chi tiết của tất cả đơn hàng tại cửa hàng",
        "args": {
            "user_id": "ID người dùng"
        },
        "returns": "Thông tin chi tiết của tất cả đơn hàng tại cửa hàng của người dùng hiện tại",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Lấy tất cả các giao dịch tiêu dùng đặt hẹn tại cửa hàng của người dùng được chỉ định",
        "preconditions": "Đang trong ngữ cảnh đến cửa hàng, cần xem tất cả các giao dịch tiêu dùng đặt hẹn tại cửa hàng",
        "postconditions": "Trả về thông tin chi tiết của tất cả các giao dịch tiêu dùng đặt hẹn tại cửa hàng",
        "args": {
            "user_id": "ID người dùng"
        },
        "returns": "Thông tin chi tiết của tất cả các giao dịch tiêu dùng đặt hẹn tại cửa hàng của người dùng hiện tại",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Lấy tất cả đặt chỗ ngồi tại cửa hàng cho người dùng được chỉ định",
        "preconditions": "Đang trong ngữ cảnh đến cửa hàng, cần xem tất cả đặt chỗ ngồi tại cửa hàng",
        "postconditions": "Trả về thông tin chi tiết của tất cả đặt chỗ ngồi tại cửa hàng",
        "args": {
            "user_id": "ID người dùng"
        },
        "returns": "Thông tin chi tiết của tất cả đặt chỗ ngồi tại cửa hàng của người dùng hiện tại",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Truy vấn thông tin đặt chỗ ngồi của người dùng, khi book_id là None, trả về tất cả đặt chỗ ngồi của người dùng, khi book_id không phải là None, trả về đặt chỗ ngồi được chỉ định",
        "preconditions": "Đang trong ngữ cảnh đến cửa hàng, khi book_id là None, trả về tất cả đặt chỗ ngồi của người dùng, khi book_id không phải là None, trả về đặt chỗ ngồi được chỉ định",
        "postconditions": "Trả về thông tin đặt chỗ ngồi, thuận tiện cho việc sửa đổi/hủy sau này",
        "args": {
            "user_id": "ID người dùng",
            "book_id": "ID đặt chỗ ngồi, tham số tùy chọn, mặc định là None"
        },
        "returns": "Thông tin đặt chỗ ngồi, nhiều đặt chỗ ngồi được phân tách bằng ký tự xuống dòng",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Tra cứu thông tin đặt hẹn tiêu dùng của người dùng",
        "preconditions": "Trong ngữ cảnh đến cửa hàng, khi reservation_id là None, trả về tất cả các đặt hẹn tiêu dùng của người dùng, khi reservation_id khác None, trả về đặt hẹn tiêu dùng được chỉ định",
        "postconditions": "Trả về thông tin đặt hẹn tiêu dùng, thuận tiện cho việc sửa đổi/hủy bỏ sau này",
        "args": {
            "user_id": "ID người dùng",
            "reservation_id": "ID đặt hẹn tiêu dùng, tham số tùy chọn, mặc định là None"
        },
        "returns": "Thông tin đặt hẹn tiêu dùng, nhiều đặt hẹn được phân cách bằng ký tự xuống dòng",
        "tool_type": "READ"
    },
}

# Tool descriptions - Turkish version
TOOL_DESCRIPTIONS_TR = {
    "instore_shop_search_recommend": {
        "description": "Mağaza ziyareti senaryosunda, kullanıcı (ihtiyaçları belirsiz, belirli bir paket belirtmemiş | belirli bir mağaza belirtmemiş) için kullanıcı kişisel tercihleri ve mağaza etiketleri gibi bilgileri birleştirerek birden fazla mağaza önerilir.",
        "preconditions": "Mağaza ziyareti senaryosunda olun, mağaza ile ilgili anahtar kelimeleri alın.",
        "postconditions": "Mağaza listesini döndür, kullanıcıyı mağaza seçip onaylamaya yönlendir, mağaza onaylandıktan sonra kullanıcının paket seçip onaylaması gerekir.",
        "args": {
            "keywords": "Mağazayı tanımlayan anahtar kelimeler"
        },
        "returns": "Yapılandırılmış olarak sunulan mağaza bilgileri",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Mağaza ziyareti senaryosunda, kullanıcı ifadelerinden paketleri tanımlayan anahtar kelimeler çıkarılarak birden fazla paket aranabilir veya önerilebilir.",
        "preconditions": "Mağaza ziyareti senaryosunda olunması, paketlerle ilgili anahtar kelimeler",
        "postconditions": "Paket listesini döndürür, kullanıcıyı paket seçmeye ve sipariş oluşturmaya yönlendirir",
        "args": {
            "keywords": "Paketi tanımlayan anahtar kelimeler"
        },
        "returns": "Yapılandırılmış paket bilgisi çıktısı",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Mağaza içi sipariş gönderimi",
        "preconditions": "Mağaza içi senaryosunda olunmalı, benzersiz bir mağaza kimliği ve bir veya daha fazla ürün kimliği belirlenmeli",
        "postconditions": "Sipariş bilgilerini (order_id dahil) döndürür ve kullanıcıya siparişi ödeyip ödemeyeceğini sorar",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "shop_id": "Mağaza kimliği",
            "product_id": "Paket kimliği",
            "quantity": "Adet"
        },
        "returns": "Sipariş bilgileri",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Mağaza içi senaryoda, önceki bağlamda sipariş bilgisi bulunur; kullanıcı ödemenin tamamlandığını veya yeniden ödemenin tamamlandığını belirtir.",
        "preconditions": "Mağaza içi senaryoda olunması, kullanıcının ödeme işlemini tamamladığını ifade etmesi, siparişin oluşturulmuş ve ödeme aşamasına girmiş olması｜Kullanıcının yeniden ödeme yaptığını belirtmesi",
        "postconditions": "Ödeme sonucu bilgilerini döndürür",
        "args": {
            "order_id": "Sipariş kimliği"
        },
        "returns": "Ödeme sonucu bilgilerini çıktı olarak verir",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Kullanıcı siparişi iptal eder veya kullanıcı ödemeyi iptal eder. Zaten iptal edilmiş durumdaki bir siparişin tekrar iptal edilmesi yasaktır.",
        "preconditions": "Mağaza varış senaryosunda olun, sipariş durumunu sorgulayın, sipariş durumunun iptal edilmiş olmadığından emin olun.",
        "postconditions": "Sipariş iptal sonuç bilgilerini döndürür.",
        "args": {
            "order_id": "Sipariş kimliği"
        },
        "returns": "Sipariş iptal sonuç bilgilerini çıktı olarak ver.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Koltuk Rezervasyonu - Seçilen işletmede fiziksel koltuk veya masa rezervasyonu yapın",
        "preconditions": "Mağazaya varış senaryosunda olun, tek bir işletme kimliği belirlenmiş olsun, işletme koltuk rezervasyon hizmetini desteklesin",
        "postconditions": "Koltuk rezervasyon bilgilerini (book_id dahil) döndürün, rezervasyon ücreti ödenmesi gerekirse kullanıcıya ödeyip ödemeyeceğini sorun",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "shop_id": "İşletme kimliği",
            "time": "Koltuk rezervasyon zamanı Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Koltuk rezervasyonu için kişi sayısı, varsayılan 1 kişi"
        },
        "returns": "Koltuk rezervasyon bilgileri",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Mekanda koltuk rezervasyonu ödemesi",
        "preconditions": "Mekanda bulunma senaryosunda, benzersiz bir rezervasyon kimliği belirlenmiş olmalıdır",
        "postconditions": "Ödeme sonucu bilgileri döndürülür",
        "args": {
            "book_id": "Rezervasyon kimliği"
        },
        "returns": "Ödeme sonucu bilgileri",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Mekana varışta rezervasyon iptali",
        "preconditions": "Mekana varış senaryosunda olunmalı ve benzersiz bir rezervasyon ID'si belirlenmeli",
        "postconditions": "Rezervasyon iptal sonuç bilgisi döndürülür",
        "args": {
            "book_id": "Rezervasyon ID'si"
        },
        "returns": "Rezervasyon iptal sonuç bilgisi",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Hizmet Randevusu - Seçilen işletme için hizmet zamanı ayarlama",
        "preconditions": "Mağazaya varış senaryosunda, benzersiz bir işletme kimliği belirlenmeli ve işletme hizmet randevusunu desteklemeli",
        "postconditions": "Hizmet randevu bilgilerini döndürür (reservation_id içerir) ve kullanıcıyı kararlaştırılan zamanda hizmeti almak üzere işletmeye gitmesi konusunda bilgilendirir",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "shop_id": "İşletme kimliği",
            "time": "Hizmet randevu zamanı Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Hizmet randevusu için kişi sayısı, varsayılan 1 kişi"
        },
        "returns": "Hizmet randevu bilgileri",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Mağaza ziyaretı senaryosunda sorgulanan rezervasyon tüketimi bilgilerini değiştirir",
        "preconditions": "Mağaza ziyaretı senaryosunda olunmalı, kullanıcının değiştirilecek rezervasyon tüketim siparişi sorgulanmalı, benzersiz bir reservation_id belirlenmeli ve kullanıcı rezervasyon tüketim zamanını ve kişi sayısını değiştirmelidir",
        "postconditions": "Değiştirilen rezervasyon tüketimi bilgileri çıktı olarak verilir ve kullanıcıya kararlaştırılan zamanda mağazada tüketim yapması için bildirim gönderilir",
        "args": {
            "reservation_id": "Rezervasyon tüketim kimliği",
            "time": "Değiştirilen rezervasyon tüketim zamanı. Doğru format %Y-%m-%d %H:%M:%S şeklindedir",
            "customer_count": "Değiştirilen rezervasyon tüketim kişi sayısı"
        },
        "returns": "Değiştirilen rezervasyon bilgileri",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Mağaza içi randevulu tüketim iptali",
        "preconditions": "Mağaza içi senaryosunda olunmalı ve benzersiz bir randevu tüketim kimliği belirlenmeli",
        "postconditions": "Randevulu tüketim iptal sonuç bilgisi döndürülür",
        "args": {
            "reservation_id": "Randevulu tüketim kimliği"
        },
        "returns": "Randevulu tüketim iptal sonuç bilgisi",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Belirtilen kullanıcının tüm mağaza içi siparişlerini getir",
        "preconditions": "Mağaza içi senaryosunda bulunulması ve tüm mağaza içi siparişlerin görüntülenmesi gerekmektedır",
        "postconditions": "Tüm mağaza içi siparişlerin ayrıntılı bilgileri döndürülür",
        "args": {
            "user_id": "Kullanıcı kimliği"
        },
        "returns": "Mevcut kullanıcının tüm mağaza içi siparişlerinin ayrıntılı bilgileri",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Belirtilen kullanıcının tüm mağaza içi randevu harcamalarını getirir",
        "preconditions": "Mağaza içi senaryosunda olunmalı ve tüm mağaza içi randevu harcamalarının görüntülenmesi gerekiyor",
        "postconditions": "Tüm mağaza içi randevu harcamalarının ayrıntılı bilgilerini döndürür",
        "args": {
            "user_id": "Kullanıcı kimliği"
        },
        "returns": "Mevcut kullanıcının tüm mağaza içi randevu harcamalarının ayrıntılı bilgileri",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Belirtilen kullanıcının tüm mağaza içi koltuk rezervasyonlarını getirir.",
        "preconditions": "Mağaza içi senaryosunda olunmalı ve tüm mağaza içi koltuk rezervasyonlarının görüntülenmesi gerekmektedır.",
        "postconditions": "Tüm mağaza içi koltuk rezervasyonlarının ayrıntılı bilgileri döndürülür.",
        "args": {
            "user_id": "Kullanıcı kimliği"
        },
        "returns": "Mevcut kullanıcının tüm mağaza içi koltuk rezervasyonlarının ayrıntılı bilgileri.",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Kullanıcının koltuk rezervasyon bilgilerini sorgular. book_id None olduğunda kullanıcının tüm koltuk rezervasyonlarını döndürür, book_id None olmadığında ise belirtilen koltuk rezervasyonunu döndürür.",
        "preconditions": "Mağazaya varış senaryosunda olunmalıdır. book_id None olduğunda kullanıcının tüm koltuk rezervasyonlarını döndürür, book_id None olmadığında ise belirtilen koltuk rezervasyonunu döndürür.",
        "postconditions": "Koltuk rezervasyon bilgilerini döndürür, böylece daha sonra düzenleme veya iptal işlemi yapılabilir.",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "book_id": "Koltuk rezervasyon kimliği, isteğe bağlı parametre, varsayılan olarak None"
        },
        "returns": "Koltuk rezervasyon bilgileri, birden fazla koltuk rezervasyonu yeni satır karakteri ile ayrılır.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Kullanıcının rezervasyon tüketim bilgilerini sorgular",
        "preconditions": "Mağaza ziyareti senaryosunda; reservation_id None olduğunda kullanıcının tüm rezervasyon tüketimlerini döndürür, reservation_id None olmadığında belirtilen rezervasyon tüketimini döndürür.",
        "postconditions": "Rezervasyon tüketim bilgilerini döndürür, böylece daha sonra düzenleme/iptal işlemi kolaylaşır.",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "reservation_id": "Rezervasyon tüketim kimliği, isteğe bağlı parametre, varsayılan olarak None"
        },
        "returns": "Rezervasyon tüketim bilgileri, birden fazla rezervasyon yeni satır karakteri ile ayrılır.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Hebrew version
TOOL_DESCRIPTIONS_HE = {
    "instore_shop_search_recommend": {
        "description": "בתרחיש הגעה לחנות, כאשר המשתמש (דרישות מעורפלות, לא ציין חבילה ספציפית | לא ציין עסק ספציפי), יש לשלב העדפות אישיות ותגיות עסקים וכדומה כדי להמליץ על מספר עסקים",
        "preconditions": "נמצאים בתרחיש הגעה לחנות, איסוף מילות מפתח הקשורות לעסקים",
        "postconditions": "החזרת רשימת עסקים, הנחיית המשתמש לבחור ולאשר עסק, לאחר אישור העסק המשתמש צריך לבחור ולאשר חבילה",
        "args": {
            "keywords": "מילות מפתח המתארות את העסק"
        },
        "returns": "מידע עסקי בפלט מובנה",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "בתרחיש הגעה לחנות, ניתן לחלץ מילות מפתח המתארות חבילות בהתבסס על ביטוי המשתמש, כדי לחפש או להמליץ על מספר חבילות",
        "preconditions": "נמצאים בתרחיש הגעה לחנות, מילות מפתח הקשורות לחבילות",
        "postconditions": "מחזיר רשימת חבילות, מנחה את המשתמש לבחור חבילה וליצור הזמנה",
        "args": {
            "keywords": "מילות מפתח המתארות חבילות"
        },
        "returns": "מידע על חבילות בפלט מובנה",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "הגשת הזמנה לחנות",
        "preconditions": "בתרחיש הגעה לחנות, זיהוי מזהה חנות יחיד ומזהה אחד או יותר של מוצרים",
        "postconditions": "החזרת מידע על ההזמנה (כולל order_id), שאילת המשתמש האם לשלם על ההזמנה",
        "args": {
            "user_id": "מזהה משתמש",
            "shop_id": "מזהה חנות",
            "product_id": "מזהה חבילה",
            "quantity": "כמות"
        },
        "returns": "מידע על ההזמנה",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "בסצנריו של הגעה לחנות, כאשר קיים מידע הזמנה בהקשר הקודם, והמשתמש מציין השלמת תשלום, או השלמת תשלום חוזר",
        "preconditions": "בסצנריו של הגעה לחנות, המשתמש מציין השלמת פעולת תשלום, ההזמנה נוצרה ונכנסה לשלב התשלום｜המשתמש מציין ביצוע תשלום חוזר",
        "postconditions": "מחזיר מידע על תוצאת התשלום",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "פלט מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "המשתמש מבטל הזמנה, או המשתמש מבטל תשלום. אסור לבטל שוב הזמנה שנמצאת כבר במצב מבוטל.",
        "preconditions": "בתרחיש הגעה לחנות, יש לבדוק את סטטוס ההזמנה ולהבטיח שהסטטוס אינו מבוטל.",
        "postconditions": "מחזיר מידע על תוצאת ביטול ההזמנה.",
        "args": {
            "order_id": "מזהה ההזמנה"
        },
        "returns": "מציג מידע על תוצאת ביטול ההזמנה.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "הזמנת מקומות ישיבה - הזמנת מקומות ישיבה או שולחנות פיזיים לאחר בחירת העסק",
        "preconditions": "בהקשר של הגעה לחנות, זיהוי מזהה עסק יחיד, והעסק תומך בשירות הזמנת מקומות ישיבה",
        "postconditions": "החזרת פרטי הזמנה (כולל book_id), אם נדרש תשלום דמי הזמנה, יש לשאול את המשתמש האם לבצע תשלום",
        "args": {
            "user_id": "מזהה משתמש",
            "shop_id": "מזהה עסק",
            "time": "זמן הזמנת מקום ישיבה תבנית: %Y-%m-%d %H:%M:%S",
            "customer_count": "מספר לקוחות להזמנה, ברירת מחדל היא אדם אחד"
        },
        "returns": "פרטי הזמנת מקומות ישיבה",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "תשלום עבור הזמנת מקום ישיבה בהגעה למקום",
        "preconditions": "נמצאים בתרחיש הגעה למקום, זיהוי מזהה הזמנה יחיד",
        "postconditions": "מחזיר מידע על תוצאת התשלום",
        "args": {
            "book_id": "מזהה הזמנת מקום"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "ביטול הזמנה בהגעה למקום",
        "preconditions": "בתרחיש של הגעה למקום, יש לזהות מזהה הזמנה יחיד",
        "postconditions": "החזרת מידע על תוצאת ביטול ההזמנה",
        "args": {
            "book_id": "מזהה הזמנה"
        },
        "returns": "מידע על תוצאת ביטול ההזמנה",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "תיאום שירות - קביעת מועד לשירות לאחר בחירת העסק",
        "preconditions": "נמצא בתרחיש הגעה לחנות, זוהה מזהה עסק יחיד, העסק תומך בתיאום שירות",
        "postconditions": "מחזיר מידע על תיאום השירות (כולל reservation_id), מודיע למשתמש להגיע לעסק בזמן המוסכם לקבלת השירות",
        "args": {
            "user_id": "מזהה משתמש",
            "shop_id": "מזהה עסק",
            "time": "זמן תיאום השירות פורמט: %Y-%m-%d %H:%M:%S",
            "customer_count": "מספר אנשים לתיאום השירות, ברירת מחדל היא אדם אחד"
        },
        "returns": "מידע על תיאום השירות",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "שינוי פרטי הזמנת הצריכה שנמצאו בחיפוש בתרחיש הגעה לחנות",
        "preconditions": "בתרחיש הגעה לחנות, יש לחפש הזמנת צריכה של המשתמש הממתינה לשינוי, לקבוע מזהה reservation_id יחיד, והמשתמש משנה את זמן הצריכה בהזמנה ואת מספר הסועדים",
        "postconditions": "הצגת פרטי הזמנת הצריכה לאחר השינוי, והודעה למשתמש להגיע לעסק לצריכה בהתאם לזמן המוסכם",
        "args": {
            "reservation_id": "מזהה הזמנת צריכה",
            "time": "זמן צריכה בהזמנה לאחר השינוי, הפורמט התקין הוא %Y-%m-%d %H:%M:%S",
            "customer_count": "מספר הסועדים בהזמנה לאחר השינוי"
        },
        "returns": "פרטי ההזמנה לאחר השינוי",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ביטול הזמנת צריכה בחנות",
        "preconditions": "בתרחיש הגעה לחנות, זיהוי מזהה יחיד להזמנת הצריכה",
        "postconditions": "החזרת מידע אודות תוצאת ביטול הזמנת הצריכה",
        "args": {
            "reservation_id": "מזהה הזמנת הצריכה"
        },
        "returns": "מידע אודות תוצאת ביטול הזמנת הצריכה",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "שלף את כל ההזמנות להגעה לחנות עבור משתמש מסוים",
        "preconditions": "בתרחיש הגעה לחנות, נדרש לצפות בכל ההזמנות להגעה לחנות",
        "postconditions": "מחזיר מידע מפורט על כל ההזמנות להגעה לחנות",
        "args": {
            "user_id": "מזהה משתמש"
        },
        "returns": "מידע מפורט על כל ההזמנות להגעה לחנות של המשתמש הנוכחי",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "קבלת כל פרטי הצריכה של מינויים לביקור בחנות עבור משתמש מסוים",
        "preconditions": "נמצאים בתרחיש של ביקור בחנות, ויש צורך לצפות בכל פרטי הצריכה של מינויים לביקור בחנות",
        "postconditions": "מחזיר את המידע המפורט על כל פרטי הצריכה של מינויים לביקור בחנות",
        "args": {
            "user_id": "מזהה משתמש"
        },
        "returns": "המידע המפורט על כל פרטי הצריכה של מינויים לביקור בחנות של המשתמש הנוכחי",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "קבלת כל הזמנות המושבים בחנות עבור משתמש מסוים",
        "preconditions": "בתרחיש הגעה לחנות, נדרש לצפות בכל הזמנות המושבים בחנות",
        "postconditions": "מחזיר מידע מפורט על כל הזמנות המושבים בחנות",
        "args": {
            "user_id": "מזהה משתמש"
        },
        "returns": "מידע מפורט על כל הזמנות המושבים בחנות של המשתמש הנוכחי",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "שאילתת מידע על הזמנת המושב של המשתמש. כאשר book_id הוא None, מוחזרות כל הזמנות המושב של המשתמש. כאשר book_id אינו None, מוחזרת הזמנת המושב הספציפית.",
        "preconditions": "בתרחיש הגעה לחנות. כאשר book_id הוא None, מוחזרות כל הזמנות המושב של המשתמש. כאשר book_id אינו None, מוחזרת הזמנת המושב הספציפית.",
        "postconditions": "מחזיר מידע על הזמנת מושב, נוח לשינוי או ביטול מאוחר יותר.",
        "args": {
            "user_id": "מזהה משתמש",
            "book_id": "מזהה הזמנת מושב, פרמטר אופציונלי, ברירת מחדל היא None."
        },
        "returns": "מידע על הזמנת מושב, הזמנות מושב מרובות מופרדות באמצעות תו שורה חדשה.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "חקירת פרטי צריכת ההזמנה של המשתמש",
        "preconditions": "בתרחיש הגעה לחנות, כאשר reservation_id הוא None, מחזיר את כל צריכות ההזמנה של המשתמש, כאשר reservation_id אינו None, מחזיר את צריכת ההזמנה הספציפית",
        "postconditions": "מחזיר פרטי צריכת הזמנה, נוח לשינוי/ביטול לאחר מכן",
        "args": {
            "user_id": "מזהה משתמש",
            "reservation_id": "מזהה צריכת הזמנה, פרמטר רשות, ברירת מחדל היא None"
        },
        "returns": "פרטי צריכת הזמנה, הזמנות מרובות מופרדות בתו שורת חדשה",
        "tool_type": "READ"
    },
}

# Tool descriptions - Indonesian version
TOOL_DESCRIPTIONS_ID = {
    "instore_shop_search_recommend": {
        "description": "Dalam skenario kunjungan ke toko, pengguna (kebutuhan ambigu, belum secara eksplisit menyatakan paket spesifik | belum secara eksplisit menyatakan merchant spesifik), perlu merekomendasikan beberapa merchant dengan menggabungkan preferensi pribadi pengguna dan informasi tag merchant, dll.",
        "preconditions": "Berada dalam skenario kunjungan ke toko, memperoleh kata kunci yang terkait dengan merchant.",
        "postconditions": "Mengembalikan daftar merchant, memandu pengguna untuk memilih dan mengonfirmasi merchant, setelah merchant dikonfirmasi pengguna perlu memilih dan mengonfirmasi paket.",
        "args": {
            "keywords": "Kata kunci yang mendeskripsikan merchant."
        },
        "returns": "Informasi merchant yang dikeluarkan secara terstruktur.",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Dalam skenario kunjungan ke toko, dapat mengekstrak kata kunci yang menggambarkan paket berdasarkan ungkapan pengguna, untuk mencari atau merekomendasikan beberapa paket.",
        "preconditions": "Berada dalam skenario kunjungan ke toko, kata kunci terkait paket.",
        "postconditions": "Mengembalikan daftar paket, memandu pengguna untuk memilih paket dan membuat pesanan.",
        "args": {
            "keywords": "Kata kunci yang menggambarkan paket."
        },
        "returns": "Informasi paket yang dihasilkan secara terstruktur.",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Pengajuan pesanan di toko",
        "preconditions": "Berada dalam skenario di toko, tentukan satu ID toko yang unik dan satu atau lebih ID produk",
        "postconditions": "Mengembalikan informasi pesanan (termasuk order_id), menanyakan pengguna apakah akan membayar pesanan",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID toko",
            "product_id": "ID paket",
            "quantity": "Jumlah"
        },
        "returns": "Informasi pesanan",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Dalam skenario di toko, terdapat informasi pesanan pada konteks sebelumnya, pengguna menyatakan pembayaran selesai, atau pembayaran ulang selesai",
        "preconditions": "Berada dalam skenario di toko, pengguna menyatakan operasi pembayaran selesai, pesanan dibuat dan masuk ke tahap pembayaran｜pengguna menyatakan pembayaran ulang",
        "postconditions": "Mengembalikan informasi hasil pembayaran",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Mengeluarkan informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Pengguna membatalkan pesanan atau pembayaran. Tidak diperbolehkan membatalkan kembali pesanan yang sudah berstatus dibatalkan.",
        "preconditions": "Berada dalam skenario kedatangan di toko, periksa status pesanan, pastikan status pesanan bukan cancelled",
        "postconditions": "Mengembalikan informasi hasil pembatalan pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Mengeluarkan informasi hasil pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Pemesanan Tempat Duduk - Memesan kursi/meja fisik setelah memilih merchant",
        "preconditions": "Berada dalam skenario kunjungan ke toko, ID merchant unik telah ditentukan, merchant mendukung layanan pemesanan tempat duduk",
        "postconditions": "Mengembalikan informasi pemesanan tempat duduk (termasuk book_id), jika ada biaya pemesanan yang perlu dibayar, tanya pengguna apakah mereka ingin membayar",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID merchant",
            "time": "Waktu pemesanan tempat duduk Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Jumlah orang untuk pemesanan tempat duduk, default 1 orang"
        },
        "returns": "Informasi pemesanan tempat duduk",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Pembayaran reservasi kursi saat kedatangan di lokasi",
        "preconditions": "Berada dalam skenario kedatangan di lokasi, ID pemesanan yang unik telah ditentukan",
        "postconditions": "Mengembalikan informasi hasil pembayaran",
        "args": {
            "book_id": "ID pemesanan kursi"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Membatalkan reservasi saat tiba di lokasi",
        "preconditions": "Berada dalam skenario kedatangan di lokasi, pastikan ID reservasi yang unik",
        "postconditions": "Mengembalikan informasi hasil pembatalan reservasi",
        "args": {
            "book_id": "ID reservasi"
        },
        "returns": "Informasi hasil pembatalan reservasi",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Reservasi Layanan - Jadwalkan waktu layanan setelah memilih merchant",
        "preconditions": "Berada dalam skenario kunjungan ke toko, ID merchant unik telah ditentukan, merchant mendukung reservasi layanan",
        "postconditions": "Mengembalikan informasi reservasi layanan (termasuk reservation_id), memberi tahu pengguna untuk datang ke merchant sesuai waktu yang disepakati untuk menerima layanan",
        "args": {
            "user_id": "ID pengguna",
            "shop_id": "ID merchant",
            "time": "Waktu reservasi layanan Format: %Y-%m-%d %H:%M:%S",
            "customer_count": "Jumlah orang untuk reservasi layanan, default 1 orang"
        },
        "returns": "Informasi reservasi layanan",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Memodifikasi informasi reservasi konsumsi yang ditemukan dalam skenario kedatangan ke toko",
        "preconditions": "Berada dalam skenario kedatangan ke toko, mencari pesanan reservasi konsumsi pengguna yang akan diubah, menentukan reservation_id yang unik, pengguna mengubah waktu dan jumlah orang untuk reservasi konsumsi",
        "postconditions": "Mengeluarkan informasi reservasi konsumsi yang telah diubah, memberi tahu pengguna untuk datang ke merchant sesuai waktu yang disepakati untuk konsumsi",
        "args": {
            "reservation_id": "ID reservasi konsumsi",
            "time": "Waktu reservasi konsumsi yang telah diubah. Format yang benar adalah %Y-%m-%d %H:%M:%S",
            "customer_count": "Jumlah orang untuk reservasi konsumsi yang telah diubah"
        },
        "returns": "Informasi reservasi yang telah diubah",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Pembatalan reservasi konsumsi di toko",
        "preconditions": "Berada dalam skenario di toko, tentukan ID reservasi konsumsi yang unik",
        "postconditions": "Mengembalikan informasi hasil pembatalan reservasi konsumsi",
        "args": {
            "reservation_id": "ID reservasi konsumsi"
        },
        "returns": "Informasi hasil pembatalan reservasi konsumsi",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Mengambil semua pesanan kedatangan di toko untuk pengguna tertentu",
        "preconditions": "Berada dalam skenario kedatangan di toko, perlu melihat semua pesanan kedatangan di toko",
        "postconditions": "Mengembalikan informasi detail semua pesanan kedatangan di toko",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Informasi detail semua pesanan kedatangan di toko untuk pengguna saat ini",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Mengambil semua konsumsi reservasi kunjungan toko untuk pengguna tertentu",
        "preconditions": "Berada dalam skenario kunjungan toko, perlu melihat semua konsumsi reservasi kunjungan toko",
        "postconditions": "Mengembalikan informasi rinci semua konsumsi reservasi kunjungan toko",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Informasi rinci semua konsumsi reservasi kunjungan toko untuk pengguna saat ini",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Mengambil semua reservasi tempat duduk untuk kunjungan ke toko pengguna tertentu",
        "preconditions": "Berada dalam skenario kunjungan ke toko, perlu melihat semua reservasi tempat duduk untuk kunjungan ke toko",
        "postconditions": "Mengembalikan informasi terperinci semua reservasi tempat duduk untuk kunjungan ke toko",
        "args": {
            "user_id": "ID pengguna"
        },
        "returns": "Informasi terperinci semua reservasi tempat duduk untuk kunjungan ke toko pengguna saat ini",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Mengambil informasi reservasi kursi pengguna. Ketika book_id adalah None, kembalikan semua reservasi kursi pengguna. Ketika book_id bukan None, kembalikan reservasi kursi yang ditentukan.",
        "preconditions": "Berada dalam skenario kedatangan di toko. Ketika book_id adalah None, kembalikan semua reservasi kursi pengguna. Ketika book_id bukan None, kembalikan reservasi kursi yang ditentukan.",
        "postconditions": "Mengembalikan informasi reservasi kursi, memudahkan untuk modifikasi atau pembatalan di kemudian hari.",
        "args": {
            "user_id": "id pengguna",
            "book_id": "id reservasi kursi, parameter opsional, default adalah None"
        },
        "returns": "Informasi reservasi kursi, beberapa reservasi kursi dipisahkan oleh karakter baris baru",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Mengambil informasi konsumsi reservasi pengguna",
        "preconditions": "Berada dalam skenario kedatangan di toko. Jika reservation_id adalah None, kembalikan semua konsumsi reservasi pengguna. Jika reservation_id bukan None, kembalikan konsumsi reservasi yang ditentukan",
        "postconditions": "Mengembalikan informasi konsumsi reservasi, memudahkan untuk modifikasi atau pembatalan di kemudian hari",
        "args": {
            "user_id": "ID pengguna",
            "reservation_id": "ID konsumsi reservasi, parameter opsional, default adalah None"
        },
        "returns": "Informasi konsumsi reservasi, beberapa reservasi dipisahkan oleh karakter baris baru",
        "tool_type": "READ"
    },
}

# Tool descriptions - Korean version
TOOL_DESCRIPTIONS_KO = {
    "instore_shop_search_recommend": {
        "description": "오프라인 방문 상황에서 사용자 (요구가 모호하여 구체적인 패키지를 명시하지 않음 | 구체적인 매장을 명시하지 않음) 는 개인 취향과 매장 태그 등의 정보를 결합하여 여러 매장을 추천받습니다.",
        "preconditions": "오프라인 방문 상황이며, 매장 관련 키워드를 수집합니다.",
        "postconditions": "매장 목록을 반환하여 사용자가 매장을 선택하고 확정하도록 유도하며, 매장 확정 후 사용자가 패키지를 선택하고 확정하도록 합니다.",
        "args": {
            "keywords": "매장을 설명하는 키워드"
        },
        "returns": "구조화된 매장 정보",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "매장 방문 상황에서 사용자의 발화를 기반으로 세트 메뉴를 설명하는 키워드를 추출하여 여러 세트 메뉴를 검색하거나 추천합니다.",
        "preconditions": "매장 방문 상황이며, 세트 메뉴 관련 키워드가 있어야 합니다.",
        "postconditions": "세트 메뉴 목록을 반환하고, 사용자가 세트 메뉴를 선택하여 주문을 생성하도록 안내합니다.",
        "args": {
            "keywords": "세트 메뉴를 설명하는 키워드"
        },
        "returns": "구조화된 세트 메뉴 정보",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "매장 주문 제출",
        "preconditions": "매장 방문 상황이며, 고유한 가게 ID 와 하나 이상의 상품 ID 를 확인함",
        "postconditions": "주문 정보 (order_id 포함) 를 반환하고, 사용자에게 주문 결제 여부를 묻습니다",
        "args": {
            "user_id": "사용자 ID",
            "shop_id": "가게 ID",
            "product_id": "세트 메뉴 ID",
            "quantity": "수량"
        },
        "returns": "주문 정보",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "매장 방문 상황에서 이전 문맥에 주문 정보가 있으며, 사용자가 결제 완료 또는 재결제 완료를 표현하는 경우",
        "preconditions": "매장 방문 상황이며, 사용자가 결제 작업 완료를 표현하고 주문이 생성되어 결제 단계에 진입함 | 사용자가 재결제를 표시함",
        "postconditions": "결제 결과 정보 반환",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보 출력",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "사용자가 주문을 취소하거나 결제를 취소합니다. 이미 취소된 상태의 주문은 다시 취소할 수 없습니다.",
        "preconditions": "매장 방문 시나리오에서 주문 상태를 조회하여 주문 상태가 취소되지 않았는지 확인합니다.",
        "postconditions": "주문 취소 결과 정보를 반환합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 취소 결과 정보를 출력합니다.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "좌석 예약 - 매장 선택 후 실제 좌석/테이블 예약",
        "preconditions": "매장 방문 상황이어야 하며, 유일한 매장 id 가 확인되고, 매장이 좌석 예약 서비스를 지원해야 함",
        "postconditions": "좌석 예약 정보 반환 (book_id 포함), 좌석 예약비 결제가 필요한 경우 사용자에게 결제 여부 확인",
        "args": {
            "user_id": "사용자 id",
            "shop_id": "매장 id",
            "time": "좌석 예약 시간 형식：%Y-%m-%d %H:%M:%S",
            "customer_count": "좌석 예약 인원, 기본값 1 명"
        },
        "returns": "좌석 예약 정보",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "매장 방문 좌석 예약 결제",
        "preconditions": "매장 방문 상황이며, 고유한 예약 ID 가 확정됨",
        "postconditions": "결제 결과 정보 반환",
        "args": {
            "book_id": "예약 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "매장 방문 예약 취소",
        "preconditions": "매장 방문 상황이며, 고유한 예약 ID 를 확인함",
        "postconditions": "예약 취소 결과 정보 반환",
        "args": {
            "book_id": "예약 ID"
        },
        "returns": "예약 취소 결과 정보",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "서비스 예약 - 업체 선택 후 서비스 시간 예약",
        "preconditions": "매장 방문 상황이며, 고유한 업체 ID 가 확정되었고, 해당 업체가 서비스 예약을 지원함",
        "postconditions": "서비스 예약 정보 (reservation_id 포함) 를 반환하고, 사용자에게 약속된 시간에 업체를 방문하여 서비스를 받도록 알림",
        "args": {
            "user_id": "사용자 ID",
            "shop_id": "업체 ID",
            "time": "서비스 예약 시간 형식：%Y-%m-%d %H:%M:%S",
            "customer_count": "서비스 예약 인원, 기본값 1 명"
        },
        "returns": "서비스 예약 정보",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "매장 방문 시나리오에서 조회된 예약 소비 정보를 수정합니다.",
        "preconditions": "매장 방문 상황이어야 하며, 수정할 사용자의 예약 소비 주문을 조회하여 고유한 reservation_id 를 확인하고, 사용자가 예약 소비 시간과 인원을 수정합니다.",
        "postconditions": "수정된 예약 소비 정보를 출력하고, 약속된 시간에 매장에서 소비하도록 사용자에게 알림을 보냅니다.",
        "args": {
            "reservation_id": "예약 소비 ID",
            "time": "수정된 예약 소비 시간 (정확한 형식: %Y-%m-%d %H:%M:%S)",
            "customer_count": "수정된 예약 소비 인원 수"
        },
        "returns": "수정된 예약 정보",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "매장 방문 예약 소비 취소",
        "preconditions": "매장 방문 상황이어야 하며, 고유한 예약 소비 ID 를 확인해야 함",
        "postconditions": "예약 소비 취소 결과 정보를 반환함",
        "args": {
            "reservation_id": "예약 소비 ID"
        },
        "returns": "예약 소비 취소 결과 정보",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "지정된 사용자의 모든 매장 방문 주문 조회",
        "preconditions": "매장 방문 상황이며 모든 방문 주문을 확인해야 함",
        "postconditions": "모든 매장 방문 주문의 상세 정보 반환",
        "args": {
            "user_id": "사용자 ID"
        },
        "returns": "현재 사용자의 모든 매장 방문 주문 상세 정보",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "지정된 사용자의 모든 매장 방문 예약 소비 내역을 조회합니다.",
        "preconditions": "매장 방문 상황이며, 모든 매장 방문 예약 소비 내역을 확인해야 합니다.",
        "postconditions": "모든 매장 방문 예약 소비 내역의 상세 정보를 반환합니다.",
        "args": {
            "user_id": "사용자 ID"
        },
        "returns": "현재 사용자의 모든 매장 방문 예약 소비 내역에 대한 상세 정보",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "지정된 사용자의 모든 매장 방문 좌석 예약 조회",
        "preconditions": "매장 방문 상황이며, 모든 매장 방문 좌석 예약을 조회해야 함",
        "postconditions": "모든 매장 방문 좌석 예약에 대한 상세 정보를 반환합니다",
        "args": {
            "user_id": "사용자 ID"
        },
        "returns": "현재 사용자의 모든 매장 방문 좌석 예약에 대한 상세 정보",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "사용자의 좌석 예약 정보를 조회합니다. book_id 가 None 일 때는 사용자의 모든 좌석 예약을 반환하고, book_id 가 None 이 아닐 때는 지정된 좌석 예약을 반환합니다.",
        "preconditions": "매장 방문 상황이어야 하며, book_id 가 None 일 때는 사용자의 모든 좌석 예약을 반환하고, book_id 가 None 이 아닐 때는 지정된 좌석 예약을 반환합니다.",
        "postconditions": "좌석 예약 정보를 반환하며, 이후 수정 또는 취소를 위해 사용됩니다.",
        "args": {
            "user_id": "사용자 ID",
            "book_id": "좌석 예약 ID, 선택 매개변수이며 기본값은 None 입니다."
        },
        "returns": "좌석 예약 정보이며, 여러 좌석 예약은 줄 바꿈 문자로 구분됩니다.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "사용자의 예약 소비 정보를 조회합니다.",
        "preconditions": "매장 도착 시나리오에서, reservation_id 가 None 일 경우 사용자의 모든 예약 소비 정보를 반환하고, reservation_id 가 None 이 아닐 경우 지정된 예약 소비 정보를 반환합니다.",
        "postconditions": "예약 소비 정보를 반환하여 이후 수정 또는 취소에 활용할 수 있습니다.",
        "args": {
            "user_id": "사용자 ID",
            "reservation_id": "예약 소비 ID, 선택적 매개변수, 기본값은 None"
        },
        "returns": "예약 소비 정보이며, 여러 예약은 줄 바꿈 문자로 구분됩니다.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Spanish version
TOOL_DESCRIPTIONS_ES = {
    "instore_shop_search_recommend": {
        "description": "En un escenario presencial, el usuario (con necesidades vagas, sin haber expresado claramente un paquete específico｜sin haber expresado claramente un comercio específico), necesita que se recomienden múltiples comercios combinando información como las preferencias personales del usuario y las etiquetas del comercio.",
        "preconditions": "Estar en un escenario presencial, obtener palabras clave relacionadas con el comercio.",
        "postconditions": "Devolver una lista de comercios, guiar al usuario para seleccionar y confirmar un comercio; una vez confirmado el comercio, el usuario debe seleccionar y confirmar un paquete.",
        "args": {
            "keywords": "Palabras clave que describen al comercio."
        },
        "returns": "Información del comercio con salida estructurada.",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "En el contexto de visita a la tienda, se pueden extraer palabras clave que describen los paquetes según la expresión del usuario, para buscar o recomendar varios paquetes.",
        "preconditions": "En el contexto de visita a la tienda, palabras clave relacionadas con los paquetes.",
        "postconditions": "Devuelve una lista de paquetes, guía al usuario para seleccionar un paquete y crear un pedido.",
        "args": {
            "keywords": "Palabras clave que describen los paquetes."
        },
        "returns": "Información estructurada de los paquetes.",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Envío de pedido en tienda",
        "preconditions": "En el contexto de tienda, identificar un ID de tienda único y uno o más IDs de productos",
        "postconditions": "Devolver información del pedido (incluyendo order_id), preguntar al usuario si desea pagar el pedido",
        "args": {
            "user_id": "ID de usuario",
            "shop_id": "ID de tienda",
            "product_id": "ID del paquete",
            "quantity": "Cantidad"
        },
        "returns": "Información del pedido",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "En el escenario de tienda física, con información del pedido en el contexto previo, el usuario indica que el pago se ha completado o que se ha realizado un nuevo pago.",
        "preconditions": "Estar en el escenario de tienda física, el usuario expresa haber completado la operación de pago, el pedido está creado y ha entrado en la fase de pago｜el usuario indica realizar el pago nuevamente.",
        "postconditions": "Devolver información del resultado del pago.",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Mostrar información del resultado del pago.",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "El usuario cancela el pedido o el pago. Está prohibido cancelar nuevamente un pedido que ya esté en estado cancelado.",
        "preconditions": "Estar en el escenario de llegada a la tienda, consultar el estado del pedido y asegurar que el estado del pedido no sea 'cancelled'",
        "postconditions": "Devolver la información del resultado de la cancelación del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Mostrar la información del resultado de la cancelación del pedido",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Reserva de asientos - Reservar asientos o mesas físicas tras seleccionar un comerciante",
        "preconditions": "En el escenario de visita al establecimiento, identificar un único ID de comerciante; el comerciante admite el servicio de reserva de asientos",
        "postconditions": "Devolver información de la reserva de asientos (incluye book_id); si se requiere pagar una tarifa de reserva, preguntar al usuario si desea pagar",
        "args": {
            "user_id": "ID de usuario",
            "shop_id": "ID de comerciante",
            "time": "Hora de reserva de asientos Formato: %Y-%m-%d %H:%M:%S",
            "customer_count": "Número de personas para la reserva de asientos, predeterminado 1 persona"
        },
        "returns": "Información de reserva de asientos",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Pago de la reserva de asiento en el local",
        "preconditions": "Estar en el escenario de llegada al local, identificar un único ID de reserva",
        "postconditions": "Devolver información del resultado del pago",
        "args": {
            "book_id": "ID de reserva de asiento"
        },
        "returns": "Información del resultado del pago",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Cancelar reserva al llegar al local",
        "preconditions": "Estar en el escenario de llegada al local y haber determinado un ID de reserva único",
        "postconditions": "Devolver información sobre el resultado de la cancelación de la reserva",
        "args": {
            "book_id": "ID de la reserva"
        },
        "returns": "Información sobre el resultado de la cancelación de la reserva",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Reserva de servicios - Programar la hora del servicio después de seleccionar un comerciante",
        "preconditions": "En el escenario de visita a la tienda, con un ID de comerciante único determinado y que el comerciante admita reservas de servicios",
        "postconditions": "Devuelve la información de la reserva de servicios (incluye reservation_id) y notifica al usuario que acuda al comerciante en la hora acordada para recibir el servicio",
        "args": {
            "user_id": "ID de usuario",
            "shop_id": "ID de comerciante",
            "time": "Hora de reserva del servicio Formato: %Y-%m-%d %H:%M:%S",
            "customer_count": "Número de personas para la reserva de servicios, por defecto 1 persona"
        },
        "returns": "Información de la reserva de servicios",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Modificar la información de la reserva de consumo consultada en el escenario de llegada a la tienda",
        "preconditions": "Estar en el escenario de llegada a la tienda, consultar la orden de reserva de consumo pendiente de modificación del usuario, determinar un único reservation_id, y el usuario modifica la hora y el número de personas de la reserva de consumo",
        "postconditions": "Mostrar la información de la reserva de consumo modificada y notificar al usuario que acuda al establecimiento a consumir según el horario acordado",
        "args": {
            "reservation_id": "ID de reserva de consumo",
            "time": "Hora de reserva de consumo modificada. El formato correcto es %Y-%m-%d %H:%M:%S",
            "customer_count": "Número de personas de la reserva de consumo modificada"
        },
        "returns": "Información de reserva modificada",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Cancelación de reserva de consumo en tienda",
        "preconditions": "Estar en el contexto de tienda, identificar un ID único de reserva de consumo",
        "postconditions": "Devolver información del resultado de la cancelación de la reserva de consumo",
        "args": {
            "reservation_id": "ID de reserva de consumo"
        },
        "returns": "Información del resultado de la cancelación de la reserva de consumo",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Obtener todos los pedidos en tienda de un usuario especificado",
        "preconditions": "En un escenario de tienda, se necesita ver todos los pedidos en tienda",
        "postconditions": "Devuelve la información detallada de todos los pedidos en tienda",
        "args": {
            "user_id": "ID de usuario"
        },
        "returns": "Información detallada de todos los pedidos en tienda del usuario actual",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Obtener todos los consumos de reservas presenciales del usuario especificado",
        "preconditions": "En un escenario presencial, se necesita ver todos los consumos de reservas presenciales",
        "postconditions": "Devuelve la información detallada de todos los consumos de reservas presenciales",
        "args": {
            "user_id": "ID del usuario"
        },
        "returns": "Información detallada de todos los consumos de reservas presenciales del usuario actual",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Obtener todas las reservas de asientos en el local para un usuario específico",
        "preconditions": "Estar en el contexto de visita al local y necesitar consultar todas las reservas de asientos en el local",
        "postconditions": "Devolver la información detallada de todas las reservas de asientos en el local",
        "args": {
            "user_id": "ID del usuario"
        },
        "returns": "Información detallada de todas las reservas de asientos en el local del usuario actual",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Consulta la información de reserva de asientos del usuario. Cuando book_id es None, devuelve todas las reservas de asientos del usuario; cuando book_id no es None, devuelve la reserva de asientos especificada.",
        "preconditions": "En el escenario de llegada al establecimiento. Cuando book_id es None, devuelve todas las reservas de asientos del usuario; cuando book_id no es None, devuelve la reserva de asientos especificada.",
        "postconditions": "Devuelve la información de reserva de asientos, facilitando su modificación o cancelación posterior.",
        "args": {
            "user_id": "ID del usuario",
            "book_id": "ID de reserva de asientos, parámetro opcional, valor predeterminado None"
        },
        "returns": "Información de reserva de asientos, múltiples reservas separadas por saltos de línea.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Consultar la información de consumo de las reservas del usuario",
        "preconditions": "En el escenario de llegada a la tienda, cuando reservation_id es None, devuelve todos los consumos de reserva del usuario; cuando reservation_id no es None, devuelve el consumo de reserva especificado",
        "postconditions": "Devuelve la información de consumo de la reserva, para facilitar su modificación/cancelación posterior",
        "args": {
            "user_id": "ID del usuario",
            "reservation_id": "ID de consumo de reserva, parámetro opcional, por defecto es None"
        },
        "returns": "Información de consumo de reserva, múltiples reservas separadas por saltos de línea",
        "tool_type": "READ"
    },
}

# Tool descriptions - Thai version
TOOL_DESCRIPTIONS_TH = {
    "instore_shop_search_recommend": {
        "description": "ในสถานการณ์การมาที่ร้าน ผู้ใช้ (ความต้องการไม่ชัดเจน, ไม่ได้ระบุแพ็กเกจเฉพาะเจาะจง | ไม่ได้ระบุร้านค้าเฉพาะเจาะจง) ต้องผสมผสานความชอบส่วนตัวของผู้ใช้และแท็กของร้านค้าและข้อมูลอื่นๆ เพื่อแนะนำร้านค้าหลายแห่ง",
        "preconditions": "อยู่ในสถานการณ์การมาที่ร้านและได้รับคำหลักที่เกี่ยวข้องกับร้านค้า",
        "postconditions": "ส่งคืนรายการร้านค้า นำทางผู้ใช้ให้เลือกและยืนยันร้านค้า หลังจากยืนยันร้านค้าแล้ว ผู้ใช้ต้องเลือกและยืนยันแพ็กเกจ",
        "args": {
            "keywords": "คำหลักที่อธิบายร้านค้า"
        },
        "returns": "ข้อมูลร้านค้าที่ส่งออกแบบมีโครงสร้าง",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "ในบริบทของการมาที่ร้าน สามารถสกัดคำสำคัญที่อธิบายแพ็กเกจจากข้อความของผู้ใช้ เพื่อค้นหาหรือแนะนำแพ็กเกจหลายรายการ",
        "preconditions": "อยู่ในบริบทของการมาที่ร้าน และมีคำสำคัญที่เกี่ยวข้องกับแพ็กเกจ",
        "postconditions": "ส่งคืนรายการแพ็กเกจ นำทางผู้ใช้ให้เลือกแพ็กเกจและสร้างคำสั่งซื้อ",
        "args": {
            "keywords": "คำสำคัญที่อธิบายแพ็กเกจ"
        },
        "returns": "ข้อมูลแพ็กเกจที่ส่งออกในรูปแบบโครงสร้าง",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "การส่งคำสั่งซื้อที่ร้าน",
        "preconditions": "อยู่ในสถานการณ์ที่ร้าน, ระบุรหัสร้านค้าหนึ่งแห่งและรหัสสินค้าหนึ่งรายการหรือมากกว่า",
        "postconditions": "คืนข้อมูลคำสั่งซื้อ (รวม order_id), ถามผู้ใช้ว่าต้องการชำระคำสั่งซื้อหรือไม่",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "shop_id": "รหัสร้านค้า",
            "product_id": "รหัสชุดสินค้า",
            "quantity": "จำนวน"
        },
        "returns": "ข้อมูลคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "ในสถานการณ์ที่หน้าร้าน มีข้อมูลคำสั่งซื้อในบริบทก่อนหน้า ผู้ใช้ระบุว่าชำระเงินเสร็จสิ้น หรือชำระเงินซ้ำเสร็จสิ้น",
        "preconditions": "อยู่ในสถานการณ์ที่หน้าร้าน ผู้ใช้ระบุว่าดำเนินการชำระเงินเสร็จสิ้น คำสั่งซื้อถูกสร้างเสร็จสิ้นและเข้าสู่ขั้นตอนการชำระเงิน | ผู้ใช้ระบุว่าชำระเงินซ้ำ",
        "postconditions": "ส่งกลับข้อมูลผลการชำระเงิน",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "แสดงข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งซื้อ หรือผู้ใช้ยกเลิกการชำระเงิน ห้ามยกเลิกคำสั่งซื้อที่อยู่ในสถานะยกเลิกแล้วซ้ำอีก",
        "preconditions": "อยู่ในสถานการณ์ที่มาถึงร้าน ตรวจสอบสถานะคำสั่งซื้อ ให้แน่ใจว่าสถานะคำสั่งซื้อไม่ใช่ยกเลิก",
        "postconditions": "ส่งกลับข้อมูลผลลัพธ์ของการยกเลิกคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "แสดงข้อมูลผลลัพธ์ของการยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "การจองที่นั่ง - จองที่นั่งหรือโต๊ะจริงหลังจากเลือกผู้ขายแล้ว",
        "preconditions": "อยู่ในสถานการณ์ที่ไปถึงร้าน, ระบุรหัสผู้ขายเพียงหนึ่งเดียว, ผู้ขายรองรับบริการจองที่นั่ง",
        "postconditions": "ส่งคืนข้อมูลการจองที่นั่ง (รวม book_id), หากจำเป็นต้องชำระค่าจองที่นั่ง จะถามผู้ใช้ว่าต้องการชำระหรือไม่",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "shop_id": "รหัสผู้ขาย",
            "time": "เวลาจองที่นั่ง รูปแบบ: %Y-%m-%d %H:%M:%S",
            "customer_count": "จำนวนคนที่จองที่นั่ง, ค่าเริ่มต้นคือ 1 คน"
        },
        "returns": "ข้อมูลการจองที่นั่ง",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "การชำระเงินสำหรับการจองที่นั่งที่ร้าน",
        "preconditions": "อยู่ในสถานการณ์ที่มาถึงร้าน และระบุรหัสการจองเพียงหนึ่งเดียว",
        "postconditions": "ส่งคืนข้อมูลผลการชำระเงิน",
        "args": {
            "book_id": "รหัสการจองที่นั่ง"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "ยกเลิกการจองเมื่อมาถึงร้าน",
        "preconditions": "อยู่ในสถานการณ์ที่มาถึงร้าน และระบุรหัสการจองที่เฉพาะเจาะจงได้",
        "postconditions": "ส่งกลับข้อมูลผลลัพธ์ของการยกเลิกการจอง",
        "args": {
            "book_id": "รหัสการจอง"
        },
        "returns": "ข้อมูลผลลัพธ์ของการยกเลิกการจอง",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "การนัดหมายบริการ - นัดหมายเวลาบริการหลังจากเลือกร้านค้าแล้ว",
        "preconditions": "อยู่ในสถานการณ์ที่ไปถึงร้าน, ระบุรหัสร้านค้าได้เพียงหนึ่งเดียว, ร้านค้ารองรับการนัดหมายบริการ",
        "postconditions": "ส่งคืนข้อมูลการนัดหมายบริการ (รวมถึง reservation_id), แจ้งให้ผู้ใช้ไปยังร้านค้าตามเวลานัดหมายเพื่อรับบริการ",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "shop_id": "รหัสร้านค้า",
            "time": "เวลานัดหมายบริการ รูปแบบ: %Y-%m-%d %H:%M:%S",
            "customer_count": "จำนวนผู้ที่นัดหมายบริการ, ค่าเริ่มต้นคือ 1 คน"
        },
        "returns": "ข้อมูลการนัดหมายบริการ",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "แก้ไขข้อมูลการจองการบริโภคที่ค้นหาได้ในสถานการณ์ที่มาถึงร้าน",
        "preconditions": "อยู่ในสถานการณ์ที่มาถึงร้าน ค้นหาคำสั่งจองการบริโภคของผู้ใช้ที่รอการแก้ไข ระบุ reservation_id ที่ไม่ซ้ำกันเพียงหนึ่งเดียว ผู้ใช้แก้ไขเวลาและจำนวนคนสำหรับการจองการบริโภค",
        "postconditions": "แสดงข้อมูลการจองการบริโภคที่แก้ไขแล้ว แจ้งให้ผู้ใช้ทราบให้ไปบริโภคที่ร้านค้าตามเวลาที่ตกลงกัน",
        "args": {
            "reservation_id": "รหัสการจองการบริโภค",
            "time": "เวลาการจองการบริโภคที่แก้ไขแล้ว รูปแบบที่ถูกต้องคือ %Y-%m-%d %H:%M:%S",
            "customer_count": "จำนวนคนสำหรับการจองการบริโภคที่แก้ไขแล้ว"
        },
        "returns": "ข้อมูลการจองที่แก้ไขแล้ว",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "ยกเลิกการจองใช้บริการที่ร้าน",
        "preconditions": "อยู่ในบริบทของการมาใช้บริการที่ร้าน และระบุรหัสการจองใช้บริการเพียงหนึ่งเดียว",
        "postconditions": "ส่งกลับข้อมูลผลลัพธ์การยกเลิกการจองใช้บริการ",
        "args": {
            "reservation_id": "รหัสการจองใช้บริการ"
        },
        "returns": "ข้อมูลผลลัพธ์การยกเลิกการจองใช้บริการ",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "ดึงข้อมูลคำสั่งซื้อที่มาที่ร้านทั้งหมดของผู้ใช้ที่ระบุ",
        "preconditions": "อยู่ในสถานการณ์ที่มาที่ร้าน และต้องการดูคำสั่งซื้อที่มาที่ร้านทั้งหมด",
        "postconditions": "ส่งกลับข้อมูลรายละเอียดของคำสั่งซื้อที่มาที่ร้านทั้งหมด",
        "args": {
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "ข้อมูลรายละเอียดของคำสั่งซื้อที่มาที่ร้านทั้งหมดของผู้ใช้ปัจจุบัน",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "ดึงข้อมูลรายการใช้จ่ายจากการนัดหมายเข้าร้านทั้งหมดของผู้ใช้ที่ระบุ",
        "preconditions": "อยู่ในสถานการณ์เข้าร้าน และต้องการดูรายการใช้จ่ายจากการนัดหมายเข้าร้านทั้งหมด",
        "postconditions": "ส่งกลับข้อมูลรายละเอียดของรายการใช้จ่ายจากการนัดหมายเข้าร้านทั้งหมด",
        "args": {
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "ข้อมูลรายละเอียดของรายการใช้จ่ายจากการนัดหมายเข้าร้านทั้งหมดของผู้ใช้ปัจจุบัน",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "รับข้อมูลการจองที่นั่งในร้านทั้งหมดของผู้ใช้ที่ระบุ",
        "preconditions": "อยู่ในสถานการณ์ที่ร้าน ต้องการดูการจองที่นั่งในร้านทั้งหมด",
        "postconditions": "ส่งกลับรายละเอียดทั้งหมดของการจองที่นั่งในร้าน",
        "args": {
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "รายละเอียดทั้งหมดของการจองที่นั่งในร้านของผู้ใช้ปัจจุบัน",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "ค้นหาข้อมูลการจองที่นั่งของผู้ใช้ เมื่อ book_id เป็น None จะส่งคืนการจองที่นั่งทั้งหมดของผู้ใช้ เมื่อ book_id ไม่ใช่ None จะส่งคืนการจองที่นั่งที่ระบุ",
        "preconditions": "อยู่ในสถานการณ์ที่มาถึงร้าน เมื่อ book_id เป็น None จะส่งคืนการจองที่นั่งทั้งหมดของผู้ใช้ เมื่อ book_id ไม่ใช่ None จะส่งคืนการจองที่นั่งที่ระบุ",
        "postconditions": "ส่งคืนข้อมูลการจองที่นั่ง เพื่อความสะดวกในการแก้ไข/ยกเลิกในภายหลัง",
        "args": {
            "user_id": "ไอดีผู้ใช้",
            "book_id": "ไอดีการจองที่นั่ง พารามิเตอร์เสริม ค่าเริ่มต้นคือ None"
        },
        "returns": "ข้อมูลการจองที่นั่ง การจองที่นั่งหลายรายการคั่นด้วยตัวอักษรขึ้นบรรทัดใหม่",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "สอบถามข้อมูลการจองและการใช้จ่ายของผู้ใช้",
        "preconditions": "อยู่ในสถานการณ์ที่ลูกค้ามาถึงร้าน เมื่อ reservation_id เป็น None จะส่งคืนข้อมูลการจองและการใช้จ่ายทั้งหมดของผู้ใช้ เมื่อ reservation_id ไม่ใช่ None จะส่งคืนข้อมูลการจองและการใช้จ่ายที่ระบุ",
        "postconditions": "ส่งคืนข้อมูลการจองและการใช้จ่าย เพื่อความสะดวกในการแก้ไข/ยกเลิกในภายหลัง",
        "args": {
            "user_id": "ไอดีผู้ใช้",
            "reservation_id": "ไอดีการจองและการใช้จ่าย, พารามิเตอร์เสริม, ค่าเริ่มต้นคือ None"
        },
        "returns": "ข้อมูลการจองและการใช้จ่าย, การจองหลายรายการคั่นด้วยตัวอักษรขึ้นบรรทัดใหม่",
        "tool_type": "READ"
    },
}

# Tool descriptions - Hindi version
TOOL_DESCRIPTIONS_HI = {
    "instore_shop_search_recommend": {
        "description": "स्टोर विजिट परिदृश्य में, उपयोगकर्ता (अस्पष्ट आवश्यकताएं, न तो विशिष्ट पैकेज स्पष्ट किया है और न ही विशिष्ट व्यापारी), उपयोगकर्ता की व्यक्तिगत पसंद और व्यापारी टैग आदि की जानकारी को संयोजित करके, कई व्यापारियों की सिफारिश करने की आवश्यकता है",
        "preconditions": "स्टोर विजिट परिदृश्य में होना, व्यापारी से संबंधित कीवर्ड प्राप्त करना",
        "postconditions": "व्यापारियों की सूची लौटाएं, उपयोगकर्ता को व्यापारी चुनने और पुष्टि करने के लिए मार्गदर्शन करें, व्यापारी की पुष्टि होने के बाद उपयोगकर्ता को पैकेज चुनने और पुष्टि करने की आवश्यकता है",
        "args": {
            "keywords": "व्यापारी का वर्णन करने वाले कीवर्ड"
        },
        "returns": "संरचित आउटपुट के रूप में व्यापारी जानकारी",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "स्टोर विजिट परिदृश्य में, उपयोगकर्ता की अभिव्यक्ति के आधार पर पैकेज का वर्णन करने वाले कीवर्ड निकाले जा सकते हैं, और कई पैकेजों को खोजा या अनुशंसित किया जा सकता है",
        "preconditions": "स्टोर विजिट परिदृश्य में होना, पैकेज से संबंधित कीवर्ड",
        "postconditions": "पैकेज सूची वापस करें, उपयोगकर्ता को पैकेज चुनने और ऑर्डर बनाने के लिए मार्गदर्शन करें",
        "args": {
            "keywords": "पैकेज का वर्णन करने वाले कीवर्ड"
        },
        "returns": "संरचित आउटपुट पैकेज जानकारी",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "स्टोर पर ऑर्डर जमा करें",
        "preconditions": "स्टोर परिदृश्य में, एक अद्वितीय विक्रेता आईडी और एक या अधिक उत्पाद आईडी निर्धारित करें",
        "postconditions": "ऑर्डर जानकारी लौटाएं (order_id सहित), उपयोगकर्ता से पूछें कि क्या वे ऑर्डर का भुगतान करना चाहते हैं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "shop_id": "विक्रेता आईडी",
            "product_id": "पैकेज आईडी",
            "quantity": "मात्रा"
        },
        "returns": "ऑर्डर जानकारी",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "स्टोर पर पहुंचने के परिदृश्य में, पिछले संदर्भ में ऑर्डर की जानकारी है, उपयोगकर्ता भुगतान पूरा होने की बात करता है, या पुनः भुगतान पूरा होने की बात करता है।",
        "preconditions": "स्टोर पर पहुंचने के परिदृश्य में होना, उपयोगकर्ता द्वारा भुगतान कार्य पूरा करने का व्यक्त करना, ऑर्डर बनना पूर्ण होना और भुगतान चरण में प्रवेश करना｜उपयोगकर्ता द्वारा पुनः भुगतान का संकेत देना।",
        "postconditions": "भुगतान परिणाम की जानकारी लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम की जानकारी आउटपुट करें।",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "उपयोगकर्ता ऑर्डर रद्द करता है, या उपयोगकर्ता भुगतान रद्द करता है। पहले से रद्द स्थिति में मौजूद ऑर्डर को फिर से रद्द करना प्रतिबंधित है।",
        "preconditions": "स्टोर परिदृश्य में, ऑर्डर स्थिति जांचें और सुनिश्चित करें कि ऑर्डर स्थिति cancelled न हो।",
        "postconditions": "ऑर्डर रद्द करने का परिणाम जानकारी लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर रद्द करने का परिणाम जानकारी आउटपुट करें।",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "सीट आरक्षण - चुने गए व्यापारी के बाद भौतिक सीट/टेबल आरक्षित करें",
        "preconditions": "स्टोर आगमन परिदृश्य में, एक अद्वितीय व्यापारी आईडी निर्धारित करें, व्यापारी सीट आरक्षण सेवा का समर्थन करता है",
        "postconditions": "सीट आरक्षण जानकारी लौटाएं (book_id सहित), यदि आरक्षण शुल्क का भुगतान करने की आवश्यकता है, तो उपयोगकर्ता से पूछें कि क्या वे भुगतान करना चाहते हैं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "shop_id": "व्यापारी आईडी",
            "time": "सीट आरक्षण समय प्रारूप: %Y-%m-%d %H:%M:%S",
            "customer_count": "सीट आरक्षण के लिए लोगों की संख्या, डिफ़ॉल्ट 1 व्यक्ति है"
        },
        "returns": "सीट आरक्षण जानकारी",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "स्टोर पर सीट आरक्षण भुगतान",
        "preconditions": "स्टोर पर मौजूदगी के परिदृश्य में, एक अद्वितीय बुकिंग आईडी निर्धारित करें",
        "postconditions": "भुगतान परिणाम जानकारी लौटाएं",
        "args": {
            "book_id": "बुकिंग आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "स्टोर पर पहुंचकर आरक्षण रद्द करें",
        "preconditions": "स्टोर पर पहुंचने के परिदृश्य में, एक अद्वितीय आरक्षण आईडी निर्धारित करें",
        "postconditions": "आरक्षण रद्द करने का परिणाम की जानकारी लौटाएं",
        "args": {
            "book_id": "आरक्षण आईडी"
        },
        "returns": "आरक्षण रद्द करने का परिणाम की जानकारी",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "सेवा बुकिंग - चुने गए विक्रेता के बाद सेवा समय बुक करें",
        "preconditions": "स्टोर विजिट परिदृश्य में, एक विशिष्ट विक्रेता आईडी निर्धारित करें, विक्रेता सेवा बुकिंग का समर्थन करता है",
        "postconditions": "सेवा बुकिंग जानकारी वापस करें (reservation_id सहित), उपयोगकर्ता को निर्धारित समय पर सेवा प्राप्त करने के लिए विक्रेता के पास जाने के लिए सूचित करें",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "shop_id": "विक्रेता आईडी",
            "time": "सेवा बुकिंग समय प्रारूप: %Y-%m-%d %H:%M:%S",
            "customer_count": "सेवा बुकिंग ग्राहक संख्या, डिफ़ॉल्ट 1 व्यक्ति"
        },
        "returns": "सेवा बुकिंग जानकारी",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "स्टोर आगमन परिदृश्य में क्वेरी की गई रिज़र्वेशन खपत जानकारी को संशोधित करें",
        "preconditions": "स्टोर आगमन परिदृश्य में रहें, उपयोगकर्ता के संशोधन लंबित रिज़र्वेशन खपत ऑर्डर को क्वेरी करें, एक अद्वितीय reservation_id निर्धारित करें, उपयोगकर्ता रिज़र्वेशन खपत के समय और लोगों की संख्या को संशोधित करता है",
        "postconditions": "संशोधित रिज़र्वेशन खपत जानकारी आउटपुट करें, उपयोगकर्ता को सहमत समय पर व्यापारी के पास खपत के लिए सूचित करें",
        "args": {
            "reservation_id": "रिज़र्वेशन खपत आईडी",
            "time": "संशोधित रिज़र्वेशन खपत समय सही प्रारूप %Y-%m-%d %H:%M:%S है",
            "customer_count": "संशोधित रिज़र्वेशन खपत लोगों की संख्या"
        },
        "returns": "संशोधित रिज़र्वेशन जानकारी",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "स्टोर विजिट अपॉइंटमेंट खपत रद्द करना",
        "preconditions": "स्टोर विजिट परिदृश्य में, एक अद्वितीय अपॉइंटमेंट खपत आईडी निर्धारित करें",
        "postconditions": "अपॉइंटमेंट खपत रद्द करने के परिणाम की जानकारी लौटाएं",
        "args": {
            "reservation_id": "अपॉइंटमेंट खपत आईडी"
        },
        "returns": "अपॉइंटमेंट खपत रद्द करने के परिणाम की जानकारी",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "निर्दिष्ट उपयोगकर्ता के सभी स्टोर विज़िट ऑर्डर प्राप्त करें",
        "preconditions": "स्टोर विज़िट परिदृश्य में, सभी स्टोर विज़िट ऑर्डर देखने की आवश्यकता है",
        "postconditions": "सभी स्टोर विज़िट ऑर्डर की विस्तृत जानकारी लौटाएं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "वर्तमान उपयोगकर्ता के सभी स्टोर विज़िट ऑर्डर की विस्तृत जानकारी",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "निर्दिष्ट उपयोगकर्ता की सभी स्टोर विजिट अपॉइंटमेंट खपत प्राप्त करें",
        "preconditions": "स्टोर विजिट परिदृश्य में, सभी स्टोर विजिट अपॉइंटमेंट खपत देखने की आवश्यकता है",
        "postconditions": "सभी स्टोर विजिट अपॉइंटमेंट खपत की विस्तृत जानकारी लौटाएं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "वर्तमान उपयोगकर्ता की सभी स्टोर विजिट अपॉइंटमेंट खपत की विस्तृत जानकारी",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "निर्दिष्ट उपयोगकर्ता के सभी स्टोर विजिट सीट आरक्षण प्राप्त करें",
        "preconditions": "स्टोर विजिट परिदृश्य में, सभी स्टोर विजिट सीट आरक्षण देखने की आवश्यकता है",
        "postconditions": "सभी स्टोर विजिट सीट आरक्षण की विस्तृत जानकारी लौटाएं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "वर्तमान उपयोगकर्ता के सभी स्टोर विजिट सीट आरक्षण की विस्तृत जानकारी",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "उपयोगकर्ता की सीट आरक्षण जानकारी जांचें। जब book_id None हो, तो उपयोगकर्ता के सभी सीट आरक्षण लौटाएं। जब book_id None न हो, तो निर्दिष्ट सीट आरक्षण लौटाएं।",
        "preconditions": "स्टोर पर पहुंचने के परिदृश्य में। जब book_id None हो, तो उपयोगकर्ता के सभी सीट आरक्षण लौटाएं। जब book_id None न हो, तो निर्दिष्ट सीट आरक्षण लौटाएं।",
        "postconditions": "सीट आरक्षण जानकारी लौटाएं, बाद में संशोधन या रद्द करने की सुविधा के लिए।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "book_id": "सीट आरक्षण आईडी, वैकल्पिक पैरामीटर, डिफ़ॉल्ट रूप से None"
        },
        "returns": "सीट आरक्षण जानकारी, एकाधिक सीट आरक्षण न्यूलाइन कैरेक्टर द्वारा अलग किए गए",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "उपयोगकर्ता की अपॉइंटमेंट खपत जानकारी जांचें",
        "preconditions": "स्टोर पहुंचने के परिदृश्य में, जब reservation_id None हो, तो उपयोगकर्ता की सभी अपॉइंटमेंट खपत वापस करें, जब reservation_id None न हो, तो निर्दिष्ट अपॉइंटमेंट खपत वापस करें",
        "postconditions": "अपॉइंटमेंट खपत जानकारी लौटाएं, जिससे बाद में संशोधन या रद्द करना आसान हो",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "reservation_id": "अपॉइंटमेंट खपत आईडी, वैकल्पिक पैरामीटर, डिफ़ॉल्ट रूप से None"
        },
        "returns": "अपॉइंटमेंट खपत जानकारी, एकाधिक अपॉइंटमेंट न्यूलाइन द्वारा अलग किए गए",
        "tool_type": "READ"
    },
}

# Tool descriptions - Arabic version
TOOL_DESCRIPTIONS_AR = {
    "instore_shop_search_recommend": {
        "description": "في سيناريو الزيارة إلى المتجر، المستخدم (متطلبات غامضة، لم يحدد باقة معينة | لم يحدد متجراً معيناً)، يحتاج إلى توصية بعدة متاجر بالجمع بين تفضيلات المستخدم الشخصية وعلامات المتجر وغيرها من المعلومات",
        "preconditions": "في سيناريو الزيارة إلى المتجر، الحصول على الكلمات الرئيسية المتعلقة بالمتجر",
        "postconditions": "إرجاع قائمة المتاجر، توجيه المستخدم لاختيار وتحديد متجر، بعد تحديد المتجر يحتاج المستخدم إلى اختيار وتحديد الباقة",
        "args": {
            "keywords": "الكلمات الرئيسية التي تصف المتجر"
        },
        "returns": "معلومات المتجر المُخرجة بشكل منظم",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "في سيناريو الوصول إلى المتجر، يمكن استخراج الكلمات الرئيسية التي تصف الباقات من تعبيرات المستخدم، والبحث عن أو توصية عدة باقات",
        "preconditions": "في سيناريو الوصول إلى المتجر، وكلمات رئيسية تتعلق بالباقات",
        "postconditions": "إرجاع قائمة الباقات، وتوجيه المستخدم لاختيار باقة وإنشاء طلب",
        "args": {
            "keywords": "الكلمات الرئيسية التي تصف الباقات"
        },
        "returns": "معلومات الباقات المخرجة بشكل هيكلي",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "تقديم طلب في المتجر",
        "preconditions": "في سيناريو المتجر، وتحديد معرف متجر فريد ومعرف منتج واحد أو أكثر",
        "postconditions": "إرجاع معلومات الطلب (بما في ذلك order_id)، وسؤال المستخدم عما إذا كان يريد دفع الطلب",
        "args": {
            "user_id": "معرف المستخدم",
            "shop_id": "معرف المتجر",
            "product_id": "معرف الباقة",
            "quantity": "الكمية"
        },
        "returns": "معلومات الطلب",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "في سياق المتجر، توجد معلومات الطلب في السياق، ويعبر المستخدم عن اكتمال الدفع، أو اكتمال إعادة الدفع",
        "preconditions": "في سياق المتجر، يعبر المستخدم عن إتمام عملية الدفع، وتم إنشاء الطلب ودخل مرحلة الدفع｜أو يشير المستخدم إلى إعادة الدفع",
        "postconditions": "إرجاع معلومات نتيجة الدفع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "إخراج معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "يقوم المستخدم بإلغاء الطلب، أو يقوم المستخدم بإلغاء الدفع. يحظر إلغاء الطلب مرة أخرى إذا كانت حالته ملغاة بالفعل.",
        "preconditions": "في سيناريو الحضور إلى المتجر، قم بالاستعلام عن حالة الطلب، وتأكد من أن حالة الطلب ليست ملغاة",
        "postconditions": "إرجاع معلومات نتيجة إلغاء الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "إخراج معلومات نتيجة إلغاء الطلب",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "حجز المقاعد - حجز مقعد/طاولة مادية بعد اختيار المتجر",
        "preconditions": "في سيناريو الوصول إلى المتجر، تحديد معرف متجر فريد، يدعم المتجر خدمة حجز المقاعد",
        "postconditions": "إرجاع معلومات حجز المقاعد (تتضمن book_id)، إذا تطلب الأمر دفع رسوم الحجز، اسأل المستخدم عما إذا كان سيدفع",
        "args": {
            "user_id": "معرف المستخدم",
            "shop_id": "معرف المتجر",
            "time": "وقت حجز المقاعد التنسيق: %Y-%m-%d %H:%M:%S",
            "customer_count": "عدد الأشخاص لحجز المقاعد، الافتراضي شخص واحد"
        },
        "returns": "معلومات حجز المقاعد",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "دفع حجز المقعد عند الوصول إلى المتجر",
        "preconditions": "في سيناريو الوصول إلى المتجر، وتحديد معرف حجز فريد",
        "postconditions": "إرجاع معلومات نتيجة الدفع",
        "args": {
            "book_id": "معرف حجز المقعد"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "إلغاء الحجز عند الوصول إلى المتجر",
        "preconditions": "في سيناريو الوصول إلى المتجر، وتحديد معرف الحجز بشكل فريد",
        "postconditions": "إرجاع معلومات نتيجة إلغاء الحجز",
        "args": {
            "book_id": "معرف الحجز"
        },
        "returns": "معلومات نتيجة إلغاء الحجز",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "حجز الخدمة - تحديد وقت الخدمة بعد اختيار المتجر",
        "preconditions": "في سيناريو الوصول إلى المتجر، وتحديد معرف متجر فريد، ودعم المتجر لحجز الخدمة",
        "postconditions": "إرجاع معلومات حجز الخدمة (تتضمن reservation_id)، وإخطار المستخدم بالذهاب إلى المتجر في الوقت المتفق عليه لتلقي الخدمة",
        "args": {
            "user_id": "معرف المستخدم",
            "shop_id": "معرف المتجر",
            "time": "وقت حجز الخدمة التنسيق: %Y-%m-%d %H:%M:%S",
            "customer_count": "عدد الأشخاص لحجز الخدمة، الافتراضي شخص واحد"
        },
        "returns": "معلومات حجز الخدمة",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "تعديل معلومات حجز الاستهلاك المستعلم عنها في سيناريو الوصول إلى المتجر",
        "preconditions": "في سيناريو الوصول إلى المتجر، قم بالاستعلام عن طلب حجز الاستهلاك الخاص بالمستخدم المراد تعديله، وحدد معرّف حجز فريد (reservation_id)، حيث يقوم المستخدم بتعديل وقت وعدد أشخاص حجز الاستهلاك",
        "postconditions": "إخراج معلومات حجز الاستهلاك المعدلة، وإعلام المستخدم بالذهاب إلى المتجر للاستهلاك وفقًا للوقت المتفق عليه",
        "args": {
            "reservation_id": "معرّف حجز الاستهلاك",
            "time": "وقت حجز الاستهلاك المعدل، التنسيق الصحيح هو %Y-%m-%d %H:%M:%S",
            "customer_count": "عدد أشخاص حجز الاستهلاك المعدل"
        },
        "returns": "معلومات الحجز المعدلة",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "إلغاء حجز الاستهلاك في المتجر",
        "preconditions": "في سيناريو المتجر، تحديد معرف استهلاك الحجز الفريد",
        "postconditions": "إرجاع معلومات نتيجة إلغاء حجز الاستهلاك",
        "args": {
            "reservation_id": "معرف استهلاك الحجز"
        },
        "returns": "معلومات نتيجة إلغاء حجز الاستهلاك",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "الحصول على جميع طلبات زيارة المتجر للمستخدم المحدد",
        "preconditions": "في سيناريو زيارة المتجر، وتحتاج إلى عرض جميع طلبات الزيارة",
        "postconditions": "إرجاع المعلومات التفصيلية لجميع طلبات زيارة المتجر",
        "args": {
            "user_id": "معرّف المستخدم"
        },
        "returns": "المعلومات التفصيلية لجميع طلبات زيارة المتجر الخاصة بالمستخدم الحالي",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "الحصول على جميع سجلات الاستهلاك لمواعيد زيارة المتجر للمستخدم المحدد",
        "preconditions": "في سيناريو زيارة المتجر، وهناك حاجة لعرض جميع سجلات الاستهلاك لمواعيد زيارة المتجر",
        "postconditions": "إرجاع المعلومات التفصيلية لجميع سجلات الاستهلاك لمواعيد زيارة المتجر",
        "args": {
            "user_id": "معرف المستخدم"
        },
        "returns": "المعلومات التفصيلية لجميع سجلات الاستهلاك لمواعيد زيارة المتجر للمستخدم الحالي",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "الحصول على جميع حجوزات المقاعد داخل المتجر لمستخدم محدد",
        "preconditions": "عند التواجد في سيناريو زيارة المتجر، وتحتاج إلى عرض جميع حجوزات المقاعد داخل المتجر",
        "postconditions": "إرجاع التفاصيل الكاملة لجميع حجوزات المقاعد داخل المتجر",
        "args": {
            "user_id": "معرف المستخدم"
        },
        "returns": "التفاصيل الكاملة لجميع حجوزات المقاعد داخل المتجر الخاصة بالمستخدم الحالي",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "استعلام عن معلومات حجز مقعد المستخدم. عندما يكون book_id هو None، يتم إرجاع جميع حجوزات مقاعد المستخدم، وعندما لا يكون book_id هو None، يتم إرجاع حجز المقعد المحدد.",
        "preconditions": "في سيناريو الوصول إلى المتجر. عندما يكون book_id هو None، يتم إرجاع جميع حجوزات مقاعد المستخدم، وعندما لا يكون book_id هو None، يتم إرجاع حجز المقعد المحدد.",
        "postconditions": "إرجاع معلومات حجز المقعد، لتسهيل التعديل أو الإلغاء لاحقًا.",
        "args": {
            "user_id": "معرف المستخدم",
            "book_id": "معرف حجز المقعد، معلمة اختيارية، القيمة الافتراضية هي None"
        },
        "returns": "معلومات حجز المقعد، يتم فصل حجوزات المقاعد المتعددة بواسطة محرف سطر جديد",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "الاستعلام عن معلومات حجز واستهلاك المستخدم",
        "preconditions": "في سيناريو التواجد في المتجر، إذا كان reservation_id برابرًا بـ None، يتم إرجاع جميع عمليات استهلاك الحجز للمستخدم، وإذا لم يكن reservation_id برابرًا بـ None، يتم إرجاع استهلاك الحجز المحدد",
        "postconditions": "يتم إرجاع معلومات استهلاك الحجز لتسهيل التعديل أو الإلغاء لاحقًا",
        "args": {
            "user_id": "معرف المستخدم",
            "reservation_id": "معرف استهلاك الحجز، معامل اختياري، قيمته الافتراضية هي None"
        },
        "returns": "معلومات استهلاك الحجز، حيث يتم فصل الحجوزات المتعددة بحرف سطر جديد",
        "tool_type": "READ"
    },
}

# Tool descriptions - Russian version
TOOL_DESCRIPTIONS_RU = {
    "instore_shop_search_recommend": {
        "description": "В сценарии посещения заведения, если потребности пользователя неясны (не указан конкретный пакет | не указано конкретное заведение), необходимо рекомендовать несколько заведений на основе личных предпочтений пользователя, тегов заведений и другой информации.",
        "preconditions": "Находится в сценарии посещения заведения, получены ключевые слова, связанные с заведениями.",
        "postconditions": "Возвращает список заведений, направляет пользователя к выбору и подтверждению заведения; после подтверждения заведения пользователь должен выбрать и подтвердить пакет.",
        "args": {
            "keywords": "Ключевые слова, описывающие заведения."
        },
        "returns": "Структурированная информация о заведениях.",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "В сценарии посещения заведения можно извлечь ключевые слова, описывающие пакеты услуг, из высказываний пользователя, чтобы найти или рекомендовать несколько пакетов",
        "preconditions": "Сценарий посещения заведения, ключевые слова, связанные с пакетами услуг",
        "postconditions": "Возвращает список пакетов услуг, направляет пользователя к выбору пакета и созданию заказа",
        "args": {
            "keywords": "Ключевые слова, описывающие пакет услуг"
        },
        "returns": "Структурированная информация о пакетах услуг",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Оформление заказа в магазине",
        "preconditions": "Сценарий посещения магазина, определен уникальный идентификатор магазина и один или несколько идентификаторов товаров",
        "postconditions": "Возвращает информацию о заказе (включая order_id), спрашивает пользователя, хочет ли он оплатить заказ",
        "args": {
            "user_id": "Идентификатор пользователя",
            "shop_id": "Идентификатор магазина",
            "product_id": "Идентификатор набора",
            "quantity": "Количество"
        },
        "returns": "Информация о заказе",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "В сценарии посещения магазина, при наличии информации о заказе в предыдущем контексте, пользователь сообщает о завершении оплаты или о повторной оплате",
        "preconditions": "Сценарий посещения магазина, пользователь сообщает о завершении операции оплаты, заказ создан и перешел к этапу оплаты｜пользователь сообщает о повторной оплате",
        "postconditions": "Возвращает информацию о результате оплаты",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Выводит информацию о результате оплаты",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "Пользователь отменяет заказ или платеж. Запрещено повторно отменять заказы, уже находящиеся в состоянии «отменено».",
        "preconditions": "В сценарии посещения магазина запросить статус заказа и убедиться, что он не «cancelled».",
        "postconditions": "Возвращает информацию о результате отмены заказа.",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Выводит информацию о результате отмены заказа.",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Бронирование мест — бронирование физических мест/столов после выбора заведения",
        "preconditions": "В сценарии посещения заведения, определен уникальный ID заведения, заведение поддерживает услугу бронирования мест",
        "postconditions": "Возвращает информацию о бронировании места (включая book_id). Если требуется оплата бронирования, спросить пользователя, хочет ли он оплатить",
        "args": {
            "user_id": "ID пользователя",
            "shop_id": "ID заведения",
            "time": "Время бронирования места. Формат: %Y-%m-%d %H:%M:%S",
            "customer_count": "Количество человек для бронирования, по умолчанию 1 человек"
        },
        "returns": "Информация о бронировании места",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Оплата бронирования стола в заведении",
        "preconditions": "Нахождение в сценарии посещения заведения, определен уникальный идентификатор бронирования",
        "postconditions": "Возвращает информацию о результате оплаты",
        "args": {
            "book_id": "Идентификатор бронирования"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Отмена бронирования стола в ресторане",
        "preconditions": "Пользователь находится в ресторане, определен уникальный идентификатор бронирования",
        "postconditions": "Возвращает информацию о результате отмены бронирования",
        "args": {
            "book_id": "Идентификатор бронирования стола"
        },
        "returns": "Информация о результате отмены бронирования",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Запись на услугу - назначение времени услуги после выбора магазина",
        "preconditions": "Сценарий посещения магазина, определен уникальный ID магазина, магазин поддерживает запись на услуги",
        "postconditions": "Возвращает информацию о записи на услугу (включая reservation_id), уведомляет пользователя о необходимости прибыть в магазин в согласованное время для получения услуги",
        "args": {
            "user_id": "ID пользователя",
            "shop_id": "ID магазина",
            "time": "Время записи на услугу. Формат: %Y-%m-%d %H:%M:%S",
            "customer_count": "Количество людей для записи на услугу, по умолчанию 1 человек"
        },
        "returns": "Информация о записи на услугу",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Изменение информации о забронированном потреблении, полученной в результате запроса, в сценарии посещения магазина",
        "preconditions": "Сценарий посещения магазина, запрос заказа на бронирование потребления пользователя, подлежащего изменению, определение уникального reservation_id, изменение пользователем времени и количества человек для бронирования",
        "postconditions": "Вывод измененной информации о бронировании потребления, уведомление пользователя о необходимости посетить магазин в согласованное время",
        "args": {
            "reservation_id": "ID бронирования потребления",
            "time": "Измененное время бронирования потребления. Правильный формат: %Y-%m-%d %H:%M:%S",
            "customer_count": "Измененное количество человек для бронирования потребления"
        },
        "returns": "Измененная информация о бронировании",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Отмена бронирования потребления в магазине",
        "preconditions": "Находится в сценарии посещения магазина, определен уникальный идентификатор бронирования потребления",
        "postconditions": "Возвращает информацию о результате отмены бронирования потребления",
        "args": {
            "reservation_id": "Идентификатор бронирования потребления"
        },
        "returns": "Информация о результате отмены бронирования потребления",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Получить все заказы конкретного пользователя для получения в магазине",
        "preconditions": "Находитесь в сценарии получения в магазине, необходимо просмотреть все заказы для получения в магазине",
        "postconditions": "Возвращает подробную информацию обо всех заказах для получения в магазине",
        "args": {
            "user_id": "ID пользователя"
        },
        "returns": "Подробная информация обо всех заказах текущего пользователя для получения в магазине",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Получение всех записей о потреблении по предварительной записи для визита в магазин для указанного пользователя",
        "preconditions": "Находясь в сценарии посещения магазина, необходимо просмотреть все записи о потреблении по предварительной записи для визита в магазин",
        "postconditions": "Возвращает подробную информацию обо всех записях о потреблении по предварительной записи для визита в магазин",
        "args": {
            "user_id": "ID пользователя"
        },
        "returns": "Подробная информация обо всех записях о потреблении по предварительной записи для визита в магазин для текущего пользователя",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Получить все бронирования столиков в заведении для указанного пользователя",
        "preconditions": "Находится в сценарии посещения заведения, необходимо просмотреть все бронирования столиков",
        "postconditions": "Возвращает подробную информацию обо всех бронированиях столиков в заведении",
        "args": {
            "user_id": "ID пользователя"
        },
        "returns": "Подробная информация обо всех бронированиях столиков в заведении для текущего пользователя",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Запрос информации о бронировании места пользователем. Если book_id равен None, возвращаются все бронирования мест пользователя. Если book_id не равен None, возвращается указанное бронирование места.",
        "preconditions": "Сценарий присутствия в магазине. Если book_id равен None, возвращаются все бронирования мест пользователя. Если book_id не равен None, возвращается указанное бронирование места.",
        "postconditions": "Возвращает информацию о бронировании места, удобную для последующего изменения/отмены.",
        "args": {
            "user_id": "ID пользователя",
            "book_id": "ID бронирования места, необязательный параметр, по умолчанию None"
        },
        "returns": "Информация о бронировании места, несколько бронирований разделены символами новой строки",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Запрос информации о бронировании и потреблении пользователя",
        "preconditions": "В сценарии посещения магазина: если reservation_id равен None, возвращается вся информация о бронировании и потреблении пользователя; если reservation_id не равен None, возвращается информация о указанном бронировании",
        "postconditions": "Возвращает информацию о бронировании и потреблении для последующего изменения или отмены",
        "args": {
            "user_id": "ID пользователя",
            "reservation_id": "ID бронирования и потребления, необязательный параметр, по умолчанию None"
        },
        "returns": "Информация о бронировании и потреблении, несколько бронирований разделены символом новой строки",
        "tool_type": "READ"
    },
}

# Tool descriptions - French version
# Tool descriptions - French version
TOOL_DESCRIPTIONS_FR = {
    "instore_shop_search_recommend": {
        "description": "Dans un scénario de visite en magasin, lorsque l'utilisateur a des besoins flous (n'a pas exprimé clairement un forfait spécifique | n'a pas exprimé clairement un commerçant spécifique), il faut combiner les préférences personnelles de l'utilisateur et les étiquettes des commerçants, entre autres informations, pour recommander plusieurs commerçants.",
        "preconditions": "Être dans un scénario de visite en magasin et obtenir des mots-clés liés aux commerçants.",
        "postconditions": "Renvoyer une liste de commerçants, guider l'utilisateur pour choisir et confirmer un commerçant ; une fois le commerçant confirmé, l'utilisateur doit choisir et confirmer un forfait.",
        "args": {
            "keywords": "Mots-clés décrivant le commerçant."
        },
        "returns": "Informations sur les commerçants générées dans un format structuré.",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "Dans un scénario de visite en magasin, permet d'extraire les mots-clés décrivant les formules à partir des expressions de l'utilisateur, afin de rechercher ou de recommander plusieurs formules.",
        "preconditions": "Contexte de visite en magasin, mots-clés relatifs aux formules.",
        "postconditions": "Retourne une liste de formules, guide l'utilisateur pour sélectionner une formule et créer une commande.",
        "args": {
            "keywords": "Mots-clés décrivant les formules."
        },
        "returns": "Informations structurées sur les formules.",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "Soumission de commande en magasin",
        "preconditions": "Dans un contexte de visite en magasin, avec un identifiant de magasin unique et un ou plusieurs identifiants de produits déterminés",
        "postconditions": "Retourne les informations de commande (incluant order_id) et demande à l'utilisateur s'il souhaite payer la commande",
        "args": {
            "user_id": "Identifiant de l'utilisateur",
            "shop_id": "Identifiant du magasin",
            "product_id": "Identifiant du forfait",
            "quantity": "Quantité"
        },
        "returns": "Informations de commande",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "Dans le scénario en magasin, avec les informations de commande dans le contexte précédent, l'utilisateur indique que le paiement est effectué ou qu'un nouveau paiement est effectué",
        "preconditions": "Scénario en magasin, l'utilisateur indique avoir terminé l'opération de paiement, la commande est créée et entrée dans l'étape de paiement｜l'utilisateur indique un nouveau paiement",
        "postconditions": "Retourne les informations sur le résultat du paiement",
        "args": {
            "order_id": "ID de la commande"
        },
        "returns": "Affiche les informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "L'utilisateur annule la commande ou le paiement. Il est interdit d'annuler à nouveau une commande déjà dans l'état annulé.",
        "preconditions": "Dans le scénario d'arrivée en magasin, vérifier le statut de la commande pour s'assurer qu'il n'est pas « cancelled »",
        "postconditions": "Retourne les informations sur le résultat de l'annulation de la commande",
        "args": {
            "order_id": "Identifiant de la commande"
        },
        "returns": "Affiche les informations sur le résultat de l'annulation de la commande",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "Réservation de place - Réserver un siège physique ou une table après avoir sélectionné un commerçant",
        "preconditions": "Contexte de visite en magasin, identifiant unique du commerçant déterminé, le commerçant prend en charge le service de réservation de places",
        "postconditions": "Retourne les informations de réservation de place (incluant book_id), si des frais de réservation sont requis, demander à l'utilisateur s'il souhaite procéder au paiement",
        "args": {
            "user_id": "Identifiant de l'utilisateur",
            "shop_id": "Identifiant du commerçant",
            "time": "Heure de réservation de place Format : %Y-%m-%d %H:%M:%S",
            "customer_count": "Nombre de personnes pour la réservation de place, par défaut 1 personne"
        },
        "returns": "Informations de réservation de place",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "Paiement de la réservation de siège en magasin",
        "preconditions": "Être dans le contexte d'une visite en magasin, déterminer un identifiant de réservation unique",
        "postconditions": "Retourne les informations sur le résultat du paiement",
        "args": {
            "book_id": "Identifiant de réservation de siège"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "Annuler la réservation sur place",
        "preconditions": "Dans le contexte d'arrivée sur place, identifier un identifiant de réservation unique",
        "postconditions": "Retourne les informations sur le résultat de l'annulation de la réservation",
        "args": {
            "book_id": "Identifiant de réservation"
        },
        "returns": "Informations sur le résultat de l'annulation de la réservation",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "Réservation de service - Réserver un créneau horaire après avoir sélectionné le commerçant",
        "preconditions": "Scénario d'arrivée en magasin, identifiant unique du commerçant déterminé, le commerçant prend en charge la réservation de services",
        "postconditions": "Retourne les informations de réservation de service (incluant reservation_id), notifie l'utilisateur de se rendre chez le commerçant à l'heure convenue pour recevoir le service",
        "args": {
            "user_id": "Identifiant de l'utilisateur",
            "shop_id": "Identifiant du commerçant",
            "time": "Heure de réservation de service Format : %Y-%m-%d %H:%M:%S",
            "customer_count": "Nombre de personnes pour la réservation de service, par défaut 1 personne"
        },
        "returns": "Informations de réservation de service",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "Modification des informations de réservation de consommation trouvées dans le scénario de visite en magasin",
        "preconditions": "Être dans le scénario de visite en magasin, consulter la commande de réservation de consommation à modifier par l'utilisateur, déterminer un unique reservation_id, l'utilisateur modifie l'heure et le nombre de personnes de la réservation de consommation",
        "postconditions": "Produire les informations de réservation de consommation modifiées, notifier l'utilisateur de se rendre chez le commerçant pour consommer selon l'heure convenue",
        "args": {
            "reservation_id": "ID de la réservation de consommation",
            "time": "Heure de réservation de consommation modifiée. Le format correct est %Y-%m-%d %H:%M:%S",
            "customer_count": "Nombre de personnes pour la réservation de consommation modifiée"
        },
        "returns": "Informations de réservation de consommation modifiées",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "Annulation de la consommation sur rendez-vous en magasin",
        "preconditions": "Être dans un contexte en magasin et identifier un identifiant unique de consommation sur rendez-vous",
        "postconditions": "Retourne les informations sur le résultat de l'annulation de la consommation sur rendez-vous",
        "args": {
            "reservation_id": "Identifiant de consommation sur rendez-vous"
        },
        "returns": "Informations sur le résultat de l'annulation de la consommation sur rendez-vous",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "Récupérer toutes les commandes de retrait en magasin d'un utilisateur spécifié",
        "preconditions": "Dans un scénario de retrait en magasin, nécessite de consulter toutes les commandes de retrait en magasin",
        "postconditions": "Retourne les informations détaillées de toutes les commandes de retrait en magasin",
        "args": {
            "user_id": "Identifiant de l'utilisateur"
        },
        "returns": "Informations détaillées de toutes les commandes de retrait en magasin de l'utilisateur actuel",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "Récupérer toutes les consommations liées aux rendez-vous en magasin pour un utilisateur spécifié",
        "preconditions": "Dans un scénario de visite en magasin, nécessité de consulter toutes les consommations liées aux rendez-vous en magasin",
        "postconditions": "Retourne les informations détaillées de toutes les consommations liées aux rendez-vous en magasin",
        "args": {
            "user_id": "ID de l'utilisateur"
        },
        "returns": "Informations détaillées de toutes les consommations liées aux rendez-vous en magasin de l'utilisateur actuel",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "Récupérer toutes les réservations de sièges en magasin pour un utilisateur spécifié.",
        "preconditions": "Dans le contexte d'une visite en magasin, nécessitant la consultation de toutes les réservations de sièges en magasin.",
        "postconditions": "Retourne les informations détaillées de toutes les réservations de sièges en magasin.",
        "args": {
            "user_id": "Identifiant de l'utilisateur"
        },
        "returns": "Informations détaillées de toutes les réservations de sièges en magasin de l'utilisateur actuel.",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "Consulter les informations de réservation de siège de l'utilisateur. Si book_id est None, renvoyer toutes les réservations de siège de l'utilisateur. Si book_id n'est pas None, renvoyer la réservation de siège spécifiée.",
        "preconditions": "Dans un scénario d'arrivée en magasin. Si book_id est None, renvoyer toutes les réservations de siège de l'utilisateur. Si book_id n'est pas None, renvoyer la réservation de siège spécifiée.",
        "postconditions": "Renvoie les informations de réservation de siège, facilitant les modifications/annulations ultérieures.",
        "args": {
            "user_id": "ID de l'utilisateur",
            "book_id": "ID de réservation de siège, paramètre optionnel, par défaut None"
        },
        "returns": "Informations de réservation de siège, plusieurs réservations de siège séparées par des sauts de ligne.",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "Consulter les informations de réservation et de consommation de l'utilisateur",
        "preconditions": "Dans un scénario de présence en magasin. Si reservation_id est None, renvoie toutes les consommations réservées de l'utilisateur. Si reservation_id n'est pas None, renvoie la consommation réservée spécifiée.",
        "postconditions": "Renvoie les informations de réservation de consommation, facilitant les modifications ou annulations ultérieures.",
        "args": {
            "user_id": "ID de l'utilisateur",
            "reservation_id": "ID de la réservation de consommation, paramètre optionnel, par défaut None"
        },
        "returns": "Informations de réservation de consommation, plusieurs réservations séparées par des sauts de ligne.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Japanese version
TOOL_DESCRIPTIONS_JA = {
    "instore_shop_search_recommend": {
        "description": "来店シーンにおいて、ユーザー（ニーズが曖昧で、具体的なセットメニューまたは具体的な店舗を明確に表現していない）に対し、ユーザーの個人的な好みや店舗タグなどの情報を組み合わせて、複数の店舗を推薦します。",
        "preconditions": "来店シーンであり、店舗関連のキーワードを取得していること。",
        "postconditions": "店舗リストを返却し、ユーザーに店舗の選択と確定を誘導します。店舗確定後、ユーザーはセットメニューを選択し確定する必要があります。",
        "args": {
            "keywords": "店舗を記述するキーワード"
        },
        "returns": "構造化されて出力された店舗情報",
        "tool_type": "READ"
    },

    "instore_product_search_recommend": {
        "description": "来店シーンにおいて、ユーザーの発話からセットメニューを説明するキーワードを抽出し、複数のセットメニューを検索または推薦します。",
        "preconditions": "来店シーンであり、セットメニュー関連のキーワードがあること。",
        "postconditions": "セットメニューのリストを返却し、ユーザーがセットメニューを選択し、注文を作成するよう誘導します。",
        "args": {
            "keywords": "セットメニューを説明するキーワード"
        },
        "returns": "構造化出力されたセットメニュー情報",
        "tool_type": "READ"
    },

    "create_instore_product_order": {
        "description": "来店注文の提交",
        "preconditions": "来店シーンであり、唯一の店舗 ID と 1 つ以上の商品 ID が確定されていること",
        "postconditions": "注文情報（order_id を含む）を返し、ユーザーに注文を支払うかどうかを確認する",
        "args": {
            "user_id": "ユーザー ID",
            "shop_id": "店舗 ID",
            "product_id": "セット ID",
            "quantity": "数量"
        },
        "returns": "注文情報",
        "tool_type": "WRITE"
    },

    "pay_instore_order": {
        "description": "来店シーンにおいて、文脈に注文情報があり、ユーザーが支払い完了、または再支払い完了を表明した場合",
        "preconditions": "来店シーンであり、ユーザーが支払い操作完了を表明し、注文が作成されて支払い段階にあること、またはユーザーが再支払いを表明すること",
        "postconditions": "支払い結果情報を返す",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報を出力する",
        "tool_type": "WRITE"
    },

    "instore_cancel_order": {
        "description": "ユーザーが注文をキャンセルするか、支払いをキャンセルします。すでにキャンセル済みの状態にある注文を再度キャンセルすることは禁止されています。",
        "preconditions": "来店シーンにおいて、注文状態を照会し、注文状態が cancelled ではないことを確認します。",
        "postconditions": "注文キャンセル結果情報を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文キャンセル結果情報を出力します。",
        "tool_type": "WRITE"
    },

    "instore_book": {
        "description": "席予約 - 店舗選択後に物理的な席またはテーブル席を予約します",
        "preconditions": "来店シーンであり、唯一の店舗 ID が確定しており、店舗が席予約サービスに対応していること",
        "postconditions": "席予約情報（book_id を含む）を返す。着席料の支払いが必要な場合、ユーザーに支払いを行うか確認する",
        "args": {
            "user_id": "ユーザー ID",
            "shop_id": "店舗 ID",
            "time": "席予約時間 形式：%Y-%m-%d %H:%M:%S",
            "customer_count": "席予約人数、デフォルトは 1 人"
        },
        "returns": "席予約情報",
        "tool_type": "WRITE"
    },

    "pay_instore_book": {
        "description": "店舗での座席予約決済",
        "preconditions": "来店シーンであり、唯一の予約 ID が確定していること",
        "postconditions": "決済結果情報を返す",
        "args": {
            "book_id": "予約 ID"
        },
        "returns": "決済結果情報",
        "tool_type": "WRITE"
    },

    "instore_cancel_book": {
        "description": "店舗での予約キャンセル",
        "preconditions": "店舗での状況であり、唯一の予約 ID が確定されていること",
        "postconditions": "予約キャンセル結果情報を返す",
        "args": {
            "book_id": "予約 ID"
        },
        "returns": "予約キャンセル結果情報",
        "tool_type": "WRITE"
    },

    "instore_reservation": {
        "description": "サービス予約 - 店舗選択後のサービス時間予約",
        "preconditions": "来店シーンであり、唯一の店舗 ID が確定しており、店舗がサービス予約に対応していること",
        "postconditions": "サービス予約情報（reservation_id を含む）を返し、ユーザーに約定時間に店舗へ来店してサービスを受けるよう通知する",
        "args": {
            "user_id": "ユーザー ID",
            "shop_id": "店舗 ID",
            "time": "サービス予約時間 形式：%Y-%m-%d %H:%M:%S",
            "customer_count": "サービス予約人数、デフォルトは 1 人"
        },
        "returns": "サービス予約情報",
        "tool_type": "WRITE"
    },

    "instore_modify_reservation": {
        "description": "来店シーンにおいて、検索された予約消費情報を変更します",
        "preconditions": "来店シーンであること。ユーザーの変更対象となる予約消費オーダーを検索し、固有の reservation_id を特定していること。ユーザーが予約消費の時間と人数を変更すること",
        "postconditions": "変更後の予約消費情報を出力し、ユーザーに約定された時間に店舗で消費するよう通知します",
        "args": {
            "reservation_id": "予約消費 ID",
            "time": "変更後の予約消費時間 正しい形式は %Y-%m-%d %H:%M:%S",
            "customer_count": "変更後の予約消費人数"
        },
        "returns": "変更後の予約情報",
        "tool_type": "WRITE"
    },

    "instore_cancel_reservation": {
        "description": "来店予約消費のキャンセル",
        "preconditions": "来店シーンであり、一意な予約消費 ID を特定していること",
        "postconditions": "予約消費キャンセルの結果情報を返す",
        "args": {
            "reservation_id": "予約消費 ID"
        },
        "returns": "予約消費キャンセルの結果情報",
        "tool_type": "WRITE"
    },

    "get_instore_orders": {
        "description": "指定されたユーザーのすべての来店注文を取得する",
        "preconditions": "来店シーンであり、すべての来店注文を確認する必要がある場合",
        "postconditions": "すべての来店注文の詳細情報を返す",
        "args": {
            "user_id": "ユーザー ID"
        },
        "returns": "現在のユーザーのすべての来店注文の詳細情報",
        "tool_type": "READ"
    },

    "get_instore_reservations": {
        "description": "指定されたユーザーのすべての来店予約消費を取得する",
        "preconditions": "来店シーンであり、すべての来店予約消費を確認する必要がある場合",
        "postconditions": "すべての来店予約消費の詳細情報を返す",
        "args": {
            "user_id": "ユーザー ID"
        },
        "returns": "現在のユーザーのすべての来店予約消費の詳細情報",
        "tool_type": "READ"
    },

    "get_instore_books": {
        "description": "指定されたユーザーのすべての来店座位予約を取得する",
        "preconditions": "来店シーンであり、すべての来店座位予約を確認する必要がある",
        "postconditions": "すべての来店座位予約の詳細情報を返す",
        "args": {
            "user_id": "ユーザー ID"
        },
        "returns": "現在のユーザーのすべての来店座位予約の詳細情報",
        "tool_type": "READ"
    },

    "search_instore_book": {
        "description": "ユーザーのシート予約情報を照会します。book_id が None の場合はユーザーのすべてのシート予約を返し、book_id が None でない場合は指定されたシート予約を返します。",
        "preconditions": "来店シーンであること。book_id が None の場合はユーザーのすべてのシート予約を返し、book_id が None でない場合は指定されたシート予約を返します。",
        "postconditions": "シート予約情報を返します。後の変更やキャンセルに便利です。",
        "args": {
            "user_id": "ユーザー ID",
            "book_id": "シート予約 ID。オプションパラメータで、デフォルトは None です。"
        },
        "returns": "シート予約情報。複数のシート予約は改行で区切られます。",
        "tool_type": "READ"
    },

    "search_instore_reservation": {
        "description": "ユーザーの予約消費情報を照会する",
        "preconditions": "来店シーンにおいて、reservation_id が None の場合はユーザーの全ての予約消費情報を返却し、reservation_id が None でない場合は指定された予約消費情報を返却する",
        "postconditions": "予約消費情報を返却し、後続の修正またはキャンセルに利用できるようにする",
        "args": {
            "user_id": "ユーザー ID",
            "reservation_id": "予約消費 ID。オプションパラメータで、デフォルトは None"
        },
        "returns": "予約消費情報。複数の予約は改行文字で区切られる",
        "tool_type": "READ"
    },
}

# Create Instore tool schema manager
_schema_manager = create_tool_schema_manager("instore", TOOL_DESCRIPTIONS_ZH, TOOL_DESCRIPTIONS_EN, japanese=TOOL_DESCRIPTIONS_JA, french=TOOL_DESCRIPTIONS_FR, russian=TOOL_DESCRIPTIONS_RU, arabic=TOOL_DESCRIPTIONS_AR, hindi=TOOL_DESCRIPTIONS_HI, thai=TOOL_DESCRIPTIONS_TH, spanish=TOOL_DESCRIPTIONS_ES, korean=TOOL_DESCRIPTIONS_KO, indonesian=TOOL_DESCRIPTIONS_ID, hebrew=TOOL_DESCRIPTIONS_HE, turkish=TOOL_DESCRIPTIONS_TR, vietnamese=TOOL_DESCRIPTIONS_VI, malay=TOOL_DESCRIPTIONS_MS, belarusian=TOOL_DESCRIPTIONS_BE, punjabi=TOOL_DESCRIPTIONS_PA, kazakh=TOOL_DESCRIPTIONS_KK, khmer=TOOL_DESCRIPTIONS_KM, burmese=TOOL_DESCRIPTIONS_MY, lao=TOOL_DESCRIPTIONS_LO, tamil=TOOL_DESCRIPTIONS_TA, telugu=TOOL_DESCRIPTIONS_TE)

# For backward compatibility, provide original function interface
def get_tool_descriptions():
    """Get tool descriptions based on language configuration."""
    return _schema_manager.get_tool_descriptions()

def get_tool_description(tool_name: str) -> Dict[str, Any]:
    """Get the description of a specific tool by name."""
    return _schema_manager.get_tool_description(tool_name)

def get_all_tool_names() -> list:
    """Get a list of all available tool names."""
    return _schema_manager.get_all_tool_names()

def get_tools_by_type(tool_type: str) -> Dict[str, Dict[str, Any]]:
    """Get all tools of a specific type."""
    return _schema_manager.get_tools_by_type(tool_type)

def get_tool_count_by_type() -> Dict[str, int]:
    """Get the count of tools by type."""
    return _schema_manager.get_tool_count_by_type()

def get_tool_args(tool_name: str) -> Dict[str, str]:
    """Get the arguments of a specific tool by name."""
    return _schema_manager.get_tool_args(tool_name)

def get_tool_returns(tool_name: str) -> str:
    """Get the return value description of a specific tool by name."""
    return _schema_manager.get_tool_returns(tool_name)

# Backward compatible variable
TOOL_DESCRIPTIONS = get_tool_descriptions()
TOOL_TYPE_MAPPING = _schema_manager.tool_type_mapping
