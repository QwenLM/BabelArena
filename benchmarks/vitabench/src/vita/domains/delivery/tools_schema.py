"""Tool schema definitions for the delivery domain.

This file contains the descriptions and mappings for all tools decorated with @is_tool
in the deliveryTools class.
"""

from typing import Dict, Any
from vita.utils.schema_utils import create_tool_schema_manager

# Tool descriptions extracted from tools.py - Chinese version
TOOL_DESCRIPTIONS_ZH = {
    "delivery_distance_to_time": {
        "description": "根据距离（米）计算外卖配送时间（分钟）",
        "preconditions": "根据从商家到用户地址的距离计算外卖配送时间",
        "postconditions": "返回配送时间（分钟）",
        "args": {
            "distance": "距离（以米为单位）"
        },
        "returns": "时间（以分钟为单位）",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "获取商家信息，包括商家id、评分、地址、经度、纬度、标签、商品列表",
        "preconditions": "处于外卖场景，需要获取商家的详细信息",
        "postconditions": "返回商家的详细信息",
        "args": {
            "store_id": "商家id"
        },
        "returns": "商家的详细信息",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "获取商品信息，包括商品名称、商品id、商店名称、商店id、商品评分、商品价格、商品标签",
        "preconditions": "处于外卖场景，需要获取商品的详细信息",
        "postconditions": "返回商品的详细信息",
        "args": {
            "food_id": "商品id"
        },
        "returns": "商品的详细信息",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "在外卖场景下，可以根据用户表达抽取出描述商家的关键词，搜索或推荐多个商家",
        "preconditions": "处于外卖场景，获取描述商家的关键词",
        "postconditions": "返回商家列表，引导用户选择确定商家",
        "args": {
            "keywords": "描述商家的关键词"
        },
        "returns": "结构化输出的商家信息",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "在外卖场景下，可以根据用户表达抽取出描述商品的关键词，搜索或推荐多个商品",
        "preconditions": "处于外卖场景，获取描述商品的关键词",
        "postconditions": "返回商品列表，引导用户选择商品并创建订单",
        "args": {
            "keywords": "描述商品的关键词"
        },
        "returns": "结构化输出的商品信息",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "外卖订单创建，仅支持单个商家下单，单个商家可以下单多个商品",
        "preconditions": "处于外卖场景，确定唯一一个店家id和一个或多个商品id，确定用户的饮食禁忌，并在订单中体现",
        "postconditions": "返回订单信息，询问用户是否支付订单",
        "args": {
            "user_id": "用户id",
            "store_id": "商店id",
            "food_ids": "商品id列表",
            "food_cnts": "商品id对应数量列表",
            "address": "外卖配送目标地址",
            "dispatch_time": "外卖订单开始配送的时间（即骑手从商家取餐出发的时间），格式为yyyy-mm-dd HH:MM:SS",
            "attributes": "商品id对应商品规格属性",
            "note": "订单备注（禁止将用户关于时间等需求直接放在备注中），如饮食禁忌信息说明"
        },
        "returns": "如果创建成功，返回订单信息（包含订单id、用户id、商店id、商品id列表、商品数量列表、地址、下单时间、更新时间、订单状态、商品列表、备注），否则返回相关提示信息",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "在外卖场景下，上文有订单信息，用户表达确认支付，或者重新支付",
        "preconditions": "处于外卖场景，用户表达确认支付，订单创建完成并进入支付环节｜用户表示重新支付",
        "postconditions": "返回支付结果信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "获取订单状态",
        "preconditions": "查询外卖订单状态",
        "postconditions": "返回订单状态信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "订单状态信息",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "用户取消订单，或者用户取消支付。禁止对处于已取消状态的订单再次取消。",
        "preconditions": "查询外卖订单状态，确保订单状态为非cancelled",
        "postconditions": "返回取消订单结果信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "取消订单结果信息",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "修改订单备注信息",
        "preconditions": "上文确定唯一一个外卖order_id，用户需要修改外卖订单备注",
        "postconditions": "输出修改后订单信息，如果订单还未支付则需要用户确认支付",
        "args": {
            "order_id": "订单id",
            "note": "新的订单备注信息"
        },
        "returns": "修改订单备注操作的结果",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "查询所有外卖订单，返回包含订单ID、订单类型、用户ID、商家ID、总价、下单时间、更新时间、订单状态等信息",
        "preconditions": "按照查询条件查看所有外卖订单",
        "postconditions": "返回所有符合条件外卖订单的详细信息",
        "args": {
            "user_id": "用户ID",
            "status": "订单状态，默认为未支付"
        },
        "returns": "返回所有符合条件的外卖订单详细信息，包括订单ID、订单类型、用户ID、商家ID、总价、下单时间、更新时间、订单状态等信息",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "根据订单ID查询外卖订单，返回包含订单ID、订单类型、商家ID、配送时间、配送耗时、送达时间、总价、下单时间、更新时间、订单状态和商品列表等详细信息",
        "preconditions": "上文确定唯一一个外卖order_id",
        "postconditions": "返回指定订单详细信息",
        "args": {
            "order_id": "订单id"
        },
        "returns": "指定订单的详细信息，包括订单ID、订单类型、商家ID、配送时间、配送耗时、送达时间、总价、下单时间、更新时间、订单状态和商品列表",
        "tool_type": "READ"
    }
}

# Tool descriptions extracted from tools.py - English version
TOOL_DESCRIPTIONS_EN = {
    "delivery_distance_to_time": {
        "description": "Calculate delivery time (minutes) based on distance (meters)",
        "preconditions": "Calculate delivery time based on distance from store to user address",
        "postconditions": "Return delivery time (minutes)",
        "args": {
            "distance": "Distance (in meters)"
        },
        "returns": "Time (in minutes)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Get store information including store id, rating, address, longitude, latitude, tags, and product list",
        "preconditions": "In delivery scenario, need to get detailed store information",
        "postconditions": "Return detailed store information",
        "args": {
            "store_id": "Store id"
        },
        "returns": "Detailed store information",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Get food information including food name, food id, store name, store id, food rating, food price, and food tags",
        "preconditions": "In delivery scenario, need to get detailed food information",
        "postconditions": "Return detailed food information",
        "args": {
            "food_id": "Food id"
        },
        "returns": "Detailed food information",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "In delivery scenario, can extract keywords describing stores from user expressions, search or recommend multiple stores",
        "preconditions": "In delivery scenario, get keywords describing stores",
        "postconditions": "Return store list, guide user to select and confirm store",
        "args": {
            "keywords": "Keywords describing stores"
        },
        "returns": "Structured store information output",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "In delivery scenario, can extract keywords describing food from user expressions, search or recommend multiple food items",
        "preconditions": "In delivery scenario, get keywords describing food",
        "postconditions": "Return food list, guide user to select food and create order",
        "args": {
            "keywords": "Keywords describing food"
        },
        "returns": "Structured food information output",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Create delivery order, only supports single store orders, single store can order multiple food items",
        "preconditions": "In delivery scenario, determine unique store id and one or more food ids, determine user dietary restrictions and reflect in order",
        "postconditions": "Return order information, ask user to confirm payment",
        "args": {
            "user_id": "User id",
            "store_id": "Store id",
            "food_ids": "Food id list",
            "food_cnts": "Food id corresponding quantity list",
            "address": "delivery target address",
            "dispatch_time": "delivery order dispatch start time (when rider picks up food from store), format: yyyy-mm-dd HH:MM:SS",
            "attributes": "Food id corresponding food specification attributes",
            "note": "Order notes (prohibited from putting user time requirements directly in notes), such as dietary restriction information"
        },
        "returns": "If creation successful, return order information (including order id, user id, store id, food id list, food quantity list, address, order time, update time, order status, food list, notes), otherwise return related prompt information",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "In delivery scenario, with order information above, user expresses confirmation of payment or re-payment",
        "preconditions": "In delivery scenario, user expresses confirmation of payment, order creation completed and enters payment phase | user indicates re-payment",
        "postconditions": "Return payment result information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Get order status",
        "preconditions": "Query delivery order status",
        "postconditions": "Return order status information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Order status information",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "User cancels order or user cancels payment. Prohibited from canceling orders that are already in cancelled status.",
        "preconditions": "Query delivery order status, ensure order status is not cancelled",
        "postconditions": "Return order cancellation result information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Order cancellation result information",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Modify order note information",
        "preconditions": "Above text determines unique delivery order_id, user needs to modify delivery order notes",
        "postconditions": "Output modified order information, if order not yet paid user needs to confirm payment",
        "args": {
            "order_id": "Order id",
            "note": "New order note information"
        },
        "returns": "Result of modifying order note operation",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Query all delivery orders, return information including order ID, order type, user ID, store ID, total price, order time, update time, order status, etc.",
        "preconditions": "View all delivery orders according to query conditions",
        "postconditions": "Return detailed information of all delivery orders meeting conditions",
        "args": {
            "user_id": "User ID",
            "status": "Order status, default is unpaid"
        },
        "returns": "Return detailed information of all delivery orders meeting conditions, including order ID, order type, user ID, store ID, total price, order time, update time, order status, etc.",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Query delivery order by order ID, return detailed information including order ID, order type, store ID, dispatch time, dispatch duration, delivery time, total price, order time, update time, order status and food list",
        "preconditions": "Above text determines unique delivery order_id",
        "postconditions": "Return specified order detailed information",
        "args": {
            "order_id": "Order id"
        },
        "returns": "Specified order detailed information, including order ID, order type, store ID, dispatch time, dispatch duration, delivery time, total price, order time, update time, order status and food list",
        "tool_type": "READ"
    }
}

# Tool descriptions - Telugu version
TOOL_DESCRIPTIONS_TE = {
    "delivery_distance_to_time": {
        "description": "దూరం (మీటర్లలో) ఆధారంగా ఫుడ్ డెలివరీ సమయాన్ని (నిమిషాల్లో) లెక్కించండి",
        "preconditions": "వ్యాపారి నుండి వినియోగదారు చిరునామాకు ఉన్న దూరం ఆధారంగా ఫుడ్ డెలివరీ సమయాన్ని లెక్కించండి",
        "postconditions": "డెలివరీ సమయాన్ని (నిమిషాల్లో) తిరిగి ఇవ్వండి",
        "args": {
            "distance": "దూరం (మీటర్లలో)"
        },
        "returns": "సమయం (నిమిషాల్లో)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "వ్యాపారి సమాచారాన్ని పొందండి, ఇందులో వ్యాపారి ఐడి, రేటింగ్, చిరునామా, రేఖాంశం, అక్షాంశం, ట్యాగ్‌లు మరియు ఉత్పత్తుల జాబితా ఉంటాయి.",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో ఉన్నప్పుడు, వ్యాపారి వివరణాత్మక సమాచారాన్ని పొందాల్సిన అవసరం ఉంది.",
        "postconditions": "వ్యాపారి వివరణాత్మక సమాచారాన్ని తిరిగి అందిస్తుంది.",
        "args": {
            "store_id": "వ్యాపారి ఐడి"
        },
        "returns": "వ్యాపారి వివరణాత్మక సమాచారం",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "ఉత్పత్తి సమాచారాన్ని పొందండి, ఇందులో ఉత్పత్తి పేరు, ఉత్పత్తి ఐడీ, దుకాణం పేరు, దుకాణం ఐడీ, ఉత్పత్తి రేటింగ్, ఉత్పత్తి ధర, ఉత్పత్తి ట్యాగ్‌లు ఉంటాయి.",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో ఉన్నప్పుడు, ఉత్పత్తి యొక్క వివరణాత్మక సమాచారాన్ని పొందాల్సిన అవసరం ఉంది.",
        "postconditions": "ఉత్పత్తి యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇస్తుంది.",
        "args": {
            "food_id": "ఉత్పత్తి ఐడీ"
        },
        "returns": "ఉత్పత్తి యొక్క వివరణాత్మక సమాచారం",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "ఫుడ్ డెలివరీ సందర్భంలో, వినియోగదారు వ్యక్తీకరణ ఆధారంగా వ్యాపారులను వర్ణించే కీవర్డ్‌లను సేకరించి, అనేక వ్యాపారులను శోధించవచ్చు లేదా సిఫార్సు చేయవచ్చు",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో ఉండటం, వ్యాపారులను వర్ణించే కీవర్డ్‌లను పొందడం",
        "postconditions": "వ్యాపారుల జాబితాను అందించడం, వినియోగదారును ఖచ్చితైన వ్యాపారిని ఎంచుకోవడానికి మార్గనిర్దేశం చేయడం",
        "args": {
            "keywords": "వ్యాపారిని వర్ణించే కీవర్డ్‌లు"
        },
        "returns": "వ్యాపారి సమాచారం యొక్క నిర్మాణాత్మక అవుట్‌పుట్",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "ఫుడ్ డెలివరీ సందర్భంలో, వినియోగదారు వ్యక్తీకరణ ఆధారంగా వస్తువులను వర్ణించే కీవర్డ్‌లను సంగ్రహించి, అనేక వస్తువులను శోధించవచ్చు లేదా సిఫారసు చేయవచ్చు.",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో ఉండి, వస్తువులను వర్ణించే కీవర్డ్‌లను పొందండి",
        "postconditions": "వస్తువుల జాబితాను అందించండి, వినియోగదారును వస్తువును ఎంచుకోవడానికి మరియు ఆర్డర్‌ను సృష్టించడానికి మార్గనిర్దేశం చేయండి",
        "args": {
            "keywords": "వస్తువులను వర్ణించే కీవర్డ్‌లు"
        },
        "returns": "నిర్మాణాత్మకంగా అందించబడిన వస్తువు సమాచారం",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "ఫుడ్ డెలివరీ ఆర్డర్ సృష్టి, ఒకే మర్చంట్ నుండి ఆర్డర్ చేయడానికి మాత్రమే మద్దతు ఇస్తుంది, ఒక మర్చంట్ నుండి బహుళ వస్తువులను ఆర్డర్ చేయవచ్చు",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో, ఒక ప్రత్యేకమైన స్టోర్ ఐడి మరియు ఒకటి లేదా అంతకంటే ఎక్కువ ఫుడ్ ఐడిలను నిర్ధారించండి, వినియోగదారు ఆహార నిషేధాలను నిర్ధారించండి మరియు ఆర్డర్‌లో ప్రతిబింబించండి",
        "postconditions": "ఆర్డర్ సమాచారాన్ని తిరిగి ఇవ్వండి, వినియోగదారు ఆర్డర్‌ను చెల్లించాలా అని అడగండి",
        "args": {
            "user_id": "వినియోగదారు ఐడి",
            "store_id": "స్టోర్ ఐడి",
            "food_ids": "వస్తువు ఐడిల జాబితా",
            "food_cnts": "వస్తువు ఐడిలకు అనుగుణంగా పరిమాణాల జాబితా",
            "address": "ఫుడ్ డెలివరీ లక్ష్య చిరునామా",
            "dispatch_time": "ఫుడ్ డెలివరీ ఆర్డర్ డెలివరీ ప్రారంభమయ్యే సమయం (అంటే డెలివరీ బాయ్ మర్చంట్ వద్ద నుండి ఆహారం తీసుకుని బయలుదేరే సమయం), ఫార్మాట్ yyyy-mm-dd HH:MM:SS",
            "attributes": "వస్తువు ఐడికి అనుగుణంగా వస్తువు స్పెసిఫికేషన్ లక్షణాలు",
            "note": "ఆర్డర్ నోట్స్ (సమయం వంటి వినియోగదారు అవసరాలను నేరుగా నోట్స్‌లో ఉంచవద్దు), ఉదాహరణకు ఆహార నిషేధ సమాచార వివరణ"
        },
        "returns": "సృష్టి విజయవంతమైతే, ఆర్డర్ సమాచారాన్ని తిరిగి ఇవ్వండి (ఆర్డర్ ఐడి, వినియోగదారు ఐడి, స్టోర్ ఐడి, వస్తువు ఐడిల జాబితా, వస్తువు పరిమాణాల జాబితా, చిరునామా, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి, వస్తువుల జాబితా, నోట్‌లు ఉంటాయి), లేకపోతే సంబంధిత సమాచార సందేశాన్ని తిరిగి ఇవ్వండి",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "ఫుడ్ డెలివరీ సందర్భంలో, పైన ఆర్డర్ సమాచారం ఉండి, వినియోగదారు చెల్లింపును నిర్ధారించడానికి లేదా మళ్లీ చెల్లించడానికి వ్యక్తపరిచినప్పుడు",
        "preconditions": "ఫుడ్ డెలివరీ సందర్భంలో ఉండి, వినియోగదారు చెల్లింపును నిర్ధారించడానికి వ్యక్తపరిచి, ఆర్డర్ సృష్టించబడి చెల్లింపు దశలోకి వెళ్ళి ఉండాలి｜వినియోగదారు మళ్లీ చెల్లింపు చేయడానికి సూచించాలి",
        "postconditions": "చెల్లింపు ఫలిత సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "order_id": "ఆర్డర్ ఐడి"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ఆర్డర్ స్థితిని పొందండి",
        "preconditions": "ఫుడ్ డెలివరీ ఆర్డర్ స్థితిని విచారించండి",
        "postconditions": "ఆర్డర్ స్థితి సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడి"
        },
        "returns": "ఆర్డర్ స్థితి సమాచారం",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "వినియోగదారు ఆర్డర్‌ను రద్దు చేయడం లేదా చెల్లింపును రద్దు చేయడం. ఇప్పటికే రద్దు చేయబడిన ఆర్డర్‌ను మళ్లీ రద్దు చేయకూడదు.",
        "preconditions": "ఫుడ్ డెలివరీ ఆర్డర్ స్థితిని తనిఖీ చేయండి, ఆర్డర్ స్థితి రద్దు చేయబడలేదని నిర్ధారించుకోండి",
        "postconditions": "ఆర్డర్ రద్దు ఫలిత సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడి"
        },
        "returns": "ఆర్డర్ రద్దు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "ఆర్డర్ వ్యాఖ్య సమాచారాన్ని సవరించండి",
        "preconditions": "సందర్భం ఒక ప్రత్యేకమైన ఫుడ్ డెలివరీ order_id ని నిర్ధారిస్తుంది, వినియోగదారుకు ఫుడ్ డెలివరీ ఆర్డర్ వ్యాఖ్యను మార్చాల్సిన అవసరం ఉంది",
        "postconditions": "సవరించిన తర్వాత ఆర్డర్ సమాచారం అందించబడుతుంది, ఒకవేళ ఆర్డర్ ఇంకా చెల్లించకపోతే వినియోగదారు చెల్లింపును నిర్ధారించాల్సి ఉంటుంది",
        "args": {
            "order_id": "ఆర్డర్ ఐడి",
            "note": "కొత్త ఆర్డర్ వ్యాఖ్య సమాచారం"
        },
        "returns": "ఆర్డర్ వ్యాఖ్యను సవరించే చర్య ఫలితం",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "అన్ని ఫుడ్ డెలివరీ ఆర్డర్లను క్వెరీ చేయండి, ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, మర్చంట్ ID, మొత్తం ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి వంటి సమాచారాన్ని తిరిగి ఇవ్వండి",
        "preconditions": "క్వెరీ షరతుల ప్రకారం అన్ని ఫుడ్ డెలివరీ ఆర్డర్లను చూడండి",
        "postconditions": "షరతులకు అనుగుణంగా ఉన్న అన్ని ఫుడ్ డెలివరీ ఆర్డర్ల వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "user_id": "వినియోగదారు ID",
            "status": "ఆర్డర్ స్థితి, డిఫాల్ట్‌గా చెల్లించబడలేదు"
        },
        "returns": "షరతులకు అనుగుణంగా ఉన్న అన్ని ఫుడ్ డెలివరీ ఆర్డర్ల వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి, ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, మర్చంట్ ID, మొత్తం ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి వంటి సమాచారంతో సహా",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ఆర్డర్ ID ఆధారంగా ఫుడ్ డెలివరీ ఆర్డర్‌ను విచారించండి, ఆర్డర్ ID, ఆర్డర్ రకం, మర్చెంట్ ID, డెలివరీ సమయం, డెలివరీ వ్యవధి, చేరుకున్న సమయం, మొత్తం ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు వస్తువుల జాబితా వంటి వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి",
        "preconditions": "పైన పేర్కొన్న సందర్భం ఒక ప్రత్యేకమైన ఫుడ్ డెలివరీ order_id ని నిర్ధారిస్తుంది",
        "postconditions": "నిర్దిష్ట ఆర్డర్ యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ id"
        },
        "returns": "నిర్దిష్ట ఆర్డర్ యొక్క వివరణాత్మక సమాచారం, ఆర్డర్ ID, ఆర్డర్ రకం, మర్చెంట్ ID, డెలివరీ సమయం, డెలివరీ వ్యవధి, చేరుకున్న సమయం, మొత్తం ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు వస్తువుల జాబితాతో సహా",
        "tool_type": "READ"
    },
}

