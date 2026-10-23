"""Tool schema utilities for the toolkit system.

This file provides utilities for generating tool descriptions and docstrings
that can be used by the is_tool decorator.
"""

from typing import Dict, Any
from vita.utils.schema_utils import (
    generate_tool_docstring, 
    get_domain_from_class,
    create_tool_schema_manager
)

# Tool descriptions for toolkit.py - Chinese version
TOOLKIT_TOOL_DESCRIPTIONS_ZH = {
    "longitude_latitude_to_distance": {
        "description": "根据经纬度计算两点之间的距离（以米为单位）",
        "preconditions": "根据两个点的经纬度计算它们之间的距离",
        "postconditions": "返回两点之间的距离（整数，以米为单位）",
        "args": {
            "longitude1": "第一个点的经度",
            "latitude1": "第一个点的纬度",
            "longitude2": "第二个点的经度",
            "latitude2": "第二个点的纬度"
        },
        "returns": "两点之间的距离（整数，以米为单位）"
    },
    
    "weather": {
        "description": "查询指定地址在date_start到date_end期间的天气信息",
        "preconditions": "查询指定地址在指定日期范围内的天气信息",
        "postconditions": "返回天气信息",
        "args": {
            "address": "要查询的地址",
            "date_start": "开始时间，格式为 yyyy-mm-dd",
            "date_end": "结束时间，格式为 yyyy-mm-dd"
        },
        "returns": "天气信息"
    },
    
    "address_to_longitude_latitude": {
        "description": "根据地址获取经纬度",
        "preconditions": "根据地址获取对应的经纬度坐标",
        "postconditions": "返回经纬度坐标",
        "args": {
            "address": "要查询的地址"
        },
        "returns": "[经度, 纬度]"
    },
    
    "get_date_holiday_info": {
        "description": "判断某日期是否为中国节假日；如果是则返回节假日中文名称",
        "preconditions": "根据日期判断是否为节假日，如果是则返回节假日名称",
        "postconditions": "返回节假日信息",
        "args": {
            "date": "日期，格式为 yyyy-mm-dd"
        },
        "returns": "节假日信息判断结果"
    },
    
    "get_holiday_date": {
        "description": "获取指定年份中某个节假日对应的具体日期",
        "preconditions": "获取指定年份中某个节假日的具体日期",
        "postconditions": "返回节假日的日期",
        "args": {
            "year": "年份",
            "holiday_name": "节假日名称，仅支持中文表述"
        },
        "returns": "节假日的日期"
    },
    
    "get_user_historical_behaviors": {
        "description": "获取用户基本信息和历史行为偏好数据，包括用户ID、家庭住址、工作地址等基本信息，以及各场景的详细消费习惯、偏好品类、价格区间、评分要求、时间偏好等信息，用于个性化推荐和服务优化",
        "preconditions": "获取用户历史行为数据",
        "postconditions": "返回用户历史行为信息",
        "args": {},
        "returns": "用户历史行为信息摘要"
    },
    
    "get_user_all_orders": {
        "description": "获取用户所有订单信息",
        "preconditions": "获取用户的所有订单信息",
        "postconditions": "返回用户所有订单信息",
        "args": {},
        "returns": "用户所有订单信息摘要"
    },
    
    "get_nearby": {
        "description": "获取附近所有商店/商业场所的信息",
        "preconditions": "获取指定范围内（米）的所有商业场所（商店、机场或火车站、酒店、景点、商铺等）的信息",
        "postconditions": "返回商业场所信息",
        "args": {
            "longitude": "经度",
            "latitude": "纬度",
            "range": "范围（以米为单位）"
        },
        "returns": "商店/商业场所信息"
    },
}

# Tool descriptions for toolkit.py - English version
TOOLKIT_TOOL_DESCRIPTIONS_EN = {
    "longitude_latitude_to_distance": {
        "description": "Calculate distance between two points based on longitude and latitude (in meters)",
        "preconditions": "Calculate distance between two points based on their longitude and latitude",
        "postconditions": "Return distance between two points (integer, in meters)",
        "args": {
            "longitude1": "Longitude of first point",
            "latitude1": "Latitude of first point",
            "longitude2": "Longitude of second point",
            "latitude2": "Latitude of second point"
        },
        "returns": "Distance between two points (integer, in meters)"
    },
    
    "weather": {
        "description": "Query weather information for specified address during date_start to date_end period",
        "preconditions": "Query weather information for specified address within specified date range",
        "postconditions": "Return weather information",
        "args": {
            "address": "Address to query",
            "date_start": "Start time, format: yyyy-mm-dd",
            "date_end": "End time, format: yyyy-mm-dd"
        },
        "returns": "Weather information"
    },
    
    "address_to_longitude_latitude": {
        "description": "Get longitude and latitude based on address",
        "preconditions": "Get corresponding longitude and latitude coordinates based on address",
        "postconditions": "Return longitude and latitude coordinates",
        "args": {
            "address": "Address to query"
        },
        "returns": "[Longitude, Latitude]"
    },
    
    "get_date_holiday_info": {
        "description": "Determine if a date is a Chinese holiday; if so, return the Chinese holiday name",
        "preconditions": "Determine if it's a holiday based on date, if so return holiday name",
        "postconditions": "Return holiday information",
        "args": {
            "date": "Date, format: yyyy-mm-dd"
        },
        "returns": "Holiday information determination result"
    },
    
    "get_holiday_date": {
        "description": "Get the specific date corresponding to a holiday in a specified year",
        "preconditions": "Get the specific date of a holiday in a specified year",
        "postconditions": "Return the holiday date",
        "args": {
            "year": "Year",
            "holiday_name": "Holiday name, only supports English expressions"
        },
        "returns": "Holiday date"
    },
    
    "get_user_historical_behaviors": {
        "description": "Get user basic information and historical behavior preference data, including user ID, home address, work address and other basic information, as well as detailed consumption habits, preferred categories, price ranges, rating requirements, time preferences and other information for various scenarios, used for personalized recommendations and service optimization",
        "preconditions": "Get user historical behavior data",
        "postconditions": "Return user historical behavior information",
        "args": {},
        "returns": "User historical behavior information summary"
    },
    
    "get_user_all_orders": {
        "description": "Get all order information for user",
        "preconditions": "Get all order information for user",
        "postconditions": "Return all order information for user",
        "args": {},
        "returns": "Summary of all order information for user"
    },
    
    "get_nearby": {
        "description": "Get information about all nearby stores/commercial establishments",
        "preconditions": "Get information about all commercial establishments (stores, airports or train stations, hotels, attractions, shops, etc.) within specified range (in meters)",
        "postconditions": "Return commercial establishment information",
        "args": {
            "longitude": "Longitude",
            "latitude": "Latitude",
            "range": "Range (in meters)"
        },
        "returns": "Store/commercial establishment information"
    },

}

# Tool descriptions - Telugu version
TOOLKIT_TOOL_DESCRIPTIONS_TE = {
    "longitude_latitude_to_distance": {
        "description": "రెండు బిందువుల మధ్య దూరాన్ని అక్షాంశం మరియు రేఖాంశం ఆధారంగా లెక్కించండి (మీటర్లలో)",
        "preconditions": "రెండు బిందువుల అక్షాంశం మరియు రేఖాంశం ఆధారంగా వాటి మధ్య దూరాన్ని లెక్కించండి",
        "postconditions": "రెండు బిందువుల మధ్య దూరాన్ని తిరిగి ఇస్తుంది (పూర్ణాంకం, మీటర్లలో)",
        "args": {
            "longitude1": "మొదటి బిందువు యొక్క రేఖాంశం",
            "latitude1": "మొదటి బిందువు యొక్క అక్షాంశం",
            "longitude2": "రెండవ బిందువు యొక్క రేఖాంశం",
            "latitude2": "రెండవ బిందువు యొక్క అక్షాంశం"
        },
        "returns": "రెండు బిందువుల మధ్య దూరం (పూర్ణాంకం, మీటర్లలో)"
    },

    "weather": {
        "description": "నిర్దిష్ట చిరునామాకు date_start నుండి date_end వరకు ఉన్న వాతావరణ సమాచారాన్ని విచారించండి",
        "preconditions": "నిర్దిష్ట చిరునామాకు నిర్దిష్ట తేదీ పరిధిలో వాతావరణ సమాచారాన్ని విచారించండి",
        "postconditions": "వాతావరణ సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "address": "విచారించాల్సిన చిరునామా",
            "date_start": "ప్రారంభ సమయం, ఫార్మాట్ yyyy-mm-dd",
            "date_end": "ముగింపు సమయం, ఫార్మాట్ yyyy-mm-dd"
        },
        "returns": "వాతావరణ సమాచారం"
    },

    "address_to_longitude_latitude": {
        "description": "చిరునామా ఆధారంగా అక్షాంశ రేఖాంశాలను పొందండి",
        "preconditions": "చిరునామా ఆధారంగా సంబంధిత అక్షాంశ రేఖాంశ నిరూపకాలను పొందండి",
        "postconditions": "అక్షాంశ రేఖాంశ నిరూపకాలను తిరిగి ఇస్తుంది",
        "args": {
            "address": "విచారించాల్సిన చిరునామా"
        },
        "returns": "[రేఖాంశం, అక్షాంశం]"
    },

    "get_date_holiday_info": {
        "description": "ఒక నిర్దిష్ట తేదీ చైనా సెలవుదినం అయితే లేదా కాదా తనిఖీ చేయండి; అయితే సెలవుదినం యొక్క చైనీస్ పేరును తిరిగి ఇవ్వండి",
        "preconditions": "తేదీ ఆధారంగా అది సెలవుదినం అయితే లేదా కాదా తనిఖీ చేయండి, అయితే సెలవుదినం పేరును తిరిగి ఇవ్వండి",
        "postconditions": "సెలవుదినం సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {
            "date": "తేదీ, ఫార్మాట్ yyyy-mm-dd"
        },
        "returns": "సెలవుదినం సమాచారం తనిఖీ ఫలితం"
    },

    "get_holiday_date": {
        "description": "నిర్దిష్ట సంవత్సరంలో ఒక సెలవు దినానికి సంబంధించిన నిర్దిష్ట తేదీని పొందండి",
        "preconditions": "నిర్దిష్ట సంవత్సరంలో ఒక సెలవు దినానికి సంబంధించిన నిర్దిష్ట తేదీని పొందండి",
        "postconditions": "సెలవు దినానికి సంబంధించిన తేదీని తిరిగి ఇస్తుంది",
        "args": {
            "year": "సంవత్సరం",
            "holiday_name": "సెలవు దినానికి సంబంధించిన పేరు, చైనీస్ భాషలో మాత్రమే మద్దతు ఇస్తుంది"
        },
        "returns": "సెలవు దినానికి సంబంధించిన తేదీ"
    },

    "get_user_historical_behaviors": {
        "description": "వినియోగదారి ప్రాథమిక సమాచారం మరియు చరిత్ర ప్రవర్తనా ప్రాధాన్యతల డేటాను పొందండి, ఇందులో వినియోగదారి ID, ఇంటి చిరునామా, పని చిరునామా వంటి ప్రాథమిక సమాచారం, అలాగే వివిధ సందర్భాలలో వివరణాత్మక ఖర్చు అలవాట్లు, ఇష్టపడే వర్గాలు, ధర పరిధి, రేటింగ్ అవసరాలు, సమయ ప్రాధాన్యతలు వంటి సమాచారం ఉంటాయి, ఇది వ్యక్తిగతీకరించిన సిఫార్సులు మరియు సేవా మెరుగుదల కోసం ఉపయోగించబడుతుంది",
        "preconditions": "వినియోగదారి చరిత్ర ప్రవర్తన డేటాను పొందండి",
        "postconditions": "వినియోగదారి చరిత్ర ప్రవర్తన సమాచారాన్ని తిరిగి ఇవ్వండి",
        "args": {},
        "returns": "వినియోగదారి చరిత్ర ప్రవర్తన సమాచార సారాంశం"
    },

    "get_user_all_orders": {
        "description": "వినియోగదారు యొక్క అన్ని ఆర్డర్ల సమాచారాన్ని పొందడం",
        "preconditions": "వినియోగదారు యొక్క అన్ని ఆర్డర్ల సమాచారాన్ని పొందడం",
        "postconditions": "వినియోగదారు యొక్క అన్ని ఆర్డర్ల సమాచారాన్ని తిరిగి ఇవ్వడం",
        "args": {},
        "returns": "వినియోగదారు యొక్క అన్ని ఆర్డర్ల సమాచార సారాంశం"
    },

    "get_nearby": {
        "description": "సమీపంలోని అన్ని దుకాణాలు/వాణిజ్య స్థలాల సమాచారాన్ని పొందండి",
        "preconditions": "నిర్దిష్ట పరిధిలో (మీటర్లలో) ఉన్న అన్ని వాణిజ్య స్థలాల (దుకాణాలు, విమానాశ్రయాలు లేదా రైల్వే స్టేషన్లు, హోటళ్లు, పర్యాటక ప్రదేశాలు, షాపులు మొదలైనవి) సమాచారాన్ని పొందండి",
        "postconditions": "వాణిజ్య స్థలాల సమాచారాన్ని తిరిగి ఇస్తుంది",
        "args": {
            "longitude": "రేఖాంశం",
            "latitude": "అక్షాంశం",
            "range": "పరిధి (మీటర్లలో)"
        },
        "returns": "దుకాణం/వాణిజ్య స్థలాల సమాచారం"
    },
}