# Tool descriptions - Tamil version
TOOL_DESCRIPTIONS_TA = {
    "delivery_distance_to_time": {
        "description": "தூரத்தின் அடிப்படையில் (மீட்டர்) உணவு டெலிவரி நேரத்தை (நிமிடங்கள்) கணக்கிடுகிறது",
        "preconditions": "வணிக நிலையத்திலிருந்து பயனர் முகவரிக்கு உள்ள தூரத்தின் அடிப்படையில் உணவு டெலிவரி நேரத்தை கணக்கிடுகிறது",
        "postconditions": "டெலிவரி நேரத்தை (நிமிடங்களில்) திருப்பி அளிக்கிறது",
        "args": {
            "distance": "தூரம் (மீட்டரில்)"
        },
        "returns": "நேரம் (நிமிடங்களில்)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "வணிகர் தகவலைப் பெறுக, இதில் வணிகர் ஐடி, மதிப்பீடு, முகவரி, தீர்க்கரேகை, அட்சரேகை, குறிச்சொற்கள் மற்றும் பொருள் பட்டியல் ஆகியவை அடங்கும்.",
        "preconditions": "உணவு டெலிவரி சூழலில் இருக்கும்போது, வணிகரின் விரிவான தகவலைப் பெற வேண்டும்.",
        "postconditions": "வணிகரின் விரிவான தகவலைத் திருப்பி அனுப்புகிறது.",
        "args": {
            "store_id": "வணிகர் ஐடி"
        },
        "returns": "வணிகரின் விரிவான தகவல்",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "பொருள் தகவலைப் பெறுக, இதில் பொருள் பெயர், பொருள் ஐடி, கடை பெயர், கடை ஐடி, பொருள் மதிப்பீடு, பொருள் விலை, பொருள் குறிச்சொற்கள் ஆகியவை அடங்கும்.",
        "preconditions": "உணவு டெலிவரி சூழலில், பொருளின் விரிவான தகவலைப் பெற வேண்டும்.",
        "postconditions": "பொருளின் விரிவான தகவலைத் திருப்பி அனுப்புக.",
        "args": {
            "food_id": "பொருள் ஐடி"
        },
        "returns": "பொருளின் விரிவான தகவல்",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "உணவு டெலிவரி சூழலில், பயனர் கூற்றின் அடிப்படையில் வணிகர்களை விவரிக்கும் முக்கிய சொற்களைப் பிரித்தெடுத்து, பல வணிகர்களைத் தேடலாம் அல்லது பரிந்துரைக்கலாம்",
        "preconditions": "உணவு டெலிவரி சூழலில் இருத்தல், வணிகர்களை விவரிக்கும் முக்கிய சொற்களைப் பெறுதல்",
        "postconditions": "வணிகர் பட்டியலைத் திருப்பி அனுப்புதல், பயனரை வணிகரைத் தேர்ந்தெடுத்து உறுதிப்படுத்த வழிநடுத்துதல்",
        "args": {
            "keywords": "வணிகர்களை விவரிக்கும் முக்கிய சொற்கள்"
        },
        "returns": "கட்டமைக்கப்பட்ட வணிகர் தகவல் வெளியீடு",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "உணவு டெலிவரி சூழலில், பயனரின் கூற்றிலிருந்து பொருட்களை விவரிக்கும் முக்கிய சொற்களைப் பிரித்தெடுத்து, பல பொருட்களைத் தேட அல்லது பரிந்துரைக்க முடியும்",
        "preconditions": "உணவு டெலிவரி சூழலில் இருத்தல், பொருட்களை விவரிக்கும் முக்கிய சொற்களைப் பெறுதல்",
        "postconditions": "பொருட்களின் பட்டியலைத் திருப்பி அனுப்புதல், பயனரை பொருளைத் தேர்ந்தெடுத்து ஆர்டரை உருவாக்க வழிநடுத்துதல்",
        "args": {
            "keywords": "பொருட்களை விவரிக்கும் முக்கிய சொற்கள்"
        },
        "returns": "கட்டமைக்கப்பட்ட வெளியீட்டு பொருள் தகவல்",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "உணவு வழங்கல் ஆர்டர் உருவாக்கம், ஒரே ஒரு விற்பனையாளரிடம் மட்டுமே ஆர்டர் செய்ய ஆதரவு, ஒரே விற்பனையாளரிடம் பல உணவுப் பொருட்களை ஆர்டர் செய்யலாம்",
        "preconditions": "உணவு வழங்கல் சூழலில், ஒரு தனித்துவமான கடை ஐடி மற்றும் ஒன்று அல்லது அதற்கு மேற்பட்ட உணவு ஐடிக்களை உறுதி செய்யவும், பயனரின் உணவு கட்டுப்பாடுகளை உறுதி செய்து, ஆர்டரில் பிரதிபலிக்கவும்",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அனுப்பவும், பயனரிடம் ஆர்டரைச் செலுத்த வேண்டுமா எனக் கேட்கவும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "store_id": "கடை ஐடி",
            "food_ids": "உணவு ஐடி பட்டியல்",
            "food_cnts": "உணவு ஐடிக்குரிய அளவு பட்டியல்",
            "address": "உணவு வழங்கல் இலக்கு முகவரி",
            "dispatch_time": "உணவு வழங்கல் ஆர்டர் விநியோகம் தொடங்கும் நேரம் (அதாவது டெலிவரி பையன் கடையிலிருந்து உணவை எடுத்துச் செல்லும் நேரம்), வடிவம் yyyy-mm-dd HH:MM:SS",
            "attributes": "உணவு ஐடிக்குரிய உணவு விவரக்குறிப்பு பண்புகள்",
            "note": "ஆர்டர் குறிப்பு (நேரம் போன்ற பயனர் தேவைகளை நேரடியாக குறிப்பில் சேர்க்கத் தடை), உணவு கட்டுப்பாடு தகவல் விளக்கம் போன்றவை"
        },
        "returns": "உருவாக்கம் வெற்றிகரமாக இருந்தால், ஆர்டர் தகவலைத் திருப்பி அனுப்பவும் (ஆர்டர் ஐடி, பயனர் ஐடி, கடை ஐடி, உணவு ஐடி பட்டியல், உணவு அளவு பட்டியல், முகவரி, ஆர்டர் நேரம், புதுப்பிப்பு நேரம், ஆர்டர் நிலை, உணவு பட்டியல், குறிப்பு ஆகியவற்றை உள்ளடக்கியது), இல்லையெனில் தொடர்புடைய தகவல் செய்தியைத் திருப்பி அனுப்பவும்",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "உணவு டெலிவரி சூழலில், முந்தைய உரையாடலில் ஆர்டர் தகவல் உள்ளது, பயனர் கட்டணத்தை உறுதிப்படுத்த அல்லது மீண்டும் செலுத்த தெரிவிக்கிறார்",
        "preconditions": "உணவு டெலிவரி சூழலில் இருத்தல், பயனர் கட்டணத்தை உறுதிப்படுத்த தெரிவித்தல், ஆர்டர் உருவாக்கப்பட்டு கட்டண நிலைக்கு செல்லுதல்｜பயனர் மீண்டும் கட்டணம் செலுத்த தெரிவித்தல்",
        "postconditions": "கட்டண முடிவு தகவலைத் திருப்பி அனுப்பு",
        "args": {
            "order_id": "ஆர்டர் அடையாளம்"
        },
        "returns": "கட்டண முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ஆர்டர் நிலையைப் பெறுக",
        "preconditions": "உணவு விநியோக ஆர்டர் நிலையை விசாரிக்க",
        "postconditions": "ஆர்டர் நிலை தகவலைத் திருப்பி அனுப்பு",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் நிலை தகவல்",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "பயனர் ஆர்டரை ரத்து செய்வது அல்லது கொடுப்பனவை ரத்து செய்வது. ஏற்கனவே ரத்து செய்யப்பட்ட நிலையில் உள்ள ஆர்டரை மீண்டும் ரத்து செய்யக் கூடாது.",
        "preconditions": "உணவு டெலிவரி ஆர்டர் நிலையை விசாரிக்கவும், ஆர்டர் நிலை ரத்து செய்யப்பட்டது அல்ல என்பதை உறுதி செய்யவும்.",
        "postconditions": "ஆர்டர் ரத்து செய்வதற்கான முடிவு தகவலை வழங்கவும்.",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் ரத்து செய்வதற்கான முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "ஆர்டர் குறிப்பு தகவலை மாற்றவும்",
        "preconditions": "முந்தைய உரையாடலில் ஒரு தனித்துவமான உணவு டெலிவரி order_id உறுதி செய்யப்பட்டுள்ளது, பயனர் உணவு டெலிவரி ஆர்டர் குறிப்பை மாற்ற விரும்புகிறார்.",
        "postconditions": "மாற்றப்பட்ட ஆர்டர் தகவலை வெளியிடவும், ஆர்டர் இன்னும் செலுத்தப்படவில்லை என்றால் பயனர் கட்டணத்தை உறுதி செய்ய வேண்டும்.",
        "args": {
            "order_id": "ஆர்டர் id",
            "note": "புதிய ஆர்டர் குறிப்பு தகவல்"
        },
        "returns": "ஆர்டர் குறிப்பை மாற்றும் செயல்பாட்டின் முடிவு",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "அனைத்து உணவு டெலிவரி ஆர்டர்களையும் விசாரிக்கவும், ஆர்டர் ID, ஆர்டர் வகை, பயனர் ID, விற்பனையாளர் ID, மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை போன்ற தகவல்களைத் திருப்பி அளிக்கவும்",
        "preconditions": "வினவல் நிபந்தனைகளின்படி அனைத்து உணவு டெலிவரி ஆர்டர்களையும் பார்க்கவும்",
        "postconditions": "நிபந்தனைகளுக்கு ஏற்ப அனைத்து உணவு டெலிவரி ஆர்டர்களின் விரிவான தகவல்களைத் திருப்பி அளிக்கவும்",
        "args": {
            "user_id": "பயனர் ID",
            "status": "ஆர்டர் நிலை, இயல்பாக செலுத்தப்படாதது"
        },
        "returns": "நிபந்தனைகளுக்கு ஏற்ப அனைத்து உணவு டெலிவரி ஆர்டர்களின் விரிவான தகவல்களைத் திருப்பி அளிக்கவும், ஆர்டர் ID, ஆர்டர் வகை, பயனர் ID, விற்பனையாளர் ID, மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை போன்ற தகவல்கள் உட்பட",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ஆர்டர் ஐடியின் அடிப்படையில் உணவு விநியோக ஆர்டரை விசாரிக்கவும், ஆர்டர் ஐடி, ஆர்டர் வகை, விற்பனையாளர் ஐடி, விநியோக நேரம், விநியோக காலம், சேரும் நேரம், மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் பொருள் பட்டியல் போன்ற விரிவான தகவல்களைத் திருப்பி அளிக்கவும்.",
        "preconditions": "மேலே உள்ள உரை தனித்துவமான உணவு விநியோக order_id ஐ உறுதிப்படுத்த வேண்டும்.",
        "postconditions": "குறிப்பிட்ட ஆர்டரின் விரிவான தகவல்களைத் திருப்பி அளிக்கவும்.",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "குறிப்பிட்ட ஆர்டரின் விரிவான தகவல்கள், ஆர்டர் ஐடி, ஆர்டர் வகை, விற்பனையாளர் ஐடி, விநியோக நேரம், விநியோக காலம், சேரும் நேரம், மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் பொருள் பட்டியல் ஆகியவை அடங்கும்.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Lao version
TOOL_DESCRIPTIONS_LO = {
    "delivery_distance_to_time": {
        "description": "ຄິດໄລ່ເວລາຈັດສົ່ງອາຫານ (ນາທີ) ອີງຕາມໄລຍະທາງ (ແມັດ)",
        "preconditions": "ຄິດໄລ່ເວລາຈັດສົ່ງອາຫານ ອີງຕາມໄລຍະທາງຈາກຮ້ານຄ້າໄປຫາທີ່ຢູ່ຂອງຜູ້ໃຊ້",
        "postconditions": "ສົ່ງຄືນເວລາຈັດສົ່ງ (ນາທີ)",
        "args": {
            "distance": "ໄລຍະທາງ (ຫົວໜ່ວຍເປັນແມັດ)"
        },
        "returns": "ເວລາ (ຫົວໜ່ວຍເປັນນາທີ)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "ດຶງຂໍ້ມູນຂອງຮ້ານຄ້າ, ປະກອບມີ ລະຫັດຮ້ານຄ້າ, ຄະແນນປະເມີນ, ທີ່ຢູ່, ພິກັດລອງຈິດ, ພິກັດລະຕິຈູດ, ແທັກ, ລາຍການສິນຄ້າ",
        "preconditions": "ຢູ່ໃນສະຖານະການສັ່ງອາຫານ, ຕ້ອງການດຶງຂໍ້ມູນລະອຽດຂອງຮ້ານຄ້າ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຮ້ານຄ້າ",
        "args": {
            "store_id": "ລະຫັດຮ້ານຄ້າ"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງຮ້ານຄ້າ",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "ດຶງຂໍ້ມູນສິນຄ້າ, ລວມທັງຊື່ສິນຄ້າ, ລະຫັດສິນຄ້າ, ຊື່ຮ້ານ, ລະຫັດຮ້ານ, ຄະແນນປະເມີນສິນຄ້າ, ລາຄາສິນຄ້າ, ປ້າຍກຳກັບສິນຄ້າ",
        "preconditions": "ຢູ່ໃນບໍລິບົດການສັ່ງອາຫານ, ຕ້ອງການຂໍ້ມູນລະອຽດຂອງສິນຄ້າ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງສິນຄ້າ",
        "args": {
            "food_id": "ລະຫັດສິນຄ້າ"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງສິນຄ້າ",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "ໃນບໍລິບົດການສັ່ງອາຫານ, ສາມາດດຶງເອົາຄຳສຳຄັນທີ່ອະທິບາຍຮ້ານຄ້າຈາກຄຳເວົ້າຂອງຜູ້ໃຊ້ ເພື່ອຄົ້ນຫາ ຫຼື ແນະນຳຮ້ານຄ້າຫຼາຍແຫ່ງ",
        "preconditions": "ຢູ່ໃນບໍລິບົດການສັ່ງອາຫານ, ດຶງເອົາຄຳສຳຄັນທີ່ອະທິບາຍຮ້ານຄ້າ",
        "postconditions": "ສົ່ງຄືນລາຍຊື່ຮ້ານຄ້າ, ຊີ້ນຳຜູ້ໃຊ້ໃຫ້ເລືອກ ແລະ ຢືນຢັນຮ້ານຄ້າ",
        "args": {
            "keywords": "ຄຳສຳຄັນທີ່ອະທິບາຍຮ້ານຄ້າ"
        },
        "returns": "ຂໍ້ມູນຮ້ານຄ້າທີ່ສະແດງຜົນອອກມາແບບໂຄງສ້າງ",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "ໃນສະຖານະການສົ່ງອາຫານ, ສາມາດດຶງເອົາຄຳສຳຄັນທີ່ອະທິບາຍສິນຄ້າອອກຈາກຄຳເວົ້າຂອງຜູ້ໃຊ້, ເພື່ອຄົ້ນຫາ ຫຼື ແນະນຳສິນຄ້າຫຼາຍຢ່າງ",
        "preconditions": "ຢູ່ໃນສະຖານະການສົ່ງອາຫານ, ດຶງເອົາຄຳສຳຄັນທີ່ອະທິບາຍສິນຄ້າ",
        "postconditions": "ສົ່ງຄືນລາຍການສິນຄ້າ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກສິນຄ້າ ແລະ ສ້າງຄຳສັ່ງຊື້",
        "args": {
            "keywords": "ຄຳສຳຄັນທີ່ອະທິບາຍສິນຄ້າ"
        },
        "returns": "ຂໍ້ມູນສິນຄ້າທີ່ຖືກສົ່ງອອກແບບມີໂຄງສ້າງ",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "ການສ້າງຄໍາສັ່ງຊື້ອາຫານສົ່ງ, ສະໜັບສະໜູນແຕ່ການສັ່ງຊື້ຈາກຮ້ານດຽວ, ຮ້ານດຽວສາມາດສັ່ງຊື້ຫຼາຍລາຍການສິນຄ້າໄດ້",
        "preconditions": "ຢູ່ໃນສະຖານະການສັ່ງອາຫານສົ່ງ, ກໍານົດໄອດີຮ້ານຄ້າໃຫ້ໄດ້ແຫ່ງດຽວ ແລະ ໄອດີສິນຄ້າໜຶ່ງຫຼືຫຼາຍຢ່າງ, ກໍານົດຂໍ້ຫ້າມທາງອາຫານຂອງຜູ້ໃຊ້, ແລະ ສະແດງໃນຄໍາສັ່ງຊື້",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຄໍາສັ່ງຊື້, ຖາມຜູ້ໃຊ້ວ່າຕ້ອງການຊໍາລະເງິນຄໍາສັ່ງຊື້ຫຼືບໍ່",
        "args": {
            "user_id": "ໄອດີຜູ້ໃຊ້",
            "store_id": "ໄອດີຮ້ານຄ້າ",
            "food_ids": "ລາຍການໄອດີສິນຄ້າ",
            "food_cnts": "ລາຍການຈໍານວນທີ່ກົງກັບໄອດີສິນຄ້າ",
            "address": "ທີ່ຢູ່ປາຍທາງສໍາລັບການສົ່ງອາຫານ",
            "dispatch_time": "ເວລາເລີ່ມຕົ້ນການສົ່ງຄໍາສັ່ງອາຫານ (ໝາຍຄວາມວ່າເວລາທີ່ຜູ້ຂັບຂີ່ຮັບອາຫານຈາກຮ້ານອອກໄປ), ຮູບແບບແມ່ນ yyyy-mm-dd HH:MM:SS",
            "attributes": "ຄຸນລັກສະນະສະເພາະຂອງສິນຄ້າທີ່ກົງກັບໄອດີສິນຄ້າ",
            "note": "ໝາຍເຫດຄໍາສັ່ງຊື້ (ຫ້າມວາງຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ກ່ຽວກັບເວລາ ແລະ ອື່ນໆໄວ້ໃນໝາຍເຫດໂດຍກົງ), ເຊັ່ນ: ຄໍາອະທິບາຍຂໍ້ມູນຂໍ້ຫ້າມທາງອາຫານ"
        },
        "returns": "ຖ້າສ້າງສໍາເລັດ, ສົ່ງຄືນຂໍ້ມູນຄໍາສັ່ງຊື້ (ລວມມີ ໄອດີຄໍາສັ່ງຊື້, ໄອດີຜູ້ໃຊ້, ໄອດີຮ້ານຄ້າ, ລາຍການໄອດີສິນຄ້າ, ລາຍການຈໍານວນສິນຄ້າ, ທີ່ຢູ່, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄໍາສັ່ງຊື້, ລາຍການສິນຄ້າ, ໝາຍເຫດ), ຖ້າບໍ່ດັ່ງນັ້ນຈະສົ່ງຄືນຂໍ້ຄວາມແຈ້ງເຕືອນທີ່ກ່ຽວຂ້ອງ",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "ໃນບໍລິບົດການສັ່ງອາຫານ, ມີຂໍ້ມູນໃບສັ່ງຊື້ໃນບໍລິບົດກ່ອນໜ້າ, ຜູ້ໃຊ້ສະແດງການຢືນຢັນການຊຳລະເງິນ ຫຼື ການຊຳລະເງິນໃໝ່",
        "preconditions": "ຢູ່ໃນບໍລິບົດການສັ່ງອາຫານ, ຜູ້ໃຊ້ສະແດງການຢືນຢັນການຊຳລະເງິນ, ໃບສັ່ງຊື້ຖືກສ້າງສຳເລັດແລະເຂົ້າສູ່ຂັ້ນຕອນການຊຳລະເງິນ｜ຜູ້ໃຊ້ສະແດງການຊຳລະເງິນໃໝ່",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "args": {
            "order_id": "ລະຫັດໃບສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ກວດສອບສະຖານະຄຳສັ່ງຊື້",
        "preconditions": "ກວດສອບສະຖານະຄຳສັ່ງຊື້ອາຫານສົ່ງ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນສະຖານະຄຳສັ່ງຊື້",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນສະຖານະຄຳສັ່ງຊື້",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄຳສັ່ງ, ຫຼື ຜູ້ໃຊ້ຍົກເລີກການຊຳລະເງິນ. ຫ້າມຍົກເລີກຄຳສັ່ງທີ່ຢູ່ໃນສະຖານະຍົກເລີກແລ້ວອີກຄັ້ງ.",
        "preconditions": "ກວດສອບສະຖານະຄຳສັ່ງສົ່ງອາຫານ, ຮັບປະກັນວ່າສະຖານະຄຳສັ່ງບໍ່ແມ່ນຖືກຍົກເລີກ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຜົນການຍົກເລີກຄຳສັ່ງ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງ"
        },
        "returns": "ຂໍ້ມູນຜົນການຍົກເລີກຄຳສັ່ງ",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "ແກ້ໄຂຂໍ້ມູນໝາຍເຫດຄຳສັ່ງຊື້",
        "preconditions": "ບໍລິບົດກ່ອນໜ້າກຳນົດ order_id ການສັ່ງອາຫານພາຍນອກທີ່ແນ່ນອນພຽງອັນດຽວ, ຜູ້ໃຊ້ຕ້ອງການແກ້ໄຂໝາຍເຫດຄຳສັ່ງຊື້ອາຫານພາຍນອກ",
        "postconditions": "ສະແດງຂໍ້ມູນຄຳສັ່ງຊື້ຫຼັງຈາກແກ້ໄຂ, ຖ້າຄຳສັ່ງຊື້ຍັງບໍ່ທັນໄດ້ຊຳລະເງິນ ກໍ່ຕ້ອງໃຫ້ຜູ້ໃຊ້ຢືນຢັນການຊຳລະເງິນ",
        "args": {
            "order_id": "ໝາຍເລກຄຳສັ່ງຊື້",
            "note": "ຂໍ້ມູນໝາຍເຫດຄຳສັ່ງຊື້ໃໝ່"
        },
        "returns": "ຜົນລັພຂອງການດຳເນີນງານແກ້ໄຂໝາຍເຫດຄຳສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "ສືບຄົ້ນຄໍາສັ່ງຊື້ອາຫານທັງໝົດ, ສົ່ງຄືນຂໍ້ມູນທີ່ປະກອບມີ ລະຫັດຄໍາສັ່ງ, ປະເພດຄໍາສັ່ງ, ລະຫັດຜູ້ໃຊ້, ລະຫັດຮ້ານຄ້າ, ລາຄາລວມ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄໍາສັ່ງ ແລະ ຂໍ້ມູນອື່ນໆ",
        "preconditions": "ສະແດງຄໍາສັ່ງຊື້ອາຫານທັງໝົດຕາມເງື່ອນໄຂການສືບຄົ້ນ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຄໍາສັ່ງຊື້ອາຫານທັງໝົດທີ່ສອດຄ່ອງກັບເງື່ອນໄຂ",
        "args": {
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "status": "ສະຖານະຄໍາສັ່ງ, ຄ່າເລີ່ມຕົ້ນແມ່ນຍັງບໍ່ທັນຊໍາລະເງິນ"
        },
        "returns": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຄໍາສັ່ງຊື້ອາຫານທັງໝົດທີ່ສອດຄ່ອງກັບເງື່ອນໄຂ, ປະກອບມີ ລະຫັດຄໍາສັ່ງ, ປະເພດຄໍາສັ່ງ, ລະຫັດຜູ້ໃຊ້, ລະຫັດຮ້ານຄ້າ, ລາຄາລວມ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄໍາສັ່ງ ແລະ ຂໍ້ມູນອື່ນໆ",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ສືບຄົ້ນຄໍາສັ່ງຊື້ອາຫານສົ່ງຕາມ ID ຄໍາສັ່ງຊື້, ສົ່ງຄືນຂໍ້ມູນລະອຽດທີ່ປະກອບມີ ID ຄໍາສັ່ງຊື້, ປະເພດຄໍາສັ່ງຊື້, ID ຮ້ານຄ້າ, ເວລາຈັດສົ່ງ, ໄລຍະເວລາຈັດສົ່ງ, ເວລາມາຮອດ, ລາຄາລວມ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄໍາສັ່ງຊື້ ແລະ ລາຍການສິນຄ້າ",
        "preconditions": "ບໍລິບົດຂ້າງເທິງກໍານົດ order_id ຂອງຄໍາສັ່ງຊື້ອາຫານສົ່ງທີ່ມີພຽງອັນດຽວ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຄໍາສັ່ງຊື້ທີ່ກໍານົດ",
        "args": {
            "order_id": "ID ຄໍາສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນລະອຽດຂອງຄໍາສັ່ງຊື້ທີ່ກໍານົດ, ປະກອບມີ ID ຄໍາສັ່ງຊື້, ປະເພດຄໍາສັ່ງຊື້, ID ຮ້ານຄ້າ, ເວລາຈັດສົ່ງ, ໄລຍະເວລາຈັດສົ່ງ, ເວລາມາຮອດ, ລາຄາລວມ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄໍາສັ່ງຊື້ ແລະ ລາຍການສິນຄ້າ",
        "tool_type": "READ"
    },
}

# Tool descriptions - Burmese version
TOOL_DESCRIPTIONS_MY = {
    "delivery_distance_to_time": {
        "description": "အကွာအဝေး (မီတာ) အပေါ် အခြေခံ၍ အစားအစာ ပို့ဆောင်ချိန် (မိနစ်) ကို တွက်ချက်သည်",
        "preconditions": "ဆိုင်မှ အသုံးပြုသူ လိပ်စာသို့ အကွာအဝေးအပေါ် အခြေခံ၍ အစားအစာ ပို့ဆောင်ချိန်ကို တွက်ချက်သည်",
        "postconditions": "ပို့ဆောင်ချိန် (မိနစ်) ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "distance": "အကွာအဝေး (မီတာဖြင့်)"
        },
        "returns": "အချိန် (မိနစ်ဖြင့်)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "ဆိုင်အချက်အလက်များကို ရယူပါ။ ဆိုင်အိုင်ဒီ၊ အဆင့်သတ်မှတ်ချက်၊ လိပ်စာ၊ လောင်ဂျီတွဒ်၊ လတ္တီတွဒ်၊ အမှတ်အသားများနှင့် ကုန်ပစ္စည်းစာရင်းတို့ ပါဝင်သည်။",
        "preconditions": "အစားအသောက် မှာယူနေသည့် အခြေအနေတွင် ဆိုင်၏ အသေးစိတ် အချက်အလက်များကို ရယူရန် လိုအပ်သည့်အခါ",
        "postconditions": "ဆိုင်၏ အသေးစိတ် အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "store_id": "ဆိုင်အိုင်ဒီ"
        },
        "returns": "ဆိုင်၏ အသေးစိတ် အချက်အလက်များ",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "အစားအစာအချက်အလက်ကို ရယူခြင်း၊ အစားအစာအမည်၊ အစားအစာအိုင်ဒီ၊ ဆိုင်အမည်၊ ဆိုင်အိုင်ဒီ၊ အစားအစာအဆင့်သတ်မှတ်ချက်၊ အစားအစာဈေးနှုန်း၊ အစားအစာအမှတ်အသားများ အပါအဝင်ဖြစ်သည်။",
        "preconditions": "အစားအစာပို့ဆောင်ရေး အခြေအနေတွင် ရှိနေပြီး အစားအစာ၏ အသေးစိတ်အချက်အလက်ကို ရယူရန် လိုအပ်သည်။",
        "postconditions": "အစားအစာ၏ အသေးစိတ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "food_id": "အစားအစာအိုင်ဒီ"
        },
        "returns": "အစားအစာ၏ အသေးစိတ်အချက်အလက်",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "အစားအသောက် မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင် အသုံးပြုသူ၏ ပြောကြားချက်မှ ဆိုင်များကို ဖော်ပြသော သော့ချက် စကားလုံးများကို ထုတ်ယူကာ ဆိုင်များကို ရှာဖွေခြင်း သို့မဟုတ် အကြံပြုခြင်း ပြုနိုင်သည်။",
        "preconditions": "အစားအသောက် မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင် ရှိနေပြီး ဆိုင်များကို ဖော်ပြသော သော့ချက် စကားလုံးများကို ရယူခြင်း။",
        "postconditions": "ဆိုင်များ စာရင်းကို ပြန်လည်ပေးပို့ပြီး အသုံးပြုသူအား ဆိုင်ကို ရွေးချယ် သတ်မှတ်ရန် လမ်းညွှန်ခြင်း။",
        "args": {
            "keywords": "ဆိုင်များကို ဖော်ပြသော သော့ချက် စကားလုံးများ"
        },
        "returns": "ဆိုင်များဆိုင်ရာ အချက်အလက်များကို စနစ်တကျ ထုတ်ပေးခြင်း",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "အစားအစာ မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင်၊ အသုံးပြုသူ၏ ပြောကြားချက်မှ ကုန်ပစ္စည်းကို ဖော်ပြသော သော့ချက် စာလုံးများကို ထုတ်ယူပြီး ကုန်ပစ္စည်းအများအပြားကို ရှာဖွေခြင်း သို့မဟုတ် အကြံပြုခြင်း ပြုလုပ်နိုင်သည်။",
        "preconditions": "အစားအစာ မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင် ရှိနေပြီး ကုန်ပစ္စည်းကို ဖော်ပြသော သော့ချက် စာလုံးများကို ရယူခြင်း။",
        "postconditions": "ကုန်ပစ္စည်း စာရင်းကို ပြန်လည်ပေးပို့ပြီး၊ အသုံးပြုသူအား ကုန်ပစ္စည်းကို ရွေးချယ်ကာ အော်ဒါဖွင့်လှစ်ရန် လမ်းညွှန်ပေးသည်။",
        "args": {
            "keywords": "ကုန်ပစ္စည်းကို ဖော်ပြသော သော့ချက် စာလုံးများ"
        },
        "returns": "စနစ်တကျ ဖွဲ့စည်းထားသော ကုန်ပစ္စည်း အချက်အလက်များ",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "အပြင်စာ အော်ဒါဖန်တီးခြင်း၊ ဆိုင်တစ်ဆိုင်တည်းမှသာ အော်ဒါတင်နိုင်ပြီး ဆိုင်တစ်ဆိုင်တည်းမှ ကုန်ပစ္စည်းအမျိုးမျိုးကို အော်ဒါတင်နိုင်သည်။",
        "preconditions": "အပြင်စာ မှာယူမှု ပြင်ဆင်နေချိန်တွင် ဆိုင်အိုင်ဒီတစ်ခုတည်းနှင့် ကုန်ပစ္စည်းအိုင်ဒီတစ်ခု သို့မဟုတ် တစ်ခုထက်ပို၍ သေချာစွာ သတ်မှတ်ပါ၊ အသုံးပြုသူ၏ အစားအသောက် ကန့်သတ်ချက်များကို သေချာစွာ သတ်မှတ်ပြီး အော်ဒါတွင် ထည့်သွင်းဖော်ပြပါ။",
        "postconditions": "အော်ဒါအချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး အသုံးပြုသူအား အော်ဒါကို ငွေချေပါမလားဟု မေးမြန်းပါ။",
        "args": {
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "store_id": "ဆိုင် အိုင်ဒီ",
            "food_ids": "ကုန်ပစ္စည်း အိုင်ဒီ စာရင်း",
            "food_cnts": "ကုန်ပစ္စည်း အိုင်ဒီနှင့် ကိုက်ညီသော အရေအတွက် စာရင်း",
            "address": "အပြင်စာ ပို့ဆောင်မည့် ပစ်မှတ်လိပ်စာ",
            "dispatch_time": "အပြင်စာ အော်ဒါ စတင်ပို့ဆောင်မည့် အချိန် (ဆိုလိုသည်မှာ မော်တော်ဆိုင်ကယ်စီးသူ ဆိုင်မှ အစားအစာကိုယူပြီး ထွက်ခွာသည့်အချိန်)၊ ပုံစံမှာ yyyy-mm-dd HH:MM:SS",
            "attributes": "ကုန်ပစ္စည်း အိုင်ဒီနှင့် ကိုက်ညီသော ကုန်ပစ္စည်း သတ်မှတ်ချက် ဂုဏ်သတ္တိများ",
            "note": "အော်ဒါ မှတ်ချက် (အချိန်နှင့် ပတ်သက်သော အသုံးပြုသူ၏ လိုအပ်ချက်များကို မှတ်ချက်တွင် တိုက်ရိုက်မထည့်ရ)၊ ဥပမာ - အစားအသောက် ကန့်သတ်ချက် အချက်အလက် ရှင်းလင်းချက်"
        },
        "returns": "အကယ်၍ အောင်မြင်စွာ ဖန်တီးပါက အော်ဒါအချက်အလက်ကို ပြန်လည်ပေးပို့ပါ (အော်ဒါ အိုင်ဒီ၊ အသုံးပြုသူ အိုင်ဒီ၊ ဆိုင် အိုင်ဒီ၊ ကုန်ပစ္စည်း အိုင်ဒီ စာရင်း၊ ကုန်ပစ္စည်း အရေအတွက် စာရင်း၊ လိပ်စာ၊ အော်ဒါတင်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါ အခြေအနေ၊ ကုန်ပစ္စည်း စာရင်း၊ မှတ်ချက် တို့ ပါဝင်သည်)၊ အကယ်၍ မဟုတ်ပါက သက်ဆိုင်ရာ အချက်အလက် မက်ဆေ့ခ်ျကို ပြန်လည်ပေးပို့ပါ။",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "အစားအသောက် မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင်၊ အထက်တွင် အော်ဒါ အချက်အလက်များ ရှိနေပြီး၊ အသုံးပြုသူက ငွေချေခြင်းကို အတည်ပြုကြောင်း ပြသခြင်း သို့မဟုတ် ပြန်လည် ငွေချေခြင်း ဖြစ်သည်။",
        "preconditions": "အစားအသောက် မှာယူခြင်း ဆိုင်ရာ အခြေအနေတွင် ရှိနေခြင်း၊ အသုံးပြုသူက ငွေချေခြင်းကို အတည်ပြုကြောင်း ပြသခြင်း၊ အော်ဒါ ဖန်တီးမှု ပြီးဆုံးပြီး ငွေချေခြင်း အဆင့်သို့ ရောက်ရှိခြင်း｜အသုံးပြုသူက ပြန်လည် ငွေချေခြင်းကို ပြောဆိုခြင်း။",
        "postconditions": "ငွေချေခြင်း ရလဒ် အချက်အလက်ကို ပြန်လည် ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "ငွေချေခြင်း ရလဒ် အချက်အလက်",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "အော်ဒါအခြေအနေကို ရယူပါ",
        "preconditions": "အပြင်စာ အော်ဒါအခြေအနေကို စစ်ဆေးသည်",
        "postconditions": "အော်ဒါအခြေအနေ အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "အော်ဒါအခြေအနေ အချက်အလက်",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "အသုံးပြုသူက အော်ဒါကို ပယ်ဖျက်ခြင်း သို့မဟုတ် ငွေပေးချေမှုကို ပယ်ဖျက်ခြင်း။ ပယ်ဖျားပြီးသား အခြေအနေရှိနေသော အော်ဒါကို ထပ်မံပယ်ဖျက်ခွင့်မရှိပါ။",
        "preconditions": "အစားအစာပို့ အော်ဒါအခြေအနေကို စစ်ဆေးပြီး အော်ဒါအခြေအနေသည် ပယ်ဖျားပြီးသား မဟုတ်ကြောင်း သေချာစေရန်။",
        "postconditions": "အော်ဒါပယ်ဖျက်မှု ရလဒ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "အော်ဒါပယ်ဖျက်မှု ရလဒ်အချက်အလက်",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "အော်ဒါမှတ်ချက်အချက်အလက်ကို ပြင်ဆင်ရန်",
        "preconditions": "အထက်ပါအချက်အလက်များတွင် ထူးခြားသော အစားအသောက်ပို့ဆောင်ရေး order_id ကို သတ်မှတ်ထားပြီး၊ အသုံးပြုသူသည် အစားအသောက်ပို့ဆောင်ရေး အော်ဒါမှတ်ချက်ကို ပြင်ဆင်လိုသည်",
        "postconditions": "ပြင်ဆင်ပြီးသော အော်ဒါအချက်အလက်ကို ထုတ်ပေးသည်၊ အကယ်၍ အော်ဒါကို ငွေမချေသေးပါက အသုံးပြုသူအနေဖြင့် ငွေချေခြင်းကို အတည်ပြုရန် လိုအသည်",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ",
            "note": "အသစ်အော်ဒါမှတ်ချက်အချက်အလက်"
        },
        "returns": "အော်ဒါမှတ်ချက်ပြင်ဆင်ခြင်း လုပ်ဆောင်ချက်၏ ရလဒ်",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "အပြင်စာအော်ဒါအားလုံးကို စစ်ဆေးရန်၊ အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ ဆိုင်အိုင်ဒီ၊ စုစုပေါင်းဈေး၊ အော်ဒါတင်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေ စသည်တို့ပါဝင်သော အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "preconditions": "စစ်ဆေးမှုစံနှုန်းများအလိုက် အပြင်စာအော်ဒါအားလုံးကို ကြည့်ရှုပါ",
        "postconditions": "စံနှုန်းနှင့်ကိုက်ညီသော အပြင်စာအော်ဒါအားလုံး၏ အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "user_id": "အသုံးပြုသူအိုင်ဒီ",
            "status": "အော်ဒါအခြေအနေ၊ ပုံသေမှာ မပေးဆောင်ရသေးသောအခြေအနေဖြစ်သည်"
        },
        "returns": "စံနှုန်းနှင့်ကိုက်ညီသော အပြင်စာအော်ဒါအားလုံး၏ အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့သည်၊ အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ ဆိုင်အိုင်ဒီ၊ စုစုပေါင်းဈေး၊ အော်ဒါတင်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေ စသည်တို့ပါဝင်သည်",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "အော်ဒါ ID အပေါ်အခြေခံ၍ အစားအစာပို့ဆောင်ရေး အော်ဒါကို စစ်ဆေးရန်နှင့် အော်ဒါ ID၊ အော်ဒါအမျိုးအစား၊ ဆိုင် ID၊ ပို့ဆောင်ချိန်၊ ပို့ဆောင်ကြာချိန်၊ ရောက်ရှိချိန်၊ စုစုပေါင်းဈေး၊ အော်ဒါမှတ်သားချိန်၊ အပ်ဒိတ်လုပ်ချိန်၊ အော်ဒါအခြေအနေနှင့် ကုန်ပစ္စည်းစာရင်းအပါအဝင် အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "အထက်ပါစာသားတွင် ထူးခြားသော အစားအစာပို့ဆောင်ရေး order_id တစ်ခုကို သတ်မှတ်ထားသည်။",
        "postconditions": "သတ်မှတ်ထားသော အော်ဒါ၏ အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါ id"
        },
        "returns": "သတ်မှတ်ထားသော အော်ဒါ၏ အသေးစိတ်အချက်အလက်များ၊ အော်ဒါ ID၊ အော်ဒါအမျိုးအစား၊ ဆိုင် ID၊ ပို့ဆောင်ချိန်၊ ပို့ဆောင်ကြာချိန်၊ ရောက်ရှိချိန်၊ စုစုပေါင်းဈေး၊ အော်ဒါမှတ်သားချိန်၊ အပ်ဒိတ်လုပ်ချိန်၊ အော်ဒါအခြေအနေနှင့် ကုန်ပစ္စည်းစာရင်းတို့ ပါဝင်သည်။",
        "tool_type": "READ"
    },
}

# Tool descriptions - Khmer version
TOOL_DESCRIPTIONS_KM = {
    "delivery_distance_to_time": {
        "description": "គណនាពេលវេលាដឹកជញ្ជូនអាហារ (នាទី) ដោយផ្អែកលើចម្ងាយ (ម៉ែត្រ)",
        "preconditions": "គណនាពេលវេលាដឹកជញ្ជូនអាហារដោយផ្អែកលើចម្ងាយពីហាងទៅកាន់អាសយដ្ឋានរបស់អ្នកប្រើប្រាស់",
        "postconditions": "ត្រឡប់មកវិញនូវពេលវេលាដឹកជញ្ជូន (នាទី)",
        "args": {
            "distance": "ចម្ងាយ (គិតជាម៉ែត្រ)"
        },
        "returns": "ពេលវេលា (គិតជានាទី)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "ទទួលបានព័ត៌មានហាង រួមមាន id ហាង ពិន្ទុ អាសយដ្ឋាន រយៈបណ្តោយ រយៈទទឹង ផ្លាកសញ្ញា និងបញ្ជីផលិតផល",
        "preconditions": "ស្ថិតក្នុងបរិបទកុម្ម៉ង់ម្ហូប ត្រូវការទទួលបានព័ត៌មានលម្អិតរបស់ហាង",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតរបស់ហាង",
        "args": {
            "store_id": "id ហាង"
        },
        "returns": "ព័ត៌មានលម្អិតរបស់ហាង",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "ទទួលបានព័ត៌មានផលិតផល រួមមានឈ្មោះផលិតផល លេខសម្គាល់ផលិតផល ឈ្មោះហាង លេខសម្គាល់ហាង ពិន្ទុផលិតផល តម្លៃផលិតផល និងស្លាកផលិតផល",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពកុម្ម៉ង់អាហារ ត្រូវការទទួលបានព័ត៌មានលម្អិតអំពីផលិតផល",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតអំពីផលិតផល",
        "args": {
            "food_id": "លេខសម្គាល់ផលិតផល"
        },
        "returns": "ព័ត៌មានលម្អិតអំពីផលិតផល",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "នៅក្នុងបរិបទនៃការកុម្ម៉ង់ម្ហូបអាហារ អាចដកស្រង់ពាក្យគន្លឹះដែលពិពណ៌នាអំពីហាងដោយផ្អែកលើការសម្តែងរបស់អ្នកប្រើប្រាស់ ដើម្បីស្វែងរក ឬណែនាំហាងជាច្រើន",
        "preconditions": "ស្ថិតនៅក្នុងបរិបទនៃការកុម្ម៉ង់ម្ហូបអាហារ ទទួលបានពាក្យគន្លឹះដែលពិពណ៌នាអំពីហាង",
        "postconditions": "ត្រឡប់បញ្ជីហាង ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើស និងកំណត់ហាង",
        "args": {
            "keywords": "ពាក្យគន្លឹះដែលពិពណ៌នាអំពីហាង"
        },
        "returns": "ព័ត៌មានអំពីហាងដែលបានបង្ហាញជាលក្ខណៈរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "ក្នុងបរិបទនៃការកុម្ម៉ង់ម្ហូប អាចដកស្រង់ពាក្យគន្លឹះដែលពិពណ៌នាអំពីផលិតផលពីការសម្តែងរបស់អ្នកប្រើប្រាស់ ដើម្បីស្វែងរក ឬណែនាំផលិតផលជាច្រើន",
        "preconditions": "ស្ថិតក្នុងបរិបទនៃការកុម្ម៉ង់ម្ហូប ទទួលបានពាក្យគន្លឹះដែលពិពណ៌នាអំពីផលិតផល",
        "postconditions": "ត្រឡប់បញ្ជីផលិតផល ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសផលិតផល និងបង្កើតការកុម្ម៉ង់",
        "args": {
            "keywords": "ពាក្យគន្លឹះដែលពិពណ៌នាអំពីផលិតផល"
        },
        "returns": "ព័ត៌មានផលិតផលដែលបានបង្ហាញជាលក្ខណៈរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "ការបង្កើតការកុម្ម៉ង់ដឹកជញ្ជូនអាហារ គាំទ្រតែការកុម្ម៉ង់ពីហាងតែមួយប៉ុណ្ណោះ ហាងតែមួយអាចកុម្ម៉ង់មុខម្ហូបជាច្រើនបាន",
        "preconditions": "ស្ថិតនៅក្នុងស្ថានភាពដឹកជញ្ជូនអាហារ កំណត់លេខសម្គាល់ហាងតែមួយ និងលេខសម្គាល់មុខម្ហូបមួយ ឬច្រើន កំណត់ការហាមឃាត់ចំណីអាហាររបស់អ្នកប្រើប្រាស់ និងបង្ហាញនៅក្នុងការកុម្ម៉ង់",
        "postconditions": "ត្រឡប់ព័ត៌មានការកុម្ម៉ង់ សួរអ្នកប្រើប្រាស់ថាតើត្រូវទូទាត់ការកុម្ម៉ង់ដែរឬទេ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "store_id": "លេខសម្គាល់ហាង",
            "food_ids": "បញ្ជីលេខសម្គាល់មុខម្ហូប",
            "food_cnts": "បញ្ជីចំនួនត្រូវនឹងលេខសម្គាល់មុខម្ហូប",
            "address": "អាសយដ្ឋានគោលដៅសម្រាប់ដឹកជញ្ជូនអាហារ",
            "dispatch_time": "ពេលវេលាចាប់ផ្តើមដឹកជញ្ជូនការកុម្ម៉ង់អាហារ (គឺពេលវេលាដែលអ្នកដឹកជញ្ជូនយកអាហារពីហាងចេញដំណើរ) ទម្រង់គឺ yyyy-mm-dd HH:MM:SS",
            "attributes": "លក្ខណៈសម្បត្តិជាក់លាក់របស់មុខម្ហូបត្រូវនឹងលេខសម្គាល់មុខម្ហូប",
            "note": "ចំណាំការកុម្ម៉ង់ (ហាមដាក់តម្រូវការរបស់អ្នកប្រើប្រាស់អំពីពេលវេលាជាដើម ដោយផ្ទាល់ក្នុងចំណាំ) ដូចជាការបញ្ជាក់ព័ត៌មានការហាមឃាត់ចំណីអាហារ"
        },
        "returns": "ប្រសិនបើបង្កើតបានជោគជ័យ ត្រឡប់ព័ត៌មានការកុម្ម៉ង់ (រួមមានលេខសម្គាល់ការកុម្ម៉ង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់ហាង បញ្ជីលេខសម្គាល់មុខម្ហូប បញ្ជីចំនួនមុខម្ហូប អាសយដ្ឋាន ពេលវេលាកុម្ម៉ង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកុម្ម៉ង់ បញ្ជីមុខម្ហូប ចំណាំ) បើមិនដូច្នោះទេ ត្រឡប់សារព័ត៌មានពាក់ព័ន្ធ",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "ក្នុងស្ថានភាពកុម្ម៉ង់ម្ហូប ប្រសិនបើមានព័ត៌មានកុម្ម៉ង់ពីមុន អ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់ ឬស្នើសុំទូទាត់ឡើងវិញ",
        "preconditions": "ស្ថិតក្នុងស្ថានភាពកុម្ម៉ង់ម្ហូប អ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់ កុម្ម៉ង់ត្រូវបានបង្កើតរួច និងចូលដំណាក់កាលទូទាត់｜អ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់ឡើងវិញ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលការទូទាត់",
        "args": {
            "order_id": "លេខសម្គាល់កុម្ម៉ង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ទទួលបានស្ថានភាពការកម្មង់",
        "preconditions": "ស្វែងរកស្ថានភាពការកម្មង់ម្ហូបអាហារដឹកជញ្ជូន",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានស្ថានភាពការកម្មង់",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានស្ថានភាពការកម្មង់",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកុម្ម៉ង់ ឬលុបចោលការទូទាត់។ ហាមឃាត់ការលុបចោលការកុម្ម៉ង់ដែលស្ថិតក្នុងស្ថានភាពបានលុបចោលរួចហើយម្តងទៀត។",
        "preconditions": "ពិនិត្យមើលស្ថានភាពការកុម្ម៉ង់អាហារ ធានាថាស្ថានភាពការកុម្ម៉ង់មិនមែនជាបានលុបចោល។",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលទ្ធផលនៃការលុបចោលការកុម្ម៉ង់។",
        "args": {
            "order_id": "លេខសម្គាល់ការកុម្ម៉ង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលនៃការលុបចោលការកុម្ម៉ង់",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "កែសម្រួលព័ត៌មានសម្គាល់ក្បាល់",
        "preconditions": "បរិបទខាងលើកំណត់ order_id ក្បាល់យកចំណីតែមួយគត់ អ្នកប្រើប្រាស់ត្រូវការកែសម្រួលសម្គាល់ក្បាល់យកចំណី",
        "postconditions": "បង្ហាញព័ត៌មានក្បាល់បន្ទាប់ពីកែសម្រួល ប្រសិនបើក្បាល់មិនទាន់បានបង់ប្រាក់ទេ នោះអ្នកប្រើប្រាស់ត្រូវតែបញ្ជាក់ការទូទាត់",
        "args": {
            "order_id": "លេខសម្គាល់ក្បាល់",
            "note": "ព័ត៌មានសម្គាល់ក្បាល់ថ្មី"
        },
        "returns": "លទ្ធផលនៃប្រតិបត្តិការកែសម្រួលសម្គាល់ក្បាល់",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "ស្វែងរកការកម្មង់ដឹកជញ្ជូនអាហារទាំងអស់ ត្រឡប់មកវិញនូវព័ត៌មានរួមមានលេខសម្គាល់ការកម្មង់ ប្រភេទការកម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់ហាង តម្លៃសរុប ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកម្មង់ និងព័ត៌មានផ្សេងៗទៀត",
        "preconditions": "មើលការកម្មង់ដឹកជញ្ជូនអាហារទាំងអស់តាមលក្ខខណ្ឌស្វែងរក",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកម្មង់ដឹកជញ្ជូនអាហារទាំងអស់ដែលត្រូវនឹងលក្ខខណ្ឌ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "status": "ស្ថានភាពការកម្មង់ លំនាំដើមគឺមិនទាន់បានទូទាត់"
        },
        "returns": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកម្មង់ដឹកជញ្ជូនអាហារទាំងអស់ដែលត្រូវនឹងលក្ខខណ្ឌ រួមមានលេខសម្គាល់ការកម្មង់ ប្រភេទការកម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់ហាង តម្លៃសរុប ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកម្មង់ និងព័ត៌មានផ្សេងៗទៀត",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ស្វែងរកកុម្ម៉ង់ដឹកជញ្ជូនអាហារតាម ID កុម្ម៉ង់ ដោយត្រឡប់មកវិញនូវព័ត៌មានលម្អិតរួមមាន ID កុម្ម៉ង់ ប្រភេទកុម្ម៉ង់ ID ហាង ពេលវេលាដឹកជញ្ជូន រយៈពេលដឹកជញ្ជូន ពេលវេលាដល់ដៃ តម្លៃសរុប ពេលវេលាកុម្ម៉ង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពកុម្ម៉ង់ និងបញ្ជីទំនិញ។",
        "preconditions": "បរិបទខាងលើបានកំណត់ order_id កុម្ម៉ង់ដឹកជញ្ជូនអាហារតែមួយគត់។",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃកុម្ម៉ង់ដែលបានកំណត់។",
        "args": {
            "order_id": "ID កុម្ម៉ង់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃកុម្ម៉ង់ដែលបានកំណត់ រួមមាន ID កុម្ម៉ង់ ប្រភេទកុម្ម៉ង់ ID ហាង ពេលវេលាដឹកជញ្ជូន រយៈពេលដឹកជញ្ជូន ពេលវេលាដល់ដៃ តម្លៃសរុប ពេលវេលាកុម្ម៉ង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពកុម្ម៉ង់ និងបញ្ជីទំនិញ។",
        "tool_type": "READ"
    },
}

# Tool descriptions - Kazakh version
TOOL_DESCRIPTIONS_KK = {
    "delivery_distance_to_time": {
        "description": "Қашықтық (метр) негізінде тамақ жеткізу уақытын (минут) есептеу",
        "preconditions": "Сатушыдан пайдаланушы мекенжайына дейінгі қашықтыққа байланысты тамақ жеткізу уақытын есептеу",
        "postconditions": "Жеткізу уақытын (минут) қайтару",
        "args": {
            "distance": "Қашықтық (метрмен)"
        },
        "returns": "Уақыт (минутпен)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Дүкен туралы ақпаратты алу, оған дүкен id-сы, рейтингі, мекенжайы, бойлық, ендік, тегтер және тауарлар тізімі кіреді",
        "preconditions": "Тамақ жеткізу сценарийінде, дүкеннің толық ақпаратын алу қажет",
        "postconditions": "Дүкеннің толық ақпаратын қайтару",
        "args": {
            "store_id": "Дүкен id-сы"
        },
        "returns": "Дүкеннің толық ақпараты",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Тауар ақпаратын алу, оның ішінде тауар атауы, тауар id, дүкен атауы, дүкен id, тауар рейтингі, тауар бағасы, тауар белгілері.",
        "preconditions": "Тамақ жеткізу сценарийінде, тауардың толық ақпаратын алу қажет.",
        "postconditions": "Тауардың толық ақпаратын қайтару.",
        "args": {
            "food_id": "Тауар id"
        },
        "returns": "Тауардың толық ақпараты.",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Тамақ жеткізу сценарийінде пайдаланушының сөздеріне сүйене отырып, дүкендерді сипаттайтын кілт сөздерді алып, бірнеше дүкенді іздеуге немесе ұсынуға болады",
        "preconditions": "Тамақ жеткізу сценарийінде болу, дүкендерді сипаттайтын кілт сөздерді алу",
        "postconditions": "Дүкендер тізімін қайтару, пайдаланушыны нақты дүкенді таңдауға жетелеу",
        "args": {
            "keywords": "Дүкенді сипаттайтын кілт сөздер"
        },
        "returns": "Дүкен ақпаратының құрылымдалған шығысы",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Тамақ жеткізу қызметінде, пайдаланушының сұранысынан тауарды сипаттайтын кілт сөздерді анықтап, бірнеше тауарды іздеуге немесе ұсынуға болады",
        "preconditions": "Тамақ жеткізу қызметінде болу, тауарды сипаттайтын кілт сөздерді алу",
        "postconditions": "Тауарлар тізімін қайтару, пайдаланушыны тауар таңдауға және тапсырыс жасауға бағыттау",
        "args": {
            "keywords": "Тауарды сипаттайтын кілт сөздер"
        },
        "returns": "Құрылымдалған түрде шығарылған тауар ақпараты",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Тамақ жеткізу тапсырысын құру, тек бір дүкенге тапсырыс беруге болады, бір дүкеннен бірнеше тауар тапсырыс беруге рұқсат етіледі",
        "preconditions": "Тамақ жеткізу жағдайында, бірегей дүкен id және бір немесе бірнеше тауар id анықталуы тиіс, пайдаланушының тағамдық тыйымдары анықталып, тапсырыста көрсетілуі керек",
        "postconditions": "Тапсырыс ақпаратын қайтару және пайдаланушыдан тапсырысты төлеуін сұрау",
        "args": {
            "user_id": "Пайдаланушы id",
            "store_id": "Дүкен id",
            "food_ids": "Тауар id тізімі",
            "food_cnts": "Тауар id-ге сәйкес сандар тізімі",
            "address": "Тамақ жеткізу мекенжайы",
            "dispatch_time": "Тамақ жеткізу тапсырысын бастау уақыты (яғни курьердің дүкеннен тамақты алып шығу уақыты), пішімі yyyy-mm-dd HH:MM:SS",
            "attributes": "Тауар id-ге сәйкес тауар сипаттамалары",
            "note": "Тапсырыс ескертпесі (пайдаланушының уақыт бойынша сұраныстарын тікелей ескертпеге жазуға тыйым салынады), мысалы тағамдық тыйымдар туралы ақпарат"
        },
        "returns": "Егер сәтті құрылса, тапсырыс ақпаратын қайтару (тапсырыс id, пайдаланушы id, дүкен id, тауар id тізімі, тауар саны тізімі, мекенжай, тапсырыс уақыты, жаңарту уақыты, тапсырыс күйі, тауарлар тізімі, ескертпе қамтиды), әйтпесе тиісті хабарламаны қайтару",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Тамақ жеткізу сценарийінде, контексте тапсырыс ақпараты бар, пайдаланушы төлемді растауды немесе қайта төлеуді білдіреді",
        "preconditions": "Тамақ жеткізу сценарийінде болу, пайдаланушы төлемді растауды білдіру, тапсырыс жасалып төлем кезеңіне өту｜пайдаланушы қайта төлеуді білдіру",
        "postconditions": "Төлем нәтижесі туралы ақпаратты қайтару",
        "args": {
            "order_id": "Тапсырыс идентификаторы"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Тапсырыс статусын алу",
        "preconditions": "Жеткізу тапсырысының статусын тексеру",
        "postconditions": "Тапсырыс статусы туралы ақпаратты қайтару",
        "args": {
            "order_id": "Тапсырыс идентификаторы"
        },
        "returns": "Тапсырыс статусы туралы ақпарат",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Пайдаланушы тапсырысты немесе төлемді жоққа шығарады. Жоққа шығарылған күйдегі тапсырысты қайта жоққа шығаруға тыйым салынады.",
        "preconditions": "Тамақ жеткізу тапсырысының күйін тексеру, тапсырыс күйінің cancelled емес екеніне көз жеткізу.",
        "postconditions": "Тапсырысты жоққа шығару нәтижесі туралы ақпаратты қайтару.",
        "args": {
            "order_id": "Тапсырыс идентификаторы"
        },
        "returns": "Тапсырысты жоққа шығару нәтижесі туралы ақпарат.",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Тапсырыс ескертпесін өзгерту",
        "preconditions": "Жоғарыда бірегей тамақ жеткізу тапсырысының order_id анықталған, пайдаланушы тамақ жеткізу тапсырысының ескертпесін өзгерткісі келеді",
        "postconditions": "Өзгертілген тапсырыс ақпаратын шығару, егер тапсырыс әлі төленбесе, пайдаланушы төлемді растауы керек",
        "args": {
            "order_id": "Тапсырыс id",
            "note": "Жаңа тапсырыс ескертпесі"
        },
        "returns": "Тапсырыс ескертпесін өзгерту операциясының нәтижесі",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Барлық тамақ жеткізу тапсырыстарын сұрау, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, сатушы ID, жалпы сомасы, тапсырыс беру уақыты, жаңарту уақыты, тапсырыс мәртебесі және басқа ақпаратты қайтару",
        "preconditions": "Сұрау шарттарына сәйкес барлық тамақ жеткізу тапсырыстарын қарау",
        "postconditions": "Барлық сәйкес келетін тамақ жеткізу тапсырыстарының толық ақпаратын қайтару",
        "args": {
            "user_id": "Пайдаланушы ID",
            "status": "Тапсырыс мәртебесі, әдепкісі төленбеген"
        },
        "returns": "Барлық сәйкес келетін тамақ жеткізу тапсырыстарының толық ақпаратын қайтару, соның ішінде тапсырыс ID, тапсырыс түрі, пайдаланушы ID, сатушы ID, жалпы сомасы, тапсырыс беру уақыты, жаңарту уақыты, тапсырыс мәртебесі және басқа ақпарат",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Тапсырыс ID бойынша тамақ жеткізу тапсырысын сұрау, тапсырыс ID, тапсырыс түрі, мерчант ID, жеткізу уақыты, жеткізу ұзақтығы, жеткізілу уақыты, жалпы құны, тапсырыс беру уақыты, жаңарту уақыты, тапсырыс күйі және тауарлар тізімі қамтылған толық ақпаратты қайтару",
        "preconditions": "Алдыңғы мәтінде бірегей тамақ жеткізу тапсырысының order_id анықталған",
        "postconditions": "Көрсетілген тапсырыстың толық ақпаратын қайтару",
        "args": {
            "order_id": "Тапсырыс id"
        },
        "returns": "Көрсетілген тапсырыстың толық ақпараты, тапсырыс ID, тапсырыс түрі, мерчант ID, жеткізу уақыты, жеткізу ұзақтығы, жеткізілу уақыты, жалпы құны, тапсырыс беру уақыты, жаңарту уақыты, тапсырыс күйі және тауарлар тізімін қамтиды",
        "tool_type": "READ"
    },
}

# Tool descriptions - Punjabi version
TOOL_DESCRIPTIONS_PA = {
    "delivery_distance_to_time": {
        "description": "ਦੂਰੀ (ਮੀਟਰ) ਦੇ ਅਧਾਰ ਤੇ ਫੂਡ ਡਿਲੀਵਰੀ ਸਮਾਂ (ਮਿੰਟ) ਦੀ ਗਣਨਾ ਕਰੋ",
        "preconditions": "ਵਿਕਰੇਤਾ ਤੋਂ ਉਪਭੋਗਤਾ ਦੇ ਪਤੇ ਤੱਕ ਦੀ ਦੂਰੀ ਦੇ ਅਧਾਰ ਤੇ ਫੂਡ ਡਿਲੀਵਰੀ ਸਮਾਂ ਦੀ ਗਣਨਾ ਕਰੋ",
        "postconditions": "ਡਿਲੀਵਰੀ ਸਮਾਂ (ਮਿੰਟ) ਵਾਪਸ ਕਰੋ",
        "args": {
            "distance": "ਦੂਰੀ (ਮੀਟਰਾਂ ਵਿੱਚ)"
        },
        "returns": "ਸਮਾਂ (ਮਿੰਟਾਂ ਵਿੱਚ)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "ਵਿਕਰੇਤਾ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਵਿਕਰੇਤਾ ਆਈਡੀ, ਰੇਟਿੰਗ, ਪਤਾ, ਦੇਸ਼ਾਂਤਰ, ਅਕਸ਼ਾਂਸ਼, ਟੈਗ, ਅਤੇ ਉਤਪਾਦ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਵਿਕਰੇਤਾ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਵਿਕਰੇਤਾ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "store_id": "ਵਿਕਰੇਤਾ ਆਈਡੀ"
        },
        "returns": "ਵਿਕਰੇਤਾ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "ਖਾਣੇ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਖਾਣੇ ਦਾ ਨਾਮ, ਖਾਣੇ ਦੀ ਆਈਡੀ, ਦੁਕਾਨ ਦਾ ਨਾਮ, ਦੁਕਾਨ ਦੀ ਆਈਡੀ, ਖਾਣੇ ਦੀ ਰੇਟਿੰਗ, ਖਾਣੇ ਦੀ ਕੀਮਤ, ਖਾਣੇ ਦੇ ਟੈਗ ਸ਼ਾਮਲ ਹਨ।",
        "preconditions": "ਟੇਕਆਉਟ ਸਥਿਤੀ ਵਿੱਚ, ਖਾਣੇ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਖਾਣੇ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "food_id": "ਖਾਣੇ ਦੀ ਆਈਡੀ"
        },
        "returns": "ਖਾਣੇ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "ਫੂਡ ਡਿਲੀਵਰੀ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਦੀ ਗੱਲਬਾਤ ਤੋਂ ਵਿਕਰੇਤਾਵਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ ਕੱਢੇ ਜਾ ਸਕਦੇ ਹਨ, ਅਤੇ ਕਈ ਵਿਕਰੇਤਾਵਾਂ ਦੀ ਖੋਜ ਜਾਂ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾ ਸਕਦੀ ਹੈ",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਸਥਿਤੀ ਵਿੱਚ ਹੋਣਾ, ਵਿਕਰੇਤਾਵਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ ਪ੍ਰਾਪਤ ਕਰਨਾ",
        "postconditions": "ਵਿਕਰੇਤਾਵਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰਨਾ, ਉਪਭੋਗਤਾ ਨੂੰ ਵਿਕਰੇਤਾ ਚੁਣਨ ਅਤੇ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰਨਾ",
        "args": {
            "keywords": "ਵਿਕਰੇਤਾਵਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ"
        },
        "returns": "ਵਿਕਰੇਤਾ ਜਾਣਕਾਰੀ ਦੀ ਬਣਤਰੀ ਆਉਟਪੁਟ",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "ਫੂਡ ਡਿਲੀਵਰੀ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਦੀ ਗੱਲਬਾਤ ਤੋਂ ਉਤਪਾਦਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ ਕੱਢੇ ਜਾ ਸਕਦੇ ਹਨ ਤਾਂ ਜੋ ਕਈ ਉਤਪਾਦਾਂ ਦੀ ਖੋਜ ਜਾਂ ਸਿਫਾਰਸ਼ ਕੀਤੀ ਜਾ ਸਕੇ।",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਦੀ ਸਥਿਤੀ ਵਿੱਚ ਹੋਣਾ ਅਤੇ ਉਤਪਾਦਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ ਪ੍ਰਾਪਤ ਕਰਨੇ।",
        "postconditions": "ਉਤਪਾਦਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਉਤਪਾਦ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਬਣਾਉਣ ਲਈ ਅਗਵਾਈ ਕਰੋ।",
        "args": {
            "keywords": "ਉਤਪਾਦਾਂ ਦਾ ਵਰਣਨ ਕਰਨ ਵਾਲੇ ਮੁੱਖ ਸ਼ਬਦ"
        },
        "returns": "ਢਾਂਚਾਗਤ ਆਉਟਪੁੱਟ ਉਤਪਾਦ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "ਟੇਕਆਵੇ ਆਰਡਰ ਬਣਾਉਣਾ, ਸਿਰਫ਼ ਇੱਕ ਹੀ ਵਿਕਰੇਤਾ ਤੋਂ ਆਰਡਰ ਕਰਨ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ, ਇੱਕ ਵਿਕਰੇਤਾ ਤੋਂ ਕਈ ਵਸਤੂਆਂ ਆਰਡਰ ਕੀਤੀਆਂ ਜਾ ਸਕਦੀਆਂ ਹਨ",
        "preconditions": "ਟੇਕਆਵੇ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਇੱਕ ਅਨੋਖੇ ਸਟੋਰ ਆਈਡੀ ਅਤੇ ਇੱਕ ਜਾਂ ਵਧੇਰੇ ਖਾਣੇ ਦੇ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕਰੋ, ਉਪਭੋਗਤਾ ਦੀਆਂ ਖੁਰਾਕ ਪਾਬੰਦੀਆਂ ਨਿਰਧਾਰਤ ਕਰੋ, ਅਤੇ ਆਰਡਰ ਵਿੱਚ ਇਸਨੂੰ ਸ਼ਾਮਲ ਕਰੋ",
        "postconditions": "ਆਰਡਰ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਪੁੱਛੋ ਕਿ ਕੀ ਉਹ ਆਰਡਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹਨ",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ",
            "store_id": "ਦੁਕਾਨ ਆਈਡੀ",
            "food_ids": "ਖਾਣੇ ਦੇ ਆਈਡੀ ਦੀ ਸੂਚੀ",
            "food_cnts": "ਖਾਣੇ ਦੇ ਆਈਡੀ ਦੇ ਅਨੁਰੂਪ ਮਾਤਰਾ ਸੂਚੀ",
            "address": "ਟੇਕਆਵੇ ਡਿਲੀਵਰੀ ਟੀਚਾ ਪਤਾ",
            "dispatch_time": "ਟੇਕਆਵੇ ਆਰਡਰ ਡਿਲੀਵਰੀ ਸ਼ੁਰੂ ਕਰਨ ਦਾ ਸਮਾਂ (ਭਾਵ ਜਦੋਂ ਰਾਈਡਰ ਵਿਕਰੇਤਾ ਤੋਂ ਖਾਣਾ ਲੈ ਕੇ ਰਵਾਨਾ ਹੁੰਦਾ ਹੈ), ਫਾਰਮੈਟ yyyy-mm-dd HH:MM:SS",
            "attributes": "ਖਾਣੇ ਦੇ ਆਈਡੀ ਦੇ ਅਨੁਰੂਪ ਖਾਣੇ ਦੀਆਂ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ",
            "note": "ਆਰਡਰ ਨੋਟਸ (ਸਮੇਂ ਬਾਰੇ ਉਪਭੋਗਤਾ ਦੀਆਂ ਲੋੜਾਂ ਨੂੰ ਸਿੱਧੇ ਤੌਰ 'ਤੇ ਨੋਟਸ ਵਿੱਚ ਪਾਉਣ ਦੀ ਮਨਾਹੀ ਹੈ), ਜਿਵੇਂ ਕਿ ਖੁਰਾਕ ਪਾਬੰਦੀਆਂ ਦੀ ਜਾਣਕਾਰੀ"
        },
        "returns": "ਜੇਕਰ ਬਣਾਉਣਾ ਸਫਲ ਹੁੰਦਾ ਹੈ, ਤਾਂ ਆਰਡਰ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ (ਜਿਸ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ, ਉਪਭੋਗਤਾ ਆਈਡੀ, ਦੁਕਾਨ ਆਈਡੀ, ਖਾਣੇ ਦੇ ਆਈਡੀ ਦੀ ਸੂਚੀ, ਖਾਣੇ ਦੀ ਮਾਤਰਾ ਸੂਚੀ, ਪਤਾ, ਆਰਡਰ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ, ਖਾਣੇ ਦੀ ਸੂਚੀ, ਨੋਟਸ ਸ਼ਾਮਲ ਹਨ), ਨਹੀਂ ਤਾਂ ਸੰਬੰਧਿਤ ਸੂਚਨਾ ਵਾਪਸ ਕਰੋ",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "ਫੂਡ ਡਿਲੀਵਰੀ ਸਥਿਤੀ ਵਿੱਚ, ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਜਾਣਕਾਰੀ ਹੈ, ਉਪਭੋਗਤਾ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਜਾਂ ਮੁੜ ਭੁਗਤਾਨ ਕਰਨ ਦਾ ਇਸ਼ਾਰਾ ਕਰਦਾ ਹੈ।",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਦਾ ਹੈ, ਆਰਡਰ ਬਣ ਚੁੱਕਾ ਹੈ ਅਤੇ ਭੁਗਤਾਨ ਪੜਾਅ ਵਿੱਚ ਹੈ | ਉਪਭੋਗਤਾ ਮੁੜ ਭੁਗਤਾਨ ਦਾ ਇਸ਼ਾਰਾ ਕਰਦਾ ਹੈ।",
        "postconditions": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ਆਰਡਰ ਸਥਿਤੀ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰ ਸਥਿਤੀ ਦੀ ਜਾਂਚ ਕਰੋ",
        "postconditions": "ਆਰਡਰ ਸਥਿਤੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਸਥਿਤੀ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਆਰਡਰ ਰੱਦ ਕਰਦਾ ਹੈ, ਜਾਂ ਵਰਤੋਂਕਾਰ ਭੁਗਤਾਨ ਰੱਦ ਕਰਦਾ ਹੈ। ਪਹਿਲਾਂ ਹੀ ਰੱਦ ਕੀਤੀ ਸਥਿਤੀ ਵਿੱਚ ਆਰਡਰ ਨੂੰ ਦੁਬਾਰਾ ਰੱਦ ਕਰਨਾ ਮਨਾ ਹੈ।",
        "preconditions": "ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰ ਸਥਿਤੀ ਦੀ ਜਾਂਚ ਕਰੋ, ਯਕੀਨੀ ਬਣਾਓ ਕਿ ਆਰਡਰ ਸਥਿਤੀ ਰੱਦ ਕੀਤੀ ਨਹੀਂ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੇ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "ਆਰਡਰ ਨੋਟ ਜਾਣਕਾਰੀ ਨੂੰ ਸੋਧੋ",
        "preconditions": "ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਇੱਕ ਅਨੋਖਾ ਟੇਕਅਵੇਟ order_id ਨਿਰਧਾਰਤ ਕੀਤਾ ਗਿਆ ਹੈ, ਉਪਭੋਗਤਾ ਨੂੰ ਟੇਕਅਵੇਟ ਆਰਡਰ ਨੋਟ ਨੂੰ ਸੋਧਣ ਦੀ ਲੋੜ ਹੈ",
        "postconditions": "ਸੋਧੇ ਗਏ ਆਰਡਰ ਦੀ ਜਾਣਕਾਰੀ ਆਉਟਪੁੱਟ ਕਰੋ, ਜੇਕਰ ਆਰਡਰ ਅਜੇ ਅਦਾ ਨਹੀਂ ਕੀਤਾ ਗਿਆ ਹੈ ਤਾਂ ਉਪਭੋਗਤਾ ਨੂੰ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਦੀ ਲੋੜ ਹੈ",
        "args": {
            "order_id": "ਆਰਡਰ id",
            "note": "ਨਵੀਂ ਆਰਡਰ ਨੋਟ ਜਾਣਕਾਰੀ"
        },
        "returns": "ਆਰਡਰ ਨੋਟ ਨੂੰ ਸੋਧਣ ਦੀ ਕਾਰਵਾਈ ਦਾ ਨਤੀਜਾ",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "ਸਾਰੇ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਮਰਚੈਂਟ ID, ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਆਦਿ ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਕੁਏਰੀ ਸ਼ਰਤਾਂ ਦੇ ਅਨੁਸਾਰ ਸਾਰੇ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰਾਂ ਨੂੰ ਵੇਖੋ।",
        "postconditions": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੇ ਸਾਰੇ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "user_id": "ਉਪਭੋਗਤਾ ID",
            "status": "ਆਰਡਰ ਸਥਿਤੀ, ਮੂਲ ਰੂਪ ਵਿੱਚ ਅਣਚੁਕਾਈ ਹੋਈ"
        },
        "returns": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੇ ਸਾਰੇ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰਾਂ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਮਰਚੈਂਟ ID, ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਆਦਿ ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਹੈ।",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ਆਰਡਰ ID ਦੇ ਅਧਾਰ ਤੇ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਮਰਚੈਂਟ ID, ਡਿਲੀਵਰੀ ਸਮਾਂ, ਡਿਲੀਵਰੀ ਅਵਧੀ, ਪਹੁੰਚਣ ਦਾ ਸਮਾਂ, ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਈਟਮਾਂ ਦੀ ਸੂਚੀ ਸਮੇਤ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਆਉਂਦੀ ਹੈ।",
        "preconditions": "ਉਪਰੋਕਤ ਸੰਦਰਭ ਵਿੱਚ ਇੱਕ ਅਨੋਖਾ ਫੂਡ ਡਿਲੀਵਰੀ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "postconditions": "ਨਿਰਧਾਰਤ ਆਰਡਰ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਨਿਰਧਾਰਤ ਆਰਡਰ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਮਰਚੈਂਟ ID, ਡਿਲੀਵਰੀ ਸਮਾਂ, ਡਿਲੀਵਰੀ ਅਵਧੀ, ਪਹੁੰਚਣ ਦਾ ਸਮਾਂ, ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਈਟਮਾਂ ਦੀ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "tool_type": "READ"
    },
}