# Tool descriptions - Tamil version
TOOLKIT_TOOL_DESCRIPTIONS_TA = {
    "longitude_latitude_to_distance": {
        "description": "அட்சரேகை மற்றும் தீர்க்கரேகையின் அடிப்படையில் இரண்டு புள்ளிகளுக்கு இடையே உள்ள தூரத்தைக் கணக்கிடவும் (மீட்டரில்)",
        "preconditions": "இரண்டு புள்ளிகளின் அட்சரேகை மற்றும் தீர்க்கரேகையின் அடிப்படையில் அவற்றுக்கு இடையே உள்ள தூரத்தைக் கணக்கிடவும்",
        "postconditions": "இரண்டு புள்ளிகளுக்கு இடையே உள்ள தூரத்தைத் திருப்பி அனுப்புகிறது (முழு எண், மீட்டரில்)",
        "args": {
            "longitude1": "முதல் புள்ளியின் தீர்க்கரேகை",
            "latitude1": "முதல் புள்ளியின் அட்சரேகை",
            "longitude2": "இரண்டாவது புள்ளியின் தீர்க்கரேகை",
            "latitude2": "இரண்டாவது புள்ளியின் அட்சரேகை"
        },
        "returns": "இரண்டு புள்ளிகளுக்கு இடையே உள்ள தூரம் (முழு எண், மீட்டரில்)"
    },

    "weather": {
        "description": "குறிப்பிட்ட முகவரிக்கான date_start முதல் date_end வரையிலான வானிலைத் தகவலை விசாரிக்கவும்",
        "preconditions": "குறிப்பிட்ட முகவரிக்கான குறிப்பிட்ட தேதி வரம்பிற்குள் வானிலைத் தகவலை விசாரிக்கவும்",
        "postconditions": "வானிலைத் தகவலைத் திருப்பி அனுப்பும்",
        "args": {
            "address": "விசாரிக்க வேண்டிய முகவரி",
            "date_start": "தொடக்க நேரம், வடிவம் yyyy-mm-dd",
            "date_end": "முடிவு நேரம், வடிவம் yyyy-mm-dd"
        },
        "returns": "வானிலைத் தகவல்"
    },

    "address_to_longitude_latitude": {
        "description": "முகவரியைக் கொண்டு அட்சரேகை மற்றும் தீர்க்கரேகையைப் பெறுக",
        "preconditions": "முகவரியைக் கொண்டு தொடர்புடைய அட்சரேகை மற்றும் தீர்க்கரேகை ஆயங்களைப் பெறுக",
        "postconditions": "அட்சரேகை மற்றும் தீர்க்கரேகை ஆயங்களைத் திருப்பி அனுப்பு",
        "args": {
            "address": "விசாரிக்க வேண்டிய முகவரி"
        },
        "returns": "[தீர்க்கரேகை, அட்சரேகை]"
    },

    "get_date_holiday_info": {
        "description": "ஒரு குறிப்பிட்ட தேதி சீன விடுமுறையா என்பதைத் தீர்மானிக்கவும்; ஆம் எனில், விடுமுறையின் சீனப் பெயரைத் திரும்ப அனுப்பவும்",
        "preconditions": "தேதியின் அடிப்படையில் அது விடுமுறையா எனத் தீர்மானிக்கவும், ஆம் எனில் விடுமுறையின் பெயரைத் திரும்ப அனுப்பவும்",
        "postconditions": "விடுமுறைத் தகவலைத் திரும்ப அனுப்பவும்",
        "args": {
            "date": "தேதி, வடிவம் yyyy-mm-dd"
        },
        "returns": "விடுமுறைத் தகவல் தீர்மானிப்பு முடிவு"
    },

    "get_holiday_date": {
        "description": "குறிப்பிட்ட ஆண்டில் ஒரு விடுமுறை நாளுக்குரிய குறிப்பிட்ட தேதியைப் பெறுக",
        "preconditions": "குறிப்பிட்ட ஆண்டில் ஒரு விடுமுறை நாளின் குறிப்பிட்ட தேதியைப் பெறுக",
        "postconditions": "விடுமுறை நாளின் தேதியைத் திருப்பி அனுப்புக",
        "args": {
            "year": "ஆண்டு",
            "holiday_name": "விடுமுறை நாளின் பெயர், சீன மொழி உரை மட்டுமே ஆதரிக்கப்படும்"
        },
        "returns": "விடுமுறை நாளின் தேதி"
    },

    "get_user_historical_behaviors": {
        "description": "பயனர் அடிப்படைத் தகவல் மற்றும் வரலாற்று நடத்தை விருப்பத் தரவைப் பெறுதல், இதில் பயனர் ஐடி, வீட்டு முகவரி, பணி முகவரி போன்ற அடிப்படைத் தகவல்கள், மேலும் பல்வேறு சூழல்களில் விரிவான நுகர்வு பழக்கங்கள், விருப்பமான வகைகள், விலை வரம்புகள், மதிப்பீட்டுத் தேவைகள், நேர விருப்பங்கள் போன்ற தகவல்கள் அடங்கும், இது தனிப்பயனாக்கப்பட்ட பரிந்துரை மற்றும் சேவை மேம்பாட்டிற்குப் பயன்படுத்தப்படுகிறது",
        "preconditions": "பயனர் வரலாற்று நடத்தைத் தரவைப் பெறுதல்",
        "postconditions": "பயனர் வரலாற்று நடத்தைத் தகவலைத் திருப்பி அனுப்புதல்",
        "args": {},
        "returns": "பயனர் வரலாற்று நடத்தைத் தகவல் சுருக்கம்"
    },

    "get_user_all_orders": {
        "description": "பயனரின் அனைத்து ஆர்டர் விவரங்களையும் பெறுக",
        "preconditions": "பயனரின் அனைத்து ஆர்டர் விவரங்களையும் பெறுக",
        "postconditions": "பயனரின் அனைத்து ஆர்டர் விவரங்களையும் திருப்பி அனுப்புக",
        "args": {},
        "returns": "பயனரின் அனைத்து ஆர்டர் விவரங்களின் சுருக்கம்"
    },

    "get_nearby": {
        "description": "அருகிலுள்ள அனைத்து கடைகள்/வணிக இடங்களின் தகவல்களைப் பெறுக",
        "preconditions": "குறிப்பிட்ட வரம்பிற்குள் (மீட்டர்) உள்ள அனைத்து வணிக இடங்களின் (கடைகள், விமான நிலையம் அல்லது ரயில் நிலையம், ஹோட்டல்கள், சுற்றுலா தலங்கள், கடைகள் போன்றவை) தகவல்களைப் பெறுக",
        "postconditions": "வணிக இடங்களின் தகவல்களைத் திருப்பி அனுப்பு",
        "args": {
            "longitude": "தீர்க்கரேகை",
            "latitude": "அட்சரேகை",
            "range": "வரம்பு (மீட்டரில்)"
        },
        "returns": "கடை/வணிக இடங்களின் தகவல்கள்"
    },
}

# Tool descriptions - Lao version
TOOLKIT_TOOL_DESCRIPTIONS_LO = {
    "longitude_latitude_to_distance": {
        "description": "ຄິດໄລ່ໄລຍະຫ່າງລະຫວ່າງສອງຈຸດໂດຍອີງໃສ່ລະຕິຈູດ ແລະ ລອງຈິຈູດ (ຫົວໜ່ວຍເປັນແມັດ)",
        "preconditions": "ຄິດໄລ່ໄລຍະຫ່າງລະຫວ່າງສອງຈຸດໂດຍອີງໃສ່ລະຕິຈູດ ແລະ ລອງຈິຈູດຂອງມັນ",
        "postconditions": "ສົ່ງຄ່າໄລຍະຫ່າງລະຫວ່າງສອງຈຸດ (ຈຳນວນຖ້ວນ, ຫົວໜ່ວຍເປັນແມັດ)",
        "args": {
            "longitude1": "ລອງຈິຈູດຂອງຈຸດທຳອິດ",
            "latitude1": "ລະຕິຈູດຂອງຈຸດທຳອິດ",
            "longitude2": "ລອງຈິຈູດຂອງຈຸດທີສອງ",
            "latitude2": "ລະຕິຈູດຂອງຈຸດທີສອງ"
        },
        "returns": "ໄລຍະຫ່າງລະຫວ່າງສອງຈຸດ (ຈຳນວນຖ້ວນ, ຫົວໜ່ວຍເປັນແມັດ)"
    },

    "weather": {
        "description": "ສືບຄົ້ນຂໍ້ມູນອາກາດສຳລັບທີ່ຢູ່ທີ່ລະບຸ ໃນໄລຍະເວລາຈາກ date_start ຫາ date_end",
        "preconditions": "ສືບຄົ້ນຂໍ້ມູນອາກາດສຳລັບທີ່ຢູ່ທີ່ລະບຸ ພາຍໃນຊ່ວງວັນທີທີ່ກຳນົດ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນອາກາດ",
        "args": {
            "address": "ທີ່ຢູ່ທີ່ຕ້ອງການສືບຄົ້ນ",
            "date_start": "ເວລາເລີ່ມຕົ້ນ, ຮູບແບບແມ່ນ yyyy-mm-dd",
            "date_end": "ເວລາສິ້ນສຸດ, ຮູບແບບແມ່ນ yyyy-mm-dd"
        },
        "returns": "ຂໍ້ມູນອາກາດ"
    },

    "address_to_longitude_latitude": {
        "description": "ຊອກຫາພິກັດຜາງແລະຂົ້ວຕາມທີ່ຢູ່",
        "preconditions": "ຊອກຫາພິກັດຜາງແລະຂົ້ວທີ່ກົງກັນຕາມທີ່ຢູ່",
        "postconditions": "ສົ່ງຄືນພິກັດຜາງແລະຂົ້ວ",
        "args": {
            "address": "ທີ່ຢູ່ທີ່ຕ້ອງການຊອກຫາ"
        },
        "returns": "[ພິກັດຜາງ, ພິກັດຂົ້ວ]"
    },

    "get_date_holiday_info": {
        "description": "ກວດເບິ່ງວ່າວັນທີສະເພາະໃດໜຶ່ງແມ່ນວັນພັກຂອງຈີນຫຼືບໍ່; ຖ້າແມ່ນແລ້ວໃຫ້ສົ່ງຄືນຊື່ວັນພັກເປັນພາສາຈີນ",
        "preconditions": "ກວດເບິ່ງວ່າເປັນວັນພັກຫຼືບໍ່ໂດຍອີງໃສ່ວັນທີ, ຖ້າແມ່ນແລ້ວໃຫ້ສົ່ງຄືນຊື່ວັນພັກ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນວັນພັກ",
        "args": {
            "date": "ວັນທີ, ຮູບແບບແມ່ນ yyyy-mm-dd"
        },
        "returns": "ຜົນການກວດເບິ່ງຂໍ້ມູນວັນພັກ"
    },

    "get_holiday_date": {
        "description": "ຊອກຫາວັນທີສະເພາະທີ່ກົງກັບວັນພັກໃນປີທີ່ລະບຸ",
        "preconditions": "ຊອກຫາວັນທີສະເພາະຂອງວັນພັກໃນປີທີ່ລະບຸ",
        "postconditions": "ສົ່ງຄືນວັນທີຂອງວັນພັກ",
        "args": {
            "year": "ປີ",
            "holiday_name": "ຊື່ວັນພັກ, ຮອງຮັບສະເພາະການລະບຸເປັນພາສາຈີນ"
        },
        "returns": "ວັນທີຂອງວັນພັກ"
    },

    "get_user_historical_behaviors": {
        "description": "ດຶງຂໍ້ມູນພື້ນຖານຂອງຜູ້ໃຊ້ ແລະ ຂໍ້ມູນຄວາມມັກພຶດຕິກຳໃນອະດີດ, ລວມທັງລະຫັດຜູ້ໃຊ້, ທີ່ຢູ່ບ້ານ, ທີ່ຢູ່ທີ່ເຮັດວຽກ ແລະ ຂໍ້ມູນພື້ນຖານອື່ນໆ, ພ້ອມທັງນິໄສການໃຊ້ຈ່າຍລະອຽດ, ປະເພດສິນຄ້າທີ່ມັກ, ຊ່ວງລາຄາ, ຂໍ້ກຳນົດການໃຫ້ຄະແນນ, ຄວາມມັກດ້ານເວລາໃນສະຖານະການຕ່າງໆ, ເພື່ອໃຊ້ສຳລັບການແນະນຳສ່ວນບຸກຄົນ ແລະ ການປັບປຸງການບໍລິການ",
        "preconditions": "ດຶງຂໍ້ມູນພຶດຕິກຳໃນອະດີດຂອງຜູ້ໃຊ້",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນພຶດຕິກຳໃນອະດີດຂອງຜູ້ໃຊ້",
        "args": {},
        "returns": "ສະຫຼຸບຂໍ້ມູນພຶດຕິກຳໃນອະດີດຂອງຜູ້ໃຊ້"
    },

    "get_user_all_orders": {
        "description": "ດຶງຂໍ້ມູນຄຳສັ່ງຊື້ທັງໝົດຂອງຜູ້ໃຊ້",
        "preconditions": "ດຶງຂໍ້ມູນຄຳສັ່ງຊື້ທັງໝົດຂອງຜູ້ໃຊ້",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຄຳສັ່ງຊື້ທັງໝົດຂອງຜູ້ໃຊ້",
        "args": {},
        "returns": "ສະຫຼຸບຂໍ້ມູນຄຳສັ່ງຊື້ທັງໝົດຂອງຜູ້ໃຊ້"
    },

    "get_nearby": {
        "description": "ດຶງຂໍ້ມູນຂອງຮ້ານຄ້າ/ສະຖານທີ່ທຸລະກິດທັງໝົດທີ່ຢູ່ໃກ້ຄຽງ",
        "preconditions": "ດຶງຂໍ້ມູນຂອງສະຖານທີ່ທຸລະກິດທັງໝົດ (ຮ້ານຄ້າ, ສະໜາມບິນ ຫຼື ສະຖານີລົດໄຟ, ໂຮງແຮມ, ສະຖານທີ່ທ່ອງທ່ຽວ, ຮ້ານຄ້າຕ່າງໆ ຯລຯ) ພາຍໃນໄລຍະທາງທີ່ກຳນົດ (ແມັດ)",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນສະຖານທີ່ທຸລະກິດ",
        "args": {
            "longitude": "ພິກັດຕາມລວງຍາວ",
            "latitude": "ພິກັດຕາມລວງກວ້າງ",
            "range": "ໄລຍະທາງ (ຫົວໜ່ວຍແມັດ)"
        },
        "returns": "ຂໍ້ມູນຮ້ານຄ້າ/ສະຖານທີ່ທຸລະກິດ"
    },
}