# Tool descriptions - Belarusian version
TOOL_DESCRIPTIONS_BE = {
    "delivery_distance_to_time": {
        "description": "Вылічае час дастаўкі ежы (у хвілінах) на аснове адлегласці (у метрах)",
        "preconditions": "Вылічае час дастаўкі ежы на аснове адлегласці ад крамы да адраса карыстальніка",
        "postconditions": "Вяртае час дастаўкі (у хвілінах)",
        "args": {
            "distance": "Адлегласць (у метрах)"
        },
        "returns": "Час (у хвілінах)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Атрымаць інфармацыю пра краму, уключаючы ід крамы, рэйтынг, адрас, даўгату, шырыню, тэгі, спіс тавараў",
        "preconditions": "У сцэнары дастаўкі ежы, калі патрабуецца атрымаць падрабязную інфармацыю пра краму",
        "postconditions": "Вяртае падрабязную інфармацыю пра краму",
        "args": {
            "store_id": "ід крамы"
        },
        "returns": "Падрабязная інфармацыя пра краму",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Атрымаць інфармацыю аб тавары, уключаючы назву тавару, id тавару, назву крамы, id крамы, рэйтынг тавару, цану тавару, тэгі тавару",
        "preconditions": "У сцэнары дастаўкі ежы, неабходна атрымаць падрабязную інфармацыю аб тавары",
        "postconditions": "Вяртае падрабязную інфармацыю аб тавары",
        "args": {
            "food_id": "id тавару"
        },
        "returns": "Падрабязная інфармацыя аб тавары",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "У сцэнарыі дастаўкі ежы можна вылучыць ключавыя словы, якія апісваюць гандлёвыя кропкі, на аснове выказванняў карыстальніка, каб шукаць або рэкамендаваць некалькі гандлёвых кропак",
        "preconditions": "Знаходзіцца ў сцэнарыі дастаўкі ежы, атрыманне ключавых слоў, якія апісваюць гандлёвыя кропкі",
        "postconditions": "Вяртаецца спіс гандлёвых кропак, карыстальніка накіроўваюць на выбар і пацверджанне канкрэтнай кропкі",
        "args": {
            "keywords": "Ключавыя словы, якія апісваюць гандлёвыя кропкі"
        },
        "returns": "Структураваная інфармацыя пра гандлёвыя кропкі",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "У сцэнарыі дастаўкі ежы можна вылучыць ключавыя словы, якія апісваюць тавары, на аснове выказванняў карыстальніка, каб шукаць або рэкамендаваць некалькі тавараў",
        "preconditions": "Знаходзіцца ў сцэнарыі дастаўкі ежы, атрыманне ключавых слоў, якія апісваюць тавары",
        "postconditions": "Вяртаецца спіс тавараў, карыстальніка накіроўваюць на выбар тавару і стварэнне замовы",
        "args": {
            "keywords": "Ключавыя словы, якія апісваюць тавары"
        },
        "returns": "Структураваная інфармацыя пра тавары",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Стварэнне замовы на дастаўку ежы, падтрымліваецца толькі заказ у адной крамы, ад адной крамы можна заказаць некалькі тавараў",
        "preconditions": "У сцэнары дастаўкі ежы вызначце ўнікальны ідэнтыфікатар крамы і адзін або некалькі ідэнтыфікатараў тавараў, вызначце дыетарычныя абмежаванні карыстальніка і адлюструйце іх у замове",
        "postconditions": "Вярнуць інфармацыю пра заказ, спытаць карыстальніка, ці жадае ён аплаціць заказ",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "store_id": "Ідэнтыфікатар крамы",
            "food_ids": "Спіс ідэнтыфікатараў тавараў",
            "food_cnts": "Спіс колькасці тавараў адпаведна ідэнтыфікатарам",
            "address": "Мэтавы адрас дастаўкі ежы",
            "dispatch_time": "Час пачатку дастаўкі замовы на ежу (г.зн. час, калі кур'ер адпраўляецца ад крамы з ежай), фармат yyyy-mm-dd HH:MM:SS",
            "attributes": "Атрыбуты спецыфікацыі тавару адпаведна ідэнтыфікатару тавару",
            "note": "Заўвагі да замовы (забаронена змяшчаць патрабаванні карыстальніка адносна часу і г.д. непасрэдна ў заўвагах), напрыклад, апісанне інфармацыі пра дыетарычныя абмежаванні"
        },
        "returns": "Калі стварэнне паспяховае, вярнуць інфармацыю пра заказ (уключае ідэнтыфікатар замовы, ідэнтыфікатар карыстальніка, ідэнтыфікатар крамы, спіс ідэнтыфікатараў тавараў, спіс колькасці тавараў, адрас, час афармлення замовы, час абнаўлення, статус замовы, спіс тавараў, заўвагі), у адваротным выпадку вярнуць адпаведную інфармацыю з падказкай",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "У сцэнарыі дастаўкі ежы, калі вышэй ёсць інфармацыя пра заказ, карыстальнік пацвярджае аплату або ініцыюе паўторную аплату",
        "preconditions": "У сцэнарыі дастаўкі ежы, карыстальнік пацвярджае аплату, заказ створаны і перайшоў да этапу аплаты | Карыстальнік ініцыюе паўторную аплату",
        "postconditions": "Вяртае інфармацыю пра вынік аплаты",
        "args": {
            "order_id": "ід заказа"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Атрымаць статус заказа",
        "preconditions": "Запыт статусу заказа на дастаўку ежы",
        "postconditions": "Вяртае інфармацыю аб статусе заказа",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Інфармацыя аб статусе заказа",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Карыстальнік скасоўвае заказ або аплату. Забаронена паўторна скасоўваць заказ, які ўжо скасаваны.",
        "preconditions": "Запытаць статус заказу дастаўкі ежы, пераканацца, што статус заказу не скасаваны",
        "postconditions": "Вярнуць інфармацыю пра вынік скасавання заказу",
        "args": {
            "order_id": "ID заказу"
        },
        "returns": "Інфармацыя пра вынік скасавання заказу",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Змяніць інфармацыю аб заўвагах да заказа",
        "preconditions": "У папярэднім кантэксце вызначаны адзіны order_id для заказа на дастаўку ежы, карыстальніку неабходна змяніць заўвагі да заказа",
        "postconditions": "Вывад інфармацыі аб змененым заказе; калі заказ яшчэ не аплачаны, неабходна пацверджанне аплаты ад карыстальніка",
        "args": {
            "order_id": "Ідэнтыфікатар заказа",
            "note": "Новая інфармацыя аб заўвагах да заказа"
        },
        "returns": "Вынік аперацыі па змене заўваг да заказа",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Запытаць усе заказы дастаўкі ежы, вярнуць інфармацыю, якая ўключае ID заказа, тып заказа, ID карыстальніка, ID прадаўца, агульную суму, час размяшчэння заказа, час абнаўлення, статус заказа і г.д.",
        "preconditions": "Праглядзець усе заказы дастаўкі ежы ў адпаведнасці з умовамі запыту",
        "postconditions": "Вярнуць падрабязную інфармацыю пра ўсе заказы дастаўкі ежы, якія адпавядаюць умовам",
        "args": {
            "user_id": "ID карыстальніка",
            "status": "Статус заказа, па змаўчанні не аплачана"
        },
        "returns": "Вярнуць падрабязную інфармацыю пра ўсе заказы дастаўкі ежы, якія адпавядаюць умовам, уключаючы ID заказа, тып заказа, ID карыстальніка, ID прадаўца, агульную суму, час размяшчэння заказа, час абнаўлення, статус заказа і г.д.",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Запыт заказа дастаўкі ежы па ID заказа, вяртае падрабязную інфармацыю, якая ўтрымлівае ID заказа, тып заказа, ID рэстарана, час дастаўкі, працягласць дастаўкі, час прыбыцця, агульную суму, час размяшчэння заказа, час абнаўлення, статус заказа і спіс тавараў",
        "preconditions": "Папярэдні кантэкст вызначае адзіны ID заказа дастаўкі ежы",
        "postconditions": "Вяртае падрабязную інфармацыю аб указаным заказе",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Падрабязная інфармацыя аб указаным заказе, уключаючы ID заказа, тып заказа, ID рэстарана, час дастаўкі, працягласць дастаўкі, час прыбыцця, агульную суму, час размяшчэння заказа, час абнаўлення, статус заказа і спіс тавараў",
        "tool_type": "READ"
    },
}