# Tool descriptions - Burmese version
TOOLKIT_TOOL_DESCRIPTIONS_MY = {
    "longitude_latitude_to_distance": {
        "description": "လောင်ဂျီတွဒ်နှင့် လတ္တီတွဒ်အပေါ် အခြေခံ၍ နေရာနှစ်ခုကြား အကွာအဝေးကို တွက်ချက်ပေးသည် (မီတာဖြင့်)",
        "preconditions": "နေရာနှစ်ခု၏ လောင်ဂျီတွဒ်နှင့် လတ္တီတွဒ်အပေါ် အခြေခံ၍ ၎င်းတို့ကြား အကွာအဝေးကို တွက်ချက်သည်",
        "postconditions": "နေရာနှစ်ခုကြား အကွာအဝေးကို ပြန်လည်ပေးပို့သည် (ကိန်းပြည့်၊ မီတာဖြင့်)",
        "args": {
            "longitude1": "ပထမနေရာ၏ လောင်ဂျီတွဒ်",
            "latitude1": "ပထမနေရာ၏ လတ္တီတွဒ်",
            "longitude2": "ဒုတိယနေရာ၏ လောင်ဂျီတွဒ်",
            "latitude2": "ဒုတိယနေရာ၏ လတ္တီတွဒ်"
        },
        "returns": "နေရာနှစ်ခုကြား အကွာအဝေး (ကိန်းပြည့်၊ မီတာဖြင့်)"
    },

    "weather": {
        "description": "သတ်မှတ်ထားသော လိပ်စာတစ်ခုအတွက် date_start မှ date_end ကြားကာလရှိ ရာသီဥတု အချက်အလက်ကို စစ်ဆေးခြင်း",
        "preconditions": "သတ်မှတ်ထားသော လိပ်စာတစ်ခုနှင့် သတ်မှတ်ထားသော ရက်စွဲအပိုင်းအခြားအတွင်းရှိ ရာသီဥတု အချက်အလက်ကို စစ်ဆေးခြင်း",
        "postconditions": "ရာသီဥတု အချက်အလက်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "address": "စစ်ဆေးလိုသော လိပ်စာ",
            "date_start": "စတင်သည့်အချိန်၊ ပုံစံမှာ yyyy-mm-dd ဖြစ်သည်",
            "date_end": "ပြီးဆုံးသည့်အချိန်၊ ပုံစံမှာ yyyy-mm-dd ဖြစ်သည်"
        },
        "returns": "ရာသီဥတု အချက်အလက်"
    },

    "address_to_longitude_latitude": {
        "description": "လိပ်စာအလိုက် လောင်ဂျီတွဒ်နှင့် လတ္တီတွဒ်ကို ရယူခြင်း",
        "preconditions": "လိပ်စာအလိုက် သက်ဆိုင်ရာ လောင်ဂျီတွဒ်နှင့် လတ္တီတွဒ် ကိုဩဒိနိတ်များကို ရယူပါ။",
        "postconditions": "လောင်ဂျီတွဒ်နှင့် လတ္တီတွဒ် ကိုဩဒိနိတ်များကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "address": "စစ်ဆေးမည့် လိပ်စာ"
        },
        "returns": "[လောင်ဂျီတွဒ်, လတ္တီတွဒ်]"
    },

    "get_date_holiday_info": {
        "description": "ရက်စွဲတစ်ခုသည် တရုတ်နိုင်ငံ၏ ရုံးပိတ်ရက်ဖြစ်မဖြစ်ကို စစ်ဆေးပြီး ဖြစ်ပါက ရုံးပိတ်ရက်အမည်ကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "ရက်စွဲအပေါ်အခြေခံ၍ ရုံးပိတ်ရက်ဖြစ်မဖြစ်ကို ဆုံးဖြတ်ပြီး ဖြစ်ပါက ရုံးပိတ်ရက်အမည်ကို ပြန်လည်ပေးပို့ပါ။",
        "postconditions": "ရုံးပိတ်ရက်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "date": "ရက်စွဲ၊ ပုံစံမှာ yyyy-mm-dd ဖြစ်သည်။"
        },
        "returns": "ရုံးပိတ်ရက်အချက်အလက် ဆုံးဖြတ်ချက်ရလဒ်။"
    },

    "get_holiday_date": {
        "description": "သတ်မှတ်ထားသော ခုနှစ်တစ်ခုရှိ အားဖြတ်ရက်တစ်ခုနှင့် ကိုက်ညီသော သီးသန့်ရက်စွဲကို ရယူပါ",
        "preconditions": "သတ်မှတ်ထားသော ခုနှစ်တစ်ခုရှိ အားဖြတ်ရက်တစ်ခု၏ သီးသန့်ရက်စွဲကို ရယူပါ",
        "postconditions": "အားဖြတ်ရက်၏ ရက်စွဲကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "year": "ခုနှစ်",
            "holiday_name": "အားဖြတ်ရက် အမည်၊ တရုတ်စာဖြင့်သာ ရေးသားနိုင်သည်"
        },
        "returns": "အားဖြတ်ရက်၏ ရက်စွဲ"
    },

    "get_user_historical_behaviors": {
        "description": "အသုံးပြုသူ၏ အခြေခံအချက်အလက်များနှင့် သမိုင်းကြောင်းဆိုင်ရာ အပြုအမူ နှစ်သက်မှုဆိုင်ရာ ဒေတာများကို ရယူခြင်း။ ၎င်းတွင် အသုံးပြုသူ အိုင်ဒီ၊ နေအိမ်လိပ်စာ၊ ရုံးလိပ်စာ စသည့် အခြေခံအချက်အလက်များနှင့် မတူညီသော အခြေအနေများရှိ သုံးစွဲမှု အလေ့အထများ၊ နှစ်သက်သော ကဏ္ဍများ၊ ဈေးနှုန်း အတိုင်းအတာများ၊ အမှတ်ပေးမှု လိုအပ်ချက်များ၊ အချိန် နှစ်သက်မှုများ စသည့် အချက်အလက်များ ပါဝင်ပြီး တစ်ဦးချင်းဆိုင်ရာ အကြံပြုချက်များနှင့် ဝန်ဆောင်မှု မြှင့်တင်ရန် အသုံးပြုသည်။",
        "preconditions": "အသုံးပြုသူ၏ သမိုင်းကြောင်းဆိုင်ရာ အပြုအမူ ဒေတာကို ရယူခြင်း။",
        "postconditions": "အသုံးပြုသူ၏ သမိုင်းကြောင်းဆိုင်ရာ အပြုအမူ အချက်အလက်ကို ပြန်လည်ပေးပို့ခြင်း။",
        "args": {},
        "returns": "အသုံးပြုသူ၏ သမိုင်းကြောင်းဆိုင်ရာ အပြုအမူ အချက်အလက် အကျဉ်းချုပ်။"
    },

    "get_user_all_orders": {
        "description": "အသုံးပြုသူ၏ အော်ဒါအားလုံးဆိုင်ရာ အချက်အလက်များကို ရယူခြင်း",
        "preconditions": "အသုံးပြုသူ၏ အော်ဒါအားလုံးဆိုင်ရာ အချက်အလက်များကို ရယူရန်",
        "postconditions": "အသုံးပြုသူ၏ အော်ဒါအားလုံးဆိုင်ရာ အချက်အလက်များကို ပြန်လည်ပေးပို့သည်",
        "args": {},
        "returns": "အသုံးပြုသူ၏ အော်ဒါအားလုံးဆိုင်ရာ အချက်အလက်များ အကျဉ်းချုပ်"
    },

    "get_nearby": {
        "description": "အနီးအနားရှိ ဆိုင်များနှင့် စီးပွားရေးလုပ်ငန်းခွင်များအကြောင်း အချက်အလက်ကို ရယူပါ။",
        "preconditions": "သတ်မှတ်ထားသော အကွာအဝေး (မီတာ) အတွင်းရှိ စီးပွားရေးလုပ်ငန်းခွင်များ (ဆိုင်များ၊ လေဆိပ် သို့မဟုတ် မီးရထားဘူတာများ၊ ဟိုတယ်များ၊ ခရီးသွားဆွဲဆောင်မှုများ၊ ဈေးဆိုင်များ စသည်) အကြောင်း အချက်အလက်ကို ရယူပါ။",
        "postconditions": "စီးပွားရေးလုပ်ငန်းခွင် အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "longitude": "လောင်ဂျီတွဒ်",
            "latitude": "လတ္တီတွဒ်",
            "range": "အကွာအဝေး (မီတာဖြင့်)"
        },
        "returns": "ဆိုင်များ/စီးပွားရေးလုပ်ငန်းခွင်များ အချက်အလက်"
    },
}

# Tool descriptions - Khmer version
TOOLKIT_TOOL_DESCRIPTIONS_KM = {
    "longitude_latitude_to_distance": {
        "description": "គណនាចម្ងាយរវាងចំណុចពីរដោយផ្អែកលើរយៈបណ្តោយ និងរយៈទទឹង (គិតជាម៉ែត្រ)",
        "preconditions": "គណនាចម្ងាយរវាងពួកវាដោយផ្អែកលើរយៈបណ្តោយ និងរយៈទទឹងនៃចំណុចពីរ",
        "postconditions": "ត្រឡប់ចម្ងាយរវាងចំណុចទាំងពីរ (ចំនួនគត់, គិតជាម៉ែត្រ)",
        "args": {
            "longitude1": "រយៈបណ្តោយនៃចំណុចទីមួយ",
            "latitude1": "រយៈទទឹងនៃចំណុចទីមួយ",
            "longitude2": "រយៈបណ្តោយនៃចំណុចទីពីរ",
            "latitude2": "រយៈទទឹងនៃចំណុចទីពីរ"
        },
        "returns": "ចម្ងាយរវាងចំណុចទាំងពីរ (ចំនួនគត់, គិតជាម៉ែត្រ)"
    },

    "weather": {
        "description": "ស្វែងរកព័ត៌មានអាកាសធាតុសម្រាប់អាសយដ្ឋានដែលបានកំណត់ចន្លោះពី date_start ដល់ date_end",
        "preconditions": "ស្វែងរកព័ត៌មានអាកាសធាតុសម្រាប់អាសយដ្ឋានដែលបានកំណត់នៅក្នុងចន្លោះកាលបរិច្ឆេទដែលបានកំណត់",
        "postconditions": "ត្រឡប់ព័ត៌មានអាកាសធាតុ",
        "args": {
            "address": "អាសយដ្ឋានដែលត្រូវស្វែងរក",
            "date_start": "ពេលវេលាចាប់ផ្តើម ទម្រង់គឺ yyyy-mm-dd",
            "date_end": "ពេលវេលាបញ្ចប់ ទម្រង់គឺ yyyy-mm-dd"
        },
        "returns": "ព័ត៌មានអាកាសធាតុ"
    },

    "address_to_longitude_latitude": {
        "description": "ទទួលបានរយៈទទឹង និងរយៈបណ្តោយតាមអាសយដ្ឋាន",
        "preconditions": "ទទួលបានកូអរដោនេរយៈទទឹង និងរយៈបណ្តោយដែលត្រូវគ្នាតាមអាសយដ្ឋាន",
        "postconditions": "ត្រឡប់មកវិញនូវកូអរដោនេរយៈទទឹង និងរយៈបណ្តោយ",
        "args": {
            "address": "អាសយដ្ឋានដែលត្រូវស្វែងរក"
        },
        "returns": "[រយៈបណ្តោយ, រយៈទទឹង]"
    },

    "get_date_holiday_info": {
        "description": "ពិនិត្យមើលថាតើកាលបរិច្ឆេទណាមួយជាថ្ងៃឈប់សម្រាករបស់ចិនឬអត់ ប្រសិនបើជាថ្ងៃឈប់សម្រាក សូមប្រគល់ឈ្មោះថ្ងៃឈប់សម្រាកជាភាសាចិន",
        "preconditions": "ផ្អែកលើកាលបរិច្ឆេទដើម្បីកំណត់ថាតើជាថ្ងៃឈប់សម្រាកឬអត់ ប្រសិនបើមែន សូមប្រគល់ឈ្មោះថ្ងៃឈប់សម្រាក",
        "postconditions": "ប្រគល់ព័ត៌មានអំពីថ្ងៃឈប់សម្រាក",
        "args": {
            "date": "កាលបរិច្ឆេទ ទម្រង់គឺ yyyy-mm-dd"
        },
        "returns": "លទ្ធផលនៃការកំណត់ព័ត៌មានថ្ងៃឈប់សម្រាក"
    },

    "get_holiday_date": {
        "description": "ប្រមូលយកកាលបរិច្ឆេទជាក់លាក់ដែលត្រូវនឹងថ្ងៃឈប់សម្រាកណាមួយក្នុងឆ្នាំដែលបានបញ្ជាក់",
        "preconditions": "ប្រមូលយកកាលបរិច្ឆេទជាក់លាក់នៃថ្ងៃឈប់សម្រាកណាមួយក្នុងឆ្នាំដែលបានបញ្ជាក់",
        "postconditions": "ត្រឡប់មកវិញនូវកាលបរិច្ឆេទនៃថ្ងៃឈប់សម្រាក",
        "args": {
            "year": "ឆ្នាំ",
            "holiday_name": "ឈ្មោះថ្ងៃឈប់សម្រាក គាំទ្រតែការបញ្ជាក់ជាភាសាចិនប៉ុណ្ណោះ"
        },
        "returns": "កាលបរិច្ឆេទនៃថ្ងៃឈប់សម្រាក"
    },

    "get_user_historical_behaviors": {
        "description": "ទទួលបានព័ត៌មានមូលដ្ឋានរបស់អ្នកប្រើប្រាស់ និងទិន្នន័យចំណូលចិត្តនៃអាកប្បកិរិយាប្រវត្តិសាស្ត្រ រួមមានលេខសម្គាល់អ្នកប្រើប្រាស់ អាសយដ្ឋានផ្ទះ អាសយដ្ឋានកន្លែងធ្វើការ និងព័ត៌មានមូលដ្ឋានផ្សេងៗទៀត ព្រមទាំងទម្លាប់ការចំណាយលម្អិត ប្រភេទផលិតផលដែលចូលចិត្ត ចន្លោះតម្លៃ តម្រូវការចំណាត់ថ្នាក់ ចំណូលចិត្តពេលវេលា និងព័ត៌មានផ្សេងៗទៀតនៅក្នុងស្ថានភាពផ្សេងៗ ដើម្បីប្រើប្រាស់សម្រាប់ការណែនាំផ្ទាល់ខ្លួន និងការកែលម្អសេវាកម្ម",
        "preconditions": "ទទួលបានទិន្នន័យអាកប្បកិរិយាប្រវត្តិសាស្ត្ររបស់អ្នកប្រើប្រាស់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានអាកប្បកិរិយាប្រវត្តិសាស្ត្ររបស់អ្នកប្រើប្រាស់",
        "args": {},
        "returns": "សេចក្តីសង្ខេបព័ត៌មានអាកប្បកិរិយាប្រវត្តិសាស្ត្ររបស់អ្នកប្រើប្រាស់"
    },

    "get_user_all_orders": {
        "description": "ទទួលបានព័ត៌មានបញ្ជាទិញទាំងអស់របស់អ្នកប្រើប្រាស់",
        "preconditions": "ទទួលបានព័ត៌មានបញ្ជាទិញទាំងអស់របស់អ្នកប្រើប្រាស់",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានបញ្ជាទិញទាំងអស់របស់អ្នកប្រើប្រាស់",
        "args": {},
        "returns": "សេចក្តីសង្ខេបនៃព័ត៌មានបញ្ជាទិញទាំងអស់របស់អ្នកប្រើប្រាស់"
    },

    "get_nearby": {
        "description": "ទទួលបានព័ត៌មានអំពីហាង ឬកន្លែងអាជីវកម្មទាំងអស់នៅជិតៗ",
        "preconditions": "ទទួលបានព័ត៌មានអំពីកន្លែងអាជីវកម្មទាំងអស់ (ហាង អាកាសយានដ្ឋាន ឬស្ថានីយ៍រថភ្លើង សណ្ឋាគារ កន្លែងទេសចរណ៍ ហាងលក់ដូរ ជាដើម) នៅក្នុងចម្ងាយកំណត់ (គិតជាម៉ែត្រ)",
        "postconditions": "ត្រឡប់ព័ត៌មានកន្លែងអាជីវកម្ម",
        "args": {
            "longitude": "បណ្តោយ",
            "latitude": "ទទឹង",
            "range": "ចម្ងាយ (គិតជាម៉ែត្រ)"
        },
        "returns": "ព័ត៌មានហាង/កន្លែងអាជីវកម្ម"
    },
}

# Tool descriptions - Kazakh version
TOOLKIT_TOOL_DESCRIPTIONS_KK = {
    "longitude_latitude_to_distance": {
        "description": "Ендік және бойлық бойынша екі нүктенің арасындағы қашықтықты есептеу (метрмен)",
        "preconditions": "Екі нүктенің ендік және бойлық мәндері бойынша олардың арасындағы қашықтықты есептеу",
        "postconditions": "Екі нүктенің арасындағы қашықтықты қайтару (бүтін сан, метрмен)",
        "args": {
            "longitude1": "Бірінші нүктенің бойлығы",
            "latitude1": "Бірінші нүктенің ендігі",
            "longitude2": "Екінші нүктенің бойлығы",
            "latitude2": "Екінші нүктенің ендігі"
        },
        "returns": "Екі нүктенің арасындағы қашықтық (бүтін сан, метрмен)"
    },

    "weather": {
        "description": "Көрсетілген мекенжай бойынша date_start пен date_end аралығындағы ауа райы ақпаратын сұрау",
        "preconditions": "Көрсетілген мекенжай бойынша көрсетілген күн аралығындағы ауа райы ақпаратын сұрау",
        "postconditions": "Ауа райы ақпаратын қайтару",
        "args": {
            "address": "Сұралатын мекенжай",
            "date_start": "Басталу уақыты, пішімі yyyy-mm-dd",
            "date_end": "Аяқталу уақыты, пішімі yyyy-mm-dd"
        },
        "returns": "Ауа райы ақпараты"
    },

    "address_to_longitude_latitude": {
        "description": "Мекенжай бойынша ендік пен бойлықты алу",
        "preconditions": "Мекенжай бойынша сәйкес ендік пен бойлық координаттарын алу",
        "postconditions": "Ендік пен бойлық координаттарын қайтару",
        "args": {
            "address": "Ізделетін мекенжай"
        },
        "returns": "[Бойлық, Ендік]"
    },

    "get_date_holiday_info": {
        "description": "Белгілі бір күннің Қытай мерекесі екенін анықтау; егер солай болса, мерекенің қытайша атауын қайтару.",
        "preconditions": "Күнге сәйкес мереке екенін анықтау, егер мереке болса, мереке атауын қайтару.",
        "postconditions": "Мереке туралы ақпаратты қайтару.",
        "args": {
            "date": "Күні, форматы yyyy-mm-dd"
        },
        "returns": "Мереке ақпаратын тексеру нәтижесі."
    },

    "get_holiday_date": {
        "description": "Көрсетілген жылдағы мерекелік күннің нақты датасын алу",
        "preconditions": "Көрсетілген жылдағы мерекелік күннің нақты датасын алу",
        "postconditions": "Мерекелік күннің датасын қайтару",
        "args": {
            "year": "Жыл",
            "holiday_name": "Мереке атауы, тек қытай тіліндегі нұсқасын қолдайды"
        },
        "returns": "Мерекелік күннің датасы"
    },

    "get_user_historical_behaviors": {
        "description": "Пайдаланушының негізгі ақпаратын және тарихи әрекеттер мен таңдаулары туралы деректерді алу, оған пайдаланушы идентификаторы, мекенжайы, жұмыс орны мекенжайы сияқты негізгі ақпараттар, сондай-ақ әртүрлі жағдайлардағы толық тұтыну әдеттері, таңдаулы санаттар, баға аралығы, рейтинг талаптары, уақыт таңдаулары кіреді; жеке ұсыныстар және қызметті оңтайландыру үшін қолданылады.",
        "preconditions": "Пайдаланушының тарихи әрекеттер деректерін алу",
        "postconditions": "Пайдаланушының тарихи әрекеттер ақпаратын қайтару",
        "args": {},
        "returns": "Пайдаланушының тарихи әрекеттер ақпаратының қорытындысы"
    },

    "get_user_all_orders": {
        "description": "Пайдаланушының барлық тапсырыс ақпаратын алу",
        "preconditions": "Пайдаланушының барлық тапсырыс ақпаратын алу",
        "postconditions": "Пайдаланушының барлық тапсырыс ақпаратын қайтару",
        "args": {},
        "returns": "Пайдаланушының барлық тапсырыс ақпаратының қорытындысы"
    },

    "get_nearby": {
        "description": "Жақын маңдағы барлық дүкендер/сауда орындары туралы ақпаратты алу",
        "preconditions": "Белгіленген ауқымдағы (метрмен) барлық сауда орындары (дүкендер, әуежай немесе теміржол вокзалы, қонақүйлер, көрікті жерлер, дүкендер және т.б.) туралы ақпаратты алу",
        "postconditions": "Сауда орындары туралы ақпаратты қайтару",
        "args": {
            "longitude": "Бойлық",
            "latitude": "Ендік",
            "range": "Ауқым (метрмен)"
        },
        "returns": "Дүкен/сауда орындары туралы ақпарат"
    },
}

# Tool descriptions - Punjabi version
TOOLKIT_TOOL_DESCRIPTIONS_PA = {
    "longitude_latitude_to_distance": {
        "description": "ਅਕਸ਼ਾਂਸ਼ ਅਤੇ ਰੇਖਾਂਸ਼ ਦੇ ਅਧਾਰ ਤੇ ਦੋ ਬਿੰਦੂਆਂ ਵਿਚਕਾਰ ਦੂਰੀ (ਮੀਟਰਾਂ ਵਿੱਚ) ਦੀ ਗਣਨਾ ਕਰੋ",
        "preconditions": "ਦੋ ਬਿੰਦੂਆਂ ਦੇ ਅਕਸ਼ਾਂਸ਼ ਅਤੇ ਰੇਖਾਂਸ਼ ਦੇ ਅਧਾਰ ਤੇ ਉਹਨਾਂ ਵਿਚਕਾਰ ਦੂਰੀ ਦੀ ਗਣਨਾ ਕਰੋ",
        "postconditions": "ਦੋ ਬਿੰਦੂਆਂ ਵਿਚਕਾਰ ਦੂਰੀ ਵਾਪਸ ਕਰੋ (ਪੂਰਨ ਅੰਕ, ਮੀਟਰਾਂ ਵਿੱਚ)",
        "args": {
            "longitude1": "ਪਹਿਲੇ ਬਿੰਦੂ ਦਾ ਰੇਖਾਂਸ਼",
            "latitude1": "ਪਹਿਲੇ ਬਿੰਦੂ ਦਾ ਅਕਸ਼ਾਂਸ਼",
            "longitude2": "ਦੂਜੇ ਬਿੰਦੂ ਦਾ ਰੇਖਾਂਸ਼",
            "latitude2": "ਦੂਜੇ ਬਿੰਦੂ ਦਾ ਅਕਸ਼ਾਂਸ਼"
        },
        "returns": "ਦੋ ਬਿੰਦੂਆਂ ਵਿਚਕਾਰ ਦੂਰੀ (ਪੂਰਨ ਅੰਕ, ਮੀਟਰਾਂ ਵਿੱਚ)"
    },

    "weather": {
        "description": "date_start ਤੋਂ date_end ਤੱਕ ਨਿਰਧਾਰਤ ਪਤੇ ਲਈ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਨਿਰਧਾਰਤ ਪਤੇ ਅਤੇ ਨਿਰਧਾਰਤ ਤਾਰੀਖ ਰੇਂਜ ਲਈ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ ਪੁੱਛੋ",
        "postconditions": "ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "address": "ਪੁੱਛਗੱਛ ਕਰਨ ਲਈ ਪਤਾ",
            "date_start": "ਸ਼ੁਰੂਆਤੀ ਸਮਾਂ, ਫਾਰਮੈਟ yyyy-mm-dd ਹੈ",
            "date_end": "ਸਮਾਪਤੀ ਸਮਾਂ, ਫਾਰਮੈਟ yyyy-mm-dd ਹੈ"
        },
        "returns": "ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ"
    },

    "address_to_longitude_latitude": {
        "description": "ਪਤੇ ਦੇ ਆਧਾਰ 'ਤੇ ਲੈਟੀਟਿਊਡ ਅਤੇ ਲੌਂਗੀਟਿਊਡ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਪਤੇ ਦੇ ਆਧਾਰ 'ਤੇ ਸੰਬੰਧਿਤ ਲੈਟੀਟਿਊਡ ਅਤੇ ਲੌਂਗੀਟਿਊਡ ਨਿਰਦੇਸ਼ਾਂਕ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਲੈਟੀਟਿਊਡ ਅਤੇ ਲੌਂਗੀਟਿਊਡ ਨਿਰਦੇਸ਼ਾਂਕ ਵਾਪਸ ਕਰੋ",
        "args": {
            "address": "ਖੋਜਣ ਲਈ ਪਤਾ"
        },
        "returns": "[ਲੌਂਗੀਟਿਊਡ, ਲੈਟੀਟਿਊਡ]"
    },

    "get_date_holiday_info": {
        "description": "ਕਿਸੇ ਮਿਤੀ ਦੀ ਜਾਂਚ ਕਰੋ ਕਿ ਕੀ ਇਹ ਚੀਨੀ ਛੁੱਟੀ ਹੈ; ਜੇਕਰ ਹਾਂ, ਤਾਂ ਛੁੱਟੀ ਦਾ ਚੀਨੀ ਨਾਮ ਵਾਪਸ ਕਰੋ।",
        "preconditions": "ਮਿਤੀ ਦੇ ਆਧਾਰ 'ਤੇ ਜਾਂਚ ਕਰੋ ਕਿ ਕੀ ਇਹ ਛੁੱਟੀ ਹੈ, ਜੇਕਰ ਹਾਂ ਤਾਂ ਛੁੱਟੀ ਦਾ ਨਾਮ ਵਾਪਸ ਕਰੋ।",
        "postconditions": "ਛੁੱਟੀ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "date": "ਮਿਤੀ, ਫਾਰਮੈਟ yyyy-mm-dd ਹੈ।"
        },
        "returns": "ਛੁੱਟੀ ਦੀ ਜਾਣਕਾਰੀ ਦਾ ਨਤੀਜਾ।"
    },

    "get_holiday_date": {
        "description": "ਕਿਸੇ ਨਿਰਧਾਰਤ ਸਾਲ ਵਿੱਚ ਕਿਸੇ ਖਾਸ ਛੁੱਟੀ ਦੀ ਸਹੀ ਤਾਰੀਖ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਕਿਸੇ ਨਿਰਧਾਰਤ ਸਾਲ ਵਿੱਚ ਕਿਸੇ ਖਾਸ ਛੁੱਟੀ ਦੀ ਸਹੀ ਤਾਰੀਖ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਛੁੱਟੀ ਦੀ ਤਾਰੀਖ ਵਾਪਸ ਕਰੋ",
        "args": {
            "year": "ਸਾਲ",
            "holiday_name": "ਛੁੱਟੀ ਦਾ ਨਾਮ, ਸਿਰਫ ਚੀਨੀ ਭਾਸ਼ਾ ਸਮਰਥਿਤ ਹੈ"
        },
        "returns": "ਛੁੱਟੀ ਦੀ ਤਾਰੀਖ"
    },

    "get_user_historical_behaviors": {
        "description": "ਵਰਤੋਂਕਾਰ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਅਤੇ ਇਤਿਹਾਸਕ ਵਿਵਹਾਰ ਪਸੰਦੀਦਗੀ ਡੇਟਾ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਵਰਤੋਂਕਾਰ ID, ਘਰ ਦਾ ਪਤਾ, ਕੰਮ ਦਾ ਪਤਾ ਆਦਿ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਹੈ, ਅਤੇ ਨਾਲ ਹੀ ਵੱਖ-ਵੱਖ ਸਥਿਤੀਆਂ ਵਿੱਚ ਵਿਸਤ੍ਰਿਤ ਖਪਤ ਆਦਤਾਂ, ਪਸੰਦੀਦਾ ਵਰਗ, ਕੀਮਤ ਰੇਂਜ, ਰੇਟਿੰਗ ਲੋੜਾਂ, ਸਮੇਂ ਦੀ ਪਸੰਦ ਆਦਿ ਜਾਣਕਾਰੀ ਸ਼ਾਮਲ ਹੈ, ਜੋ ਵਿਅਕਤੀਗਤ ਸਿਫਾਰਸ਼ ਅਤੇ ਸੇਵਾ ਅਨੁਕੂਲਨ ਲਈ ਵਰਤੀ ਜਾਂਦੀ ਹੈ।",
        "preconditions": "ਵਰਤੋਂਕਾਰ ਦੇ ਇਤਿਹਾਸਕ ਵਿਵਹਾਰ ਡੇਟਾ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਵਰਤੋਂਕਾਰ ਦੀ ਇਤਿਹਾਸਕ ਵਿਵਹਾਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {},
        "returns": "ਵਰਤੋਂਕਾਰ ਦੀ ਇਤਿਹਾਸਕ ਵਿਵਹਾਰ ਜਾਣਕਾਰੀ ਦਾ ਸਾਰ"
    },

    "get_user_all_orders": {
        "description": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਆਰਡਰ ਜਾਣਕਾਰੀਆਂ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਆਰਡਰ ਜਾਣਕਾਰੀਆਂ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਆਰਡਰ ਜਾਣਕਾਰੀਆਂ ਵਾਪਸ ਕਰੋ",
        "args": {},
        "returns": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਾਰੀਆਂ ਆਰਡਰ ਜਾਣਕਾਰੀਆਂ ਦਾ ਸਾਰ"
    },

    "get_nearby": {
        "description": "ਨੇੜੇ ਦੇ ਸਾਰੇ ਦੁਕਾਨਾਂ/ਵਪਾਰਕ ਸਥਾਨਾਂ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ",
        "preconditions": "ਨਿਰਧਾਰਤ ਸੀਮਾ (ਮੀਟਰਾਂ ਵਿੱਚ) ਦੇ ਅੰਦਰ ਸਾਰੇ ਵਪਾਰਕ ਸਥਾਨਾਂ (ਦੁਕਾਨਾਂ, ਹਵਾਈ ਅੱਡੇ ਜਾਂ ਰੇਲਵੇ ਸਟੇਸ਼ਨ, ਹੋਟਲ, ਆਕਰਸ਼ਣ, ਸਟੋਰ ਆਦਿ) ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ",
        "postconditions": "ਵਪਾਰਕ ਸਥਾਨ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ",
        "args": {
            "longitude": "ਰੇਖਾਂਸ਼",
            "latitude": "ਅਕਸ਼ਾਂਸ਼",
            "range": "ਸੀਮਾ (ਮੀਟਰਾਂ ਵਿੱਚ)"
        },
        "returns": "ਦੁਕਾਨ/ਵਪਾਰਕ ਸਥਾਨ ਜਾਣਕਾਰੀ"
    },
}

# Tool descriptions - Belarusian version
TOOLKIT_TOOL_DESCRIPTIONS_BE = {
    "longitude_latitude_to_distance": {
        "description": "Вылічае адлегласць паміж двума кропкамі на аснове даўготы і шыраты (у метрах)",
        "preconditions": "Вылічае адлегласць паміж двума кропкамі на аснове іх даўготы і шыраты",
        "postconditions": "Вяртае адлегласць паміж двума кропкамі (цэлы лік, у метрах)",
        "args": {
            "longitude1": "Даўгата першай кропкі",
            "latitude1": "Шырата першай кропкі",
            "longitude2": "Даўгата другой кропкі",
            "latitude2": "Шырата другой кропкі"
        },
        "returns": "Адлегласць паміж двума кропкамі (цэлы лік, у метрах)"
    },

    "weather": {
        "description": "Запытаць інфармацыю пра надвор'е для ўказанага адрасу ў перыяд з date_start па date_end",
        "preconditions": "Запытаць інфармацыю пра надвор'е для ўказанага адрасу ў зададзеным дыяпазоне дат",
        "postconditions": "Вярнуць інфармацыю пра надвор'е",
        "args": {
            "address": "Адрас для запыту",
            "date_start": "Час пачатку, фармат yyyy-mm-dd",
            "date_end": "Час заканчэння, фармат yyyy-mm-dd"
        },
        "returns": "Інфармацыя пра надвор'е"
    },

    "address_to_longitude_latitude": {
        "description": "Атрымаць шырату і даўгату па адрасе",
        "preconditions": "Атрымаць адпаведныя каардынаты шыраты і даўгаты па адрасе",
        "postconditions": "Вяртае каардынаты шыраты і даўгаты",
        "args": {
            "address": "Адрас для запыту"
        },
        "returns": "[Даўгата, Шырата]"
    },

    "get_date_holiday_info": {
        "description": "Вызначыць, ці з'яўляецца пэўная дата кітайскім святам; калі так, вярнуць назву свята на кітайскай мове",
        "preconditions": "Праверыць па даце, ці з'яўляецца яна святам, і калі так, вярнуць назву свята",
        "postconditions": "Вярнуць інфармацыю пра свята",
        "args": {
            "date": "Дата, фармат yyyy-mm-dd"
        },
        "returns": "Вынік праверкі інфармацыі пра свята"
    },

    "get_holiday_date": {
        "description": "Атрымаць канкрэтную дату, якая адпавядае пэўнаму святу ў указаным годзе",
        "preconditions": "Атрымаць канкрэтную дату пэўнага свята ў указаным годзе",
        "postconditions": "Вяртае дату свята",
        "args": {
            "year": "Год",
            "holiday_name": "Назва свята, падтрымліваецца толькі кітайская мова"
        },
        "returns": "Дата свята"
    },

    "get_user_historical_behaviors": {
        "description": "Атрыманне асноўнай інфармацыі пра карыстальніка і даных пра гістарычныя паводзіны і перавагі, уключаючы ідэнтыфікатар карыстальніка, хатні адрас, працоўны адрас і іншую асноўную інфармацыю, а таксама дэталёвыя звычкі спажывання, пераважныя катэгорыі, цэнавыя дыяпазоны, патрабаванні да рэйтынгу, часовыя перавагі ў розных сцэнарыях і іншую інфармацыю, якая выкарыстоўваецца для персаналізаваных рэкамендацый і аптымізацыі сэрвісу",
        "preconditions": "Атрыманне даных пра гістарычныя паводзіны карыстальніка",
        "postconditions": "Вяртанне інфармацыі пра гістарычныя паводзіны карыстальніка",
        "args": {},
        "returns": "Зводка інфармацыі пра гістарычныя паводзіны карыстальніка"
    },

    "get_user_all_orders": {
        "description": "Атрымаць інфармацыю аб усіх заказах карыстальніка",
        "preconditions": "Атрымаць інфармацыю аб усіх заказах карыстальніка",
        "postconditions": "Вярнуць інфармацыю аб усіх заказах карыстальніка",
        "args": {},
        "returns": "Зводка інфармацыі аб усіх заказах карыстальніка"
    },

    "get_nearby": {
        "description": "Атрымаць інфармацыю пра ўсе крамы/камерцыйныя аб'екты побач",
        "preconditions": "Атрымаць інфармацыю пра ўсе камерцыйныя аб'екты (крамы, аэрапорты або чыгуначныя вакзалы, гатэлі, славутасці, гандлёвыя кропкі і г.д.) у зададзеным дыяпазоне (метры)",
        "postconditions": "Вяртае інфармацыю пра камерцыйныя аб'екты",
        "args": {
            "longitude": "Даўгата",
            "latitude": "Шырата",
            "range": "Дыяпазон (у метрах)"
        },
        "returns": "Інфармацыя пра крамы/камерцыйныя аб'екты"
    },
}