# Tool descriptions - Malay version
TOOL_DESCRIPTIONS_MS = {
    "delivery_distance_to_time": {
        "description": "Mengira masa penghantaran makanan (minit) berdasarkan jarak (meter)",
        "preconditions": "Mengira masa penghantaran makanan berdasarkan jarak dari penjual ke alamat pengguna",
        "postconditions": "Memulangkan masa penghantaran (minit)",
        "args": {
            "distance": "Jarak (dalam meter)"
        },
        "returns": "Masa (dalam minit)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Dapatkan maklumat pedagang, termasuk id pedagang, penilaian, alamat, longitud, latitud, tag, senarai produk",
        "preconditions": "Dalam senario penghantaran makanan, perlu mendapatkan maklumat terperinci pedagang",
        "postconditions": "Memulangkan maklumat terperinci pedagang",
        "args": {
            "store_id": "id pedagang"
        },
        "returns": "Maklumat terperinci pedagang",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Dapatkan maklumat produk, termasuk nama produk, id produk, nama kedai, id kedai, penilaian produk, harga produk, tag produk",
        "preconditions": "Dalam senario penghantaran makanan, perlu mendapatkan maklumat terperinci produk",
        "postconditions": "Mengembalikan maklumat terperinci produk",
        "args": {
            "food_id": "id produk"
        },
        "returns": "Maklumat terperinci produk",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Dalam konteks penghantaran makanan, kata kunci yang menerangkan kedai boleh diekstrak berdasarkan ungkapan pengguna untuk mencari atau mengesyorkan beberapa kedai.",
        "preconditions": "Berada dalam konteks penghantaran makanan dan mendapatkan kata kunci yang menerangkan kedai.",
        "postconditions": "Memulangkan senarai kedai dan membimbing pengguna untuk memilih serta menentukan kedai.",
        "args": {
            "keywords": "Kata kunci yang menerangkan kedai"
        },
        "returns": "Maklumat kedai yang dikeluarkan secara berstruktur",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Dalam senario penghantaran makanan, boleh mengekstrak kata kunci yang menerangkan produk berdasarkan ungkapan pengguna untuk mencari atau mengesyorkan beberapa produk",
        "preconditions": "Berada dalam senario penghantaran makanan, mendapatkan kata kunci yang menerangkan produk",
        "postconditions": "Mengembalikan senarai produk, membimbing pengguna untuk memilih produk dan mencipta pesanan",
        "args": {
            "keywords": "Kata kunci yang menerangkan produk"
        },
        "returns": "Maklumat produk yang dikeluarkan secara berstruktur",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Penciptaan pesanan penghantaran makanan, hanya menyokong pesanan dari satu peniaga, satu peniaga boleh memesan beberapa item",
        "preconditions": "Berada dalam senario penghantaran makanan, tentukan ID kedai yang unik dan satu atau lebih ID makanan, tentukan pantangan diet pengguna, dan maklumkannya dalam pesanan",
        "postconditions": "Kembalikan maklumat pesanan, tanya pengguna sama ada ingin membayar pesanan",
        "args": {
            "user_id": "ID pengguna",
            "store_id": "ID kedai",
            "food_ids": "Senarai ID makanan",
            "food_cnts": "Senarai kuantiti yang sepadan dengan ID makanan",
            "address": "Alamat sasaran penghantaran makanan",
            "dispatch_time": "Masa penghantaran pesanan makanan dimulakan (iaitu masa rider bertolak dari peniaga untuk mengambil makanan), format ialah yyyy-mm-dd HH:MM:SS",
            "attributes": "Atribut spesifikasi makanan yang sepadan dengan ID makanan",
            "note": "Nota pesanan (dilarang meletakkan keperluan pengguna mengenai masa dll. secara langsung dalam nota), seperti penjelasan maklumat pantangan diet"
        },
        "returns": "Jika penciptaan berjaya, kembalikan maklumat pesanan (mengandungi ID pesanan, ID pengguna, ID kedai, senarai ID makanan, senarai kuantiti makanan, alamat, masa pesanan, masa kemaskini, status pesanan, senarai makanan, nota), jika tidak kembalikan maklumat prompt yang berkaitan",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Dalam senario penghantaran makanan, maklumat pesanan wujud dalam konteks sebelumnya, pengguna menyatakan pengesahan pembayaran, atau pembayaran semula",
        "preconditions": "Berada dalam senario penghantaran makanan, pengguna menyatakan pengesahan pembayaran, pesanan telah selesai dicipta dan memasuki peringkat pembayaran｜Pengguna menyatakan pembayaran semula",
        "postconditions": "Memulangkan maklumat hasil pembayaran",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Dapatkan status pesanan",
        "preconditions": "Semak status pesanan penghantaran makanan",
        "postconditions": "Kembalikan maklumat status pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Maklumat status pesanan",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Pengguna membatalkan pesanan atau pembayaran. Dilarang membatalkan pesanan yang telah berstatus dibatalkan.",
        "preconditions": "Semak status pesanan penghantaran makanan, pastikan status pesanan bukan dibatalkan.",
        "postconditions": "Memulangkan maklumat hasil pembatalan pesanan.",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Maklumat hasil pembatalan pesanan.",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Ubah maklumat catatan pesanan",
        "preconditions": "ID pesanan penghantaran makanan yang unik telah ditentukan sebelumnya, pengguna perlu mengubah catatan pesanan tersebut",
        "postconditions": "Keluarkan maklumat pesanan yang telah diubah, jika pesanan belum dibayar maka pengguna perlu mengesahkan pembayaran",
        "args": {
            "order_id": "ID pesanan",
            "note": "Maklumat catatan pesanan baharu"
        },
        "returns": "Hasil operasi mengubah catatan pesanan",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Semak semua pesanan makanan luar, mengembalikan maklumat termasuk ID pesanan, jenis pesanan, ID pengguna, ID peniaga, jumlah harga, masa pesanan, masa kemaskini, status pesanan, dan lain-lain",
        "preconditions": "Paparkan semua pesanan makanan luar berdasarkan syarat carian",
        "postconditions": "Memulangkan maklumat terperinci bagi semua pesanan makanan luar yang memenuhi syarat",
        "args": {
            "user_id": "ID Pengguna",
            "status": "Status pesanan, secara lalai ialah belum dibayar"
        },
        "returns": "Memulangkan maklumat terperinci bagi semua pesanan makanan luar yang memenuhi syarat, termasuk ID pesanan, jenis pesanan, ID pengguna, ID peniaga, jumlah harga, masa pesanan, masa kemaskini, status pesanan, dan lain-lain",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Dapatkan pesanan penghantaran makanan berdasarkan ID Pesanan, mengembalikan maklumat terperinci termasuk ID Pesanan, Jenis Pesanan, ID Peniaga, Masa Penghantaran, Tempoh Penghantaran, Masa Tiba, Jumlah Harga, Masa Pesanan, Masa Kemaskini, Status Pesanan dan Senarai Item",
        "preconditions": "ID pesanan penghantaran makanan yang unik telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Kembalikan maklumat terperinci bagi pesanan yang ditentukan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Maklumat terperinci bagi pesanan yang ditentukan, termasuk ID Pesanan, Jenis Pesanan, ID Peniaga, Masa Penghantaran, Tempoh Penghantaran, Masa Tiba, Jumlah Harga, Masa Pesanan, Masa Kemaskini, Status Pesanan dan Senarai Item",
        "tool_type": "READ"
    },
}

# Tool descriptions - Vietnamese version
TOOL_DESCRIPTIONS_VI = {
    "delivery_distance_to_time": {
        "description": "Tính thời gian giao đồ ăn (phút) dựa trên khoảng cách (mét)",
        "preconditions": "Tính thời gian giao đồ ăn dựa trên khoảng cách từ cửa hàng đến địa chỉ của người dùng",
        "postconditions": "Trả về thời gian giao hàng (phút)",
        "args": {
            "distance": "Khoảng cách (tính bằng mét)"
        },
        "returns": "Thời gian (tính bằng phút)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Lấy thông tin nhà hàng, bao gồm id nhà hàng, đánh giá, địa chỉ, kinh độ, vĩ độ, nhãn, danh sách sản phẩm",
        "preconditions": "Trong ngữ cảnh giao đồ ăn, cần lấy thông tin chi tiết của nhà hàng",
        "postconditions": "Trả về thông tin chi tiết của nhà hàng",
        "args": {
            "store_id": "id nhà hàng"
        },
        "returns": "Thông tin chi tiết của nhà hàng",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Lấy thông tin sản phẩm, bao gồm tên sản phẩm, id sản phẩm, tên cửa hàng, id cửa hàng, đánh giá sản phẩm, giá sản phẩm, nhãn sản phẩm",
        "preconditions": "Trong ngữ cảnh đặt đồ ăn, cần lấy thông tin chi tiết của sản phẩm",
        "postconditions": "Trả về thông tin chi tiết của sản phẩm",
        "args": {
            "food_id": "id sản phẩm"
        },
        "returns": "Thông tin chi tiết của sản phẩm",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Trong ngữ cảnh giao đồ ăn, có thể trích xuất các từ khóa mô tả nhà hàng dựa trên biểu đạt của người dùng để tìm kiếm hoặc đề xuất nhiều nhà hàng",
        "preconditions": "Đang trong ngữ cảnh giao đồ ăn, đã có các từ khóa mô tả nhà hàng",
        "postconditions": "Trả về danh sách nhà hàng, hướng dẫn người dùng lựa chọn và xác nhận nhà hàng",
        "args": {
            "keywords": "Các từ khóa mô tả nhà hàng"
        },
        "returns": "Thông tin nhà hàng được xuất dưới dạng cấu trúc",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Trong ngữ cảnh giao đồ ăn, có thể trích xuất các từ khóa mô tả sản phẩm dựa trên biểu đạt của người dùng để tìm kiếm hoặc đề xuất nhiều sản phẩm.",
        "preconditions": "Đang trong ngữ cảnh giao đồ ăn, lấy được các từ khóa mô tả sản phẩm.",
        "postconditions": "Trả về danh sách sản phẩm, hướng dẫn người dùng chọn sản phẩm và tạo đơn hàng.",
        "args": {
            "keywords": "Các từ khóa mô tả sản phẩm."
        },
        "returns": "Thông tin sản phẩm được xuất dưới dạng cấu trúc.",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Tạo đơn hàng giao đồ ăn, chỉ hỗ trợ đặt hàng từ một nhà hàng duy nhất, một nhà hàng có thể đặt nhiều món ăn",
        "preconditions": "Đang trong kịch bản giao đồ ăn, xác định duy nhất một ID nhà hàng và một hoặc nhiều ID món ăn, xác định các kiêng kỵ ăn uống của người dùng và thể hiện trong đơn hàng",
        "postconditions": "Trả về thông tin đơn hàng, hỏi người dùng xem có thanh toán đơn hàng không",
        "args": {
            "user_id": "ID người dùng",
            "store_id": "ID cửa hàng",
            "food_ids": "Danh sách ID món ăn",
            "food_cnts": "Danh sách số lượng tương ứng với ID món ăn",
            "address": "Địa chỉ giao hàng mục tiêu",
            "dispatch_time": "Thời gian bắt đầu giao hàng của đơn đồ ăn (tức là thời gian shipper lấy đồ từ nhà hàng và xuất phát), định dạng yyyy-mm-dd HH:MM:SS",
            "attributes": "Thuộc tính quy cách món ăn tương ứng với ID món ăn",
            "note": "Ghi chú đơn hàng (Cấm đưa trực tiếp các yêu cầu về thời gian của người dùng vào ghi chú), ví dụ như thông tin giải thích về kiêng kỵ ăn uống"
        },
        "returns": "Nếu tạo thành công, trả về thông tin đơn hàng (bao gồm ID đơn hàng, ID người dùng, ID cửa hàng, danh sách ID món ăn, danh sách số lượng món ăn, địa chỉ, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng, danh sách món ăn, ghi chú), nếu không trả về thông báo liên quan",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Trong kịch bản giao đồ ăn, thông tin đơn hàng có trong ngữ cảnh trước, người dùng xác nhận thanh toán hoặc thanh toán lại.",
        "preconditions": "Trong kịch bản giao đồ ăn, người dùng xác nhận thanh toán, đơn hàng đã được tạo và chuyển sang giai đoạn thanh toán｜Người dùng yêu cầu thanh toán lại.",
        "postconditions": "Trả về thông tin kết quả thanh toán.",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả thanh toán.",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Lấy trạng thái đơn hàng",
        "preconditions": "Truy vấn trạng thái đơn hàng giao đồ ăn",
        "postconditions": "Trả về thông tin trạng thái đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin trạng thái đơn hàng",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Người dùng hủy đơn hàng, hoặc người dùng hủy thanh toán. Không được phép hủy lại đối với đơn hàng đang ở trạng thái đã hủy.",
        "preconditions": "Truy vấn trạng thái đơn hàng giao đồ ăn, đảm bảo trạng thái đơn hàng không phải là đã hủy",
        "postconditions": "Trả về thông tin kết quả hủy đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả hủy đơn hàng",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Sửa đổi thông tin ghi chú đơn hàng",
        "preconditions": "Ngữ cảnh trước đó đã xác định duy nhất một order_id đơn hàng giao đồ ăn, người dùng cần sửa đổi ghi chú đơn hàng giao đồ ăn",
        "postconditions": "Xuất thông tin đơn hàng sau khi sửa đổi, nếu đơn hàng chưa thanh toán thì cần người dùng xác nhận thanh toán",
        "args": {
            "order_id": "ID đơn hàng",
            "note": "Thông tin ghi chú đơn hàng mới"
        },
        "returns": "Kết quả của thao tác sửa đổi ghi chú đơn hàng",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Truy vấn tất cả đơn hàng giao đồ ăn, trả về thông tin bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID cửa hàng, tổng tiền, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và các thông tin khác",
        "preconditions": "Xem tất cả đơn hàng giao đồ ăn theo điều kiện truy vấn",
        "postconditions": "Trả về thông tin chi tiết của tất cả đơn hàng giao đồ ăn thỏa mãn điều kiện",
        "args": {
            "user_id": "ID người dùng",
            "status": "Trạng thái đơn hàng, mặc định là chưa thanh toán"
        },
        "returns": "Trả về thông tin chi tiết của tất cả đơn hàng giao đồ ăn thỏa mãn điều kiện, bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID cửa hàng, tổng tiền, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và các thông tin khác",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Tra cứu đơn hàng giao đồ ăn dựa trên ID đơn hàng, trả về thông tin chi tiết bao gồm ID đơn hàng, loại đơn hàng, ID nhà hàng, thời gian giao hàng, thời gian vận chuyển, thời gian đến nơi, tổng giá, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và danh sách sản phẩm",
        "preconditions": "Ngữ cảnh trước đó xác định duy nhất một ID đơn hàng giao đồ ăn",
        "postconditions": "Trả về thông tin chi tiết của đơn hàng được chỉ định",
        "args": {
            "order_id": "id đơn hàng"
        },
        "returns": "Thông tin chi tiết của đơn hàng được chỉ định, bao gồm ID đơn hàng, loại đơn hàng, ID nhà hàng, thời gian giao hàng, thời gian vận chuyển, thời gian đến nơi, tổng giá, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và danh sách sản phẩm",
        "tool_type": "READ"
    },
}

# Tool descriptions - Turkish version
TOOL_DESCRIPTIONS_TR = {
    "delivery_distance_to_time": {
        "description": "Mesafeye (metre) göre yemek teslimat süresini (dakika) hesaplar",
        "preconditions": "Restorandan kullanıcı adresine olan mesafeye göre yemek teslimat süresini hesaplar",
        "postconditions": "Teslimat süresini (dakika) döndürür",
        "args": {
            "distance": "Mesafe (metre cinsinden)"
        },
        "returns": "Süre (dakika cinsinden)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Mağaza kimliği, puanı, adresi, boylamı, enlemi, etiketleri ve ürün listesini içeren mağaza bilgilerini getirir.",
        "preconditions": "Yemek teslimatı senaryosunda olunmalı ve mağazanın ayrıntılı bilgilerine ihtiyaç duyulmalıdır.",
        "postconditions": "Mağazanın ayrıntılı bilgilerini döndürür.",
        "args": {
            "store_id": "Mağaza kimliği"
        },
        "returns": "Mağazanın ayrıntılı bilgileri",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Ürün adı, ürün kimliği, mağaza adı, mağaza kimliği, ürün puanı, ürün fiyatı ve ürün etiketleri dahil olmak üzere ürün bilgilerini alır.",
        "preconditions": "Yemek teslimatı senaryosunda olunmalı ve ürünün ayrıntılı bilgilerine ihtiyaç duyulmalıdır.",
        "postconditions": "Ürünün ayrıntılı bilgilerini döndürür.",
        "args": {
            "food_id": "Ürün kimliği"
        },
        "returns": "Ürünün ayrıntılı bilgileri",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Yemek siparişi durumunda, kullanıcının ifadelerine göre işletmeyi tanımlayan anahtar kelimeler çıkarılarak birden fazla işletme aranabilir veya önerilebilir.",
        "preconditions": "Yemek siparişi durumunda olunmalı ve işletmeyi tanımlayan anahtar kelimeler alınmalıdır.",
        "postconditions": "İşletme listesi döndürülür ve kullanıcının bir işletme seçip onaylaması sağlanır.",
        "args": {
            "keywords": "İşletmeyi tanımlayan anahtar kelimeler"
        },
        "returns": "Yapılandırılmış biçimde sunulan işletme bilgileri",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Yemek teslimatı senaryosunda, kullanıcının ifadelerine göre ürünü tanımlayan anahtar kelimeler çıkarılabilir ve birden fazla ürün aranabilir veya önerilebilir.",
        "preconditions": "Yemek teslimatı senaryosunda olmak ve ürünü tanımlayan anahtar kelimeleri almak.",
        "postconditions": "Ürün listesini döndürür, kullanıcıyı ürün seçmeye ve sipariş oluşturmaya yönlendirir.",
        "args": {
            "keywords": "Ürünü tanımlayan anahtar kelimeler"
        },
        "returns": "Yapılandırılmış olarak sunulan ürün bilgileri",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Yemek teslimat siparişi oluşturma, yalnızca tek bir satıcıdan sipariş vermeyi destekler; tek bir satıcıdan birden fazla ürün sipariş edilebilir",
        "preconditions": "Yemek teslimat senaryosunda olun, benzersiz bir satıcı kimliği ve bir veya daha fazla ürün kimliği belirleyin, kullanıcının diyet kısıtlamalarını belirleyin ve bunları siparişte yansıtın",
        "postconditions": "Sipariş bilgilerini döndürün ve kullanıcıya siparişi ödeyip ödemeyeceğini sorun",
        "args": {
            "user_id": "Kullanıcı kimliği",
            "store_id": "Mağaza kimliği",
            "food_ids": "Ürün kimliği listesi",
            "food_cnts": "Ürün kimliğine karşılık gelen miktar listesi",
            "address": "Yemek teslimat hedef adresi",
            "dispatch_time": "Yemek siparişinin teslimata başlama zamanı (yani kuryenin restorandan yemeği alıp yola çıkma zamanı), format yyyy-mm-dd HH:MM:SS",
            "attributes": "Ürün kimliğine karşılık gelen ürün özellikleri",
            "note": "Sipariş notu (kullanıcının zaman gibi taleplerini doğrudan nota koymak yasaktır), diyet kısıtlamaları bilgisi açıklaması gibi"
        },
        "returns": "Başarıyla oluşturulursa sipariş bilgilerini döndürün (sipariş kimliği, kullanıcı kimliği, mağaza kimliği, ürün kimliği listesi, ürün miktar listesi, adres, sipariş verme zamanı, güncelleme zamanı, sipariş durumu, ürün listesi, notlar dahil), aksi takdirde ilgili bilgilendirme mesajını döndürün",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Yemek siparişi senaryosunda, bağlamda sipariş bilgisi vardır, kullanıcı ödemeyi onayladığını veya yeniden ödeme yapacağını belirtir.",
        "preconditions": "Yemek siparişi senaryosunda olunması, kullanıcının ödemeyi onayladığını belirtmesi, siparişin oluşturulmuş ve ödeme aşamasına girmiş olması｜Kullanıcının yeniden ödeme yapacağını belirtmesi",
        "postconditions": "Ödeme sonucu bilgilerini döndürür",
        "args": {
            "order_id": "Sipariş kimliği"
        },
        "returns": "Ödeme sonucu bilgileri",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Sipariş durumunu getir",
        "preconditions": "Yemek siparişi durumunu sorgula",
        "postconditions": "Sipariş durumu bilgilerini döndür",
        "args": {
            "order_id": "Sipariş kimliği"
        },
        "returns": "Sipariş durumu bilgileri",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Kullanıcı siparişi veya ödemeyi iptal eder. Zaten iptal edilmiş olan siparişler tekrar iptal edilemez.",
        "preconditions": "Yemek siparişinin durumunu sorgulayın ve sipariş durumunun iptal edilmediğinden emin olun.",
        "postconditions": "Sipariş iptal sonuç bilgilerini döndürür.",
        "args": {
            "order_id": "Sipariş kimliği"
        },
        "returns": "Sipariş iptal sonuç bilgileri",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Sipariş notu bilgilerini değiştir",
        "preconditions": "Önceki metinde benzersiz bir yemek siparişi order_id belirlenmiştir, kullanıcının yemek siparişi notunu değiştirmesi gerekmektedir",
        "postconditions": "Değiştirilen sipariş bilgilerini çıktı olarak ver, eğer sipariş henüz ödenmediyse kullanıcının ödemeyi onaylaması gerekir",
        "args": {
            "order_id": "Sipariş kimliği",
            "note": "Yeni sipariş notu bilgisi"
        },
        "returns": "Sipariş notunu değiştirme işleminin sonucu",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Tüm yemek teslimat siparişlerini sorgular; sipariş ID'si, sipariş tipi, kullanıcı ID'si, satıcı ID'si, toplam fiyat, sipariş zamanı, güncelleme zamanı, sipariş durumu gibi bilgileri içeren sonuçları döndürür",
        "preconditions": "Sorgu koşullarına göre tüm yemek teslimat siparişlerini görüntüler",
        "postconditions": "Koşullara uyan tüm yemek teslimat siparişlerinin ayrıntılı bilgilerini döndürür",
        "args": {
            "user_id": "Kullanıcı ID'si",
            "status": "Sipariş durumu, varsayılan olarak ödenmemiş"
        },
        "returns": "Koşullara uyan tüm yemek teslimat siparişlerinin ayrıntılı bilgilerini döndürür; sipariş ID'si, sipariş tipi, kullanıcı ID'si, satıcı ID'si, toplam fiyat, sipariş zamanı, güncelleme zamanı, sipariş durumu gibi bilgileri içerir",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Sipariş ID'sine göre yemek siparişini sorgular ve Sipariş ID'si, Sipariş Türü, Mağaza ID'si, Teslimat Zamanı, Teslimat Süresi, Teslimat Varış Zamanı, Toplam Fiyat, Sipariş Verme Zamanı, Güncelleme Zamanı, Sipariş Durumu ve Ürün Listesi gibi ayrıntılı bilgileri döndürür",
        "preconditions": "Yukarıdaki bağlamda benzersiz bir yemek siparişi order_id'si belirlenmelidir",
        "postconditions": "Belirtilen siparişin ayrıntılı bilgilerini döndürür",
        "args": {
            "order_id": "Sipariş id'si"
        },
        "returns": "Belirtilen siparişin ayrıntılı bilgileri; Sipariş ID'si, Sipariş Türü, Mağaza ID'si, Teslimat Zamanı, Teslimat Süresi, Teslimat Varış Zamanı, Toplam Fiyat, Sipariş Verme Zamanı, Güncelleme Zamanı, Sipariş Durumu ve Ürün Listesi dahil",
        "tool_type": "READ"
    },
}