# Tool descriptions - Malay version
TOOLKIT_TOOL_DESCRIPTIONS_MS = {
    "longitude_latitude_to_distance": {
        "description": "Kira jarak antara dua titik berdasarkan longitud dan latitud (dalam meter)",
        "preconditions": "Kira jarak antara keduanya berdasarkan longitud dan latitud dua titik",
        "postconditions": "Memulangkan jarak antara dua titik (nombor bulat, dalam meter)",
        "args": {
            "longitude1": "Longitud titik pertama",
            "latitude1": "Latitud titik pertama",
            "longitude2": "Longitud titik kedua",
            "latitude2": "Latitud titik kedua"
        },
        "returns": "Jarak antara dua titik (nombor bulat, dalam meter)"
    },

    "weather": {
        "description": "Semak maklumat cuaca untuk alamat tertentu dalam tempoh dari date_start hingga date_end",
        "preconditions": "Semak maklumat cuaca untuk alamat tertentu dalam julat tarikh yang ditentukan",
        "postconditions": "Memulangkan maklumat cuaca",
        "args": {
            "address": "Alamat yang hendak disemak",
            "date_start": "Masa mula, format yyyy-mm-dd",
            "date_end": "Masa tamat, format yyyy-mm-dd"
        },
        "returns": "Maklumat cuaca"
    },

    "address_to_longitude_latitude": {
        "description": "Dapatkan longitud dan latitud berdasarkan alamat",
        "preconditions": "Dapatkan koordinat longitud dan latitud yang sepadan berdasarkan alamat",
        "postconditions": "Memulangkan koordinat longitud dan latitud",
        "args": {
            "address": "Alamat yang ingin dicari"
        },
        "returns": "[Longitud, Latitud]"
    },

    "get_date_holiday_info": {
        "description": "Menentukan sama ada tarikh tertentu adalah cuti umum di China; jika ya, pulangkan nama cuti tersebut dalam bahasa Cina",
        "preconditions": "Menentukan sama ada ia adalah cuti umum berdasarkan tarikh, jika ya pulangkan nama cuti tersebut",
        "postconditions": "Memulangkan maklumat cuti umum",
        "args": {
            "date": "Tarikh, format ialah yyyy-mm-dd"
        },
        "returns": "Keputusan penilaian maklumat cuti umum"
    },

    "get_holiday_date": {
        "description": "Mendapatkan tarikh spesifik bagi hari cuti tertentu dalam tahun yang ditentukan",
        "preconditions": "Mendapatkan tarikh spesifik bagi hari cuti tertentu dalam tahun yang ditentukan",
        "postconditions": "Memulangkan tarikh hari cuti",
        "args": {
            "year": "Tahun",
            "holiday_name": "Nama hari cuti, hanya menyokong ungkapan dalam bahasa Cina"
        },
        "returns": "Tarikh hari cuti"
    },

    "get_user_historical_behaviors": {
        "description": "Dapatkan maklumat asas pengguna dan data keutamaan sejarah tingkah laku, termasuk ID pengguna, alamat rumah, alamat kerja dan maklumat asas lain, serta tabiat perbelanjaan terperinci, kategori kegemaran, julat harga, keperluan penilaian, keutamaan masa dalam pelbagai senario, digunakan untuk cadangan diperibadikan dan pengoptimuman perkhidmatan",
        "preconditions": "Dapatkan data sejarah tingkah laku pengguna",
        "postconditions": "Kembalikan maklumat sejarah tingkah laku pengguna",
        "args": {},
        "returns": "Ringkasan maklumat sejarah tingkah laku pengguna"
    },

    "get_user_all_orders": {
        "description": "Dapatkan semua maklumat pesanan pengguna",
        "preconditions": "Dapatkan semua maklumat pesanan pengguna",
        "postconditions": "Mengembalikan semua maklumat pesanan pengguna",
        "args": {},
        "returns": "Ringkasan semua maklumat pesanan pengguna"
    },

    "get_nearby": {
        "description": "Dapatkan maklumat semua kedai/tempat perniagaan berhampiran",
        "preconditions": "Dapatkan maklumat semua tempat perniagaan dalam jarak yang ditentukan (meter) (kedai, lapangan terbang atau stesen kereta api, hotel, tempat menarik, kedai, dll.)",
        "postconditions": "Memulangkan maklumat tempat perniagaan",
        "args": {
            "longitude": "Longitud",
            "latitude": "Latitud",
            "range": "Jarak (dalam meter)"
        },
        "returns": "Maklumat kedai/tempat perniagaan"
    },
}

# Tool descriptions - Vietnamese version
TOOLKIT_TOOL_DESCRIPTIONS_VI = {
    "longitude_latitude_to_distance": {
        "description": "Tính khoảng cách giữa hai điểm dựa trên kinh độ và vĩ độ (đơn vị mét)",
        "preconditions": "Tính khoảng cách giữa chúng dựa trên kinh độ và vĩ độ của hai điểm",
        "postconditions": "Trả về khoảng cách giữa hai điểm (số nguyên, đơn vị mét)",
        "args": {
            "longitude1": "Kinh độ của điểm thứ nhất",
            "latitude1": "Vĩ độ của điểm thứ nhất",
            "longitude2": "Kinh độ của điểm thứ hai",
            "latitude2": "Vĩ độ của điểm thứ hai"
        },
        "returns": "Khoảng cách giữa hai điểm (số nguyên, đơn vị mét)"
    },

    "weather": {
        "description": "Truy vấn thông tin thời tiết tại địa chỉ cụ thể trong khoảng thời gian từ date_start đến date_end",
        "preconditions": "Truy vấn thông tin thời tiết tại địa chỉ cụ thể trong phạm vi ngày đã chỉ định",
        "postconditions": "Trả về thông tin thời tiết",
        "args": {
            "address": "Địa chỉ cần truy vấn",
            "date_start": "Thời gian bắt đầu, định dạng yyyy-mm-dd",
            "date_end": "Thời gian kết thúc, định dạng yyyy-mm-dd"
        },
        "returns": "Thông tin thời tiết"
    },

    "address_to_longitude_latitude": {
        "description": "Lấy kinh độ và vĩ độ dựa trên địa chỉ",
        "preconditions": "Lấy tọa độ kinh độ và vĩ độ tương ứng dựa trên địa chỉ",
        "postconditions": "Trả về tọa độ kinh độ và vĩ độ",
        "args": {
            "address": "Địa chỉ cần truy vấn"
        },
        "returns": "[Kinh độ, Vĩ độ]"
    },

    "get_date_holiday_info": {
        "description": "Xác định xem một ngày cụ thể có phải là ngày lễ Trung Quốc hay không; nếu có thì trả về tên tiếng Trung của ngày lễ đó",
        "preconditions": "Xác định xem có phải là ngày lễ hay không dựa trên ngày, nếu có thì trả về tên ngày lễ",
        "postconditions": "Trả về thông tin ngày lễ",
        "args": {
            "date": "Ngày, định dạng yyyy-mm-dd"
        },
        "returns": "Kết quả xác định thông tin ngày lễ"
    },

    "get_holiday_date": {
        "description": "Lấy ngày cụ thể tương ứng với một ngày lễ nhất định trong năm được chỉ định",
        "preconditions": "Lấy ngày cụ thể của một ngày lễ nhất định trong năm được chỉ định",
        "postconditions": "Trả về ngày của ngày lễ",
        "args": {
            "year": "Năm",
            "holiday_name": "Tên ngày lễ, chỉ hỗ trợ biểu diễn bằng tiếng Trung"
        },
        "returns": "Ngày của ngày lễ"
    },

    "get_user_historical_behaviors": {
        "description": "Lấy thông tin cơ bản và dữ liệu sở thích hành vi lịch sử của người dùng, bao gồm ID người dùng, địa chỉ nhà, địa chỉ làm việc và các thông tin cơ bản khác, cũng như thói quen tiêu dùng chi tiết, danh mục ưa thích, khoảng giá, yêu cầu đánh giá, sở thích thời gian trong các kịch bản khác nhau, dùng cho khuyến nghị cá nhân hóa và tối ưu hóa dịch vụ",
        "preconditions": "Lấy dữ liệu hành vi lịch sử của người dùng",
        "postconditions": "Trả về thông tin hành vi lịch sử của người dùng",
        "args": {},
        "returns": "Tóm tắt thông tin hành vi lịch sử của người dùng"
    },

    "get_user_all_orders": {
        "description": "Lấy tất cả thông tin đơn hàng của người dùng",
        "preconditions": "Lấy tất cả thông tin đơn hàng của người dùng",
        "postconditions": "Trả về tất cả thông tin đơn hàng của người dùng",
        "args": {},
        "returns": "Tóm tắt tất cả thông tin đơn hàng của người dùng"
    },

    "get_nearby": {
        "description": "Lấy thông tin về tất cả các cửa hàng/địa điểm thương mại lân cận",
        "preconditions": "Lấy thông tin về tất cả các địa điểm thương mại (cửa hàng, sân bay hoặc ga tàu, khách sạn, điểm tham quan, cơ sở kinh doanh, v.v.) trong phạm vi chỉ định (tính bằng mét)",
        "postconditions": "Trả về thông tin địa điểm thương mại",
        "args": {
            "longitude": "Kinh độ",
            "latitude": "Vĩ độ",
            "range": "Phạm vi (tính bằng mét)"
        },
        "returns": "Thông tin cửa hàng/địa điểm thương mại"
    },
}

# Tool descriptions - Turkish version
TOOLKIT_TOOL_DESCRIPTIONS_TR = {
    "longitude_latitude_to_distance": {
        "description": "Enlem ve boylama göre iki nokta arasındaki mesafeyi hesaplar (metre cinsinden)",
        "preconditions": "İki noktanın enlem ve boylamına göre aralarındaki mesafeyi hesaplar",
        "postconditions": "İki nokta arasındaki mesafeyi döndürür (tamsayı, metre cinsinden)",
        "args": {
            "longitude1": "İlk noktanın boylamı",
            "latitude1": "İlk noktanın enlemi",
            "longitude2": "İkinci noktanın boylamı",
            "latitude2": "İkinci noktanın enlemi"
        },
        "returns": "İki nokta arasındaki mesafe (tamsayı, metre cinsinden)"
    },

    "weather": {
        "description": "Belirtilen adres için date_start ile date_end arasındaki hava durumu bilgilerini sorgular",
        "preconditions": "Belirtilen adres için belirtilen tarih aralığında hava durumu bilgilerini sorgular",
        "postconditions": "Hava durumu bilgilerini döndürür",
        "args": {
            "address": "Sorgulanacak adres",
            "date_start": "Başlangıç tarihi, format: yyyy-mm-dd",
            "date_end": "Bitiş tarihi, format: yyyy-mm-dd"
        },
        "returns": "Hava durumu bilgileri"
    },

    "address_to_longitude_latitude": {
        "description": "Adrese göre enlem ve boylam alma",
        "preconditions": "Adrese göre ilgili enlem ve boylam koordinatlarını alma",
        "postconditions": "Enlem ve boylam koordinatlarını döndürür",
        "args": {
            "address": "Sorgulanacak adres"
        },
        "returns": "[Boylam, Enlem]"
    },

    "get_date_holiday_info": {
        "description": "Belirli bir tarihin Çin tatili olup olmadığını kontrol eder; eğer öyleyse tatilin Çince adını döndürür.",
        "preconditions": "Tarihe göre tatil olup olmadığına karar verir, eğer tatil ise tatil adını döndürür.",
        "postconditions": "Tatil bilgilerini döndürür.",
        "args": {
            "date": "Tarih, yyyy-mm-dd formatında."
        },
        "returns": "Tatil bilgisi kontrol sonucu."
    },

    "get_holiday_date": {
        "description": "Belirtilen yıldaki belirli bir tatil gününün tarihini alır",
        "preconditions": "Belirtilen yıldaki belirli bir tatil gününün tarihini alır",
        "postconditions": "Tatil gününün tarihini döndürür",
        "args": {
            "year": "Yıl",
            "holiday_name": "Tatil gününün adı, yalnızca Çince ifadeyi destekler"
        },
        "returns": "Tatil gününün tarihi"
    },

    "get_user_historical_behaviors": {
        "description": "Kullanıcı temel bilgilerini ve geçmiş davranış tercih verilerini alır, kullanıcı kimliği, ev adresi, iş adresi gibi temel bilgilerin yanı sıra çeşitli senaryolardaki detaylı tüketim alışkanlıkları, tercih edilen kategoriler, fiyat aralıkları, puanlama gereksinimleri, zaman tercihleri gibi bilgileri içerir ve kişiselleştirilmiş öneri ile hizmet optimizasyonu için kullanılır",
        "preconditions": "Kullanıcı geçmiş davranış verilerini alır",
        "postconditions": "Kullanıcı geçmiş davranış bilgilerini döndürür",
        "args": {},
        "returns": "Kullanıcı geçmiş davranış bilgileri özeti"
    },

    "get_user_all_orders": {
        "description": "Kullanıcının tüm sipariş bilgilerini getir",
        "preconditions": "Kullanıcının tüm sipariş bilgilerini getir",
        "postconditions": "Kullanıcının tüm sipariş bilgilerini döndürür",
        "args": {},
        "returns": "Kullanıcının tüm sipariş bilgilerinin özeti"
    },

    "get_nearby": {
        "description": "Yakındaki tüm mağazaların ve ticari mekanların bilgilerini alın",
        "preconditions": "Belirtilen menzil içindeki (metre cinsinden) tüm ticari mekanların (mağazalar, havaalanları veya tren istasyonları, oteller, turistik yerler, dükkanlar vb.) bilgilerini alın",
        "postconditions": "Ticari mekan bilgilerini döndürür",
        "args": {
            "longitude": "Boylam",
            "latitude": "Enlem",
            "range": "Menzil (metre cinsinden)"
        },
        "returns": "Mağaza/ticari mekan bilgileri"
    },
}