# Tool descriptions - Hebrew version
TOOL_DESCRIPTIONS_HE = {
    "delivery_distance_to_time": {
        "description": "לחשב את זמן משלוח המזון (דקות) על פי המרחק (מטרים)",
        "preconditions": "לחשב את זמן משלוח המזון על פי המרחק מהעסק לכתובת המשתמש",
        "postconditions": "מחזיר את זמן המשלוח (בדקות)",
        "args": {
            "distance": "מרחק (במטרים)"
        },
        "returns": "זמן (בדקות)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "קבלת מידע על העסק, כולל מזהה עסק, דירוג, כתובת, קו אורך, קו רוחב, תגיות, רשימת מוצרים",
        "preconditions": "בתרחיש של משלוחי מזון, נדרש לקבל מידע מפורט על העסק",
        "postconditions": "מחזיר מידע מפורט על העסק",
        "args": {
            "store_id": "מזהה עסק"
        },
        "returns": "מידע מפורט על העסק",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "קבלת מידע על המוצר, כולל שם המוצר, מזהה המוצר, שם החנות, מזהה החנות, דירוג המוצר, מחיר המוצר ותגיות המוצר",
        "preconditions": "בהקשר של משלוחי מזון, נדרש לקבל מידע מפורט על המוצר",
        "postconditions": "מחזיר מידע מפורט על המוצר",
        "args": {
            "food_id": "מזהה המוצר"
        },
        "returns": "מידע מפורט על המוצר",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "בהקשר של משלוחי מזון, ניתן לחלץ מילות מפתח המתארות עסקים על סמך דברי המשתמש, ולחפש או להמליץ על מספר עסקים",
        "preconditions": "בהקשר של משלוחי מזון, קבלת מילות מפתח המתארות עסקים",
        "postconditions": "החזרת רשימת עסקים, הנחיית המשתמש לבחור ולאשר עסק",
        "args": {
            "keywords": "מילות מפתח המתארות את העסק"
        },
        "returns": "מידע על עסקים בפורמט מובנה",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "בתרחיש משלוחי מזון, ניתן לחלץ מילות מפתח המתארות מוצרים בהתבסס על דברי המשתמש, כדי לחפש או להמליץ על מספר מוצרים",
        "preconditions": "בתרחיש משלוחי מזון, השגת מילות מפתח המתארות מוצרים",
        "postconditions": "החזרת רשימת מוצרים, הנחיית המשתמש לבחור מוצר וליצור הזמנה",
        "args": {
            "keywords": "מילות מפתח המתארות את המוצר"
        },
        "returns": "מידע על המוצר בפלט מובנה",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "יצירת הזמנת משלוח מזון, תומך בהזמנה ממסעדה אחת בלבד, ניתן להזמין מספר מוצרים ממסעדה אחת",
        "preconditions": "בתרחיש משלוח מזון, יש לקבוע מזהה מסעדה ייחודי ומזהה אחד או יותר של מוצרים, לזהות הגבלות תזונתיות של המשתמש ולכלול אותן בהזמנה",
        "postconditions": "מחזיר מידע על ההזמנה, שואל את המשתמש האם לשלם על ההזמנה",
        "args": {
            "user_id": "מזהה משתמש",
            "store_id": "מזהה חנות",
            "food_ids": "רשימת מזהי מוצרים",
            "food_cnts": "רשימת כמויות התואמת למזהי המוצרים",
            "address": "כתובת יעד למשלוח מזון",
            "dispatch_time": "זמן תחילת המשלוח להזמנת מזון (כלומר הזמן שהשליח יוצא מהחנות עם האוכל), פורמט yyyy-mm-dd HH:MM:SS",
            "attributes": "מאפייני מפרט המוצר התואמים למזהה המוצר",
            "note": "הערות להזמנה (אסור לשים בקשות של המשתמש לגבי זמן וכדומה ישירות בהערות), כגון הסבר על הגבלות תזונתיות"
        },
        "returns": "אם היצירה הצליחה, מחזיר מידע על ההזמנה (כולל מזהה הזמנה, מזהה משתמש, מזהה חנות, רשימת מזהי מוצרים, רשימת כמויות מוצרים, כתובת, זמן ביצוע ההזמנה, זמן עדכון, סטטוס הזמנה, רשימת מוצרים, הערות), אחרת מחזיר הודעת מידע רלוונטית",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "בהקשר של משלוחי מזון, כאשר יש מידע על הזמנה בהקשר הקודם, והמשתמש מאשר תשלום או מבצע תשלום חוזר",
        "preconditions": "בהקשר של משלוחי מזון, המשתמש מאשר תשלום, ההזמנה נוצרה והגיעה לשלב התשלום | המשתמש מציין תשלום חוזר",
        "postconditions": "מחזיר מידע על תוצאת התשלום",
        "args": {
            "order_id": "מזהה ההזמנה"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "קבלת סטטוס הזמנה",
        "preconditions": "בדיקת סטטוס הזמנת משלוח",
        "postconditions": "החזרת מידע על סטטוס ההזמנה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "מידע על סטטוס ההזמנה",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "המשתמש מבטל הזמנה, או מבטל תשלום. אסור לבטל הזמנה שנמצאת כבר במצב 'בוטל'.",
        "preconditions": "בדיקת סטטוס הזמנת משלוח מזון, וווידוא שסטטוס ההזמנה אינו 'בוטל'.",
        "postconditions": "החזרת מידע על תוצאת ביטול ההזמנה.",
        "args": {
            "order_id": "מזהה ההזמנה"
        },
        "returns": "מידע על תוצאת ביטול ההזמנה",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "שינוי הערות ההזמנה",
        "preconditions": "מזהה הזמנה יחיד למשלוח חוץ (order_id) זוהה בהקשר הקודם, והמשתמש מעוניין לשנות את הערות ההזמנה",
        "postconditions": "הצגת פרטי ההזמנה לאחר השינוי, אם ההזמנה טרם שולמה יידרש אישור תשלום מהמשתמש",
        "args": {
            "order_id": "מזהה ההזמנה",
            "note": "פרטי הערה חדשים להזמנה"
        },
        "returns": "תוצאת פעולת שינוי הערות ההזמנה",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "שאילתת כל הזמנות משלוחי המזון, מחזירה מידע הכולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה עסק, מחיר כולל, זמן הזמנה, זמן עדכון, סטטוס הזמנה ועוד",
        "preconditions": "הצגת כל הזמנות משלוחי המזון בהתאם לתנאי השאילתא",
        "postconditions": "מחזיר מידע מפורט על כל הזמנות משלוחי המזון העומדות בתנאים",
        "args": {
            "user_id": "מזהה משתמש",
            "status": "סטטוס הזמנה, ברירת מחדל היא לא שולם"
        },
        "returns": "מחזיר מידע מפורט על כל הזמנות משלוחי המזון העומדות בתנאים, כולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה עסק, מחיר כולל, זמן הזמנה, זמן עדכון, סטטוס הזמנה ועוד",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "חקור הזמנת משלוח מזון לפי מזהה הזמנה, החזר מידע מפורט הכולל מזהה הזמנה, סוג הזמנה, מזהה עסק, זמן משלוח, משך משלוח, זמן הגעה, מחיר כולל, זמן ביצוע הזמנה, זמן עדכון, סטטוס הזמנה ורשימת פריטים",
        "preconditions": "ההקשר הקודם קובע מזהה הזמנה יחיד למשלוח מזון",
        "postconditions": "החזר מידע מפורט של ההזמנה שצוינה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "מידע מפורט של ההזמנה שצוינה, כולל מזהה הזמנה, סוג הזמנה, מזהה עסק, זמן משלוח, משך משלוח, זמן הגעה, מחיר כולל, זמן ביצוע הזמנה, זמן עדכון, סטטוס הזמנה ורשימת פריטים",
        "tool_type": "READ"
    },
}

# Tool descriptions - Indonesian version
TOOL_DESCRIPTIONS_ID = {
    "delivery_distance_to_time": {
        "description": "Menghitung waktu pengiriman makanan (menit) berdasarkan jarak (meter)",
        "preconditions": "Menghitung waktu pengiriman makanan berdasarkan jarak dari penjual ke alamat pengguna",
        "postconditions": "Mengembalikan waktu pengiriman (menit)",
        "args": {
            "distance": "Jarak (dalam meter)"
        },
        "returns": "Waktu (dalam menit)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Mengambil informasi toko, termasuk id toko, rating, alamat, garis bujur, garis lintang, tag, daftar produk",
        "preconditions": "Berada dalam skenario pesan antar makanan, perlu mengambil informasi detail toko",
        "postconditions": "Mengembalikan informasi detail toko",
        "args": {
            "store_id": "id toko"
        },
        "returns": "Informasi detail toko",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Mengambil informasi produk, termasuk nama produk, id produk, nama toko, id toko, rating produk, harga produk, dan label produk",
        "preconditions": "Berada dalam skenario pesan antar makanan, perlu memperoleh informasi detail produk",
        "postconditions": "Mengembalikan informasi detail produk",
        "args": {
            "food_id": "id produk"
        },
        "returns": "Informasi detail produk",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Dalam skenario pesan antar makanan, dapat mengekstrak kata kunci yang menggambarkan merchant berdasarkan ungkapan pengguna, serta mencari atau merekomendasikan beberapa merchant.",
        "preconditions": "Berada dalam skenario pesan antar makanan dan mendapatkan kata kunci yang menggambarkan merchant.",
        "postconditions": "Mengembalikan daftar merchant dan memandu pengguna untuk memilih serta menentukan merchant.",
        "args": {
            "keywords": "Kata kunci yang menggambarkan merchant."
        },
        "returns": "Informasi merchant yang dikeluarkan secara terstruktur.",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Dalam skenario pesan antar makanan, dapat mengekstrak kata kunci yang mendeskripsikan produk berdasarkan ungkapan pengguna, mencari atau merekomendasikan beberapa produk",
        "preconditions": "Berada dalam skenario pesan antar makanan, mendapatkan kata kunci yang mendeskripsikan produk",
        "postconditions": "Mengembalikan daftar produk, memandu pengguna untuk memilih produk dan membuat pesanan",
        "args": {
            "keywords": "Kata kunci yang mendeskripsikan produk"
        },
        "returns": "Informasi produk yang dikeluarkan secara terstruktur",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Pembuatan pesanan pesan antar makanan, hanya mendukung pemesanan dari satu toko, satu toko dapat memesan beberapa produk",
        "preconditions": "Berada dalam skenario pesan antar makanan, tentukan satu ID toko yang unik dan satu atau lebih ID produk, tentukan pantangan makanan pengguna, dan mencerminkannya dalam pesanan",
        "postconditions": "Mengembalikan informasi pesanan, menanyakan kepada pengguna apakah akan membayar pesanan",
        "args": {
            "user_id": "ID pengguna",
            "store_id": "ID toko",
            "food_ids": "Daftar ID produk",
            "food_cnts": "Daftar jumlah yang sesuai dengan ID produk",
            "address": "Alamat tujuan pengiriman pesan antar makanan",
            "dispatch_time": "Waktu mulai pengiriman pesanan pesan antar makanan (yaitu waktu kurir berangkat mengambil makanan dari toko), format yyyy-mm-dd HH:MM:SS",
            "attributes": "Atribut spesifikasi produk yang sesuai dengan ID produk",
            "note": "Catatan pesanan (dilarang menempatkan permintaan pengguna mengenai waktu dll. secara langsung dalam catatan), seperti penjelasan informasi pantangan makanan"
        },
        "returns": "Jika pembuatan berhasil, kembalikan informasi pesanan (termasuk ID pesanan, ID pengguna, ID toko, daftar ID produk, daftar jumlah produk, alamat, waktu pemesanan, waktu pembaruan, status pesanan, daftar produk, catatan), jika tidak kembalikan informasi pemberitahuan yang relevan",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Dalam skenario pesan antar makanan, terdapat informasi pesanan dalam konteks sebelumnya, pengguna menyatakan konfirmasi pembayaran, atau pembayaran ulang",
        "preconditions": "Berada dalam skenario pesan antar makanan, pengguna menyatakan konfirmasi pembayaran, pesanan telah dibuat dan masuk ke tahap pembayaran｜pengguna menyatakan pembayaran ulang",
        "postconditions": "Mengembalikan informasi hasil pembayaran",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Mengambil status pesanan",
        "preconditions": "Memeriksa status pesanan pengiriman makanan",
        "postconditions": "Mengembalikan informasi status pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Informasi status pesanan",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Pengguna membatalkan pesanan atau pembayaran. Dilarang membatalkan pesanan yang sudah berstatus dibatalkan.",
        "preconditions": "Periksa status pesanan makanan, pastikan status pesanan tidak dibatalkan",
        "postconditions": "Mengembalikan informasi hasil pembatalan pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Informasi hasil pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Mengubah informasi catatan pesanan",
        "preconditions": "order_id pesan antar makanan yang unik telah ditentukan di konteks sebelumnya, pengguna perlu mengubah catatan pesanan pesan antar makanan",
        "postconditions": "Keluarkan informasi pesanan setelah diubah, jika pesanan belum dibayar maka pengguna perlu mengkonfirmasi pembayaran",
        "args": {
            "order_id": "id pesanan",
            "note": "informasi catatan pesanan baru"
        },
        "returns": "Hasil operasi mengubah catatan pesanan",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Query semua pesanan delivery makanan, mengembalikan informasi yang mencakup ID pesanan, jenis pesanan, ID pengguna, ID merchant, total harga, waktu pemesanan, waktu pembaruan, status pesanan, dan informasi lainnya",
        "preconditions": "Melihat semua pesanan delivery makanan sesuai kondisi query",
        "postconditions": "Mengembalikan informasi rinci semua pesanan delivery makanan yang memenuhi kondisi",
        "args": {
            "user_id": "ID Pengguna",
            "status": "Status pesanan, default adalah belum dibayar"
        },
        "returns": "Mengembalikan informasi rinci semua pesanan delivery makanan yang memenuhi kondisi, termasuk ID pesanan, jenis pesanan, ID pengguna, ID merchant, total harga, waktu pemesanan, waktu pembaruan, status pesanan, dan informasi lainnya",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Cari pesanan antar makanan berdasarkan ID pesanan, kembalikan informasi terperinci yang mencakup ID pesanan, jenis pesanan, ID penjual, waktu pengiriman, durasi pengiriman, waktu tiba, total harga, waktu pemesanan, waktu pembaruan, status pesanan, dan daftar produk",
        "preconditions": "Konteks sebelumnya telah menentukan satu order_id pesanan antar makanan yang unik",
        "postconditions": "Kembalikan informasi terperinci pesanan yang ditentukan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Informasi terperinci pesanan yang ditentukan, termasuk ID pesanan, jenis pesanan, ID penjual, waktu pengiriman, durasi pengiriman, waktu tiba, total harga, waktu pemesanan, waktu pembaruan, status pesanan, dan daftar produk",
        "tool_type": "READ"
    },
}

# Tool descriptions - Korean version
TOOL_DESCRIPTIONS_KO = {
    "delivery_distance_to_time": {
        "description": "거리 (미터) 를 기준으로 배달 시간 (분) 을 계산합니다.",
        "preconditions": "가게에서 사용자 주소까지의 거리에 따라 배달 시간을 계산합니다.",
        "postconditions": "배달 시간 (분) 을 반환합니다.",
        "args": {
            "distance": "거리 (미터 단위)"
        },
        "returns": "시간 (분 단위)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "가게 정보를 가져옵니다. 가게 id, 평점, 주소, 경도, 위도, 태그, 상품 목록을 포함합니다.",
        "preconditions": "배달 주문 상황이며 가게의 상세 정보를 가져와야 합니다.",
        "postconditions": "가게의 상세 정보를 반환합니다.",
        "args": {
            "store_id": "가게 id"
        },
        "returns": "가게의 상세 정보",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "상품 정보를 조회하며, 상품명, 상품 ID, 가게 이름, 가게 ID, 상품 평점, 상품 가격, 상품 태그를 포함합니다.",
        "preconditions": "배달 주문 상황에서 상품의 상세 정보가 필요할 때",
        "postconditions": "상품의 상세 정보를 반환합니다.",
        "args": {
            "food_id": "상품 ID"
        },
        "returns": "상품의 상세 정보",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "배달 주문 상황에서 사용자의 발화를 기반으로 가게를 설명하는 키워드를 추출하여 여러 가게를 검색하거나 추천합니다.",
        "preconditions": "배달 주문 상황이어야 하며, 가게를 설명하는 키워드를 확보합니다.",
        "postconditions": "가게 목록을 반환하고 사용자가 가게를 선택하여 확정하도록 안내합니다.",
        "args": {
            "keywords": "가게를 설명하는 키워드"
        },
        "returns": "구조화된 가게 정보",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "배달 주문 상황에서 사용자의 발화를 기반으로 상품을 설명하는 키워드를 추출하여 여러 상품을 검색하거나 추천합니다.",
        "preconditions": "배달 주문 상황이며, 상품을 설명하는 키워드를 획득합니다.",
        "postconditions": "상품 목록을 반환하고, 사용자가 상품을 선택하여 주문을 생성하도록 안내합니다.",
        "args": {
            "keywords": "상품을 설명하는 키워드"
        },
        "returns": "구조화된 상품 정보",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "배달 주문 생성, 단일 가게 주문만 지원하며 한 가게에서 여러 상품을 주문할 수 있습니다.",
        "preconditions": "배달 주문 상황이어야 하며, 고유한 가게 ID 와 하나 이상의 상품 ID 를 확인하고, 사용자의 식이 제한 사항을 확인하여 주문 내용에 반영해야 합니다.",
        "postconditions": "주문 정보를 반환하고 사용자에게 주문 결제를 진행할지 묻습니다.",
        "args": {
            "user_id": "사용자 ID",
            "store_id": "가게 ID",
            "food_ids": "상품 ID 목록",
            "food_cnts": "상품 ID 에 해당하는 수량 목록",
            "address": "배달 목표 주소",
            "dispatch_time": "배달 주문 배송 시작 시간 (즉, 배달 기사가 가게에서 음식을 픽업하여 출발하는 시간), 형식: yyyy-mm-dd HH:MM:SS",
            "attributes": "상품 ID 에 해당하는 상품 규격 속성",
            "note": "주문 비고 (사용자의 시간 관련 요구사항 등을 비고에 직접 기재 금지), 예: 식이 제한 사항 설명"
        },
        "returns": "생성에 성공하면 주문 정보 (주문 ID, 사용자 ID, 가게 ID, 상품 ID 목록, 상품 수량 목록, 주소, 주문 시간, 업데이트 시간, 주문 상태, 상품 목록, 비고 포함) 를 반환하고, 실패 시 관련 안내 메시지를 반환합니다.",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "배달 주문 상황에서 이전 문맥에 주문 정보가 있고, 사용자가 결제 확인 또는 재결제를 표현할 때",
        "preconditions": "배달 주문 상황, 사용자 결제 확인 표현 및 주문 생성 완료 후 결제 단계 진입 | 사용자 재결제 표시",
        "postconditions": "결제 결과 정보 반환",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "주문 상태 조회",
        "preconditions": "배달 주문 상태 조회",
        "postconditions": "주문 상태 정보 반환",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 상태 정보",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "사용자가 주문을 취소하거나 결제를 취소합니다. 이미 취소된 상태의 주문은 다시 취소할 수 없습니다.",
        "preconditions": "배달 주문 상태를 조회하여 주문 상태가 취소되지 않았는지 확인합니다.",
        "postconditions": "주문 취소 결과 정보를 반환합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 취소 결과 정보",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "주문 비고 정보 수정",
        "preconditions": "문맥상 유일한 배달 order_id 가 확인되었으며, 사용자가 배달 주문 비고를 수정해야 함",
        "postconditions": "수정된 주문 정보 출력, 주문이 아직 결제되지 않았다면 사용자에게 결제 확인 필요",
        "args": {
            "order_id": "주문 id",
            "note": "새로운 주문 비고 정보"
        },
        "returns": "주문 비고 수정 작업의 결과",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "모든 배달 주문을 조회하며, 주문 ID, 주문 유형, 사용자 ID, 업체 ID, 총액, 주문 시간, 업데이트 시간, 주문 상태 등의 정보를 반환합니다.",
        "preconditions": "조회 조건에 따라 모든 배달 주문을 확인합니다.",
        "postconditions": "조건에 맞는 모든 배달 주문의 상세 정보를 반환합니다.",
        "args": {
            "user_id": "사용자 ID",
            "status": "주문 상태, 기본값은 미결제"
        },
        "returns": "조건에 맞는 모든 배달 주문의 상세 정보를 반환하며, 주문 ID, 주문 유형, 사용자 ID, 업체 ID, 총액, 주문 시간, 업데이트 시간, 주문 상태 등의 정보를 포함합니다.",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "주문 ID 를 기반으로 배달 주문을 조회하며, 주문 ID, 주문 유형, 가게 ID, 배달 시간, 배달 소요 시간, 도착 시간, 총 금액, 주문 시간, 업데이트 시간, 주문 상태 및 상품 목록 등 상세 정보를 반환합니다.",
        "preconditions": "상기 내용에서 유일한 배달 order_id 가 확인되어야 합니다.",
        "postconditions": "지정된 주문의 상세 정보를 반환합니다.",
        "args": {
            "order_id": "주문 id"
        },
        "returns": "지정된 주문의 상세 정보이며, 주문 ID, 주문 유형, 가게 ID, 배달 시간, 배달 소요 시간, 도착 시간, 총 금액, 주문 시간, 업데이트 시간, 주문 상태 및 상품 목록을 포함합니다.",
        "tool_type": "READ"
    },
}

# Tool descriptions - Spanish version
TOOL_DESCRIPTIONS_ES = {
    "delivery_distance_to_time": {
        "description": "Calcula el tiempo de entrega de comida a domicilio (minutos) según la distancia (metros)",
        "preconditions": "Calcula el tiempo de entrega de comida a domicilio según la distancia desde el comerciante hasta la dirección del usuario",
        "postconditions": "Devuelve el tiempo de entrega (minutos)",
        "args": {
            "distance": "Distancia (en metros)"
        },
        "returns": "Tiempo (en minutos)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Obtener información de la tienda, incluyendo ID de la tienda, valoración, dirección, longitud, latitud, etiquetas y lista de productos",
        "preconditions": "En un escenario de pedido de comida a domicilio, se necesita obtener la información detallada de la tienda",
        "postconditions": "Devuelve la información detallada de la tienda",
        "args": {
            "store_id": "ID de la tienda"
        },
        "returns": "Información detallada de la tienda",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Obtener información del producto, incluyendo nombre del producto, id del producto, nombre de la tienda, id de la tienda, puntuación del producto, precio del producto, etiquetas del producto",
        "preconditions": "En el escenario de entrega de comida, se necesita obtener la información detallada del producto",
        "postconditions": "Devolver la información detallada del producto",
        "args": {
            "food_id": "id del producto"
        },
        "returns": "Información detallada del producto",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "En el contexto de pedidos a domicilio, se pueden extraer palabras clave que describen al comerciante basándose en la expresión del usuario para buscar o recomendar múltiples comerciantes.",
        "preconditions": "Estar en el contexto de pedidos a domicilio y obtener palabras clave que describan al comerciante.",
        "postconditions": "Devolver una lista de comerciantes y guiar al usuario para seleccionar y confirmar el comerciante.",
        "args": {
            "keywords": "Palabras clave que describen al comerciante."
        },
        "returns": "Información del comerciante con salida estructurada.",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "En el contexto de entrega de comida, permite extraer palabras clave descriptivas de los productos a partir de la expresión del usuario, para buscar o recomendar múltiples artículos.",
        "preconditions": "Estar en el contexto de entrega de comida y obtener palabras clave que describan los productos.",
        "postconditions": "Devolver una lista de productos, guiar al usuario para seleccionar un producto y crear un pedido.",
        "args": {
            "keywords": "Palabras clave descriptivas de los productos."
        },
        "returns": "Información de productos con formato estructurado.",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Creación de pedido de entrega de comida, solo se admite realizar pedidos a un único comerciante, un único comerciante puede incluir múltiples productos en el pedido",
        "preconditions": "En el contexto de entrega de comida, determinar un único ID de tienda y uno o más IDs de productos, identificar las restricciones dietéticas del usuario y reflejarlas en el pedido",
        "postconditions": "Devolver la información del pedido y preguntar al usuario si desea pagar el pedido",
        "args": {
            "user_id": "ID de usuario",
            "store_id": "ID de tienda",
            "food_ids": "Lista de IDs de productos",
            "food_cnts": "Lista de cantidades correspondientes a los IDs de productos",
            "address": "Dirección objetivo de entrega",
            "dispatch_time": "Hora de inicio de entrega del pedido (es decir, la hora en que el repartidor recoge la comida del comerciante y sale), formato yyyy-mm-dd HH:MM:SS",
            "attributes": "Atributos de especificación del producto correspondientes al ID del producto",
            "note": "Nota del pedido (prohibido incluir directamente solicitudes del usuario sobre el tiempo, etc., en la nota), como explicación de restricciones dietéticas"
        },
        "returns": "Si la creación es exitosa, devolver la información del pedido (incluye ID del pedido, ID de usuario, ID de tienda, lista de IDs de productos, lista de cantidades de productos, dirección, hora de realización del pedido, hora de actualización, estado del pedido, lista de productos, nota), de lo contrario devolver mensajes de información relevantes",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "En el escenario de entrega de comida, con información del pedido en el contexto anterior, el usuario expresa confirmar el pago o volver a pagar",
        "preconditions": "En el escenario de entrega de comida, el usuario expresa confirmar el pago, el pedido está creado y en la etapa de pago | el usuario indica volver a pagar",
        "postconditions": "Devuelve información del resultado del pago",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del resultado del pago",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Obtener el estado del pedido",
        "preconditions": "Consultar el estado del pedido de comida a domicilio",
        "postconditions": "Devolver información del estado del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del estado del pedido",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "El usuario cancela el pedido o el pago. No se permite cancelar nuevamente un pedido que ya esté cancelado.",
        "preconditions": "Consultar el estado del pedido de comida a domicilio y asegurarse de que el estado del pedido no esté cancelado.",
        "postconditions": "Devolver la información del resultado de la cancelación del pedido.",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del resultado de la cancelación del pedido.",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Modificar la información de la nota del pedido",
        "preconditions": "El contexto anterior determina un order_id único de pedido a domicilio, y el usuario necesita modificar la nota del pedido a domicilio",
        "postconditions": "Mostrar la información del pedido modificada. Si el pedido aún no ha sido pagado, se requiere que el usuario confirme el pago",
        "args": {
            "order_id": "ID del pedido",
            "note": "Nueva información de la nota del pedido"
        },
        "returns": "Resultado de la operación de modificación de la nota del pedido",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Consulta todos los pedidos de comida a domicilio y devuelve información que incluye ID del pedido, tipo de pedido, ID de usuario, ID del comerciante, precio total, hora del pedido, hora de actualización, estado del pedido, etc.",
        "preconditions": "Ver todos los pedidos de comida a domicilio según las condiciones de consulta",
        "postconditions": "Devuelve la información detallada de todos los pedidos de comida a domicilio que cumplan las condiciones",
        "args": {
            "user_id": "ID de usuario",
            "status": "Estado del pedido, por defecto no pagado"
        },
        "returns": "Devuelve la información detallada de todos los pedidos de comida a domicilio que cumplan las condiciones, incluyendo ID del pedido, tipo de pedido, ID de usuario, ID del comerciante, precio total, hora del pedido, hora de actualización, estado del pedido, etc.",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Consulta un pedido de entrega de comida según el ID del pedido, devuelve información detallada que incluye ID del pedido, tipo de pedido, ID del comerciante, tiempo de entrega, duración de la entrega, hora de llegada, precio total, hora del pedido, hora de actualización, estado del pedido y lista de productos",
        "preconditions": "El contexto anterior determina un único order_id de entrega de comida",
        "postconditions": "Devuelve la información detallada del pedido especificado",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información detallada del pedido especificado, incluyendo ID del pedido, tipo de pedido, ID del comerciante, tiempo de entrega, duración de la entrega, hora de llegada, precio total, hora del pedido, hora de actualización, estado del pedido y lista de productos",
        "tool_type": "READ"
    },
}

# Tool descriptions - Thai version
TOOL_DESCRIPTIONS_TH = {
    "delivery_distance_to_time": {
        "description": "คำนวณเวลาจัดส่งอาหารเดลิเวอรี่ (นาที) ตามระยะทาง (เมตร)",
        "preconditions": "คำนวณเวลาจัดส่งอาหารเดลิเวอรี่ตามระยะทางจากร้านค้าไปยังที่อยู่ของผู้ใช้",
        "postconditions": "ส่งคืนเวลาจัดส่ง (นาที)",
        "args": {
            "distance": "ระยะทาง (หน่วยเป็นเมตร)"
        },
        "returns": "เวลา (หน่วยเป็นนาที)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "รับข้อมูลร้านค้า รวมถึงรหัสร้านค้า คะแนน ที่อยู่ ละติจูด ลองจิจูด แท็ก และรายการสินค้า",
        "preconditions": "อยู่ในบริบทของการสั่งอาหารเดลิเวอรี่ และต้องการรับข้อมูลรายละเอียดของร้านค้า",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของร้านค้า",
        "args": {
            "store_id": "รหัสร้านค้า"
        },
        "returns": "ข้อมูลรายละเอียดของร้านค้า",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "ดึงข้อมูลสินค้า รวมถึงชื่อสินค้า, รหัสสินค้า, ชื่อร้านค้า, รหัสร้านค้า, คะแนนประเมินสินค้า, ราคาสินค้า, แท็กสินค้า",
        "preconditions": "อยู่ในบริบทการสั่งอาหารเดลิเวอรี่ และต้องการดึงข้อมูลรายละเอียดของสินค้า",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของสินค้า",
        "args": {
            "food_id": "รหัสสินค้า"
        },
        "returns": "ข้อมูลรายละเอียดของสินค้า",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "ในสถานการณ์การสั่งอาหารจัดส่ง สามารถดึงคำสำคัญที่อธิบายร้านค้าออกมาจากการแสดงออกของผู้ใช้ เพื่อค้นหาหรือแนะนำร้านค้าหลายแห่ง",
        "preconditions": "อยู่ในสถานการณ์การสั่งอาหารจัดส่ง และได้รับคำสำคัญที่อธิบายร้านค้า",
        "postconditions": "ส่งคืนรายการร้านค้า และแนะนำผู้ใช้ให้เลือกและยืนยันร้านค้า",
        "args": {
            "keywords": "คำสำคัญที่อธิบายร้านค้า"
        },
        "returns": "ข้อมูลร้านค้าที่ส่งออกในรูปแบบโครงสร้าง",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "ในบริบทของการสั่งอาหารจัดส่ง สามารถสกัดคำหลักที่บรรยายสินค้าจากสิ่งที่ผู้ใช้สื่อสารได้ เพื่อค้นหาหรือแนะนำสินค้าหลายรายการ",
        "preconditions": "อยู่ในบริบทของการสั่งอาหารจัดส่ง และได้รับคำหลักที่บรรยายสินค้า",
        "postconditions": "ส่งคืนรายการสินค้า นำทางผู้ใช้ให้เลือกสินค้าและสร้างคำสั่งซื้อ",
        "args": {
            "keywords": "คำหลักที่บรรยายสินค้า"
        },
        "returns": "ข้อมูลสินค้าที่ส่งออกในรูปแบบโครงสร้าง",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "สร้างคำสั่งซื้ออาหารเดลิเวอรี่ รองรับเฉพาะการสั่งซื้อจากร้านค้าเดียว แต่สามารถสั่งสินค้าหลายรายการจากร้านค้านั้นได้",
        "preconditions": "อยู่ในสถานการณ์อาหารเดลิเวอรี่ ระบุรหัสร้านค้าหนึ่งแห่งและรหัสสินค้าหนึ่งรายการหรือมากกว่า ระบุข้อจำกัดด้านอาหารของผู้ใช้ และรวมไว้ในคำสั่งซื้อ",
        "postconditions": "คืนข้อมูลคำสั่งซื้อ และถามผู้ใช้ว่าต้องการชำระเงินสำหรับคำสั่งซื้อหรือไม่",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "store_id": "รหัสร้านค้า",
            "food_ids": "รายการรหัสสินค้า",
            "food_cnts": "รายการจำนวนที่สอดคล้องกับรหัสสินค้า",
            "address": "ที่อยู่เป้าหมายสำหรับการจัดส่งอาหารเดลิเวอรี่",
            "dispatch_time": "เวลาเริ่มจัดส่งสำหรับคำสั่งซื้ออาหารเดลิเวอรี่ (หมายถึงเวลาที่ไรเดอร์ออกจากร้านค้าเพื่อรับอาหาร) รูปแบบคือ yyyy-mm-dd HH:MM:SS",
            "attributes": "คุณลักษณะเฉพาะของสินค้าที่สอดคล้องกับรหัสสินค้า",
            "note": "หมายเหตุคำสั่งซื้อ (ห้ามใส่ความต้องการเกี่ยวกับเวลา ฯลฯ ของผู้ใช้โดยตรงในหมายเหตุ) เช่น คำอธิบายข้อมูลข้อจำกัดด้านอาหาร"
        },
        "returns": "หากสร้างสำเร็จ จะคืนข้อมูลคำสั่งซื้อ (ประกอบด้วยรหัสคำสั่งซื้อ, รหัสผู้ใช้, รหัสร้านค้า, รายการรหัสสินค้า, รายการจำนวนสินค้า, ที่อยู่, เวลาสั่งซื้อ, เวลาอัปเดต, สถานะคำสั่งซื้อ, รายการสินค้า, หมายเหตุ) มิฉะนั้นจะคืนข้อความข้อมูลที่เกี่ยวข้อง",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "ในบริบทการจัดส่งอาหาร เมื่อมีข้อมูลคำสั่งซื้อในบริบทก่อนหน้า ผู้ใช้ยืนยันการชำระเงิน หรือต้องการชำระเงินใหม่",
        "preconditions": "อยู่ในบริบทการจัดส่งอาหาร, ผู้ใช้ยืนยันการชำระเงิน, คำสั่งซื้อถูกสร้างเสร็จสมบูรณ์และเข้าสู่ขั้นตอนการชำระเงิน | หรือผู้ใช้ต้องการชำระเงินใหม่",
        "postconditions": "คืนข้อมูลผลการชำระเงิน",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "รับสถานะคำสั่งซื้อ",
        "preconditions": "ตรวจสอบสถานะคำสั่งซื้ออาหารเดลิเวอรี่",
        "postconditions": "ส่งคืนข้อมูลสถานะคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลสถานะคำสั่งซื้อ",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งซื้อ หรือผู้ใช้ยกเลิกการชำระเงิน ห้ามทำการยกเลิกคำสั่งซื้อที่อยู่ในสถานะถูกยกเลิกไปแล้ว",
        "preconditions": "ตรวจสอบสถานะคำสั่งซื้ออาหาร และให้แน่ใจว่าสถานะคำสั่งซื้อไม่ใช่ cancelled",
        "postconditions": "ส่งกลับข้อมูลผลลัพธ์การยกเลิกคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลลัพธ์การยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "แก้ไขข้อมูลหมายเหตุคำสั่งซื้อ",
        "preconditions": "บทสนทนาก่อนหน้าระบุ order_id สำหรับการจัดส่งอาหารเพียงหนึ่งเดียว และผู้ใช้ต้องการแก้ไขหมายเหตุคำสั่งซื้อจัดส่งอาหาร",
        "postconditions": "แสดงข้อมูลคำสั่งซื้อหลังแก้ไข หากคำสั่งซื้อยังไม่ได้ชำระเงิน ผู้ใช้ต้องยืนยันการชำระเงิน",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "note": "ข้อมูลหมายเหตุคำสั่งซื้อใหม่"
        },
        "returns": "ผลลัพธ์ของการดำเนินการแก้ไขหมายเหตุคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "ค้นหาออเดอร์จัดส่งอาหารทั้งหมด ส่งกลับข้อมูลที่ประกอบด้วยรหัสออเดอร์ ประเภทออเดอร์ รหัสผู้ใช้ รหัสร้านค้า ราคารวม เวลาที่สั่ง เวลาอัปเดต สถานะออเดอร์ และอื่นๆ",
        "preconditions": "ดูออเดอร์จัดส่งอาหารทั้งหมดตามเงื่อนไขการค้นหา",
        "postconditions": "ส่งกลับข้อมูลโดยละเอียดของออเดอร์จัดส่งอาหารทั้งหมดที่ตรงตามเงื่อนไข",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "status": "สถานะออเดอร์, ค่าเริ่มต้นคือยังไม่ชำระเงิน"
        },
        "returns": "ส่งกลับข้อมูลโดยละเอียดของออเดอร์จัดส่งอาหารทั้งหมดที่ตรงตามเงื่อนไข รวมถึงรหัสออเดอร์ ประเภทออเดอร์ รหัสผู้ใช้ รหัสร้านค้า ราคารวม เวลาที่สั่ง เวลาอัปเดต สถานะออเดอร์ และอื่นๆ",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ค้นหาออเดอร์จัดส่งอาหารตาม ID ออเดอร์ โดยส่งกลับข้อมูลรายละเอียดที่รวมถึง ID ออเดอร์, ประเภทออเดอร์, ID ร้านค้า, เวลาจัดส่ง, ระยะเวลาจัดส่ง, เวลาถึง, ราคารวม, เวลาสั่งซื้อ, เวลาอัปเดต, สถานะออเดอร์ และรายการสินค้า",
        "preconditions": "บริบทก่อนหน้านี้ระบุ order_id อาหารเพียงหนึ่งเดียว",
        "postconditions": "ส่งกลับข้อมูลรายละเอียดของออเดอร์ที่ระบุ",
        "args": {
            "order_id": "ID ออเดอร์"
        },
        "returns": "ข้อมูลรายละเอียดของออเดอร์ที่ระบุ รวมถึง ID ออเดอร์, ประเภทออเดอร์, ID ร้านค้า, เวลาจัดส่ง, ระยะเวลาจัดส่ง, เวลาถึง, ราคารวม, เวลาสั่งซื้อ, เวลาอัปเดต, สถานะออเดอร์ และรายการสินค้า",
        "tool_type": "READ"
    },
}