# Tool descriptions - Hebrew version
TOOLKIT_TOOL_DESCRIPTIONS_HE = {
    "longitude_latitude_to_distance": {
        "description": "חישוב המרחק בין שתי נקודות על בסיס קווי אורך ורוחב (במטרים)",
        "preconditions": "חישוב המרחק ביניהן על בסיס קווי האורך והרוחב של שתי הנקודות",
        "postconditions": "מחזיר את המרחק בין שתי הנקודות (מספר שלם, במטרים)",
        "args": {
            "longitude1": "קו האורך של הנקודה הראשונה",
            "latitude1": "קו הרוחב של הנקודה הראשונה",
            "longitude2": "קו האורך של הנקודה השנייה",
            "latitude2": "קו הרוחב של הנקודה השנייה"
        },
        "returns": "המרחק בין שתי הנקודות (מספר שלם, במטרים)"
    },

    "weather": {
        "description": "שאילת מידע מזג אוויר עבור כתובת נתונה בתקופה שבין date_start ל-date_end",
        "preconditions": "שאילת מידע מזג אוויר עבור כתובת נתונה בטווח תאריכים נתון",
        "postconditions": "מחזיר מידע מזג אוויר",
        "args": {
            "address": "הכתובת לשאילתה",
            "date_start": "זמן התחלה, בפורמט yyyy-mm-dd",
            "date_end": "זמן סיום, בפורמט yyyy-mm-dd"
        },
        "returns": "מידע מזג אוויר"
    },

    "address_to_longitude_latitude": {
        "description": "קבלת קווי רוחב ואורך בהתבסס על כתובת",
        "preconditions": "קבלת קואורדינטות של קו רוחב וקו אורך המתאימות לכתובת",
        "postconditions": "החזרת קואורדינטות של קו רוחב וקו אורך",
        "args": {
            "address": "הכתובת לחיפוש"
        },
        "returns": "[קו אורך, קו רוחב]"
    },

    "get_date_holiday_info": {
        "description": "בודק האם תאריך מסוים הוא חג סיני; אם כן, מחזיר את השם הסיני של החג",
        "preconditions": "בודק על בסיס התאריך אם מדובר בחג, אם כן מחזיר את שם החג",
        "postconditions": "מחזיר מידע על החג",
        "args": {
            "date": "תאריך, בפורמט yyyy-mm-dd"
        },
        "returns": "תוצאת בדיקת מידע החג"
    },

    "get_holiday_date": {
        "description": "קבלת התאריך המדויק של חג מסוים בשנה נתונה",
        "preconditions": "קבלת התאריך המדויק של חג מסוים בשנה נתונה",
        "postconditions": "מחזיר את תאריך החג",
        "args": {
            "year": "שנה",
            "holiday_name": "שם החג, תומך רק בניסוח בסינית"
        },
        "returns": "תאריך החג"
    },

    "get_user_historical_behaviors": {
        "description": "קבלת מידע בסיסי על המשתמש ונתוני העדפות התנהגות היסטוריים, כולל מזהה משתמש, כתובת בית, כתובת עבודה ומידע בסיסי אחר, וכן הרגלי צריכה מפורטים, קטגוריות מועדפות, טווחי מחירים, דרישות דירוג, העדפות זמן וכדומה בתרחישים שונים, המשמשים להמלצה אישית ושיפור השירות",
        "preconditions": "קבלת נתוני התנהגות היסטוריים של המשתמש",
        "postconditions": "החזרת מידע על התנהגות היסטורית של המשתמש",
        "args": {},
        "returns": "סיכום מידע על התנהגות היסטורית של המשתמש"
    },

    "get_user_all_orders": {
        "description": "קבלת כל פרטי ההזמנות של המשתמש",
        "preconditions": "קבלת כל פרטי ההזמנות של המשתמש",
        "postconditions": "החזרת כל פרטי ההזמנות של המשתמש",
        "args": {},
        "returns": "סיכום כל פרטי ההזמנות של המשתמש"
    },

    "get_nearby": {
        "description": "קבלת מידע על כל החנויות והמקומות העסקיים הסמוכים",
        "preconditions": "קבלת מידע על כל המקומות העסקיים (חנויות, שדות תעופה או תחנות רכבת, מלונות, אטרקציות, חנויות וכו׳) בטווח מוגדר (מטרים)",
        "postconditions": "מחזיר מידע על מקומות עסקיים",
        "args": {
            "longitude": "קו אורך",
            "latitude": "קו רוחב",
            "range": "טווח (במטרים)"
        },
        "returns": "מידע על חנויות/מקומות עסקיים"
    },
}

# Tool descriptions - Indonesian version
TOOLKIT_TOOL_DESCRIPTIONS_ID = {
    "longitude_latitude_to_distance": {
        "description": "Menghitung jarak antara dua titik berdasarkan bujur dan lintang (dalam meter)",
        "preconditions": "Menghitung jarak antara dua titik berdasarkan bujur dan lintang mereka",
        "postconditions": "Mengembalikan jarak antara dua titik (bilangan bulat, dalam meter)",
        "args": {
            "longitude1": "Bujur titik pertama",
            "latitude1": "Lintang titik pertama",
            "longitude2": "Bujur titik kedua",
            "latitude2": "Lintang titik kedua"
        },
        "returns": "Jarak antara dua titik (bilangan bulat, dalam meter)"
    },

    "weather": {
        "description": "Memeriksa informasi cuaca untuk alamat tertentu dalam periode dari date_start hingga date_end",
        "preconditions": "Memeriksa informasi cuaca untuk alamat tertentu dalam rentang tanggal yang ditentukan",
        "postconditions": "Mengembalikan informasi cuaca",
        "args": {
            "address": "Alamat yang akan diperiksa",
            "date_start": "Waktu mulai, format yyyy-mm-dd",
            "date_end": "Waktu akhir, format yyyy-mm-dd"
        },
        "returns": "Informasi cuaca"
    },

    "address_to_longitude_latitude": {
        "description": "Dapatkan koordinat lintang dan bujur berdasarkan alamat",
        "preconditions": "Dapatkan koordinat lintang dan bujur yang sesuai berdasarkan alamat",
        "postconditions": "Kembalikan koordinat lintang dan bujur",
        "args": {
            "address": "Alamat yang ingin dicari"
        },
        "returns": "[Bujur, Lintang]"
    },

    "get_date_holiday_info": {
        "description": "Menentukan apakah suatu tanggal adalah hari libur Tiongkok; jika ya, kembalikan nama hari libur dalam bahasa Tiongkok",
        "preconditions": "Menentukan apakah merupakan hari libur berdasarkan tanggal, jika ya maka kembalikan nama hari libur",
        "postconditions": "Mengembalikan informasi hari libur",
        "args": {
            "date": "Tanggal, format yyyy-mm-dd"
        },
        "returns": "Hasil penilaian informasi hari libur"
    },

    "get_holiday_date": {
        "description": "Mengambil tanggal spesifik untuk hari libur tertentu pada tahun yang ditentukan",
        "preconditions": "Mengambil tanggal spesifik untuk hari libur tertentu pada tahun yang ditentukan",
        "postconditions": "Mengembalikan tanggal hari libur",
        "args": {
            "year": "Tahun",
            "holiday_name": "Nama hari libur, hanya mendukung penyebutan dalam bahasa Mandarin"
        },
        "returns": "Tanggal hari libur"
    },

    "get_user_historical_behaviors": {
        "description": "Mengambil informasi dasar pengguna dan data preferensi perilaku historis, termasuk ID pengguna, alamat rumah, alamat kerja, dan informasi dasar lainnya, serta kebiasaan konsumsi terperinci, kategori preferensi, rentang harga, persyaratan peringkat, preferensi waktu, dan informasi lainnya untuk berbagai skenario, digunakan untuk rekomendasi yang dipersonalisasi dan optimisasi layanan",
        "preconditions": "Mengambil data perilaku historis pengguna",
        "postconditions": "Mengembalikan informasi perilaku historis pengguna",
        "args": {},
        "returns": "Ringkasan informasi perilaku historis pengguna"
    },

    "get_user_all_orders": {
        "description": "Mengambil semua informasi pesanan pengguna",
        "preconditions": "Mengambil semua informasi pesanan pengguna",
        "postconditions": "Mengembalikan semua informasi pesanan pengguna",
        "args": {},
        "returns": "Ringkasan semua informasi pesanan pengguna"
    },

    "get_nearby": {
        "description": "Mengambil informasi semua toko/tempat komersial di sekitarnya",
        "preconditions": "Mengambil informasi semua tempat komersial (toko, bandara atau stasiun kereta, hotel, objek wisata, gerai, dll.) dalam jarak yang ditentukan (meter)",
        "postconditions": "Mengembalikan informasi tempat komersial",
        "args": {
            "longitude": "Garis bujur",
            "latitude": "Garis lintang",
            "range": "Jarak (dalam meter)"
        },
        "returns": "Informasi toko/tempat komersial"
    },
}

# Tool descriptions - Korean version
TOOLKIT_TOOL_DESCRIPTIONS_KO = {
    "longitude_latitude_to_distance": {
        "description": "위도와 경도를 기반으로 두 지점 사이의 거리를 미터 단위로 계산합니다.",
        "preconditions": "두 지점의 위도와 경도를 기반으로 그 사이의 거리를 계산합니다.",
        "postconditions": "두 지점 사이의 거리를 반환합니다 (정수, 미터 단위).",
        "args": {
            "longitude1": "첫 번째 지점의 경도",
            "latitude1": "첫 번째 지점의 위도",
            "longitude2": "두 번째 지점의 경도",
            "latitude2": "두 번째 지점의 위도"
        },
        "returns": "두 지점 사이의 거리 (정수, 미터 단위)"
    },

    "weather": {
        "description": "지정된 주소의 date_start 부터 date_end 까지 기간 동안의 날씨 정보를 조회합니다",
        "preconditions": "지정된 주소의 지정된 날짜 범위 내 날씨 정보를 조회합니다",
        "postconditions": "날씨 정보를 반환합니다",
        "args": {
            "address": "조회할 주소",
            "date_start": "시작 시간, 형식은 yyyy-mm-dd",
            "date_end": "종료 시간, 형식은 yyyy-mm-dd"
        },
        "returns": "날씨 정보"
    },

    "address_to_longitude_latitude": {
        "description": "주소를 기반으로 위도 및 경도 조회",
        "preconditions": "주소를 기반으로 해당 위도 및 경도 좌표 조회",
        "postconditions": "위도 및 경도 좌표 반환",
        "args": {
            "address": "조회할 주소"
        },
        "returns": "[경도, 위도]"
    },

    "get_date_holiday_info": {
        "description": "특정 날짜가 중국 공휴일인지 판단하며, 공휴일인 경우 공휴일 중국어 이름을 반환합니다.",
        "preconditions": "날짜를 기준으로 공휴일 여부를 판단하고, 공휴일인 경우 공휴일 이름을 반환합니다.",
        "postconditions": "공휴일 정보를 반환합니다.",
        "args": {
            "date": "날짜, 형식은 yyyy-mm-dd 입니다."
        },
        "returns": "공휴일 정보 판단 결과"
    },

    "get_holiday_date": {
        "description": "지정된 연도에서 특정 공휴일에 해당하는 구체적인 날짜를 가져옵니다.",
        "preconditions": "지정된 연도에서 특정 공휴일의 구체적인 날짜를 가져옵니다.",
        "postconditions": "공휴일의 날짜를 반환합니다.",
        "args": {
            "year": "연도",
            "holiday_name": "공휴일 이름, 중국어 표현만 지원됨"
        },
        "returns": "공휴일의 날짜"
    },

    "get_user_historical_behaviors": {
        "description": "사용자 기본 정보 및 과거 행동 선호도 데이터를 가져옵니다. 사용자 ID, 자택 주소, 직장 주소 등 기본 정보와 각 시나리오의 상세 소비 습관, 선호 카테고리, 가격 범위, 평점 요구 사항, 시간 선호도 등의 정보를 포함하며, 개인화된 추천 및 서비스 최적화에 사용됩니다.",
        "preconditions": "사용자 과거 행동 데이터 획득",
        "postconditions": "사용자 과거 행동 정보 반환",
        "args": {},
        "returns": "사용자 과거 행동 정보 요약"
    },

    "get_user_all_orders": {
        "description": "사용자의 모든 주문 정보를 조회합니다",
        "preconditions": "사용자의 모든 주문 정보를 조회합니다",
        "postconditions": "사용자의 모든 주문 정보를 반환합니다",
        "args": {},
        "returns": "사용자의 모든 주문 정보 요약"
    },

    "get_nearby": {
        "description": "근처의 모든 상점/상업 시설 정보를 조회합니다.",
        "preconditions": "지정된 범위 (미터) 내 모든 상업 시설 (상점, 공항 또는 기차역, 호텔, 관광명소, 가게 등) 의 정보를 조회합니다.",
        "postconditions": "상업 시설 정보를 반환합니다.",
        "args": {
            "longitude": "경도",
            "latitude": "위도",
            "range": "범위 (미터 단위)"
        },
        "returns": "상점/상업 시설 정보"
    },
}

# Tool descriptions - French version
TOOLKIT_TOOL_DESCRIPTIONS_FR = {
    "longitude_latitude_to_distance": {
        "description": "Calcule la distance entre deux points en fonction de la longitude et de la latitude (en mètres)",
        "preconditions": "Calcule la distance entre deux points en fonction de leur longitude et latitude",
        "postconditions": "Retourne la distance entre les deux points (entier, en mètres)",
        "args": {
            "longitude1": "Longitude du premier point",
            "latitude1": "Latitude du premier point",
            "longitude2": "Longitude du deuxième point",
            "latitude2": "Latitude du deuxième point"
        },
        "returns": "Distance entre les deux points (entier, en mètres)"
    },

    "weather": {
        "description": "Rechercher les informations météorologiques pour une adresse spécifiée entre date_start et date_end",
        "preconditions": "Rechercher les informations météorologiques pour une adresse spécifiée dans une plage de dates donnée",
        "postconditions": "Retourne les informations météorologiques",
        "args": {
            "address": "L'adresse à rechercher",
            "date_start": "Date de début, format yyyy-mm-dd",
            "date_end": "Date de fin, format yyyy-mm-dd"
        },
        "returns": "Informations météorologiques"
    },

    "address_to_longitude_latitude": {
        "description": "Obtenir la latitude et la longitude à partir d'une adresse",
        "preconditions": "Obtenir les coordonnées de latitude et de longitude correspondantes à partir de l'adresse",
        "postconditions": "Retourne les coordonnées de latitude et de longitude",
        "args": {
            "address": "L'adresse à rechercher"
        },
        "returns": "[Longitude, Latitude]"
    },

    "get_date_holiday_info": {
        "description": "Vérifie si une date donnée est un jour férié en Chine ; si c'est le cas, renvoie le nom du jour férié en chinois.",
        "preconditions": "Vérifie si la date correspond à un jour férié et renvoie le nom du jour férié si c'est le cas.",
        "postconditions": "Renvoie les informations sur le jour férié.",
        "args": {
            "date": "Date, au format yyyy-mm-dd"
        },
        "returns": "Résultat de la vérification des informations sur le jour férié."
    },

    "get_holiday_date": {
        "description": "Récupère la date exacte correspondant à un jour férié spécifique pour une année donnée.",
        "preconditions": "Récupère la date exacte d'un jour férié spécifique pour une année donnée.",
        "postconditions": "Renvoie la date du jour férié.",
        "args": {
            "year": "Année",
            "holiday_name": "Nom du jour férié, uniquement en chinois."
        },
        "returns": "Date du jour férié."
    },

    "get_user_historical_behaviors": {
        "description": "Récupère les informations de base de l'utilisateur et les données de préférences comportementales historiques, incluant l'identifiant utilisateur, l'adresse du domicile, l'adresse professionnelle, ainsi que les habitudes de consommation détaillées, les catégories préférées, les gammes de prix, les exigences de notation et les préférences horaires selon les différents scénarios, utilisées pour la recommandation personnalisée et l'optimisation des services.",
        "preconditions": "Récupération des données de comportement historique de l'utilisateur",
        "postconditions": "Retour des informations de comportement historique de l'utilisateur",
        "args": {},
        "returns": "Résumé des informations de comportement historique de l'utilisateur"
    },

    "get_user_all_orders": {
        "description": "Récupérer toutes les informations de commande de l'utilisateur",
        "preconditions": "Récupérer toutes les informations de commande de l'utilisateur",
        "postconditions": "Renvoyer toutes les informations de commande de l'utilisateur",
        "args": {},
        "returns": "Résumé de toutes les informations de commande de l'utilisateur"
    },

    "get_nearby": {
        "description": "Récupérer les informations de tous les magasins/lieux commerciaux à proximité",
        "preconditions": "Récupérer les informations de tous les lieux commerciaux dans un rayon spécifié (en mètres) (magasins, aéroports ou gares, hôtels, sites touristiques, boutiques, etc.)",
        "postconditions": "Retourne les informations sur les lieux commerciaux",
        "args": {
            "longitude": "Longitude",
            "latitude": "Latitude",
            "range": "Rayon (en mètres)"
        },
        "returns": "Informations sur les magasins/lieux commerciaux"
    },
}

# Tool descriptions - Spanish version
TOOLKIT_TOOL_DESCRIPTIONS_ES = {
    "longitude_latitude_to_distance": {
        "description": "Calcula la distancia entre dos puntos según longitud y latitud (en metros)",
        "preconditions": "Calcula la distancia entre ellos según la longitud y latitud de dos puntos",
        "postconditions": "Devuelve la distancia entre los dos puntos (entero, en metros)",
        "args": {
            "longitude1": "Longitud del primer punto",
            "latitude1": "Latitud del primer punto",
            "longitude2": "Longitud del segundo punto",
            "latitude2": "Latitud del segundo punto"
        },
        "returns": "Distancia entre los dos puntos (entero, en metros)"
    },

    "weather": {
        "description": "Consulta la información meteorológica para la dirección especificada entre date_start y date_end",
        "preconditions": "Consulta la información meteorológica para una dirección especificada dentro de un rango de fechas determinado",
        "postconditions": "Devuelve la información meteorológica",
        "args": {
            "address": "La dirección a consultar",
            "date_start": "Fecha de inicio, formato yyyy-mm-dd",
            "date_end": "Fecha de fin, formato yyyy-mm-dd"
        },
        "returns": "Información meteorológica"
    },

    "address_to_longitude_latitude": {
        "description": "Obtener latitud y longitud según la dirección",
        "preconditions": "Obtener las coordenadas de latitud y longitud correspondientes según la dirección",
        "postconditions": "Devolver las coordenadas de latitud y longitud",
        "args": {
            "address": "Dirección a consultar"
        },
        "returns": "[Longitud, Latitud]"
    },

    "get_date_holiday_info": {
        "description": "Determina si una fecha específica es un festivo en China; si es así, devuelve el nombre del festivo en chino.",
        "preconditions": "Determinar según la fecha si es un festivo; si es así, devolver el nombre del festivo.",
        "postconditions": "Devuelve información sobre el festivo.",
        "args": {
            "date": "Fecha, formato yyyy-mm-dd"
        },
        "returns": "Resultado de la verificación de información del festivo."
    },

    "get_holiday_date": {
        "description": "Obtiene la fecha exacta correspondiente a un día festivo específico en un año determinado.",
        "preconditions": "Obtener la fecha exacta de un día festivo específico en un año determinado.",
        "postconditions": "Devuelve la fecha del día festivo.",
        "args": {
            "year": "Año",
            "holiday_name": "Nombre del día festivo, solo se admite expresión en chino."
        },
        "returns": "Fecha del día festivo."
    },

    "get_user_historical_behaviors": {
        "description": "Obtiene información básica del usuario y datos de preferencias de comportamiento histórico, incluyendo información básica como ID de usuario, dirección residencial, dirección de trabajo, así como información detallada sobre hábitos de consumo en varios escenarios, categorías preferidas, rangos de precios, requisitos de puntuación, preferencias de tiempo, etc., utilizada para recomendaciones personalizadas y optimización del servicio",
        "preconditions": "Obtener datos de comportamiento histórico del usuario",
        "postconditions": "Devolver información de comportamiento histórico del usuario",
        "args": {},
        "returns": "Resumen de la información de comportamiento histórico del usuario"
    },

    "get_user_all_orders": {
        "description": "Obtener toda la información de pedidos del usuario",
        "preconditions": "Obtener toda la información de pedidos del usuario",
        "postconditions": "Devolver toda la información de pedidos del usuario",
        "args": {},
        "returns": "Resumen de toda la información de pedidos del usuario"
    },

    "get_nearby": {
        "description": "Obtener información de todas las tiendas/establecimientos comerciales cercanos",
        "preconditions": "Obtener información de todos los establecimientos comerciales (tiendas, aeropuertos o estaciones de tren, hoteles, atracciones, comercios, etc.) dentro de un rango especificado (metros)",
        "postconditions": "Devolver información de establecimientos comerciales",
        "args": {
            "longitude": "Longitud",
            "latitude": "Latitud",
            "range": "Rango (en metros)"
        },
        "returns": "Información de tiendas/establecimientos comerciales"
    },
}

# Tool descriptions - Thai version
TOOLKIT_TOOL_DESCRIPTIONS_TH = {
    "longitude_latitude_to_distance": {
        "description": "คำนวณระยะห่างระหว่างสองจุดโดยใช้ละติจูดและลองจิจูด (หน่วยเป็นเมตร)",
        "preconditions": "คำนวณระยะห่างระหว่างสองจุดโดยใช้ละติจูดและลองจิจูดของจุดเหล่านั้น",
        "postconditions": "ส่งคืนระยะห่างระหว่างสองจุด (จำนวนเต็ม, หน่วยเป็นเมตร)",
        "args": {
            "longitude1": "ลองจิจูดของจุดแรก",
            "latitude1": "ละติจูดของจุดแรก",
            "longitude2": "ลองจิจูดของจุดที่สอง",
            "latitude2": "ละติจูดของจุดที่สอง"
        },
        "returns": "ระยะห่างระหว่างสองจุด (จำนวนเต็ม, หน่วยเป็นเมตร)"
    },

    "weather": {
        "description": "ค้นหาข้อมูลสภาพอากาศสำหรับที่อยู่ระบุในช่วงระหว่าง date_start ถึง date_end",
        "preconditions": "ค้นหาข้อมูลสภาพอากาศสำหรับที่อยู่ระบุในช่วงวันที่กำหนด",
        "postconditions": "ส่งคืนข้อมูลสภาพอากาศ",
        "args": {
            "address": "ที่อยู่ที่ต้องการค้นหา",
            "date_start": "เวลาเริ่มต้น รูปแบบคือ yyyy-mm-dd",
            "date_end": "เวลาสิ้นสุด รูปแบบคือ yyyy-mm-dd"
        },
        "returns": "ข้อมูลสภาพอากาศ"
    },

    "address_to_longitude_latitude": {
        "description": "รับละติจูดและลองจิจูดตามที่อยู่",
        "preconditions": "รับพิกัดละติจูดและลองจิจูดที่สอดคล้องกับที่อยู่",
        "postconditions": "ส่งคืนพิกัดละติจูดและลองจิจูด",
        "args": {
            "address": "ที่อยู่ที่ต้องการค้นหา"
        },
        "returns": "[ลองจิจูด, ละติจูด]"
    },

    "get_date_holiday_info": {
        "description": "ตรวจสอบว่าวันที่ระบุเป็นวันหยุดของจีนหรือไม่ หากใช่ให้ส่งคืนชื่อวันหยุดเป็นภาษาจีน",
        "preconditions": "ตรวจสอบตามวันที่ว่าเป็นวันหยุดหรือไม่ หากใช่ให้ส่งคืนชื่อวันหยุด",
        "postconditions": "ส่งคืนข้อมูลวันหยุด",
        "args": {
            "date": "วันที่ รูปแบบคือ yyyy-mm-dd"
        },
        "returns": "ผลลัพธ์การตรวจสอบข้อมูลวันหยุด"
    },

    "get_holiday_date": {
        "description": "รับวันที่เฉพาะของวันหยุดที่กำหนดในปีที่ระบุ",
        "preconditions": "รับวันที่เฉพาะของวันหยุดที่กำหนดในปีที่ระบุ",
        "postconditions": "ส่งคืนวันที่ของวันหยุด",
        "args": {
            "year": "ปี",
            "holiday_name": "ชื่อวันหยุด, รองรับเฉพาะข้อความภาษาจีน"
        },
        "returns": "วันที่ของวันหยุด"
    },

    "get_user_historical_behaviors": {
        "description": "ดึงข้อมูลพื้นฐานของผู้ใช้และข้อมูลความชอบจากพฤติกรรมในอดีต รวมถึงข้อมูลพื้นฐานเช่น รหัสผู้ใช้ ที่อยู่อาศัย ที่อยู่ที่ทำงาน ตลอดจนนิสัยการใช้จ่ายโดยละเอียด หมวดหมู่สินค้าที่ชอบ ช่วงราคา ข้อกำหนดการให้คะแนน ความชอบด้านเวลา ฯลฯ ในสถานการณ์ต่างๆ เพื่อใช้ในการแนะนำส่วนบุคคลและการปรับปรุงบริการ",
        "preconditions": "ดึงข้อมูลพฤติกรรมในอดีตของผู้ใช้",
        "postconditions": "ส่งคืนข้อมูลพฤติกรรมในอดีตของผู้ใช้",
        "args": {},
        "returns": "สรุปข้อมูลพฤติกรรมในอดีตของผู้ใช้"
    },

    "get_user_all_orders": {
        "description": "ดึงข้อมูลคำสั่งซื้อทั้งหมดของผู้ใช้",
        "preconditions": "ดึงข้อมูลคำสั่งซื้อทั้งหมดของผู้ใช้",
        "postconditions": "ส่งคืนข้อมูลคำสั่งซื้อทั้งหมดของผู้ใช้",
        "args": {},
        "returns": "สรุปข้อมูลคำสั่งซื้อทั้งหมดของผู้ใช้"
    },

    "get_nearby": {
        "description": "รับข้อมูลเกี่ยวกับร้านค้า/สถานที่เชิงพาณิชย์ทั้งหมดที่อยู่ใกล้เคียง",
        "preconditions": "รับข้อมูลเกี่ยวกับสถานที่เชิงพาณิชย์ทั้งหมด (ร้านค้า, สนามบินหรือสถานีรถไฟ, โรงแรม, สถานที่ท่องเที่ยว, ร้านค้า ฯลฯ) ภายในระยะที่กำหนด (เมตร)",
        "postconditions": "ส่งคืนข้อมูลสถานที่เชิงพาณิชย์",
        "args": {
            "longitude": "ลองจิจูด",
            "latitude": "ละติจูด",
            "range": "ระยะ (หน่วยเป็นเมตร)"
        },
        "returns": "ข้อมูลร้านค้า/สถานที่เชิงพาณิชย์"
    },
}

# Tool descriptions - Hindi version
TOOLKIT_TOOL_DESCRIPTIONS_HI = {
    "longitude_latitude_to_distance": {
        "description": "अक्षांश और देशांतर के आधार पर दो बिंदुओं के बीच की दूरी की गणना करें (मीटर में)",
        "preconditions": "दो बिंदुओं के अक्षांश और देशांतर के आधार पर उनके बीच की दूरी की गणना करें",
        "postconditions": "दो बिंदुओं के बीच की दूरी लौटाता है (पूर्णांक, मीटर में)",
        "args": {
            "longitude1": "पहले बिंदु का देशांतर",
            "latitude1": "पहले बिंदु का अक्षांश",
            "longitude2": "दूसरे बिंदु का देशांतर",
            "latitude2": "दूसरे बिंदु का अक्षांश"
        },
        "returns": "दो बिंदुओं के बीच की दूरी (पूर्णांक, मीटर में)"
    },

    "weather": {
        "description": "date_start से date_end तक निर्दिष्ट पते के लिए मौसम की जानकारी जांचें",
        "preconditions": "निर्दिष्ट दिनांक सीमा में निर्दिष्ट पते के लिए मौसम की जानकारी जांचें",
        "postconditions": "मौसम की जानकारी लौटाएं",
        "args": {
            "address": "जांच करने के लिए पता",
            "date_start": "प्रारंभ समय, प्रारूप yyyy-mm-dd",
            "date_end": "समाप्ति समय, प्रारूप yyyy-mm-dd"
        },
        "returns": "मौसम की जानकारी"
    },

    "address_to_longitude_latitude": {
        "description": "पते के आधार पर अक्षांश और देशांतर प्राप्त करें",
        "preconditions": "पते के आधार पर संबंधित अक्षांश और देशांतर निर्देशांक प्राप्त करें",
        "postconditions": "अक्षांश और देशांतर निर्देशांक लौटाएं",
        "args": {
            "address": "जांच किया जाने वाला पता"
        },
        "returns": "[देशांतर, अक्षांश]"
    },

    "get_date_holiday_info": {
        "description": "किसी तिथि की जांच करें कि क्या यह चीनी अवकाश है; यदि हां, तो अवकाश का चीनी नाम वापस करें",
        "preconditions": "तिथि के आधार पर जांचें कि क्या यह अवकाश है, यदि हां तो अवकाश का नाम वापस करें",
        "postconditions": "अवकाश की जानकारी वापस करें",
        "args": {
            "date": "तिथि, प्रारूप yyyy-mm-dd"
        },
        "returns": "अवकाश जानकारी जांच का परिणाम"
    },

    "get_holiday_date": {
        "description": "निर्दिष्ट वर्ष में किसी विशेष अवकाश की विशिष्ट तिथि प्राप्त करें",
        "preconditions": "निर्दिष्ट वर्ष में किसी विशेष अवकाश की विशिष्ट तिथि प्राप्त करें",
        "postconditions": "अवकाश की तिथि लौटाएं",
        "args": {
            "year": "वर्ष",
            "holiday_name": "अवकाश का नाम, केवल चीनी अभिव्यक्ति का समर्थन करता है"
        },
        "returns": "अवकाश की तिथि"
    },

    "get_user_historical_behaviors": {
        "description": "उपयोगकर्ता की बुनियादी जानकारी और ऐतिहासिक व्यवहार वरीयता डेटा प्राप्त करें, जिसमें उपयोगकर्ता आईडी, घर का पता, कार्य पता आदि बुनियादी जानकारी शामिल है, साथ ही विभिन्न परिदृश्यों में विस्तृत उपभोग आदतें, पसंदीदा श्रेणियां, मूल्य सीमा, रेटिंग आवश्यकताएं, समय वरीयताएं आदि जानकारी शामिल है, जो व्यक्तिगत अनुशंसा और सेवा अनुकूलन के लिए उपयोग की जाती है।",
        "preconditions": "उपयोगकर्ता ऐतिहासिक व्यवहार डेटा प्राप्त करें",
        "postconditions": "उपयोगकर्ता ऐतिहासिक व्यवहार जानकारी लौटाएं",
        "args": {},
        "returns": "उपयोगकर्ता ऐतिहासिक व्यवहार जानकारी सारांश"
    },

    "get_user_all_orders": {
        "description": "उपयोगकर्ता की सभी ऑर्डर जानकारी प्राप्त करें",
        "preconditions": "उपयोगकर्ता की सभी ऑर्डर जानकारी प्राप्त करें",
        "postconditions": "उपयोगकर्ता की सभी ऑर्डर जानकारी वापस करें",
        "args": {},
        "returns": "उपयोगकर्ता की सभी ऑर्डर जानकारी का सारांश"
    },

    "get_nearby": {
        "description": "आसपास के सभी दुकानों/व्यावसायिक स्थानों की जानकारी प्राप्त करें",
        "preconditions": "निर्दिष्ट सीमा (मीटर में) के भीतर सभी व्यावसायिक स्थानों (दुकानें, हवाई अड्डे या रेलवे स्टेशन, होटल, पर्यटन स्थल, स्टोर आदि) की जानकारी प्राप्त करें",
        "postconditions": "व्यावसायिक स्थान की जानकारी वापस करें",
        "args": {
            "longitude": "देशांतर",
            "latitude": "अक्षांश",
            "range": "सीमा (मीटर में)"
        },
        "returns": "दुकान/व्यावसायिक स्थान की जानकारी"
    },
}