# Tool descriptions - Hindi version
TOOL_DESCRIPTIONS_HI = {
    "delivery_distance_to_time": {
        "description": "दूरी (मीटर) के आधार पर खाद्य वितरण समय (मिनट) की गणना करें",
        "preconditions": "विक्रेता से उपयोगकर्ता के पते तक की दूरी के आधार पर खाद्य वितरण समय की गणना करें",
        "postconditions": "वितरण समय (मिनट) लौटाएं",
        "args": {
            "distance": "दूरी (मीटर में)"
        },
        "returns": "समय (मिनटों में)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "विक्रेता की जानकारी प्राप्त करें, जिसमें विक्रेता आईडी, रेटिंग, पता, देशांतर, अक्षांश, टैग और उत्पाद सूची शामिल है।",
        "preconditions": "फूड डिलीवरी परिदृश्य में, विक्रेता की विस्तृत जानकारी प्राप्त करने की आवश्यक है।",
        "postconditions": "विक्रेता की विस्तृत जानकारी लौटाएं।",
        "args": {
            "store_id": "विक्रेता आईडी"
        },
        "returns": "विक्रेता की विस्तृत जानकारी",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "उत्पाद की जानकारी प्राप्त करें, जिसमें उत्पाद का नाम, उत्पाद आईडी, स्टोर का नाम, स्टोर आईडी, उत्पाद रेटिंग, उत्पाद की कीमत, उत्पाद टैग शामिल हैं।",
        "preconditions": "फूड डिलीवरी परिदृश्य में, उत्पाद की विस्तृत जानकारी प्राप्त करने की आवश्यकता है।",
        "postconditions": "उत्पाद की विस्तृत जानकारी लौटाएं।",
        "args": {
            "food_id": "उत्पाद आईडी"
        },
        "returns": "उत्पाद की विस्तृत जानकारी",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "फूड डिलीवरी परिदृश्य में, उपयोगकर्ता की अभिव्यक्ति के आधार पर व्यापारी का वर्णन करने वाले कीवर्ड निकालकर कई व्यापारियों को खोजा या अनुशंसा की जा सकती है",
        "preconditions": "फूड डिलीवरी परिदृश्य में होना, व्यापारी का वर्णन करने वाले कीवर्ड प्राप्त करना",
        "postconditions": "व्यापारी की सूची लौटाएं, उपयोगकर्ता को व्यापारी चुनने और पुष्टि करने के लिए मार्गदर्शन करें",
        "args": {
            "keywords": "व्यापारी का वर्णन करने वाले कीवर्ड"
        },
        "returns": "व्यापारी जानकारी का संरचित आउटपुट",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "फूड डिलीवरी परिदृश्य में, उपयोगकर्ता की अभिव्यक्ति के आधार पर उत्पादों का वर्णन करने वाले कीवर्ड निकाले जा सकते हैं ताकि कई उत्पादों को खोजा या अनुशंसित किया जा सके।",
        "preconditions": "फूड डिलीवरी परिदृश्य में होना, उत्पादों का वर्णन करने वाले कीवर्ड प्राप्त करना।",
        "postconditions": "उत्पादों की सूची लौटाएं, उपयोगकर्ता को उत्पाद चुनने और ऑर्डर बनाने के लिए निर्देशित करें।",
        "args": {
            "keywords": "उत्पादों का वर्णन करने वाले कीवर्ड"
        },
        "returns": "संरचित आउटपुट के रूप में उत्पाद जानकारी",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "फूड डिलीवरी ऑर्डर बनाना, केवल एक ही स्टोर से ऑर्डर करने का समर्थन करता है, एक स्टोर से कई आइटम ऑर्डर किए जा सकते हैं",
        "preconditions": "फूड डिलीवरी परिदृश्य में होना, एक अद्वितीय स्टोर आईडी और एक या अधिक आइटम आईडी निर्धारित करें, उपयोगकर्ता की आहार संबंधी प्रतिबंधों की पुष्टि करें, और इसे ऑर्डर में प्रतिबिंबित करें",
        "postconditions": "ऑर्डर जानकारी वापस करें, उपयोगकर्ता से पूछें कि क्या वे ऑर्डर का भुगतान करना चाहते हैं",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "store_id": "स्टोर आईडी",
            "food_ids": "आइटम आईडी की सूची",
            "food_cnts": "आइटम आईडी के अनुरूप मात्रा की सूची",
            "address": "फूड डिलीवरी लक्ष्य पता",
            "dispatch_time": "फूड डिलीवरी ऑर्डर डिलीवरी शुरू होने का समय (यानी राइडर द्वारा स्टोर से भोजन लेने और प्रस्थान करने का समय), प्रारूप yyyy-mm-dd HH:MM:SS",
            "attributes": "आइटम आईडी के अनुरूप आइटम विनिर्देश गुण",
            "note": "ऑर्डर नोट्स (समय आदि के बारे में उपयोगकर्ता की आवश्यकताओं को सीधे नोट्स में रखने की अनुमति नहीं है), जैसे आहार संबंधी प्रतिबंध जानकारी विवरण"
        },
        "returns": "यदि सफलतापूर्वक बनाया गया, तो ऑर्डर जानकारी वापस करें (जिसमें ऑर्डर आईडी, उपयोगकर्ता आईडी, स्टोर आईडी, आइटम आईडी की सूची, आइटम मात्रा की सूची, पता, ऑर्डर करने का समय, अद्यतन समय, ऑर्डर स्थिति, आइटम सूची, नोट्स शामिल हैं), अन्यथा संबंधित सूचना संदेश वापस करें",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "फूड डिलीवरी परिदृश्य में, संदर्भ में ऑर्डर जानकारी है, उपयोगकर्ता भुगतान की पुष्टि करता है, या पुनः भुगतान करता है",
        "preconditions": "फूड डिलीवरी परिदृश्य में, उपयोगकर्ता भुगतान की पुष्टि करता है, ऑर्डर बनाया गया है और भुगतान चरण में है｜उपयोगकर्ता पुनः भुगतान का संकेत देता है",
        "postconditions": "भुगतान परिणाम जानकारी लौटाएं",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "ऑर्डर की स्थिति प्राप्त करें",
        "preconditions": "फूड डिलीवरी ऑर्डर की स्थिति जांचें",
        "postconditions": "ऑर्डर स्थिति जानकारी वापस करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर स्थिति जानकारी",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "उपयोगकर्ता ऑर्डर रद्द करता है, या उपयोगकर्ता भुगतान रद्द करता है। पहले से रद्द स्थिति में वाले ऑर्डर को फिर से रद्द करना निषिद्ध है।",
        "preconditions": "फूड डिलीवरी ऑर्डर की स्थिति जांचें, सुनिश्चित करें कि ऑर्डर की स्थिति रद्द न हो।",
        "postconditions": "ऑर्डर रद्द करने के परिणाम की जानकारी लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर रद्द करने के परिणाम की जानकारी",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "ऑर्डर टिप्पणी जानकारी संशोधित करें",
        "preconditions": "पिछले संदर्भ में एक अद्वितीय फूड डिलीवरी order_id निर्धारित है, उपयोगकर्ता को फूड डिलीवरी ऑर्डर टिप्पणी संशोधित करने की आवश्यकता है",
        "postconditions": "संशोधित ऑर्डर जानकारी आउटपुट करें, यदि ऑर्डर का भुगतान अभी तक नहीं हुआ है तो उपयोगकर्ता को भुगतान की पुष्टि करने की आवश्यकता है",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "note": "नई ऑर्डर टिप्पणी जानकारी"
        },
        "returns": "ऑर्डर टिप्पणी संशोधित करने की कार्रवाई का परिणाम",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "सभी फूड डिलीवरी ऑर्डर क्वेरी करें, और ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, विक्रेता आईडी, कुल मूल्य, ऑर्डर करने का समय, अपडेट समय, ऑर्डर स्थिति आदि जानकारी लौटाएं।",
        "preconditions": "क्वेरी शर्तों के अनुसार सभी फूड डिलीवरी ऑर्डर देखें।",
        "postconditions": "शर्तों से मेल खाने वाले सभी फूड डिलीवरी ऑर्डर की विस्तृत जानकारी लौटाएं।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "status": "ऑर्डर स्थिति, डिफ़ॉल्ट रूप से भुगतान नहीं किया गया"
        },
        "returns": "शर्तों से मेल खाने वाले सभी फूड डिलीवरी ऑर्डर की विस्तृत जानकारी लौटाएं, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, विक्रेता आईडी, कुल मूल्य, ऑर्डर करने का समय, अपडेट समय, ऑर्डर स्थिति आदि शामिल हैं।",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "ऑर्डर आईडी के आधार पर फूड डिलीवरी ऑर्डर क्वेरी करें, ऑर्डर आईडी, ऑर्डर प्रकार, विक्रेता आईडी, डिलीवरी समय, डिलीवरी अवधि, पहुंचने का समय, कुल कीमत, ऑर्डर समय, अपडेट समय, ऑर्डर स्थिति और आइटम सूची सहित विस्तृत जानकारी वापस करें",
        "preconditions": "पिछले संदर्भ में एक अद्वितीय फूड डिलीवरी ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "निर्दिष्ट ऑर्डर की विस्तृत जानकारी वापस करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "निर्दिष्ट ऑर्डर की विस्तृत जानकारी, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, विक्रेता आईडी, डिलीवरी समय, डिलीवरी अवधि, पहुंचने का समय, कुल कीमत, ऑर्डर समय, अपडेट समय, ऑर्डर स्थिति और आइटम सूची शामिल है",
        "tool_type": "READ"
    },
}

# Tool descriptions - Arabic version
TOOL_DESCRIPTIONS_AR = {
    "delivery_distance_to_time": {
        "description": "حساب وقت توصيل الطعام (بالدقائق) بناءً على المسافة (بالأمتار)",
        "preconditions": "حساب وقت توصيل الطعام بناءً على المسافة من المتجر إلى عنوان المستخدم",
        "postconditions": "إرجاع وقت التوصيل (بالدقائق)",
        "args": {
            "distance": "المسافة (بالأمتار)"
        },
        "returns": "الوقت (بالدقائق)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "الحصول على معلومات المتجر، بما في ذلك معرف المتجر، والتقييم، والعنوان، وخط الطول، وخط العرض، والعلامات، وقائمة المنتجات",
        "preconditions": "في سياق توصيل الطعام، هناك حاجة للحصول على المعلومات التفصيلية للمتجر",
        "postconditions": "إرجاع المعلومات التفصيلية للمتجر",
        "args": {
            "store_id": "معرف المتجر"
        },
        "returns": "المعلومات التفصيلية للمتجر",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "الحصول على معلومات المنتج، بما في ذلك اسم المنتج، ومعرف المنتج، واسم المتجر، ومعرف المتجر، وتقييم المنتج، وسعر المنتج، ووسوم المنتج",
        "preconditions": "في سياق توصيل الطعام، عند الحاجة إلى الحصول على معلومات مفصلة عن المنتج",
        "postconditions": "إرجاع التفاصيل المفصلة للمنتج",
        "args": {
            "food_id": "معرف المنتج"
        },
        "returns": "التفاصيل المفصلة للمنتج",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "في سياق توصيل الطعام، يمكن استخراج الكلمات الرئيسية التي تصف المتاجر بناءً على تعبير المستخدم للبحث عن أو توصية عدة متاجر",
        "preconditions": "التواجد في سياق توصيل الطعام، والحصول على الكلمات الرئيسية التي تصف المتاجر",
        "postconditions": "إرجاع قائمة بالمتاجر، وتوجيه المستخدم لاختيار وتحديد متجر",
        "args": {
            "keywords": "الكلمات الرئيسية التي تصف المتاجر"
        },
        "returns": "معلومات المتاجر المخرجة بشكل هيكلي",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "في سياق توصيل الطعام، يمكن استخراج الكلمات الرئيسية التي تصف المنتجات بناءً على تعبير المستخدم للبحث عن منتجات متعددة أو توصيتها",
        "preconditions": "التواجد في سياق توصيل الطعام، والحصول على الكلمات الرئيسية التي تصف المنتجات",
        "postconditions": "إرجاع قائمة المنتجات، وتوجيه المستخدم لاختيار منتج وإنشاء الطلب",
        "args": {
            "keywords": "الكلمات الرئيسية التي تصف المنتج"
        },
        "returns": "معلومات المنتج بشكل هيكلي",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "إنشاء طلب توصيل طعام، يدعم فقط الطلب من متجر واحد، ويمكن طلب منتجات متعددة من هذا المتجر",
        "preconditions": "في سياق طلبات التوصيل، يجب تحديد معرف متجر فريد ومعرف منتج واحد أو أكثر، وتحديد القيود الغذائية للمستخدم وإدراجها في الطلب",
        "postconditions": "إرجاع تفاصيل الطلب، وسؤال المستخدم عما إذا كان يرغب في دفع ثمن الطلب",
        "args": {
            "user_id": "معرف المستخدم",
            "store_id": "معرف المتجر",
            "food_ids": "قائمة معرفات المنتجات",
            "food_cnts": "قائمة الكميات المقابلة للمنتجات",
            "address": "عنوان الهدف لتوصيل الطلب الخارجي",
            "dispatch_time": "وقت بدء توصيل طلب الطعام الخارجي (أي الوقت الذي يغادر فيه السائق المتجر لاستلام الوجبة)، التنسيق هو yyyy-mm-dd HH:MM:SS",
            "attributes": "خصائص مواصفات المنتج المقابلة لمعرف المنتج",
            "note": "ملاحظات الطلب (يمنع وضع متطلبات المستخدم حول الوقت وغيرها مباشرة في الملاحظات)، مثل شرح معلومات القيود الغذائية"
        },
        "returns": "في حال نجاح الإنشاء، يتم إرجاع تفاصيل الطلب (تتضمن معرف الطلب، معرف المستخدم، معرف المتجر، قائمة معرفات المنتجات، قائمة كميات المنتجات، العنوان، وقت تقديم الطلب، وقت التحديث، حالة الطلب، قائمة المنتجات، الملاحظات)، وإلا يتم إرجاع رسالة تنبيه ذات صلة",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "في سياق طلبات الطعام الخارجي، عندما تكون معلومات الطلب موجودة في السياق السابق، ويعبر المستخدم عن تأكيد الدفع أو إعادة الدفع",
        "preconditions": "في سياق طلبات الطعام الخارجي، يعبر المستخدم عن تأكيد الدفع، وقد اكتمل إنشاء الطلب ودخل مرحلة الدفع｜أو يعبر المستخدم عن إعادة الدفع",
        "postconditions": "إرجاع معلومات نتيجة الدفع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "الحصول على حالة الطلب",
        "preconditions": "الاستعلام عن حالة طلب توصيل الطعام",
        "postconditions": "إرجاع معلومات حالة الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات حالة الطلب",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "يقوم المستخدم بإلغاء الطلب، أو إلغاء الدفع. يُحظر إلغاء الطلب مرة أخرى إذا كانت حالته بالفعل \"ملغاة\".",
        "preconditions": "الاستعلام عن حالة طلب الطعام، والتأكد من أن حالة الطلب ليست \"ملغاة\"",
        "postconditions": "إرجاع معلومات نتيجة إلغاء الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة إلغاء الطلب",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "تعديل معلومات ملاحظات الطلب",
        "preconditions": "تم تحديد معرف طلب توصيل طعام فريد order_id في السياق السابق، ويحتاج المستخدم إلى تعديل ملاحظات طلب توصيل الطعام",
        "postconditions": "إخراج معلومات الطلب بعد التعديل، وإذا لم يتم دفع الطلب بعد فيحتاج المستخدم إلى تأكيد الدفع",
        "args": {
            "order_id": "معرف الطلب",
            "note": "معلومات ملاحظات الطلب الجديدة"
        },
        "returns": "نتيجة عملية تعديل ملاحظات الطلب",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "استعلام عن جميع طلبات التوصيل، وإرجاع معلومات تتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف المتجر، والسعر الإجمالي، ووقت تقديم الطلب، ووقت التحديث، وحالة الطلب، وغيرها من المعلومات",
        "preconditions": "عرض جميع طلبات التوصيل بناءً على شروط الاستعلام",
        "postconditions": "إرجاع التفاصيل الكاملة لجميع طلبات التوصيل التي تستوفي الشروط",
        "args": {
            "user_id": "معرف المستخدم",
            "status": "حالة الطلب، القيمة الافتراضية هي غير مدفوع"
        },
        "returns": "إرجاع التفاصيل الكاملة لجميع طلبات التوصيل المطابقة للشروط، بما في ذلك معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف المتجر، والسعر الإجمالي، ووقت تقديم الطلب، ووقت التحديث، وحالة الطلب، وغيرها من المعلومات",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "الاستعلام عن طلب توصيل طعام بناءً على معرف الطلب، وإرجاع معلومات مفصلة تشمل معرف الطلب، ونوع الطلب، ومعرف المتجر، ووقت التوصيل، ومدة التوصيل، ووقت الوصول، والسعر الإجمالي، ووقت الطلب، ووقت التحديث، وحالة الطلب، وقائمة المنتجات",
        "preconditions": "يحدد السياق السابق معرف طلب توصيل طعام فريدًا واحدًا",
        "postconditions": "إرجاع المعلومات التفصيلية للطلب المحدد",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "المعلومات التفصيلية للطلب المحدد، بما في ذلك معرف الطلب، ونوع الطلب، ومعرف المتجر، ووقت التوصيل، ومدة التوصيل، ووقت الوصول، والسعر الإجمالي، ووقت الطلب، ووقت التحديث، وحالة الطلب، وقائمة المنتجات",
        "tool_type": "READ"
    },
}