# Tool descriptions - Arabic version
TOOLKIT_TOOL_DESCRIPTIONS_AR = {
    "longitude_latitude_to_distance": {
        "description": "حساب المسافة بين نقطتين بناءً على خط الطول والعرض (بالأمتار)",
        "preconditions": "حساب المسافة بينهما بناءً على خط الطول والعرض للنقطتين",
        "postconditions": "إرجاع المسافة بين النقطتين (عدد صحيح، بالأمتار)",
        "args": {
            "longitude1": "خط طول النقطة الأولى",
            "latitude1": "خط عرض النقطة الأولى",
            "longitude2": "خط طول النقطة الثانية",
            "latitude2": "خط عرض النقطة الثانية"
        },
        "returns": "المسافة بين النقطتين (عدد صحيح، بالأمتار)"
    },

    "weather": {
        "description": "الاستعلام عن معلومات الطقس للعنوان المحدد خلال الفترة من date_start إلى date_end",
        "preconditions": "الاستعلام عن معلومات الطقس للعنوان المحدد ضمن نطاق التاريخ المحدد",
        "postconditions": "إرجاع معلومات الطقس",
        "args": {
            "address": "العنوان المراد الاستعلام عنه",
            "date_start": "وقت البدء، التنسيق هو yyyy-mm-dd",
            "date_end": "وقت الانتهاء، التنسيق هو yyyy-mm-dd"
        },
        "returns": "معلومات الطقس"
    },

    "address_to_longitude_latitude": {
        "description": "الحصول على خطوط الطول والعرض بناءً على العنوان",
        "preconditions": "الحصول على إحداثيات خطوط الطول والعرض المقابلة للعنوان",
        "postconditions": "إرجاع إحداثيات خطوط الطول والعرض",
        "args": {
            "address": "العنوان المراد الاستعلام عنه"
        },
        "returns": "[خط الطول، خط العرض]"
    },

    "get_date_holiday_info": {
        "description": "تحديد ما إذا كان تاريخ معين عطلة رسمية في الصين؛ وإذا كان كذلك، إرجاع الاسم الصيني للعطلة",
        "preconditions": "تحديد ما إذا كان التاريخ عطلة رسمية، وإذا كان كذلك إرجاع اسم العطلة",
        "postconditions": "إرجاع معلومات العطلة",
        "args": {
            "date": "التاريخ، التنسيق هو yyyy-mm-dd"
        },
        "returns": "نتيجة تحديد معلومات العطلة"
    },

    "get_holiday_date": {
        "description": "الحصول على التاريخ المحدد المقابل لعطلة معينة في سنة محددة",
        "preconditions": "الحصول على التاريخ المحدد لعطلة معينة في سنة محددة",
        "postconditions": "إرجاع تاريخ العطلة",
        "args": {
            "year": "السنة",
            "holiday_name": "اسم العطلة، يدعم فقط الصياغة باللغة الصينية"
        },
        "returns": "تاريخ العطلة"
    },

    "get_user_historical_behaviors": {
        "description": "الحصول على معلومات المستخدم الأساسية وبيانات تفضيلات السلوك التاريخي، بما في ذلك معرف المستخدم، والعنوان المنزلي، وعنوان العمل، وغيرها من المعلومات الأساسية، بالإضافة إلى عادات الاستهلاك التفصيلية، والفئات المفضلة، ونطاقات الأسعار، ومتطلبات التقييم، وتفضيلات الوقت في مختلف السيناريوهات، المستخدمة للتوصيات الشخصية وتحسين الخدمة",
        "preconditions": "الحصول على بيانات السلوك التاريخي للمستخدم",
        "postconditions": "إرجاع معلومات السلوك التاريخي للمستخدم",
        "args": {},
        "returns": "ملخص معلومات السلوك التاريخي للمستخدم"
    },

    "get_user_all_orders": {
        "description": "الحصول على معلومات جميع طلبات المستخدم",
        "preconditions": "الحصول على معلومات جميع طلبات المستخدم",
        "postconditions": "إرجاع معلومات جميع طلبات المستخدم",
        "args": {},
        "returns": "ملخص معلومات جميع طلبات المستخدم"
    },

    "get_nearby": {
        "description": "الحصول على معلومات حول جميع المتاجر/الأماكن التجارية القريبة",
        "preconditions": "الحصول على معلومات حول جميع الأماكن التجارية (متاجر، مطارات أو محطات قطار، فنادق، معالم سياحية، محلات، إلخ) ضمن نطاق محدد (بالأمتار)",
        "postconditions": "إرجاع معلومات الأماكن التجارية",
        "args": {
            "longitude": "خط الطول",
            "latitude": "خط العرض",
            "range": "النطاق (بالأمتار)"
        },
        "returns": "معلومات المتاجر/الأماكن التجارية"
    },
}

# Tool descriptions - Russian version
TOOLKIT_TOOL_DESCRIPTIONS_RU = {
    "longitude_latitude_to_distance": {
        "description": "Вычисляет расстояние между двумя точками по широте и долготе (в метрах)",
        "preconditions": "Вычисляет расстояние между двумя точками на основе их широты и долготы",
        "postconditions": "Возвращает расстояние между двумя точками (целое число, в метрах)",
        "args": {
            "longitude1": "Долгота первой точки",
            "latitude1": "Широта первой точки",
            "longitude2": "Долгота второй точки",
            "latitude2": "Широта второй точки"
        },
        "returns": "Расстояние между двумя точками (целое число, в метрах)"
    },

    "weather": {
        "description": "Запрос информации о погоде для указанного адреса в период с date_start по date_end",
        "preconditions": "Запрос информации о погоде для указанного адреса в заданном диапазоне дат",
        "postconditions": "Возвращает информацию о погоде",
        "args": {
            "address": "Адрес для запроса",
            "date_start": "Время начала, формат yyyy-mm-dd",
            "date_end": "Время окончания, формат yyyy-mm-dd"
        },
        "returns": "Информация о погоде"
    },

    "address_to_longitude_latitude": {
        "description": "Получение широты и долготы по адресу",
        "preconditions": "Получение соответствующих координат широты и долготы по адресу",
        "postconditions": "Возвращает координаты широты и долготы",
        "args": {
            "address": "Адрес для запроса"
        },
        "returns": "[Долгота, Широта]"
    },

    "get_date_holiday_info": {
        "description": "Определяет, является ли указанная дата китайским праздником; если да, возвращает китайское название праздника",
        "preconditions": "Определяет по дате, является ли она праздником, и если да, возвращает название праздника",
        "postconditions": "Возвращает информацию о празднике",
        "args": {
            "date": "Дата в формате yyyy-mm-dd"
        },
        "returns": "Результат проверки информации о празднике"
    },

    "get_holiday_date": {
        "description": "Получение конкретной даты для определенного праздника в заданном году",
        "preconditions": "Получение конкретной даты для определенного праздника в заданном году",
        "postconditions": "Возвращает дату праздника",
        "args": {
            "year": "Год",
            "holiday_name": "Название праздника, поддерживается только китайское написание"
        },
        "returns": "Дата праздника"
    },

    "get_user_historical_behaviors": {
        "description": "Получение основной информации о пользователе и данных о предпочтениях на основе истории поведения, включая ID пользователя, домашний адрес, рабочий адрес и другие базовые данные, а также подробные привычки потребления, предпочтительные категории, ценовые диапазоны, требования к оценкам, предпочтения по времени в различных сценариях, используемые для персонализированных рекомендаций и оптимизации сервиса",
        "preconditions": "Получение данных об истории поведения пользователя",
        "postconditions": "Возврат информации об истории поведения пользователя",
        "args": {},
        "returns": "Сводка информации об истории поведения пользователя"
    },

    "get_user_all_orders": {
        "description": "Получение информации обо всех заказах пользователя",
        "preconditions": "Получение всей информации о заказах пользователя",
        "postconditions": "Возврат всей информации о заказах пользователя",
        "args": {},
        "returns": "Сводка всей информации о заказах пользователя"
    },

    "get_nearby": {
        "description": "Получение информации обо всех магазинах и коммерческих заведениях, расположенных поблизости",
        "preconditions": "Получение информации обо всех коммерческих заведениях (магазины, аэропорты или железнодорожные вокзалы, отели, достопримечательности, торговые точки и т. д.) в указанном диапазоне (в метрах)",
        "postconditions": "Возвращает информацию о коммерческих заведениях",
        "args": {
            "longitude": "Долгота",
            "latitude": "Широта",
            "range": "Диапазон (в метрах)"
        },
        "returns": "Информация о магазинах/коммерческих заведениях"
    },
}

# Tool descriptions - Japanese version
TOOLKIT_TOOL_DESCRIPTIONS_JA = {
    "longitude_latitude_to_distance": {
        "description": "緯度経度に基づいて 2 点間の距離を計算します（単位：メートル）",
        "preconditions": "2 点の緯度経度に基づいてそれらの間の距離を計算します",
        "postconditions": "2 点間の距離を返します（整数、単位：メートル）",
        "args": {
            "longitude1": "1 点目の経度",
            "latitude1": "1 点目の緯度",
            "longitude2": "2 点目の経度",
            "latitude2": "2 点目の緯度"
        },
        "returns": "2 点間の距離（整数、単位：メートル）"
    },

    "weather": {
        "description": "指定された住所の date_start から date_end までの天気情報を照会します",
        "preconditions": "指定された住所の指定された日付範囲内の天気情報を照会します",
        "postconditions": "天気情報を返します",
        "args": {
            "address": "照会する住所",
            "date_start": "開始時間、形式は yyyy-mm-dd",
            "date_end": "終了時間、形式は yyyy-mm-dd"
        },
        "returns": "天気情報"
    },

    "address_to_longitude_latitude": {
        "description": "住所から緯度経度を取得する",
        "preconditions": "住所から対応する緯度経度座標を取得する",
        "postconditions": "緯度経度座標を返す",
        "args": {
            "address": "検索したい住所"
        },
        "returns": "[経度，緯度]"
    },

    "get_date_holiday_info": {
        "description": "特定の日付が中国の祝日かどうかを判定し、祝日であればその中国語名を返します。",
        "preconditions": "日付に基づいて祝日かどうかを判断し、祝日であれば祝日名を返します。",
        "postconditions": "祝日情報を返します。",
        "args": {
            "date": "日付。形式は yyyy-mm-dd です。"
        },
        "returns": "祝日情報の判定結果"
    },

    "get_holiday_date": {
        "description": "指定された年における特定の祝日に対応する具体的な日付を取得します",
        "preconditions": "指定された年における特定の祝日の具体的な日付を取得します",
        "postconditions": "祝日の日付を返します",
        "args": {
            "year": "年",
            "holiday_name": "祝日名、中国語表記のみサポート"
        },
        "returns": "祝日の日付"
    },

    "get_user_historical_behaviors": {
        "description": "ユーザーの基本情報および過去の行動嗜好データを取得します。ユーザー ID、自宅住所、勤務先住所などの基本情報に加え、各シーンにおける詳細な消費習慣、嗜好カテゴリ、価格帯、評価基準、時間傾向などの情報を含み、パーソナライズされた推薦およびサービス最適化に利用されます。",
        "preconditions": "ユーザーの履歴行動データの取得",
        "postconditions": "ユーザーの履歴行動情報の返却",
        "args": {},
        "returns": "ユーザーの履歴行動情報サマリー"
    },

    "get_user_all_orders": {
        "description": "ユーザーのすべての注文情報を取得します",
        "preconditions": "ユーザーのすべての注文情報を取得すること",
        "postconditions": "ユーザーのすべての注文情報を返します",
        "args": {},
        "returns": "ユーザーのすべての注文情報の概要"
    },

    "get_nearby": {
        "description": "近くのすべての商店/商業施設に関する情報を取得します",
        "preconditions": "指定された範囲（メートル）内にあるすべての商業施設（商店、空港または駅、ホテル、観光スポット、店舗など）の情報を取得します",
        "postconditions": "商業施設情報を返します",
        "args": {
            "longitude": "経度",
            "latitude": "緯度",
            "range": "範囲（メートル単位）"
        },
        "returns": "商店/商業施設情報"
    },
}

# Create Toolkit tool schema manager
_schema_manager = create_tool_schema_manager("toolkit", TOOLKIT_TOOL_DESCRIPTIONS_ZH, TOOLKIT_TOOL_DESCRIPTIONS_EN, japanese=TOOLKIT_TOOL_DESCRIPTIONS_JA, russian=TOOLKIT_TOOL_DESCRIPTIONS_RU, arabic=TOOLKIT_TOOL_DESCRIPTIONS_AR, hindi=TOOLKIT_TOOL_DESCRIPTIONS_HI, thai=TOOLKIT_TOOL_DESCRIPTIONS_TH, spanish=TOOLKIT_TOOL_DESCRIPTIONS_ES, french=TOOLKIT_TOOL_DESCRIPTIONS_FR, korean=TOOLKIT_TOOL_DESCRIPTIONS_KO, indonesian=TOOLKIT_TOOL_DESCRIPTIONS_ID, hebrew=TOOLKIT_TOOL_DESCRIPTIONS_HE, turkish=TOOLKIT_TOOL_DESCRIPTIONS_TR, vietnamese=TOOLKIT_TOOL_DESCRIPTIONS_VI, malay=TOOLKIT_TOOL_DESCRIPTIONS_MS, belarusian=TOOLKIT_TOOL_DESCRIPTIONS_BE, punjabi=TOOLKIT_TOOL_DESCRIPTIONS_PA, kazakh=TOOLKIT_TOOL_DESCRIPTIONS_KK, khmer=TOOLKIT_TOOL_DESCRIPTIONS_KM, burmese=TOOLKIT_TOOL_DESCRIPTIONS_MY, lao=TOOLKIT_TOOL_DESCRIPTIONS_LO, tamil=TOOLKIT_TOOL_DESCRIPTIONS_TA, telugu=TOOLKIT_TOOL_DESCRIPTIONS_TE)

# For backward compatibility, provide original function interface
def get_toolkit_tool_descriptions():
    """Get toolkit tool descriptions based on language configuration."""
    return _schema_manager.get_tool_descriptions()

# Backward compatible variable
TOOLKIT_TOOL_DESCRIPTIONS = get_toolkit_tool_descriptions()