# Tool descriptions - Russian version
TOOL_DESCRIPTIONS_RU = {
    "delivery_distance_to_time": {
        "description": "Рассчитывает время доставки еды (в минутах) на основе расстояния (в метрах)",
        "preconditions": "Вычисляет время доставки еды на основе расстояния от магазина до адреса пользователя",
        "postconditions": "Возвращает время доставки (в минутах)",
        "args": {
            "distance": "Расстояние (в метрах)"
        },
        "returns": "Время (в минутах)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Получение информации о магазине, включая ID магазина, рейтинг, адрес, долготу, широту, теги и список товаров",
        "preconditions": "В контексте доставки еды, требуется получить подробную информацию о магазине",
        "postconditions": "Возвращает подробную информацию о магазине",
        "args": {
            "store_id": "ID магазина"
        },
        "returns": "Подробная информация о магазине",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Получение информации о товаре, включая название товара, ID товара, название магазина, ID магазина, рейтинг товара, цену товара и теги товара",
        "preconditions": "В сценарии доставки еды, требуется получить подробную информацию о товаре",
        "postconditions": "Возвращает подробную информацию о товаре",
        "args": {
            "food_id": "ID товара"
        },
        "returns": "Подробная информация о товаре",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "В сценарии доставки еды можно извлечь ключевые слова, описывающие заведения, на основе запроса пользователя, чтобы найти или рекомендовать несколько заведений",
        "preconditions": "В контексте доставки еды, получены ключевые слова, описывающие заведения",
        "postconditions": "Возвращает список заведений и помогает пользователю выбрать и подтвердить конкретное заведение",
        "args": {
            "keywords": "Ключевые слова, описывающие заведения"
        },
        "returns": "Структурированная информация о заведениях",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "В сценарии доставки еды можно извлечь ключевые слова, описывающие товары, на основе выражения пользователя, чтобы найти или рекомендовать несколько товаров",
        "preconditions": "В сценарии доставки еды, получены ключевые слова, описывающие товары",
        "postconditions": "Возвращает список товаров, направляет пользователя к выбору товара и созданию заказа",
        "args": {
            "keywords": "Ключевые слова, описывающие товары"
        },
        "returns": "Структурированная информация о товарах",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Создание заказа на доставку еды, поддерживается заказ только у одного продавца, у одного продавца можно заказать несколько товаров",
        "preconditions": "В сценарии доставки еды, определен уникальный ID продавца и один или несколько ID товаров, определены пищевые ограничения пользователя и отражены в заказе",
        "postconditions": "Возвращает информацию о заказе, спрашивает пользователя, хочет ли он оплатить заказ",
        "args": {
            "user_id": "ID пользователя",
            "store_id": "ID магазина",
            "food_ids": "Список ID товаров",
            "food_cnts": "Список количеств, соответствующих ID товаров",
            "address": "Целевой адрес доставки еды",
            "dispatch_time": "Время начала доставки заказа на еду (то есть время, когда курьер забирает еду у продавца), формат yyyy-mm-dd HH:MM:SS",
            "attributes": "Атрибуты спецификации товара, соответствующие ID товара",
            "note": "Примечание к заказу (запрещено напрямую помещать требования пользователя относительно времени и т.д. в примечание), например, описание пищевых ограничений"
        },
        "returns": "Если создание успешно, возвращает информацию о заказе (включая ID заказа, ID пользователя, ID магазина, список ID товаров, список количеств товаров, адрес, время размещения заказа, время обновления, статус заказа, список товаров, примечание), в противном случае возвращает соответствующее информационное сообщение",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "В сценарии доставки еды, если выше есть информация о заказе, пользователь подтверждает оплату или производит повторную оплату",
        "preconditions": "В сценарии доставки еды, пользователь подтверждает оплату, заказ создан и перешел к этапу оплаты｜пользователь выражает желание оплатить повторно",
        "postconditions": "Возвращает информацию о результате оплаты",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Получить статус заказа",
        "preconditions": "Запрос статуса заказа доставки еды",
        "postconditions": "Возвращает информацию о статусе заказа",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Информация о статусе заказа",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "Пользователь отменяет заказ или платеж. Запрещено повторно отменять заказ, находящийся в состоянии «отменен».",
        "preconditions": "Запросить статус заказа доставки еды и убедиться, что статус заказа не «отменен»",
        "postconditions": "Возвращает информацию о результате отмены заказа",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Информация о результате отмены заказа",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Изменение информации о примечании к заказу",
        "preconditions": "В предыдущем контексте определен уникальный order_id заказа доставки еды, пользователю необходимо изменить примечание к заказу доставки еды",
        "postconditions": "Вывод информации о заказе после изменения, если заказ еще не оплачен, требуется подтверждение оплаты пользователем",
        "args": {
            "order_id": "ID заказа",
            "note": "Новое примечание к заказу"
        },
        "returns": "Результат операции изменения примечания к заказу",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Запрос всех заказов на доставку еды, возвращает информацию, включающую ID заказа, тип заказа, ID пользователя, ID продавца, общую сумму, время оформления, время обновления, статус заказа и другую информацию",
        "preconditions": "Просмотр всех заказов на доставку еды в соответствии с условиями запроса",
        "postconditions": "Возвращает подробную информацию обо всех заказах на доставку еды, соответствующих условиям",
        "args": {
            "user_id": "ID пользователя",
            "status": "Статус заказа, по умолчанию «Не оплачено»"
        },
        "returns": "Возвращает подробную информацию обо всех подходящих заказах на доставку еды, включая ID заказа, тип заказа, ID пользователя, ID продавца, общую сумму, время оформления, время обновления, статус заказа и другую информацию",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Запрос заказа доставки еды по идентификатору заказа, возврат подробной информации, включая идентификатор заказа, тип заказа, идентификатор продавца, время доставки, длительность доставки, время прибытия, общую сумму, время размещения заказа, время обновления, статус заказа и список товаров",
        "preconditions": "В предыдущем контексте определен уникальный order_id заказа доставки еды",
        "postconditions": "Возвращает подробную информацию указанного заказа",
        "args": {
            "order_id": "Идентификатор заказа"
        },
        "returns": "Подробная информация указанного заказа, включая идентификатор заказа, тип заказа, идентификатор продавца, время доставки, длительность доставки, время прибытия, общую сумму, время размещения заказа, время обновления, статус заказа и список товаров",
        "tool_type": "READ"
    },
}

# Tool descriptions - French version
# Tool descriptions - French version
TOOL_DESCRIPTIONS_FR = {
    "delivery_distance_to_time": {
        "description": "Calcule le temps de livraison de repas (en minutes) en fonction de la distance (en mètres)",
        "preconditions": "Calcule le temps de livraison de repas en fonction de la distance entre le commerçant et l'adresse de l'utilisateur",
        "postconditions": "Renvoie le temps de livraison (en minutes)",
        "args": {
            "distance": "Distance (en mètres)"
        },
        "returns": "Temps (en minutes)",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "Récupérer les informations du commerçant, y compris l'identifiant du commerçant, la note, l'adresse, la longitude, la latitude, les étiquettes et la liste des produits",
        "preconditions": "Dans un contexte de livraison de repas, nécessite d'obtenir les informations détaillées du commerçant",
        "postconditions": "Renvoie les informations détaillées du commerçant",
        "args": {
            "store_id": "Identifiant du commerçant"
        },
        "returns": "Informations détaillées du commerçant",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "Récupérer les informations sur le produit, y compris le nom du produit, l'identifiant du produit, le nom du magasin, l'identifiant du magasin, la note du produit, le prix du produit et les étiquettes du produit",
        "preconditions": "Dans un scénario de livraison de repas, nécessité d'obtenir les informations détaillées du produit",
        "postconditions": "Retourne les informations détaillées du produit",
        "args": {
            "food_id": "Identifiant du produit"
        },
        "returns": "Informations détaillées du produit",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "Dans le contexte de la livraison de repas, permet d'extraire des mots-clés décrivant les commerçants à partir des expressions de l'utilisateur, pour rechercher ou recommander plusieurs commerçants",
        "preconditions": "Être dans le contexte de la livraison de repas, obtenir des mots-clés décrivant les commerçants",
        "postconditions": "Renvoie une liste de commerçants, guide l'utilisateur pour choisir et confirmer un commerçant",
        "args": {
            "keywords": "Mots-clés décrivant les commerçants"
        },
        "returns": "Informations sur les commerçants fournies dans un format structuré",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "Dans le contexte de la livraison de repas, permet d'extraire des mots-clés décrivant les produits à partir des expressions de l'utilisateur, pour rechercher ou recommander plusieurs produits",
        "preconditions": "Être dans le contexte de la livraison de repas, obtenir des mots-clés décrivant les produits",
        "postconditions": "Retourne une liste de produits, guide l'utilisateur pour sélectionner un produit et créer une commande",
        "args": {
            "keywords": "Mots-clés décrivant les produits"
        },
        "returns": "Informations sur les produits avec une sortie structurée",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "Création de commande de livraison de repas. Prend uniquement en charge la commande auprès d'un seul commerçant ; plusieurs articles peuvent être commandés auprès d'un seul commerçant.",
        "preconditions": "Dans le scénario de livraison de repas, déterminer un identifiant de commerçant unique et un ou plusieurs identifiants d'articles, déterminer les restrictions alimentaires de l'utilisateur et les refléter dans la commande.",
        "postconditions": "Renvoie les informations de la commande et demande à l'utilisateur s'il souhaite procéder au paiement.",
        "args": {
            "user_id": "Identifiant de l'utilisateur",
            "store_id": "Identifiant du commerçant",
            "food_ids": "Liste des identifiants d'articles",
            "food_cnts": "Liste des quantités correspondant aux identifiants d'articles",
            "address": "Adresse de livraison cible",
            "dispatch_time": "Heure de début de livraison de la commande (c'est-à-dire l'heure de départ du livreur depuis le commerçant), format yyyy-mm-dd HH:MM:SS",
            "attributes": "Attributs de spécification de l'article correspondant à l'identifiant de l'article",
            "note": "Notes de commande (interdiction de placer directement les demandes de l'utilisateur concernant l'heure, etc. dans les notes), par exemple les informations sur les restrictions alimentaires"
        },
        "returns": "Si la création réussit, renvoie les informations de la commande (incluant l'identifiant de commande, l'identifiant de l'utilisateur, l'identifiant du commerçant, la liste des identifiants d'articles, la liste des quantités, l'adresse, l'heure de commande, l'heure de mise à jour, le statut de la commande, la liste des articles, les notes), sinon renvoie un message d'information pertinent.",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "Dans le contexte de la livraison de repas, lorsque les informations de commande sont disponibles précédemment et que l'utilisateur confirme le paiement ou effectue un nouveau paiement",
        "preconditions": "Contexte de livraison de repas, l'utilisateur confirme le paiement, la commande est créée et entrée dans l'étape de paiement｜l'utilisateur indique un nouveau paiement",
        "postconditions": "Retourne les informations sur le résultat du paiement",
        "args": {
            "order_id": "Identifiant de la commande"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "Récupérer le statut de la commande",
        "preconditions": "Vérifier le statut de la commande de livraison",
        "postconditions": "Retourne les informations sur le statut de la commande",
        "args": {
            "order_id": "ID de la commande"
        },
        "returns": "Informations sur le statut de la commande",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "L'utilisateur annule une commande ou un paiement. Il est interdit d'annuler à nouveau une commande déjà dans l'état annulé.",
        "preconditions": "Vérifier le statut de la commande de livraison de repas et s'assurer que le statut de la commande n'est pas « cancelled ».",
        "postconditions": "Renvoie les informations relatives au résultat de l'annulation de la commande.",
        "args": {
            "order_id": "Identifiant de la commande"
        },
        "returns": "Informations relatives au résultat de l'annulation de la commande",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "Modifier les notes de la commande",
        "preconditions": "Le contexte précédent a identifié un unique order_id de commande de livraison de repas, l'utilisateur souhaite modifier la note de la commande",
        "postconditions": "Affiche les informations de la commande après modification. Si la commande n'est pas encore payée, l'utilisateur doit confirmer le paiement",
        "args": {
            "order_id": "ID de la commande",
            "note": "Nouvelle note de commande"
        },
        "returns": "Résultat de la modification de la note de la commande",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "Interroger toutes les commandes de livraison, retourner les informations incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID du commerçant, le prix total, l'heure de commande, l'heure de mise à jour, le statut de la commande, etc.",
        "preconditions": "Afficher toutes les commandes de livraison selon les conditions de requête",
        "postconditions": "Retourner les informations détaillées de toutes les commandes de livraison conformes aux conditions",
        "args": {
            "user_id": "ID utilisateur",
            "status": "Statut de la commande, par défaut non payé"
        },
        "returns": "Retourner les informations détaillées de toutes les commandes de livraison conformes aux conditions, incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID du commerçant, le prix total, l'heure de commande, l'heure de mise à jour, le statut de la commande, etc.",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "Interroger une commande de livraison de nourriture en fonction de l'ID de commande, renvoyer des informations détaillées comprenant l'ID de commande, le type de commande, l'ID du commerçant, l'heure de livraison, la durée de livraison, l'heure d'arrivée, le prix total, l'heure de passation de la commande, l'heure de mise à jour, le statut de la commande et la liste des produits",
        "preconditions": "Un order_id unique de commande de livraison de nourriture doit être déterminé dans le contexte précédent",
        "postconditions": "Renvoie les informations détaillées de la commande spécifiée",
        "args": {
            "order_id": "Identifiant de la commande"
        },
        "returns": "Informations détaillées de la commande spécifiée, comprenant l'ID de commande, le type de commande, l'ID du commerçant, l'heure de livraison, la durée de livraison, l'heure d'arrivée, le prix total, l'heure de passation de la commande, l'heure de mise à jour, le statut de la commande et la liste des produits",
        "tool_type": "READ"
    },
}

# Tool descriptions - Japanese version
TOOL_DESCRIPTIONS_JA = {
    "delivery_distance_to_time": {
        "description": "距離（メートル）に基づいてフードデリバリーの配送時間（分）を計算します",
        "preconditions": "店舗からユーザーの住所までの距離に基づいてフードデリバリーの配送時間を計算します",
        "postconditions": "配送時間（分）を返します",
        "args": {
            "distance": "距離（メートル単位）"
        },
        "returns": "時間（分単位）",
        "tool_type": "GENERIC"
    },

    "get_delivery_store_info": {
        "description": "店舗情報を取得します。店舗 ID、評価、住所、経度、緯度、タグ、商品リストを含みます。",
        "preconditions": "出前シナリオにおいて、店舗の詳細情報を取得する必要がある場合",
        "postconditions": "店舗の詳細情報を返します",
        "args": {
            "store_id": "店舗 ID"
        },
        "returns": "店舗の詳細情報",
        "tool_type": "READ"
    },

    "get_delivery_product_info": {
        "description": "商品情報を取得します。商品名、商品 ID、店舗名、店舗 ID、商品評価、商品価格、商品タグを含みます。",
        "preconditions": "フードデリバリーのシーンであり、商品の詳細情報を取得する必要がある場合。",
        "postconditions": "商品の詳細情報を返します。",
        "args": {
            "food_id": "商品 ID"
        },
        "returns": "商品の詳細情報",
        "tool_type": "READ"
    },

    "delivery_store_search_recommend": {
        "description": "出前サービスのシーンにおいて、ユーザーの発言から店舗を説明するキーワードを抽出し、複数の店舗を検索または推薦します。",
        "preconditions": "出前サービスのシーンであり、店舗を説明するキーワードが取得されていること。",
        "postconditions": "店舗リストを返し、ユーザーが店舗を選択して確定するよう誘導します。",
        "args": {
            "keywords": "店舗を説明するキーワード"
        },
        "returns": "構造化されて出力された店舗情報",
        "tool_type": "READ"
    },

    "delivery_product_search_recommend": {
        "description": "出前サービスのシーンにおいて、ユーザーの発言から商品を説明するキーワードを抽出し、複数の商品を検索または推薦します。",
        "preconditions": "出前サービスのシーンであり、商品を説明するキーワードが取得されていること。",
        "postconditions": "商品リストを返し、ユーザーに商品を選択して注文を作成するよう誘導します。",
        "args": {
            "keywords": "商品を説明するキーワード"
        },
        "returns": "構造化された商品情報",
        "tool_type": "READ"
    },

    "create_delivery_order": {
        "description": "出前注文の作成。単一店舗からの注文のみ対応可能で、同一店舗から複数の商品を注文できます。",
        "preconditions": "出前シーンであること。唯一の store_id と 1 つ以上の food_id を特定し、ユーザーの食事制限を確認し、注文に反映させる必要があります。",
        "postconditions": "注文情報を返し、ユーザーに注文の支払いを行うかどうか確認します。",
        "args": {
            "user_id": "ユーザーID",
            "store_id": "店舗ID",
            "food_ids": "商品IDリスト",
            "food_cnts": "数量リスト",
            "address": "出前配送先の住所",
            "dispatch_time": "出前注文の配送開始時間（つまりライダーが店舗から食事を受け取り出発する時間）。形式は yyyy-mm-dd HH:MM:SS",
            "attributes": "food_id に対応する商品仕様属性",
            "note": "注文備考（ユーザーの時間などの要望を直接備考に記載することは禁止）。例：食事制限情報の説明"
        },
        "returns": "作成成功の場合、注文情報（order_id、user_id、store_id、food_ids、food_cnts、address、注文時間、更新時間、注文ステータス、商品リスト、note を含む）を返します。失敗の場合、関連するメッセージを返します。",
        "tool_type": "WRITE"
    },

    "pay_delivery_order": {
        "description": "フードデリバリーのシナリオでは、文脈に注文情報があり、ユーザーが支払い確認、または再支払いを表明している",
        "preconditions": "フードデリバリーのシナリオであり、ユーザーが支払い確認を表明し、注文作成が完了し支払い段階に入っている｜ユーザーが再支払いを表明している",
        "postconditions": "支払い結果情報を返す",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報",
        "tool_type": "WRITE"
    },

    "get_delivery_order_status": {
        "description": "注文ステータスを取得する",
        "preconditions": "配達注文のステータスを照会する",
        "postconditions": "注文ステータス情報を返す",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文ステータス情報",
        "tool_type": "READ"
    },

    "cancel_delivery_order": {
        "description": "ユーザーによる注文または支払いのキャンセル処理を行います。すでにキャンセル済みの状態にある注文に対して、再度キャンセルすることは禁止されています。",
        "preconditions": "出前注文のステータスを照会し、注文ステータスが cancelled ではないことを確認します。",
        "postconditions": "注文キャンセルの結果情報を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文キャンセルの結果情報",
        "tool_type": "WRITE"
    },

    "modify_delivery_order": {
        "description": "注文備考情報を変更する",
        "preconditions": "文脈上で唯一のデリバリー注文 order_id が特定されており、ユーザーがデリバリー注文の備考を変更する必要があること",
        "postconditions": "変更後の注文情報を出力する。注文が未支払いの場合、ユーザーに支払い確認が必要となる",
        "args": {
            "order_id": "注文の order_id",
            "note": "新しい注文備考情報"
        },
        "returns": "注文備考変更操作の結果",
        "tool_type": "WRITE"
    },

    "search_delivery_orders": {
        "description": "全てのデリバリー注文を検索し、注文 ID、注文タイプ、ユーザー ID、店舗 ID、合計金額、注文時間、更新時間、注文ステータスなどの情報を返します。",
        "preconditions": "検索条件に基づいて全てのデリバリー注文を表示します。",
        "postconditions": "条件に適合する全てのデリバリー注文の詳細情報を返します。",
        "args": {
            "user_id": "ユーザー ID",
            "status": "注文ステータス。デフォルトは未払い。"
        },
        "returns": "条件に適合する全てのデリバリー注文の詳細情報を返します。注文 ID、注文タイプ、ユーザー ID、店舗 ID、合計金額、注文時間、更新時間、注文ステータスなどの情報を含みます。",
        "tool_type": "READ"
    },

    "get_delivery_order_detail": {
        "description": "注文 ID に基づいて配達注文を検索し、注文 ID、注文タイプ、店舗 ID、配達時間、配達所要時間、配達完了時間、合計金額、注文時間、更新時間、注文ステータス、商品リストなどの詳細情報を返します。",
        "preconditions": "前の文脈で唯一の配達 order_id が特定されていること。",
        "postconditions": "指定された注文の詳細情報を返します。",
        "args": {
            "order_id": "注文 id"
        },
        "returns": "指定された注文の詳細情報。注文 ID、注文タイプ、店舗 ID、配達時間、配達所要時間、配達完了時間、合計金額、注文時間、更新時間、注文ステータス、商品リストを含みます。",
        "tool_type": "READ"
    },
}

# Create Delivery tool schema manager
_schema_manager = create_tool_schema_manager("delivery", TOOL_DESCRIPTIONS_ZH, TOOL_DESCRIPTIONS_EN, japanese=TOOL_DESCRIPTIONS_JA, french=TOOL_DESCRIPTIONS_FR, russian=TOOL_DESCRIPTIONS_RU, arabic=TOOL_DESCRIPTIONS_AR, hindi=TOOL_DESCRIPTIONS_HI, thai=TOOL_DESCRIPTIONS_TH, spanish=TOOL_DESCRIPTIONS_ES, korean=TOOL_DESCRIPTIONS_KO, indonesian=TOOL_DESCRIPTIONS_ID, hebrew=TOOL_DESCRIPTIONS_HE, turkish=TOOL_DESCRIPTIONS_TR, vietnamese=TOOL_DESCRIPTIONS_VI, malay=TOOL_DESCRIPTIONS_MS, belarusian=TOOL_DESCRIPTIONS_BE, punjabi=TOOL_DESCRIPTIONS_PA, kazakh=TOOL_DESCRIPTIONS_KK, khmer=TOOL_DESCRIPTIONS_KM, burmese=TOOL_DESCRIPTIONS_MY, lao=TOOL_DESCRIPTIONS_LO, tamil=TOOL_DESCRIPTIONS_TA, telugu=TOOL_DESCRIPTIONS_TE)

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
