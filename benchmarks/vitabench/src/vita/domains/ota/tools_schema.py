"""Tool schema definitions for the ota domain.

This file contains the descriptions and mappings for all tools decorated with @is_tool
in the OTATools class.
"""

from typing import Dict, Any
from vita.utils.schema_utils import create_tool_schema_manager

# Tool descriptions extracted from tools.py - Chinese version
TOOL_DESCRIPTIONS_ZH = {
    "get_ota_hotel_info": {
        "description": "获取酒店信息，包含酒店id、名称、评分、星级、地址、标签、房间列表",
        "preconditions": "在酒店查询预订场景，需要获取酒店的详细信息",
        "postconditions": "返回酒店的详细信息，引导用户选择房间并下单",
        "args": {
            "hotel_id": "酒店id"
        },
        "returns": "酒店信息",
        "tool_type": "READ"
    },
    
    "get_ota_attraction_info": {
        "description": "获取景点信息，包含景点id、名称、地址、描述、评分、开放时间、门票价格、票种列表",
        "preconditions": "在景点旅游场景，需要获取景点的详细信息",
        "postconditions": "返回景点的详细信息，引导用户选择门票并下单",
        "args": {
            "attraction_id": "景点id"
        },
        "returns": "景点信息",
        "tool_type": "READ"
    },
    
    "get_ota_flight_info": {
        "description": "获取航班信息，包含航班id、航班号、出发城市、到达城市、出发机场位置、到达机场位置、出发时间、到达时间、航班标签、座位类型列表",
        "preconditions": "在机票查询购买场景，需要获取航班的详细信息",
        "postconditions": "返回航班的详细信息，引导用户选择座位并下单",
        "args": {
            "flight_id": "航班id"
        },
        "returns": "航班信息",
        "tool_type": "READ"
    },
    
    "get_ota_train_info": {
        "description": "获取火车信息，包含火车id、车次、出发城市、到达城市、出发车站位置、到达车站位置、出发时间、到达时间、火车标签、座位类型列表",
        "preconditions": "在火车票查询购买场景，需要获取火车的详细信息",
        "postconditions": "返回火车的详细信息，引导用户选择座位并下单",
        "args": {
            "train_id": "火车id"
        },
        "returns": "火车信息",
        "tool_type": "READ"
    },
    
    "hotel_search_recommend": {
        "description": "酒旅场景下，基于用户的地点需求和偏好，推荐合适的酒店选项，提供酒店的基础信息，包含酒店id、名称、评分、星级、地址、标签",
        "preconditions": "用户请求预定酒店，给出了酒店相关的关键词或地点",
        "postconditions": "返回符合条件的酒店列表，如需查看酒店详情（房间列表、价格等）需要使用酒店详情查询工具，引导用户选择酒店",
        "args": {
            "city_name": "城市名称",
            "key_words": "搜索关键词(匹配酒店名称、酒店介绍等)"
        },
        "returns": "结构化输出酒店基础信息",
        "tool_type": "READ"
    },
    
    "attractions_search_recommend": {
        "description": "基于用户的地点需求和偏好，推荐合适的景点选项，提供景点的基础信息，包含景点id、名称、地址、描述、评分、开放时间",
        "preconditions": "用户请求预定景点，给出了景点相关的关键词或地点",
        "postconditions": "返回符合条件的景点列表，如需查看景点详情（门票列表、价格等）需要使用景点详情查询工具，引导用户选择景点",
        "args": {
            "city_name": "城市名称",
            "key_words": "搜索关键词(匹配景点名称、位置、地址、特色等)"
        },
        "returns": "结构化输出景点基础信息",
        "tool_type": "READ"
    },
    
    "flight_search_recommend": {
        "description": "基于用户的地点需求和偏好，推荐合适的航班选项，提供航班的基础信息，包含航班id、航班号、出发城市、到达城市、出发机场位置、到达机场位置、出发时间、到达时间、航班标签",
        "preconditions": "用户请求预定航班，给出了航班相关的关键词或地点",
        "postconditions": "返回符合条件的航班列表，如需查看航班详情（座位类型列表、价格、日期等）需要使用航班详情查询工具，引导用户选择航班",
        "args": {
            "departure": "出发城市",
            "destination": "目的城市"
        },
        "returns": "结构化输出航班基础信息",
        "tool_type": "READ"
    },
    
    "train_ticket_search": {
        "description": "基于用户的地点需求和偏好，推荐合适的火车选项，提供火车票的基础信息，包含火车id、车次、出发城市、到达城市、出发车站位置、到达车站位置、出发时间、到达时间、火车标签",
        "preconditions": "用户请求预定火车，给出了火车相关的关键词或地点",
        "postconditions": "返回符合条件的火车票列表，如需查看火车票详情（座位类型列表、价格、日期等）需要使用火车票详情查询工具，引导用户选择火车票",
        "args": {
            "departure": "出发城市",
            "destination": "目的城市",
            "date": "出发日期"
        },
        "returns": "结构化输出火车基础信息",
        "tool_type": "READ"
    },
    
    "create_hotel_order": {
        "description": "用户预订酒店时，系统根据用户的需求（如酒店名称、入住日期、人数等）生成订单",
        "preconditions": "用户已登录并提供有效的身份标识（user_id），用户提供了有效的酒店名称（hotel_name）和房间类型（room_type），系统有关于目标酒店的信息，并且该酒店在所请求的日期内有房间",
        "postconditions": "生成订单，请用户确认支付",
        "args": {
            "hotel_id": "酒店ID",
            "room_id": "房间ID",
            "user_id": "用户ID"
        },
        "returns": "创建订单操作的反馈输出",
        "tool_type": "WRITE"
    },
    
    "create_attraction_order": {
        "description": "用户根据景点和日期购买门票，系统返回门票的相关信息并进行下单",
        "preconditions": "在景点旅游场景，用户请求预定景点，给出了预定相关必要信息",
        "postconditions": "生成订单，请用户确认支付",
        "args": {
            "attraction_id": "景点ID",
            "ticket_id": "门票ID",
            "user_id": "用户ID",
            "date": "参观日期，格式为 %Y-%m-%d",
            "quantity": "数量"
        },
        "returns": "创建订单操作的反馈输出",
        "tool_type": "WRITE"
    },
    
    "create_flight_order": {
        "description": "用户根据航班号、日期、座位类型、数量购买机票，系统返回机票的相关信息并进行下单",
        "preconditions": "在机票查询购买场景，用户请求预定航班，给出了预定相关必要信息",
        "postconditions": "生成订单，请用户确认支付",
        "args": {
            "flight_id": "航班ID",
            "seat_id": "座位ID",
            "user_id": "用户ID",
            "date": "出发日期",
            "quantity": "数量"
        },
        "returns": "创建订单操作的反馈输出",
        "tool_type": "WRITE"
    },
    
    "create_train_order": {
        "description": "用户根据车次、日期、座位类型、数量购买火车票，系统返回火车票的相关信息并进行下单",
        "preconditions": "在火车票查询购买场景，用户请求预定火车，给出了预定相关必要信息",
        "postconditions": "生成订单，请用户确认支付",
        "args": {
            "train_id": "火车ID",
            "seat_id": "座位ID",
            "user_id": "用户ID",
            "date": "出发日期",
            "quantity": "数量"
        },
        "returns": "创建订单操作的反馈输出",
        "tool_type": "WRITE"
    },
    
    "pay_hotel_order": {
        "description": "用户进行酒店订单支付",
        "preconditions": "在酒店查询预订场景，用户请求支付酒店订单，上文确定了订单ID",
        "postconditions": "确认支付并更新订单状态为已支付",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },
    
    "pay_attraction_order": {
        "description": "用户进行门票订单支付",
        "preconditions": "在景点旅游场景，用户请求支付景点门票订单，上文确定了订单ID",
        "postconditions": "确认支付并更新订单状态为已支付",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },
    
    "pay_flight_order": {
        "description": "用户进行机票订单支付",
        "preconditions": "在机票查询购买场景，用户请求支付航班订单，上文确定了订单ID",
        "postconditions": "确认支付并更新订单状态为已支付",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },
    
    "pay_train_order": {
        "description": "用户进行火车票订单支付",
        "preconditions": "在火车票查询购买场景，用户请求支付火车票订单，上文确定了订单ID",
        "postconditions": "确认支付并更新订单状态为已支付",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "支付结果信息",
        "tool_type": "WRITE"
    },
    
    "search_hotel_order": {
        "description": "根据用户ID，查询用户的酒店订单，返回包含订单ID、订单类型、用户ID、酒店ID、订单总价、下单时间、更新时间和订单状态",
        "preconditions": "用户需求为查询酒店订单",
        "postconditions": "返回订单信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户ID",
            "date": "日期",
            "status": "订单状态"
        },
        "returns": "指定用户的酒店订单信息",
        "tool_type": "READ"
    },
    
    "search_attraction_order": {
        "description": "根据用户ID，查询用户的景点门票订单，返回包含订单ID、订单类型、用户ID、景点ID、订单总价、下单时间、更新时间和订单状态",
        "preconditions": "用户需求为查询景点门票订单",
        "postconditions": "返回订单信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户ID",
            "date": "日期",
            "status": "订单状态"
        },
        "returns": "指定用户的景点门票订单信息",
        "tool_type": "READ"
    },
    
    "search_flight_order": {
        "description": "根据用户ID，查询用户的机票订单，返回包含订单ID、订单类型、用户ID、航班ID、订单总价、下单时间、更新时间和订单状态",
        "preconditions": "用户需求为查询机票订单",
        "postconditions": "返回订单信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户ID",
            "date": "日期",
            "status": "订单状态"
        },
        "returns": "指定用户的机票订单信息",
        "tool_type": "READ"
    },
    
    "search_train_order": {
        "description": "根据用户ID，查询用户的火车票订单，返回包含订单ID、订单类型、用户ID、火车ID、订单总价、下单时间、更新时间和订单状态",
        "preconditions": "用户需求为查询火车票订单",
        "postconditions": "返回订单信息，方便之后进行修改/取消",
        "args": {
            "user_id": "用户ID",
            "date": "日期",
            "status": "订单状态"
        },
        "returns": "指定用户的火车票订单信息",
        "tool_type": "READ"
    },
    
    "get_hotel_order_detail": {
        "description": "获取酒店订单详情，包含订单ID、订单类型、用户ID、酒店ID、订单总价、下单时间、更新时间、订单状态和订单房间详细信息（房间类型、入住日期、价格、房间ID）",
        "preconditions": "用户请求获取酒店订单详情，上文确定了订单ID",
        "postconditions": "返回订单详情",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "订单详情",
        "tool_type": "READ"
    },
    
    "get_attraction_order_detail": {
        "description": "获取景点门票订单详情，包含订单ID、订单类型、用户ID、景点ID、订单总价、下单时间、更新时间、订单状态和订单景点详细信息（门票类型、日期、价格、门票ID）",
        "preconditions": "用户请求获取景点门票订单详情，上文确定了订单ID",
        "postconditions": "返回订单详情",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "订单详情",
        "tool_type": "READ"
    },
    
    "get_flight_order_detail": {
        "description": "获取机票订单详情，包含订单ID、订单类型、用户ID、航班ID、订单总价、下单时间、更新时间、订单状态和订单机票详细信息（座位类型、日期、价格、座位ID）",
        "preconditions": "用户请求获取机票订单详情，上文确定了订单ID",
        "postconditions": "返回订单详情",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "订单详情",
        "tool_type": "READ"
    },
    
    "get_train_order_detail": {
        "description": "获取火车票订单详情，包含订单ID、订单类型、用户ID、火车ID、订单总价、下单时间、更新时间、订单状态和订单火车票详细信息（座位类型、日期、价格、座位ID）",
        "preconditions": "用户请求获取火车票订单详情，上文确定了订单ID",
        "postconditions": "返回订单详情",
        "args": {
            "order_id": "订单ID"
        },
        "returns": "订单详情",
        "tool_type": "READ"
    },
    
    "modify_train_order": {
        "description": "修改火车票订单，支持更改出发日期，自动处理补差价或退差价。",
        "preconditions": "在火车票查询购买场景，用户请求修改火车票订单，上文确定了订单ID",
        "postconditions": "修改订单并更新订单状态，若需补差价，订单状态改为unpaid，否则保持原状态，如需补差价，需引导用户支付当笔订单",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID",
            "new_date": "新的出发日期，格式为 %Y-%m-%d"
        },
        "returns": "(修改后的订单内容, 差价，正为需补差价，负为退差价)",
        "tool_type": "WRITE"
    },
    
    "modify_flight_order": {
        "description": "修改机票订单，支持更改出发日期，自动处理补差价或退差价。",
        "preconditions": "在机票查询购买场景，用户请求修改机票订单，上文确定了订单ID",
        "postconditions": "修改订单并更新订单状态，若需补差价，订单状态改为unpaid，否则保持原状态，如需补差价，需引导用户支付当笔订单",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID",
            "new_date": "新的出发日期，格式为 %Y-%m-%d"
        },
        "returns": "(修改后的订单内容, 差价，正为需补差价，负为退差价)",
        "tool_type": "WRITE"
    },
    
    "cancel_hotel_order": {
        "description": "用户取消已预订的酒店订单",
        "preconditions": "在酒店查询预订场景，用户请求取消酒店订单，上文确定了订单ID",
        "postconditions": "取消订单并更新订单状态，若需退差价，告知用户即可",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID"
        },
        "returns": "取消订单的退款金额",
        "tool_type": "WRITE"
    },
    
    "cancel_attraction_order": {
        "description": "用户取消已预订的景点门票订单",
        "preconditions": "历史对话中有订单id或者已经进行过订单查询，用户有权限取消该订单",
        "postconditions": "如果退差价，告知用户即可",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID"
        },
        "returns": "取消订单的退款金额",
        "tool_type": "WRITE"
    },
    
    "cancel_flight_order": {
        "description": "用户取消已预订的机票订单",
        "preconditions": "历史对话中有订单id或者已经进行过订单查询，用户有权限取消该订单",
        "postconditions": "如果退差价，告知用户即可",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID"
        },
        "returns": "取消订单的退款金额",
        "tool_type": "WRITE"
    },
    
    "cancel_train_order": {
        "description": "用户取消已预订的火车票订单",
        "preconditions": "历史对话中有订单id或者已经进行过订单查询，用户有权限取消该订单",
        "postconditions": "如果退差价，告知用户即可",
        "args": {
            "order_id": "订单ID",
            "user_id": "用户ID"
        },
        "returns": "取消订单的退款金额",
        "tool_type": "WRITE"
    }
}

# Tool descriptions extracted from tools.py - English version
TOOL_DESCRIPTIONS_EN = {
    "get_ota_hotel_info": {
        "description": "Get hotel information including hotel id, name, rating, star level, address, tags, and room list",
        "preconditions": "In hotel query and booking scenario, need to get detailed hotel information",
        "postconditions": "Return detailed hotel information, guide user to select room and place order",
        "args": {
            "hotel_id": "Hotel id"
        },
        "returns": "Hotel information",
        "tool_type": "READ"
    },
    
    "get_ota_attraction_info": {
        "description": "Get attraction information including attraction id, name, address, description, rating, opening hours, ticket prices, and ticket type list",
        "preconditions": "In attraction travel scenario, need to get detailed attraction information",
        "postconditions": "Return detailed attraction information, guide user to select tickets and place order",
        "args": {
            "attraction_id": "Attraction id"
        },
        "returns": "Attraction information",
        "tool_type": "READ"
    },
    
    "get_ota_flight_info": {
        "description": "Get flight information including flight id, flight number, departure city, arrival city, departure airport location, arrival airport location, departure time, arrival time, flight tags, and seat type list",
        "preconditions": "In flight ticket query and purchase scenario, need to get detailed flight information",
        "postconditions": "Return detailed flight information, guide user to select seats and place order",
        "args": {
            "flight_id": "Flight id"
        },
        "returns": "Flight information",
        "tool_type": "READ"
    },
    
    "get_ota_train_info": {
        "description": "Get train information including train id, train number, departure city, arrival city, departure station location, arrival station location, departure time, arrival time, train tags, and seat type list",
        "preconditions": "In train ticket query and purchase scenario, need to get detailed train information",
        "postconditions": "Return detailed train information, guide user to select seats and place order",
        "args": {
            "train_id": "Train id"
        },
        "returns": "Train information",
        "tool_type": "READ"
    },
    
    "hotel_search_recommend": {
        "description": "In hotel query and booking scenario, recommend suitable hotel options based on user location needs and preferences, provide basic hotel information including hotel id, name, rating, star level, address, and tags",
        "preconditions": "User requests hotel booking, provides hotel-related keywords or location",
        "postconditions": "Return list of hotels meeting criteria, if hotel details (room list, prices, etc.) are needed, use hotel detail query tool, guide user to select hotel",
        "args": {
            "city_name": "City name",
            "key_words": "Search keywords (matching hotel name, hotel introduction, etc.)"
        },
        "returns": "Structured output of basic hotel information",
        "tool_type": "READ"
    },
    
    "attractions_search_recommend": {
        "description": "Recommend suitable attraction options based on user location needs and preferences, provide basic attraction information including attraction id, name, address, description, rating, and opening hours",
        "preconditions": "User requests attraction booking, provides attraction-related keywords or location",
        "postconditions": "Return list of attractions meeting criteria, if attraction details (ticket list, prices, etc.) are needed, use attraction detail query tool, guide user to select attraction",
        "args": {
            "city_name": "City name",
            "key_words": "Search keywords (matching attraction name, location, address, features, etc.)"
        },
        "returns": "Structured output of basic attraction information",
        "tool_type": "READ"
    },
    
    "flight_search_recommend": {
        "description": "Recommend suitable flight options based on user location needs and preferences, provide basic flight information including flight id, flight number, departure city, arrival city, departure airport location, arrival airport location, departure time, arrival time, and flight tags",
        "preconditions": "User requests flight booking, provides flight-related keywords or location",
        "postconditions": "Return list of flights meeting criteria, if flight details (seat type list, prices, dates, etc.) are needed, use flight detail query tool, guide user to select flight",
        "args": {
            "departure": "Departure city",
            "destination": "Destination city"
        },
        "returns": "Structured output of basic flight information",
        "tool_type": "READ"
    },
    
    "train_ticket_search": {
        "description": "Recommend suitable train options based on user location needs and preferences, provide basic train ticket information including train id, train number, departure city, arrival city, departure station location, arrival station location, departure time, arrival time, and train tags",
        "preconditions": "User requests train booking, provides train-related keywords or location",
        "postconditions": "Return list of train tickets meeting criteria, if train ticket details (seat type list, prices, dates, etc.) are needed, use train ticket detail query tool, guide user to select train ticket",
        "args": {
            "departure": "Departure city",
            "destination": "Destination city",
            "date": "Departure date"
        },
        "returns": "Structured output of basic train information",
        "tool_type": "READ"
    },
    
    "create_hotel_order": {
        "description": "When user books hotel, system generates order based on user requirements (such as hotel name, check-in date, number of people, etc.)",
        "preconditions": "User is logged in and provides valid identity (user_id), user provides valid hotel name (hotel_name) and room type (room_type), system has information about target hotel, and hotel has rooms available on requested dates",
        "postconditions": "Generate order, ask user to confirm payment",
        "args": {
            "hotel_id": "Hotel ID",
            "room_id": "Room ID",
            "user_id": "User ID"
        },
        "returns": "Feedback output of creating order operation",
        "tool_type": "WRITE"
    },
    
    "create_attraction_order": {
        "description": "User purchases tickets based on attraction and date, system returns ticket-related information and places order",
        "preconditions": "In attraction travel scenario, user requests to book attraction, provides necessary booking information",
        "postconditions": "Generate order, ask user to confirm payment",
        "args": {
            "attraction_id": "Attraction ID",
            "ticket_id": "Ticket ID",
            "user_id": "User ID",
            "date": "Visit date, format: %Y-%m-%d",
            "quantity": "Quantity"
        },
        "returns": "Feedback output of creating order operation",
        "tool_type": "WRITE"
    },
    
    "create_flight_order": {
        "description": "User purchases flight tickets based on flight and seat type, system returns flight ticket-related information and places order",
        "preconditions": "In flight ticket query and purchase scenario, user requests to book flight, provides necessary booking information",
        "postconditions": "Generate order, ask user to confirm payment",
        "args": {
            "flight_id": "Flight ID",
            "seat_id": "Seat ID",
            "user_id": "User ID",
            "date": "Departure date, format: %Y-%m-%d",
            "quantity": "Quantity"
        },
        "returns": "Feedback output of creating order operation",
        "tool_type": "WRITE"
    },
    
    "create_train_order": {
        "description": "User purchases train tickets based on train and seat type, system returns train ticket-related information and places order",
        "preconditions": "In train ticket query and purchase scenario, user requests to book train, provides necessary booking information",
        "postconditions": "Generate order, ask user to confirm payment",
        "args": {
            "train_id": "Train ID",
            "seat_id": "Seat ID",
            "user_id": "User ID",
            "date": "Departure date, format: %Y-%m-%d",
            "quantity": "Quantity"
        },
        "returns": "Feedback output of creating order operation",
        "tool_type": "WRITE"
    },
    
    "pay_hotel_order": {
        "description": "User pays for hotel order",
        "preconditions": "In hotel query and booking scenario, user requests payment for hotel order, order ID is determined above",
        "postconditions": "Confirm payment and update order status to paid",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },
    
    "pay_attraction_order": {
        "description": "User pays for attraction ticket order",
        "preconditions": "In attraction travel scenario, user requests payment for attraction ticket order, order ID is determined above",
        "postconditions": "Confirm payment and update order status to paid",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },
    
    "pay_flight_order": {
        "description": "User pays for flight order",
        "preconditions": "In flight ticket query and purchase scenario, user requests payment for flight order, order ID is determined above",
        "postconditions": "Confirm payment and update order status to paid",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },
    
    "pay_train_order": {
        "description": "User pays for train ticket order",
        "preconditions": "In train ticket query and purchase scenario, user requests payment for train ticket order, order ID is determined above",
        "postconditions": "Confirm payment and update order status to paid",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Payment result information",
        "tool_type": "WRITE"
    },
    
    "search_hotel_order": {
        "description": "Query user's hotel orders based on user ID, return order ID, order type, user ID, hotel ID, order total price, order time, update time and order status",
        "preconditions": "User needs to query hotel orders",
        "postconditions": "Return order information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User ID",
            "date": "Date",
            "status": "Order status"
        },
        "returns": "Specified user's hotel order information",
        "tool_type": "READ"
    },
    
    "search_attraction_order": {
        "description": "Query user's attraction ticket orders based on user ID, return order ID, order type, user ID, attraction ID, order total price, order time, update time and order status",
        "preconditions": "User needs to query attraction ticket orders",
        "postconditions": "Return order information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User ID",
            "date": "Date",
            "status": "Order status"
        },
        "returns": "Specified user's attraction ticket order information",
        "tool_type": "READ"
    },
    
    "search_flight_order": {
        "description": "Query user's flight orders based on user ID, return order ID, order type, user ID, flight ID, order total price, order time, update time and order status",
        "preconditions": "User needs to query flight orders",
        "postconditions": "Return order information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User ID",
            "date": "Date",
            "status": "Order status"
        },
        "returns": "Specified user's flight order information",
        "tool_type": "READ"
    },
    
    "search_train_order": {
        "description": "Query user's train ticket orders based on user ID, return order ID, order type, user ID, train ID, order total price, order time, update time and order status",
        "preconditions": "User needs to query train ticket orders",
        "postconditions": "Return order information, convenient for later modification/cancellation",
        "args": {
            "user_id": "User ID",
            "date": "Date",
            "status": "Order status"
        },
        "returns": "Specified user's train ticket order information",
        "tool_type": "READ"
    },
    
    "get_hotel_order_detail": {
        "description": "Get hotel order details, including order ID, order type, user ID, hotel ID, order total price, order time, update time, order status and order room detailed information (room type, check-in date, price, room ID)",
        "preconditions": "User requests hotel order details, order ID is determined above",
        "postconditions": "Return order details",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Order details",
        "tool_type": "READ"
    },
    
    "get_attraction_order_detail": {
        "description": "Get attraction ticket order details, including order ID, order type, user ID, attraction ID, order total price, order time, update time, order status and order attraction detailed information (ticket type, date, price, ticket ID)",
        "preconditions": "User requests attraction ticket order details, order ID is determined above",
        "postconditions": "Return order details",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Order details",
        "tool_type": "READ"
    },
    
    "get_flight_order_detail": {
        "description": "Get flight order details, including order ID, order type, user ID, flight ID, order total price, order time, update time, order status and order flight ticket detailed information (seat type, date, price, seat ID)",
        "preconditions": "User requests flight order details, order ID is determined above",
        "postconditions": "Return order details",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Order details",
        "tool_type": "READ"
    },
    
    "get_train_order_detail": {
        "description": "Get train ticket order details, including order ID, order type, user ID, train ID, order total price, order time, update time, order status and order train ticket detailed information (seat type, date, price, seat ID)",
        "preconditions": "User requests train ticket order details, order ID is determined above",
        "postconditions": "Return order details",
        "args": {
            "order_id": "Order ID"
        },
        "returns": "Order details",
        "tool_type": "READ"
    },
    
    "modify_train_order": {
        "description": "Modify train ticket order, support changing departure date, automatically handle price difference compensation or refund",
        "preconditions": "In train ticket query and purchase scenario, user requests to modify train ticket order, order ID is determined above",
        "postconditions": "Modify order and update order status, if price difference compensation is needed, order status changes to unpaid, otherwise maintains original status, if price difference compensation is needed, guide user to pay for current order",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID",
            "new_date": "New departure date, format: %Y-%m-%d"
        },
        "returns": "(Modified order content, price difference, positive means need to compensate, negative means refund)",
        "tool_type": "WRITE"
    },
    
    "modify_flight_order": {
        "description": "Modify flight order, support changing departure date, automatically handle price difference compensation or refund",
        "preconditions": "In flight ticket query and purchase scenario, user requests to modify flight order, order ID is determined above",
        "postconditions": "Modify order and update order status, if price difference compensation is needed, order status changes to unpaid, otherwise maintains original status, if price difference compensation is needed, guide user to pay for current order",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID",
            "new_date": "New departure date, format: %Y-%m-%d"
        },
        "returns": "(Modified order content, price difference, positive means need to compensate, negative means refund)",
        "tool_type": "WRITE"
    },
    
    "cancel_hotel_order": {
        "description": "User cancels booked hotel order",
        "preconditions": "In hotel query and booking scenario, user requests to cancel hotel order, order ID is determined above",
        "postconditions": "Cancel order and update order status, if refund is needed, inform user",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID"
        },
        "returns": "Order cancellation refund amount",
        "tool_type": "WRITE"
    },
    
    "cancel_attraction_order": {
        "description": "User cancels booked attraction ticket order",
        "preconditions": "Order ID exists in conversation history or order query has been performed, user has permission to cancel this order",
        "postconditions": "If refund is needed, inform user",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID"
        },
        "returns": "Order cancellation refund amount",
        "tool_type": "WRITE"
    },
    
    "cancel_flight_order": {
        "description": "User cancels booked flight order",
        "preconditions": "Order ID exists in conversation history or order query has been performed, user has permission to cancel this order",
        "postconditions": "If refund is needed, inform user",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID"
        },
        "returns": "Order cancellation refund amount",
        "tool_type": "WRITE"
    },
    
    "cancel_train_order": {
        "description": "User cancels booked train ticket order",
        "preconditions": "Order ID exists in conversation history or order query has been performed, user has permission to cancel this order",
        "postconditions": "If refund is needed, inform user",
        "args": {
            "order_id": "Order ID",
            "user_id": "User ID"
        },
        "returns": "Order cancellation refund amount",
        "tool_type": "WRITE"
    }
}

# Tool descriptions - Telugu version
TOOL_DESCRIPTIONS_TE = {
    "get_ota_hotel_info": {
        "description": "హోటల్ సమాచారాన్ని పొందండి, ఇందులో హోటల్ ఐడి, పేరు, రేటింగ్, స్టార్ ర్యాంకింగ్, చిరునామా, ట్యాగ్‌లు మరియు గదుల జాబితా ఉంటాయి",
        "preconditions": "హోటల్ శోధన మరియు బుకింగ్ సందర్భంలో, హోటల్ యొక్క వివరణాత్మక సమాచారాన్ని పొందాల్సిన అవసరం ఉంది",
        "postconditions": "హోటల్ యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి, వినియోగదారును గదిని ఎంచుకోవడానికి మరియు ఆర్డర్ చేయడానికి మార్గనిర్దేశం చేయండి",
        "args": {
            "hotel_id": "హోటల్ ఐడి"
        },
        "returns": "హోటల్ సమాచారం",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "ఆకర్షణ సమాచారాన్ని పొందండి, ఇందులో ఆకర్షణ ఐడి, పేరు, చిరునామా, వివరణ, రేటింగ్, తెరిచే సమయాలు, టికెట్ ధర మరియు టికెట్ రకాల జాబితా ఉంటాయి",
        "preconditions": "ఆకర్షణ పర్యాటక సందర్భంలో, ఆకర్షణ యొక్క వివరణాత్మక సమాచారాన్ని పొందాల్సిన అవసరం ఉంది",
        "postconditions": "ఆకర్షణ యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి, వినియోగదారును టికెట్లను ఎంచుకోవడానికి మరియు ఆర్డర్ చేయడానికి మార్గనిర్దేశం చేయండి",
        "args": {
            "attraction_id": "ఆకర్షణ ఐడి"
        },
        "returns": "ఆకర్షణ సమాచారం",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "విమాన సమాచారాన్ని పొందండి, ఇందులో విమాన ఐడీ, విమాన నంబర్, బయలుదేరు నగరం, చేరు నగరం, బయలుదేరు విమానాశ్రయం స్థానం, చేరు విమానాశ్రయం స్థానం, బయలుదేరు సమయం, చేరు సమయం, విమాన ట్యాగ్‌లు, సీటు రకాల జాబితా ఉంటాయి.",
        "preconditions": "విమాన టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, విమానం యొక్క వివరణాత్మక సమాచారాన్ని పొందాల్సి ఉంటుంది.",
        "postconditions": "విమానం యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి, వినియోగదారును సీటును ఎంచుకోవడానికి మరియు ఆర్డర్ చేయడానికి మార్గనిర్దేశం చేయండి.",
        "args": {
            "flight_id": "విమాన ఐడీ"
        },
        "returns": "విమాన సమాచారం",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "రైలు సమాచారాన్ని పొందండి, ఇందులో రైలు ఐడి, రైలు నంబర్, బయలుదేరే నగరం, చేరే నగరం, బయలుదేరే స్టేషన్ స్థానం, చేరే స్టేషన్ స్థానం, బయలుదేరే సమయం, చేరే సమయం, రైలు ట్యాగ్‌లు, సీటు రకాల జాబితా ఉంటాయి.",
        "preconditions": "రైలు టికెట్ విచారణ మరియు కొనుగోలు సందర్భంలో, రైలు యొక్క వివరణాత్మక సమాచారాన్ని పొందాల్సిన అవసరం ఉంది.",
        "postconditions": "రైలు యొక్క వివరణాత్మక సమాచారాన్ని తిరిగి ఇవ్వండి, వినియోగదారును సీటును ఎంచుకోవడానికి మరియు ఆర్డర్ చేయడానికి మార్గనిర్దేశం చేయండి.",
        "args": {
            "train_id": "రైలు ఐడి"
        },
        "returns": "రైలు సమాచారం",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "హోటల్ మరియు ప్రయాణ సందర్భంలో, వినియోగదారుని స్థల అవసరాలు మరియు ప్రాధాన్యతల ఆధారంగా, సరైన హోటల్ ఎంపికలను సిఫార్సు చేయండి, హోటల్ ఐడి, పేరు, రేటింగ్, స్టార్ ర్యాంకింగ్, చిరునామా, ట్యాగ్‌లతో సహా హోటల్ యొక్క ప్రాథమిక సమాచారాన్ని అందించండి",
        "preconditions": "వినియోగదారుడు హోటల్ బుక్ చేయకోరుకున్నప్పుడు, హోటల్‌కు సంబంధించిన కీవర్డ్‌లు లేదా స్థలాన్ని అందించినప్పుడు",
        "postconditions": "అర్హత కలిగిన హోటల్‌ల జాబితాను తిరిగి ఇవ్వండి, హోటల్ వివరాలు (గదుల జాబితా, ధరలు మొదలైనవి) చూడాలంటే హోటల్ వివరాల క్వెరీ సాధనాన్ని ఉపయోగించాలి, వినియోగదారుని హోటల్ ఎంచుకోవడానికి మార్గనిర్దేశం చేయండి",
        "args": {
            "city_name": "నగరం పేరు",
            "key_words": "శోధన కీవర్డ్‌లు (హోటల్ పేరు, హోటల్ పరిచయం మొదలైనవాటితో సరిపోలుస్తాయి)"
        },
        "returns": "హోటల్ ప్రాథమిక సమాచారాన్ని నిర్మాణాత్మకంగా అవుట్‌పుట్ చేయండి",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "వినియోగదారుని స్థల అవసరాలు మరియు ప్రాధాన్యతల ఆధారంగా, సరైన పర్యాటక ప్రదేశాల ఎంపికలను సిఫార్సు చేస్తుంది, పర్యాటక ప్రదేశం యొక్క ప్రాథమిక సమాచారాన్ని అందిస్తుంది, ఇందులో పర్యాటక ప్రదేశం ఐడి, పేరు, చిరునామా, వివరణ, రేటింగ్, తెరిచే సమయం ఉంటాయి",
        "preconditions": "వినియోగదారుడు పర్యాటక ప్రదేశాన్ని బుక్ చేయాలని కోరుకుంటారు, పర్యాటక ప్రదేశానికి సంబంధించిన కీవర్డ్‌లు లేదా స్థలాలను అందిస్తారు",
        "postconditions": "అర్హత ఉన్న పర్యాటక ప్రదేశాల జాబితాను తిరిగి ఇస్తుంది, పర్యాటక ప్రదేశం వివరాలను (టికెట్ల జాబితా, ధరలు మొదలైనవి) చూడాలంటే పర్యాటక ప్రదేశం వివరాల క్వెరీ సాధనాన్ని ఉపయోగించాలి, వినియోగదారుని పర్యాటక ప్రదేశాన్ని ఎంచుకోవడానికి మార్గనిర్దేశం చేస్తుంది",
        "args": {
            "city_name": "నగరం పేరు",
            "key_words": "శోధన కీవర్డ్‌లు (పర్యాటక ప్రదేశం పేరు, స్థలం, చిరునామా, లక్షణాలు మొదలైనవాటితో సరిపోలుస్తాయి)"
        },
        "returns": "పర్యాటక ప్రదేశం ప్రాథమిక సమాచారం యొక్క నిర్మాణాత్మక అవుట్‌పుట్",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "వినియోగదారుని స్థల అవసరాలు మరియు ప్రాధాన్యతల ఆధారంగా, సరైన విమాన ఎంపికలను సిఫార్సు చేయండి, విమాన ప్రాథమిక సమాచారాన్ని అందించండి, ఇందులో విమాన ఐడి, విమాన సంఖ్య, బయలుదేరు నగరం, చేరుకునే నగరం, బయలుదేరు విమానాశ్రయం స్థానం, చేరుకునే విమానాశ్రయం స్థానం, బయలుదేరు సమయం, చేరుకునే సమయం, విమాన ట్యాగ్‌లు ఉంటాయి.",
        "preconditions": "వినియోగదారుడు విమానం బుక్ చేయాలని కోరుకుంటాడు, విమానానికి సంబంధించిన కీవర్డ్‌లు లేదా స్థలాలను ఇస్తాడు.",
        "postconditions": "అర్హత ఉన్న విమానాల జాబితాను తిరిగి ఇవ్వండి, విమాన వివరాలను (సీటు రకాల జాబితా, ధర, తేదీలు మొదలైనవి) చూడాలంటే విమాన వివరాల క్వెరీ సాధనాన్ని ఉపయోగించాలి, వినియోగదారుని విమానాన్ని ఎంచుకోవడానికి మార్గనిర్దేశం చేయండి.",
        "args": {
            "departure": "బయలుదేరు నగరం",
            "destination": "గమ్యస్థాన నగరం"
        },
        "returns": "విమాన ప్రాథమిక సమాచారం యొక్క నిర్మాణాత్మక అవుట్‌పుట్",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "వినియోగదారుని స్థల అవసరాలు మరియు ప్రాధాన్యతల ఆధారంగా, సరైన రైలు ఎంపికలను సిఫార్సు చేస్తుంది, రైలు టికెట్ల ప్రాథమిక సమాచారాన్ని అందిస్తుంది, ఇందులో రైలు ఐడి, రైలు సంఖ్య, బయలుదేరు నగరం, చేరుకునే నగరం, బయలుదేరు స్టేషన్ స్థానం, చేరుకునే స్టేషన్ స్థానం, బయలుదేరు సమయం, చేరుకునే సమయం, రైలు ట్యాగ్‌లు ఉంటాయి",
        "preconditions": "వినియోగదారుడు రైలు బుక్ చేయాలని కోరుకుంటాడు, రైలుకు సంబంధించిన కీవర్డ్‌లు లేదా స్థలాలను ఇస్తాడు",
        "postconditions": "అర్హత ఉన్న రైలు టికెట్ల జాబితాను తిరిగి ఇస్తుంది, రైలు టికెట్ వివరాలు (సీటు రకాల జాబితా, ధర, తేదీ మొదలైనవి) చూడాలంటే రైలు టికెట్ వివరాల క్వెరీ సాధనాన్ని ఉపయోగించాలి, వినియోగదారుని రైలు టికెట్ ఎంచుకోవడానికి మార్గనిర్దేశం చేస్తుంది",
        "args": {
            "departure": "బయలుదేరు నగరం",
            "destination": "గమ్యస్థాన నగరం",
            "date": "బయలుదేరు తేదీ"
        },
        "returns": "రైలు ప్రాథమిక సమాచారం యొక్క నిర్మాణాత్మక అవుట్‌పుట్",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "వినియోగదారుడు హోటల్ బుక్ చేసుకున్నప్పుడు, సిస్టమ్ వినియోగదారు అవసరాల ప్రకారం (హోటల్ పేరు, చెక్-ఇన్ తేదీ, వ్యక్తుల సంఖ్య మొదలైనవి) ఆర్డర్‌ను సృష్టిస్తుంది.",
        "preconditions": "వినియోగదారు లాగిన్ అయ్యి చెల్లుబాటు అయ్యే గుర్తింపును (user_id) అందించాలి, వినియోగదారు చెల్లుబాటు అయ్యే హోటల్ పేరు (hotel_name) మరియు రూమ్ రకం (room_type) అందించాలి, సిస్టమ్‌లో లక్ష్య హోటల్ సమాచారం ఉండాలి, మరియు ఆ హోటల్‌లో కోరిన తేదీలలో గదులు అందుబాటులో ఉండాలి.",
        "postconditions": "ఆర్డర్ సృష్టించబడుతుంది, వినియోగదారు చెల్లింపును నిర్ధారించమని అడగబడుతుంది.",
        "args": {
            "hotel_id": "హోటల్ ID",
            "room_id": "రూమ్ ID",
            "user_id": "వినియోగదారు ID"
        },
        "returns": "ఆర్డర్ సృష్టించే చర్య యొక్క ఫీడ్‌బ్యాక్ అవుట్‌పుట్",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "వినియోగదారులు ఆకర్షణ మరియు తేదీ ఆధారంగా టికెట్లను కొనుగోలు చేస్తారు, వ్యవస్థ టికెట్ సంబంధిత సమాచారాన్ని అందించి ఆర్డర్ చేస్తుంది.",
        "preconditions": "ఆకర్షణ పర్యాటక సందర్భంలో, వినియోగదారుడు ఆకర్షణను రిజర్వ్ చేయడానికి అభ్యర్థిస్తాడు, రిజర్వేషన్‌కు అవసరమైన సమాచారాన్ని అందిస్తాడు.",
        "postconditions": "ఆర్డర్ సృష్టించబడింది, వినియోగదారు చెల్లింపును నిర్ధారించమని అడగండి.",
        "args": {
            "attraction_id": "ఆకర్షణ ID",
            "ticket_id": "టికెట్ ID",
            "user_id": "వినియోగదారు ID",
            "date": "సందర్శన తేదీ, ఫార్మాట్ %Y-%m-%d",
            "quantity": "పరిమాణం"
        },
        "returns": "ఆర్డర్ సృష్టించే చర్య యొక్క ఫీడ్‌బ్యాక్ అవుట్‌పుట్",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "వినియోగదారులు విమాన సంఖ్య, తేదీ, సీటు రకం మరియు సంఖ్య ఆధారంగా విమాన టికెట్లను కొనుగోలు చేస్తారు, వ్యవస్థ టికెట్ సంబంధిత సమాచారాన్ని అందించి ఆర్డర్‌ను పూర్తి చేస్తుంది.",
        "preconditions": "విమాన టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, వినియోగదారుడు విమానాన్ని బుక్ చేయడానికి అభ్యర్థించి, బుకింగ్‌కు అవసరమైన సమాచారాన్ని అందిస్తారు.",
        "postconditions": "ఆర్డర్ సృష్టించబడింది, వినియోగదారు చెల్లింపును నిర్ధారించమని కోరబడతారు.",
        "args": {
            "flight_id": "విమాన ID",
            "seat_id": "సీటు ID",
            "user_id": "వినియోగదారుడు ID",
            "date": "ప్రయాణ తేదీ",
            "quantity": "సంఖ్య"
        },
        "returns": "ఆర్డర్ సృష్టించే చర్య యొక్క ఫీడ్‌బ్యాక్ అవుట్‌పుట్.",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "వినియోగదారులు రైలు నంబర్, తేదీ, సీటు రకం మరియు సంఖ్య ఆధారంగా రైలు టికెట్లను కొనుగోలు చేస్తారు, వ్యవస్థ రైలు టికెట్కు సంబంధించిన సమాచారాన్ని అందించి ఆర్డర్ చేస్తుంది.",
        "preconditions": "రైలు టికెట్ క్వెరీ మరియు కొనుగోలు సందర్భంలో, వినియోగదారుడు రైలును బుక్ చేయడానికి అభ్యర్థిస్తాడు మరియు బుకింగ్‌కు అవసరమైన సమాచారాన్ని అందిస్తాడు.",
        "postconditions": "ఆర్డర్ సృష్టించబడింది, వినియోగదారు చెల్లింపును నిర్ధారించమని అడగండి.",
        "args": {
            "train_id": "రైలు గుర్తింపు సంఖ్య",
            "seat_id": "సీటు గుర్తింపు సంఖ్య",
            "user_id": "వినియోగదారు గుర్తింపు సంఖ్య",
            "date": "ప్రయాణ తేదీ",
            "quantity": "సంఖ్య"
        },
        "returns": "ఆర్డర్ సృష్టించే చర్యకు సంబంధించిన ఫీడ్‌బ్యాక్ అవుట్‌పుట్",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "వినియోగదారుడు హోటల్ ఆర్డర్‌కు చెల్లింపు చేస్తారు",
        "preconditions": "హోటల్ బుకింగ్ సందర్భంలో, వినియోగదారుడు హోటల్ ఆర్డర్‌కు చెల్లింపు చేయాలని కోరుతున్నారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది",
        "postconditions": "చెల్లింపును నిర్ధారించి, ఆర్డర్ స్థితిని చెల్లించబడినదిగా నవీకరించండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "వినియోగదారుడు టికెట్ ఆర్డర్‌కు చెల్లింపు చేస్తారు",
        "preconditions": "పర్యాటక ప్రదేశ సందర్భంలో, వినియోగదారుడు టికెట్ ఆర్డర్ చెల్లింపును కోరుతారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది",
        "postconditions": "చెల్లింపును నిర్ధారించి, ఆర్డర్ స్థితిని చెల్లించబడినదిగా నవీకరించండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "వినియోగదారుడు విమాన టికెట్ ఆర్డర్ చెల్లింపును నిర్వహిస్తారు",
        "preconditions": "విమాన టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, వినియోగదారుడు విమాన ఆర్డర్ చెల్లింపును కోరుకుంటారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది",
        "postconditions": "చెల్లింపును నిర్ధారించండి మరియు ఆర్డర్ స్థితిని చెల్లించబడిందిగా నవీకరించండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "వినియోగదారు రైలు టికెట్ ఆర్డర్‌కు చెల్లింపు చేస్తారు",
        "preconditions": "రైలు టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, వినియోగదారు రైలు టికెట్ ఆర్డర్‌కు చెల్లింపు చేయడానికి అభ్యర్థిస్తారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది",
        "postconditions": "చెల్లింపును నిర్ధారించి, ఆర్డర్ స్థితిని చెల్లించబడిందిగా నవీకరించండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ"
        },
        "returns": "చెల్లింపు ఫలిత సమాచారం",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "వినియోగదారు ID ఆధారంగా, వినియోగదారు యొక్క హోటల్ ఆర్డర్‌లను విచారించండి, ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, హోటల్ ID, ఆర్డర్ మొత్తం ధర, ఆర్డర్ చేసిన సమయం, నవీకరించిన సమయం మరియు ఆర్డర్ స్థితిని కలిగి ఉన్న సమాచారాన్ని తిరిగి ఇవ్వండి",
        "preconditions": "వినియోగదారు అవసరం హోటల్ ఆర్డర్‌లను విచారించడం",
        "postconditions": "ఆర్డర్ సమాచారాన్ని తిరిగి ఇవ్వండి, తర్వాత సవరించడానికి/రద్దు చేయడానికి వీలుగా",
        "args": {
            "user_id": "వినియోగదారు ID",
            "date": "తేదీ",
            "status": "ఆర్డర్ స్థితి"
        },
        "returns": "నిర్దిష్ట వినియోగదారు యొక్క హోటల్ ఆర్డర్ సమాచారం",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "వినియోగదారు ఐడి ఆధారంగా వినియోగదారు పర్యాటక ప్రదేశ టికెట్ ఆర్డర్లను విచారించండి, ఆర్డర్ ఐడి, ఆర్డర్ రకం, వినియోగదారు ఐడి, పర్యాటక ప్రదేశ ఐడి, ఆర్డర్ మొత్తం ధర, ఆర్డర్ చేసిన సమయం, నవీకరణ సమయం మరియు ఆర్డర్ స్థితిని కలిగి ఉన్న సమాచారాన్ని తిరిగి ఇస్తుంది.",
        "preconditions": "వినియోగదారు అవసరం పర్యాటక ప్రదేశ టికెట్ ఆర్డర్లను విచారించడం.",
        "postconditions": "ఆర్డర్ సమాచారాన్ని అందిస్తుంది, తర్వాత సవరణ లేదా రద్దు చేయడానికి అనుకూలంగా ఉంటుంది.",
        "args": {
            "user_id": "వినియోగదారు ఐడి",
            "date": "తేదీ",
            "status": "ఆర్డర్ స్థితి"
        },
        "returns": "నిర్దిష్ట వినియోగదారు యొక్క పర్యాటక ప్రదేశ టికెట్ ఆర్డర్ సమాచారం.",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "వినియోగదారుని ID ఆధారంగా వినియోగదారుని విమాన టికెట్ ఆర్డర్‌ను విచారించండి. ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారుని ID, విమాన ID, ఆర్డర్ మొత్తం ధర, ఆర్డర్ చేసిన సమయం, నవీకరణ సమయం మరియు ఆర్డర్ స్థితిని కలిగిన సమాచారాన్ని తిరిగి ఇవ్వండి.",
        "preconditions": "వినియోగదారి విమాన టికెట్ ఆర్డర్‌లను విచారించాలనుకుంటున్నారు.",
        "postconditions": "ఆర్డర్ సమాచారాన్ని అందించండి, తరువాత సవరణ లేదా రద్దు చేయడానికి వీలుగా.",
        "args": {
            "user_id": "వినియోగదారుని ID",
            "date": "తేదీ",
            "status": "ఆర్డర్ స్థితి"
        },
        "returns": "నిర్దిష్ట వినియోగదారి యొక్క విమాన టికెట్ ఆర్డర్ సమాచారం.",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "వినియోగదారు ID ఆధారంగా వినియోగదారు యొక్క రైలు టికెట్ ఆర్డర్‌లను సెర్చ్ చేస్తుంది, ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, రైలు ID, ఆర్డర్ మొత్తం ధర, ఆర్డర్ చేసిన సమయం, నవీకరణ సమయం మరియు ఆర్డర్ స్థితి వివరాలను తిరిగి ఇస్తుంది.",
        "preconditions": "వినియోగదారు రైలు టికెట్ ఆర్డర్‌లను సెర్చ్ చేయాలనుకుంటున్నారు",
        "postconditions": "ఆర్డర్ సమాచారాన్ని అందిస్తుంది, తర్వాత సవరణ లేదా రద్దు చేయడానికి వీలు కల్పిస్తుంది",
        "args": {
            "user_id": "వినియోగదారు ID",
            "date": "తేదీ",
            "status": "ఆర్డర్ స్థితి"
        },
        "returns": "నిర్దిష్ట వినియోగదారు యొక్క రైలు టికెట్ ఆర్డర్ సమాచారం",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "హోటల్ ఆర్డర్ వివరాలను పొందండి, ఇందులో ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, హోటల్ ID, మొత్తం ఆర్డర్ ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు ఆర్డర్ గది వివరాలు (గది రకం, చెక్-ఇన్ తేదీ, ధర, గది ID) ఉంటాయి",
        "preconditions": "వినియోగదారు హోటల్ ఆర్డర్ వివరాలను పొందడానికి కోరుకుంటారు, మునుపటి సందర్భంలో ఆర్డర్ ID నిర్ధారించబడింది",
        "postconditions": "ఆర్డర్ వివరాలను తిరిగి ఇస్తుంది",
        "args": {
            "order_id": "ఆర్డర్ ID"
        },
        "returns": "ఆర్డర్ వివరాలు",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "ఆకర్షణ టికెట్ ఆర్డర్ వివరాలను పొందండి, ఇందులో ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, ఆకర్షణ ID, మొత్తం ఆర్డర్ ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు ఆర్డర్ ఆకర్షణ వివరణాత్మక సమాచారం (టికెట్ రకం, తేదీ, ధర, టికెట్ ID) ఉంటాయి",
        "preconditions": "వినియోగదారు ఆకర్షణ టికెట్ ఆర్డర్ వివరాలను పొందాలని కోరుతున్నారు, పైన ఆర్డర్ ID నిర్ధారించబడింది",
        "postconditions": "ఆర్డర్ వివరాలను తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ ID"
        },
        "returns": "ఆర్డర్ వివరాలు",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "విమాన టికెట్ ఆర్డర్ వివరాలను పొందండి, ఇందులో ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, విమాన ID, మొత్తం ఆర్డర్ ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు ఆర్డర్ టికెట్ వివరణాత్మక సమాచారం (సీటు రకం, తేదీ, ధర, సీటు ID) ఉంటాయి",
        "preconditions": "వినియోగదారు విమాన టికెట్ ఆర్డర్ వివరాలను పొందడానికి అభ్యర్థించారు, పైన ఆర్డర్ ID నిర్ధారించబడింది",
        "postconditions": "ఆర్డర్ వివరాలను తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ ID"
        },
        "returns": "ఆర్డర్ వివరాలు",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "రైలు టికెట్ ఆర్డర్ వివరాలను పొందండి, ఇందులో ఆర్డర్ ID, ఆర్డర్ రకం, వినియోగదారు ID, రైలు ID, ఆర్డర్ మొత్తం ధర, ఆర్డర్ సమయం, నవీకరణ సమయం, ఆర్డర్ స్థితి మరియు ఆర్డర్ రైలు టికెట్ వివరణాత్మక సమాచారం (సీటు రకం, తేదీ, ధర, సీటు ID) ఉంటాయి",
        "preconditions": "వినియోగదారు రైలు టికెట్ ఆర్డర్ వివరాలను పొందడానికి అభ్యర్థించారు, పైన ఆర్డర్ ID నిర్ణయించబడింది",
        "postconditions": "ఆర్డర్ వివరాలను తిరిగి ఇవ్వండి",
        "args": {
            "order_id": "ఆర్డర్ ID"
        },
        "returns": "ఆర్డర్ వివరాలు",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "రైలు టికెట్ ఆర్డర్‌ను సవరించండి, ప్రయాణ తేదీని మార్చడానికి మద్దతు ఇస్తుంది, ధర తేడాను చెల్లించడం లేదా తిరిగి చెల్లించడం స్వయంచాలకంగా నిర్వహిస్తుంది.",
        "preconditions": "రైలు టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, వినియోగదారు రైలు టికెట్ ఆర్డర్‌ను సవరించమని కోరుకుంటారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది.",
        "postconditions": "ఆర్డర్‌ను సవరించి ఆర్డర్ స్థితిని నవీకరించండి, ధర తేడాను చెల్లించాల్సి వస్తే, ఆర్డర్ స్థితిని unpaid గా మార్చండి, లేదంటే అసలు స్థితిని ఉంచండి, ధర తేడాను చెల్లించాల్సి వస్తే, వినియోగదారును ఈ ఆర్డర్‌ను చెల్లించమని మార్గనిర్దేశం చేయాలి.",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ",
            "user_id": "వినియోగదారు ఐడీ",
            "new_date": "కొత్త ప్రయాణ తేదీ, ఫార్మాట్ %Y-%m-%d"
        },
        "returns": "(సవరించిన ఆర్డర్ వివరాలు, ధర తేడా, ధనాత్మకం అంటే తేడాను చెల్లించాలి, రుణాత్మకం అంటే తేడాను తిరిగి చెల్లిస్తారు)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "విమాన టికెట్ ఆర్డర్‌ను సవరించండి, బయలుదేరు తేదీని మార్చడానికి మద్దతు ఇస్తుంది, ధర తేడాను చెల్లించడం లేదా తిరిగి చెల్లించడం స్వయంచాలకంగా నిర్వహిస్తుంది.",
        "preconditions": "విమాన టికెట్ శోధన మరియు కొనుగోలు సందర్భంలో, వినియోగదారు విమాన టికెట్ ఆర్డర్‌ను సవరించమని కోరుకుంటారు, పైన ఆర్డర్ ID నిర్ణయించబడింది",
        "postconditions": "ఆర్డర్‌ను సవరించి ఆర్డర్ స్థితిని నవీకరించండి, ధర తేడాను చెల్లించాల్సి ఉంటే, ఆర్డర్ స్థితిని unpaid గా మార్చండి, లేకపోతే అసలు స్థితిని ఉంచండి, ధర తేడాను చెల్లించాల్సి ఉంటే, వినియోగదారును ఈ ఆర్డర్‌ను చెల్లించమని మార్గనిర్దేశం చేయాలి",
        "args": {
            "order_id": "ఆర్డర్ ID",
            "user_id": "వినియోగదారు ID",
            "new_date": "కొత్త బయలుదేరు తేదీ, ఫార్మాట్ %Y-%m-%d"
        },
        "returns": "(సవరించిన ఆర్డర్ కంటెంట్, ధర తేడా, ధనాత్మకం అంటే తేడాను చెల్లించాలి, రుణాత్మకం అంటే తేడాను తిరిగి చెల్లించాలి)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "వినియోగదారు బుక్ చేసిన హోటల్ ఆర్డర్‌ను రద్దు చేస్తారు",
        "preconditions": "హోటల్ బుకింగ్ విచారణ సందర్భంలో, వినియోగదారు హోటల్ ఆర్డర్‌ను రద్దు చేయాలని కోరుకుంటారు, మునుపటి సందర్భంలో ఆర్డర్ ఐడీ నిర్ధారించబడింది",
        "postconditions": "ఆర్డర్‌ను రద్దు చేసి ఆర్డర్ స్థితిని నవీకరించండి, ధర తేడాను తిరిగి చెల్లించాల్సి వస్తే, వినియోగదారుకు తెలియజేయండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడీ",
            "user_id": "వినియోగదారు ఐడీ"
        },
        "returns": "ఆర్డర్ రద్దుపై తిరిగి చెల్లించే మొత్తం",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "వినియోగదారు బుక్ చేసిన ఆకర్షణ టికెట్ ఆర్డర్‌ను రద్దు చేస్తారు",
        "preconditions": "గత సంభాషణలో ఆర్డర్ ఐడి ఉండాలి లేదా ఆర్డర్ విచారణ ఇప్పటికే జరిగి ఉండాలి, వినియోగదారుకు ఈ ఆర్డర్‌ను రద్దు చేయడానికి అనుమతి ఉండాలి",
        "postconditions": "ధర తేడాను రీఫండ్ చేస్తే, వినియోగదారుకు తెలియజేయాలి",
        "args": {
            "order_id": "ఆర్డర్ ఐడి",
            "user_id": "వినియోగదారు ఐడి"
        },
        "returns": "ఆర్డర్ రద్దు చేయడానికి రీఫండ్ మొత్తం",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "వినియోగదారు బుక్ చేసిన విమాన టికెట్ ఆర్డర్‌ను రద్దు చేస్తారు",
        "preconditions": "గత సంభాషణలో ఆర్డర్ ఐడి ఉండాలి లేదా ఆర్డర్ విచారణ ఇప్పటికే జరిగి ఉండాలి, వినియోగదారుకు ఈ ఆర్డర్‌ను రద్దు చేయడానికి అనుమతి ఉండాలి",
        "postconditions": "ధర తేడాను రీఫండ్ చేస్తే, వినియోగదారుకు తెలియజేయాలి",
        "args": {
            "order_id": "ఆర్డర్ ఐడి",
            "user_id": "వినియోగదారు ఐడి"
        },
        "returns": "ఆర్డర్ రద్దు చేయడానికి రీఫండ్ మొత్తం",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "వినియోగదారుడు బుక్ చేసుకున్న రైలు టికెట్ ఆర్డర్‌ను రద్దు చేస్తారు",
        "preconditions": "గత సంభాషణలో ఆర్డర్ ఐడి ఉండాలి లేదా ఆర్డర్ విచారణ ఇప్పటికే జరిగి ఉండాలి, వినియోగదారుకు ఈ ఆర్డర్‌ను రద్దు చేయడానికి అనుమతి ఉండాలి",
        "postconditions": "ధర తేడాను తిరిగి చెల్లిస్తే, వినియోగదారుకు తెలియజేయండి",
        "args": {
            "order_id": "ఆర్డర్ ఐడి",
            "user_id": "వినియోగదారు ఐడి"
        },
        "returns": "ఆర్డర్ రద్దుపై తిరిగి చెల్లించే మొత్తం",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Tamil version
TOOL_DESCRIPTIONS_TA = {
    "get_ota_hotel_info": {
        "description": "ஹோட்டல் தகவலைப் பெறுகிறது, ஹோட்டல் ஐடி, பெயர், மதிப்பீடு, நட்சத்திர தரம், முகவரி, குறிச்சொற்கள் மற்றும் அறை பட்டியல் ஆகியவற்றை உள்ளடக்கியது",
        "preconditions": "ஹோட்டல் விசாரணை மற்றும் முன்பதிவு சூழலில், ஹோட்டலின் விரிவான தகவலைப் பெற வேண்டும்",
        "postconditions": "ஹோட்டலின் விரிவான தகவலைத் வழங்குகிறது, அறையைத் தேர்ந்தெடுத்து ஆர்டர் செய்ய பயனரை வழிநடத்துகிறது",
        "args": {
            "hotel_id": "ஹோட்டல் ஐடி"
        },
        "returns": "ஹோட்டல் தகவல்",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "சுற்றுலாத் தலத்தின் தகவல்களைப் பெறுகிறது; இதில் சுற்றுலாத் தலத்தின் ஐடி, பெயர், முகவரி, விளக்கம், மதிப்பீடு, திறப்பு நேரம், டிக்கெட் விலை மற்றும் டிக்கெட் வகைகளின் பட்டியல் ஆகியவை அடங்கும்.",
        "preconditions": "சுற்றுலாத் தலச் சூழலில், சுற்றுலாத் தலத்தின் விரிவான தகவல்களைப் பெற வேண்டும்.",
        "postconditions": "சுற்றுலாத் தலத்தின் விரிவான தகவல்களைத் திருப்பி அனுப்புகிறது, பயனர் டிக்கெத்தைத் தேர்ந்தெடுத்து ஆர்டர் செய்ய வழிநடத்துகிறது.",
        "args": {
            "attraction_id": "சுற்றுலாத் தலத்தின் ஐடி"
        },
        "returns": "சுற்றுலாத் தலத்தின் தகவல்",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "விமானத் தகவலைப் பெறுகிறது, இதில் விமான ஐடி, விமான எண், புறப்படும் நகரம், சென்றடையும் நகரம், புறப்படும் விமான நிலைய இருப்பிடம், சென்றடையும் விமான நிலைய இருப்பிடம், புறப்படும் நேரம், சென்றடையும் நேரம், விமான குறியீடுகள், இருக்கை வகை பட்டியல் ஆகியவை அடங்கும்.",
        "preconditions": "விமான டிக்கெட் விசாரணை மற்றும் கொள்முதல் சூழலில், விமானத்தின் விரிவான தகவலைப் பெற வேண்டும்.",
        "postconditions": "விமானத்தின் விரிவான தகவலைத் திருப்பி அனுப்புகிறது, பயனர் இருக்கையைத் தேர்ந்தெடுத்து ஆர்டர் செய்ய வழிநடத்துகிறது.",
        "args": {
            "flight_id": "விமான ஐடி"
        },
        "returns": "விமானத் தகவல்",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ரயில் தகவலைப் பெறுகிறது, இதில் ரயில் ஐடி, ரயில் எண், புறப்படும் நகரம், சேரும் நகரம், புறப்படும் நிலையம் இருப்பிடம், சேரும் நிலையம் இருப்பிடம், புறப்படும் நேரம், சேரும் நேரம், ரயில் குறியீடுகள், இருக்கை வகைகள் பட்டியல் ஆகியவை அடங்கும்.",
        "preconditions": "ரயில் டிக்கெட் விசாரணை மற்றும் வாங்கும் சூழலில், ரயிலின் விரிவான தகவலைப் பெற வேண்டும்.",
        "postconditions": "ரயிலின் விரிவான தகவலைத் திருப்பி அளிக்கிறது, பயனர் இருக்கையைத் தேர்ந்தெடுத்து ஆர்டர் செய்ய வழிநடத்துகிறது.",
        "args": {
            "train_id": "ரயில் ஐடி"
        },
        "returns": "ரயில் தகவல்",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "பயண மற்றும் விடுதி சூழலில், பயனரின் இடத் தேவைகள் மற்றும் விருப்பத்தேர்வுகளின் அடிப்படையில், பொருத்தமான விடுதி விருப்பங்களைப் பரிந்துரைக்கிறது, விடுதி ஐடி, பெயர், மதிப்பீடு, நட்சத்திர தரம், முகவரி, குறிச்சொற்கள் உட்பட விடுதியின் அடிப்படைத் தகவல்களை வழங்குகிறது",
        "preconditions": "பயனர் விடுதி ஒன்றை முன்பதிவு செய்யக் கோருகிறார், விடுதி சார்ந்த முக்கிய சொற்கள் அல்லது இடத்தை வழங்குகிறார்",
        "postconditions": "நிபந்தனைகளுக்கு ஏற்ப விடுதி பட்டியலைத் திருப்பி அளிக்கிறது, விடுதி விவரங்களை (அறை பட்டியல், விலை போன்றவை) பார்க்க வேண்டும் என்றால் விடுதி விவர வினவல் கருவியைப் பயன்படுத்த வேண்டும், பயனரை விடுதியைத் தேர்ந்தெடுக்க வழிநடத்துகிறது",
        "args": {
            "city_name": "நகரத்தின் பெயர்",
            "key_words": "தேடல் முக்கிய சொற்கள் (விடுதி பெயர், விடுதி அறிமுகம் போன்றவற்றுடன் பொருத்தும்)"
        },
        "returns": "விடுதியின் அடிப்படைத் தகவல்களை கட்டமைக்கப்பட்ட வடிவில் வெளியிடுகிறது",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "பயனரின் இடத் தேவைகள் மற்றும் விருப்பத்தேர்வுகளின் அடிப்படையில், பொருத்தமான சுற்றுலாத் தலங்களைப் பரிந்துரைக்கிறது, சுற்றுலாத் தலத்தின் அடிப்படைத் தகவல்களை வழங்குகிறது, சுற்றுலாத் தலத்தின் ஐடி, பெயர், முகவரி, விளக்கம், மதிப்பீடு, திறந்திருக்கும் நேரம் ஆகியவற்றை உள்ளடக்கியது",
        "preconditions": "பயனர் ஒரு சுற்றுலாத் தலத்தை முன்பதிவு செய்யக் கோருகிறார், சுற்றுலாத் தலத்துடன் தொடர்புடைய முக்கிய சொற்கள் அல்லது இடத்தை வழங்குகிறார்",
        "postconditions": "நிபந்தனைகளைப் பூர்த்தி செய்யும் சுற்றுலாத் தலங்களின் பட்டியலைத் திருப்பி அளிக்கிறது, சுற்றுலாத் தலத்தின் விவரங்களைப் (டிக்கெட் பட்டியல், விலை போன்றவை) பார்க்க விரும்பினால் சுற்றுலாத் தல விவர வினவல் கருவியைப் பயன்படுத்த வேண்டும், பயனரை சுற்றுலாத் தலத்தைத் தேர்ந்தெடுக்க வழிநடத்துகிறது",
        "args": {
            "city_name": "நகரத்தின் பெயர்",
            "key_words": "தேடல் முக்கிய சொற்கள் (சுற்றுலாத் தலத்தின் பெயர், இடம், முகவரி, சிறப்பம்சங்கள் போன்றவற்றைப் பொருத்துகிறது)"
        },
        "returns": "சுற்றுலாத் தலத்தின் அடிப்படைத் தகவல்களை கட்டமைக்கப்பட்ட வெளியீடாக வழங்குகிறது",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "பயனரின் இடத் தேவைகள் மற்றும் விருப்பத்தின் அடிப்படையில், பொருத்தமான விமான விருப்பங்களைப் பரிந்துரைக்கிறது, விமான அடையாளம், விமான எண், புறப்படும் நகரம், சென்றடையும் நகரம், புறப்படும் விமான நிலைய இருப்பிடம், சென்றடையும் விமான நிலைய இருப்பிடம், புறப்படும் நேரம், சென்றடையும் நேரம், விமான குறிச்சொற்கள் ஆகியவற்றை உள்ளடக்கிய விமானத்தின் அடிப்படைத் தகவல்களை வழங்குகிறது.",
        "preconditions": "பயனர் ஒரு விமானத்தை முன்பதிவு செய்யக் கோருகிறார், விமானம் சார்ந்த முக்கிய சொற்கள் அல்லது இடங்களை வழங்குகிறார்.",
        "postconditions": "நிபந்தனைகளை பூர்த்தி செய்யும் விமானங்களின் பட்டியலைத் திருப்பி அளிக்கிறது, விமான விவரங்களைப் (இருக்கை வகை பட்டியல், விலை, தேதி போன்றவை) பார்க்க வேண்டும் என்றால் விமான விவர வினவல் கருவியைப் பயன்படுத்த வேண்டும், பயனரை விமானத்தைத் தேர்ந்தெடுக்க வழிநடத்தும்.",
        "args": {
            "departure": "புறப்படும் நகரம்",
            "destination": "இலக்கு நகரம்"
        },
        "returns": "விமான அடிப்படைத் தகவல்களை கட்டமைக்கப்பட்ட வெளியீடாக வழங்குகிறது",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "பயனரின் இடத் தேவைகள் மற்றும் விருப்பத்தேர்வுகளின் அடிப்படையில், பொருத்தமான ரயில் விருப்பங்களைப் பரிந்துரைக்கிறது, ரயில் டிக்கெட்டின் அடிப்படைத் தகவல்களை வழங்குகிறது, ரயில் ஐடி, ரயில் எண், புறப்படும் நகரம், சென்றடையும் நகரம், புறப்படும் நிலையம் இருப்பிடம், சென்றடையும் நிலையம் இருப்பிடம், புறப்படும் நேரம், சென்றடையும் நேரம், ரயில் குறிச்சொற்கள் ஆகியவற்றை உள்ளடக்கியது",
        "preconditions": "பயனர் ரயில் புக் செய்யக் கோருகிறார், ரயில் தொடர்பான முக்கிய சொற்கள் அல்லது இடங்களை வழங்குகிறார்",
        "postconditions": "நிபந்தனைகளை பூர்த்தி செய்யும் ரயில் டிக்கெட்டுகளின் பட்டியலைத் திருப்பி அளிக்கிறது, ரயில் டிக்கெட் விவரங்களை (இருக்கை வகை பட்டியல், விலை, தேதி போன்றவை) பார்க்க வேண்டும் என்றால் ரயில் டிக்கெட் விவர வினவல் கருவியைப் பயன்படுத்த வேண்டும், பயனரை ரயில் டிக்கெத்தைத் தேர்ந்தெடுக்க வழிநடத்துகிறது",
        "args": {
            "departure": "புறப்படும் நகரம்",
            "destination": "சென்றடையும் நகரம்",
            "date": "புறப்படும் தேதி"
        },
        "returns": "ரயில் அடிப்படைத் தகவல்களின் கட்டமைக்கப்பட்ட வெளியீடு",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "பயனர் ஒரு ஹோட்டலை முன்பதிவு செய்யும் போது, அமைப்பு பயனரின் தேவைகளின் அடிப்படையில் (ஹோட்டல் பெயர், தங்கும் தேதி, நபர்களின் எண்ணிக்கை போன்றவை) ஒரு ஆர்டரை உருவாக்குகிறது",
        "preconditions": "பயனர் உள்நுழைந்து செல்லுபடியாகும் அடையாளத்தை (user_id) வழங்கியுள்ளார், பயனர் செல்லுபடியாகும் ஹோட்டல் பெயர் (hotel_name) மற்றும் அறை வகை (room_type) ஆகியவற்றை வழங்கியுள்ளார், அமைப்பில் இலக்கு ஹோட்டல் பற்றிய தகவல் உள்ளது, மேலும் கேட்கப்பட்ட தேதிகளில் அந்த ஹோட்டலில் அறைகள் கிடைக்கின்றன",
        "postconditions": "ஆர்டரை உருவாக்கி, பயனரை கட்டணத்தை உறுதிப்படுத்தக் கோரவும்",
        "args": {
            "hotel_id": "ஹோட்டல் ஐடி",
            "room_id": "அறை ஐடி",
            "user_id": "பயனர் ஐடி"
        },
        "returns": "ஆர்டரை உருவாக்கும் செயல்பாட்டின் பின்னூட்ட வெளியீடு",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "பயனர்கள் சுற்றுலா தலம் மற்றும் தேதியின் அடிப்படையில் டிக்கெட்டுகளை வாங்குகிறார்கள், அமைப்பு டிக்கெட் தொடர்பான தகவல்களை வழங்கி ஆர்டரை உருவாக்குகிறது.",
        "preconditions": "சுற்றுலா தல சூழலில், பயனர் சுற்றுலா தலத்தை முன்பதிவு செய்யக் கோரி, முன்பதிவுக்கான அவசியமான தகவல்களை வழங்குகிறார்.",
        "postconditions": "ஆர்டர் உருவாக்கப்படுகிறது, பயனர் கட்டணத்தை உறுதிப்படுத்த அழைக்கப்படுகிறார்.",
        "args": {
            "attraction_id": "சுற்றுலா தல ஐடி",
            "ticket_id": "டிக்கெட் ஐடி",
            "user_id": "பயனர் ஐடி",
            "date": "பார்வை தேதி, வடிவம் %Y-%m-%d",
            "quantity": "அளவு"
        },
        "returns": "ஆர்டர் உருவாக்க செயல்பாட்டிற்கான பின்னூட்ட வெளியீடு",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "பயனர்கள் விமான எண், தேதி, இருக்கை வகை மற்றும் எண்ணிக்கையின் அடிப்படையில் விமான டிக்கெட்டுகளை வாங்குகிறார்கள்; அமைப்பு டிக்கெட் தொடர்பான தகவல்களை வழங்கி ஆர்டரை மேற்கொள்கிறது.",
        "preconditions": "விமான டிக்கெட் விசாரணை மற்றும் கொள்முதல் சூழலில், பயனர் ஒரு விமானத்தை முன்பதிவு செய்யக் கோருகிறார் மற்றும் முன்பதிவு தொடர்பான அவசியமான தகவல்களை வழங்குகிறார்.",
        "postconditions": "ஆர்டர் உருவாக்கப்பட்டது, பயனர் கட்டணத்தை உறுதிப்படுத்தவும்.",
        "args": {
            "flight_id": "விமான ஐடி",
            "seat_id": "இருக்கை ஐடி",
            "user_id": "பயனர் ஐடி",
            "date": "புறப்படும் தேதி",
            "quantity": "எண்ணிக்கை"
        },
        "returns": "ஆர்டர் உருவாக்கும் செயல்பாட்டின் பின்னூட்ட வெளியீடு",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "பயனர்கள் ரயில் எண், தேதி, இருக்கை வகை மற்றும் எண்ணிக்கையின் அடிப்படையில் ரயில் டிக்கெட்டுகளை வாங்குகிறார்கள்; அமைப்பு ரயில் டிக்கெட் தொடர்பான தகவல்களை வழங்கி ஆர்டரை மேற்கொள்கிறது.",
        "preconditions": "ரயில் டிக்கெட் விசாரணை மற்றும் வாங்கும் சூழலில், பயனர் ரயிலை முன்பதிவு செய்யக் கோரி, முன்பதிவுக்கான அவசியமான தகவல்களை வழங்குகிறார்.",
        "postconditions": "ஆர்டர் உருவாக்கப்படுகிறது, பயனர் கட்டணத்தை உறுதிப்படுத்த வேண்டும்.",
        "args": {
            "train_id": "ரயில் ஐடி",
            "seat_id": "இருக்கை ஐடி",
            "user_id": "பயனர் ஐடி",
            "date": "புறப்படும் தேதி",
            "quantity": "எண்ணிக்கை"
        },
        "returns": "ஆர்டர் உருவாக்கம் செயல்பாட்டிற்கான பின்னூட்ட வெளியீடு",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "பயனர் ஹோட்டல் ஆர்டர் கட்டணத்தை செலுத்துதல்",
        "preconditions": "ஹோட்டல் முன்பதிவு விசாரணை சூழலில், பயனர் ஹோட்டல் ஆர்டர் கட்டணத்தை செலுத்தக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது",
        "postconditions": "கட்டணத்தை உறுதி செய்து, ஆர்டர் நிலையை செலுத்தப்பட்டது என புதுப்பிக்கவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "கட்டண முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "பயனர் டிக்கெட் ஆர்டர் கட்டணத்தை செலுத்துதல்",
        "preconditions": "சுற்றுலா தல சூழலில், பயனர் சுற்றுலா டிக்கெட் ஆர்டர் கட்டணத்தை செலுத்தக் கோருகிறார், முன்பே ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது",
        "postconditions": "கட்டணம் செலுத்தப்பட்டதை உறுதி செய்து, ஆர்டர் நிலையை 'கட்டணம் செலுத்தப்பட்டது' என புதுப்பிக்கவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "கட்டணம் செலுத்திய முடிவுத் தகவல்",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "பயனர் விமான டிக்கெட் ஆர்டர் கட்டணத்தை செலுத்துதல்",
        "preconditions": "விமான டிக்கெட் தேடல் மற்றும் கொள்முதல் சூழலில், பயனர் விமான ஆர்டருக்கு கட்டணம் செலுத்த கோருகிறார், முன்பே ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது",
        "postconditions": "கட்டணம் செலுத்தப்பட்டதை உறுதி செய்து, ஆர்டர் நிலையை 'செலுத்தப்பட்டது' என புதுப்பிக்கவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "கட்டணம் செலுத்தியதற்கான முடிவு தகவல்",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "பயனர் ரயில் டிக்கெட் ஆர்டருக்கு பணம் செலுத்துதல்",
        "preconditions": "ரயில் டிக்கெட் தேடல் மற்றும் வாங்கும் சூழலில், பயனர் ரயில் டிக்கெட் ஆர்டருக்கு பணம் செலுத்தக் கோருகிறார்; முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது",
        "postconditions": "பணம் செலுத்துவதை உறுதி செய்து, ஆர்டர் நிலையை 'செலுத்தப்பட்டது' என புதுப்பிக்கவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "பணம் செலுத்துதல் முடிவு விவரங்கள்",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "பயனர் ஐடியின் அடிப்படையில், பயனரின் ஹோட்டல் ஆர்டர்களை விசாரிக்கிறது. ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, ஹோட்டல் ஐடி, ஆர்டர் மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பித்த நேரம் மற்றும் ஆர்டர் நிலை ஆகியவற்றைக் கொண்ட தகவலைத் திருப்பி அனுப்புகிறது.",
        "preconditions": "பயனரின் தேவை ஹோட்டல் ஆர்டர்களை விசாரிப்பதாகும்.",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அனுப்புகிறது, பின்னர் மாற்றம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்.",
        "args": {
            "user_id": "பயனர் ஐடி",
            "date": "தேதி",
            "status": "ஆர்டர் நிலை"
        },
        "returns": "குறிப்பிட்ட பயனரின் ஹோட்டல் ஆர்டர் தகவல்.",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "பயனர் ஐடியின் அடிப்படையில், பயனரின் சுற்றுலா தல டிக்கெட் ஆர்டர்களை விசாரிக்கவும், ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, சுற்றுலா தல ஐடி, ஆர்டர் மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பித்த நேரம் மற்றும் ஆர்டர் நிலை ஆகியவற்றை உள்ளடக்கிய தகவலைத் திருப்பி அளிக்கும்",
        "preconditions": "பயனரின் தேவை சுற்றுலா தல டிக்கெட் ஆர்டர்களை விசாரிப்பதாகும்",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அளிக்கும், பின்னர் மாற்றம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "date": "தேதி",
            "status": "ஆர்டர் நிலை"
        },
        "returns": "குறிப்பிட்ட பயனரின் சுற்றுலா தல டிக்கெட் ஆர்டர் தகவல்",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "பயனர் ஐடி அடிப்படையில் பயனரின் விமான டிக்கெட் ஆர்டரை விசாரித்து, ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, விமான ஐடி, ஆர்டர் மொத்தத் தொகை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம் மற்றும் ஆர்டர் நிலை ஆகியவற்றைக் கொண்ட விவரங்களைத் திருப்பி அளிக்கிறது",
        "preconditions": "பயனரின் தேவை விமான டிக்கெட் ஆர்டரை விசாரிப்பதாகும்",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அளிக்கிறது, பின்னர் மாற்றம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "date": "தேதி",
            "status": "ஆர்டர் நிலை"
        },
        "returns": "குறிப்பிட்ட பயனரின் விமான டிக்கெட் ஆர்டர் தகவல்",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "பயனர் ஐடியின் அடிப்படையில் பயனரின் ரயில் டிக்கெட் ஆர்டர்களை விசாரிக்கிறது. ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, ரயில் ஐடி, ஆர்டர் மொத்தத் தொகை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம் மற்றும் ஆர்டர் நிலை ஆகியவற்றைத் திருப்பி அளிக்கிறது",
        "preconditions": "பயனரின் தேவை ரயில் டிக்கெட் ஆர்டர்களை விசாரிப்பதாகும்",
        "postconditions": "ஆர்டர் தகவலைத் திருப்பி அளிக்கிறது, பின்னர் மாற்றம் அல்லது ரத்து செய்வதற்கு வசதியாக இருக்கும்",
        "args": {
            "user_id": "பயனர் ஐடி",
            "date": "தேதி",
            "status": "ஆர்டர் நிலை"
        },
        "returns": "குறிப்பிட்ட பயனரின் ரயில் டிக்கெட் ஆர்டர் தகவல்",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ஹோட்டல் ஆர்டர் விவரங்களைப் பெறுகிறது, இதில் ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, ஹோட்டல் ஐடி, மொத்த ஆர்டர் தொகை, ஆர்டர் செய்யப்பட்ட நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் ஆர்டர் அறை விவரங்கள் (அறை வகை, தங்கும் தேதி, விலை, அறை ஐடி) ஆகியவை அடங்கும்.",
        "preconditions": "பயனர் ஹோட்டல் ஆர்டர் விவரங்களைப் பெறக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது.",
        "postconditions": "ஆர்டர் விவரங்களைத் திருப்பி அளிக்கிறது.",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் விவரங்கள்",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "சுற்றுலா தல டிக்கெட் ஆர்டர் விவரங்களைப் பெறுகிறது, ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, சுற்றுலா தல ஐடி, மொத்த ஆர்டர் விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் ஆர்டர் சுற்றுலா தல விவரங்கள் (டிக்கெட் வகை, தேதி, விலை, டிக்கெட் ஐடி) ஆகியவற்றை உள்ளடக்கியது.",
        "preconditions": "பயனர் சுற்றுலா தல டிக்கெட் ஆர்டர் விவரங்களைப் பெறக் கோருகிறார், முந்தைய உரையாடலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டுள்ளது.",
        "postconditions": "ஆர்டர் விவரங்களைத் திருப்பி அனுப்புகிறது.",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் விவரங்கள்",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "விமான டிக்கெட் ஆர்டர் விவரங்களைப் பெறுகிறது, இதில் ஆர்டர் ID, ஆர்டர் வகை, பயனர் ID, விமான ID, ஆர்டர் மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் ஆர்டர் டிக்கெட் விரிவான தகவல்கள் (இருக்கை வகை, தேதி, விலை, இருக்கை ID) ஆகியவை அடங்கும்.",
        "preconditions": "பயனர் விமான டிக்கெட் ஆர்டர் விவரங்களைப் பெறக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ID உறுதி செய்யப்பட்டுள்ளது.",
        "postconditions": "ஆர்டர் விவரங்களைத் திருப்பி அளிக்கிறது.",
        "args": {
            "order_id": "ஆர்டர் ID"
        },
        "returns": "ஆர்டர் விவரங்கள்",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ரயில் டிக்கெட் ஆர்டர் விவரங்களைப் பெறுகிறது, ஆர்டர் ஐடி, ஆர்டர் வகை, பயனர் ஐடி, ரயில் ஐடி, ஆர்டர் மொத்த விலை, ஆர்டர் செய்த நேரம், புதுப்பிக்கப்பட்ட நேரம், ஆர்டர் நிலை மற்றும் ஆர்டர் ரயில் டிக்கெட் விவரமான தகவல் (இருக்கை வகை, தேதி, விலை, இருக்கை ஐடி) ஆகியவற்றை உள்ளடக்கியது.",
        "preconditions": "பயனர் ரயில் டிக்கெட் ஆர்டர் விவரங்களைப் பெறக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டது.",
        "postconditions": "ஆர்டர் விவரங்களைத் திருப்பி அளிக்கிறது.",
        "args": {
            "order_id": "ஆர்டர் ஐடி"
        },
        "returns": "ஆர்டர் விவரங்கள்",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "ரயில் டிக்கெட் ஆர்டரை மாற்றவும், புறப்படும் தேதியை மாற்ற ஆதரவு அளிக்கிறது, விலை வேறுபாட்டை செலுத்துதல் அல்லது திரும்பப் பெறுதலை தானியங்கி முறையில் கையாள்கிறது.",
        "preconditions": "ரயில் டிக்கெட் விசாரணை மற்றும் கொள்முதல் சூழலில், பயனர் ரயில் டிக்கெட் ஆர்டரை மாற்றக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டது.",
        "postconditions": "ஆர்டரை மாற்றி ஆர்டர் நிலையைப் புதுப்பிக்கவும், விலை வேறுபாட்டை செலுத்த வேண்டியிருந்தால், ஆர்டர் நிலையை unpaid என மாற்றவும், இல்லையெனில் அசல் நிலையை வைத்திருக்கவும், விலை வேறுபாட்டை செலுத்த வேண்டியிருந்தால், பயனரை இந்த ஆர்டரை செலுத்த வழிநடத்த வேண்டும்.",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி",
            "new_date": "புதிய புறப்படும் தேதி, வடிவம் %Y-%m-%d"
        },
        "returns": "(மாற்றிய பிறகு ஆர்டர் விவரங்கள், விலை வேறுபாடு, நேர்மறை என்பது செலுத்த வேண்டிய தொகை, எதிர்மறை என்பது திரும்பப் பெற வேண்டிய தொகை)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "விமான டிக்கெட் ஆர்டரை மாற்றவும், புறப்படும் தேதியை மாற்ற ஆதரவு அளிக்கிறது, விலை வேறுபாட்டைச் செலுத்துவது அல்லது திருப்பிச் செலுத்துவதை தானியங்கியாகக் கையாள்கிறது.",
        "preconditions": "விமான டிக்கெட் தேடல் மற்றும் கொள்முதல் சூழலில், பயனர் விமான டிக்கெட் ஆர்டரை மாற்றக் கோருகிறார், முந்தைய சூழலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டது.",
        "postconditions": "ஆர்டரை மாற்றி ஆர்டர் நிலையைப் புதுப்பிக்கவும், விலை வேறுபாட்டைச் செலுத்த வேண்டியிருந்தால், ஆர்டர் நிலையை unpaid என மாற்றவும், இல்லையெனில் அசல் நிலையை வைத்திருக்கவும், விலை வேறுபாட்டைச் செலுத்த வேண்டியிருந்தால், பயனரை இந்த ஆர்டரைச் செலுத்த வழிநடத்த வேண்டும்.",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி",
            "new_date": "புதிய புறப்படும் தேதி, வடிவம் %Y-%m-%d"
        },
        "returns": "(மாற்றப்பட்ட ஆர்டர் உள்ளடக்கம், விலை வேறுபாடு, நேர்மறை என்பது வேறுபாட்டைச் செலுத்த வேண்டும் என்பதாகும், எதிர்மறை என்பது வேறுபாட்டைத் திருப்பிச் செலுத்துவதாகும்)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "பயனர் முன்பதிவு செய்த ஹோட்டல் ஆர்டரை ரத்து செய்தல்",
        "preconditions": "ஹோட்டல் முன்பதிவு விசாரணை சூழலில், பயனர் ஹோட்டல் ஆர்டரை ரத்து செய்ய கோருகிறார், முந்தைய உரையாடலில் ஆர்டர் ஐடி உறுதி செய்யப்பட்டது",
        "postconditions": "ஆர்டரை ரத்து செய்து, ஆர்டர் நிலையை புதுப்பிக்கவும். வேறுபட்ட தொகையை திருப்பி செலுத்த வேண்டும் என்றால், பயனருக்கு தெரியப்படுத்தவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி"
        },
        "returns": "ஆர்டரை ரத்து செய்ததற்கான திருப்பி செலுத்தும் தொகை",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "பயனர் முன்பதிவு செய்த சுற்றுலா தல டிக்கெட் ஆர்டரை ரத்து செய்தல்",
        "preconditions": "வரலாற்று உரையாடலில் ஆர்டர் ஐடி இருக்க வேண்டும் அல்லது ஏற்கனவே ஆர்டர் விசாரணை நடத்தப்பட்டிருக்க வேண்டும், பயனர் இந்த ஆர்டரை ரத்து செய்ய உரிமை கொண்டவர்",
        "postconditions": "விலை வேறுபாடு திருப்பி அளிக்கப்பட்டால், பயனருக்கு தெரியப்படுத்தவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி"
        },
        "returns": "ஆர்டரை ரத்து செய்ததற்கான திரும்பிச் செலுத்தும் தொகை",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "பயனர் முன்பதிவு செய்த விமான டிக்கெட் ஆர்டரை ரத்து செய்கிறார்",
        "preconditions": "முந்தைய உரையாடலில் ஆர்டர் ஐடி இருக்க வேண்டும் அல்லது ஏற்கனவே ஆர்டர் விசாரணை நடத்தப்பட்டிருக்க வேண்டும், பயனர் இந்த ஆர்டரை ரத்து செய்ய அனுமதி கொண்டிருக்க வேண்டும்",
        "postconditions": "வேறுபாடு தொகை திருப்பி அளிக்கப்பட்டால், பயனருக்கு தெரியப்படுத்தவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி"
        },
        "returns": "ஆர்டர் ரத்து செய்ததற்கான திரும்பி வரும் தொகை",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "பயனர் முன்பதிவு செய்த ரயில் டிக்கெட் ஆர்டரை ரத்து செய்தல்",
        "preconditions": "முந்தைய உரையாடலில் ஆர்டர் ஐடி இருக்க வேண்டும் அல்லது ஏற்கனவே ஆர்டர் விசாரணை நடந்திருக்க வேண்டும்; பயனர் இந்த ஆர்டரை ரத்து செய்ய உரிமை பெற்றிருக்க வேண்டும்",
        "postconditions": "வேறுபட்ட தொகை திருப்பி அளிக்கப்பட்டால், பயனருக்கு தெரியப்படுத்தவும்",
        "args": {
            "order_id": "ஆர்டர் ஐடி",
            "user_id": "பயனர் ஐடி"
        },
        "returns": "ஆர்டரை ரத்து செய்ததற்கான திருப்பி செலுத்தும் தொகை",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Lao version
TOOL_DESCRIPTIONS_LO = {
    "get_ota_hotel_info": {
        "description": "ດຶງຂໍ້ມູນໂຮງແຮມ, ປະກອບມີ ລະຫັດໂຮງແຮມ, ຊື່, ຄະແນນ, ລະດັບດາວ, ທີ່ຢູ່, ປ້າຍກຳກັບ, ລາຍການຫ້ອງພັກ",
        "preconditions": "ໃນສະຖານະການຄົ້ນຫາ ແລະ ຈອງໂຮງແຮມ, ຕ້ອງການດຶງຂໍ້ມູນລະອຽດຂອງໂຮງແຮມ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງໂຮງແຮມ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກຫ້ອງພັກ ແລະ ສັ່ງຈອງ",
        "args": {
            "hotel_id": "ລະຫັດໂຮງແຮມ"
        },
        "returns": "ຂໍ້ມູນໂຮງແຮມ",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "ດຶງຂໍ້ມູນສະຖານທີ່ທ່ອງທ່ຽວ, ລວມມີ ລະຫັດສະຖານທີ່, ຊື່, ທີ່ຢູ່, ຄຳອະທິບາຍ, ຄະແນນປະເມີນ, ເວລາເປີດ-ປິດ, ລາຄາຕົວ, ລາຍການປະເພດຕົວ",
        "preconditions": "ໃນບໍລິບົດການທ່ອງທ່ຽວສະຖານທີ່, ຕ້ອງການດຶງຂໍ້ມູນລະອຽດຂອງສະຖານທີ່",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງສະຖານທີ່, ຊີ້ນຳຜູ້ໃຊ້ເລືອກຕົວ ແລະ ດຳເນີນການສັ່ງຊື້",
        "args": {
            "attraction_id": "ລະຫັດສະຖານທີ່"
        },
        "returns": "ຂໍ້ມູນສະຖານທີ່",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "ດຶງຂໍ້ມູນຖ້ຽວບິນ, ລວມມີ ລະຫັດຖ້ຽວບິນ, ເລກຖ້ຽວບິນ, ເມືອງອອກເດີນທາງ, ເມືອງຮອດ, ຕຳແໜ່ງທ່າອາກາດຍົນອອກເດີນທາງ, ຕຳແໜ່ງທ່າອາກາດຍົນຮອດ, ເວລາອອກເດີນທາງ, ເວລາຮອດ, ປ້າຍກຳກັບຖ້ຽວບິນ, ລາຍການປະເພດທີ່ນັ່ງ",
        "preconditions": "ໃນສະຖານະການສືບຄົ້ນ ແລະ ຊື້ປີ້ຍົນ, ຕ້ອງການດຶງຂໍ້ມູນລະອຽດຂອງຖ້ຽວບິນ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງຖ້ຽວບິນ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກທີ່ນັ່ງ ແລະ ດຳເນີນການສັ່ງຊື້",
        "args": {
            "flight_id": "ລະຫັດຖ້ຽວບິນ"
        },
        "returns": "ຂໍ້ມູນຖ້ຽວບິນ",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ດຶງຂໍ້ມູນລົດໄຟ, ລວມມີ ລະຫັດລົດໄຟ, ເລກຂະບວນ, ເມືອງອອກເດີນທາງ, ເມືອງທີ່ໄປຮອດ, ຕຳແໜ່ງສະຖານີອອກເດີນທາງ, ຕຳແໜ່ງສະຖານີທີ່ໄປຮອດ, ເວລາອອກເດີນທາງ, ເວລາທີ່ໄປຮອດ, ປ້າຍກຳກັບລົດໄຟ, ລາຍການປະເພດທີ່ນັ່ງ",
        "preconditions": "ໃນສະຖານະການສືບຄົ້ນ ແລະ ຊື້ປີ້ລົດໄຟ, ຕ້ອງການດຶງຂໍ້ມູນລະອຽດຂອງລົດໄຟ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນລະອຽດຂອງລົດໄຟ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກທີ່ນັ່ງ ແລະ ສັ່ງຊື້",
        "args": {
            "train_id": "ລະຫັດລົດໄຟ"
        },
        "returns": "ຂໍ້ມູນລົດໄຟ",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "ໃນບໍລິບົດການທ່ອງທ່ຽວ ແລະ ພັກຜ່ອນ, ອີງໃສ່ຄວາມຕ້ອງການດ້ານສະຖານທີ່ ແລະ ຄວາມມັກຂອງຜູ້ໃຊ້, ແນະນຳຕົວເລືອກໂຮງແຮມທີ່ເໝາະສົມ, ສະໜອງຂໍ້ມູນພື້ນຖານຂອງໂຮງແຮມ, ປະກອບມີ ລະຫັດໂຮງແຮມ, ຊື່, ຄະແນນປະເມີນ, ລະດັບດາວ, ທີ່ຢູ່, ແລະ ແທັກ",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍຈອງໂຮງແຮມ, ພ້ອມໃຫ້ຄຳສຳຄັນທີ່ກ່ຽວຂ້ອງກັບໂຮງແຮມ ຫຼື ສະຖານທີ່",
        "postconditions": "ສົ່ງຄືນລາຍຊື່ໂຮງແຮມທີ່ຕອບສະໜອງເງື່ອນໄຂ, ຖ້າຕ້ອງການເບິ່ງລາຍລະອຽດໂຮງແຮມ (ລາຍຊື່ຫ້ອງ, ລາຄາ ແລະ ອື່ນໆ) ຕ້ອງໃຊ້ເຄື່ອງມືສືບຄົ້ນລາຍລະອຽດໂຮງແຮມ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກໂຮງແຮມ",
        "args": {
            "city_name": "ຊື່ເມືອງ",
            "key_words": "ຄຳສຳຄັນສຳລັບການຄົ້ນຫາ (ກົງກັບຊື່ໂຮງແຮມ, ຄຳອະທິບາຍໂຮງແຮມ ແລະ ອື່ນໆ)"
        },
        "returns": "ຜົນລັພອອກແບບໂຄງສ້າງຂອງຂໍ້ມູນພື້ນຖານໂຮງແຮມ",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "ອີງໃສ່ຄວາມຕ້ອງການແລະຄວາມມັກຂອງຜູ້ໃຊ້ກ່ຽວກັບສະຖານທີ່, ແນະນຳຕົວເລືອກສະຖານທີ່ທ່ອງທ່ຽວທີ່ເໝາະສົມ, ໃຫ້ຂໍ້ມູນພື້ນຖານຂອງສະຖານທີ່ທ່ອງທ່ຽວ, ລວມມີ ລະຫັດສະຖານທີ່, ຊື່, ທີ່ຢູ່, ຄຳອະທິບາຍ, ຄະແນນປະເມີນ, ເວລາເປີດ-ປິດ",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍຈອງສະຖານທີ່ທ່ອງທ່ຽວ, ໃຫ້ຄຳສຳຄັນ ຫຼື ສະຖານທີ່ທີ່ກ່ຽວຂ້ອງກັບສະຖານທີ່ທ່ອງທ່ຽວ",
        "postconditions": "ສົ່ງຄືນລາຍການສະຖານທີ່ທ່ອງທ່ຽວທີ່ຕອບສະໜອງເງື່ອນໄຂ, ຖ້າຕ້ອງການເບິ່ງລາຍລະອຽດສະຖານທີ່ທ່ອງທ່ຽວ (ລາຍການປີ້ເຂົ້າຊົມ, ລາຄາ ແລະ ອື່ນໆ) ຕ້ອງໃຊ້ເຄື່ອງມືສືບຄົ້ນລາຍລະອຽດສະຖານທີ່ທ່ອງທ່ຽວ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກສະຖານທີ່ທ່ອງທ່ຽວ",
        "args": {
            "city_name": "ຊື່ເມືອງ",
            "key_words": "ຄຳສຳຄັນສຳລັບການຄົ້ນຫາ (ກົງກັບຊື່ສະຖານທີ່ທ່ອງທ່ຽວ, ຕຳແໜ່ງ, ທີ່ຢູ່, ຈຸດເດັ່ນ ແລະ ອື່ນໆ)"
        },
        "returns": "ຜົນລັພທາງໂຄງສ້າງຂອງຂໍ້ມູນພື້ນຖານສະຖານທີ່ທ່ອງທ່ຽວ",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "ອີງໃສ່ຄວາມຕ້ອງການດ້ານສະຖານທີ່ ແລະ ຄວາມມັກຂອງຜູ້ໃຊ້, ແນະນຳຕົວເລືອກຖ້ຽວບິນທີ່ເໝາະສົມ, ໃຫ້ຂໍ້ມູນພື້ນຖານຂອງຖ້ຽວບິນ, ລວມມີ ລະຫັດຖ້ຽວບິນ, ເລກຖ້ຽວບິນ, ເມືອງອອກເດີນທາງ, ເມືອງປາຍທາງ, ຕຳແໜ່ງສະໜາມບິນອອກເດີນທາງ, ຕຳແໜ່ງສະໜາມບິນປາຍທາງ, ເວລາອອກເດີນທາງ, ເວລາຮອດ, ປ້າຍກຳກັບຖ້ຽວບິນ",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍຈອງຖ້ຽວບິນ, ໃຫ້ຄຳສຳຄັນທີ່ກ່ຽວຂ້ອງກັບຖ້ຽວບິນ ຫຼື ສະຖານທີ່",
        "postconditions": "ສົ່ງຄືນລາຍການຖ້ຽວບິນທີ່ຕອບສະໜອງເງື່ອນໄຂ, ຖ້າຕ້ອງການເບິ່ງລາຍລະອຽດຖ້ຽວບິນ (ລາຍການປະເພດທີ່ນັ່ງ, ລາຄາ, ວັນທີ ແລະ ອື່ນໆ) ຕ້ອງໃຊ້ເຄື່ອງມືສືບຖາມລາຍລະອຽດຖ້ຽວບິນ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກຖ້ຽວບິນ",
        "args": {
            "departure": "ເມືອງອອກເດີນທາງ",
            "destination": "ເມືອງປາຍທາງ"
        },
        "returns": "ຜົນລັພອອກແບບໂຄງສ້າງຂອງຂໍ້ມູນພື້ນຖານຖ້ຽວບິນ",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "ອີງໃສ່ຄວາມຕ້ອງການດ້ານສະຖານທີ່ ແລະ ຄວາມມັກຂອງຜູ້ໃຊ້, ແນະນຳຕົວເລືອກລົດໄຟທີ່ເໝາະສົມ, ໃຫ້ຂໍ້ມູນພື້ນຖານຂອງປີ້ລົດໄຟ, ປະກອບມີ ລະຫັດລົດໄຟ, ເລກຂະບວນລົດ, ເມືອງອອກເດີນທາງ, ເມືອງປາຍທາງ, ຕຳແໜ່ງສະຖານີອອກເດີນທາງ, ຕຳແໜ່ງສະຖານີປາຍທາງ, ເວລາອອກເດີນທາງ, ເວລາຮອດ, ແລະ ແທັກລົດໄຟ",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍຈອງລົດໄຟ, ໃຫ້ຄຳສຳຄັນທີ່ກ່ຽວຂ້ອງກັບລົດໄຟ ຫຼື ສະຖານທີ່",
        "postconditions": "ສົ່ງຄືນລາຍການປີ້ລົດໄຟທີ່ເໝາະສົມ, ຖ້າຕ້ອງການເບິ່ງລາຍລະອຽດປີ້ລົດໄຟ (ລາຍການປະເພດທີ່ນັ່ງ, ລາຄາ, ວັນທີ ແລະ ອື່ນໆ) ຕ້ອງໃຊ້ເຄື່ອງມືສືບຄົ້ນລາຍລະອຽດປີ້ລົດໄຟ, ຊີ້ນຳຜູ້ໃຊ້ເລືອກປີ້ລົດໄຟ",
        "args": {
            "departure": "ເມືອງອອກເດີນທາງ",
            "destination": "ເມືອງປາຍທາງ",
            "date": "ວັນທີອອກເດີນທາງ"
        },
        "returns": "ຜົນລັພໂຄງສ້າງຂໍ້ມູນພື້ນຖານຂອງລົດໄຟ",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "ເມື່ອຜູ້ໃຊ້ຈອງໂຮງແຮມ, ລະບົບຈະສ້າງໃບສັ່ງຊື້ຕາມຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ (ເຊັ່ນ: ຊື່ໂຮງແຮມ, ວັນທີເຂົ້າພັກ, ຈຳນວນຄົນ, ຯລຯ).",
        "preconditions": "ຜູ້ໃຊ້ໄດ້ເຂົ້າສູ່ລະບົບແລະໃຫ້ລະຫັດປະຈຳຕົວທີ່ຖືກຕ້ອງ (user_id), ຜູ້ໃຊ້ໃຫ້ຊື່ໂຮງແຮມ (hotel_name) ແລະ ປະເພດຫ້ອງພັກ (room_type) ທີ່ຖືກຕ້ອງ, ລະບົບມີຂໍ້ມູນກ່ຽວກັບໂຮງແຮມເປົ້າໝາຍ, ແລະ ໂຮງແຮມນັ້ນມີຫ້ອງພັກວ່າງໃນວັນທີທີ່ຖືກຮ້ອງຂໍ.",
        "postconditions": "ສ້າງໃບສັ່ງຊື້, ກະລຸນາໃຫ້ຜູ້ໃຊ້ຢືນຢັນການຊຳລະເງິນ.",
        "args": {
            "hotel_id": "ລະຫັດໂຮງແຮມ",
            "room_id": "ລະຫັດຫ້ອງພັກ",
            "user_id": "ລະຫັດຜູ້ໃຊ້"
        },
        "returns": "ຜົນການຕອບຮັບຂອງການດຳເນີນການສ້າງໃບສັ່ງຊື້.",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "ຜູ້ໃຊ້ຊື້ປີ້ເຂົ້າຊົມຕາມສະຖານທີ່ທ່ອງທ່ຽວ ແລະ ວັນທີ, ລະບົບຈະສົ່ງຄືນຂໍ້ມູນທີ່ກ່ຽວຂ້ອງກັບປີ້ເຂົ້າຊົມ ແລະ ດຳເນີນການສັ່ງຊື້",
        "preconditions": "ໃນສະຖານະການທ່ອງທ່ຽວສະຖານທີ່, ຜູ້ໃຊ້ຮ້ອງຂໍຈອງສະຖານທີ່ ແລະ ໃຫ້ຂໍ້ມູນທີ່ຈຳເປັນທີ່ກ່ຽວຂ້ອງກັບການຈອງ",
        "postconditions": "ສ້າງໃບສັ່ງຊື້, ກະລຸນາໃຫ້ຜູ້ໃຊ້ຢືນຢັນການຊຳລະເງິນ",
        "args": {
            "attraction_id": "ລະຫັດສະຖານທີ່ທ່ອງທ່ຽວ",
            "ticket_id": "ລະຫັດປີ້ເຂົ້າຊົມ",
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "date": "ວັນທີເຂົ້າຊົມ, ຮູບແບບ %Y-%m-%d",
            "quantity": "ຈຳນວນ"
        },
        "returns": "ຜົນການຕອບຮັບຂອງການດຳເນີນການສ້າງໃບສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "ຜູ້ໃຊ້ຊື້ປີ້ຍົນຕາມເລກຖ້ຽວບິນ, ວັນທີ, ປະເພດທີ່ນັ່ງ, ຈຳນວນ, ລະບົບຈະສົ່ງຄືນຂໍ້ມູນທີ່ກ່ຽວຂ້ອງກັບປີ້ຍົນ ແລະ ດຳເນີນການສັ່ງຊື້",
        "preconditions": "ໃນສະຖານະການສອບຖາມ ແລະ ຊື້ປີ້ຍົນ, ຜູ້ໃຊ້ຮ້ອງຂໍຈອງຖ້ຽວບິນ, ໃຫ້ຂໍ້ມູນທີ່ຈຳເປັນທີ່ກ່ຽວຂ້ອງກັບການຈອງ",
        "postconditions": "ສ້າງໃບສັ່ງຊື້, ກະລຸນາຜູ້ໃຊ້ຢືນຢັນການຊຳລະເງິນ",
        "args": {
            "flight_id": "ລະຫັດຖ້ຽວບິນ",
            "seat_id": "ລະຫັດທີ່ນັ່ງ",
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "date": "ວັນທີອອກເດີນທາງ",
            "quantity": "ຈຳນວນ"
        },
        "returns": "ຜົນການຕອບຮັບຂອງການດຳເນີນການສ້າງໃບສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "ຜູ້ໃຊ້ສາມາດຊື້ປີ້ລົດໄຟໂດຍອີງໃສ່ເລກຂະບວນລົດ, ວັນທີ, ປະເພດທີ່ນັ່ງ ແລະ ຈຳນວນ, ລະບົບຈະສະແດງຂໍ້ມູນປີ້ລົດໄຟທີ່ກ່ຽວຂ້ອງ ແລະ ດຳເນີນການສັ່ງຊື້",
        "preconditions": "ໃນສະຖານະການສອບຖາມ ແລະ ຊື້ປີ້ລົດໄຟ, ຜູ້ໃຊ້ຮ້ອງຂໍຈອງລົດໄຟ ແລະ ໃຫ້ຂໍ້ມູນທີ່ຈຳເປັນສຳລັບການຈອງ",
        "postconditions": "ສ້າງໃບສັ່ງຊື້ຂຶ້ນ, ກະລຸນາຜູ້ໃຊ້ຢືນຢັນການຊຳລະເງິນ",
        "args": {
            "train_id": "ເລກປະຈຳຕົວລົດໄຟ",
            "seat_id": "ເລກປະຈຳຕົວທີ່ນັ່ງ",
            "user_id": "ເລກປະຈຳຕົວຜູ້ໃຊ້",
            "date": "ວັນທີອອກເດີນທາງ",
            "quantity": "ຈຳນວນ"
        },
        "returns": "ຜົນການຕອບຮັບຈາກການດຳເນີນການສ້າງໃບສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "ຜູ້ໃຊ້ດຳເນີນການຊຳລະເງິນຄຳສັ່ງໂຮງແຮມ",
        "preconditions": "ໃນສະຖານະການສອບຖາມການຈອງໂຮງແຮມ, ຜູ້ໃຊ້ຮ້ອງຂໍຊຳລະເງິນຄຳສັ່ງໂຮງແຮມ, ບໍລິບົດຂ້າງເທິງໄດ້ກຳນົດລະຫັດຄຳສັ່ງແລ້ວ",
        "postconditions": "ຢືນຢັນການຊຳລະເງິນ ແລະ ອັບເດດສະຖານະຄຳສັ່ງເປັນຊຳລະແລ້ວ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງ"
        },
        "returns": "ຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "ຜູ້ໃຊ້ດຳເນີນການຊຳລະເງິນຄຳສັ່ງຊື້ປີ້",
        "preconditions": "ໃນສະຖານະການທ່ອງທ່ຽວຢູ່ສະຖານທີ່ທ່ອງທ່ຽວ, ຜູ້ໃຊ້ຮ້ອງຂໍຊຳລະເງິນຄຳສັ່ງຊື້ປີ້ເຂົ້າຊົມ, ບໍລິບົດກ່ອນໜ້ານີ້ໄດ້ກຳນົດລະຫັດຄຳສັ່ງຊື້ແລ້ວ",
        "postconditions": "ຢືນຢັນການຊຳລະເງິນ ແລະ ອັບເດດສະຖານະຄຳສັ່ງຊື້ເປັນຊຳລະແລ້ວ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "ຜູ້ໃຊ້ດຳເນີນການຊຳລະເງິນຄຳສັ່ງຊື້ປີ້ຍົນ",
        "preconditions": "ໃນສະຖານະການສອບຖາມ ແລະ ຊື້ປີ້ຍົນ, ຜູ້ໃຊ້ຮ້ອງຂໍຊຳລະເງິນຄຳສັ່ງຊື້ຖ້ຽວບິນ, ບໍລິບົດກ່ອນໜ້າໄດ້ກຳນົດລະຫັດຄຳສັ່ງຊື້ແລ້ວ",
        "postconditions": "ຢືນຢັນການຊຳລະເງິນ ແລະ ອັບເດດສະຖານະຄຳສັ່ງຊື້ເປັນຊຳລະແລ້ວ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "ຜູ້ໃຊ້ດຳເນີນການຊຳລະເງິນສຳລັບຄຳສັ່ງຊື້ປີ້ລົດໄຟ",
        "preconditions": "ໃນສະຖານະການສອບຖາມ ແລະ ຊື້ປີ້ລົດໄຟ, ຜູ້ໃຊ້ຮ້ອງຂໍຊຳລະເງິນຄຳສັ່ງຊື້ປີ້ລົດໄຟ, ບໍລິບົດກ່ອນໜ້າໄດ້ກຳນົດລະຫັດຄຳສັ່ງແລ້ວ",
        "postconditions": "ຢືນຢັນການຊຳລະເງິນ ແລະ ອັບເດດສະຖານະຄຳສັ່ງເປັນຊຳລະແລ້ວ",
        "args": {
            "order_id": "ລະຫັດຄຳສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນຜົນການຊຳລະເງິນ",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "ອີງຕາມ ID ຜູ້ໃຊ້, ສືບຄົ້ນຄຳສັ່ງຊື້ໂຮງແຮມຂອງຜູ້ໃຊ້, ສົ່ງຄືນລວມມີ ID ຄຳສັ່ງຊື້, ປະເພດຄຳສັ່ງຊື້, ID ຜູ້ໃຊ້, ID ໂຮງແຮມ, ລາຄາລວມຂອງຄຳສັ່ງຊື້, ເວລາສັ່ງຊື້, ເວລາອັບເດດ ແລະ ສະຖານະຄຳສັ່ງຊື້",
        "preconditions": "ຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ແມ່ນການສືບຄົ້ນຄຳສັ່ງຊື້ໂຮງແຮມ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນຄຳສັ່ງຊື້, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ID ຜູ້ໃຊ້",
            "date": "ວັນທີ",
            "status": "ສະຖານະຄຳສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນຄຳສັ່ງຊື້ໂຮງແຮມຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "ອີງຕາມ ID ຜູ້ໃຊ້, ສືບຄົ້ນໃບສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວຂອງຜູ້ໃຊ້, ສົ່ງຄືນລວມມີ ID ໃບສັ່ງຊື້, ປະເພດໃບສັ່ງຊື້, ID ຜູ້ໃຊ້, ID ສະຖານທີ່ທ່ອງທ່ຽວ, ລາຄາລວມຂອງໃບສັ່ງຊື້, ເວລາສັ່ງຊື້, ເວລາອັບເດດ ແລະ ສະຖານະໃບສັ່ງຊື້",
        "preconditions": "ຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ແມ່ນການສືບຄົ້ນໃບສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນໃບສັ່ງຊື້, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ID ຜູ້ໃຊ້",
            "date": "ວັນທີ",
            "status": "ສະຖານະໃບສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນໃບສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "ອີງຕາມ ID ຜູ້ໃຊ້, ສືບຄົ້ນໃບສັ່ງຊື້ປີ້ຍົນຂອງຜູ້ໃຊ້, ສົ່ງຄືນລວມມີ ID ໃບສັ່ງຊື້, ປະເພດໃບສັ່ງຊື້, ID ຜູ້ໃຊ້, ID ຖ້ຽວບິນ, ລາຄາລວມຂອງໃບສັ່ງຊື້, ເວລາສັ່ງຊື້, ເວລາອັບເດດ ແລະ ສະຖານະໃບສັ່ງຊື້",
        "preconditions": "ຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ແມ່ນການສືບຄົ້ນໃບສັ່ງຊື້ປີ້ຍົນ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນໃບສັ່ງຊື້, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ID ຜູ້ໃຊ້",
            "date": "ວັນທີ",
            "status": "ສະຖານະໃບສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນໃບສັ່ງຊື້ປີ້ຍົນຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "ອີງຕາມ ID ຜູ້ໃຊ້, ສືບຄົ້ນໃບສັ່ງຊື້ປີ້ລົດໄຟຂອງຜູ້ໃຊ້, ສົ່ງຄືນທີ່ປະກອບມີ ID ໃບສັ່ງຊື້, ປະເພດໃບສັ່ງຊື້, ID ຜູ້ໃຊ້, ID ລົດໄຟ, ລາຄາລວມຂອງໃບສັ່ງຊື້, ເວລາສັ່ງຊື້, ເວລາອັບເດດ ແລະ ສະຖານະໃບສັ່ງຊື້",
        "preconditions": "ຄວາມຕ້ອງການຂອງຜູ້ໃຊ້ແມ່ນການສືບຄົ້ນໃບສັ່ງຊື້ປີ້ລົດໄຟ",
        "postconditions": "ສົ່ງຄືນຂໍ້ມູນໃບສັ່ງຊື້, ສະດວກສຳລັບການແກ້ໄຂ/ຍົກເລີກໃນພາຍຫຼັງ",
        "args": {
            "user_id": "ID ຜູ້ໃຊ້",
            "date": "ວັນທີ",
            "status": "ສະຖານະໃບສັ່ງຊື້"
        },
        "returns": "ຂໍ້ມູນໃບສັ່ງຊື້ປີ້ລົດໄຟຂອງຜູ້ໃຊ້ທີ່ລະບຸ",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຈອງໂຮງແຮມ, ລວມມີ ID ຄຳສັ່ງ, ປະເພດຄຳສັ່ງ, ID ຜູ້ໃຊ້, ID ໂຮງແຮມ, ລາຄາລວມຂອງຄຳສັ່ງ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄຳສັ່ງ ແລະ ຂໍ້ມູນລະອຽດຫ້ອງພັກຂອງຄຳສັ່ງ (ປະເພດຫ້ອງ, ວັນທີເຂົ້າພັກ, ລາຄາ, ID ຫ້ອງ)",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍໃຫ້ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຈອງໂຮງແຮມ, ບໍລິບົດຂ້າງເທິງໄດ້ກຳນົດ ID ຄຳສັ່ງແລ້ວ",
        "postconditions": "ສົ່ງຄືນລາຍລະອຽດຄຳສັ່ງ",
        "args": {
            "order_id": "ID ຄຳສັ່ງ"
        },
        "returns": "ລາຍລະອຽດຄຳສັ່ງ",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວ, ປະກອບມີ ID ຄຳສັ່ງ, ປະເພດຄຳສັ່ງ, ID ຜູ້ໃຊ້, ID ສະຖານທີ່ທ່ອງທ່ຽວ, ລາຄາລວມຂອງຄຳສັ່ງ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄຳສັ່ງ ແລະ ຂໍ້ມູນລາຍລະອຽດຂອງສະຖານທີ່ທ່ອງທ່ຽວໃນຄຳສັ່ງ (ປະເພດປີ້, ວັນທີ, ລາຄາ, ID ປີ້)",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວ, ບໍລິບົດກ່ອນໜ້າໄດ້ກຳນົດ ID ຄຳສັ່ງແລ້ວ",
        "postconditions": "ສົ່ງຄືນລາຍລະອຽດຄຳສັ່ງ",
        "args": {
            "order_id": "ID ຄຳສັ່ງ"
        },
        "returns": "ລາຍລະອຽດຄຳສັ່ງ",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ຍົນ, ລວມມີ ID ຄຳສັ່ງ, ປະເພດຄຳສັ່ງ, ID ຜູ້ໃຊ້, ID ຖ້ຽວບິນ, ລາຄາລວມຂອງຄຳສັ່ງ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄຳສັ່ງ ແລະ ຂໍ້ມູນລະອຽດປີ້ຍົນຂອງຄຳສັ່ງ (ປະເພດທີ່ນັ່ງ, ວັນທີ, ລາຄາ, ID ທີ່ນັ່ງ)",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ຍົນ, ID ຄຳສັ່ງຖືກກຳນົດແລ້ວໃນຂໍ້ຄວາມກ່ອນໜ້າ",
        "postconditions": "ສົ່ງຄືນລາຍລະອຽດຄຳສັ່ງ",
        "args": {
            "order_id": "ID ຄຳສັ່ງ"
        },
        "returns": "ລາຍລະອຽດຄຳສັ່ງ",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ລົດໄຟ, ປະກອບມີ ID ຄຳສັ່ງ, ປະເພດຄຳສັ່ງ, ID ຜູ້ໃຊ້, ID ລົດໄຟ, ລາຄາລວມຂອງຄຳສັ່ງ, ເວລາສັ່ງຊື້, ເວລາອັບເດດ, ສະຖານະຄຳສັ່ງ ແລະ ຂໍ້ມູນລະອຽດປີ້ລົດໄຟຂອງຄຳສັ່ງ (ປະເພດທີ່ນັ່ງ, ວັນທີ, ລາຄາ, ID ທີ່ນັ່ງ)",
        "preconditions": "ຜູ້ໃຊ້ຮ້ອງຂໍໃຫ້ດຶງຂໍ້ມູນລາຍລະອຽດຄຳສັ່ງຊື້ປີ້ລົດໄຟ, ບໍລິບົດກ່ອນໜ້າໄດ້ກຳນົດ ID ຄຳສັ່ງແລ້ວ",
        "postconditions": "ສົ່ງຄືນລາຍລະອຽດຄຳສັ່ງ",
        "args": {
            "order_id": "ID ຄຳສັ່ງ"
        },
        "returns": "ລາຍລະອຽດຄຳສັ່ງ",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "ແກ້ໄຂຄໍາສັ່ງປີ້ລົດໄຟ, ສະໜັບສະໜູນການປ່ຽນວັນທີອອກເດີນທາງ, ຈັດການຈ່າຍເງິນສ່ວນຕ່າງຫຼືຄືນເງິນໂດຍອັດຕະໂນມັດ.",
        "preconditions": "ໃນສະຖານະການສອບຖາມ ແລະ ຊື້ປີ້ລົດໄຟ, ຜູ້ໃຊ້ຮ້ອງຂໍແກ້ໄຂຄໍາສັ່ງປີ້ລົດໄຟ, ລະຫັດຄໍາສັ່ງຖືກກໍານົດໄວ້ໃນບໍລິບົດກ່ອນໜ້າ",
        "postconditions": "ແກ້ໄຂຄໍາສັ່ງ ແລະ ອັບເດດສະຖານະຄໍາສັ່ງ, ຖ້າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ສະຖານະຄໍາສັ່ງປ່ຽນເປັນ unpaid, ຖ້າບໍ່ດັ່ງນັ້ນໃຫ້ຮັກສາສະຖານະເດີມ, ຖ້າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ຕ້ອງຊີ້ນໍາຜູ້ໃຊ້ໃຫ້ຈ່າຍຄໍາສັ່ງນີ້",
        "args": {
            "order_id": "ລະຫັດຄໍາສັ່ງ",
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "new_date": "ວັນທີອອກເດີນທາງໃໝ່, ຮູບແບບ %Y-%m-%d"
        },
        "returns": "(ເນື້ອໃນຄໍາສັ່ງທີ່ແກ້ໄຂແລ້ວ, ສ່ວນຕ່າງລາຄາ, ບວກໝາຍຄວາມວ່າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ລບໝາຍຄວາມວ່າຄືນເງິນສ່ວນຕ່າງ)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "ປັບປຸງຄໍາສັ່ງຊື້ປີ້ຍົນ, ສະໜັບສະໜູນການປ່ຽນວັນອອກເດີນທາງ, ດໍາເນີນການຈ່າຍເງິນສ່ວນຕ່າງຫຼືຄືນເງິນສ່ວນຕ່າງໂດຍອັດຕະໂນມັດ.",
        "preconditions": "ໃນສະຖານະການຄົ້ນຫາ ແລະ ຊື້ປີ້ຍົນ, ຜູ້ໃຊ້ຮ້ອງຂໍປັບປຸງຄໍາສັ່ງຊື້ປີ້ຍົນ, ລະຫັດຄໍາສັ່ງຖືກກໍານົດໄວ້ໃນບົດສົນທະນາກ່ອນໜ້າ.",
        "postconditions": "ປັບປຸງຄໍາສັ່ງ ແລະ ອັບເດດສະຖານະຄໍາສັ່ງ, ຖ້າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ສະຖານະຄໍາສັ່ງປ່ຽນເປັນ unpaid, ຖ້າບໍ່ດັ່ງນັ້ນຮັກສາສະຖານະເດີມ, ຖ້າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ຕ້ອງຊີ້ນໍາຜູ້ໃຊ້ໃຫ້ຊໍາລະຄໍາສັ່ງນີ້.",
        "args": {
            "order_id": "ລະຫັດຄໍາສັ່ງ",
            "user_id": "ລະຫັດຜູ້ໃຊ້",
            "new_date": "ວັນອອກເດີນທາງໃໝ່, ຮູບແບບ %Y-%m-%d"
        },
        "returns": "(ເນື້ອໃນຄໍາສັ່ງທີ່ປັບປຸງແລ້ວ, ສ່ວນຕ່າງລາຄາ, ບວກໝາຍຄວາມວ່າຕ້ອງຈ່າຍເງິນສ່ວນຕ່າງ, ລບໝາຍຄວາມວ່າຄືນເງິນສ່ວນຕ່າງ)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄໍາສັ່ງໂຮງແຮມທີ່ໄດ້ຈອງໄວ້ແລ້ວ",
        "preconditions": "ໃນສະຖານະການສອບຖາມການຈອງໂຮງແຮມ, ຜູ້ໃຊ້ຮ້ອງຂໍຍົກເລີກຄໍາສັ່ງໂຮງແຮມ, ລະຫັດຄໍາສັ່ງໄດ້ຖືກກໍານົດໄວ້ໃນຂໍ້ຄວາມກ່ອນຫນ້ານີ້",
        "postconditions": "ຍົກເລີກຄໍາສັ່ງແລະອັບເດດສະຖານະຄໍາສັ່ງ, ຖ້າມີການຄືນເງິນສ່ວນຕ່າງ, ໃຫ້ແຈ້ງຜູ້ໃຊ້ຊາບ",
        "args": {
            "order_id": "ລະຫັດຄໍາສັ່ງ",
            "user_id": "ລະຫັດຜູ້ໃຊ້"
        },
        "returns": "ຈໍານວນເງິນທີ່ຄືນສໍາລັບການຍົກເລີກຄໍາສັ່ງ",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄຳສັ່ງຊື້ປີ້ເຂົ້າຊົມສະຖານທີ່ທ່ອງທ່ຽວທີ່ໄດ້ຈອງໄວ້ແລ້ວ",
        "preconditions": "ມີ ID ຄຳສັ່ງຊື້ໃນປະຫວັດການສົນທະນາ ຫຼື ໄດ້ສອບຖາມຄຳສັ່ງຊື້ແລ້ວ, ຜູ້ໃຊ້ມີສິດຍົກເລີກຄຳສັ່ງຊື້ນີ້ໄດ້",
        "postconditions": "ຖ້າມີການຄືນເງິນສ່ວນຕ່າງ, ແຈ້ງໃຫ້ຜູ້ໃຊ້ຊາບ",
        "args": {
            "order_id": "ID ຄຳສັ່ງຊື້",
            "user_id": "ID ຜູ້ໃຊ້"
        },
        "returns": "ຈຳນວນເງິນຄືນຈາກການຍົກເລີກຄຳສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄໍາສັ່ງຊື້ປີ້ຍົນທີ່ໄດ້ຈອງໄວ້ແລ້ວ",
        "preconditions": "ມີ ID ຄໍາສັ່ງຊື້ໃນປະຫວັດການສົນທະນາ ຫຼື ໄດ້ດໍາເນີນການສອບຖາມຄໍາສັ່ງຊື້ແລ້ວ, ຜູ້ໃຊ້ມີສິດທິໃນການຍົກເລີກຄໍາສັ່ງຊື້ນີ້",
        "postconditions": "ຖ້າຫາກມີການຄືນເງິນສ່ວນຕ່າງ, ແຈ້ງໃຫ້ຜູ້ໃຊ້ຊາບກໍ່ພໍ",
        "args": {
            "order_id": "ID ຄໍາສັ່ງຊື້",
            "user_id": "ID ຜູ້ໃຊ້"
        },
        "returns": "ຈໍານວນເງິນຄືນທີ່ໄດ້ຮັບຈາກການຍົກເລີກຄໍາສັ່ງຊື້",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "ຜູ້ໃຊ້ຍົກເລີກຄໍາສັ່ງຊື້ປີ້ລົດໄຟທີ່ໄດ້ຈອງໄວ້ແລ້ວ",
        "preconditions": "ມີ ID ຄໍາສັ່ງໃນການສົນທະນາກ່ອນໜ້າ ຫຼື ໄດ້ດໍາເນີນການສອບຖາມຄໍາສັ່ງແລ້ວ, ຜູ້ໃຊ້ມີສິດທິໃນການຍົກເລີກຄໍາສັ່ງນີ້",
        "postconditions": "ຖ້າຫາກມີການຄືນເງິນສ່ວນຕ່າງ, ແຈ້ງໃຫ້ຜູ້ໃຊ້ຊາບກໍ່ພໍ",
        "args": {
            "order_id": "ID ຄໍາສັ່ງ",
            "user_id": "ID ຜູ້ໃຊ້"
        },
        "returns": "ຈໍານວນເງິນຄືນທີ່ໄດ້ຮັບຈາກການຍົກເລີກຄໍາສັ່ງ",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Burmese version
TOOL_DESCRIPTIONS_MY = {
    "get_ota_hotel_info": {
        "description": "ဟိုတယ်အချက်အလက်များကို ရယူပါ၊ ဟိုတယ် အိုင်ဒီ၊ အမည်၊ အမှတ်ပေးမှု၊ ကြယ်အဆင့်၊ လိပ်စာ၊ အမှတ်အသားများ၊ အခန်းစာရင်းတို့ ပါဝင်သည်။",
        "preconditions": "ဟိုတယ်ရှာဖွေခြင်းနှင့် ကြိုတင်မှာကြားခြင်း လုပ်ငန်းစဉ်များတွင် ဟိုတယ်၏ အသေးစိတ်အချက်အလက်များကို ရယူရန် လိုအပ်သည်။",
        "postconditions": "ဟိုတယ်၏ အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့ပြီး အခန်းရွေးချယ်ကာ အော်ဒါတင်ရန် အသုံးပြုသူကို လမ်းညွှန်သည်။",
        "args": {
            "hotel_id": "ဟိုတယ် အိုင်ဒီ"
        },
        "returns": "ဟိုတယ်အချက်အလက်",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "အထိမ်းအမှတ်နေရာ အချက်အလက်များကို ရယူခြင်း၊ အထိမ်းအမှတ်နေရာ အိုင်ဒီ၊ အမည်၊ လိပ်စာ၊ ဖော်ပြချက်၊ အဆင့်သတ်မှတ်ချက်၊ ဖွင့်လှစ်ချိန်၊ လက်မှတ်ဈေးနှုန်းနှင့် လက်မှတ်အမျိုးအစား စာရင်းတို့ ပါဝင်သည်။",
        "preconditions": "အထိမ်းအမှတ်နေရာ ခရီးသွားကဏ္ဍတွင် အထိမ်းအမှတ်နေရာ၏ အသေးစိတ်အချက်အလက်များကို ရယူရန် လိုအပ်သောအခါ။",
        "postconditions": "အထိမ်းအမှတ်နေရာ၏ အသေးစိတ်အချက်အလက်များကို ပြန်လည်ပေးပို့ပြီး၊ အသုံးပြုသူအား လက်မှတ်များကို ရွေးချယ်ရန်နှင့် အော်ဒါတင်ရန် လမ်းညွှန်ပေးသည်။",
        "args": {
            "attraction_id": "အထိမ်းအမှတ်နေရာ အိုင်ဒီ"
        },
        "returns": "အထိမ်းအမှတ်နေရာ အချက်အလက်",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "ပျံသန်းမှုဆိုင်ရာ အချက်အလက်များကို ရယူပါ။ ပျံသန်းမှု အိုင်ဒီ၊ ပျံသန်းမှု အမှတ်စဉ်၊ ထွက်ခွာရာ မြို့၊ ဆိုက်ရောက်ရာ မြို့၊ ထွက်ခွာရာ လေဆိပ် တည်နေရာ၊ ဆိုက်ရောက်ရာ လေဆိပ် တည်နေရာ၊ ထွက်ခွာချိန်၊ ဆိုက်ရောက်ချိန်၊ ပျံသန်းမှု အမှတ်အသားများ၊ ထိုင်ခုံ အမျိုးအစား စာရင်းတို့ ပါဝင်သည်။",
        "preconditions": "လေယာဉ်လက်မှတ် ရှာဖွေဝယ်ယူခြင်း ဆိုင်ရာ ကိစ္စရပ်များတွင် ပျံသန်းမှုဆိုင်ရာ အသေးစိတ် အချက်အလက်များကို ရယူရန် လိုအပ်သည်။",
        "postconditions": "ပျံသန်းမှုဆိုင်ရာ အသေးစိတ် အချက်အလက်များကို ပြန်လည်ပေးပို့ပြီး၊ အသုံးပြုသူအား ထိုင်ခုံရွေးချယ်ရန်နှင့် အော်ဒါတင်ရန် လမ်းညွှန်သည်။",
        "args": {
            "flight_id": "ပျံသန်းမှု အိုင်ဒီ"
        },
        "returns": "ပျံသန်းမှုဆိုင်ရာ အချက်အလက်များ",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ရထားအချက်အလက်ကို ရယူပါ၊ ရထား အိုင်ဒီ၊ ရထားအမှတ်၊ ထွက်ခွာမည့်မြို့၊ ရောက်ရှိမည့်မြို့၊ ထွက်ခွာမည့်ဘူတာရုံတည်နေရာ၊ ရောက်ရှိမည့်ဘူတာရုံတည်နေရာ၊ ထွက်ခွာချိန်၊ ရောက်ရှိချိန်၊ ရထားအမှတ်အသားများ၊ ထိုင်ခုံအမျိုးအစားစာရင်းတို့ ပါဝင်သည်။",
        "preconditions": "ရထားလက်မှတ် စုံစမ်းမေးမြန်းခြင်းနှင့် ဝယ်ယူခြင်းဆိုင်ရာ အခြေအနေတွင် ရထား၏ အသေးစိတ်အချက်အလက်ကို ရယူရန် လိုအပါသည်။",
        "postconditions": "ရထား၏ အသေးစိတ်အချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး၊ အသုံးပြုသူအား ထိုင်ခုံရွေးချယ်ရန်နှင့် အော်ဒါတင်ရန် လမ်းညွှန်ပါသည်။",
        "args": {
            "train_id": "ရထား အိုင်ဒီ"
        },
        "returns": "ရထားအချက်အလက်",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "ခရီးသွားနှင့် ဟိုတယ် ဝန်ဆောင်မှု ကဏ္ဍတွင်၊ အသုံးပြုသူ၏ နေရာဒေသဆိုင်ရာ လိုအပ်ချက်များနှင့် နှစ်သက်မှုများအပေါ် အခြေခံ၍ သင့်လျော်သော ဟိုတယ်ရွေးချယ်စရာများကို အကြံပြုပေးပြီး ဟိုတယ် အခြေခံ အချက်အလက်များ (ဟိုတယ် အိုင်ဒီ၊ အမည်၊ အမှတ်ပေးမှု၊ အဆင့်သတ်မှတ်ချက်၊ လိပ်စာ၊ အမှတ်အသားများ) ကို ပံ့ပိုးပေးသည်။",
        "preconditions": "အသုံးပြုသူက ဟိုတယ် ချိန်းဆိုထားရန် တောင်းဆိုပြီး ဟိုတယ်နှင့် သက်ဆိုင်သော သော့ချက် စာလုံးများ သို့မဟုတ် နေရာဒေသကို ပေးထားသည်။",
        "postconditions": "သတ်မှတ်ချက်နှင့် ကိုက်ညီသော ဟိုတယ်စာရင်းကို ပြန်လည်ပေးပို့သည်။ ဟိုတယ် အသေးစိတ် အချက်အလက်များ (အခန်းစာရင်း၊ ဈေးနှုန်းများ စသည်) ကို ကြည့်ရှုလိုပါက ဟိုတယ် အသေးစိတ် အချက်အလက် မေးမြန်းခြင်း ကိရိယာကို အသုံးပြုရမည်ဖြစ်ပြီး အသုံးပြုသူအား ဟိုတယ်ကို ရွေးချယ်ရန် လမ်းညွှန်သည်။",
        "args": {
            "city_name": "မြို့ အမည်",
            "key_words": "ရှာဖွေရေး သော့ချက် စာလုံးများ (ဟိုတယ် အမည်၊ ဟိုတယ် မိတ်ဆက်ချက် စသည်တို့နှင့် ကိုက်ညီသည်)"
        },
        "returns": "ဟိုတယ် အခြေခံ အချက်အလက်များကို စနစ်တကျ ထုတ်ပေးသည်။",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "အသုံးပြုသူ၏ နေရာလိုအပ်ချက်နှင့် နှစ်သက်ရာအပေါ် အခြေခံ၍ သင့်လျော်သော ခရီးသွားဆွဲဆောင်မှုရွေးချယ်စရာများကို အကြံပြုပေးပြီး၊ ခရီးသွားဆွဲဆောင်မှု၏ အခြေခံအချက်အလက်များ (ခရီးသွားဆွဲဆောင်မှု အိုင်ဒီ၊ အမည်၊ လိပ်စာ၊ ဖော်ပြချက်၊ အဆင့်သတ်မှတ်ချက်၊ ဖွင့်လှစ်ချိန်) ကို ပေးပါသည်။",
        "preconditions": "အသုံးပြုသူသည် ခရီးသွားဆွဲဆောင်မှုကို ကြိုတင်မှာယူရန် တောင်းဆိုထားပြီး ခရီးသွားဆွဲဆောင်မှုနှင့် သက်ဆိုင်သော သော့ချက်စာလုံးများ သို့မဟုတ် နေရာဒေသကို ပေးထားသည်။",
        "postconditions": "သတ်မှတ်ချက်နှင့် ကိုက်ညီသော ခရီးသွားဆွဲဆောင်မှုစာရင်းကို ပြန်လည်ပေးပို့သည်၊ ခရီးသွားဆွဲဆောင်မှုအကြောင်းအရာ (လက်မှတ်စာရင်း၊ ဈေးနှုန်းများ စသည်) ကို ကြည့်ရှုလိုပါက ခရီးသွားဆွဲဆောင်မှုအကြောင်းအရာ စစ်ဆေးမေးမြန်းခြင်း ကိရိယာကို အသုံးပြုရမည်ဖြစ်ပြီး အသုံးပြုသူအား ခရီးသွားဆွဲဆောင်မှုကို ရွေးချယ်ရန် လမ်းညွှန်ပါသည်။",
        "args": {
            "city_name": "မြို့နာမည်",
            "key_words": "ရှာဖွေရေး သော့ချက်စာလုံးများ (ခရီးသွားဆွဲဆောင်မှု အမည်၊ တည်နေရာ၊ လိပ်စာ၊ ထူးခြားချက်များ စသည်တို့နှင့် ကိုက်ညီသည်)"
        },
        "returns": "ခရီးသွားဆွဲဆောင်မှုဆိုင်ရာ အခြေခံအချက်အလက်များကို စနစ်တကျ ထုတ်ပေးသည်",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "အသုံးပြုသူ၏ နေရာဒေသဆိုင်ရာ လိုအပ်ချက်များနှင့် နှစ်သက်ရာများအပေါ် အခြေခံ၍ သင့်လျော်သော လေယာဉ်ခရီးစဉ်များကို အကြံပြုပြီး လေယာဉ်ခရီးစဉ် အခြေခံအချက်အလက်များကို ပေးပါသည်။ လေယာဉ်ခရီးစဉ် အိုင်ဒီ၊ လေယာဉ်အမှတ်၊ ထွက်ခွာမြို့၊ ဆိုက်ရောက်မြို့၊ ထွက်ခွာလေဆိပ်တည်နေရာ၊ ဆိုက်ရောက်လေဆိပ်တည်နေရာ၊ ထွက်ခွာအချိန်၊ ဆိုက်ရောက်အချိန်နှင့် လေယာဉ်ခရီးစဉ် အမှတ်အသားများ ပါဝင်သည်။",
        "preconditions": "အသုံးပြုသူသည် လေယာဉ်ခရီးစဉ် ကြိုတင်မှာယူရန် တောင်းဆိုပြီး လေယာဉ်ခရီးစဉ်နှင့် သက်ဆိုင်သော သော့ချက်စာလုံးများ သို့မဟုတ် နေရာဒေသများကို ပေးသည်။",
        "postconditions": "သတ်မှတ်ချက်နှင့် ကိုက်ညီသော လေယာဉ်ခရီးစဉ်စာရင်းကို ပြန်လည်ပေးပို့သည်။ လေယာဉ်ခရီးစဉ် အသေးစိတ်အချက်အလက်များ (ထိုင်ခုံအမျိုးအစားစာရင်း၊ ဈေးနှုန်း၊ ရက်စွဲ စသည်) ကို ကြည့်ရှုလိုပါက လေယာဉ်ခရီးစဉ် အသေးစိတ်အချက်အလက် မေးမြန်းခြင်း ကိရိယာကို အသုံးပြုရမည်ဖြစ်ပြီး အသုံးပြုသူအား လေယာဉ်ခရီးစဉ်ကို ရွေးချယ်ရန် လမ်းညွှန်သည်။",
        "args": {
            "departure": "ထွက်ခွာမည့်မြို့",
            "destination": "ဆိုက်ရောက်မည့်မြို့"
        },
        "returns": "လေယာဉ်ခရီးစဉ် အခြေခံအချက်အလက်များကို စနစ်တကျ ထုတ်ပေးသည်",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "အသုံးပြုသူ၏ နေရာဒေသဆိုင်ရာ လိုအပ်ချက်များနှင့် ဦးစားပေးမှုများအပေါ် အခြေခံ၍ သင့်လျော်သော ရထားရွေးချယ်စရာများကို အကြံပြုပြီး ရထားလက်မှတ် အခြေခံအချက်အလက်များကို ပေးပို့သည်။ ၎င်းတွင် ရထားအိုင်ဒီ၊ ရထားအမှတ်၊ ထွက်ခွာမြို့၊ ရောက်ရှိမြို့၊ ထွက်ခွာဘူတာရုံတည်နေရာ၊ ရောက်ရှိဘူတာရုံတည်နေရာ၊ ထွက်ခွာအချိန်၊ ရောက်ရှိအချိန်နှင့် ရထားအမျိုးအစား အမှတ်အသားများ ပါဝင်သည်။",
        "preconditions": "အသုံးပြုသူသည် ရထားကြိုတင်မှာယူရန် တောင်းဆိုပြီး ရထားနှင့် သက်ဆိုင်သော သော့ချက်စာလုံးများ သို့မဟုတ် နေရာဒေသများကို ပေးထားသည်။",
        "postconditions": "သတ်မှတ်ချက်များနှင့် ကိုက်ညီသော ရထားလက်မှတ်စာရင်းကို ပြန်လည်ပေးပို့သည်။ ရထားလက်မှတ် အသေးစိတ်အချက်အလက်များ (ထိုင်ခုံအမျိုးအစားစာရင်း၊ ဈေးနှုန်း၊ ရက်စွဲ စသည်) ကို ကြည့်ရှုလိုပါက ရထားလက်မှတ် အသေးစိတ်အချက်အလက် မေးမြန်းခြင်း ကိရိယာကို အသုံးပြုရန်လိုအပ်ပြီး အသုံးပြုသူအား ရထားလက်မှတ်ကို ရွေးချယ်ရန် လမ်းညွှန်သည်။",
        "args": {
            "departure": "ထွက်ခွာမြို့",
            "destination": "ရောက်ရှိမည့်မြို့",
            "date": "ထွက်ခွာရက်စွဲ"
        },
        "returns": "ရထားအခြေခံအချက်အလက်များကို စနစ်တကျ ဖွဲ့စည်းထားသော ပုံစံဖြင့် ထုတ်ပေးသည်။",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "အသုံးပြုသူများ ဟိုတယ်အခန်းကြိုထားသည့်အခါ စနစ်သည် အသုံးပြုသူ၏ လိုအပ်ချက်များ (ဥပမာ - ဟိုတယ်အမည်၊ ဝင်ရောက်တည်းခံမည့်ရက်၊ လူဦးရေ စသည်) အပေါ်အခြေခံ၍ အော်ဒါကို ဖန်တီးပေးသည်။",
        "preconditions": "အသုံးပြုသူသည် စနစ်ထဲသို့ ဝင်ရောက်ပြီး မှန်ကန်သော အထောက်အထား (user_id) ပေးထားရမည်၊ အသုံးပြုသူသည် မှန်ကန်သော ဟိုတယ်အမည် (hotel_name) နှင့် အခန်းအမျိုးအစား (room_type) ကို ပေးထားရမည်၊ စနစ်တွင် သက်ဆိုင်ရာ ဟိုတယ်အကြောင်းအချက်အလက်များ ရှိရမည် ထို့အပြင် ထိုဟိုတယ်သည် တောင်းဆိုထားသော ရက်စွဲများတွင် အခန်းလွတ် ရှိရမည်။",
        "postconditions": "အော်ဒါကို ဖန်တီးပြီး အသုံးပြုသူအား ငွေချေသင်္ချာမှုကို အတည်ပြုရန် တောင်းဆိုသည်။",
        "args": {
            "hotel_id": "ဟိုတယ် အိုင်ဒီ",
            "room_id": "အခန်း အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "အော်ဒါဖန်တီးခြင်း လုပ်ဆောင်ချက်၏ တုံ့ပြန်မှု ရလဒ်။",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "အသုံးပြုသူများသည် ခရီးသွားနေရာနှင့် ရက်စွဲအလိုက် လက်မှတ်များကို ဝယ်ယူပြီး စနစ်က လက်မှတ်အချက်အလက်များကို ပြန်လည်ပေးကာ အော်ဒါတင်ပေးသည်။",
        "preconditions": "ခရီးသွားနေရာစခန်းများတွင် အသုံးပြုသူက နေရာကြိုတင်မှာကြားရန် တောင်းဆိုပြီး မှာကြားရန် လိုအပ်သော အချက်အလက်များကို ပေးသည်။",
        "postconditions": "အော်ဒါကို ဖန်တီးပြီး အသုံးပြုသူအား ငွေချေခြင်းကို အတည်ပြုရန် တောင်းဆိုသည်။",
        "args": {
            "attraction_id": "ခရီးသွားနေရာ ID",
            "ticket_id": "လက်မှတ် ID",
            "user_id": "အသုံးပြုသူ ID",
            "date": "လည်ပတ်မည့်ရက်စွဲ၊ ပုံစံမှာ %Y-%m-%d",
            "quantity": "အရေအတွက်"
        },
        "returns": "အော်ဒါဖန်တီးခြင်း လုပ်ဆောင်ချက်၏ တုံ့ပြန်မှု ရလဒ်",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "အသုံးပြုသူများသည် ခရီးစဉ်အမှတ်၊ ရက်စွဲ၊ ထိုင်ခုံအမျိုးအစားနှင့် အရေအတွက်အပေါ်မူတည်၍ လေယာဉ်လက်မှတ်များကို ဝယ်ယူပြီး စနစ်က လက်မှတ်အချက်အလက်များကို ပြန်လည်ပေးကာ အော်ဒါတင်ပေးသည်။",
        "preconditions": "လေယာဉ်လက်မှတ် ရှာဖွေဝယ်ယူခြင်း ဆက်စပ်မှုတွင် အသုံးပြုသူက ခရီးစဉ်ကြိုတင်မှာကြားရန် တောင်းဆိုပြီး ကြိုတင်မှာကြားရန် လိုအပ်သော အချက်အလက်များကို ပေးသည်။",
        "postconditions": "အော်ဒါကို ဖန်တီးပြီး အသုံးပြုသူအား ငွေချေခြင်းကို အတည်ပြုရန် တောင်းဆိုသည်။",
        "args": {
            "flight_id": "လေယာဉ်ခရီးစဉ် အိုင်ဒီ",
            "seat_id": "ထိုင်ခုံ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "date": "ထွက်ခွာမည့် ရက်စွဲ",
            "quantity": "အရေအတွက်"
        },
        "returns": "အော်ဒါဖန်တီးခြင်း လုပ်ဆောင်ချက်၏ တုံ့ပြန်မှု ထွက်ရှိချက်",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "အသုံးပြုသူများသည် ရထားအမှတ်၊ ရက်စွဲ၊ ထိုင်ခုံအမျိုးအစားနှင့် အရေအတွက်အပေါ်အခြေခံ၍ ရထားလက်မှတ်များကို ဝယ်ယူပြီး စနစ်က ရထားလက်မှတ်ဆိုင်ရာ အချက်အလက်များကို ပြန်လည်ပေးကာ အော်ဒါတင်ပေးသည်။",
        "preconditions": "ရထားလက်မှတ် စစ်ဆေးဝယ်ယူခြင်း ဆောင်ရွက်ချက်တွင် အသုံးပြုသူက ရထားကြိုတင်မှာကြားရန် တောင်းဆိုပြီး ကြိုတင်မှာကြားခြင်းနှင့် သက်ဆိုင်သော လိုအပ်သည့် အချက်အလက်များကို ပေးသည်။",
        "postconditions": "အော်ဒါကို ဖန်တီးပြီး အသုံးပြုသူအား ငွေချေခြင်းကို အတည်ပြုရန် တောင်းဆိုသည်။",
        "args": {
            "train_id": "ရထား အိုင်ဒီ",
            "seat_id": "ထိုင်ခုံ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "date": "ထွက်ခွာမည့် ရက်စွဲ",
            "quantity": "အရေအတွက်"
        },
        "returns": "အော်ဒါဖန်တီးခြင်း လုပ်ဆောင်ချက်၏ တုံ့ပြန်မှု ထုတ်လွှတ်ချက်",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "အသုံးပြုသူ ဟိုတယ်အော်ဒါ ငွေပေးချေခြင်း",
        "preconditions": "ဟိုတယ် ကြိုတင်မှာယူမှု ရှာဖွေခြင်း အခြေအနေတွင် အသုံးပြုသူသည် ဟိုတယ်အော်ဒါကို ငွေပေးချေရန် တောင်းဆိုပြီး ယခင်စကားဝိုင်းတွင် အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်",
        "postconditions": "ငွေပေးချေမှုကို အတည်ပြုပြီး အော်ဒါအခြေအနေကို ငွေပေးချေပြီးသားအဖြစ် အပ်ဒိတ်လုပ်သည်",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "ငွေပေးချေမှု ရလဒ်အချက်အလက်",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "အသုံးပြုသူများမှ လက်မှတ်အော်ဒါ ပေးချေခြင်း",
        "preconditions": "ခရီးသွားနေရာများဆိုင်ရာ အခြေအနေတွင် အသုံးပြုသူသည် ခရီးသွားနေရာ လက်မှတ်အော်ဒါကို ပေးချေရန် တောင်းဆိုပြီး အထက်တွင် အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "ပေးချေမှုကို အတည်ပြုကာ အော်ဒါအခြေအနေကို ပေးချေပြီးဟု အပ်ဒိတ်လုပ်သည်။",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "ပေးချေမှုရလဒ် အချက်အလက်",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "အသုံးပြုသူများ လေယာဉ်လက်မှတ် အော်ဒါ ပေးချေခြင်း",
        "preconditions": "လေယာဉ်လက်မှတ် ရှာဖွေဝယ်ယူခြင်း ကိစ္စရပ်တွင် အသုံးပြုသူက လေယာဉ်ခရီး အော်ဒါကို ပေးချေရန် တောင်းဆိုထားပြီး ယခင်အပိုင်းတွင် အော်ဒါ အိုင်ဒီကို သတ်မှတ်ထားပြီးဖြစ်သည်",
        "postconditions": "ပေးချေမှုကို အတည်ပြုကာ အော်ဒါ အခြေအနေကို ပေးချေပြီးသား အဖြစ် အပ်ဒိတ်လုပ်သည်",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "ပေးချေမှု ရလဒ် အချက်အလက်",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "အသုံးပြုသူများ မီးရထားလက်မှတ် အော်ဒါများကို ငွေချေခြင်း",
        "preconditions": "မီးရထားလက်မှတ် ရှာဖွေဝယ်ယူခြင်း ကိစ္စရပ်တွင် အသုံးပြုသူက မီးရထားလက်မှတ် အော်ဒါကို ငွေချေရန် တောင်းဆိုထားပြီး အထက်တွင် အော်ဒါ အိုင်ဒီကို သတ်မှတ်ထားသည်",
        "postconditions": "ငွေချေမှုကို အတည်ပြုကာ အော်ဒါ အခြေအနေကို ငွေချေပြီးသား အဖြစ် အပ်ဒိတ်လုပ်သည်",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ"
        },
        "returns": "ငွေချေမှု ရလဒ် အချက်အလက်",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "အသုံးပြုသူ ID အပေါ်အခြေခံ၍ အသုံးပြုသူ၏ ဟိုတယ်အမှာစာများကို စစ်ဆေးပြီး အမှာစာ ID၊ အမှာစာအမျိုးအစား၊ အသုံးပြုသူ ID၊ ဟိုတယ် ID၊ အမှာစာစုစုပေါင်းတန်ဖိုး၊ အမှာစာတင်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်နှင့် အမှာစာအခြေအနေတို့ ပါဝင်သော အချက်အလက်များကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "အသုံးပြုသူ၏ လိုအပ်ချက်မှာ ဟိုတယ်အမှာစာများကို စစ်ဆေးရန်ဖြစ်သည်။",
        "postconditions": "အမှာစာအချက်အလက်များကို ပြန်လည်ပေးပို့ပြီး နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်း ပြုလုပ်ရန် လွယ်ကူစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ ID",
            "date": "ရက်စွဲ",
            "status": "အမှာစာအခြေအနေ"
        },
        "returns": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ ဟိုတယ်အမှာစာအချက်အလက်များ",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "အသုံးပြုသူ ID အပေါ်အခြေခံ၍ အသုံးပြုသူ၏ ခရီးသွားဆွဲဆောင်မှု လက်မှတ်အော်ဒါများကို စစ်ဆေးပြီး အော်ဒါ ID၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူ ID၊ ခရီးသွားဆွဲဆောင်မှု ID၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါတင်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်နှင့် အော်ဒါအခြေအနေတို့ ပါဝင်သော အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "အသုံးပြုသူ၏ လိုအပ်ချက်မှာ ခရီးသွားဆွဲဆောင်မှု လက်မှတ်အော်ဒါများကို စစ်ဆေးရန်ဖြစ်သည်။",
        "postconditions": "အော်ဒါအချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်း ပြုလုပ်ရန် လွယ်ကူစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ ID",
            "date": "ရက်စွဲ",
            "status": "အော်ဒါအခြေအနေ"
        },
        "returns": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ ခရီးသွားဆွဲဆောင်မှု လက်မှတ်အော်ဒါ အချက်အလက်",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "အသုံးပြုသူ ID အလိုက် အသုံးပြုသူ၏ လေယာဉ်လက်မှတ် အော်ဒါကို စစ်ဆေးပြီး အော်ဒါ ID၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူ ID၊ လေယာဉ်ခရီးစဉ် ID၊ အော်ဒါ စုစုပေါင်းတန်ဖိုး၊ အော်ဒါပြုလုပ်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်နှင့် အော်ဒါအခြေအနေတို့ ပါဝင်သော အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "အသုံးပြုသူ၏ လိုအပ်ချက်မှာ လေယာဉ်လက်မှတ် အော်ဒါကို စစ်ဆေးရန်ဖြစ်သည်။",
        "postconditions": "အော်ဒါအချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်း ပြုလုပ်ရန် လွယ်ကူစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ ID",
            "date": "ရက်စွဲ",
            "status": "အော်ဒါအခြေအနေ"
        },
        "returns": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ လေယာဉ်လက်မှတ် အော်ဒါအချက်အလက်",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "အသုံးပြုသူ ID အပေါ်အခြေခံ၍ အသုံးပြုသူ၏ မီးရထားလက်မှတ် အော်ဒါများကို စစ်ဆေးပြီး အော်ဒါ ID၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူ ID၊ မီးရထား ID၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါမှာကြားသည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်နှင့် အော်ဒါအခြေအနေတို့ ပါဝင်သော အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "preconditions": "အသုံးပြုသူ၏ လိုအပ်ချက်မှာ မီးရထားလက်မှတ် အော်ဒါများကို စစ်ဆေးရန် ဖြစ်သည်။",
        "postconditions": "အော်ဒါအချက်အလက်ကို ပြန်လည်ပေးပို့ပြီး နောက်ပိုင်းတွင် ပြင်ဆင်ခြင်း သို့မဟုတ် ပယ်ဖျက်ခြင်း ပြုလုပ်ရန် လွယ်ကူစေသည်။",
        "args": {
            "user_id": "အသုံးပြုသူ ID",
            "date": "ရက်စွဲ",
            "status": "အော်ဒါအခြေအနေ"
        },
        "returns": "သတ်မှတ်ထားသော အသုံးပြုသူ၏ မီးရထားလက်မှတ် အော်ဒါအချက်အလက်",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ဟိုတယ်အော်ဒါအသေးစိတ်ကို ရယူသည်၊ အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ ဟိုတယ်အိုင်ဒီ၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါပြုလုပ်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေနှင့် အော်ဒါအခန်းအသေးစိတ်အချက်အလက်များ (အခန်းအမျိုးအစား၊ ဝင်ရောက်နေထိုင်မည့်ရက်စွဲ၊ ဈေးနှုန်း၊ အခန်းအိုင်ဒီ) တို့ ပါဝင်သည်",
        "preconditions": "အသုံးပြုသူက ဟိုတယ်အော်ဒါအသေးစိတ်ကို ရယူရန် တောင်းဆိုထားပြီး ယခင်အချက်အလက်များတွင် အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်",
        "postconditions": "အော်ဒါအသေးစိတ်ကို ပြန်လည်ပေးပို့သည်",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "အော်ဒါအသေးစိတ်",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "ခရီးသွားဆွဲဆောင်မှု လက်မှတ်အော်ဒါ အသေးစိတ်ကို ရယူခြင်းဖြစ်ပြီး အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ ခရီးသွားဆွဲဆောင်မှုအိုင်ဒီ၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါပြုလုပ်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေနှင့် အော်ဒါ ခရီးသွားဆွဲဆောင်မှု အသေးစိတ်အချက်အလက်များ (လက်မှတ်အမျိုးအစား၊ ရက်စွဲ၊ ဈေးနှုန်း၊ လက်မှတ်အိုင်ဒီ) တို့ ပါဝင်သည်။",
        "preconditions": "အသုံးပြုသူသည် ခရီးသွားဆွဲဆောင်မှု လက်မှတ်အော်ဒါ အသေးစိတ်ကို ရယူရန် တောင်းဆိုထားပြီး အထက်တွင် အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါအသေးစိတ်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "အော်ဒါအသေးစိတ်",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "လေယာဉ်လက်မှတ် အော်ဒါအသေးစိတ်အချက်အလက်ကို ရယူခြင်း၊ အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ လေယာဉ်ခရီးအိုင်ဒီ၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါပြုလုပ်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေနှင့် အော်ဒါရှိ လေယာဉ်လက်မှတ် အသေးစိတ်အချက်အလက်များ (ထိုင်ခုံအမျိုးအစား၊ ရက်စွဲ၊ ဈေးနှုန်း၊ ထိုင်ခုံအိုင်ဒီ) တို့ ပါဝင်သည်။",
        "preconditions": "အသုံးပြုသူသည် လေယာဉ်လက်မှတ် အော်ဒါအသေးစိတ်အချက်အလက်ကို ရယူရန် တောင်းဆိုပြီး၊ အထက်တွင် အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါအသေးစိတ်အချက်အလက်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "အော်ဒါအသေးစိတ်အချက်အလက်",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ရထားလက်မှတ် အော်ဒါအသေးစိတ်ကို ရယူခြင်း၊ အော်ဒါအိုင်ဒီ၊ အော်ဒါအမျိုးအစား၊ အသုံးပြုသူအိုင်ဒီ၊ ရထားအိုင်ဒီ၊ အော်ဒါစုစုပေါင်းတန်ဖိုး၊ အော်ဒါပြုလုပ်သည့်အချိန်၊ အပ်ဒိတ်လုပ်သည့်အချိန်၊ အော်ဒါအခြေအနေနှင့် အော်ဒါရထားလက်မှတ် အသေးစိတ်အချက်အလက်များ (ထိုင်ခုံအမျိုးအစား၊ ရက်စွဲ၊ ဈေးနှုန်း၊ ထိုင်ခုံအိုင်ဒီ) တို့ ပါဝင်သည်။",
        "preconditions": "အသုံးပြုသူက ရထားလက်မှတ် အော်ဒါအသေးစိတ်ကို ရယူရန် တောင်းဆိုပြီး ယခင်က အော်ဒါအိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါအသေးစိတ်ကို ပြန်လည်ပေးပို့သည်။",
        "args": {
            "order_id": "အော်ဒါအိုင်ဒီ"
        },
        "returns": "အော်ဒါအသေးစိတ်",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "ရထားလက်မှတ် အော်ဒါကို ပြင်ဆန်ခြင်း၊ ထွက်ခွာရက်စွဲကို ပြောင်းလဲခြင်းကို ပံ့ပိုးပေးသည်၊ ကွာခြားသောကြေး ပေးချေခြင်း သို့မဟုတ် ပြန်အမ်းခြင်းကို အလိုအလျောက် ကိုင်တွယ်သည်။",
        "preconditions": "ရထားလက်မှတ် စစ်ဆေးခြင်းနှင့် ဝယ်ယူခြင်း ဆိုင်ရာ အခြေအနေတွင်၊ အသုံးပြုသူက ရထားလက်မှတ် အော်ဒါကို ပြင်ဆန်ရန် တောင်းဆိုပြီး၊ အထက်တွင် အော်ဒါ အိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါကို ပြင်ဆန်ပြီး အော်ဒါ အခြေအနေကို အပ်ဒိတ်လုပ်ပါ၊ ကွာခြားသောကြေး ပေးချေရန်လိုအပ်ပါက အော်ဒါ အခြေအနေကို unpaid သို့ ပြောင်းလဲပါ၊ သို့မဟုတ်ပါက မူလအခြေအနေအတိုင်း ထားရှိပါ၊ ကွာခြားသောကြေး ပေးချေရန်လိုအပ်ပါက အသုံးပြုသူအား ယခုအော်ဒါကို ပေးချေရန် လမ်းညွှန်ပေးရပါမည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "new_date": "ထွက်ခွာရန် အသစ်သတ်မှတ်ထားသော ရက်စွဲ၊ ပုံစံမှာ %Y-%m-%d ဖြစ်သည်"
        },
        "returns": "(ပြင်ဆန်ပြီးသော အော်ဒါ အကြောင်းအရာ၊ ကွာခြားသောကြေး၊ အပေါင်းကိန်းသည် ကွာခြားသောကြေး ပေးချေရန်လိုအပ်ကြောင်း၊ အနှုတ်ကိန်းသည် ကွာခြားသောကြေး ပြန်အမ်းကြောင်း)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "လေယာဉ်လက်မှတ် အော်ဒါကို ပြင်ဆင်ခြင်း၊ ထွက်ခွာရက်စွဲကို ပြောင်းလဲခြင်းကို ပံ့ပိုးပေးပြီး၊ ကွာခြားသော ဈေးနှုန်းကို ပေးချေခြင်း သို့မဟုတ် ပြန်အမ်းခြင်းကို အလိုအလျောက် ကိုင်တွယ်ဖြေရှင်းပေးသည်။",
        "preconditions": "လေယာဉ်လက်မှတ် ရှာဖွေဝယ်ယူသည့် အခြေအနေတွင်၊ အသုံးပြုသူက လေယာဉ်လက်မှတ် အော်ဒါကို ပြင်ဆန်ရန် တောင်းဆိုပြီး၊ အထက်တွင် အော်ဒါ အိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါကို ပြင်ဆင်ပြီး အော်ဒါ အခြေအနေကို အပ်ဒိတ်လုပ်ပါ၊ ကွာခြားသော ဈေးနှုန်း ပေးချေရန် လိုအပ်ပါက၊ အော်ဒါ အခြေအနေကို unpaid သို့ ပြောင်းလဲပါ၊ သို့မဟုတ်ပါက မူလအခြေအနေအတိုင်း ထားရှိပါ၊ ကွာခြားသော ဈေးနှုန်း ပေးချေရန် လိုအပ်ပါက၊ အသုံးပြုသူအား ယခုအော်ဒါကို ပေးချေရန် လမ်းညွှန်ပေးရပါမည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ",
            "new_date": "အသစ် ထွက်ခွာရက်စွဲ၊ ပုံစံမှာ %Y-%m-%d ဖြစ်သည်"
        },
        "returns": "(ပြင်ဆင်ပြီးသော အော်ဒါ အကြောင်းအရာ၊ ဈေးနှုန်း ကွာခြားချက်၊ အပေါင်းကိန်းသည် ကွာခြားသော ဈေးနှုန်း ပေးချေရန်လို၊ အနှုတ်ကိန်းသည် ကွာခြားသော ဈေးနှုန်း ပြန်အမ်းရန်လို)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "အသုံးပြုသူက ကြိုတင်မှာကြားထားသော ဟိုတယ်အော်ဒါကို ပယ်ဖျက်သည်။",
        "preconditions": "ဟိုတယ် ကြိုတင်မှာကြားမှု စစ်ဆေးသည့် အခြေအနေတွင်၊ အသုံးပြုသူက ဟိုတယ်အော်ဒါကို ပယ်ဖျက်ရန် တောင်းဆိုပြီး၊ အထက်တွင် အော်ဒါ အိုင်ဒီကို သတ်မှတ်ထားသည်။",
        "postconditions": "အော်ဒါကို ပယ်ဖျက်ပြီး အော်ဒါ အခြေအနေကို အပ်ဒိတ်လုပ်ပါ၊ ဈေးကွာခြားချက် ပြန်အမ်းရန် လိုအပ်ပါက အသုံးပြုသူကို အကြောင်းကြားပါ။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "အော်ဒါ ပယ်ဖျက်မှုအတွက် ပြန်အမ်းငွေ ပမာဏ",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "အသုံးပြုသူသည် ကြိုတင်မှာကြားထားသော ခရီးသွားနေရာလက်မှတ် အော်ဒါကို ပယ်ဖျားသည်",
        "preconditions": "သမိုင်းကြောင်း ဆွေးနွေးချက်တွင် အော်ဒါ အိုင်ဒီ ပါရှိသည် သို့မဟုတ် အော်ဒါ စစ်ဆေးမှု ပြုလုပ်ပြီးဖြစ်သည်၊ အသုံးပြုသူတွင် ဤအော်ဒါကို ပယ်ဖျားခွင့် ရှိသည်",
        "postconditions": "အကယ်၍ ဈေးကွာခြားချက် ပြန်အမ်းပါက အသုံးပြုသူကို အကြောင်းကြားပါ",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "အော်ဒါ ပယ်ဖျားခြင်းဆိုင်ရာ ပြန်အမ်းငွေ ပမာဏ",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "အသုံးပြုသူသည် ကြိုတင်မှာကြားထားသော လေယာဉ်လက်မှတ် အော်ဒါကို ပယ်ဖျက်သည်။",
        "preconditions": "ယခင် ဆွေးနွေးမှုများတွင် အော်ဒါ အိုင်ဒီ ပါရှိသည် သို့မဟုတ် အော်ဒါကို စစ်ဆေးထားပြီးဖြစ်သည်၊ အသုံးပြုသူတွင် ဤအော်ဒါကို ပယ်ဖျက်ခွင့် ရှိသည်။",
        "postconditions": "ကွာခြားငွေ ပြန်အမ်းပါက အသုံးပြုသူကို အကြောင်းကြားရုံသာ ဖြစ်သည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "အော်ဒါ ပယ်ဖျက်ခြင်းအတွက် ပြန်အမ်းငွေ ပမာဏ",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "အသုံးပြုသူက ကြိုတင်မှာကြားထားသော မီးရထားလက်မှတ် အော်ဒါကို ပယ်ဖျားသည်။",
        "preconditions": "သမိုင်းကြောင်း ဆွေးနွေးချက်တွင် အော်ဒါ အိုင်ဒီ ပါရှိသည် သို့မဟုတ် အော်ဒါ စစ်ဆေးမှု ပြုလုပ်ပြီးဖြစ်သည်၊ အသုံးပြုသူတွင် ဤအော်ဒါကို ပယ်ဖျားခွင့် ရှိသည်။",
        "postconditions": "အကယ်၍ ဈေးကွာခြားချက် ပြန်အမ်းငွေ ရှိပါက အသုံးပြုသူအား အကြောင်းကြားရုံသာ ဖြစ်သည်။",
        "args": {
            "order_id": "အော်ဒါ အိုင်ဒီ",
            "user_id": "အသုံးပြုသူ အိုင်ဒီ"
        },
        "returns": "အော်ဒါ ပယ်ဖျားမှုအတွက် ပြန်အမ်းငွေ ပမာဏ",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Khmer version
TOOL_DESCRIPTIONS_KM = {
    "get_ota_hotel_info": {
        "description": "ទទួលបានព័ត៌មានសណ្ឋាគារ រួមមានលេខសម្គាល់សណ្ឋាគារ ឈ្មោះ ពិន្ទុ ចំណាត់ថ្នាក់ផ្កាយ អាសយដ្ឋាន ផ្លាកសម្គាល់ និងបញ្ជីបន្ទប់",
        "preconditions": "នៅក្នុងស្ថានភាពស្វែងរក និងកក់សណ្ឋាគារ ត្រូវការទទួលបានព័ត៌មានលម្អិតរបស់សណ្ឋាគារ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតរបស់សណ្ឋាគារ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសបន្ទប់ និងដាក់ពាក្យកុម្ម៉ង់",
        "args": {
            "hotel_id": "លេខសម្គាល់សណ្ឋាគារ"
        },
        "returns": "ព័ត៌មានសណ្ឋាគារ",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "ទទួលបានព័ត៌មានអំពីកន្លែងទេសចរណ៍ រួមមានលេខសម្គាល់កន្លែងទេសចរណ៍ ឈ្មោះ អាសយដ្ឋាន ការពិពណ៌នា ចំណាត់ថ្នាក់ ម៉ោងបើក តម្លៃសំបុត្រ និងបញ្ជីប្រភេទសំបុត្រ",
        "preconditions": "នៅក្នុងស្ថានភាពទេសចរណ៍កន្លែងទេសចរណ៍ ត្រូវការទទួលបានព័ត៌មានលម្អិតអំពីកន្លែងទេសចរណ៍",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតអំពីកន្លែងទេសចរណ៍ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសសំបុត្រ និងបញ្ជាទិញ",
        "args": {
            "attraction_id": "លេខសម្គាល់កន្លែងទេសចរណ៍"
        },
        "returns": "ព័ត៌មានកន្លែងទេសចរណ៍",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "ទទួលបានព័ត៌មានជើងហោះហើរ រួមមានលេខសម្គាល់ជើងហោះហើរ លេខជើងហោះហើរ ទីក្រុងចាកចេញ ទីក្រុងមកដល់ ទីតាំងអាកាសយានដ្ឋានចាកចេញ ទីតាំងអាកាសយានដ្ឋានមកដល់ ពេលចាកចេញ ពេលមកដល់ ស្លាកជើងហោះហើរ និងបញ្ជីប្រភេទកៅអី",
        "preconditions": "នៅក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្រយន្តហោះ ត្រូវការទទួលបានព័ត៌មានលម្អិតរបស់ជើងហោះហើរ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតរបស់ជើងហោះហើរ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសកៅអី និងបញ្ជាទិញ",
        "args": {
            "flight_id": "លេខសម្គាល់ជើងហោះហើរ"
        },
        "returns": "ព័ត៌មានជើងហោះហើរ",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ទទួលបានព័ត៌មានរថភ្លើង រួមមានលេខសម្គាល់រថភ្លើង លេខជើងរថភ្លើង ក្រុងចេញដំណើរ ក្រុងមកដល់ ទីតាំងស្ថានីយចេញដំណើរ ទីតាំងស្ថានីយមកដល់ ម៉ោងចេញដំណើរ ម៉ោងមកដល់ ស្លាករថភ្លើង និងបញ្ជីប្រភេទកៅអី",
        "preconditions": "នៅក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្ររថភ្លើង ត្រូវការទទួលបានព័ត៌មានលម្អិតអំពីរថភ្លើង",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតអំពីរថភ្លើង ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសកៅអី និងដាក់ពាក្យបញ្ជាទិញ",
        "args": {
            "train_id": "លេខសម្គាល់រថភ្លើង"
        },
        "returns": "ព័ត៌មានរថភ្លើង",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "ក្នុងបរិបទនៃការធ្វើដំណើរ និងស្នាក់នៅ ផ្អែកលើតម្រូវការទីតាំង និងចំណូលចិត្តរបស់អ្នកប្រើប្រាស់ ណែនាំជម្រើសសណ្ឋាគារដែលសមស្រប ផ្តល់នូវព័ត៌មានមូលដ្ឋានរបស់សណ្ឋាគារ រួមមានលេខសម្គាល់សណ្ឋាគារ ឈ្មោះ ពិន្ទុ ចំណាត់ថ្នាក់ផ្កាយ អាសយដ្ឋាន និងស្លាកសញ្ញា",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំកក់សណ្ឋាគារ ដោយបានផ្តល់ពាក្យគន្លឹះ ឬទីតាំងដែលពាក់ព័ន្ធនឹងសណ្ឋាគារ",
        "postconditions": "ត្រឡប់មកវិញនូវបញ្ជីសណ្ឋាគារដែលសមស្របតាមលក្ខខណ្ឌ ប្រសិនបើត្រូវការមើលព័ត៌មានលម្អិតរបស់សណ្ឋាគារ (បញ្ជីបន្ទប់ តម្លៃ ជាដើម) ត្រូវតែប្រើឧបករណ៍ស្វែងរកព័ត៌មានលម្អិតសណ្ឋាគារ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសសណ្ឋាគារ",
        "args": {
            "city_name": "ឈ្មោះក្រុង",
            "key_words": "ពាក្យគន្លឹះស្វែងរក (ផ្គូផ្គងឈ្មោះសណ្ឋាគារ ការណែនាំអំពីសណ្ឋាគារ ជាដើម)"
        },
        "returns": "បង្ហាញព័ត៌មានមូលដ្ឋានរបស់សណ្ឋាគារជាទម្រង់មានរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "ផ្អែកលើតម្រូវការទីតាំង និងចំណង់ចំណូលចិត្តរបស់អ្នកប្រើប្រាស់ ណែនាំជម្រើសកន្លែងទេសចរណ៍ដែលសមស្រប ផ្តល់នូវព័ត៌មានមូលដ្ឋានរបស់កន្លែងទេសចរណ៍ រួមមាន id កន្លែងទេសចរណ៍ ឈ្មោះ អាសយដ្ឋាន ការពិពណ៌នា ពិន្ទុ និងម៉ោងបើក",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំកក់កន្លែងទេសចរណ៍ បានផ្តល់នូវពាក្យគន្លឹះ ឬទីតាំងដែលពាក់ព័ន្ធនឹងកន្លែងទេសចរណ៍",
        "postconditions": "ត្រឡប់មកវិញនូវបញ្ជីកន្លែងទេសចរណ៍ដែលត្រូវនឹងលក្ខខណ្ឌ ប្រសិនបើចង់មើលព័ត៌មានលម្អិតរបស់កន្លែងទេសចរណ៍ (បញ្ជីសំបុត្រ តម្លៃ ជាដើម) ត្រូវប្រើឧបករណ៍ស្វែងរកព័ត៌មានលម្អិតកន្លែងទេសចរណ៍ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសកន្លែងទេសចរណ៍",
        "args": {
            "city_name": "ឈ្មោះក្រុង",
            "key_words": "ពាក្យគន្លឹះស្វែងរក (ផ្គូផ្គងឈ្មោះកន្លែងទេសចរណ៍ ទីតាំង អាសយដ្ឋាន លក្ខណៈពិសេស ជាដើម)"
        },
        "returns": "បង្ហាញព័ត៌មានមូលដ្ឋានរបស់កន្លែងទេសចរណ៍ជាទម្រង់មានរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "ផ្អែកលើតម្រូវការទីតាំង និងចំណូលចិត្តរបស់អ្នកប្រើប្រាស់ ណែនាំជម្រើសជើងហោះហើរដែលសមស្រប ផ្តល់នូវព័ត៌មានមូលដ្ឋានរបស់ជើងហោះហើរ រួមមានលេខសម្គាល់ជើងហោះហើរ លេខជើងហោះហើរ ទីក្រុងចាកចេញ ទីក្រុងមកដល់ ទីតាំងអាកាសយានដ្ឋានចាកចេញ ទីតាំងអាកាសយានដ្ឋានមកដល់ ពេលចាកចេញ ពេលមកដល់ និងស្លាកសញ្ញាជើងហោះហើរ",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំកក់ជើងហោះហើរ ដោយបានផ្តល់ពាក្យគន្លឹះ ឬទីតាំងដែលពាក់ព័ន្ធនឹងជើងហោះហើរ",
        "postconditions": "ត្រឡប់មកវិញនូវបញ្ជីជើងហោះហើរដែលត្រូវនឹងលក្ខខណ្ឌ ប្រសិនបើត្រូវការមើលព័ត៌មានលម្អិតរបស់ជើងហោះហើរ (បញ្ជីប្រភេទកៅអី តម្លៃ កាលបរិច្ឆេទ ជាដើម) ត្រូវប្រើឧបករណ៍ស្វែងរកព័ត៌មានលម្អិតជើងហោះហើរ ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសជើងហោះហើរ",
        "args": {
            "departure": "ទីក្រុងចាកចេញ",
            "destination": "ទីក្រុងគោលដៅ"
        },
        "returns": "បង្ហាញព័ត៌មានមូលដ្ឋានរបស់ជើងហោះហើរជាទម្រង់មានរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "ផ្អែកលើតម្រូវការទីតាំង និងចំណូលចិត្តរបស់អ្នកប្រើប្រាស់ ណែនាំជម្រើសរថភ្លើងដែលសមស្រប ផ្តល់នូវព័ត៌មានមូលដ្ឋានរបស់សំបុត្ររថភ្លើង រួមមានលេខសម្គាល់រថភ្លើង លេខជើងរថភ្លើង ទីក្រុងចាការចេញ ទីក្រុងចាការដល់ ទីតាំងស្ថានីយ៍ចាការចេញ ទីតាំងស្ថានីយ៍ចាការដល់ ពេលវេលាចាការចេញ ពេលវេលាចាការដល់ និងស្លាកស្នាមរថភ្លើង",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំកក់រថភ្លើង បានផ្តល់នូវពាក្យគន្លឹះ ឬទីតាំងដែលពាក់ព័ន្ធនឹងរថភ្លើង",
        "postconditions": "ត្រឡប់មកវិញនូវបញ្ជីសំបុត្ររថភ្លើងដែលត្រូវនឹងលក្ខខណ្ឌ ប្រសិនបើត្រូវការមើលព័ត៌មានលម្អិតរបស់សំបុត្ររថភ្លើង (បញ្ជីប្រភេទកៅអី តម្លៃ កាលបរិច្ឆេទ ជាដើម) ត្រូវប្រើឧបករណ៍ស្វែងរកព័ត៌មានលម្អិតសំបុត្ររថភ្លើង ណែនាំអ្នកប្រើប្រាស់ឱ្យជ្រើសរើសសំបុត្ររថភ្លើង",
        "args": {
            "departure": "ទីក្រុងចាការចេញ",
            "destination": "ទីក្រុងគោលដៅ",
            "date": "កាលបរិច្ឆេទចាការចេញ"
        },
        "returns": "បង្ហាញព័ត៌មានមូលដ្ឋានរបស់រថភ្លើងជាទម្រង់មានរចនាសម្ព័ន្ធ",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "នៅពេលអ្នកប្រើប្រាស់កក់សណ្ឋាគារ ប្រព័ន្ធនឹងបង្កើតការកម្មង់ដោយផ្អែកលើតម្រូវការរបស់អ្នកប្រើប្រាស់ (ដូចជា ឈ្មោះសណ្ឋាគារ កាលបរិច្ឆេទចូលស្នាក់ ចំនួនមនុស្ស ជាដើម)",
        "preconditions": "អ្នកប្រើប្រាស់បានចូលគណនី និងផ្តល់នូវអត្តសញ្ញាណត្រឹមត្រូវ (user_id), អ្នកប្រើប្រាស់បានផ្តល់នូវឈ្មោះសណ្ឋាគារត្រឹមត្រូវ (hotel_name) និងប្រភេទបន្ទប់ (room_type), ប្រព័ន្ធមានព័ត៌មានអំពីសណ្ឋាគារគោលដៅ ហើយសណ្ឋាគារនោះមានបន្ទប់ទំនេរនៅកាលបរិច្ឆេទដែលបានស្នើសុំ",
        "postconditions": "បង្កើតការកម្មង់ ហើយសូមអ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់",
        "args": {
            "hotel_id": "អត្តសញ្ញាណសណ្ឋាគារ",
            "room_id": "អត្តសញ្ញាណបន្ទប់",
            "user_id": "អត្តសញ្ញាណអ្នកប្រើប្រាស់"
        },
        "returns": "លទ្ធផលត្រឡប់មកវិញនៃប្រតិបត្តិការបង្កើតការកម្មង់",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "អ្នកប្រើប្រាស់ទិញសំបុត្រចូលទស្សនាដោយផ្អែកលើកន្លែងទស្សនា និងកាលបរិច្ឆេទ ប្រព័ន្ធបានត្រឡប់មកវិញនូវព័ត៌មានពាក់ព័ន្ធនឹងសំបុត្រ និងអនុវត្តការបញ្ជាទិញ",
        "preconditions": "នៅក្នុងស្ថានភាពទេសចរណ៍កន្លែងទស្សនា អ្នកប្រើប្រាស់ស្នើសុំកក់កន្លែងទស្សនា ដោយបានផ្តល់ព័ត៌មានចាំបាច់ពាក់ព័ន្ធនឹងការកក់",
        "postconditions": "បង្កើតបញ្ជាទិញ សូមអ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់",
        "args": {
            "attraction_id": "អត្តសញ្ញាណកន្លែងទស្សនា",
            "ticket_id": "អត្តសញ្ញាណសំបុត្រ",
            "user_id": "អត្តសញ្ញាណអ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទទស្សនា ទម្រង់ %Y-%m-%d",
            "quantity": "ចំនួន"
        },
        "returns": "លទ្ធផលត្រឡប់មកវិញនៃប្រតិបត្តិការបង្កើតបញ្ជាទិញ",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "អ្នកប្រើប្រាស់ទិញសំបុត្រយន្តហោះដោយផ្អែកលើលេខជើងហោះហើរ កាលបរិច្ឆេទ ប្រភេទកៅអី និងចំនួន ប្រព័ន្ធនឹងត្រឡប់មកវិញនូវព័ត៌មានពាក់ព័ន្ធនឹងសំបុត្រយន្តហោះ និងអនុវត្តការកម្មង់",
        "preconditions": "នៅក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្រយន្តហោះ អ្នកប្រើប្រាស់ស្នើសុំកក់ជើងហោះហើរ ដោយបានផ្តល់ព័ត៌មានចាំបាច់ពាក់ព័ន្ធនឹងការកក់",
        "postconditions": "បង្កើតការកម្មង់ សូមអ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់",
        "args": {
            "flight_id": "លេខសម្គាល់ជើងហោះហើរ",
            "seat_id": "លេខសម្គាល់កៅអី",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេធ្វើដំណើរ",
            "quantity": "ចំនួន"
        },
        "returns": "លទ្ធផលត្រឡប់មកវិញនៃប្រតិបត្តិការបង្កើតការកម្មង់",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "អ្នកប្រើប្រាស់ទិញសំបុត្ររថភ្លើងតាមរយៈលេខរថភ្លើង កាលបរិច្ឆេទ ប្រភេទកៅអី និងចំនួន ប្រព័ន្ធនឹងផ្តល់ព័ត៌មានពាក់ព័ន្ធនឹងសំបុត្ររថភ្លើង និងអនុវត្តការបញ្ជាទិញ",
        "preconditions": "ក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្ររថភ្លើង អ្នកប្រើប្រាស់ស្នើសុំកក់រថភ្លើង ដោយបានផ្តល់ព័ត៌មានចាំបាច់សម្រាប់ការកក់",
        "postconditions": "បង្កើតការបញ្ជាទិញ សូមអ្នកប្រើប្រាស់បញ្ជាក់ការទូទាត់",
        "args": {
            "train_id": "លេខសម្គាល់រថភ្លើង",
            "seat_id": "លេខសម្គាល់កៅអី",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទចេញដំណើរ",
            "quantity": "ចំនួន"
        },
        "returns": "លទ្ធផលត្រឡប់មកវិញនៃប្រតិបត្តិការបង្កើតការបញ្ជាទិញ",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "អ្នកប្រើប្រាស់ធ្វើការទូទាត់កម្មង់សណ្ឋាគារ",
        "preconditions": "ក្នុងស្ថានភាពស្វែងរក និងកក់សណ្ឋាគារ អ្នកប្រើប្រាស់ស្នើសុំទូទាត់កម្មង់សណ្ឋាគារ ដោយលេខសម្គាល់កម្មង់ត្រូវបានកំណត់រួចហើយនៅក្នុងបរិបទមុន",
        "postconditions": "បញ្ជាក់ការទូទាត់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពកម្មង់ជាបានទូទាត់ហើយ",
        "args": {
            "order_id": "លេខសម្គាល់កម្មង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "អ្នកប្រើប្រាស់ធ្វើការទូទាត់លើការកម្មង់សំបុត្រចូលទស្សនា",
        "preconditions": "នៅក្នុងបរិបទទេសចរណ៍កន្លែងទស្សនា អ្នកប្រើប្រាស់ស្នើសុំទូទាត់ប្រាក់សម្រាប់ការកម្មង់សំបុត្រចូលទស្សនា ដោយលេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់រួចហើយនៅខាងលើ",
        "postconditions": "បញ្ជាក់ការទូទាត់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកម្មង់ទៅជាបានទូទាត់",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "អ្នកប្រើប្រាស់ធ្វើការទូទាត់សម្រាប់ការកម្មង់ក្បួនយន្តហោះ",
        "preconditions": "ក្នុងបរិបទនៃការស្វែងរក និងទិញក្បួនយន្តហោះ អ្នកប្រើប្រាស់ស្នើសុំទូទាត់ប្រាក់សម្រាប់ការកម្មង់ជើងហោះហើរ ដោយលេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់រួចហើយនៅក្នុងបរិបទមុន",
        "postconditions": "បញ្ជាក់ការទូទាត់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកម្មង់ទៅជាបានទូទាត់រួច",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "អ្នកប្រើប្រាស់ធ្វើការទូទាត់ការកម្មង់សំបុត្ររថភ្លើង",
        "preconditions": "ក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្ររថភ្លើង អ្នកប្រើប្រាស់ស្នើសុំទូទាត់ប្រាក់សម្រាប់ការកម្មង់សំបុត្ររថភ្លើង ដោយលេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់រួចហើយនៅខាងលើ",
        "postconditions": "បញ្ជាក់ការទូទាត់ប្រាក់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកម្មង់ជាបានទូទាត់ហើយ",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានលទ្ធផលការទូទាត់ប្រាក់",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "ផ្អែកលើលេខសម្គាល់អ្នកប្រើប្រាស់ ស្វែងរកការកក់សណ្ឋាគាររបស់អ្នកប្រើប្រាស់ ដោយត្រឡប់មកវិញនូវលេខសម្គាល់ការកក់ ប្រភេទការកក់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់សណ្ឋាគារ តម្លៃសរុបការកក់ ពេលវេលាកក់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព និងស្ថានភាពការកក់",
        "preconditions": "តម្រូវការរបស់អ្នកប្រើប្រាស់គឺស្វែងរកការកក់សណ្ឋាគារ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានការកក់ ដើម្បីងាយស្រួលក្នុងការកែប្រែ ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទ",
            "status": "ស្ថានភាពការកក់"
        },
        "returns": "ព័ត៌មានការកក់សណ្ឋាគាររបស់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "ផ្អែកលើអត្តសញ្ញាណអ្នកប្រើប្រាស់ ស្វែងរកការកម្មង់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍របស់អ្នកប្រើប្រាស់ ដោយត្រឡប់មកវិញនូវអត្តសញ្ញាណការកម្មង់ ប្រភេទការកម្មង់ អត្តសញ្ញាណអ្នកប្រើប្រាស់ អត្តសញ្ញាណកន្លែងទេសចរណ៍ តម្លៃសរុបការកម្មង់ ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព និងស្ថានភាពការកម្មង់",
        "preconditions": "តម្រូវការរបស់អ្នកប្រើប្រាស់គឺស្វែងរកការកម្មង់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានការកម្មង់ ដើម្បីងាយស្រួលក្នុងការកែសម្រួល ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "អត្តសញ្ញាណអ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទ",
            "status": "ស្ថានភាពការកម្មង់"
        },
        "returns": "ព័ត៌មានការកម្មង់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍សម្រាប់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "ផ្អែកលើលេខសម្គាល់អ្នកប្រើប្រាស់ ស្វែងរកកំម្មង់ជើងហោះហើររបស់អ្នកប្រើប្រាស់ ដោយត្រឡប់មកវិញនូវលេខសម្គាល់កំម្មង់ ប្រភេទកំម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់ជើងហោះហើរ តម្លៃសរុបកំម្មង់ ពេលវេលាកំម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព និងស្ថានភាពកំម្មង់",
        "preconditions": "តម្រូវការរបស់អ្នកប្រើប្រាស់គឺស្វែងរកកំម្មង់ជើងហោះហើរ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានកំម្មង់ ដើម្បីងាយស្រួលក្នុងការកែសម្រួល ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទ",
            "status": "ស្ថានភាពកំម្មង់"
        },
        "returns": "ព័ត៌មានកំម្មង់ជើងហោះហើររបស់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "ផ្អែកលើលេខសម្គាល់អ្នកប្រើប្រាស់ ស្វែងរកការកម្មង់សំបុត្ររថភ្លើងរបស់អ្នកប្រើប្រាស់ ដោយត្រឡប់មកវិញនូវលេខសម្គាល់ការកម្មង់ ប្រភេទការកម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់រថភ្លើង តម្លៃសរុបការកម្មង់ ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព និងស្ថានភាពការកម្មង់",
        "preconditions": "តម្រូវការរបស់អ្នកប្រើប្រាស់គឺស្វែងរកការកម្មង់សំបុត្ររថភ្លើង",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានការកម្មង់ ដើម្បីងាយស្រួលក្នុងការកែសម្រួល ឬលុបចោលនៅពេលក្រោយ",
        "args": {
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "date": "កាលបរិច្ឆេទ",
            "status": "ស្ថានភាពការកម្មង់"
        },
        "returns": "ព័ត៌មានការកម្មង់សំបុត្ររថភ្លើងសម្រាប់អ្នកប្រើប្រាស់ដែលបានកំណត់",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ទទួលបានព័ត៌មានលម្អិតនៃការកក់សណ្ឋាគារ រួមមានលេខសម្គាល់ការកក់ ប្រភេទការកក់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់សណ្ឋាគារ តម្លៃសរុបការកក់ ពេលវេលាកក់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកក់ និងព័ត៌មានលម្អិតនៃបន្ទប់កក់ (ប្រភេទបន្ទប់ កាលបរិច្ឆេទចូលស្នាក់ តម្លៃ លេខសម្គាល់បន្ទប់)",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំទទួលបានព័ត៌មានលម្អិតនៃការកក់សណ្ឋាគារ លេខសម្គាល់ការកក់ត្រូវបានកំណត់រួចហើយនៅក្នុងបរិបទខាងលើ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកក់",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការកក់",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "ទទួលបានព័ត៌មានលម្អិតនៃការកម្មង់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍ រួមមានលេខសម្គាល់ការកម្មង់ ប្រភេទការកម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់កន្លែងទេសចរណ៍ តម្លៃសរុបការកម្មង់ ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកម្មង់ និងព័ត៌មានលម្អិតអំពីកន្លែងទេសចរណ៍នៃការកម្មង់ (ប្រភេទសំបុត្រ កាលបរិច្ឆេទ តម្លៃ លេខសម្គាល់សំបុត្រ)",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំទទួលបានព័ត៌មានលម្អិតនៃការកម្មង់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍ លេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់រួចហើយនៅក្នុងបរិបទខាងលើ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតការកម្មង់",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានលម្អិតការកម្មង់",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "ទទួលបានព័ត៌មានលម្អិតនៃការកក់សំបុត្រយន្តហោះ រួមមានលេខសម្គាល់ការកក់ ប្រភេទការកក់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់ជើងហោះហើរ តម្លៃសរុបនៃការកក់ ពេលវេលាកក់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកក់ និងព័ត៌មានលម្អិតនៃសំបុត្រយន្តហោះក្នុងការកក់ (ប្រភេទកៅអី កាលបរិច្ឆេទ តម្លៃ លេខសម្គាល់កៅអី)",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំទទួលបានព័ត៌មានលម្អិតនៃការកក់សំបុត្រយន្តហោះ លេខសម្គាល់ការកក់ត្រូវបានកំណត់នៅក្នុងបរិបទខាងលើ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកក់",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការកក់",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ទទួលបានព័ត៌មានលម្អិតនៃការកម្មង់សំបុត្ររថភ្លើង រួមមានលេខសម្គាល់ការកម្មង់ ប្រភេទការកម្មង់ លេខសម្គាល់អ្នកប្រើប្រាស់ លេខសម្គាល់រថភ្លើង តម្លៃសរុបនៃការកម្មង់ ពេលវេលាកម្មង់ ពេលវេលាធ្វើបច្ចុប្បន្នភាព ស្ថានភាពការកម្មង់ និងព័ត៌មានលម្អិតនៃសំបុត្ររថភ្លើងនៃការកម្មង់ (ប្រភេទកៅអី កាលបរិច្ឆេទ តម្លៃ លេខសម្គាល់កៅអី)",
        "preconditions": "អ្នកប្រើប្រាស់ស្នើសុំទទួលបានព័ត៌មានលម្អិតនៃការកម្មង់សំបុត្ររថភ្លើង លេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់នៅក្នុងបរិបទខាងលើ",
        "postconditions": "ត្រឡប់មកវិញនូវព័ត៌មានលម្អិតនៃការកម្មង់",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់"
        },
        "returns": "ព័ត៌មានលម្អិតនៃការកម្មង់",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "កែប្រែការកម្មង់សំបុត្ររថភ្លើង គាំទ្រការផ្លាស់ប្តូរកាលបរិច្ឆេទចេញដំណើរ ដោះស្រាយដោយស្វ័យប្រវត្តិនូវការបង់ប្រាក់បន្ថែម ឬសងប្រាក់វិញ។",
        "preconditions": "នៅក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្ររថភ្លើង អ្នកប្រើប្រាស់ស្នើសុំកែប្រែការកម្មង់សំបុត្ររថភ្លើង លេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់នៅក្នុងបរិបទមុន។",
        "postconditions": "កែប្រែការកម្មង់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកម្មង់ ប្រសិនបើត្រូវបង់ប្រាក់បន្ថែម ស្ថានភាពការកម្មង់ផ្លាស់ប្តូរទៅជា unpaid ផ្ទុយទៅវិញរក្សាស្ថានភាពដើម ប្រសិនបើត្រូវបង់ប្រាក់បន្ថែម ត្រូវណែនាំអ្នកប្រើប្រាស់ឱ្យទូទាត់ការកម្មង់នេះ។",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "new_date": "កាលបរិច្ឆេទចេញដំណើរថ្មី ទម្រង់ %Y-%m-%d"
        },
        "returns": "(មាតិកាការកម្មង់ដែលបានកែប្រែ ចំនួនទឹកប្រាក់ផ្លាស់ប្តូរ វិជ្ជមានមានន័យថាត្រូវបង់ប្រាក់បន្ថែម អវិជ្ជមានមានន័យថាសងប្រាក់វិញ)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "កែប្រែការកម្មង់សំបុត្រយន្តហោះ គាំទ្រការផ្លាស់ប្តូរកាលបរិច្ឆេទចេញដំណើរ ដោះស្រាយដោយស្វ័យប្រវត្តិនូវការបង់ប្រាក់បន្ថែម ឬសងប្រាក់វិញ។",
        "preconditions": "ក្នុងស្ថានភាពស្វែងរក និងទិញសំបុត្រយន្តហោះ អ្នកប្រើប្រាស់ស្នើសុំកែប្រែការកម្មង់សំបុត្រយន្តហោះ លេខសម្គាល់ការកម្មង់ត្រូវបានកំណត់នៅក្នុងបរិបទមុន",
        "postconditions": "កែប្រែការកម្មង់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកម្មង់ ប្រសិនបើត្រូវបង់ប្រាក់បន្ថែម ស្ថានភាពការកម្មង់ប្តូរទៅជា unpaid បើមិនដូច្នេះទេ រក្សាស្ថានភាពដើម ប្រសិនបើត្រូវបង់ប្រាក់បន្ថែម ត្រូវណែនាំអ្នកប្រើប្រាស់ឱ្យទូទាត់ការកម្មង់នេះ",
        "args": {
            "order_id": "លេខសម្គាល់ការកម្មង់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់",
            "new_date": "កាលបរិច្ឆេទចេញដំណើរថ្មី ទម្រង់ %Y-%m-%d"
        },
        "returns": "(មាតិកាការកម្មង់ដែលបានកែប្រែ ចំនួនទឹកប្រាក់ផ្លាស់ប្តូរ វិជ្ជមានមានន័យថាត្រូវបង់បន្ថែម អវិជ្ជមានមានន័យថាសងប្រាក់វិញ)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកក់សណ្ឋាគារដែលបានកក់រួច",
        "preconditions": "ក្នុងស្ថានភាពស្វែងរកការកក់សណ្ឋាគារ អ្នកប្រើប្រាស់ស្នើសុំលុបចោលការកក់សណ្ឋាគារ ហើយលេខសម្គាល់ការកក់ត្រូវបានកំណត់រួចហើយនៅក្នុងបរិបទមុន",
        "postconditions": "លុបចោលការកក់ និងធ្វើបច្ចុប្បន្នភាពស្ថានភាពការកក់ ប្រសិនបើចាំបាច់ត្រូវសងចំនួនទឹកប្រាក់វិញ គ្រាន់តែជូនដំណឹងដល់អ្នកប្រើប្រាស់",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ចំនួនទឹកប្រាក់សងវិញសម្រាប់ការលុបចោលការកក់",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកក់សំបុត្រចូលទស្សនាកន្លែងទេសចរណ៍ដែលបានកក់រួចហើយ",
        "preconditions": "មានលេខសម្គាល់ការកក់នៅក្នុងការសន្ទនាកន្លងមក ឬបានស្វែងរកព័ត៌មានការកក់រួចហើយ ហើយអ្នកប្រើប្រាស់មានសិទ្ធិលុបចោលការកក់នេះ",
        "postconditions": "ប្រសិនបើមានការសងប្រាក់ផ្នែកខ្លះ សូមជូនដំណឹងដល់អ្នកប្រើប្រាស់",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ចំនួនទឹកប្រាក់សងត្រឡប់មកវិញសម្រាប់ការលុបចោលការកក់",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកក់សំបុត្រយន្តហោះដែលបានកក់រួច",
        "preconditions": "មានលេខសម្គាល់ការកក់នៅក្នុងប្រវត្តិការសន្ទនា ឬបានស្វែងរកព័ត៌មានការកក់រួចហើយ ហើយអ្នកប្រើប្រាស់មានសិទ្ធិលុបចោលការកក់នេះ",
        "postconditions": "ប្រសិនបើមានការសងប្រាក់វិញ គ្រាន់តែជូនដំណឹងដល់អ្នកប្រើប្រាស់គឺបាន",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ចំនួនប្រាក់សងវិញសម្រាប់ការលុបចោលការកក់",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "អ្នកប្រើប្រាស់លុបចោលការកក់សំបុត្ររថភ្លើងដែលបានកក់រួច",
        "preconditions": "មានលេខសម្គាល់ការកក់នៅក្នុងប្រវត្តិការសន្ទនា ឬបានធ្វើការស្វែងរកការកក់រួចហើយ ហើយអ្នកប្រើប្រាស់មានសិទ្ធិលុបចោលការកក់នេះ",
        "postconditions": "ប្រសិនបើមានការសងចំណុះប្រាក់ គ្រាន់តែជូនដំណឹងដល់អ្នកប្រើប្រាស់",
        "args": {
            "order_id": "លេខសម្គាល់ការកក់",
            "user_id": "លេខសម្គាល់អ្នកប្រើប្រាស់"
        },
        "returns": "ចំនួនទឹកប្រាក់សងត្រឡប់មកវិញសម្រាប់ការលុបចោលការកក់",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Kazakh version
TOOL_DESCRIPTIONS_KK = {
    "get_ota_hotel_info": {
        "description": "Қонақүй туралы ақпаратты алу, оның ішінде қонақүй id, атауы, рейтингі, жұлдыздылығы, мекенжайы, тегтері және бөлме тізімі.",
        "preconditions": "Қонақүйді іздеу және брондау сценарийінде қонақүй туралы толық ақпаратты алу қажет.",
        "postconditions": "Қонақүй туралы толық ақпаратты қайтарады, пайдаланушыны бөлме таңдауға және тапсырыс беруге бағыттайды.",
        "args": {
            "hotel_id": "Қонақүй id"
        },
        "returns": "Қонақүй ақпараты",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Көрікті жер туралы ақпаратты алу, оның ішінде көрікті жердің id-сі, атауы, мекенжайы, сипаттамасы, рейтингі, жұмыс уақыты, билет бағасы, билет түрлерінің тізімі",
        "preconditions": "Көрікті жерлерге саяхаттау сценарийінде, көрікті жер туралы толық ақпаратты алу қажет",
        "postconditions": "Көрікті жер туралы толық ақпаратты қайтару, пайдаланушыны билет таңдауға және тапсырыс беруге бағыттау",
        "args": {
            "attraction_id": "Көрікті жердің id-сі"
        },
        "returns": "Көрікті жер туралы ақпарат",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Ұшу ақпаратын алу, оның ішінде: ұшу идентификаторы, ұшу нөмірі, шығу қаласы, келу қаласы, шығу әуежайының орналасқан жері, келу әуежайының орналасқан жері, шығу уақыты, келу уақыты, ұшу белгілері, орын түрлерінің тізімі",
        "preconditions": "Ұшу билеттерін іздеу және сатып алу сценарийінде ұшу туралы толық ақпаратты алу қажет",
        "postconditions": "Ұшу туралы толық ақпаратты қайтарады, пайдаланушыны орын таңдауға және тапсырыс беруге бағыттайды",
        "args": {
            "flight_id": "Ұшу идентификаторы"
        },
        "returns": "Ұшу ақпараты",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Поезд туралы ақпаратты алу, оның ішінде поезд идентификаторы, рейс нөмірі, шығу қаласы, келу қаласы, шығу станциясының орны, келу станциясының орны, шығу уақыты, келу уақыты, поезд белгілері, орын түрлерінің тізімі қамтылады.",
        "preconditions": "Поезд билеттерін іздеу және сатып алу сценарийінде поезд туралы толық ақпаратты алу қажет.",
        "postconditions": "Поезд туралы толық ақпаратты қайтару, пайдаланушыны орын таңдауға және тапсырыс беруге бағыттау.",
        "args": {
            "train_id": "Поезд идентификаторы"
        },
        "returns": "Поезд ақпараты",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Саяхат және қонақүй саласында пайдаланушының орналасу қажеттіліктері мен таңдауларына негізделіп, қолайлы қонақүй нұсқаларын ұсыну, қонақүй id-сы, атауы, рейтингі, жұлдыздылығы, мекенжайы, тегтері қамтылған негізгі ақпаратты қамтамасыз ету.",
        "preconditions": "Пайдаланушы қонақүй брондауды сұрайды, қонақүйге қатысты кілт сөздерді немесе орынды көрсетеді.",
        "postconditions": "Шарттарға сәйкес келетін қонақүйлер тізімін қайтару, егер қонақүй туралы толық ақпаратты (бөлме тізімі, бағасы және т.б.) көру қажет болса, қонақүй туралы ақпаратты сұрау құралын қолдану керек, пайдаланушыны қонақүй таңдауға бағыттау.",
        "args": {
            "city_name": "Қала атауы",
            "key_words": "Іздеу кілт сөздері (қонақүй атауы, сипаттамасы және т.б. сәйкестендіру)"
        },
        "returns": "Қонақүйдің негізгі ақпаратын құрылымдық түрде ұсыну",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Пайдаланушының орналасу қажеттіліктері мен қалауларына негізделіп, қолайлы көрікті жерлерді ұсыну, көрікті жерлердің негізгі ақпаратын қамтамасыз ету, оған көрікті жердің id-і, атауы, мекенжайы, сипаттамасы, рейтингі, жұмыс уақыты кіреді",
        "preconditions": "Пайдаланушы көрікті жерді брондауды сұрайды, көрікті жерге қатысты кілт сөздерді немесе орынды көрсетеді",
        "postconditions": "Шарттарға сәйкес келетін көрікті жерлер тізімін қайтарады, егер көрікті жердің толық ақпаратын (билеттер тізімі, бағалар және т.б.) көру қажет болса, көрікті жер ақпаратын сұрау құралын қолдану қажет, пайдаланушыны көрікті жерді таңдауға бағыттау",
        "args": {
            "city_name": "Қала атауы",
            "key_words": "Іздеу кілт сөздері (көрікті жердің атауы, орналасуы, мекенжайы, ерекшеліктері және т.б. сәйкестендіру)"
        },
        "returns": "Көрікті жерлердің негізгі ақпаратын құрылымдалған түрде қайтару",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Пайдаланушының орналасу қажеттіліктері мен қалауларына негізделіп, қолайлы ұшу нұсқаларын ұсынады, ұшу туралы негізгі ақпаратты береді, оған ұшу идентификаторы, ұшу нөмірі, шығу қаласы, келу қаласы, шығу әуежайының орны, келу әуежайының орны, шығу уақыты, келу уақыты, ұшу белгілері кіреді",
        "preconditions": "Пайдаланушы ұшу билетін брондауды сұрайды және ұшуға қатысты кілт сөздерді немесе орындарды ұсынады",
        "postconditions": "Шарттарға сай келетін ұшу тізімін қайтарады, егер ұшу туралы толық ақпаратты (орын түрлерінің тізімі, баға, күні және т.б.) көру қажет болса, ұшу мәліметтерін сұрау құралын қолдану керек, пайдаланушыны ұшуды таңдауға бағыттау",
        "args": {
            "departure": "Шығу қаласы",
            "destination": "Бару қаласы"
        },
        "returns": "Ұшу туралы негізгі ақпаратты құрылымдық түрде шығару",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Пайдаланушының локацияға қатысты қажеттіліктері мен таңдауларына негізделіп, қолайлы пойыз нұсқаларын ұсынады және пойыз билетінің негізгі ақпаратын қамтамасыз етеді, оған пойыз ID-сы, рейс нөмірі, шығу қаласы, келу қаласы, шығу стансасының орналасуы, келу стансасының орналасуы, шығу уақыты, келу уақыты, пойыз белгілері кіреді.",
        "preconditions": "Пайдаланушы пойызға тапсырыс беруді сұрайды және пойызға қатысты кілт сөздер немесе локацияларды көрсетеді.",
        "postconditions": "Шарттарға сәйкес келетін пойыз билеттерінің тізімін қайтарады; егер пойыз билетінің толық ақпаратын (орын түрлерінің тізімі, бағасы, күні және т.б.) көру қажет болса, пойыз билетінің мәліметтерін сұрау құралын қолдану керек, пайдаланушыны пойыз билетін таңдауға бағыттау.",
        "args": {
            "departure": "Шығу қаласы",
            "destination": "Келу қаласы",
            "date": "Шығу күні"
        },
        "returns": "Пойыздың негізгі ақпаратын құрылымдық түрде шығарады.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Пайдаланушы қонақүй брондаған кезде, жүйе пайдаланушының сұранысына (мысалы, қонақүй атауы, тұру күні, адам саны және т.б.) сәйкес тапсырыс жасайды.",
        "preconditions": "Пайдаланушы жүйеге кіріп, жарамды сәйкестендірушіні (user_id) ұсынды, пайдаланушы жарамды қонақүй атауын (hotel_name) және бөлме түрін (room_type) ұсынды, жүйеде мақсатты қонақүй туралы ақпарат бар және сол қонақүйде сұралған күндері бос бөлмелер бар.",
        "postconditions": "Тапсырыс жасалды, пайдаланушыдан төлемді растауды сұрау.",
        "args": {
            "hotel_id": "Қонақүй ID",
            "room_id": "Бөлме ID",
            "user_id": "Пайдаланушы ID"
        },
        "returns": "Тапсырыс жасау операциясының кері байланыс шығысы.",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Пайдаланушы аттракцион мен күнге қарай билет сатып алады, жүйе билет туралы ақпаратты қайтарып, тапсырыс береді.",
        "preconditions": "Аттракцион туризм сценарийінде, пайдаланушы аттракционды брондауды сұрайды және брондауға қажетті ақпаратты ұсынады.",
        "postconditions": "Тапсырыс жасалады, пайдаланушыдан төлемді растау сұралады.",
        "args": {
            "attraction_id": "Аттракцион ID-сы",
            "ticket_id": "Билет ID-сы",
            "user_id": "Пайдаланушы ID-сы",
            "date": "Келу күні, пішімі %Y-%m-%d",
            "quantity": "Саны"
        },
        "returns": "Тапсырыс жасау операциясының кері байланыс шығысы",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Пайдаланушы рейс нөмірі, күні, орын түрі және саны бойынша авиабилет сатып алады, жүйе билет туралы ақпаратты қайтарып, тапсырыс береді",
        "preconditions": "Авиабилетті іздеу және сатып алу сценарийінде пайдаланушы рейсті брондауды сұрайды және брондауға қажетті ақпаратты ұсынады",
        "postconditions": "Тапсырыс жасалады, пайдаланушыдан төлемді растау сұралады",
        "args": {
            "flight_id": "Рейс ID-сы",
            "seat_id": "Орын ID-сы",
            "user_id": "Пайдаланушы ID-сы",
            "date": "Ұшу күні",
            "quantity": "Саны"
        },
        "returns": "Тапсырыс құру операциясының кері байланыс шығысы",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Пайдаланушы пойыз нөмірі, күні, орын түрі және саны бойынша пойыз билетін сатып алады, жүйе пойыз билеті туралы ақпаратты қайтарып, тапсырысты жасайды",
        "preconditions": "Пойыз билетін іздеу және сатып алу сценарийінде пайдаланушы пойызға тапсырыс беруді сұрайды және тапсырыс беру үшін қажетті ақпаратты ұсынады",
        "postconditions": "Тапсырыс жасалады, пайдаланушыдан төлемді растау сұралады",
        "args": {
            "train_id": "Пойыз идентификаторы",
            "seat_id": "Орын идентификаторы",
            "user_id": "Пайдаланушы идентификаторы",
            "date": "Жөнелту күні",
            "quantity": "Саны"
        },
        "returns": "Тапсырыс жасау операциясының кері байланыс шығысы",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Пайдаланушы қонақүй тапсырысын төлейді",
        "preconditions": "Қонақүйді іздеу және брондау сценарийінде пайдаланушы тапсырысты төлеуді сұрайды, алдыңғы контексте тапсырыс ID анықталған",
        "postconditions": "Төлем расталады және тапсырыс мәртебесі «төленді» деп жаңартылады",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Пайдаланушы билет тапсырысын төлейді",
        "preconditions": "Туристік көрікті жерлер сценарийінде пайдаланушы билет тапсырысын төлеуді сұрайды, тапсырыс ID алдыңғы мәтінде анықталған",
        "postconditions": "Төлемді растау және тапсырыс статусын төленген деп жаңарту",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Пайдаланушы авиабилет тапсырысын төлейді",
        "preconditions": "Авиабилетті іздеу және сатып алу сценарийінде пайдаланушы ұшу тапсырысын төлеуді сұрайды, алдыңғы мәтінде тапсырыс ID анықталған",
        "postconditions": "Төлем расталып, тапсырыс статусы 'төленген' деп жаңартылады",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Пайдаланушы пойыз билеті тапсырысын төлейді",
        "preconditions": "Пойыз билетін іздеу және сатып алу сценарийінде пайдаланушы пойыз билеті тапсырысын төлеуді сұрайды, алдыңғы мәтінде тапсырыс ID анықталған",
        "postconditions": "Төлем расталып, тапсырыс статусы төленген болып жаңартылады",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Төлем нәтижесі туралы ақпарат",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Пайдаланушы ID бойынша пайдаланушының қонақүй тапсырыстарын іздеу, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, қонақүй ID, тапсырыстың жалпы құны, тапсырыс уақыты, жаңарту уақыты және тапсырыс статусы қамтылған нәтижені қайтару",
        "preconditions": "Пайдаланушының қажеттілігі қонақүй тапсырыстарын іздеу",
        "postconditions": "Тапсырыс ақпаратын қайтару, кейінірек өзгерту/болдырмау үшін ыңғайлы",
        "args": {
            "user_id": "Пайдаланушы ID",
            "date": "Күні",
            "status": "Тапсырыс статусы"
        },
        "returns": "Көрсетілген пайдаланушының қонақүй тапсырысының ақпараты",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Пайдаланушы ID бойынша пайдаланушының көрнекті жерлерге билет тапсырыстарын іздеу, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, көрнекті жер ID, тапсырыстың жалпы құны, тапсырыс берілген уақыт, жаңартылған уақыт және тапсырыс мәртебесін қамтитын нәтиже қайтару",
        "preconditions": "Пайдаланушының көрнекті жерлерге билет тапсырыстарын іздеу қажеттілігі",
        "postconditions": "Тапсырыс ақпаратын қайтару, кейіннен өзгерту немесе болдырмау үшін ыңғайлы",
        "args": {
            "user_id": "Пайдаланушы ID",
            "date": "Күні",
            "status": "Тапсырыс мәртебесі"
        },
        "returns": "Көрсетілген пайдаланушының көрнекті жерлерге билет тапсырыстары туралы ақпарат",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Пайдаланушы ID бойынша пайдаланушының авиабилет тапсырысын іздеу, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, рейс ID, тапсырыстың жалпы құны, тапсырыс жасау уақыты, жаңарту уақыты және тапсырыс мәртебесін қамтитын нәтиже қайтару",
        "preconditions": "Пайдаланушының қажеттілігі авиабилет тапсырысын іздеу",
        "postconditions": "Тапсырыс ақпаратын қайтару, кейінірек өзгерту немесе болдырмау үшін ыңғайлы",
        "args": {
            "user_id": "Пайдаланушы ID",
            "date": "Күні",
            "status": "Тапсырыс мәртебесі"
        },
        "returns": "Көрсетілген пайдаланушының авиабилет тапсырысының ақпараты",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Пайдаланушы ID бойынша пайдаланушының пойыз билеті тапсырыстарын сұрау, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, пойыз ID, тапсырыстың жалпы құны, тапсырыс уақыты, жаңарту уақыты және тапсырыс статусы қамтылған нәтижені қайтару",
        "preconditions": "Пайдаланушының қажеттілігі пойыз билеті тапсырыстарын сұрау",
        "postconditions": "Тапсырыс ақпаратын қайтару, кейінірек өзгерту/болдырмау үшін ыңғайлы",
        "args": {
            "user_id": "Пайдаланушы ID",
            "date": "Күні",
            "status": "Тапсырыс статусы"
        },
        "returns": "Көрсетілген пайдаланушының пойыз билеті тапсырысының ақпараты",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Қонақүй тапсырысының толық ақпаратын алу, оған тапсырыс ID, тапсырыс түрі, пайдаланушы ID, қонақүй ID, тапсырыстың жалпы құны, тапсырыс берілген уақыт, жаңарту уақыты, тапсырыс күйі және тапсырыс бөлмесінің толық ақпараты (бөлме түрі, орналасу күні, бағасы, бөлме ID) кіреді",
        "preconditions": "Пайдаланушы қонақүй тапсырысының толық ақпаратын сұрайды, жоғарыда тапсырыс ID анықталған",
        "postconditions": "Тапсырыс толық ақпараты қайтарылады",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Тапсырыс толық ақпараты",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Көрікті жерлерге арналған билет тапсырысының мәліметтерін алу. Құрамында тапсырыс ID, тапсырыс түрі, пайдаланушы ID, көрікті жер ID, тапсырыстың жалпы құны, тапсырыс беру уақыты, жаңарту уақыты, тапсырыс мәртебесі және тапсырыс бойынша көрікті жердің толық мәліметтері (билет түрі, күні, бағасы, билет ID) бар.",
        "preconditions": "Пайдаланушы көрікті жерлерге арналған билет тапсырысының мәліметтерін сұрайды, жоғарыда тапсырыс ID анықталған.",
        "postconditions": "Тапсырыс мәліметтері қайтарылады.",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Тапсырыс мәліметтері",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Ұшу билеті тапсырысының мәліметтерін алу, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, рейс ID, тапсырыстың жалпы құны, тапсырыс уақыты, жаңарту уақыты, тапсырыс мәртебесі және тапсырыс билетінің толық ақпаратын (орын түрі, күні, бағасы, орын ID) қамтиды",
        "preconditions": "Пайдаланушы ұшу билеті тапсырысының мәліметтерін алуды сұрайды, жоғарыда тапсырыс ID анықталған",
        "postconditions": "Тапсырыс мәліметтерін қайтару",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Тапсырыс мәліметтері",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Пойыз билеті тапсырысының мәліметтерін алу, тапсырыс ID, тапсырыс түрі, пайдаланушы ID, пойыз ID, тапсырыстың жалпы құны, тапсырыс жасалған уақыт, жаңартылған уақыт, тапсырыс күйі және тапсырыстағы пойыз билетінің толық ақпаратын (орын түрі, күні, бағасы, орын ID) қамтиды",
        "preconditions": "Пайдаланушы пойыз билеті тапсырысының ақпаратын сұрайды, жоғарыда тапсырыс ID анықталған",
        "postconditions": "Тапсырыс ақпаратын қайтару",
        "args": {
            "order_id": "Тапсырыс ID"
        },
        "returns": "Тапсырыс ақпараты",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Теміржол билеті тапсырысын өзгерту, шығу күнін өзгертуді қолдайды, баға айырмашылығын төлеуді немесе қайтаруды автоматты түрде өңдейді.",
        "preconditions": "Теміржол билетін іздеу және сатып алу сценарийінде, пайдаланушы теміржол билеті тапсырысын өзгертуді сұрайды, алдыңғы мәтінде тапсырыс ID анықталған",
        "postconditions": "Тапсырысты өзгерту және тапсырыс күйін жаңарту, егер баға айырмашылығын төлеу қажет болса, тапсырыс күйі unpaid болып өзгереді, әйтпесе бастапқы күйін сақтайды, егер баға айырмашылығын төлеу қажет болса, пайдаланушыны осы тапсырысты төлеуге бағыттау қажет",
        "args": {
            "order_id": "Тапсырыс ID",
            "user_id": "Пайдаланушы ID",
            "new_date": "Жаңа шығу күні, пішімі %Y-%m-%d"
        },
        "returns": "(Өзгертілген тапсырыс мазмұны, баға айырмашылығы, оң мән айырмашылықты төлеуді білдіреді, теріс мән айырмашылықты қайтаруды білдіреді)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Ұшу билеті тапсырысын өзгерту, ұшу күнін өзгертуді қолдайды, баға айырмашылығын төлеу немесе қайтаруды автоматты түрде өңдейді.",
        "preconditions": "Ұшу билетін іздеу және сатып алу сценарийінде, пайдаланушы ұшу билеті тапсырысын өзгертуді сұрайды, жоғарыда тапсырыс ID анықталған",
        "postconditions": "Тапсырысты өзгерту және тапсырыс күйін жаңарту, егер баға айырмашылығын төлеу қажет болса, тапсырыс күйі unpaid деп өзгереді, әйтпесе бастапқы күйінде қалады, егер баға айырмашылығын төлеу қажет болса, пайдаланушыны осы тапсырысты төлеуге бағыттау қажет",
        "args": {
            "order_id": "Тапсырыс ID",
            "user_id": "Пайдаланушы ID",
            "new_date": "Жаңа ұшу күні, пішімі %Y-%m-%d"
        },
        "returns": "(Өзгертілген тапсырыс мазмұны, баға айырмашылығы, оң мән айырмашылықты төлеуді білдіреді, теріс мән айырмашылықты қайтаруды білдіреді)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Пайдаланушы брондалған қонақүй тапсырысын болдырмау",
        "preconditions": "Қонақүй брондау сценарийінде пайдаланушы қонақүй тапсырысын болдыруды сұрайды, алдыңғы мәтінде тапсырыс ID анықталған",
        "postconditions": "Тапсырысты болдыру және тапсырыс күйін жаңарту, егер баға айырмашылығын қайтару қажет болса, пайдаланушыға хабарлау жеткілікті",
        "args": {
            "order_id": "Тапсырыс ID",
            "user_id": "Пайдаланушы ID"
        },
        "returns": "Тапсырысты болдырудан қайтарым соммасы",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Пайдаланушы брондалған көрнекті орындарға арналған билет тапсырысын жою",
        "preconditions": "Алдыңғы сөйлесуде тапсырыс ID-сы бар немесе тапсырысты тексеру жүргізілген, пайдаланушының бұл тапсырысты жоюға рұқсаты бар",
        "postconditions": "Егер айырмашылық қайтарылса, пайдаланушыға хабарлау жеткілікті",
        "args": {
            "order_id": "Тапсырыс ID-сы",
            "user_id": "Пайдаланушы ID-сы"
        },
        "returns": "Тапсырысты жоюға байланысты қайтарылған қаражат мөлшері",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Пайдаланушы брондалған авиабилет тапсырысын жою",
        "preconditions": "Алдыңғы сөйлесуде тапсырыс ID бар немесе тапсырысты сұрау жүргізілген, пайдаланушының бұл тапсырысты жоюға құқығы бар",
        "postconditions": "Егер айырмашылық қайтарылса, пайдаланушыға хабарлау жеткілікті",
        "args": {
            "order_id": "Тапсырыс ID",
            "user_id": "Пайдаланушы ID"
        },
        "returns": "Тапсырысты жоюға арналған қайтарым сомасы",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Пайдаланушы брондалған пойыз билеті тапсырысын болдырмау",
        "preconditions": "Сөйлесу тарихында тапсырыс ID-сы бар немесе тапсырысты тексеру жүргізілген, пайдаланушының бұл тапсырысты болдырмауға құқығы бар",
        "postconditions": "Егер қайтарым айырмашылығы болса, пайдаланушыға хабарлау жеткілікті",
        "args": {
            "order_id": "Тапсырыс ID-сы",
            "user_id": "Пайдаланушы ID-сы"
        },
        "returns": "Тапсырысты болдырмаудан кейінгі қайтарым соммасы",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Punjabi version
TOOL_DESCRIPTIONS_PA = {
    "get_ota_hotel_info": {
        "description": "ਹੋਟਲ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਹੋਟਲ ਆਈਡੀ, ਨਾਮ, ਰੇਟਿੰਗ, ਸਟਾਰ, ਪਤਾ, ਟੈਗ, ਕਮਰਿਆਂ ਦੀ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਹੋਟਲ ਖੋਜ ਅਤੇ ਬੁਕਿੰਗ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਹੋਟਲ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਹੋਟਲ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਕਮਰਾ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਕਰਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "hotel_id": "ਹੋਟਲ ਆਈਡੀ"
        },
        "returns": "ਹੋਟਲ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "ਆਕਰਸ਼ਣ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਕਰਸ਼ਣ ਆਈਡੀ, ਨਾਮ, ਪਤਾ, ਵੇਰਵਾ, ਰੇਟਿੰਗ, ਖੁੱਲ੍ਹਣ ਦਾ ਸਮਾਂ, ਟਿਕਟ ਕੀਮਤ, ਟਿਕਟ ਕਿਸਮਾਂ ਦੀ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਆਕਰਸ਼ਣ ਸੈਰ-ਸਪਾਟੇ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਆਕਰਸ਼ਣ ਬਾਰੇ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਆਕਰਸ਼ਣ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਟਿਕਟਾਂ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਕਰਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "attraction_id": "ਆਕਰਸ਼ਣ ਆਈਡੀ"
        },
        "returns": "ਆਕਰਸ਼ਣ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "ਉਡਾਣ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਉਡਾਣ ਆਈਡੀ, ਉਡਾਣ ਨੰਬਰ, ਰਵਾਨਗੀ ਸ਼ਹਿਰ, ਆਗਮਨ ਸ਼ਹਿਰ, ਰਵਾਨਗੀ ਹਵਾਈ ਅੱਡੇ ਦੀ ਸਥਿਤੀ, ਆਗਮਨ ਹਵਾਈ ਅੱਡੇ ਦੀ ਸਥਿਤੀ, ਰਵਾਨਗੀ ਦਾ ਸਮਾਂ, ਆਗਮਨ ਦਾ ਸਮਾਂ, ਉਡਾਣ ਟੈਗ, ਸੀਟ ਦੀ ਕਿਸਮ ਦੀ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦਾਰੀ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਉਡਾਣ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਉਡਾਣ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਸੀਟ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਦੇਣ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "flight_id": "ਉਡਾਣ ਆਈਡੀ"
        },
        "returns": "ਉਡਾਣ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ਰੇਲ ਗੱਡੀ ਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਰੇਲ ਗੱਡੀ ਆਈਡੀ, ਟਰੇਨ ਨੰਬਰ, ਰਵਾਨਗੀ ਸ਼ਹਿਰ, ਪਹੁੰਚ ਸ਼ਹਿਰ, ਰਵਾਨਗੀ ਸਟੇਸ਼ਨ ਸਥਿਤੀ, ਪਹੁੰਚ ਸਟੇਸ਼ਨ ਸਥਿਤੀ, ਰਵਾਨਗੀ ਸਮਾਂ, ਪਹੁੰਚ ਸਮਾਂ, ਰੇਲ ਗੱਡੀ ਟੈਗ, ਸੀਟ ਦੀ ਕਿਸਮ ਦੀ ਸੂਚੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਰੇਲਵੇ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦਾਰੀ ਦੇ ਮਾਮਲੇ ਵਿੱਚ, ਰੇਲ ਗੱਡੀ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਲੋੜ ਹੈ।",
        "postconditions": "ਰੇਲ ਗੱਡੀ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਸੀਟ ਚੁਣਨ ਅਤੇ ਆਰਡਰ ਦੇਣ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "train_id": "ਰੇਲ ਗੱਡੀ ਆਈਡੀ"
        },
        "returns": "ਰੇਲ ਗੱਡੀ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "ਯਾਤਰਾ ਅਤੇ ਹੋਟਲ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਦੀ ਸਥਾਨ ਲੋੜ ਅਤੇ ਪਸੰਦ ਦੇ ਆਧਾਰ ਤੇ, ਢੁਕਵੇਂ ਹੋਟਲ ਵਿਕਲਪਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰੋ, ਹੋਟਲ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਹੋਟਲ ਆਈਡੀ, ਨਾਮ, ਰੇਟਿੰਗ, ਸਟਾਰ ਪੱਧਰ, ਪਤਾ ਅਤੇ ਟੈਗ ਸ਼ਾਮਲ ਹਨ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਹੋਟਲ ਬੁਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ ਅਤੇ ਹੋਟਲ ਨਾਲ ਸੰਬੰਧਿਤ ਕੀਵਰਡ ਜਾਂ ਸਥਾਨ ਦਿੰਦਾ ਹੈ।",
        "postconditions": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੇ ਹੋਟਲਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ। ਜੇਕਰ ਹੋਟਲ ਦੇ ਵੇਰਵੇ (ਕਮਰੇ ਦੀ ਸੂਚੀ, ਕੀਮਤ ਆਦਿ) ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਹੋਟਲ ਵੇਰਵਾ ਜਾਂਚ ਸਾਧਨ ਦੀ ਵਰਤੋਂ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ, ਅਤੇ ਉਪਭੋਗਤਾ ਨੂੰ ਹੋਟਲ ਚੁਣਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "city_name": "ਸ਼ਹਿਰ ਦਾ ਨਾਮ",
            "key_words": "ਖੋਜ ਕੀਵਰਡ (ਹੋਟਲ ਦੇ ਨਾਮ, ਹੋਟਲ ਪਰਿਚੈ ਆਦਿ ਨਾਲ ਮੇਲ ਖਾਂਦਾ ਹੈ)"
        },
        "returns": "ਹੋਟਲ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਦੀ ਢਾਂਚਾਗਤ ਆਉਟਪੁਟ",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਥਾਨ ਲੋੜਾਂ ਅਤੇ ਪਸੰਦਾਂ ਦੇ ਆਧਾਰ ਤੇ, ਢੁਕਵੇਂ ਸੈਲਾਨੀ ਸਥਾਨਾਂ ਦੇ ਵਿਕਲਪਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰੋ, ਸੈਲਾਨੀ ਸਥਾਨ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਸੈਲਾਨੀ ਸਥਾਨ ਆਈਡੀ, ਨਾਮ, ਪਤਾ, ਵੇਰਵਾ, ਰੇਟਿੰਗ, ਖੁੱਲ੍ਹਣ ਦੇ ਸਮੇਂ ਸ਼ਾਮਲ ਹਨ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਸੈਲਾਨੀ ਸਥਾਨ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਸੈਲਾਨੀ ਸਥਾਨ ਨਾਲ ਸਬੰਧਤ ਕੀਵਰਡ ਜਾਂ ਸਥਾਨ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।",
        "postconditions": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੇ ਸੈਲਾਨੀ ਸਥਾਨਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਜੇਕਰ ਸੈਲਾਨੀ ਸਥਾਨ ਦੇ ਵੇਰਵੇ (ਟਿਕਟ ਸੂਚੀ, ਕੀਮਤਾਂ ਆਦਿ) ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ ਤਾਂ ਸੈਲਾਨੀ ਸਥਾਨ ਵੇਰਵਾ ਖੋਜ ਸਾਧਨ ਦੀ ਵਰਤੋਂ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ, ਉਪਭੋਗਤਾ ਨੂੰ ਸੈਲਾਨੀ ਸਥਾਨ ਚੁਣਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "city_name": "ਸ਼ਹਿਰ ਦਾ ਨਾਮ",
            "key_words": "ਖੋਜ ਕੀਵਰਡ (ਸੈਲਾਨੀ ਸਥਾਨ ਦੇ ਨਾਮ, ਸਥਾਨ, ਪਤੇ, ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ ਆਦਿ ਨਾਲ ਮੇਲ ਖਾਂਦਾ ਹੈ)"
        },
        "returns": "ਸੈਲਾਨੀ ਸਥਾਨ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਦੀ ਸੰਰਚਿਤ ਆਉਟਪੁਟ",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਥਾਨ ਲੋੜਾਂ ਅਤੇ ਪਸੰਦਾਂ ਦੇ ਆਧਾਰ ਤੇ, ਢੁਕਵੇਂ ਉਡਾਣ ਵਿਕਲਪਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰੋ, ਉਡਾਣ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਉਡਾਣ ਆਈਡੀ, ਉਡਾਣ ਨੰਬਰ, ਰਵਾਨਗੀ ਸ਼ਹਿਰ, ਆਗਮਨ ਸ਼ਹਿਰ, ਰਵਾਨਗੀ ਹਵਾਈ ਅੱਡੇ ਦਾ ਸਥਾਨ, ਆਗਮਨ ਹਵਾਈ ਅੱਡੇ ਦਾ ਸਥਾਨ, ਰਵਾਨਗੀ ਦਾ ਸਮਾਂ, ਆਗਮਨ ਦਾ ਸਮਾਂ, ਉਡਾਣ ਟੈਗ ਸ਼ਾਮਲ ਹਨ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਉਡਾਣ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਉਡਾਣ ਨਾਲ ਸਬੰਧਤ ਕੀਵਰਡ ਜਾਂ ਸਥਾਨ ਦਿੰਦਾ ਹੈ।",
        "postconditions": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੀਆਂ ਉਡਾਣਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਜੇਕਰ ਉਡਾਣ ਦੇ ਵੇਰਵੇ (ਸੀਟ ਦੀ ਕਿਸਮ ਦੀ ਸੂਚੀ, ਕੀਮਤ, ਤਾਰੀਖ ਆਦਿ) ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ ਤਾਂ ਉਡਾਣ ਵੇਰਵਾ ਖੋਜ ਸਾਧਨ ਦੀ ਵਰਤੋਂ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ, ਉਪਭੋਗਤਾ ਨੂੰ ਉਡਾਣ ਚੁਣਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "departure": "ਰਵਾਨਗੀ ਸ਼ਹਿਰ",
            "destination": "ਮੰਜ਼ਿਲ ਸ਼ਹਿਰ"
        },
        "returns": "ਉਡਾਣ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਦਾ ਬਣਤਰੀ ਆਉਟਪੁੱਟ",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "ਉਪਭੋਗਤਾ ਦੀਆਂ ਸਥਾਨ ਲੋੜਾਂ ਅਤੇ ਪਸੰਦਾਂ ਦੇ ਆਧਾਰ 'ਤੇ, ਢੁਕਵੇਂ ਟਰੇਨ ਵਿਕਲਪਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰੋ, ਟਰੇਨ ਟਿਕਟਾਂ ਦੀ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਟਰੇਨ ਆਈਡੀ, ਟਰੇਨ ਨੰਬਰ, ਰਵਾਨਗੀ ਸ਼ਹਿਰ, ਆਗਮਨ ਸ਼ਹਿਰ, ਰਵਾਨਗੀ ਸਟੇਸ਼ਨ ਸਥਾਨ, ਆਗਮਨ ਸਟੇਸ਼ਨ ਸਥਾਨ, ਰਵਾਨਗੀ ਸਮਾਂ, ਆਗਮਨ ਸਮਾਂ, ਟਰੇਨ ਟੈਗ ਸ਼ਾਮਲ ਹਨ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਟਰੇਨ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਟਰੇਨ ਨਾਲ ਸਬੰਧਤ ਕੀਵਰਡ ਜਾਂ ਸਥਾਨ ਦਿੰਦਾ ਹੈ।",
        "postconditions": "ਸ਼ਰਤਾਂ ਨੂੰ ਪੂਰਾ ਕਰਨ ਵਾਲੀਆਂ ਟਰੇਨ ਟਿਕਟਾਂ ਦੀ ਸੂਚੀ ਵਾਪਸ ਕਰੋ, ਜੇਕਰ ਟਰੇਨ ਟਿਕਟ ਵਿਵਰਣ (ਸੀਟ ਦੀ ਕਿਸਮ ਦੀ ਸੂਚੀ, ਕੀਮਤ, ਤਾਰੀਖ ਆਦਿ) ਦੇਖਣ ਦੀ ਲੋੜ ਹੈ ਤਾਂ ਟਰੇਨ ਟਿਕਟ ਵਿਵਰਣ ਕੁਐਰੀ ਟੂਲ ਦੀ ਵਰਤੋਂ ਕਰਨੀ ਚਾਹੀਦੀ ਹੈ, ਉਪਭੋਗਤਾ ਨੂੰ ਟਰੇਨ ਟਿਕਟ ਚੁਣਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "departure": "ਰਵਾਨਗੀ ਸ਼ਹਿਰ",
            "destination": "ਮੰਜ਼ਿਲ ਸ਼ਹਿਰ",
            "date": "ਰਵਾਨਗੀ ਤਾਰੀਖ"
        },
        "returns": "ਟਰੇਨ ਬੁਨਿਆਦੀ ਜਾਣਕਾਰੀ ਦੀ ਢਾਂਚਾਗਤ ਆਉਟਪੁਟ",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "ਜਦੋਂ ਉਪਭੋਗਤਾ ਹੋਟਲ ਬੁੱਕ ਕਰਦਾ ਹੈ, ਤਾਂ ਸਿਸਟਮ ਉਪਭੋਗਤਾ ਦੀਆਂ ਲੋੜਾਂ (ਜਿਵੇਂ ਕਿ ਹੋਟਲ ਦਾ ਨਾਮ, ਚੈਕ-ਇਨ ਮਿਤੀ, ਲੋਕਾਂ ਦੀ ਗਿਣਤੀ, ਆਦਿ) ਦੇ ਅਧਾਰ ਤੇ ਆਰਡਰ ਤਿਆਰ ਕਰਦਾ ਹੈ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਲੌਗ ਇਨ ਹੈ ਅਤੇ ਇੱਕ ਵੈਧ ਪਛਾਣ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ (user_id), ਉਪਭੋਗਤਾ ਇੱਕ ਵੈਧ ਹੋਟਲ ਦਾ ਨਾਮ (hotel_name) ਅਤੇ ਕਮਰੇ ਦੀ ਕਿਸਮ (room_type) ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ, ਸਿਸਟਮ ਕੋਲ ਟਾਰਗੇਟ ਹੋਟਲ ਬਾਰੇ ਜਾਣਕਾਰੀ ਹੈ, ਅਤੇ ਉਸ ਹੋਟਲ ਕੋਲ ਮੰਗੀ ਗਈ ਮਿਤੀ ਤੇ ਕਮਰੇ ਉਪਲਬਧ ਹਨ।",
        "postconditions": "ਆਰਡਰ ਤਿਆਰ ਕਰੋ, ਉਪਭੋਗਤਾ ਨੂੰ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਕਹੋ।",
        "args": {
            "hotel_id": "ਹੋਟਲ ID",
            "room_id": "ਕਮਰਾ ID",
            "user_id": "ਉਪਭੋਗਤਾ ID"
        },
        "returns": "ਆਰਡਰ ਬਣਾਉਣ ਦੀ ਕਾਰਵਾਈ ਲਈ ਫੀਡਬੈਕ ਆਉਟਪੁੱਟ।",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਆਕਰਸ਼ਣ ਅਤੇ ਤਾਰੀਖ ਦੇ ਅਧਾਰ ਤੇ ਟਿਕਟਾਂ ਖਰੀਦਦੇ ਹਨ, ਸਿਸਟਮ ਟਿਕਟ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰਦਾ ਹੈ ਅਤੇ ਆਰਡਰ ਕਰਦਾ ਹੈ",
        "preconditions": "ਆਕਰਸ਼ਣ ਸੈਰ-ਸਪਾਟੇ ਦੇ ਸਥਿਤੀ ਵਿੱਚ, ਵਰਤੋਂਕਾਰ ਆਕਰਸ਼ਣ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਅਤੇ ਬੁਕਿੰਗ ਲਈ ਲੋੜੀਂਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ",
        "postconditions": "ਆਰਡਰ ਤਿਆਰ ਕਰੋ, ਵਰਤੋਂਕਾਰ ਨੂੰ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਕਹੋ",
        "args": {
            "attraction_id": "ਆਕਰਸ਼ਣ ID",
            "ticket_id": "ਟਿਕਟ ID",
            "user_id": "ਵਰਤੋਂਕਾਰ ID",
            "date": "ਦੌਰਾ ਕਰਨ ਦੀ ਤਾਰੀਖ, ਫਾਰਮੈਟ %Y-%m-%d ਹੈ",
            "quantity": "ਮਾਤਰਾ"
        },
        "returns": "ਆਰਡਰ ਬਣਾਉਣ ਦੀ ਕਾਰਵਾਈ ਦੀ ਪ੍ਰਤੀਕਿਰਿਆ ਆਉਟਪੁਟ",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "ਯੂਜ਼ਰ ਉਡਾਣ ਨੰਬਰ, ਤਾਰੀਖ, ਸੀਟ ਦੀ ਕਿਸਮ ਅਤੇ ਗਿਣਤੀ ਦੇ ਅਧਾਰ ਤੇ ਹਵਾਈ ਟਿਕਟ ਖਰੀਦਦੇ ਹਨ, ਸਿਸਟਮ ਟਿਕਟ ਦੀ ਸੰਬੰਧਿਤ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰਦਾ ਹੈ ਅਤੇ ਆਰਡਰ ਪ੍ਰੋਸੈਸ ਕਰਦਾ ਹੈ।",
        "preconditions": "ਹਵਾਈ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਯੂਜ਼ਰ ਉਡਾਣ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ ਅਤੇ ਬੁਕਿੰਗ ਲਈ ਜ਼ਰੂਰੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਤਿਆਰ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਯੂਜ਼ਰ ਨੂੰ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਕਿਹਾ ਜਾਂਦਾ ਹੈ।",
        "args": {
            "flight_id": "ਉਡਾਣ ID",
            "seat_id": "ਸੀਟ ID",
            "user_id": "ਯੂਜ਼ਰ ID",
            "date": "ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ",
            "quantity": "ਗਿਣਤੀ"
        },
        "returns": "ਆਰਡਰ ਬਣਾਉਣ ਦੀ ਕਾਰਵਾਈ ਦਾ ਫੀਡਬੈਕ ਆਉਟਪੁਟ",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਟਰੇਨ ਨੰਬਰ, ਤਾਰੀਖ, ਸੀਟ ਦੀ ਕਿਸਮ ਅਤੇ ਮਾਤਰਾ ਦੇ ਅਧਾਰ ਤੇ ਟਰੇਨ ਟਿਕਟ ਖਰੀਦਦੇ ਹਨ, ਸਿਸਟਮ ਟਰੇਨ ਟਿਕਟ ਦੀ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰਦਾ ਹੈ ਅਤੇ ਆਰਡਰ ਬਣਾਉਂਦਾ ਹੈ।",
        "preconditions": "ਟਰੇਨ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਵਰਤੋਂਕਾਰ ਟਰੇਨ ਬੁੱਕ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ ਅਤੇ ਬੁਕਿੰਗ ਲਈ ਲੋੜੀਂਦੀ ਜਾਣਕਾਰੀ ਪ੍ਰਦਾਨ ਕਰਦਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਤਿਆਰ ਕਰੋ, ਵਰਤੋਂਕਾਰ ਨੂੰ ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰਨ ਲਈ ਕਹੋ।",
        "args": {
            "train_id": "ਟਰੇਨ ਪਛਾਣ",
            "seat_id": "ਸੀਟ ਪਛਾਣ",
            "user_id": "ਵਰਤੋਂਕਾਰ ਪਛਾਣ",
            "date": "ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ",
            "quantity": "ਮਾਤਰਾ"
        },
        "returns": "ਆਰਡਰ ਬਣਾਉਣ ਦੀ ਕਾਰਵਾਈ ਦਾ ਫੀਡਬੈਕ ਆਉਟਪੁਟ",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "ਉਪਭੋਗਤਾ ਹੋਟਲ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਕਰਦਾ ਹੈ",
        "preconditions": "ਹੋਟਲ ਬੁਕਿੰਗ ਕੁਐਰੀ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਹੋਟਲ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕੀਤੀ ਗਈ ਹੈ",
        "postconditions": "ਅਦਾਇਗੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ ਅਤੇ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ ਅਦਾ ਕੀਤਾ ਗਿਆ ਵਿੱਚ ਅਪਡੇਟ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਅਦਾਇਗੀ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਟਿਕਟ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਕਰਦਾ ਹੈ",
        "preconditions": "ਸੈਰ-ਸਪਾਟਾ ਦ੍ਰਿਸ਼ ਵਿੱਚ, ਵਰਤੋਂਕਾਰ ਸੈਰ-ਸਪਾਟਾ ਟਿਕਟ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕੀਤੀ ਗਈ ਹੈ",
        "postconditions": "ਅਦਾਇਗੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਨੂੰ 'ਅਦਾ ਕੀਤਾ ਗਿਆ' ਵਜੋਂ ਅਪਡੇਟ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਅਦਾਇਗੀ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "ਯੂਜ਼ਰ ਵੱਲੋਂ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਲਈ ਭੁਗਤਾਨ ਕਰਨਾ",
        "preconditions": "ਹਵਾਈ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦਾਰੀ ਦੀ ਸਥਿਤੀ ਵਿੱਚ, ਯੂਜ਼ਰ ਫਲਾਈਟ ਆਰਡਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਪਹਿਲਾਂ ਹੀ ਤੈਅ ਕੀਤਾ ਗਿਆ ਹੈ",
        "postconditions": "ਭੁਗਤਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ ਅਤੇ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ ਭੁਗਤਾਨ ਕੀਤਾ ਗਿਆ ਵਿੱਚ ਅਪਡੇਟ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਭੁਗਤਾਨ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "ਯੂਜ਼ਰ ਰੇਲਵੇ ਟਿਕਟ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਕਰਦਾ ਹੈ",
        "preconditions": "ਰੇਲਵੇ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦਾਰੀ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਯੂਜ਼ਰ ਰੇਲਵੇ ਟਿਕਟ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਅਤੇ ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਦੀ ਪੁਸ਼ਟੀ ਕੀਤੀ ਗਈ ਹੈ",
        "postconditions": "ਅਦਾਇਗੀ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ ਅਤੇ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ 'ਅਦਾ ਕੀਤਾ ਗਿਆ' ਵਜੋਂ ਅਪਡੇਟ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ"
        },
        "returns": "ਅਦਾਇਗੀ ਨਤੀਜੇ ਦੀ ਜਾਣਕਾਰੀ",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "ਯੂਜ਼ਰ ID ਦੇ ਅਧਾਰ ਤੇ, ਯੂਜ਼ਰ ਦੇ ਹੋਟਲ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰੋ, ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਯੂਜ਼ਰ ID, ਹੋਟਲ ID, ਆਰਡਰ ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਸਮੇਤ ਵਾਪਸ ਕਰੋ।",
        "preconditions": "ਯੂਜ਼ਰ ਦੀ ਲੋੜ ਹੋਟਲ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰਨਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ/ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ ਹੈ।",
        "args": {
            "user_id": "ਯੂਜ਼ਰ ID",
            "date": "ਤਾਰੀਖ",
            "status": "ਆਰਡਰ ਸਥਿਤੀ"
        },
        "returns": "ਨਿਰਧਾਰਤ ਯੂਜ਼ਰ ਦੀ ਹੋਟਲ ਆਰਡਰ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "ਯੂਜ਼ਰ ID ਦੇ ਅਧਾਰ ਤੇ, ਯੂਜ਼ਰ ਦੇ ਸੈਲਾਨੀ ਸਥਾਨ ਟਿਕਟ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਯੂਜ਼ਰ ID, ਸੈਲਾਨੀ ਸਥਾਨ ID, ਆਰਡਰ ਕੁੱਲ ਰਕਮ, ਆਰਡਰ ਕਰਨ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਕਰਨ ਦਾ ਸਮਾਂ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਯੂਜ਼ਰ ਦੀ ਲੋੜ ਸੈਲਾਨੀ ਸਥਾਨ ਟਿਕਟ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰਨਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ/ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ ਹੈ।",
        "args": {
            "user_id": "ਯੂਜ਼ਰ ID",
            "date": "ਤਾਰੀਖ",
            "status": "ਆਰਡਰ ਸਥਿਤੀ"
        },
        "returns": "ਨਿਰਧਾਰਤ ਯੂਜ਼ਰ ਦੀ ਸੈਲਾਨੀ ਸਥਾਨ ਟਿਕਟ ਆਰਡਰ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "ਯੂਜ਼ਰ ID ਦੇ ਅਧਾਰ ਤੇ, ਯੂਜ਼ਰ ਦੇ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਦੀ ਜਾਂਚ ਕਰੋ, ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਯੂਜ਼ਰ ID, ਉਡਾਣ ID, ਆਰਡਰ ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਸਮੇਤ ਵਾਪਸ ਕਰੋ।",
        "preconditions": "ਯੂਜ਼ਰ ਦੀ ਲੋੜ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਦੀ ਜਾਂਚ ਕਰਨਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ/ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ।",
        "args": {
            "user_id": "ਯੂਜ਼ਰ ID",
            "date": "ਤਾਰੀਖ",
            "status": "ਆਰਡਰ ਸਥਿਤੀ"
        },
        "returns": "ਨਿਰਧਾਰਤ ਯੂਜ਼ਰ ਦੀ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "ਯੂਜ਼ਰ ID ਦੇ ਅਧਾਰ ਤੇ, ਯੂਜ਼ਰ ਦੇ ਟਰੇਨ ਟਿਕਟ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਯੂਜ਼ਰ ID, ਟਰੇਨ ID, ਆਰਡਰ ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਯੂਜ਼ਰ ਦੀ ਲੋੜ ਟਰੇਨ ਟਿਕਟ ਆਰਡਰਾਂ ਦੀ ਜਾਂਚ ਕਰਨਾ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਜਾਣਕਾਰੀ ਵਾਪਸ ਕਰੋ, ਬਾਅਦ ਵਿੱਚ ਸੋਧ/ਰੱਦ ਕਰਨ ਲਈ ਸੁਵਿਧਾਜਨਕ ਹੈ।",
        "args": {
            "user_id": "ਯੂਜ਼ਰ ID",
            "date": "ਤਾਰੀਖ",
            "status": "ਆਰਡਰ ਸਥਿਤੀ"
        },
        "returns": "ਨਿਰਧਾਰਤ ਯੂਜ਼ਰ ਦੀ ਟਰੇਨ ਟਿਕਟ ਆਰਡਰ ਜਾਣਕਾਰੀ",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ਹੋਟਲ ਆਰਡਰ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਹੋਟਲ ID, ਆਰਡਰ ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਕਰਨ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਰਡਰ ਕਮਰੇ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ (ਕਮਰੇ ਦੀ ਕਿਸਮ, ਚੈਕ-ਇਨ ਤਾਰੀਖ, ਕੀਮਤ, ਕਮਰਾ ID) ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਹੋਟਲ ਆਰਡਰ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਵਿਵਰਣ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਆਰਡਰ ਵਿਵਰਣ",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "ਆਕਰਸ਼ਣ ਟਿਕਟ ਆਰਡਰ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਆਕਰਸ਼ਣ ID, ਕੁੱਲ ਆਰਡਰ ਕੀਮਤ, ਆਰਡਰ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਰਡਰ ਆਕਰਸ਼ਣ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ (ਟਿਕਟ ਕਿਸਮ, ਤਾਰੀਖ, ਕੀਮਤ, ਟਿਕਟ ID) ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਆਕਰਸ਼ਣ ਟਿਕਟ ਆਰਡਰ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਵਿਵਰਣ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਆਰਡਰ ਵਿਵਰਣ",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਦੇ ਵੇਰਵੇ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਉਡਾਣ ID, ਆਰਡਰ ਕੁੱਲ ਕੀਮਤ, ਆਰਡਰ ਕਰਨ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਰਡਰ ਟਿਕਟ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ (ਸੀਟ ਕਿਸਮ, ਤਾਰੀਖ, ਕੀਮਤ, ਸੀਟ ID) ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਦੇ ਵੇਰਵੇ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਦੀ ਪੁਸ਼ਟੀ ਕੀਤੀ ਗਈ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਦੇ ਵੇਰਵੇ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਆਰਡਰ ਦੇ ਵੇਰਵੇ",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ਰੇਲਗੱਡੀ ਟਿਕਟ ਆਰਡਰ ਦੇ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰੋ, ਜਿਸ ਵਿੱਚ ਆਰਡਰ ID, ਆਰਡਰ ਕਿਸਮ, ਉਪਭੋਗਤਾ ID, ਰੇਲਗੱਡੀ ID, ਆਰਡਰ ਕੁਲ ਕੀਮਤ, ਆਰਡਰ ਕਰਨ ਦਾ ਸਮਾਂ, ਅਪਡੇਟ ਸਮਾਂ, ਆਰਡਰ ਸਥਿਤੀ ਅਤੇ ਆਰਡਰ ਰੇਲਗੱਡੀ ਟਿਕਟ ਦੀ ਵਿਸਤ੍ਰਿਤ ਜਾਣਕਾਰੀ (ਸੀਟ ਕਿਸਮ, ਤਾਰੀਖ, ਕੀਮਤ, ਸੀਟ ID) ਸ਼ਾਮਲ ਹੈ।",
        "preconditions": "ਉਪਭੋਗਤਾ ਰੇਲਗੱਡੀ ਟਿਕਟ ਆਰਡਰ ਦੇ ਵਿਵਰਣ ਪ੍ਰਾਪਤ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤਾ ਗਿਆ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਵਿਵਰਣ ਵਾਪਸ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID"
        },
        "returns": "ਆਰਡਰ ਵਿਵਰਣ",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "ਰੇਲਗੱਡੀ ਦੇ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਸੋਧੋ, ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ ਬਦਲਣ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ, ਅਤੇ ਮੁੱਲ ਦੇ ਅੰਤਰ ਦਾ ਭੁਗਤਾਨ ਜਾਂ ਵਾਪਸੀ ਸਵੈਚਾਲਿਤ ਤੌਰ 'ਤੇ ਸੰਭਾਲਦਾ ਹੈ।",
        "preconditions": "ਰੇਲਗੱਡੀ ਦੇ ਟਿਕਟ ਦੀ ਜਾਂਚ ਅਤੇ ਖਰੀਦ ਦੇ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਰੇਲਗੱਡੀ ਦੇ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਸੋਧਣ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤੀ ਗਈ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਨੂੰ ਸੋਧੋ ਅਤੇ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ ਅਪਡੇਟ ਕਰੋ। ਜੇਕਰ ਮੁੱਲ ਦੇ ਅੰਤਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ unpaid ਕਰੋ, ਨਹੀਂ ਤਾਂ ਮੂਲ ਸਥਿਤੀ ਬਣਾਈ ਰੱਖੋ। ਜੇਕਰ ਮੁੱਲ ਦੇ ਅੰਤਰ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਉਪਭੋਗਤਾ ਨੂੰ ਇਸ ਆਰਡਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID",
            "user_id": "ਉਪਭੋਗਤਾ ID",
            "new_date": "ਨਵੀਂ ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ, ਫਾਰਮੈਟ %Y-%m-%d ਹੈ"
        },
        "returns": "(ਸੋਧੇ ਗਏ ਆਰਡਰ ਦੀ ਸਮੱਗਰੀ, ਮੁੱਲ ਦਾ ਅੰਤਰ, ਸਕਾਰਾਤਮਕ ਦਾ ਅਰਥ ਹੈ ਅੰਤਰ ਦਾ ਭੁਗਤਾਨ ਕਰਨ ਦੀ ਲੋੜ ਹੈ, ਨਕਾਰਾਤਮਕ ਦਾ ਅਰਥ ਹੈ ਅੰਤਰ ਦੀ ਵਾਪਸੀ)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਸੋਧੋ, ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ ਬਦਲਣ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ, ਅਤੇ ਕੀਮਤ ਅੰਤਰ ਦੀ ਅਦਾਇਗੀ ਜਾਂ ਵਾਪਸੀ ਨੂੰ ਸਵੈਚਾਲਿਤ ਤੌਰ 'ਤੇ ਸੰਭਾਲਦਾ ਹੈ।",
        "preconditions": "ਹਵਾਈ ਟਿਕਟ ਖੋਜ ਅਤੇ ਖਰੀਦ ਦੇ ਸੰਦਰਭ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਹਵਾਈ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਸੋਧਣ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ID ਨਿਰਧਾਰਤ ਕੀਤੀ ਗਈ ਹੈ।",
        "postconditions": "ਆਰਡਰ ਨੂੰ ਸੋਧੋ ਅਤੇ ਆਰਡਰ ਸਥਿਤੀ ਨੂੰ ਅਪਡੇਟ ਕਰੋ, ਜੇਕਰ ਕੀਮਤ ਅੰਤਰ ਭਰਨ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਆਰਡਰ ਸਥਿਤੀ ਨੂੰ unpaid ਕਰੋ, ਨਹੀਂ ਤਾਂ ਮੂਲ ਸਥਿਤੀ ਬਣਾਈ ਰੱਖੋ, ਜੇਕਰ ਕੀਮਤ ਅੰਤਰ ਭਰਨ ਦੀ ਲੋੜ ਹੈ, ਤਾਂ ਉਪਭੋਗਤਾ ਨੂੰ ਇਸ ਆਰਡਰ ਦੀ ਅਦਾਇਗੀ ਲਈ ਮਾਰਗਦਰਸ਼ਨ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ID",
            "user_id": "ਉਪਭੋਗਤਾ ID",
            "new_date": "ਨਵੀਂ ਰਵਾਨਗੀ ਦੀ ਤਾਰੀਖ, ਫਾਰਮੈਟ %Y-%m-%d ਹੈ"
        },
        "returns": "(ਸੋਧੇ ਗਏ ਆਰਡਰ ਦੀ ਸਮੱਗਰੀ, ਕੀਮਤ ਅੰਤਰ, ਸਕਾਰਾਤਮਕ ਦਾ ਅਰਥ ਹੈ ਅੰਤਰ ਭਰਨ ਦੀ ਲੋੜ ਹੈ, ਨਕਾਰਾਤਮਕ ਦਾ ਅਰਥ ਹੈ ਅੰਤਰ ਵਾਪਸ ਕੀਤਾ ਜਾਵੇਗਾ)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "ਉਪਭੋਗਤਾ ਦੁਆਰਾ ਪਹਿਲਾਂ ਤੋਂ ਬੁੱਕ ਕੀਤੀ ਹੋਟਲ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨਾ",
        "preconditions": "ਹੋਟਲ ਬੁਕਿੰਗ ਜਾਂਚ ਸਥਿਤੀ ਵਿੱਚ, ਉਪਭੋਗਤਾ ਹੋਟਲ ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੀ ਬੇਨਤੀ ਕਰਦਾ ਹੈ, ਪਿਛਲੇ ਸੰਦਰਭ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਨਿਰਧਾਰਤ ਕੀਤੀ ਗਈ ਹੈ",
        "postconditions": "ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰੋ ਅਤੇ ਆਰਡਰ ਦੀ ਸਥਿਤੀ ਨੂੰ ਅਪਡੇਟ ਕਰੋ, ਜੇਕਰ ਕੋਈ ਰਿਫੰਡ ਅੰਤਰ ਹੈ ਤਾਂ ਉਪਭੋਗਤਾ ਨੂੰ ਸੂਚਿਤ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ",
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਤੇ ਰਿਫੰਡ ਰਕਮ",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "ਉਪਭੋਗਤਾ ਦੁਆਰਾ ਬੁੱਕ ਕੀਤੇ ਗਏ ਆਕਰਸ਼ਣ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨਾ",
        "preconditions": "ਇਤਿਹਾਸਕ ਗੱਲਬਾਤ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਮੌਜੂਦ ਹੈ ਜਾਂ ਪਹਿਲਾਂ ਹੀ ਆਰਡਰ ਜਾਂਚ ਕੀਤੀ ਗਈ ਹੈ, ਉਪਭੋਗਤਾ ਕੋਲ ਇਸ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨ ਦੀ ਇਜਾਜ਼ਤ ਹੈ।",
        "postconditions": "ਜੇਕਰ ਕੋਈ ਮੁੱਲ ਅੰਤਰ ਵਾਪਸ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਤਾਂ ਬਸ ਉਪਭੋਗਤਾ ਨੂੰ ਸੂਚਿਤ ਕਰੋ।",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ",
            "user_id": "ਉਪਭੋਗਤਾ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਲਈ ਵਾਪਸੀ ਰਕਮ",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "ਯੂਜ਼ਰ ਵੱਲੋਂ ਬੁੱਕ ਕੀਤੀ ਉਡਾਣ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨਾ",
        "preconditions": "ਇਤਿਹਾਸਕ ਗੱਲਬਾਤ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਮੌਜੂਦ ਹੈ ਜਾਂ ਪਹਿਲਾਂ ਹੀ ਆਰਡਰ ਜਾਂਚ ਕੀਤੀ ਗਈ ਹੈ, ਯੂਜ਼ਰ ਕੋਲ ਇਸ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨ ਦੀ ਇਜਾਜ਼ਤ ਹੈ",
        "postconditions": "ਜੇਕਰ ਕੋਈ ਅੰਤਰ ਵਾਪਸ ਕੀਤਾ ਜਾਂਦਾ ਹੈ, ਤਾਂ ਯੂਜ਼ਰ ਨੂੰ ਸੂਚਿਤ ਕਰੋ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ",
            "user_id": "ਯੂਜ਼ਰ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ 'ਤੇ ਵਾਪਸ ਕੀਤੀ ਗਈ ਰਕਮ",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "ਵਰਤੋਂਕਾਰ ਵੱਲੋਂ ਬੁੱਕ ਕੀਤੀ ਟਰੇਨ ਟਿਕਟ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨਾ",
        "preconditions": "ਇਤਿਹਾਸਕ ਗੱਲਬਾਤ ਵਿੱਚ ਆਰਡਰ ਆਈਡੀ ਮੌਜੂਦ ਹੋਵੇ ਜਾਂ ਪਹਿਲਾਂ ਹੀ ਆਰਡਰ ਜਾਂਚ ਕੀਤੀ ਗਈ ਹੋਵੇ, ਅਤੇ ਵਰਤੋਂਕਾਰ ਕੋਲ ਇਸ ਆਰਡਰ ਨੂੰ ਰੱਦ ਕਰਨ ਦੀ ਇਜਾਜ਼ਤ ਹੋਵੇ",
        "postconditions": "ਜੇਕਰ ਕੋਈ ਅੰਤਰ ਰਕਮ ਵਾਪਸ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਤਾਂ ਵਰਤੋਂਕਾਰ ਨੂੰ ਸੂਚਿਤ ਕਰਨਾ ਕਾਫੀ ਹੈ",
        "args": {
            "order_id": "ਆਰਡਰ ਆਈਡੀ",
            "user_id": "ਵਰਤੋਂਕਾਰ ਆਈਡੀ"
        },
        "returns": "ਆਰਡਰ ਰੱਦ ਕਰਨ ਦੀ ਵਾਪਸੀ ਰਕਮ",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Belarusian version
TOOL_DESCRIPTIONS_BE = {
    "get_ota_hotel_info": {
        "description": "Атрымаць інфармацыю аб гатэлі, уключаючы ідэнтыфікатар гатэля, назву, рэйтынг, зорнасць, адрас, тэгі, спіс нумароў",
        "preconditions": "У сцэнары пошуку і браніравання гатэля неабходна атрымаць падрабязную інфармацыю аб гатэлі",
        "postconditions": "Вяртае падрабязную інфармацыю аб гатэлі, накіроўвае карыстальніка на выбар нумара і афармленне замовы",
        "args": {
            "hotel_id": "Ідэнтыфікатар гатэля"
        },
        "returns": "Інфармацыя аб гатэлі",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Атрымаць інфармацыю аб славутасці, уключаючы ідэнтыфікатар славутасці, назву, адрас, апісанне, рэйтынг, гадзіны працы, кошт квітка, спіс відаў квіткоў",
        "preconditions": "У сцэнары наведвання славутасцяў, калі неабходна атрымаць падрабязную інфармацыю аб славутасці",
        "postconditions": "Вяртае падрабязную інфармацыю аб славутасці, накіроўвае карыстальніка на выбар квіткоў і афармленне замовы",
        "args": {
            "attraction_id": "ідэнтыфікатар славутасці"
        },
        "returns": "Інфармацыя аб славутасці",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Атрымаць інфармацыю аб рэйсе, якая ўключае ідэнтыфікатар рэйса, нумар рэйса, горад вылету, горад прыбыцця, месцазнаходжанне аэрапорта вылету, месцазнаходжанне аэрапорта прыбыцця, час вылету, час прыбыцця, тэгі рэйса, спіс тыпаў месцаў",
        "preconditions": "У сцэнары пошуку і пакупкі авіябілетаў неабходна атрымаць падрабязную інфармацыю аб рэйсе",
        "postconditions": "Вяртае падрабязную інфармацыю аб рэйсе, накіроўвае карыстальніка да выбару месцаў і афармлення замовы",
        "args": {
            "flight_id": "Ідэнтыфікатар рэйса"
        },
        "returns": "Інфармацыя аб рэйсе",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Атрымаць інфармацыю пра цягнік, уключаючы ідэнтыфікатар цягніка, нумар цягніка, горад адпраўлення, горад прыбыцця, месцазнаходжанне станцыі адпраўлення, месцазнаходжанне станцыі прыбыцця, час адпраўлення, час прыбыцця, тэгі цягніка, спіс тыпаў сядзенняў",
        "preconditions": "У сцэнары пошуку і пакупкі квіткоў на цягнік неабходна атрымаць падрабязную інфармацыю пра цягнік",
        "postconditions": "Вяртае падрабязную інфармацыю пра цягнік, накіроўвае карыстальніка да выбару сядзення і афармлення замовы",
        "args": {
            "train_id": "ідэнтыфікатар цягніка"
        },
        "returns": "Інфармацыя пра цягнік",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "У кантэксце падарожжаў і пражывання, на аснове лакацыйных патрэб і пераваг карыстальніка, рэкамендаваць падыходзячыя варыянты гатэляў і прадастаўляць базавую інфармацыю пра гатэль, якая ўключае id гатэля, назву, рэйтынг, зорнасць, адрас і тэгі",
        "preconditions": "Карыстальнік просіць забраніраваць гатэль і падае ключавыя словы, звязаныя з гатэлем, або месцазнаходжанне",
        "postconditions": "Вяртае спіс гатэляў, якія адпавядаюць крытэрыям. Калі неабходна праглядзець дэталі гатэля (спіс пакояў, цэны і г.д.), трэба выкарыстоўваць інструмент запыту дэталяў гатэля. Накіроўвае карыстальніка да выбару гатэля",
        "args": {
            "city_name": "Назва горада",
            "key_words": "Ключавыя словы для пошуку (супадзенне з назвай гатэля, апісаннем гатэля і г.д.)"
        },
        "returns": "Структураваны вывад базавая інфармацыі пра гатэль",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "На аснове патрэбаў і пераваг карыстальніка адносна месца, рэкамендаваць падыходзячыя варыянты славутасцяў, прадастаўляць базавую інфармацыю пра славутасці, якая ўключае id славутасці, назву, адрас, апісанне, рэйтынг, час працы",
        "preconditions": "Карыстальнік просіць забраніраваць славутасць і падае ключавыя словы або месцы, звязаныя са славутасцю",
        "postconditions": "Вяртае спіс славутасцяў, якія адпавядаюць умовам; калі неабходна праглядзець дэталі славутасці (спіс квіткоў, цэны і г.д.), трэба выкарыстоўваць інструмент запыту дэталяў славутасці, накіроўваць карыстальніка на выбар славутасці",
        "args": {
            "city_name": "Назва горада",
            "key_words": "Ключавыя словы для пошуку (супадзенне з назвай славутасці, месцазнаходжаннем, адрасам, асаблівасцямі і г.д.)"
        },
        "returns": "Структураваны вывад базавая інфармацыі пра славутасці",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Рэкамендуе падыходзячыя варыянты рэйсаў на аснове месцавых патрэбаў і пераваг карыстальніка, надае асноўную інфармацыю аб рэйсе, уключаючы ідэнтыфікатар рэйса, нумар рэйса, горад вылету, горад прыбыцця, месцазнаходжанне аэрапорта вылету, месцазнаходжанне аэрапорта прыбыцця, час вылету, час прыбыцця, тэгі рэйса",
        "preconditions": "Карыстальнік запытвае браніраванне рэйса і надае ключавыя словы або месцазнаходжанні, звязаныя з рэйсам",
        "postconditions": "Вяртае спіс рэйсаў, якія адпавядаюць умовам; калі неабходна праглядзець дэталі рэйса (спіс тыпаў месцаў, цана, дата і г.д.), трэба выкарыстоўваць інструмент запыту дэталяў рэйса; накіроўвае карыстальніка на выбар рэйса",
        "args": {
            "departure": "Горад вылету",
            "destination": "Горад прыбыцця"
        },
        "returns": "Структураваны вывад асноўнай інфармацыі аб рэйсе",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "На аснове патрэбаў і пераваг карыстальніка адносна месцазнаходжання рэкамендуе падыходзячыя варыянты цягнікоў, надае асноўную інфармацыю пра квіткі на цягнік, уключаючы ідэнтыфікатар цягніка, нумар рэйса, горад адпраўлення, горад прыбыцця, месцазнаходжанне станцыі адпраўлення, месцазнаходжанне станцыі прыбыцця, час адпраўлення, час прыбыцця, тэгі цягніка",
        "preconditions": "Карыстальнік запытвае забраніраваць цягнік і падае ключавыя словы або месцы, звязаныя з цягніком",
        "postconditions": "Вяртае спіс квіткоў на цягнік, якія адпавядаюць умовам; калі неабходна праглядзець дэталі квітка (спіс тыпаў месцаў, цана, дата і г.д.), трэба выкарыстоўваць інструмент запыту дэталяў квітка на цягнік, накіроўвае карыстальніка на выбар квітка на цягнік",
        "args": {
            "departure": "Горад адпраўлення",
            "destination": "Горад прыбыцця",
            "date": "Дата адпраўлення"
        },
        "returns": "Структураваны вывад асноўнай інфармацыі пра цягнік",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Калі карыстальнік браніруе гатэль, сістэма фарміруе заказ на аснове патрабаванняў карыстальніка (напрыклад, назва гатэля, дата заезду, колькасць людзей і г.д.)",
        "preconditions": "Карыстальнік увайшоў у сістэму і прадаставіў сапраўдны ідэнтыфікатар (user_id), карыстальнік прадаставіў сапраўдную назву гатэля (hotel_name) і тып пакоя (room_type), сістэма мае інфармацыю аб мэтавым гатэлі, і ў гэтым гатэлі ёсць нумары на запрошаныя даты",
        "postconditions": "Заказ сфарміраваны, карыстальніка просяць пацвердзіць аплату",
        "args": {
            "hotel_id": "ID гатэля",
            "room_id": "ID пакоя",
            "user_id": "ID карыстальніка"
        },
        "returns": "Вынік аперацыі стварэння заказа",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Карыстальнік набывае квіткі на славутасць паводле даты, сістэма вяртае адпаведную інфармацыю пра квіткі і афармляе заказ.",
        "preconditions": "У сцэнары наведвання славутасцяў карыстальнік запрашае забраніраваць славутасць і надае неабходную інфармацыю для браніравання.",
        "postconditions": "Заказ створаны, карыстальніка просяць пацвердзіць аплату.",
        "args": {
            "attraction_id": "Ідэнтыфікатар славутасці",
            "ticket_id": "Ідэнтыфікатар квітка",
            "user_id": "Ідэнтыфікатар карыстальніка",
            "date": "Дата наведвання, фармат %Y-%m-%d",
            "quantity": "Колькасць"
        },
        "returns": "Зваротная сувязь аперацыі стварэння заказа.",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Карыстальнік набывае авіябілеты паводле нумара рэйса, даты, тыпу месца і колькасці; сістэма вяртае адпаведную інфармацыю аб білеце і афармляе заказ",
        "preconditions": "У сцэнары пошуку і пакупкі авіябілетаў карыстальнік запатраваў браніраванне рэйса і прадаставіў неабходную інфармацыю для браніравання",
        "postconditions": "Заказ створаны, карыстальніка просяць пацвердзіць аплату",
        "args": {
            "flight_id": "ID рэйса",
            "seat_id": "ID месца",
            "user_id": "ID карыстальніка",
            "date": "Дата вылету",
            "quantity": "Колькасць"
        },
        "returns": "Вынік аперацыі стварэння заказа",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Карыстальнік купляе чыгуначныя білеты паводле нумара цягніка, даты, тыпу месца і колькасці, сістэма вяртае адпаведную інфармацыю пра білет і афармляе заказ",
        "preconditions": "У сцэнары пошуку і пакупкі чыгуначных білетаў карыстальнік робіць запыт на браніраванне цягніка і надае неабходную інфармацыю для браніравання",
        "postconditions": "Заказ створаны, калі ласка, пацвердзіце аплату",
        "args": {
            "train_id": "ID цягніка",
            "seat_id": "ID месца",
            "user_id": "ID карыстальніка",
            "date": "Дата адпраўлення",
            "quantity": "Колькасць"
        },
        "returns": "Вынік аперацыі стварэння заказа",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Карыстальнік ажыццяўляе аплату замовы на гатэль",
        "preconditions": "У сцэнары пошуку і браніравання гатэля карыстальнік запрашвае аплату замовы на гатэль, ідэнтыфікатар замовы ўжо вызначаны ў папярэднім кантэксце",
        "postconditions": "Пацвердзіць аплату і абнавіць статус замовы на «аплачана»",
        "args": {
            "order_id": "Ідэнтыфікатар замовы"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Карыстальнік ажыццяўляе аплату замовы на квіток",
        "preconditions": "У сцэнарыі наведвання славутасцяў карыстальнік ініцыюе аплату замовы на квіток, ідэнтыфікатар замовы быў вызначаны ў папярэднім кантэксце",
        "postconditions": "Пацвярджае аплату і абнаўляе статус замовы на «аплачана»",
        "args": {
            "order_id": "Ідэнтыфікатар замовы"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Карыстальнік ажыццяўляе аплату замовы на авіябілет",
        "preconditions": "У сцэнары пошуку і пакупкі авіябілетаў карыстальнік запрашвае аплату замовы на рэйс, ідэнтыфікатар замовы быў вызначаны раней",
        "postconditions": "Аплата пацвярджаецца, і статус замовы абнаўляецца на аплачаны",
        "args": {
            "order_id": "Ідэнтыфікатар замовы"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Карыстальнік ажыццяўляе аплату замовы на чыгуначны білет",
        "preconditions": "У сцэнары пошуку і пакупкі чыгуначных білетаў карыстальнік ініцыюе аплату замовы, ідэнтыфікатар замовы быў вызначаны раней",
        "postconditions": "Пацвярджае аплату і абнаўляе статус замовы на «аплачана»",
        "args": {
            "order_id": "Ідэнтыфікатар замовы"
        },
        "returns": "Інфармацыя пра вынік аплаты",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Па ID карыстальніка запытаць гатэльныя заказы карыстальніка, вярнуць інфармацыю, якая ўтрымлівае ID заказа, тып заказа, ID карыстальніка, ID гатэля, агульную суму заказа, час афармлення заказа, час абнаўлення і статус заказа",
        "preconditions": "Запыт карыстальніка заключаецца ў пошуку гатэльных заказаў",
        "postconditions": "Вяртае інфармацыю аб заказе, што зручна для наступнага змянення або скасавання",
        "args": {
            "user_id": "ID карыстальніка",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Інфармацыя аб гатэльных заказах указанага карыстальніка",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Па ідэнтыфікатары карыстальніка запытаць заказы на квіткі на славутасці для карыстальніка, вярнуць інфармацыю, якая ўтрымлівае ідэнтыфікатар заказа, тып заказа, ідэнтыфікатар карыстальніка, ідэнтыфікатар славутасці, агульную суму заказа, час афармлення, час абнаўлення і статус заказа",
        "preconditions": "Запыт карыстальніка заключаецца ў пошуку заказаў на квіткі на славутасці",
        "postconditions": "Вяртае інфармацыю аб заказе, зручную для наступнага змянення або скасавання",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Інфармацыя аб заказах на квіткі на славутасці для ўказанага карыстальніка",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Па ідэнтыфікатары карыстальніка запытаць заказы на авіябілеты карыстальніка, вярнуць інфармацыю, якая ўтрымлівае ідэнтыфікатар заказа, тып заказа, ідэнтыфікатар карыстальніка, ідэнтыфікатар рэйса, агульную суму заказа, час афармлення, час абнаўлення і статус заказа",
        "preconditions": "Запыт карыстальніка на пошук заказаў на авіябілеты",
        "postconditions": "Вярнуць інфармацыю аб заказе для зручнасці наступнага змянення або скасавання",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Інфармацыя аб заказах на авіябілеты для ўказанага карыстальніка",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Па ідэнтыфікатары карыстальніка запытвае заказы на чыгуначныя білеты карыстальніка, вяртае інфармацыю, якая ўключае ідэнтыфікатар заказа, тып заказа, ідэнтыфікатар карыстальніка, ідэнтыфікатар цягніка, агульную суму заказа, час афармлення, час абнаўлення і статус заказа",
        "preconditions": "Запыт карыстальніка заключаецца ў пошуку заказаў на чыгуначныя білеты",
        "postconditions": "Вяртае інфармацыю аб заказе, што зручна для наступнага змянення або скасавання",
        "args": {
            "user_id": "Ідэнтыфікатар карыстальніка",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Інфармацыя аб заказах на чыгуначныя білеты для ўказанага карыстальніка",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Атрымаць дэталі замовы гатэля, уключае ID замовы, тып замовы, ID карыстальніка, ID гатэля, агульную суму замовы, час афармлення замовы, час абнаўлення, статус замовы і дэталі пакоя замовы (тып пакоя, дата засялення, цана, ID пакоя)",
        "preconditions": "Карыстальнік запрашае атрымаць дэталі замовы гатэля, ID замовы вызначаны вышэй",
        "postconditions": "Вяртае дэталі замовы",
        "args": {
            "order_id": "ID замовы"
        },
        "returns": "Дэталі замовы",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Атрымаць падрабязнасці замовы на квіткі да славутасці, уключаючы ID замовы, тып замовы, ID карыстальніка, ID славутасці, агульную суму замовы, час афармлення замовы, час абнаўлення, статус замовы і падрабязную інфармацыю пра славутасць у замове (тып квітка, дата, цана, ID квітка)",
        "preconditions": "Карыстальнік запрашвае атрымаць падрабязнасці замовы на квіткі да славутасці, ID замовы быў вызначаны вышэй",
        "postconditions": "Вяртае падрабязнасці замовы",
        "args": {
            "order_id": "ID замовы"
        },
        "returns": "Падрабязнасці замовы",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Атрыманне дэталяў замовы на авіябілет, якія ўключаюць ID замовы, тып замовы, ID карыстальніка, ID рэйса, агульны кошт замовы, час афармлення замовы, час абнаўлення, статус замовы і дэталі авіябілетаў у замове (тып месца, дата, кошт, ID месца)",
        "preconditions": "Карыстальнік запрашае атрымаць дэталі замовы на авіябілет, ID замовы вызначаны вышэй",
        "postconditions": "Вяртае дэталі замовы",
        "args": {
            "order_id": "ID замовы"
        },
        "returns": "Дэталі замовы",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Атрымаць падрабязнасці замовы на чыгуначны білет, уключаючы ID замовы, тып замовы, ID карыстальніка, ID цягніка, агульную суму замовы, час афармлення, час абнаўлення, статус замовы і падрабязную інфармацыю пра чыгуначны білет у замове (тып месца, дата, цана, ID месца)",
        "preconditions": "Карыстальнік запрашвае атрымаць падрабязнасці замовы на чыгуначны білет, ID замовы вызначаны вышэй",
        "postconditions": "Вяртае падрабязнасці замовы",
        "args": {
            "order_id": "ID замовы"
        },
        "returns": "Падрабязнасці замовы",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Змяніць замову на чыгуначны квіток, падтрымлівае змену даты адпраўлення, аўтаматычна апрацоўвае даплату або вяртанне розніцы ў цане.",
        "preconditions": "У сцэнары пошуку і пакупкі чыгуначных квіткоў, калі карыстальнік просіць змяніць замову на чыгуначны квіток, ідэнтыфікатар замовы ўжо вызначаны вышэй.",
        "postconditions": "Змяніць замову і абнавіць статус замовы; калі патрабуецца даплата, статус замовы змяняецца на unpaid, у адваротным выпадку застаецца ранейшы статус; калі патрабуецца даплата, карыстальніка неабходна накіраваць да аплаты гэтай замовы.",
        "args": {
            "order_id": "ID замовы",
            "user_id": "ID карыстальніка",
            "new_date": "Новая дата адпраўлення, фармат %Y-%m-%d"
        },
        "returns": "(Змест змененай замовы, розніца ў цане, дадатнае значэнне азначае неабходнасць даплаты, адмоўнае — вяртанне розніцы)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Змяніць заказ на авіябілеты, падтрымлівае змену даты вылету, аўтаматычна апрацоўвае даплату або вяртанне розніцы ў цане.",
        "preconditions": "У сцэнары пошуку і пакупкі авіябілетаў, карыстальнік просіць змяніць заказ на авіябілеты, ID заказа вызначаны ў папярэднім кантэксце.",
        "postconditions": "Змяніць заказ і абнавіць статус заказа; калі неабходна даплаціць розніцу, статус заказа змяняецца на unpaid, у адваротным выпадку захоўваецца зыходны статус; калі патрабуецца даплата, неабходна накіраваць карыстальніка да аплаты дадзенага заказа.",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID карыстальніка",
            "new_date": "Новая дата вылету, фармат %Y-%m-%d"
        },
        "returns": "(Змест змененага заказа, розніца ў цане, дадатнае значэнне азначае неабходнасць даплаты, адмоўнае — вяртанне розніцы)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Карыстальнік скасоўвае ўжо забраніраваны заказ на гатэль",
        "preconditions": "У сцэнарыі пошуку і браніравання гатэля, карыстальнік просіць скасаваць заказ на гатэль, ідэнтыфікатар заказа вызначаны вышэй",
        "postconditions": "Заказ скасаваны і статус заказа абноўлены; калі неабходна вярнуць розніцу ў коште, дастаткова паведаміць пра гэта карыстальніку",
        "args": {
            "order_id": "Ідэнтыфікатар заказа",
            "user_id": "Ідэнтыфікатар карыстальніка"
        },
        "returns": "Сума вяртання сродкаў за скасаваны заказ",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Карыстальнік скасоўвае заказ на квіткі да славутасці, які быў забраніраваны",
        "preconditions": "У гісторыі дыялогу ёсць ідэнтыфікатар заказа, або ўжо быў выкананы запыт па заказе; карыстальнік мае права скасаваць гэты заказ",
        "postconditions": "Калі неабходна вярнуць розніцу ў коште, дастаткова паведаміць пра гэта карыстальніку",
        "args": {
            "order_id": "Ідэнтыфікатар заказа",
            "user_id": "Ідэнтыфікатар карыстальніка"
        },
        "returns": "Сума вяртання сродкаў за скасаванне заказа",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Карыстальнік скасоўвае ўжо забраніраваны заказ на авіябілет",
        "preconditions": "У гісторыі дыялогу ёсць ідэнтыфікатар заказа або ўжо быў выкананы запыт па заказе, і карыстальнік мае права скасаваць гэты заказ",
        "postconditions": "Калі неабходна вярнуць розніцу ў коште, дастаткова паведаміць пра гэта карыстальніку",
        "args": {
            "order_id": "Ідэнтыфікатар заказа",
            "user_id": "Ідэнтыфікатар карыстальніка"
        },
        "returns": "Сума вяртання сродкаў за скасаванне заказа",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Карыстальнік скасоўвае ўжо забраніраваны заказ на квіткі на цягнік",
        "preconditions": "У гісторыі размовы ёсць ID заказа або ўжо выконваўся запыт па заказе, карыстальнік мае права скасаваць гэты заказ",
        "postconditions": "Калі неабходна вярнуць розніцу ў цане, дастаткова паведаміць пра гэта карыстальніку",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID карыстальніка"
        },
        "returns": "Сума вяртання сродкаў за скасаванне заказа",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Malay version
TOOL_DESCRIPTIONS_MS = {
    "get_ota_hotel_info": {
        "description": "Dapatkan maklumat hotel, termasuk ID hotel, nama, penilaian, bintang, alamat, tag, senarai bilik",
        "preconditions": "Dalam senario pertanyaan dan tempahan hotel, perlu mendapatkan maklumat terperinci hotel",
        "postconditions": "Mengembalikan maklumat terperinci hotel, membimbing pengguna memilih bilik dan membuat pesanan",
        "args": {
            "hotel_id": "ID hotel"
        },
        "returns": "Maklumat hotel",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Dapatkan maklumat tarikan, termasuk ID tarikan, nama, alamat, deskripsi, penilaian, waktu operasi, harga tiket, senarai jenis tiket",
        "preconditions": "Dalam senario pelancongan tarikan, perlu mendapatkan maklumat terperinci tentang tarikan tersebut",
        "postconditions": "Kembalikan maklumat terperinci tentang tarikan, membimbing pengguna untuk memilih tiket dan membuat pesanan",
        "args": {
            "attraction_id": "ID tarikan"
        },
        "returns": "Maklumat tarikan",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Dapatkan maklumat penerbangan, termasuk ID penerbangan, nombor penerbangan, bandar berlepas, bandar tiba, lokasi lapangan terbang berlepas, lokasi lapangan terbang tiba, masa berlepas, masa tiba, label penerbangan, senarai jenis tempat duduk",
        "preconditions": "Dalam senario pencarian dan pembelian tiket penerbangan, perlu mendapatkan maklumat terperinci penerbangan",
        "postconditions": "Memulangkan maklumat terperinci penerbangan, membimbing pengguna memilih tempat duduk dan membuat pesanan",
        "args": {
            "flight_id": "ID penerbangan"
        },
        "returns": "Maklumat penerbangan",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Dapatkan maklumat kereta api, termasuk ID kereta api, nombor kereta api, bandar berlepas, bandar tiba, lokasi stesen berlepas, lokasi stesen tiba, masa berlepas, masa tiba, tag kereta api, senarai jenis tempat duduk",
        "preconditions": "Dalam senario pencarian dan pembelian tiket kereta api, perlu mendapatkan maklumat terperinci kereta api",
        "postconditions": "Mengembalikan maklumat terperinci kereta api, membimbing pengguna untuk memilih tempat duduk dan membuat pesanan",
        "args": {
            "train_id": "ID kereta api"
        },
        "returns": "Maklumat kereta api",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Dalam konteks perjalanan dan penginapan, berdasarkan keperluan lokasi dan keutamaan pengguna, mengesyorkan pilihan hotel yang sesuai dan menyediakan maklumat asas hotel, termasuk ID hotel, nama, penilaian, bintang, alamat, dan tag",
        "preconditions": "Pengguna meminta untuk menempah hotel dan memberikan kata kunci berkaitan hotel atau lokasi",
        "postconditions": "Memulangkan senarai hotel yang memenuhi syarat. Jika perlu melihat butiran hotel (senarai bilik, harga, dll.), alat pertanyaan butiran hotel perlu digunakan. Membimbing pengguna untuk memilih hotel",
        "args": {
            "city_name": "Nama bandar",
            "key_words": "Kata kunci carian (padanan nama hotel, pengenalan hotel, dll.)"
        },
        "returns": "Output berstruktur maklumat asas hotel",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Berdasarkan keperluan lokasi dan keutamaan pengguna, cadangkan pilihan tempat tarikan yang sesuai, sediakan maklumat asas tempat tarikan, termasuk ID tempat tarikan, nama, alamat, keterangan, penilaian, waktu operasi",
        "preconditions": "Pengguna meminta untuk menempah tempat tarikan, memberikan kata kunci atau lokasi yang berkaitan dengan tempat tarikan",
        "postconditions": "Mengembalikan senarai tempat tarikan yang memenuhi syarat, jika perlu melihat butiran tempat tarikan (senarai tiket, harga dan lain-lain) perlu menggunakan alat pertanyaan butiran tempat tarikan, pandu pengguna untuk memilih tempat tarikan",
        "args": {
            "city_name": "Nama bandar",
            "key_words": "Kata kunci carian (padankan nama tempat tarikan, lokasi, alamat, ciri-ciri dan lain-lain)"
        },
        "returns": "Output berstruktur maklumat asas tempat tarikan",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Berdasarkan keperluan lokasi dan keutamaan pengguna, mengesyorkan pilihan penerbangan yang sesuai, menyediakan maklumat asas penerbangan, termasuk ID penerbangan, nombor penerbangan, bandar berlepas, bandar tujuan, lokasi lapangan terbang berlepas, lokasi lapangan terbang tujuan, waktu berlepas, waktu tiba, label penerbangan",
        "preconditions": "Pengguna meminta untuk menempah penerbangan, memberikan kata kunci atau lokasi berkaitan penerbangan",
        "postconditions": "Memulangkan senarai penerbangan yang memenuhi syarat; jika perlu melihat butiran penerbangan (senarai jenis tempat duduk, harga, tarikh, dll.), alat pertanyaan butiran penerbangan perlu digunakan; membimbing pengguna untuk memilih penerbangan",
        "args": {
            "departure": "Bandar berlepas",
            "destination": "Bandar tujuan"
        },
        "returns": "Output berstruktur maklumat asas penerbangan",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Berdasarkan keperluan lokasi dan keutamaan pengguna, mengesyorkan pilihan kereta api yang sesuai, menyediakan maklumat asas tiket kereta api, termasuk ID kereta api, nombor kereta api, bandar berlepas, bandar tujuan, lokasi stesen berlepas, lokasi stesen tujuan, waktu berlepas, waktu kedatangan, label kereta api",
        "preconditions": "Pengguna meminta untuk menempah kereta api, memberikan kata kunci atau lokasi berkaitan kereta api",
        "postconditions": "Memulangkan senarai tiket kereta api yang memenuhi syarat, jika perlu melihat butiran tiket kereta api (senarai jenis tempat duduk, harga, tarikh, dll.) perlu menggunakan alat pertanyaan butiran tiket kereta api, membimbing pengguna untuk memilih tiket kereta api",
        "args": {
            "departure": "Bandar berlepas",
            "destination": "Bandar tujuan",
            "date": "Tarikh berlepas"
        },
        "returns": "Output berstruktur maklumat asas kereta api",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Apabila pengguna menempah hotel, sistem menjana pesanan berdasarkan keperluan pengguna (seperti nama hotel, tarikh daftar masuk, bilangan orang, dll.)",
        "preconditions": "Pengguna telah log masuk dan menyediakan identiti yang sah (user_id), pengguna menyediakan nama hotel yang sah (hotel_name) dan jenis bilik (room_type), sistem mempunyai maklumat mengenai hotel sasaran, dan hotel tersebut mempunyai bilik pada tarikh yang diminta",
        "postconditions": "Pesanan dijana, minta pengguna mengesahkan pembayaran",
        "args": {
            "hotel_id": "ID Hotel",
            "room_id": "ID Bilik",
            "user_id": "ID Pengguna"
        },
        "returns": "Output maklum balas untuk operasi penciptaan pesanan",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Pengguna membeli tiket berdasarkan tempat tarikan dan tarikh, sistem memulangkan maklumat berkaitan tiket dan membuat pesanan",
        "preconditions": "Dalam senario pelancongan tempat tarikan, pengguna meminta untuk menempah tempat tarikan dan memberikan maklumat perlu berkaitan tempahan",
        "postconditions": "Pesanan dijana, pengguna diminta mengesahkan pembayaran",
        "args": {
            "attraction_id": "ID Tempat Tarikan",
            "ticket_id": "ID Tiket",
            "user_id": "ID Pengguna",
            "date": "Tarikh lawatan, format %Y-%m-%d",
            "quantity": "Kuantiti"
        },
        "returns": "Maklum balas output untuk operasi penciptaan pesanan",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Pengguna membeli tiket penerbangan berdasarkan nombor penerbangan, tarikh, jenis tempat duduk, dan kuantiti. Sistem memulangkan maklumat berkaitan tiket penerbangan dan memproses pesanan.",
        "preconditions": "Dalam senario pertanyaan dan pembelian tiket penerbangan, pengguna meminta tempahan penerbangan dan memberikan maklumat perlu yang berkaitan dengan tempahan.",
        "postconditions": "Pesanan dijana dan pengguna diminta untuk mengesahkan pembayaran.",
        "args": {
            "flight_id": "ID Penerbangan",
            "seat_id": "ID Tempat Duduk",
            "user_id": "ID Pengguna",
            "date": "Tarikh Berlepas",
            "quantity": "Kuantiti"
        },
        "returns": "Output maklum balas bagi operasi penciptaan pesanan.",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Pengguna membeli tiket kereta api berdasarkan nombor kereta api, tarikh, jenis tempat duduk, dan kuantiti. Sistem memulangkan maklumat berkaitan tiket kereta api dan memproses pesanan.",
        "preconditions": "Dalam senario pertanyaan dan pembelian tiket kereta api, pengguna meminta untuk menempah kereta api dan telah memberikan maklumat perlu berkaitan tempahan.",
        "postconditions": "Pesanan dijana, silakan pengguna mengesahkan pembayaran.",
        "args": {
            "train_id": "ID Kereta Api",
            "seat_id": "ID Tempat Duduk",
            "user_id": "ID Pengguna",
            "date": "Tarikh Berlepas",
            "quantity": "Kuantiti"
        },
        "returns": "Output maklum balas bagi operasi penciptaan pesanan.",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Pengguna membuat pembayaran untuk pesanan hotel",
        "preconditions": "Dalam senario tempahan hotel, pengguna meminta untuk membayar pesanan hotel, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Sahkan pembayaran dan kemas kini status pesanan kepada telah dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Pengguna membuat pembayaran untuk pesanan tiket",
        "preconditions": "Dalam senario pelancongan tempat menarik, pengguna meminta pembayaran untuk pesanan tiket tempat menarik, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Sahkan pembayaran dan kemas kini status pesanan kepada dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Pengguna melakukan pembayaran pesanan tiket penerbangan",
        "preconditions": "Dalam senario pencarian dan pembelian tiket penerbangan, pengguna meminta pembayaran pesanan penerbangan, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Sahkan pembayaran dan kemas kini status pesanan kepada dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Pengguna membuat pembayaran untuk pesanan tiket kereta api",
        "preconditions": "Dalam senario pencarian dan pembelian tiket kereta api, pengguna meminta pembayaran untuk pesanan tiket kereta api, dan ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Pembayaran disahkan dan status pesanan dikemas kini kepada dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Maklumat hasil pembayaran",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Berdasarkan ID pengguna, cari pesanan hotel pengguna dan kembalikan maklumat yang merangkumi ID pesanan, jenis pesanan, ID pengguna, ID hotel, jumlah harga pesanan, masa pemesanan, masa kemaskini, dan status pesanan.",
        "preconditions": "Keperluan pengguna ialah untuk menyemak pesanan hotel.",
        "postconditions": "Maklumat pesanan dikembalikan untuk memudahkan pengubahsuaian atau pembatalan kemudian.",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tarikh",
            "status": "Status Pesanan"
        },
        "returns": "Maklumat pesanan hotel bagi pengguna yang ditentukan.",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Berdasarkan ID pengguna, semak pesanan tiket tempat menarik pengguna, mengembalikan maklumat yang merangkumi ID pesanan, jenis pesanan, ID pengguna, ID tempat menarik, jumlah harga pesanan, masa pemesanan, masa kemaskini dan status pesanan",
        "preconditions": "Keperluan pengguna adalah untuk menyemak pesanan tiket tempat menarik",
        "postconditions": "Mengembalikan maklumat pesanan, memudahkan pengubahsuaian atau pembatalan pada masa hadapan",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tarikh",
            "status": "Status Pesanan"
        },
        "returns": "Maklumat pesanan tiket tempat menarik untuk pengguna yang ditentukan",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Berdasarkan ID pengguna, semak pesanan tiket penerbangan pengguna, mengembalikan maklumat termasuk ID pesanan, jenis pesanan, ID pengguna, ID penerbangan, jumlah harga pesanan, masa pemesanan, masa kemaskini dan status pesanan",
        "preconditions": "Keperluan pengguna adalah untuk menyemak pesanan tiket penerbangan",
        "postconditions": "Mengembalikan maklumat pesanan, memudahkan pengubahsuaian atau pembatalan kemudian",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tarikh",
            "status": "Status Pesanan"
        },
        "returns": "Maklumat pesanan tiket penerbangan untuk pengguna yang ditentukan",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Berdasarkan ID pengguna, semak pesanan tiket kereta api pengguna, mengembalikan maklumat yang mengandungi ID pesanan, jenis pesanan, ID pengguna, ID kereta api, jumlah harga pesanan, masa pemesanan, masa kemaskini dan status pesanan",
        "preconditions": "Keperluan pengguna adalah untuk menyemak pesanan tiket kereta api",
        "postconditions": "Mengembalikan maklumat pesanan untuk memudahkan pengubahsuaian atau pembatalan kemudian",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tarikh",
            "status": "Status Pesanan"
        },
        "returns": "Maklumat pesanan tiket kereta api untuk pengguna tertentu",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Dapatkan butiran pesanan hotel, termasuk ID pesanan, jenis pesanan, ID pengguna, ID hotel, jumlah harga pesanan, masa pesanan, masa kemaskini, status pesanan dan butiran terperinci bilik pesanan (jenis bilik, tarikh daftar masuk, harga, ID bilik)",
        "preconditions": "Pengguna meminta untuk mendapatkan butiran pesanan hotel, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Memulangkan butiran pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Butiran pesanan",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Dapatkan butiran pesanan tiket tarikan, termasuk ID Pesanan, Jenis Pesanan, ID Pengguna, ID Tarikan, Jumlah Harga Pesanan, Masa Pesanan Dibuat, Masa Kemaskini, Status Pesanan dan maklumat terperinci tarikan pesanan (Jenis Tiket, Tarikh, Harga, ID Tiket)",
        "preconditions": "Pengguna meminta butiran pesanan tiket tarikan, ID Pesanan telah ditentukan sebelumnya",
        "postconditions": "Kembalikan butiran pesanan",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Butiran Pesanan",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Dapatkan butiran pesanan tiket penerbangan, termasuk ID pesanan, jenis pesanan, ID pengguna, ID penerbangan, jumlah harga pesanan, masa pesanan, masa kemaskini, status pesanan dan butiran terperinci tiket pesanan (jenis tempat duduk, tarikh, harga, ID tempat duduk)",
        "preconditions": "Pengguna meminta untuk mendapatkan butiran pesanan tiket penerbangan, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Memulangkan butiran pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Butiran pesanan",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Dapatkan butiran pesanan tiket kereta api, termasuk ID pesanan, jenis pesanan, ID pengguna, ID kereta api, jumlah harga pesanan, masa pesanan, masa kemaskini, status pesanan dan butiran terperinci tiket kereta api pesanan (jenis tempat duduk, tarikh, harga, ID tempat duduk)",
        "preconditions": "Pengguna meminta untuk mendapatkan butiran pesanan tiket kereta api, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Memulangkan butiran pesanan",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Butiran pesanan",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Ubah pesanan tiket kereta api, menyokong perubahan tarikh berlepas, mengendalikan secara automatik pembayaran perbezaan harga atau pemulangan wang.",
        "preconditions": "Dalam senario pertanyaan dan pembelian tiket kereta api, pengguna meminta untuk mengubah pesanan tiket kereta api, ID pesanan telah ditentukan dalam konteks sebelumnya.",
        "postconditions": "Ubah pesanan dan kemas kini status pesanan, jika perlu membayar perbezaan harga, status pesanan ditukar kepada unpaid, jika tidak kekalkan status asal, jika perlu membayar perbezaan harga, perlu membimbing pengguna untuk membayar pesanan ini.",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna",
            "new_date": "Tarikh berlepas baharu, format %Y-%m-%d"
        },
        "returns": "(Kandungan pesanan yang diubah, perbezaan harga, positif bermaksud perlu membayar perbezaan, negatif bermaksud pemulangan wang perbezaan)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Ubah pesanan tiket penerbangan, menyokong perubahan tarikh berlepas, serta mengendalikan secara automatik pembayaran tambahan atau pemulangan wang bagi perbezaan harga.",
        "preconditions": "Dalam senario pencarian dan pembelian tiket penerbangan, pengguna meminta untuk mengubah pesanan tiket penerbangan, ID pesanan telah ditentukan dalam konteks sebelumnya.",
        "postconditions": "Ubah pesanan dan kemas kini status pesanan, jika perlu membayar perbezaan harga, status pesanan ditukar kepada 'unpaid', jika tidak kekalkan status asal, jika perlu membayar perbezaan harga, perlu membimbing pengguna untuk membayar pesanan tersebut.",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna",
            "new_date": "Tarikh berlepas baharu, format %Y-%m-%d"
        },
        "returns": "(Kandungan pesanan yang diubah, perbezaan harga, positif bermaksud perlu membayar perbezaan, negatif bermaksud pemulangan perbezaan)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Pengguna membatalkan pesanan hotel yang telah ditempah.",
        "preconditions": "Dalam senario pertanyaan tempahan hotel, pengguna meminta untuk membatalkan pesanan hotel, dan ID pesanan telah ditentukan dalam konteks sebelumnya.",
        "postconditions": "Pesanan dibatalkan dan status pesanan dikemas kini. Jika terdapat bayaran balik, maklumkan kepada pengguna.",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah bayaran balik untuk pembatalan pesanan.",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Pengguna membatalkan tempahan tiket tarikan pelancongan yang telah ditempah",
        "preconditions": "ID tempahan terdapat dalam riwayat perbualan atau semakan tempahan telah dilakukan, dan pengguna mempunyai kebenaran untuk membatalkan tempahan tersebut",
        "postconditions": "Jika terdapat bayaran balik perbezaan harga, maklumkan kepada pengguna sahaja",
        "args": {
            "order_id": "ID Tempahan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah bayaran balik untuk pembatalan tempahan",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Pengguna membatalkan pesanan tiket penerbangan yang telah ditempah",
        "preconditions": "ID pesanan terdapat dalam sejarah perbualan atau pertanyaan pesanan telah dilakukan, dan pengguna mempunyai kebenaran untuk membatalkan pesanan tersebut",
        "postconditions": "Jika terdapat bayaran balik perbezaan harga, maklumkan kepada pengguna sahaja",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah bayaran balik untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Pengguna membatalkan pesanan tiket kereta api yang telah ditempah",
        "preconditions": "ID pesanan terdapat dalam sejarah perbualan atau semakan pesanan telah dilakukan sebelumnya, dan pengguna mempunyai kebenaran untuk membatalkan pesanan tersebut",
        "postconditions": "Jika terdapat bayaran balik perbezaan harga, maklumkan kepada pengguna sahaja",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah bayaran balik untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Vietnamese version
TOOL_DESCRIPTIONS_VI = {
    "get_ota_hotel_info": {
        "description": "Lấy thông tin khách sạn, bao gồm id khách sạn, tên, điểm đánh giá, xếp hạng sao, địa chỉ, nhãn, danh sách phòng",
        "preconditions": "Trong kịch bản tìm kiếm và đặt phòng khách sạn, cần lấy thông tin chi tiết của khách sạn",
        "postconditions": "Trả về thông tin chi tiết của khách sạn, hướng dẫn người dùng chọn phòng và đặt phòng",
        "args": {
            "hotel_id": "id khách sạn"
        },
        "returns": "Thông tin khách sạn",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Lấy thông tin điểm tham quan, bao gồm id điểm tham quan, tên, địa chỉ, mô tả, đánh giá, giờ mở cửa, giá vé, danh sách loại vé",
        "preconditions": "Trong ngữ cảnh du lịch điểm tham quan, cần lấy thông tin chi tiết của điểm tham quan",
        "postconditions": "Trả về thông tin chi tiết của điểm tham quan, hướng dẫn người dùng chọn vé và đặt hàng",
        "args": {
            "attraction_id": "id điểm tham quan"
        },
        "returns": "Thông tin điểm tham quan",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Lấy thông tin chuyến bay, bao gồm id chuyến bay, số hiệu chuyến bay, thành phố khởi hành, thành phố đến, vị trí sân bay khởi hành, vị trí sân bay đến, thời gian khởi hành, thời gian đến, nhãn chuyến bay, danh sách loại ghế",
        "preconditions": "Trong kịch bản tra cứu và mua vé máy bay, cần lấy thông tin chi tiết của chuyến bay",
        "postconditions": "Trả về thông tin chi tiết của chuyến bay, hướng dẫn người dùng chọn ghế và đặt hàng",
        "args": {
            "flight_id": "id chuyến bay"
        },
        "returns": "Thông tin chuyến bay",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Lấy thông tin tàu hỏa, bao gồm id tàu, số chuyến, thành phố khởi hành, thành phố đến, vị trí ga khởi hành, vị trí ga đến, thời gian khởi hành, thời gian đến, nhãn tàu, danh sách loại ghế",
        "preconditions": "Trong kịch bản tra cứu và mua vé tàu hỏa, cần lấy thông tin chi tiết của tàu",
        "postconditions": "Trả về thông tin chi tiết của tàu, hướng dẫn người dùng chọn ghế và đặt vé",
        "args": {
            "train_id": "id tàu"
        },
        "returns": "Thông tin tàu hỏa",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Trong bối cảnh du lịch và khách sạn, dựa trên nhu cầu địa điểm và sở thích của người dùng, đề xuất các tùy chọn khách sạn phù hợp, cung cấp thông tin cơ bản về khách sạn, bao gồm ID khách sạn, tên, đánh giá, xếp hạng sao, địa chỉ, nhãn.",
        "preconditions": "Người dùng yêu cầu đặt khách sạn, cung cấp từ khóa liên quan đến khách sạn hoặc địa điểm.",
        "postconditions": "Trả về danh sách khách sạn phù hợp với điều kiện, nếu cần xem chi tiết khách sạn (danh sách phòng, giá, v.v.) cần sử dụng công cụ truy vấn chi tiết khách sạn, hướng dẫn người dùng chọn khách sạn.",
        "args": {
            "city_name": "Tên thành phố",
            "key_words": "Từ khóa tìm kiếm (khớp tên khách sạn, giới thiệu khách sạn, v.v.)"
        },
        "returns": "Đầu ra có cấu trúc thông tin cơ bản về khách sạn",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Dựa trên nhu cầu về địa điểm và sở thích của người dùng, đề xuất các điểm tham quan phù hợp, cung cấp thông tin cơ bản về điểm tham quan, bao gồm id, tên, địa chỉ, mô tả, đánh giá, giờ mở cửa",
        "preconditions": "Người dùng yêu cầu đặt điểm tham quan, cung cấp từ khóa liên quan đến điểm tham quan hoặc địa điểm",
        "postconditions": "Trả về danh sách các điểm tham quan phù hợp, nếu cần xem chi tiết điểm tham quan (danh sách vé, giá cả, v.v.) cần sử dụng công cụ truy vấn chi tiết điểm tham quan, hướng dẫn người dùng lựa chọn điểm tham quan",
        "args": {
            "city_name": "Tên thành phố",
            "key_words": "Từ khóa tìm kiếm (khớp với tên điểm tham quan, vị trí, địa chỉ, đặc điểm, v.v.)"
        },
        "returns": "Đầu ra có cấu trúc thông tin cơ bản về điểm tham quan",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Dựa trên nhu cầu địa điểm và sở thích của người dùng, đề xuất các tùy chọn chuyến bay phù hợp, cung cấp thông tin cơ bản về chuyến bay, bao gồm ID chuyến bay, số hiệu chuyến bay, thành phố khởi hành, thành phố đến, vị trí sân bay khởi hành, vị trí sân bay đến, thời gian khởi hành, thời gian đến, nhãn chuyến bay",
        "preconditions": "Người dùng yêu cầu đặt chuyến bay, cung cấp các từ khóa hoặc địa điểm liên quan đến chuyến bay",
        "postconditions": "Trả về danh sách chuyến bay phù hợp. Nếu cần xem chi tiết chuyến bay (danh sách loại ghế, giá, ngày tháng, v.v.), cần sử dụng công cụ truy vấn chi tiết chuyến bay, hướng dẫn người dùng chọn chuyến bay",
        "args": {
            "departure": "Thành phố khởi hành",
            "destination": "Thành phố đích"
        },
        "returns": "Xuất thông tin cơ bản về chuyến bay dưới dạng cấu trúc",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Dựa trên nhu cầu về địa điểm và sở thích của người dùng, đề xuất các tùy chọn tàu hỏa phù hợp, cung cấp thông tin cơ bản về vé tàu, bao gồm ID tàu, số hiệu chuyến, thành phố khởi hành, thành phố đến, vị trí ga đi, vị trí ga đến, thời gian khởi hành, thời gian đến, nhãn tàu",
        "preconditions": "Người dùng yêu cầu đặt vé tàu và cung cấp các từ khóa hoặc địa điểm liên quan đến tàu hỏa",
        "postconditions": "Trả về danh sách vé tàu phù hợp với điều kiện. Nếu cần xem chi tiết vé tàu (danh sách loại ghế, giá, ngày, v.v.), cần sử dụng công cụ truy vấn chi tiết vé tàu để hướng dẫn người dùng chọn vé tàu",
        "args": {
            "departure": "Thành phố khởi hành",
            "destination": "Thành phố đến",
            "date": "Ngày khởi hành"
        },
        "returns": "Đầu ra có cấu trúc về thông tin cơ bản của tàu hỏa",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Khi người dùng đặt phòng khách sạn, hệ thống tạo đơn hàng dựa trên nhu cầu của người dùng (ví dụ: tên khách sạn, ngày nhận phòng, số lượng người, v.v.)",
        "preconditions": "Người dùng đã đăng nhập và cung cấp mã định danh hợp lệ (user_id), người dùng đã cung cấp tên khách sạn hợp lệ (hotel_name) và loại phòng (room_type), hệ thống có thông tin về khách sạn mục tiêu và khách sạn đó còn phòng trống vào ngày được yêu cầu",
        "postconditions": "Tạo đơn hàng, yêu cầu người dùng xác nhận thanh toán",
        "args": {
            "hotel_id": "ID khách sạn",
            "room_id": "ID phòng",
            "user_id": "ID người dùng"
        },
        "returns": "Đầu ra phản hồi của thao tác tạo đơn hàng",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Người dùng mua vé tham quan dựa trên địa điểm và ngày tháng, hệ thống trả về thông tin vé và tiến hành đặt hàng",
        "preconditions": "Trong ngữ cảnh du lịch tham quan, người dùng yêu cầu đặt vé tham quan và đã cung cấp các thông tin cần thiết liên quan",
        "postconditions": "Tạo đơn hàng, yêu cầu người dùng xác nhận thanh toán",
        "args": {
            "attraction_id": "ID điểm tham quan",
            "ticket_id": "ID vé",
            "user_id": "ID người dùng",
            "date": "Ngày tham quan, định dạng %Y-%m-%d",
            "quantity": "Số lượng"
        },
        "returns": "Đầu ra phản hồi của thao tác tạo đơn hàng",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Người dùng mua vé máy bay dựa trên số hiệu chuyến bay, ngày tháng, loại ghế và số lượng; hệ thống trả về thông tin liên quan đến vé và tiến hành đặt hàng",
        "preconditions": "Trong kịch bản tìm kiếm và mua vé máy bay, người dùng yêu cầu đặt chỗ chuyến bay và đã cung cấp các thông tin cần thiết liên quan",
        "postconditions": "Đơn hàng được tạo, yêu cầu người dùng xác nhận thanh toán",
        "args": {
            "flight_id": "ID chuyến bay",
            "seat_id": "ID ghế ngồi",
            "user_id": "ID người dùng",
            "date": "Ngày khởi hành",
            "quantity": "Số lượng"
        },
        "returns": "Kết quả phản hồi từ thao tác tạo đơn hàng",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Người dùng mua vé tàu hỏa theo chuyến, ngày, loại ghế và số lượng, hệ thống trả về thông tin vé tương ứng và tiến hành đặt hàng",
        "preconditions": "Trong kịch bản tra cứu và mua vé tàu hỏa, người dùng yêu cầu đặt vé tàu và đã cung cấp các thông tin cần thiết liên quan đến việc đặt chỗ",
        "postconditions": "Tạo đơn hàng, yêu cầu người dùng xác nhận thanh toán",
        "args": {
            "train_id": "ID tàu hỏa",
            "seat_id": "ID ghế ngồi",
            "user_id": "ID người dùng",
            "date": "Ngày khởi hành",
            "quantity": "Số lượng"
        },
        "returns": "Kết quả phản hồi của thao tác tạo đơn hàng",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Người dùng thực hiện thanh toán đơn đặt phòng khách sạn",
        "preconditions": "Trong kịch bản tìm kiếm và đặt phòng khách sạn, người dùng yêu cầu thanh toán đơn đặt phòng, ID đơn hàng đã được xác định ở ngữ cảnh trước",
        "postconditions": "Xác nhận thanh toán và cập nhật trạng thái đơn hàng thành đã thanh toán",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Người dùng thực hiện thanh toán đơn hàng vé",
        "preconditions": "Trong kịch bản du lịch tham quan, người dùng yêu cầu thanh toán đơn hàng vé tham quan, ID đơn hàng đã được xác định ở ngữ cảnh trước",
        "postconditions": "Xác nhận thanh toán và cập nhật trạng thái đơn hàng thành đã thanh toán",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Người dùng thực hiện thanh toán đơn đặt vé máy bay",
        "preconditions": "Trong kịch bản tìm kiếm và mua vé máy bay, người dùng yêu cầu thanh toán đơn hàng chuyến bay, ID đơn hàng đã được xác định trước đó",
        "postconditions": "Xác nhận thanh toán và cập nhật trạng thái đơn hàng thành đã thanh toán",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Người dùng thực hiện thanh toán đơn hàng vé tàu hỏa",
        "preconditions": "Trong ngữ cảnh tìm kiếm và mua vé tàu hỏa, người dùng yêu cầu thanh toán đơn hàng vé tàu hỏa, ID đơn hàng đã được xác định ở trên",
        "postconditions": "Xác nhận thanh toán và cập nhật trạng thái đơn hàng thành đã thanh toán",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Thông tin kết quả thanh toán",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Dựa trên ID người dùng, truy vấn đơn đặt phòng khách sạn của người dùng, trả về thông tin bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID khách sạn, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật và trạng thái đơn hàng",
        "preconditions": "Nhu cầu của người dùng là truy vấn đơn đặt phòng khách sạn",
        "postconditions": "Trả về thông tin đơn hàng, thuận tiện cho việc chỉnh sửa/hủy sau này",
        "args": {
            "user_id": "ID người dùng",
            "date": "Ngày",
            "status": "Trạng thái đơn hàng"
        },
        "returns": "Thông tin đơn đặt phòng khách sạn của người dùng được chỉ định",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Dựa trên ID người dùng, truy vấn đơn đặt vé tham quan của người dùng, trả về bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID điểm tham quan, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật và trạng thái đơn hàng",
        "preconditions": "Nhu cầu của người dùng là truy vấn đơn đặt vé tham quan",
        "postconditions": "Trả về thông tin đơn hàng, thuận tiện cho việc sửa/hủy sau này",
        "args": {
            "user_id": "ID người dùng",
            "date": "Ngày",
            "status": "Trạng thái đơn hàng"
        },
        "returns": "Thông tin đơn đặt vé tham quan của người dùng được chỉ định",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Dựa trên ID người dùng, truy vấn đơn đặt vé máy bay của người dùng, trả về bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID chuyến bay, tổng tiền đơn hàng, thời gian đặt hàng, thời gian cập nhật và trạng thái đơn hàng",
        "preconditions": "Nhu cầu của người dùng là truy vấn đơn đặt vé máy bay",
        "postconditions": "Trả về thông tin đơn hàng, thuận tiện cho việc chỉnh sửa/hủy bỏ sau này",
        "args": {
            "user_id": "ID người dùng",
            "date": "Ngày",
            "status": "Trạng thái đơn hàng"
        },
        "returns": "Thông tin đơn đặt vé máy bay của người dùng được chỉ định",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Dựa trên ID người dùng, truy vấn đơn đặt vé tàu hỏa của người dùng, trả về bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID tàu hỏa, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật và trạng thái đơn hàng",
        "preconditions": "Nhu cầu của người dùng là truy vấn đơn đặt vé tàu hỏa",
        "postconditions": "Trả về thông tin đơn hàng, thuận tiện cho việc sửa đổi/hủy bỏ sau này",
        "args": {
            "user_id": "ID người dùng",
            "date": "Ngày",
            "status": "Trạng thái đơn hàng"
        },
        "returns": "Thông tin đơn đặt vé tàu hỏa của người dùng được chỉ định",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Lấy chi tiết đơn đặt phòng khách sạn, bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID khách sạn, tổng giá trị đơn hàng, thời gian đặt, thời gian cập nhật, trạng thái đơn hàng và thông tin chi tiết phòng trong đơn hàng (loại phòng, ngày nhận phòng, giá, ID phòng)",
        "preconditions": "Người dùng yêu cầu lấy chi tiết đơn đặt phòng khách sạn, ID đơn hàng đã được xác định trong ngữ cảnh trước",
        "postconditions": "Trả về chi tiết đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Chi tiết đơn hàng",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Lấy chi tiết đơn hàng vé tham quan điểm du lịch, bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID điểm du lịch, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và thông tin chi tiết điểm du lịch của đơn hàng (loại vé, ngày, giá, ID vé)",
        "preconditions": "Người dùng yêu cầu lấy chi tiết đơn hàng vé tham quan điểm du lịch, ID đơn hàng đã được xác định ở phần trước",
        "postconditions": "Trả về chi tiết đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Chi tiết đơn hàng",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Lấy chi tiết đơn đặt hàng vé máy bay, bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID chuyến bay, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và thông tin chi tiết vé máy bay của đơn hàng (loại ghế, ngày, giá, ID ghế)",
        "preconditions": "Người dùng yêu cầu lấy chi tiết đơn đặt hàng vé máy bay, ID đơn hàng đã được xác định trước đó",
        "postconditions": "Trả về chi tiết đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Chi tiết đơn hàng",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Lấy chi tiết đơn đặt hàng vé tàu hỏa, bao gồm ID đơn hàng, loại đơn hàng, ID người dùng, ID tàu hỏa, tổng giá trị đơn hàng, thời gian đặt hàng, thời gian cập nhật, trạng thái đơn hàng và thông tin chi tiết vé tàu hỏa của đơn hàng (loại ghế, ngày, giá, ID ghế)",
        "preconditions": "Người dùng yêu cầu lấy chi tiết đơn đặt hàng vé tàu hỏa, ID đơn hàng đã được xác định trong ngữ cảnh trước",
        "postconditions": "Trả về chi tiết đơn hàng",
        "args": {
            "order_id": "ID đơn hàng"
        },
        "returns": "Chi tiết đơn hàng",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Sửa đổi đơn đặt vé tàu hỏa, hỗ trợ thay đổi ngày khởi hành, tự động xử lý khoản chênh lệch cần trả thêm hoặc hoàn lại.",
        "preconditions": "Trong ngữ cảnh tìm kiếm và mua vé tàu hỏa, người dùng yêu cầu sửa đổi đơn vé tàu hỏa, ID đơn hàng đã được xác định ở trên.",
        "postconditions": "Sửa đổi đơn hàng và cập nhật trạng thái đơn hàng, nếu cần trả thêm chênh lệch, trạng thái đơn hàng chuyển thành unpaid, nếu không thì giữ nguyên trạng thái cũ; nếu cần trả thêm chênh lệch, cần hướng dẫn người dùng thanh toán đơn hàng này.",
        "args": {
            "order_id": "ID đơn hàng",
            "user_id": "ID người dùng",
            "new_date": "Ngày khởi hành mới, định dạng %Y-%m-%d"
        },
        "returns": "(Nội dung đơn hàng đã sửa đổi, khoản chênh lệch, dương là cần trả thêm, âm là được hoàn lại)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Sửa đổi đơn đặt vé máy bay, hỗ trợ thay đổi ngày khởi hành, tự động xử lý việc bù hoặc hoàn chênh lệch.",
        "preconditions": "Trong ngữ cảnh tìm kiếm và mua vé máy bay, người dùng yêu cầu sửa đổi đơn đặt vé máy bay, ID đơn hàng đã được xác định ở trên.",
        "postconditions": "Sửa đổi đơn hàng và cập nhật trạng thái đơn hàng, nếu cần bù chênh lệch, trạng thái đơn hàng đổi thành unpaid, nếu không giữ nguyên trạng thái cũ, nếu cần bù chênh lệch, cần hướng dẫn người dùng thanh toán đơn hàng này.",
        "args": {
            "order_id": "ID đơn hàng",
            "user_id": "ID người dùng",
            "new_date": "Ngày khởi hành mới, định dạng %Y-%m-%d"
        },
        "returns": "(Nội dung đơn hàng đã sửa đổi, khoản chênh lệch, dương là cần bù chênh lệch, âm là hoàn chênh lệch)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Người dùng hủy đơn đặt phòng khách sạn đã đặt trước",
        "preconditions": "Trong kịch bản tra cứu đặt phòng khách sạn, người dùng yêu cầu hủy đơn đặt phòng khách sạn, ID đơn hàng đã được xác định ở ngữ cảnh trước",
        "postconditions": "Hủy đơn hàng và cập nhật trạng thái đơn hàng, nếu cần hoàn lại số tiền chênh lệch, chỉ cần thông báo cho người dùng",
        "args": {
            "order_id": "ID đơn hàng",
            "user_id": "ID người dùng"
        },
        "returns": "Số tiền hoàn lại khi hủy đơn hàng",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Người dùng hủy đơn đặt vé tham quan đã được đặt trước",
        "preconditions": "Có ID đơn hàng trong lịch sử trò chuyện hoặc đã thực hiện truy vấn đơn hàng, người dùng có quyền hủy đơn hàng này",
        "postconditions": "Nếu có hoàn lại số tiền chênh lệch, chỉ cần thông báo cho người dùng",
        "args": {
            "order_id": "ID đơn hàng",
            "user_id": "ID người dùng"
        },
        "returns": "Số tiền hoàn lại khi hủy đơn hàng",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Người dùng hủy đơn đặt vé máy bay đã đặt trước",
        "preconditions": "Có mã đơn hàng trong lịch sử trò chuyện hoặc đã thực hiện tra cứu đơn hàng, người dùng có quyền hủy đơn hàng này",
        "postconditions": "Nếu có hoàn lại chênh lệch giá, chỉ cần thông báo cho người dùng",
        "args": {
            "order_id": "Mã đơn hàng",
            "user_id": "ID người dùng"
        },
        "returns": "Số tiền hoàn lại khi hủy đơn hàng",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Người dùng hủy đơn đặt vé tàu hỏa đã đặt trước",
        "preconditions": "Trong lịch sử hội thoại có ID đơn hàng hoặc đã thực hiện tra cứu đơn hàng, người dùng có quyền hủy đơn hàng này",
        "postconditions": "Nếu có hoàn lại chênh lệch, chỉ cần thông báo cho người dùng",
        "args": {
            "order_id": "ID đơn hàng",
            "user_id": "ID người dùng"
        },
        "returns": "Số tiền hoàn lại khi hủy đơn hàng",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Turkish version
TOOL_DESCRIPTIONS_TR = {
    "get_ota_hotel_info": {
        "description": "Otel bilgilerini getirir; otel kimliği, adı, puanı, yıldız derecesi, adresi, etiketleri ve oda listesini içerir.",
        "preconditions": "Otel sorgulama ve rezervasyon senaryosunda otelin ayrıntılı bilgilerinin alınması gerektiğinde.",
        "postconditions": "Otelin ayrıntılı bilgilerini döndürür ve kullanıcıyı oda seçip sipariş vermeye yönlendirir.",
        "args": {
            "hotel_id": "Otel kimliği"
        },
        "returns": "Otel bilgileri",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Turistik nokta bilgilerini alın; nokta id'si, adı, adresi, açıklaması, puanı, açık olduğu saatler, bilet fiyatı ve bilet türü listesini içerir.",
        "preconditions": "Turistik nokta ziyareti senaryosunda, noktanın ayrıntılı bilgilerini almak gerektiğinde.",
        "postconditions": "Turistik noktanın ayrıntılı bilgilerini döndürür, kullanıcıyı bilet seçmeye ve sipariş vermeye yönlendirir.",
        "args": {
            "attraction_id": "Turistik nokta id'si"
        },
        "returns": "Turistik nokta bilgileri",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Uçuş bilgilerini getirir; uçuş kimliği, uçuş numarası, kalkış şehri, varış şehri, kalkış havalimanı konumu, varış havalimanı konumu, kalkış zamanı, varış zamanı, uçuş etiketleri ve koltuk tipi listesini içerir.",
        "preconditions": "Uçak bileti sorgulama ve satın alma senaryosunda, uçuşun ayrıntılı bilgilerini almak gerekir.",
        "postconditions": "Uçuşun ayrıntılı bilgilerini döndürür, kullanıcıyı koltuk seçmeye ve sipariş vermeye yönlendirir.",
        "args": {
            "flight_id": "Uçuş kimliği"
        },
        "returns": "Uçuş bilgileri",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Tren bilgilerini alır; tren kimliği, sefer numarası, kalkış şehri, varış şehri, kalkış istasyonu konumu, varış istasyonu konumu, kalkış saati, varış saati, tren etiketleri ve koltuk tipi listesini içerir.",
        "preconditions": "Tren bileti sorgulama ve satın alma senaryosunda, trenin ayrıntılı bilgilerine ihtiyaç duyulduğunda.",
        "postconditions": "Trenin ayrıntılı bilgilerini döndürür, kullanıcıyı koltuk seçmeye ve sipariş vermeye yönlendirir.",
        "args": {
            "train_id": "Tren kimliği"
        },
        "returns": "Tren bilgileri",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Otel ve seyahat senaryosunda, kullanıcının konum ihtiyaçlarına ve tercihlerine dayanarak uygun otel seçeneklerini önerir, otel kimliği, adı, puanı, yıldız sayısı, adresi ve etiketleri dahil olmak üzere otelin temel bilgilerini sağlar.",
        "preconditions": "Kullanıcı otel rezervasyonu talep eder, otel ile ilgili anahtar kelimeler veya konum bilgisi verir.",
        "postconditions": "Koşulları sağlayan otel listesini döndürür, otel detaylarını (oda listesi, fiyatlar vb.) görüntülemek gerekirse otel detay sorgulama aracı kullanılmalıdır, kullanıcıyı otel seçmeye yönlendirir.",
        "args": {
            "city_name": "Şehir adı",
            "key_words": "Arama anahtar kelimeleri (otel adı, otel tanıtımı vb. ile eşleşir)"
        },
        "returns": "Otel temel bilgilerinin yapılandırılmış çıktısı",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Kullanıcının konum ihtiyaçlarına ve tercihlerine dayanarak uygun turistik yerler önerir, turistik yer kimliği, adı, adresi, açıklaması, puanı, açılış saatleri gibi temel bilgileri sağlar.",
        "preconditions": "Kullanıcı bir turistik yer rezervasyonu talep eder ve turistik yerle ilgili anahtar kelimeler veya konumlar belirtir.",
        "postconditions": "Koşulları sağlayan turistik yerlerin listesini döndürür, turistik yer detaylarını (bilet listesi, fiyatlar vb.) görüntülemek gerekirse turistik yer detay sorgulama aracını kullanmak gerekir, kullanıcıyı turistik yer seçmeye yönlendirir.",
        "args": {
            "city_name": "Şehir adı",
            "key_words": "Arama anahtar kelimeleri (turistik yer adı, konum, adres, özellikler vb. ile eşleşir)"
        },
        "returns": "Turistik yer temel bilgilerinin yapılandırılmış çıktısı",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Kullanıcının konum ihtiyaçlarına ve tercihlerine dayanarak uygun uçuş seçeneklerini önerir; uçuş kimliği, uçuş numarası, kalkış şehri, varış şehri, kalkış havalimanı konumu, varış havalimanı konumu, kalkış zamanı, varış zamanı ve uçuş etiketleri dahil olmak üzere uçuşun temel bilgilerini sağlar",
        "preconditions": "Kullanıcı uçuş rezervasyonu talep eder ve uçuşla ilgili anahtar kelimeler veya konumlar belirtir",
        "postconditions": "Koşulları karşılayan uçuş listesini döndürür, uçuş detaylarını (koltuk tipi listesi, fiyat, tarih vb.) görüntülemek gerekirse uçuş detay sorgulama aracını kullanmanız gerekir, kullanıcıyı uçuş seçmeye yönlendirir",
        "args": {
            "departure": "Kalkış şehri",
            "destination": "Varış şehri"
        },
        "returns": "Uçuş temel bilgilerinin yapılandırılmış çıktısı",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Kullanıcının konum ihtiyaçlarına ve tercihlerine dayanarak uygun tren seçeneklerini önerir, tren bileti temel bilgilerini sağlar; tren kimliği, tren numarası, kalkış şehri, varış şehri, kalkış istasyonu konumu, varış istasyonu konumu, kalkış zamanı, varış zamanı ve tren etiketlerini içerir.",
        "preconditions": "Kullanıcı tren rezervasyonu talep eder ve trenle ilgili anahtar kelimeler veya konumlar verir.",
        "postconditions": "Koşulları karşılayan tren bileti listesini döndürür; tren bileti ayrıntılarını (koltuk tipi listesi, fiyat, tarih vb.) görüntülemek gerekirse tren bileti ayrıntı sorgulama aracını kullanın ve kullanıcıyı tren bileti seçmeye yönlendirin.",
        "args": {
            "departure": "Kalkış şehri",
            "destination": "Varış şehri",
            "date": "Kalkış tarihi"
        },
        "returns": "Tren temel bilgilerinin yapılandırılmış çıktısı",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Kullanıcı otel rezervasyonu yaptığında, sistem kullanıcının ihtiyaçlarına (otel adı, giriş tarihi, kişi sayısı vb.) göre sipariş oluşturur.",
        "preconditions": "Kullanıcı oturum açmış ve geçerli bir kimlik sağlamıştır (user_id), kullanıcı geçerli bir otel adı (hotel_name) ve oda tipi (room_type) sağlamıştır, sistem hedef otel hakkında bilgiye sahiptir ve ilgili otel talep edilen tarihlerde oda bulunmaktadır.",
        "postconditions": "Sipariş oluşturulur, kullanıcıdan ödemeyi onaylaması istenir.",
        "args": {
            "hotel_id": "Otel Kimliği",
            "room_id": "Oda Kimliği",
            "user_id": "Kullanıcı Kimliği"
        },
        "returns": "Sipariş oluşturma işleminin geri bildirim çıktısı.",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Kullanıcı, turistik noktaya ve tarihe göre bilet satın alır; sistem biletle ilgili bilgileri döndürür ve sipariş oluşturur.",
        "preconditions": "Turistik nokta gezisi senaryosunda, kullanıcı turistik nokta rezervasyonu talep eder ve rezervasyonla ilgili gerekli bilgileri sağlar.",
        "postconditions": "Sipariş oluşturulur, kullanıcıdan ödemeyi onaylaması istenir.",
        "args": {
            "attraction_id": "Turistik nokta kimliği",
            "ticket_id": "Bilet kimliği",
            "user_id": "Kullanıcı kimliği",
            "date": "Ziyaret tarihi, biçimi %Y-%m-%d",
            "quantity": "Adet"
        },
        "returns": "Sipariş oluşturma işleminin geri bildirim çıktısı",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Kullanıcı uçuş numarası, tarih, koltuk tipi ve adede göre uçak bileti satın alır; sistem bilet bilgilerini döndürür ve siparişi oluşturur.",
        "preconditions": "Uçak bileti sorgulama ve satın alma senaryosunda, kullanıcı uçuş rezervasyonu talep eder ve rezervasyon için gerekli bilgileri sağlar.",
        "postconditions": "Sipariş oluşturulur, kullanıcıdan ödemeyi onaylaması istenir.",
        "args": {
            "flight_id": "Uçuş Kimliği",
            "seat_id": "Koltuk Kimliği",
            "user_id": "Kullanıcı Kimliği",
            "date": "Kalkış Tarihi",
            "quantity": "Adet"
        },
        "returns": "Sipariş oluşturma işleminin geri bildirim çıktısı",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Kullanıcı tren numarası, tarih, koltuk tipi ve adete göre tren bileti satın alır; sistem tren bileti ile ilgili bilgileri döndürür ve siparişi oluşturur.",
        "preconditions": "Tren bileti sorgulama ve satın alma senaryosunda, kullanıcı tren rezervasyonu talep eder ve rezervasyonla ilgili gerekli bilgileri sağlar.",
        "postconditions": "Sipariş oluşturulur, kullanıcıdan ödemeyi onaylaması istenir.",
        "args": {
            "train_id": "Tren Kimliği",
            "seat_id": "Koltuk Kimliği",
            "user_id": "Kullanıcı Kimliği",
            "date": "Hareket Tarihi",
            "quantity": "Adet"
        },
        "returns": "Sipariş oluşturma işleminin geri bildirim çıktısı",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Kullanıcı otel sipariş ödemesini gerçekleştirir",
        "preconditions": "Otel sorgulama ve rezervasyon senaryosunda, kullanıcı otel siparişini ödemeyi talep eder ve önceki bağlamda sipariş kimliği belirlenmiştir.",
        "postconditions": "Ödeme onaylanır ve sipariş durumu 'ödendi' olarak güncellenir.",
        "args": {
            "order_id": "Sipariş Kimliği"
        },
        "returns": "Ödeme sonucu bilgisi",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Kullanıcı bilet siparişi ödemesini gerçekleştirir",
        "preconditions": "Turistik gezi senaryosunda, kullanıcı gezi bileti siparişinin ödemesini talep eder ve önceki bağlamda sipariş kimliği belirlenmiştir",
        "postconditions": "Ödemeyi onayla ve sipariş durumunu ödendi olarak güncelle",
        "args": {
            "order_id": "Sipariş Kimliği"
        },
        "returns": "Ödeme sonucu bilgisi",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Kullanıcı uçak bileti siparişinin ödemesini yapar",
        "preconditions": "Uçak bileti sorgulama ve satın alma senaryosunda, kullanıcı uçuş siparişinin ödemesini talep eder ve önceki bağlamda sipariş ID'si belirlenmiştir",
        "postconditions": "Ödeme onaylanır ve sipariş durumu ödenmiş olarak güncellenir",
        "args": {
            "order_id": "Sipariş ID'si"
        },
        "returns": "Ödeme sonuç bilgisi",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Kullanıcı tren bileti sipariş ödemesini gerçekleştirir",
        "preconditions": "Tren bileti sorgulama ve satın alma senaryosunda, kullanıcı tren bileti siparişinin ödenmesini talep eder ve önceki bağlamda sipariş kimliği belirlenmiştir",
        "postconditions": "Ödeme onaylanır ve sipariş durumu ödenmiş olarak güncellenir",
        "args": {
            "order_id": "Sipariş Kimliği"
        },
        "returns": "Ödeme sonucu bilgisi",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Kullanıcı Kimliği'ne göre kullanıcının otel siparişlerini sorgular ve Sipariş Kimliği, Sipariş Türü, Kullanıcı Kimliği, Otel Kimliği, Sipariş Toplam Tutarı, Sipariş Veriliş Zamanı, Güncelleme Zamanı ve Sipariş Durumu'nu içeren sonuçları döndürür.",
        "preconditions": "Kullanıcının ihtiyacı otel siparişlerini sorgulamaktır.",
        "postconditions": "Sipariş bilgilerini döndürür, böylece daha sonra değiştirme/iptal etme kolaylaşır.",
        "args": {
            "user_id": "Kullanıcı Kimliği",
            "date": "Tarih",
            "status": "Sipariş Durumu"
        },
        "returns": "Belirtilen kullanıcının otel sipariş bilgileri",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Kullanıcı ID'sine göre kullanıcının gezi yeri bileti siparişlerini sorgular; sipariş ID'si, sipariş türü, kullanıcı ID'si, gezi yeri ID'si, sipariş toplam tutarı, sipariş verme zamanı, güncelleme zamanı ve sipariş durumunu içeren sonuçları döndürür.",
        "preconditions": "Kullanıcının ihtiyacı gezi yeri bileti siparişlerini sorgulamaktır.",
        "postconditions": "Sipariş bilgilerini döndürür, böylece daha sonra değiştirme/iptal etme kolaylaşır.",
        "args": {
            "user_id": "Kullanıcı ID'si",
            "date": "Tarih",
            "status": "Sipariş Durumu"
        },
        "returns": "Belirtilen kullanıcının gezi yeri bileti sipariş bilgileri.",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Kullanıcı Kimliği'ne göre kullanıcının uçak bileti siparişlerini sorgular; Sipariş Kimliği, Sipariş Türü, Kullanıcı Kimliği, Uçuş Kimliği, Sipariş Toplam Tutarı, Sipariş Verme Zamanı, Güncelleme Zamanı ve Sipariş Durumu içeren sonuçları döndürür.",
        "preconditions": "Kullanıcının ihtiyacı uçak bileti siparişlerini sorgulamaktır",
        "postconditions": "Sipariş bilgilerini döndürür, böylece daha sonra değiştirme/iptal etme kolaylaşır",
        "args": {
            "user_id": "Kullanıcı Kimliği",
            "date": "Tarih",
            "status": "Sipariş Durumu"
        },
        "returns": "Belirtilen kullanıcının uçak bileti sipariş bilgileri",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Kullanıcı ID'sine göre kullanıcının tren bileti siparişlerini sorgular; sipariş ID'si, sipariş tipi, kullanıcı ID'si, tren ID'si, sipariş toplam tutarı, sipariş verme zamanı, güncelleme zamanı ve sipariş durumunu içeren sonuçları döndürür.",
        "preconditions": "Kullanıcının ihtiyacı tren bileti siparişlerini sorgulamaktır.",
        "postconditions": "Sipariş bilgilerini döndürür, böylece daha sonra düzenleme/iptal etme işlemi kolaylaşır.",
        "args": {
            "user_id": "Kullanıcı ID'si",
            "date": "Tarih",
            "status": "Sipariş Durumu"
        },
        "returns": "Belirtilen kullanıcının tren bileti sipariş bilgileri",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Otel sipariş detaylarını getirir; sipariş ID'si, sipariş türü, kullanıcı ID'si, otel ID'si, toplam sipariş tutarı, sipariş zamanı, güncelleme zamanı, sipariş durumu ve sipariş oda detayları (oda türü, giriş tarihi, fiyat, oda ID'si) içerir.",
        "preconditions": "Kullanıcı otel sipariş detaylarını talep eder, önceki bağlamda sipariş ID'si belirlenmiştir.",
        "postconditions": "Sipariş detaylarını döndürür.",
        "args": {
            "order_id": "Sipariş ID'si"
        },
        "returns": "Sipariş detayları",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Sipariş ID, sipariş türü, kullanıcı ID, gezilecek yer ID, sipariş toplam tutarı, sipariş zamanı, güncelleme zamanı, sipariş durumu ve sipariş gezilecek yer detaylı bilgilerini (bilet türü, tarih, fiyat, bilet ID) içeren gezilecek yer bilet sipariş detaylarını alın.",
        "preconditions": "Kullanıcı gezilecek yer bilet sipariş detaylarını talep eder, önceki bağlamda sipariş ID belirlenmiştir.",
        "postconditions": "Sipariş detaylarını döndürür.",
        "args": {
            "order_id": "Sipariş ID"
        },
        "returns": "Sipariş detayları",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Sipariş ID'si, sipariş türü, kullanıcı ID'si, uçuş ID'si, toplam sipariş tutarı, sipariş zamanı, güncelleme zamanı, sipariş durumu ve bilet detayları (koltuk tipi, tarih, fiyat, koltuk ID'si) dahil olmak üzere uçak bileti sipariş detaylarını getirir.",
        "preconditions": "Kullanıcı uçak bileti sipariş detaylarını talep eder ve önceki bağlamda sipariş ID'si belirlenmiştir.",
        "postconditions": "Sipariş detayları döndürülür.",
        "args": {
            "order_id": "Sipariş ID'si"
        },
        "returns": "Sipariş detayları",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Tren bileti sipariş detaylarını getirir; sipariş ID'si, sipariş türü, kullanıcı ID'si, tren ID'si, sipariş toplam tutarı, sipariş zamanı, güncelleme zamanı, sipariş durumu ve sipariş tren bileti detaylı bilgileri (koltuk tipi, tarih, fiyat, koltuk ID'si) içerir.",
        "preconditions": "Kullanıcı tren bileti sipariş detaylarını talep eder, önceki bağlamda sipariş ID'si belirlenmiştir.",
        "postconditions": "Sipariş detayları döndürülür.",
        "args": {
            "order_id": "Sipariş ID'si"
        },
        "returns": "Sipariş detayları",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Tren bileti siparişini değiştirir, kalkış tarihini değiştirmeyi destekler, fiyat farkı ödemesi veya iadesini otomatik olarak işler.",
        "preconditions": "Tren bileti sorgulama ve satın alma senaryosunda, kullanıcı tren bileti siparişini değiştirmeyi talep eder, önceki bağlamda sipariş ID'si belirlenmiştir.",
        "postconditions": "Siparişi değiştirir ve sipariş durumunu günceller, eğer fiyat farkı ödenmesi gerekiyorsa, sipariş durumu unpaid olarak değiştirilir, aksi takdirde mevcut durum korunur, eğer fiyat farkı ödenmesi gerekiyorsa, kullanıcı bu siparişi ödemeye yönlendirilmelidir.",
        "args": {
            "order_id": "Sipariş ID'si",
            "user_id": "Kullanıcı ID'si",
            "new_date": "Yeni kalkış tarihi, formatı %Y-%m-%d"
        },
        "returns": "(Değiştirilen sipariş içeriği, fiyat farkı, pozitif ise fark ödenmesi gerekir, negatif ise fark iadesi yapılır)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Uçak bileti siparişini değiştirir, kalkış tarihini değiştirmeye olanak tanır ve fiyat farkı tahsilatını veya iadesini otomatik olarak yönetir.",
        "preconditions": "Uçak bileti sorgulama ve satın alma senaryosunda, kullanıcı bir uçak bileti siparişini değiştirmeyi talep eder ve önceki adımlarda sipariş ID'si belirlenmiştir.",
        "postconditions": "Sipariş değiştirilir ve durum güncellenir. Ek ödeme gerekirse durum 'unpaid' olarak değişir, aksi halde mevcut durum korunur. Ek ödeme gerekirse, kullanıcı ilgili siparişi ödemeye yönlendirilir.",
        "args": {
            "order_id": "Sipariş ID'si",
            "user_id": "Kullanıcı ID'si",
            "new_date": "Yeni kalkış tarihi, format: %Y-%m-%d"
        },
        "returns": "(Değiştirilen sipariş içeriği, fiyat farkı; pozitif değer ek ödeme gerektiğini, negatif değer iade olduğunu gösterir)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Kullanıcının önceden rezerve ettiği otel siparişini iptal eder",
        "preconditions": "Otel rezervasyon sorgulama senaryosunda kullanıcı otel siparişini iptal etmeyi talep eder ve önceki bağlamda sipariş kimliği belirlenmiştir",
        "postconditions": "Sipariş iptal edilir ve durum güncellenir; eğer fiyat farkı iadesi gerekirse kullanıcı bilgilendirilir",
        "args": {
            "order_id": "Sipariş Kimliği",
            "user_id": "Kullanıcı Kimliği"
        },
        "returns": "İptal edilen siparişin iade tutarı",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Kullanıcının önceden rezerve edilmiş gezi bileti siparişini iptal etmesi",
        "preconditions": "Geçmiş konuşmada sipariş kimliği bulunmalı veya daha önce sipariş sorgusu yapılmış olmalı; kullanıcının bu siparişi iptal etme yetkisi olmalıdır",
        "postconditions": "Eğer fiyat farkı iadesi varsa, kullanıcıya bildirilmesi yeterlidir",
        "args": {
            "order_id": "Sipariş Kimliği",
            "user_id": "Kullanıcı Kimliği"
        },
        "returns": "Sipariş iptali için iade edilen tutar",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Kullanıcının önceden rezerve edilmiş uçak bileti siparişini iptal etmesi",
        "preconditions": "Geçmiş konuşmada sipariş ID'si bulunmalı veya daha önce sipariş sorgusu yapılmış olmalı ve kullanıcının bu siparişi iptal etme yetkisi olmalıdır",
        "postconditions": "Eğer fiyat farkı iadesi söz konusuysa, kullanıcıya bilgi verilmelidir",
        "args": {
            "order_id": "Sipariş ID'si",
            "user_id": "Kullanıcı ID'si"
        },
        "returns": "Sipariş iptali için iade edilen tutar",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Kullanıcının önceden rezerve edilmiş tren bileti siparişini iptal etmesi",
        "preconditions": "Geçmiş konuşmada sipariş kimliği bulunmalı veya daha önce sipariş sorgusu yapılmış olmalıdır; kullanıcının bu siparişi iptal etme yetkisi olmalıdır",
        "postconditions": "Eğer fiyat farkı iadesi söz konusuysa, kullanıcıya bilgi verilmesi yeterlidir",
        "args": {
            "order_id": "Sipariş Kimliği",
            "user_id": "Kullanıcı Kimliği"
        },
        "returns": "Sipariş iptali için iade edilen tutar",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Hebrew version
TOOL_DESCRIPTIONS_HE = {
    "get_ota_hotel_info": {
        "description": "קבלת פרטי המלון, כולל מזהה המלון, שם, דירוג, דירוג כוכבים, כתובת, תגיות ורשימת החדרים",
        "preconditions": "בתרחיש חיפוש והזמנת מלון, נדרש לקבל את פרטי המלון המפורטים",
        "postconditions": "מחזיר את פרטי המלון המפורטים, ומנחה את המשתמש לבחור חדר ולהשלים את ההזמנה",
        "args": {
            "hotel_id": "מזהה המלון"
        },
        "returns": "מידע על המלון",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "קבלת מידע על אטרקציה, הכולל מזהה אטרקציה, שם, כתובת, תיאור, דירוג, שעות פעילות, מחיר כרטיס ורשימת סוגי כרטיסים",
        "preconditions": "בתרחיש ביקור באטרקציה, כאשר נדרש לקבל מידע מפורט על האטרקציה",
        "postconditions": "מחזיר מידע מפורט על האטרקציה, ומנחה את המשתמש לבחור כרטיס ולהשלים הזמנה",
        "args": {
            "attraction_id": "מזהה האטרקציה"
        },
        "returns": "מידע על האטרקציה",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "קבלת מידע על טיסה, כולל מזהה טיסה, מספר טיסה, עיר מוצא, עיר יעד, מיקום שדה התעופה במוצא, מיקום שדה התעופה ביעד, זמן המראה, זמן נחיתה, תגיות טיסה, רשימת סוגי מושבים",
        "preconditions": "בתרחיש של חיפוש ורכישת כרטיסי טיסה, נדרש לקבל מידע מפורט על הטיסה",
        "postconditions": "מחזיר מידע מפורט על הטיסה, מנחה את המשתמש לבחור מושב ולהזמין",
        "args": {
            "flight_id": "מזהה טיסה"
        },
        "returns": "מידע על טיסה",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "קבלת מידע על הרכבת, כולל מזהה הרכבת, מספר הרכבת, עיר המוצא, עיר היעד, מיקום תחנת המוצא, מיקום תחנת היעד, זמן היציאה, זמן ההגעה, תגיות הרכבת, רשימת סוגי המושבים",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי רכבת, נדרש לקבל מידע מפורט על הרכבת",
        "postconditions": "מחזיר את המידע המפורט על הרכבת, ומנחה את המשתמש לבחור מושב ולהזמין",
        "args": {
            "train_id": "מזהה הרכבת"
        },
        "returns": "מידע על הרכבת",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "בהקשר של תיירות ומלונאות, המלצה על אפשרויות מלון מתאימות בהתבסס על צרכי המיקום וההעדפות של המשתמש. מספקת מידע בסיסי על המלון, הכולל מזהה מלון, שם, דירוג, דירוג כוכבים, כתובת ותגים",
        "preconditions": "המשתמש מבקש להזמין מלון, ומספק מילות מפתח הקשורות למלון או מיקום",
        "postconditions": "מחזירה רשימת מלונות העומדים בקריטריונים. אם יש צורך לצפות בפרטי המלון (רשימת חדרים, מחירים וכו'), יש להשתמש בכלי שאילתת פרטי המלון, ולהנחות את המשתמש לבחור מלון",
        "args": {
            "city_name": "שם העיר",
            "key_words": "מילות מפתח לחיפוש (תואמות לשם המלון, תיאור המלון וכו')"
        },
        "returns": "פלט מובנה של מידע בסיסי על המלון",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "בהתבסס על צרכי המיקום וההעדפות של המשתמש, ממליץ על אפשרויות מתאימות לאטרקציות, מספק מידע בסיסי על האטרקציות, כולל מזהה האטרקציה, שם, כתובת, תיאור, דירוג ושעות פתיחה",
        "preconditions": "המשתמש מבקש להזמין אטרקציה, ומספק מילות מפתח או מיקומים הקשורים לאטרקציה",
        "postconditions": "מחזיר רשימת אטרקציות העומדות בתנאים, אם יש צורך לצפות בפרטי האטרקציה (רשימת כרטיסים, מחירים וכו') יש להשתמש בכלי שאילתת פרטי האטרקציה, ומנחה את המשתמש לבחור אטרקציה",
        "args": {
            "city_name": "שם העיר",
            "key_words": "מילות מפתח לחיפוש (התאמה לשם האטרקציה, מיקום, כתובת, מאפיינים וכו')"
        },
        "returns": "פלט מובנה של מידע בסיסי על האטרקציה",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "בהתבסס על צרכי המיקום וההעדפות של המשתמש, ממליצה על אפשרויות טיסה מתאימות ומספקת מידע בסיסי על הטיסה, הכולל מזהה טיסה, מספר טיסה, עיר מוצא, עיר יעד, מיקום שדה התעופה במוצא, מיקום שדה התעופה ביעד, זמן המראה, זמן נחיתה ותגיות טיסה",
        "preconditions": "המשתמש מבקש להזמין טיסה ומספק מילות מפתח או מיקומים הקשורים לטיסה",
        "postconditions": "מחזירה רשימת טיסות העומדות בתנאים. אם יש צורך לצפות בפרטי הטיסה (רשימת סוגי מושבים, מחיר, תאריכים וכו'), יש להשתמש בכלי שאילתת פרטי הטיסה ולהנחות את המשתמש לבחור טיסה",
        "args": {
            "departure": "עיר מוצא",
            "destination": "עיר יעד"
        },
        "returns": "פלט מובנה של מידע בסיסי על הטיסה",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "ממליץ על אפשרויות רכבת מתאימות בהתבסס על צרכי המיקום וההעדפות של המשתמש, ומספק מידע בסיסי על כרטיסי רכבת, הכולל מזהה רכבת, מספר רכבת, עיר מוצא, עיר יעד, מיקום תחנת המוצא, מיקום תחנת היעד, זמן יציאה, זמן הגעה ותגיות רכבת",
        "preconditions": "המשתמש מבקש להזמין רכבת, וסיפק מילות מפתח או מיקומים הקשורים לרכבת",
        "postconditions": "מחזיר רשימת כרטיסי רכבת העומדים בתנאים. אם יש צורך לצפות בפרטי כרטיס הרכבת (רשימת סוגי מושבים, מחיר, תאריך וכו'), יש להשתמש בכלי שאילתת פרטי כרטיס הרכבת. מנחה את המשתמש לבחור כרטיס רכבת",
        "args": {
            "departure": "עיר מוצא",
            "destination": "עיר יעד",
            "date": "תאריך יציאה"
        },
        "returns": "פלט מובנה של מידע בסיסי על הרכבת",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "כאשר משתמש מזמין מלון, המערכת יוצרת הזמנה בהתבסס על דרישות המשתמש (כגון שם המלון, תאריך צ'ק-אין, מספר אנשים וכו')",
        "preconditions": "המשתמש התחבר וסיפק מזהה זהות תקף (user_id), המשתמש סיפק שם מלון תקף (hotel_name) וסוג חדר (room_type), למערכת יש מידע על המלון היעד, ולמלון זה יש חדרים פנויים בתאריכים המבוקשים",
        "postconditions": "ההזמנה נוצרה, נא לאשר את התשלום",
        "args": {
            "hotel_id": "מזהה מלון",
            "room_id": "מזהה חדר",
            "user_id": "מזהה משתמש"
        },
        "returns": "פלט משוב של פעולת יצירת ההזמנה",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "המשתמש רוכש כרטיסים בהתבסס על האטרקציה והתאריך, המערכת מחזירה מידע רלוונטי על הכרטיסים ומבצעת את ההזמנה",
        "preconditions": "בתרחיש תיירותי של אטרקציה, המשתמש מבקש להזמין אטרקציה וסיפק את המידע ההכרחי להזמנה",
        "postconditions": "יצירת הזמנה, בקשה מהמשתמש לאשר תשלום",
        "args": {
            "attraction_id": "מזהה האטרקציה",
            "ticket_id": "מזהה הכרטיס",
            "user_id": "מזהה המשתמש",
            "date": "תאריך הביקור, בפורמט %Y-%m-%d",
            "quantity": "כמות"
        },
        "returns": "פלט משוב של פעולת יצירת ההזמנה",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "משתמשים רוכשים כרטיסי טיסה לפי מספר טיסה, תאריך, סוג מושב וכמות; המערכת מחזירה מידע על הכרטיס ומבצעת את ההזמנה",
        "preconditions": "בתרחיש של חיפוש ורכישת כרטיסי טיסה, המשתמש מבקש להזמין טיסה ומספק את המידע הנדרש להזמנה",
        "postconditions": "נוצרה הזמנה, נא לאשר תשלום",
        "args": {
            "flight_id": "מזהה טיסה",
            "seat_id": "מזהה מושב",
            "user_id": "מזהה משתמש",
            "date": "תאריך יציאה",
            "quantity": "כמות"
        },
        "returns": "פלט משוב של פעולת יצירת ההזמנה",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "משתמשים רוכשים כרטיסי רכבת לפי מספר רכבת, תאריך, סוג מושב וכמות; המערכת מחזירה מידע רלוונטי על כרטיסי הרכבת ומבצעת הזמנה",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי רכבת, המשתמש מבקש להזמין רכבת וסיפק את המידע ההכרחי להזמנה",
        "postconditions": "יצירת הזמנה, בקשה מהמשתמש לאשר את התשלום",
        "args": {
            "train_id": "מזהה רכבת",
            "seat_id": "מזהה מושב",
            "user_id": "מזהה משתמש",
            "date": "תאריך יציאה",
            "quantity": "כמות"
        },
        "returns": "פלט משוב עבור פעולת יצירת ההזמנה",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "המשתמש מבצע תשלום עבור הזמנת מלון",
        "preconditions": "בתרחיש חיפוש והזמנת מלון, המשתמש מבקש לשלם על הזמנת המלון, ומזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "אישור התשלום ועדכון סטטוס ההזמנה ל״שולם״",
        "args": {
            "order_id": "מזהה ההזמנה"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "המשתמש מבצע תשלום על הזמנת כרטיסים לאתר",
        "preconditions": "בתרחיש תיירותי באתר, המשתמש מבקש לשלם על הזמנת כרטיסים לאתר, ומזהה ההזמנה נקבע קודם לכן",
        "postconditions": "אישור התשלום ועדכון סטטוס ההזמנה ל\"שולם\"",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "המשתמש מבצע תשלום על הזמנת כרטיסי טיסה",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי טיסה, המשתמש מבקש לשלם על הזמנת הטיסה, ומזהה ההזמנה נקבע כבר קודם לכן",
        "postconditions": "אישור התשלום ועדכון סטטוס ההזמנה ל״שולם״",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "ביצוע תשלום על הזמנת כרטיסי רכבת",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי רכבת, המשתמש מבקש לשלם על הזמנת כרטיסי הרכבת, ומזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "לאשר את התשלום ולעדכן את סטטוס ההזמנה לשולם",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "מידע על תוצאת התשלום",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "בהתבסס על מזהה המשתמש, חפש הזמנות מלון של המשתמש, והחזר מידע הכולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה מלון, סכום כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון וסטטוס ההזמנה",
        "preconditions": "דרישת המשתמש היא לאחזר הזמנות מלון",
        "postconditions": "החזר מידע על ההזמנה, כדי להקל על שינוי או ביטול מאוחר יותר",
        "args": {
            "user_id": "מזהה משתמש",
            "date": "תאריך",
            "status": "סטטוס הזמנה"
        },
        "returns": "מידע על הזמנות המלון של המשתמש שצוין",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "בהתבסס על מזהה המשתמש, שולף הזמנות כרטיסים לאטרקציות של המשתמש, ומחזיר מידע הכולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה אטרקציה, סכום כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון וסטטוס ההזמנה",
        "preconditions": "דרישת המשתמש היא לבדוק הזמנות כרטיסים לאטרקציות",
        "postconditions": "מחזיר מידע על ההזמנה, המאפשר שינוי או ביטול עתידיים",
        "args": {
            "user_id": "מזהה משתמש",
            "date": "תאריך",
            "status": "סטטוס הזמנה"
        },
        "returns": "מידע על הזמנות כרטיסים לאטרקציות של המשתמש שצוין",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "בהתבסס על מזהה המשתמש, אחזר את הזמנות כרטיסי הטיסה של המשתמש, והחזר מידע הכולל את מזהה ההזמנה, סוג ההזמנה, מזהה המשתמש, מזהה הטיסה, המחיר הכולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון ומצב ההזמנה",
        "preconditions": "דרישת המשתמש היא לאחזר הזמנות כרטיסי טיסה",
        "postconditions": "החזר מידע על ההזמנה, כדי להקל על שינוי או ביטול מאוחר יותר",
        "args": {
            "user_id": "מזהה משתמש",
            "date": "תאריך",
            "status": "מצב הזמנה"
        },
        "returns": "מידע על הזמנות כרטיסי הטיסה של המשתמש שצוין",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "בהתבסס על מזהה המשתמש, שלף הזמנות כרטיסי רכבת של המשתמש, והחזר מידע הכולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה רכבת, מחיר כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון וסטטוס ההזמנה",
        "preconditions": "דרישת המשתמש היא לשלוף הזמנות כרטיסי רכבת",
        "postconditions": "החזר מידע על ההזמנה, כדי לאפשר שינוי או ביטול עתידיים",
        "args": {
            "user_id": "מזהה משתמש",
            "date": "תאריך",
            "status": "סטטוס הזמנה"
        },
        "returns": "מידע על הזמנות כרטיסי הרכבת של המשתמש שצוין",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "קבלת פרטי הזמנת מלון, הכוללת מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה מלון, מחיר כולל, זמן הזמנה, זמן עדכון, סטטוס הזמנה ופרטי חדר מפורטים (סוג חדר, תאריך כניסה, מחיר, מזהה חדר)",
        "preconditions": "המשתמש מבקש לקבל פרטי הזמנת מלון, מזהה ההזמנה נקבע בטקסט הקודם",
        "postconditions": "החזרת פרטי ההזמנה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "פרטי ההזמנה",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "קבלת פרטי הזמנת כרטיסים לאתר תיירותי, כולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה אתר, סכום כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון, סטטוס ההזמנה ופרטים מפורטים של האתר בהזמנה (סוג כרטיס, תאריך, מחיר, מזהה כרטיס)",
        "preconditions": "המשתמש מבקש לקבל פרטי הזמנת כרטיסים לאתר תיירותי, מזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "מחזיר את פרטי ההזמנה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "פרטי ההזמנה",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "קבלת פרטי הזמנת כרטיס טיסה, כולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה טיסה, מחיר כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון, סטטוס הזמנה ופרטים מפורטים של כרטיס הטיסה בהזמנה (סוג מושב, תאריך, מחיר, מזהה מושב)",
        "preconditions": "המשתמש מבקש לקבל פרטי הזמנת כרטיס טיסה, מזהה ההזמנה נקבע בטקסט הקודם",
        "postconditions": "החזרת פרטי ההזמנה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "פרטי ההזמנה",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "קבלת פרטי הזמנת כרטיס רכבת, כולל מזהה הזמנה, סוג הזמנה, מזהה משתמש, מזהה רכבת, מחיר כולל של ההזמנה, זמן ביצוע ההזמנה, זמן עדכון, סטטוס הזמנה ופרטים מפורטים של כרטיס הרכבת בהזמנה (סוג מושב, תאריך, מחיר, מזהה מושב)",
        "preconditions": "המשתמש מבקש לקבל פרטי הזמנת כרטיס רכבת, מזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "החזרת פרטי ההזמנה",
        "args": {
            "order_id": "מזהה הזמנה"
        },
        "returns": "פרטי ההזמנה",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "שינוי הזמנת כרטיסי רכבת, תומך בשינוי תאריך היציאה, טיפול אוטומטי בתשלום הפרש מחיר או החזר הפרש מחיר.",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי רכבת, המשתמש מבקש לשנות הזמנת כרטיסי רכבת, מזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "שינוי ההזמנה ועדכון סטטוס ההזמנה, אם נדרש תשלום הפרש מחיר, סטטוס ההזמנה משתנה ל-unpaid, אחרת נשמר הסטטוס המקורי, אם נדרש תשלום הפרש מחיר, יש להנחות את המשתמש לשלם עבור הזמנה זו",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש",
            "new_date": "תאריך יציאה חדש, בפורמט %Y-%m-%d"
        },
        "returns": "(תוכן ההזמנה לאחר השינוי, הפרש מחיר, חיובי משמעו נדרש תשלום הפרש מחיר, שלילי משמעו החזר הפרש מחיר)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "שינוי הזמנת כרטיסי טיסה, תומך בשינוי תאריך היציאה, טיפול אוטומטי בהפרשי מחיר לתשלום או להחזר.",
        "preconditions": "בתרחיש חיפוש ורכישת כרטיסי טיסה, המשתמש מבקש לשנות הזמנת כרטיסי טיסה, מזהה ההזמנה נקבע בהקשר הקודם.",
        "postconditions": "שינוי ההזמנה ועדכון סטטוס ההזמנה, אם נדרש תשלום הפרש מחיר, סטטוס ההזמנה משתנה ל-unpaid, אחרת נשמר הסטטוס המקורי, אם נדרש תשלום הפרש מחיר, יש להנחות את המשתמש לשלם הזמנה זו.",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש",
            "new_date": "תאריך יציאה חדש, פורמט %Y-%m-%d"
        },
        "returns": "(תוכן ההזמנה לאחר השינוי, הפרש מחיר, חיובי מציין נדרש תשלום הפרש, שלילי מציין החזר הפרש)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "המשתמש מבטל הזמנת מלון שכבר הוזמנה",
        "preconditions": "בתרחיש בדיקת הזמנות מלון, המשתמש מבקש לבטל הזמנת מלון, ומזהה ההזמנה נקבע בהקשר הקודם",
        "postconditions": "ביטול ההזמנה ועדכון סטטוס ההזמנה, אם נדרש החזר כספי על ההפרש, יש ליידע את המשתמש",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש"
        },
        "returns": "סכום ההחזר הכספי עבור ביטול ההזמנה",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "המשתמש מבטל הזמנת כרטיסים לאתר תיירותי שנקבעה מראש",
        "preconditions": "מזהה ההזמנה קיים בהיסטוריית השיחה או שבוצע כבר ברור לגבי ההזמנה, ולמשתמש יש הרשאה לבטל את ההזמנה הזו",
        "postconditions": "אם קיים החזר הפרש מחירים, יש ליידע את המשתמש בלבד",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש"
        },
        "returns": "סכום ההחזר בגין ביטול ההזמנה",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "המשתמש מבטל הזמנת כרטיס טיסה שכבר הוזמנה",
        "preconditions": "מזהה ההזמנה מופיע בהיסטוריית השיחה או שבוצע כבר חיפוש הזמנה, ולמשתמש יש הרשאה לבטל את ההזמנה הזו",
        "postconditions": "במקרה של החזר הפרש מחיר, יש ליידע את המשתמש בלבד",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש"
        },
        "returns": "סכום ההחזר בגין ביטול ההזמנה",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "ביטול הזמנת כרטיס רכבת שכבר הוזמנה על ידי המשתמש",
        "preconditions": "קיים מזהה הזמנה בשיחה הקודמת או שבוצע כבר ברור הזמנה, ולמשתמש יש הרשאה לבטל את ההזמנה",
        "postconditions": "אם יש החזר הפרש מחיר, יש ליידע את המשתמש בלבד",
        "args": {
            "order_id": "מזהה הזמנה",
            "user_id": "מזהה משתמש"
        },
        "returns": "סכום ההחזר עבור ביטול ההזמנה",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Indonesian version
TOOL_DESCRIPTIONS_ID = {
    "get_ota_hotel_info": {
        "description": "Mengambil informasi hotel, mencakup ID hotel, nama, rating, bintang, alamat, label, daftar kamar",
        "preconditions": "Dalam skenario pencarian dan pemesanan hotel, perlu mendapatkan informasi detail hotel",
        "postconditions": "Mengembalikan informasi detail hotel, memandu pengguna untuk memilih kamar dan melakukan pemesanan",
        "args": {
            "hotel_id": "ID hotel"
        },
        "returns": "Informasi hotel",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Mengambil informasi objek wisata, termasuk ID objek wisata, nama, alamat, deskripsi, peringkat, jam buka, harga tiket, dan daftar jenis tiket",
        "preconditions": "Dalam skenario wisata, perlu mendapatkan informasi detail objek wisata",
        "postconditions": "Mengembalikan informasi detail objek wisata, membimbing pengguna untuk memilih tiket dan melakukan pemesanan",
        "args": {
            "attraction_id": "ID objek wisata"
        },
        "returns": "Informasi objek wisata",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Mengambil informasi penerbangan, mencakup ID penerbangan, nomor penerbangan, kota keberangkatan, kota tujuan, lokasi bandara keberangkatan, lokasi bandara tujuan, waktu keberangkatan, waktu kedatangan, label penerbangan, dan daftar jenis kursi",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket penerbangan, perlu memperoleh informasi rinci penerbangan",
        "postconditions": "Mengembalikan informasi rinci penerbangan, memandu pengguna untuk memilih kursi dan melakukan pemesanan",
        "args": {
            "flight_id": "ID penerbangan"
        },
        "returns": "Informasi penerbangan",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Mengambil informasi kereta, termasuk ID kereta, nomor kereta, kota keberangkatan, kota tujuan, lokasi stasiun keberangkatan, lokasi stasiun tujuan, waktu keberangkatan, waktu kedatangan, label kereta, daftar jenis kursi",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket kereta, perlu mendapatkan informasi detail kereta",
        "postconditions": "Mengembalikan informasi detail kereta, memandu pengguna untuk memilih kursi dan melakukan pemesanan",
        "args": {
            "train_id": "ID kereta"
        },
        "returns": "Informasi kereta",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Dalam konteks perjalanan dan perhotelan, berdasarkan kebutuhan lokasi dan preferensi pengguna, rekomendasikan opsi hotel yang sesuai, berikan informasi dasar hotel, termasuk ID hotel, nama, rating, bintang, alamat, dan tag",
        "preconditions": "Pengguna meminta untuk memesan hotel, memberikan kata kunci terkait hotel atau lokasi",
        "postconditions": "Mengembalikan daftar hotel yang memenuhi syarat, jika perlu melihat detail hotel (daftar kamar, harga, dll.) perlu menggunakan alat kueri detail hotel, memandu pengguna untuk memilih hotel",
        "args": {
            "city_name": "Nama kota",
            "key_words": "Kata kunci pencarian (cocok dengan nama hotel, deskripsi hotel, dll.)"
        },
        "returns": "Keluarkan informasi dasar hotel secara terstruktur",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Berdasarkan kebutuhan lokasi dan preferensi pengguna, rekomendasikan opsi tempat wisata yang sesuai, sediakan informasi dasar tempat wisata, termasuk id tempat wisata, nama, alamat, deskripsi, peringkat, dan jam buka",
        "preconditions": "Pengguna meminta untuk memesan tempat wisata, memberikan kata kunci terkait tempat wisata atau lokasi",
        "postconditions": "Mengembalikan daftar tempat wisata yang memenuhi kondisi. Jika perlu melihat detail tempat wisata (daftar tiket, harga, dll.), perlu menggunakan alat kueri detail tempat wisata untuk memandu pengguna memilih tempat wisata",
        "args": {
            "city_name": "Nama kota",
            "key_words": "Kata kunci pencarian (cocok dengan nama tempat wisata, lokasi, alamat, ciri khas, dll.)"
        },
        "returns": "Keluarkan informasi dasar tempat wisata secara terstruktur",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Berdasarkan kebutuhan lokasi dan preferensi pengguna, merekomendasikan opsi penerbangan yang sesuai, menyediakan informasi dasar penerbangan, termasuk ID penerbangan, nomor penerbangan, kota keberangkatan, kota tujuan, lokasi bandara keberangkatan, lokasi bandara tujuan, waktu keberangkatan, waktu kedatangan, label penerbangan",
        "preconditions": "Pengguna meminta untuk memesan penerbangan, memberikan kata kunci atau lokasi terkait penerbangan",
        "postconditions": "Mengembalikan daftar penerbangan yang memenuhi kriteria, jika perlu melihat detail penerbangan (daftar jenis kursi, harga, tanggal, dll.) perlu menggunakan alat kueri detail penerbangan, memandu pengguna untuk memilih penerbangan",
        "args": {
            "departure": "Kota keberangkatan",
            "destination": "Kota tujuan"
        },
        "returns": "Mengeluarkan informasi dasar penerbangan secara terstruktur",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Berdasarkan kebutuhan lokasi dan preferensi pengguna, rekomendasikan opsi kereta yang sesuai, sediakan informasi dasar tiket kereta, mencakup ID kereta, nomor kereta, kota keberangkatan, kota tujuan, lokasi stasiun keberangkatan, lokasi stasiun tujuan, waktu keberangkatan, waktu kedatangan, dan label kereta.",
        "preconditions": "Pengguna meminta pemesanan kereta dan memberikan kata kunci terkait kereta atau lokasi.",
        "postconditions": "Mengembalikan daftar tiket kereta yang memenuhi syarat. Jika perlu melihat detail tiket kereta (daftar jenis kursi, harga, tanggal, dll.), perlu menggunakan alat kueri detail tiket kereta, dan pandu pengguna untuk memilih tiket kereta.",
        "args": {
            "departure": "Kota keberangkatan",
            "destination": "Kota tujuan",
            "date": "Tanggal keberangkatan"
        },
        "returns": "Output terstruktur informasi dasar kereta.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Saat pengguna memesan hotel, sistem membuat pesanan berdasarkan kebutuhan pengguna (seperti nama hotel, tanggal check-in, jumlah orang, dll.)",
        "preconditions": "Pengguna telah login dan memberikan identitas valid (user_id), pengguna memberikan nama hotel (hotel_name) dan tipe kamar (room_type) yang valid, sistem memiliki informasi tentang hotel target, dan hotel tersebut memiliki kamar pada tanggal yang diminta",
        "postconditions": "Pesanan dibuat, pengguna diminta mengkonfirmasi pembayaran",
        "args": {
            "hotel_id": "ID Hotel",
            "room_id": "ID Kamar",
            "user_id": "ID Pengguna"
        },
        "returns": "Output umpan balik dari operasi pembuatan pesanan",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Pengguna membeli tiket berdasarkan objek wisata dan tanggal, sistem mengembalikan informasi terkait tiket dan melakukan pemesanan",
        "preconditions": "Dalam skenario kunjungan objek wisata, pengguna meminta pemesanan objek wisata dan menyediakan informasi yang diperlukan untuk pemesanan",
        "postconditions": "Pesanan dihasilkan, minta pengguna untuk konfirmasi pembayaran",
        "args": {
            "attraction_id": "ID Objek Wisata",
            "ticket_id": "ID Tiket",
            "user_id": "ID Pengguna",
            "date": "Tanggal kunjungan, format %Y-%m-%d",
            "quantity": "Jumlah"
        },
        "returns": "Output umpan balik dari operasi pembuatan pesanan",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Pengguna membeli tiket pesawat berdasarkan nomor penerbangan, tanggal, jenis kursi, dan jumlah; sistem mengembalikan informasi terkait tiket dan melakukan pemesanan",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket, pengguna meminta untuk memesan penerbangan dan memberikan informasi yang diperlukan terkait pemesanan",
        "postconditions": "Pesanan dibuat, minta pengguna untuk mengkonfirmasi pembayaran",
        "args": {
            "flight_id": "ID Penerbangan",
            "seat_id": "ID Kursi",
            "user_id": "ID Pengguna",
            "date": "Tanggal Keberangkatan",
            "quantity": "Jumlah"
        },
        "returns": "Output umpan balik untuk operasi pembuatan pesanan",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Pengguna membeli tiket kereta berdasarkan nomor kereta, tanggal, jenis kursi, dan jumlah; sistem mengembalikan informasi terkait tiket kereta dan melakukan pemesanan.",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket kereta, pengguna meminta pemesanan kereta dan memberikan informasi yang diperlukan terkait pemesanan.",
        "postconditions": "Pesanan dibuat, mohon pengguna mengkonfirmasi pembayaran.",
        "args": {
            "train_id": "ID Kereta",
            "seat_id": "ID Kursi",
            "user_id": "ID Pengguna",
            "date": "Tanggal Keberangkatan",
            "quantity": "Jumlah"
        },
        "returns": "Output umpan balik dari operasi pembuatan pesanan.",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Pengguna melakukan pembayaran pesanan hotel",
        "preconditions": "Dalam skenario pencarian dan pemesanan hotel, pengguna meminta pembayaran pesanan hotel, dan ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Konfirmasi pembayaran dan perbarui status pesanan menjadi telah dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Pengguna melakukan pembayaran pesanan tiket",
        "preconditions": "Dalam skenario wisata atraksi, pengguna meminta pembayaran pesanan tiket atraksi, ID pesanan telah ditentukan dalam konteks sebelumnya",
        "postconditions": "Konfirmasi pembayaran dan perbarui status pesanan menjadi telah dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Pengguna melakukan pembayaran pesanan tiket pesawat",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket pesawat, pengguna meminta pembayaran pesanan penerbangan, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Konfirmasi pembayaran dan perbarui status pesanan menjadi telah dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Pengguna melakukan pembayaran pesanan tiket kereta api",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket kereta api, pengguna meminta pembayaran pesanan tiket kereta api, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Konfirmasi pembayaran dan perbarui status pesanan menjadi telah dibayar",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Informasi hasil pembayaran",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Berdasarkan ID pengguna, cari pesanan hotel pengguna dan kembalikan informasi yang mencakup ID pesanan, jenis pesanan, ID pengguna, ID hotel, total harga pesanan, waktu pemesanan, waktu pembaruan, dan status pesanan.",
        "preconditions": "Kebutuhan pengguna adalah mencari pesanan hotel.",
        "postconditions": "Mengembalikan informasi pesanan agar mudah dimodifikasi atau dibatalkan nanti.",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tanggal",
            "status": "Status Pesanan"
        },
        "returns": "Informasi pesanan hotel dari pengguna yang ditentukan.",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Berdasarkan ID pengguna, cari pesanan tiket tempat wisata pengguna, kembalikan informasi yang mencakup ID pesanan, jenis pesanan, ID pengguna, ID tempat wisata, total harga pesanan, waktu pemesanan, waktu pembaruan, dan status pesanan",
        "preconditions": "Kebutuhan pengguna adalah untuk mencari pesanan tiket tempat wisata",
        "postconditions": "Mengembalikan informasi pesanan untuk memudahkan modifikasi atau pembatalan di kemudian hari",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tanggal",
            "status": "Status Pesanan"
        },
        "returns": "Informasi pesanan tiket tempat wisata untuk pengguna yang ditentukan",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Berdasarkan ID pengguna, cari pesanan tiket pesawat pengguna, kembalikan informasi yang mencakup ID pesanan, jenis pesanan, ID pengguna, ID penerbangan, total harga pesanan, waktu pemesanan, waktu pembaruan, dan status pesanan",
        "preconditions": "Kebutuhan pengguna adalah mencari pesanan tiket pesawat",
        "postconditions": "Mengembalikan informasi pesanan untuk memudahkan modifikasi atau pembatalan selanjutnya",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tanggal",
            "status": "Status Pesanan"
        },
        "returns": "Informasi pesanan tiket pesawat untuk pengguna yang ditentukan",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Berdasarkan ID pengguna, cari pesanan tiket kereta pengguna dan kembalikan informasi yang mencakup ID pesanan, jenis pesanan, ID pengguna, ID kereta, total harga pesanan, waktu pemesanan, waktu pembaruan, dan status pesanan.",
        "preconditions": "Kebutuhan pengguna adalah untuk mencari pesanan tiket kereta.",
        "postconditions": "Mengembalikan informasi pesanan untuk memudahkan modifikasi atau pembatalan di kemudian hari.",
        "args": {
            "user_id": "ID Pengguna",
            "date": "Tanggal",
            "status": "Status Pesanan"
        },
        "returns": "Informasi pesanan tiket kereta untuk pengguna yang ditentukan.",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Mengambil detail pesanan hotel, mencakup ID pesanan, jenis pesanan, ID pengguna, ID hotel, total harga pesanan, waktu pemesanan, waktu pembaruan, status pesanan, dan informasi rinci kamar pesanan (jenis kamar, tanggal check-in, harga, ID kamar)",
        "preconditions": "Pengguna meminta untuk mengambil detail pesanan hotel, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Mengembalikan detail pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Detail pesanan",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Mengambil detail pesanan tiket tempat wisata, termasuk ID Pesanan, Jenis Pesanan, ID Pengguna, ID Tempat Wisata, Total Harga Pesanan, Waktu Pemesanan, Waktu Pembaruan, Status Pesanan, dan informasi detail tempat wisata pesanan (Jenis Tiket, Tanggal, Harga, ID Tiket)",
        "preconditions": "Pengguna meminta untuk mengambil detail pesanan tiket tempat wisata, ID Pesanan telah ditentukan sebelumnya",
        "postconditions": "Mengembalikan detail pesanan",
        "args": {
            "order_id": "ID Pesanan"
        },
        "returns": "Detail pesanan",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Mengambil detail pesanan tiket pesawat, termasuk ID pesanan, jenis pesanan, ID pengguna, ID penerbangan, total harga pesanan, waktu pemesanan, waktu pembaruan, status pesanan, dan informasi detail tiket pesanan (jenis kursi, tanggal, harga, ID kursi)",
        "preconditions": "Pengguna meminta detail pesanan tiket pesawat, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Mengembalikan detail pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "detail pesanan",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Mengambil detail pesanan tiket kereta api, termasuk ID pesanan, jenis pesanan, ID pengguna, ID kereta, total harga pesanan, waktu pemesanan, waktu pembaruan, status pesanan, dan informasi detail tiket kereta api pesanan (jenis kursi, tanggal, harga, ID kursi)",
        "preconditions": "Pengguna meminta detail pesanan tiket kereta api, ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Mengembalikan detail pesanan",
        "args": {
            "order_id": "ID pesanan"
        },
        "returns": "Detail pesanan",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Mengubah pesanan tiket kereta api, mendukung perubahan tanggal keberangkatan, serta secara otomatis menangani pembayaran selisih atau pengembalian dana.",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket kereta api, pengguna meminta untuk mengubah pesanan tiket kereta api, dan ID pesanan telah ditentukan sebelumnya.",
        "postconditions": "Mengubah pesanan dan memperbarui status pesanan. Jika diperlukan pembayaran selisih, status pesanan diubah menjadi unpaid, jika tidak tetap status semula. Jika diperlukan pembayaran selisih, pengguna perlu diarahkan untuk membayar pesanan tersebut.",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna",
            "new_date": "Tanggal keberangkatan baru, format %Y-%m-%d"
        },
        "returns": "(Konten pesanan setelah diubah, selisih harga, nilai positif menunjukkan perlu pembayaran selisih, nilai negatif menunjukkan pengembalian selisih)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Mengubah pesanan tiket pesawat, mendukung perubahan tanggal keberangkatan, dan secara otomatis menangani pembayaran selisih harga atau pengembalian dana.",
        "preconditions": "Dalam skenario pencarian dan pembelian tiket pesawat, pengguna meminta perubahan pesanan tiket pesawat, dan ID pesanan telah ditentukan pada konteks sebelumnya.",
        "postconditions": "Mengubah pesanan dan memperbarui status pesanan. Jika terdapat selisih harga yang harus dibayar, status pesanan diubah menjadi unpaid, jika tidak tetap pada status semula. Jika terdapat selisih harga yang harus dibayar, pengguna perlu diarahkan untuk melakukan pembayaran untuk pesanan tersebut.",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna",
            "new_date": "Tanggal keberangkatan baru, format %Y-%m-%d"
        },
        "returns": "(Konten pesanan setelah diubah, selisih harga, nilai positif berarti perlu pembayaran tambahan, nilai negatif berarti pengembalian dana)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Pengguna membatalkan pesanan hotel yang telah dipesan",
        "preconditions": "Dalam skenario pencarian pemesanan hotel, pengguna meminta pembatalan pesanan hotel, dan ID pesanan telah ditentukan sebelumnya",
        "postconditions": "Membatalkan pesanan dan memperbarui status pesanan; jika diperlukan pengembalian dana selisih, cukup informasikan kepada pengguna",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah pengembalian dana untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Pengguna membatalkan pesanan tiket tempat wisata yang telah dipesan",
        "preconditions": "ID pesanan terdapat dalam riwayat percakapan atau pencarian pesanan telah dilakukan, serta pengguna memiliki izin untuk membatalkan pesanan tersebut",
        "postconditions": "Jika terdapat pengembalian dana selisih, cukup informasikan kepada pengguna",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah pengembalian dana untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Pengguna membatalkan pesanan tiket pesawat yang telah dipesan",
        "preconditions": "ID pesanan terdapat dalam riwayat percakapan atau pencarian pesanan telah dilakukan, dan pengguna memiliki izin untuk membatalkan pesanan tersebut",
        "postconditions": "Jika terdapat pengembalian dana selisih, cukup beri tahu pengguna",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah pengembalian dana untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Pengguna membatalkan pesanan tiket kereta api yang telah dipesan",
        "preconditions": "ID pesanan terdapat dalam riwayat percakapan atau pencarian pesanan telah dilakukan, pengguna memiliki izin untuk membatalkan pesanan tersebut",
        "postconditions": "Jika terdapat pengembalian selisih harga, cukup informasikan kepada pengguna",
        "args": {
            "order_id": "ID Pesanan",
            "user_id": "ID Pengguna"
        },
        "returns": "Jumlah dana yang dikembalikan untuk pembatalan pesanan",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Korean version
TOOL_DESCRIPTIONS_KO = {
    "get_ota_hotel_info": {
        "description": "호텔 정보를 가져오며, 호텔 ID, 이름, 평점, 등급, 주소, 태그, 객실 목록을 포함합니다.",
        "preconditions": "호텔 조회 및 예약 상황에서 호텔의 상세 정보가 필요할 때",
        "postconditions": "호텔의 상세 정보를 반환하여 사용자가 객실을 선택하고 예약하도록 안내합니다.",
        "args": {
            "hotel_id": "호텔 ID"
        },
        "returns": "호텔 정보",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "관광지 정보를 조회합니다. 관광지 ID, 이름, 주소, 설명, 평점, 운영 시간, 입장료, 티켓 종류 목록을 포함합니다.",
        "preconditions": "관광지 관광 시나리오에서 관광지의 상세 정보가 필요한 경우",
        "postconditions": "관광지의 상세 정보를 반환하며, 사용자가 티켓을 선택하고 주문하도록 유도합니다.",
        "args": {
            "attraction_id": "관광지 ID"
        },
        "returns": "관광지 정보",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "항공편 정보를 조회합니다. 항공편 ID, 항공편 번호, 출발 도시, 도착 도시, 출발 공항 위치, 도착 공항 위치, 출발 시간, 도착 시간, 항공편 태그, 좌석 유형 목록을 포함합니다.",
        "preconditions": "항공권 조회 및 구매 시나리오에서 항공편의 상세 정보가 필요할 때",
        "postconditions": "항공편의 상세 정보를 반환하고, 사용자가 좌석을 선택하여 주문하도록 안내합니다.",
        "args": {
            "flight_id": "항공편 ID"
        },
        "returns": "항공편 정보",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "기차 정보를 조회합니다. 기차 ID, 열차 번호, 출발 도시, 도착 도시, 출발역 위치, 도착역 위치, 출발 시간, 도착 시간, 기차 태그, 좌석 유형 목록을 포함합니다.",
        "preconditions": "기차표 조회 및 구매 상황에서 기차의 상세 정보가 필요할 때입니다.",
        "postconditions": "기차의 상세 정보를 반환하며, 사용자가 좌석을 선택하고 주문하도록 유도합니다.",
        "args": {
            "train_id": "기차 ID"
        },
        "returns": "기차 정보",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "여행 및 숙박 상황에서 사용자의 위치 요구 사항과 선호도를 기반으로 적합한 호텔 옵션을 추천하며, 호텔 ID, 이름, 평점, 등급, 주소, 태그를 포함한 호텔 기본 정보를 제공합니다.",
        "preconditions": "사용자가 호텔 예약을 요청하며, 호텔 관련 키워드 또는 위치를 제공한 경우.",
        "postconditions": "조건에 맞는 호텔 목록을 반환하며, 호텔 상세 정보 (방 목록, 가격 등) 를 확인하려면 호텔 상세 조회 도구를 사용해야 하며, 사용자에게 호텔 선택을 유도합니다.",
        "args": {
            "city_name": "도시 이름",
            "key_words": "검색 키워드 (호텔 이름, 호텔 소개 등 매칭)"
        },
        "returns": "호텔 기본 정보의 구조화된 출력",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "사용자의 위치 요구 사항 및 선호도에 기반하여 적합한 관광지 옵션을 추천하고, 관광지 ID, 이름, 주소, 설명, 평점, 운영 시간을 포함한 기본 정보를 제공합니다.",
        "preconditions": "사용자가 관광지 예약을 요청하며, 관광지 관련 키워드 또는 위치를 제공했습니다.",
        "postconditions": "조건에 맞는 관광지 목록을 반환합니다. 관광지 상세 정보 (티켓 목록, 가격 등) 를 확인하려면 관광지 상세 조회 도구를 사용해야 하며, 사용자에게 관광지 선택을 유도합니다.",
        "args": {
            "city_name": "도시 이름",
            "key_words": "검색 키워드 (관광지 이름, 위치, 주소, 특징 등 매칭)"
        },
        "returns": "구조화된 형태로 관광지 기본 정보를 출력합니다",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "사용자의 위치 요구 사항 및 선호도에 기반하여 적합한 항공편 옵션을 추천하고, 항공편 ID, 항공편 번호, 출발 도시, 도착 도시, 출발 공항 위치, 도착 공항 위치, 출발 시간, 도착 시간, 항공편 태그를 포함한 항공편 기본 정보를 제공합니다.",
        "preconditions": "사용자가 항공편 예약을 요청하며 항공편 관련 키워드 또는 위치를 제공한 경우",
        "postconditions": "조건에 맞는 항공편 목록을 반환하며, 항공편 세부 정보 (좌석 유형 목록, 가격, 날짜 등) 를 확인하려면 항공편 세부 정보 조회 도구를 사용해야 하며, 사용자에게 항공편 선택을 유도합니다.",
        "args": {
            "departure": "출발 도시",
            "destination": "목적지 도시"
        },
        "returns": "항공편 기본 정보를 구조화하여 출력",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "사용자의 위치 요구사항과 선호도에 따라 적합한 기차 옵션을 추천하며, 기차 ID, 열차 번호, 출발 도시, 도착 도시, 출발 역 위치, 도착 역 위치, 출발 시간, 도착 시간, 기차 태그를 포함한 기차표 기본 정보를 제공합니다.",
        "preconditions": "사용자가 기차 예약을 요청하며 기차 관련 키워드 또는 위치를 제공했을 때",
        "postconditions": "조건에 부합하는 기차표 목록을 반환합니다. 기차표 상세 정보 (좌석 유형 목록, 가격, 날짜 등) 를 확인하려면 기차표 상세 정보 조회 도구를 사용해야 하며, 사용자가 기차표를 선택하도록 안내합니다.",
        "args": {
            "departure": "출발 도시",
            "destination": "목적지 도시",
            "date": "출발 날짜"
        },
        "returns": "기차 기본 정보를 구조화하여 출력합니다.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "사용자가 호텔을 예약할 때, 시스템은 사용자의 요구 사항 (예: 호텔 이름, 체크인 날짜, 인원 수 등) 에 따라 주문을 생성합니다.",
        "preconditions": "사용자가 로그인하여 유효한 신원 식별자 (user_id) 를 제공해야 하며, 유효한 호텔 이름 (hotel_name) 및 객실 유형 (room_type) 을 제공해야 하고, 시스템에 대상 호텔에 대한 정보가 있어야 하며, 해당 호텔이 요청된 날짜에 객실이 있어야 합니다.",
        "postconditions": "주문이 생성되며 사용자에게 결제 확인을 요청합니다.",
        "args": {
            "hotel_id": "호텔 ID",
            "room_id": "객실 ID",
            "user_id": "사용자 ID"
        },
        "returns": "주문 생성 작업의 피드백 출력",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "사용자가 관광명소와 날짜에 따라 티켓을 구매하면, 시스템은 티켓 관련 정보를 반환하고 주문을 생성합니다.",
        "preconditions": "관광지 방문 상황에서 사용자가 관광지 예약을 요청하며, 예약 관련 필수 정보를 제공합니다.",
        "postconditions": "주문이 생성되며, 사용자에게 결제를 확인하도록 요청합니다.",
        "args": {
            "attraction_id": "관광지 ID",
            "ticket_id": "티켓 ID",
            "user_id": "사용자 ID",
            "date": "방문 날짜, 형식: %Y-%m-%d",
            "quantity": "수량"
        },
        "returns": "주문 생성 작업의 피드백 출력",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "사용자가 항공편 번호, 날짜, 좌석 유형, 수량에 따라 항공권을 구매하면 시스템은 항공권 관련 정보를 반환하고 주문을 진행합니다.",
        "preconditions": "항공권 조회 및 구매 시나리오에서 사용자가 항공편 예약을 요청하며 예약에 필요한 필수 정보를 제공했습니다.",
        "postconditions": "주문이 생성되었으며, 사용자에게 결제를 확인하도록 요청합니다.",
        "args": {
            "flight_id": "항공편 ID",
            "seat_id": "좌석 ID",
            "user_id": "사용자 ID",
            "date": "출발 날짜",
            "quantity": "수량"
        },
        "returns": "주문 생성 작업의 피드백 출력",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "사용자가 열차 번호, 날짜, 좌석 유형, 수량에 따라 기차표를 구매하면 시스템이 기차표 관련 정보를 반환하고 주문을 진행합니다.",
        "preconditions": "기차표 조회 및 구매 시나리오에서 사용자가 기차 예약을 요청하며 예약 관련 필수 정보를 제공한 경우",
        "postconditions": "주문이 생성되며 사용자에게 결제 확인을 요청합니다.",
        "args": {
            "train_id": "기차 ID",
            "seat_id": "좌석 ID",
            "user_id": "사용자 ID",
            "date": "출발 날짜",
            "quantity": "수량"
        },
        "returns": "주문 생성 작업의 피드백 출력",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "사용자가 호텔 주문 결제를 수행합니다.",
        "preconditions": "호텔 조회 및 예약 시나리오에서 사용자가 호텔 주문 결제를 요청하며, 이전 문맥에서 주문 ID 가 확인되었습니다.",
        "postconditions": "결제를 확인하고 주문 상태를 '결제 완료'로 업데이트합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "사용자가 티켓 주문 결제를 진행합니다.",
        "preconditions": "관광지 관광 시나리오에서 사용자가 관광지 티켓 주문 결제를 요청하며, 이전 문맥에서 주문 ID 가 확인되었습니다.",
        "postconditions": "결제를 확인하고 주문 상태를 결제 완료로 업데이트합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "사용자가 항공권 주문 결제를 진행합니다.",
        "preconditions": "항공권 조회 및 구매 시나리오에서 사용자가 항공권 주문 결제를 요청하며, 이전 대화에서 주문 ID 가 확인되었습니다.",
        "postconditions": "결제를 확인하고 주문 상태를 '결제 완료'로 업데이트합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "사용자가 기차표 주문을 결제합니다",
        "preconditions": "기차표 조회 및 구매 시나리오에서 사용자가 기차표 주문 결제를 요청하며, 이전 문맥에서 주문 ID 가 확인된 경우",
        "postconditions": "결제를 확인하고 주문 상태를 결제 완료로 업데이트합니다",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "결제 결과 정보",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "사용자 ID 를 기반으로 사용자의 호텔 주문을 조회하며, 주문 ID, 주문 유형, 사용자 ID, 호텔 ID, 주문 총액, 주문 시간, 업데이트 시간 및 주문 상태를 포함하여 반환합니다.",
        "preconditions": "사용자가 호텔 주문을 조회하려는 경우",
        "postconditions": "주문 정보를 반환하여 이후 수정 또는 취소에 활용할 수 있습니다.",
        "args": {
            "user_id": "사용자 ID",
            "date": "날짜",
            "status": "주문 상태"
        },
        "returns": "지정된 사용자의 호텔 주문 정보",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "사용자 ID 에 따라 사용자의 관광명소 티켓 주문을 조회하고, 주문 ID, 주문 유형, 사용자 ID, 관광명소 ID, 주문 총액, 주문 시간, 업데이트 시간, 주문 상태를 포함하여 반환합니다.",
        "preconditions": "사용자가 관광명소 티켓 주문을 조회하고자 하는 경우",
        "postconditions": "주문 정보를 반환하여 추후 수정 또는 취소가 가능하도록 합니다.",
        "args": {
            "user_id": "사용자 ID",
            "date": "날짜",
            "status": "주문 상태"
        },
        "returns": "지정된 사용자의 관광명소 티켓 주문 정보",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "사용자 ID 에 따라 사용자의 항공권 주문을 조회하고, 주문 ID, 주문 유형, 사용자 ID, 항공편 ID, 주문 총액, 주문 시간, 업데이트 시간 및 주문 상태를 반환합니다.",
        "preconditions": "사용자가 항공권 주문 조회를 원하는 경우",
        "postconditions": "주문 정보를 반환하여 이후 수정 또는 취소에 용이하도록 합니다.",
        "args": {
            "user_id": "사용자 ID",
            "date": "날짜",
            "status": "주문 상태"
        },
        "returns": "지정된 사용자의 항공권 주문 정보",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "사용자 ID 를 기반으로 사용자의 기차표 주문을 조회하며, 주문 ID, 주문 유형, 사용자 ID, 기차 ID, 주문 총액, 주문 시간, 업데이트 시간 및 주문 상태를 포함하여 반환합니다.",
        "preconditions": "사용자가 기차표 주문을 조회하려는 경우",
        "postconditions": "주문 정보를 반환하여 이후 수정 또는 취소에 활용할 수 있습니다.",
        "args": {
            "user_id": "사용자 ID",
            "date": "날짜",
            "status": "주문 상태"
        },
        "returns": "지정된 사용자의 기차표 주문 정보",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "호텔 주문 상세 정보를 조회하며, 주문 ID, 주문 유형, 사용자 ID, 호텔 ID, 주문 총액, 주문 시간, 업데이트 시간, 주문 상태 및 주문 객실 상세 정보 (객실 유형, 체크인 날짜, 가격, 객실 ID) 를 포함합니다.",
        "preconditions": "사용자가 호텔 주문 상세 정보를 요청했고, 이전 문맥에서 주문 ID 가 확인된 경우",
        "postconditions": "주문 상세 정보를 반환합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 상세 정보",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "관광지 티켓 주문 상세 정보를 조회합니다. 주문 ID, 주문 유형, 사용자 ID, 관광지 ID, 주문 총액, 주문 시간, 업데이트 시간, 주문 상태 및 주문 관광지 상세 정보 (티켓 유형, 날짜, 가격, 티켓 ID) 를 포함합니다.",
        "preconditions": "사용자가 관광지 티켓 주문 상세 정보를 요청하며, 이전 문맥에서 주문 ID 가 확인되었습니다.",
        "postconditions": "주문 상세 정보를 반환합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 상세 정보",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "항공권 주문 상세 정보를 조회하며, 주문 ID, 주문 유형, 사용자 ID, 항공편 ID, 주문 총액, 주문 시간, 업데이트 시간, 주문 상태 및 주문 항공권 상세 정보 (좌석 유형, 날짜, 가격, 좌석 ID) 를 포함합니다.",
        "preconditions": "사용자가 항공권 주문 상세 정보 조회를 요청하며, 이전 문맥에서 주문 ID 가 확인된 경우",
        "postconditions": "주문 상세 정보 반환",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 상세 정보",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "기차표 주문 상세 정보를 조회하며, 주문 ID, 주문 유형, 사용자 ID, 기차 ID, 주문 총액, 주문 시간, 업데이트 시간, 주문 상태 및 주문 기차표 상세 정보 (좌석 유형, 날짜, 가격, 좌석 ID) 를 포함합니다.",
        "preconditions": "사용자가 기차표 주문 상세 정보를 요청하며, 이전 문맥에서 주문 ID 가 확인되었습니다.",
        "postconditions": "주문 상세 정보를 반환합니다.",
        "args": {
            "order_id": "주문 ID"
        },
        "returns": "주문 상세 정보",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "기차표 주문을 수정하며 출발 날짜 변경을 지원하고, 추가 요금 또는 환불 차액을 자동으로 처리합니다.",
        "preconditions": "기차표 조회 및 구매 상황에서 사용자가 기차표 주문 수정을 요청하며, 이전 문맥에서 주문 ID 가 확인된 상태",
        "postconditions": "주문을 수정하고 주문 상태를 업데이트합니다. 추가 요금 납부가 필요하면 주문 상태를 'unpaid'로 변경하고, 그렇지 않으면 기존 상태를 유지합니다. 추가 요금 납부가 필요할 경우 사용자에게 해당 주문 결제를 안내해야 합니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID",
            "new_date": "새로운 출발 날짜, 형식: %Y-%m-%d"
        },
        "returns": "(수정된 주문 내용, 차액, 양수는 추가 납부 필요, 음수는 환불 필요)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "항공권 주문을 수정하고 출발 날짜 변경을 지원하며, 추가 요금 또는 환불 차액을 자동으로 처리합니다.",
        "preconditions": "항공권 조회 및 구매 상황에서 사용자가 항공권 주문 수정을 요청하고, 이전 문맥에서 주문 ID 가 확인된 경우",
        "postconditions": "주문을 수정하고 주문 상태를 업데이트합니다. 추가 요금이 필요하면 주문 상태를 'unpaid'로 변경하고, 그렇지 않으면 기존 상태를 유지합니다. 추가 요금이 필요한 경우 사용자에게 해당 주문 결제를 안내해야 합니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID",
            "new_date": "새로운 출발 날짜, 형식: %Y-%m-%d"
        },
        "returns": "(수정된 주문 내용, 차액, 양수는 추가 납부 필요, 음수는 환불 차액)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "사용자가 예약한 호텔 주문을 취소합니다.",
        "preconditions": "호텔 예약 조회 시나리오에서 사용자가 호텔 주문 취소를 요청하며, 이전 대화에서 주문 ID 가 확인된 경우",
        "postconditions": "주문을 취소하고 주문 상태를 업데이트하며, 환불 차액이 필요한 경우 사용자에게 알립니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID"
        },
        "returns": "주문 취소 시 환불 금액",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "사용자가 예약한 관광지 티켓 주문을 취소합니다.",
        "preconditions": "이전 대화에 주문 ID 가 있거나 이미 주문 조회를 수행했으며, 사용자가 해당 주문을 취소할 권한이 있어야 합니다.",
        "postconditions": "차액 환불이 발생하는 경우 사용자에게 알려주기만 하면 됩니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID"
        },
        "returns": "주문 취소 시 환불 금액",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "사용자가 예약한 항공권 주문을 취소합니다.",
        "preconditions": "이전 대화에 주문 ID 가 있거나 이미 주문 조회를 수행했으며, 사용자가 해당 주문을 취소할 권한이 있어야 합니다.",
        "postconditions": "차액 환불이 있는 경우 사용자에게 알려주기만 하면 됩니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID"
        },
        "returns": "주문 취소 시 환불 금액",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "사용자가 예약한 기차표 주문을 취소합니다.",
        "preconditions": "이전 대화에 주문 ID 가 있거나 이미 주문 조회를 수행했어야 하며, 사용자가 해당 주문을 취소할 권한이 있어야 합니다.",
        "postconditions": "차액 환불이 있는 경우 사용자에게 알려주기만 하면 됩니다.",
        "args": {
            "order_id": "주문 ID",
            "user_id": "사용자 ID"
        },
        "returns": "주문 취소 시 환불 금액",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Spanish version
TOOL_DESCRIPTIONS_ES = {
    "get_ota_hotel_info": {
        "description": "Obtener información del hotel, incluye ID del hotel, nombre, valoración, categoría, dirección, etiquetas, lista de habitaciones",
        "preconditions": "En el escenario de consulta y reserva de hoteles, es necesario obtener la información detallada del hotel",
        "postconditions": "Devolver la información detallada del hotel, guiar al usuario para seleccionar una habitación y realizar la reserva",
        "args": {
            "hotel_id": "ID del hotel"
        },
        "returns": "Información del hotel",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Obtener información del atractivo turístico, incluyendo ID del atractivo, nombre, dirección, descripción, calificación, horario de apertura, precio de la entrada y lista de tipos de entradas",
        "preconditions": "En el escenario de turismo de atractivos, se necesita obtener la información detallada del atractivo",
        "postconditions": "Devuelve la información detallada del atractivo, guía al usuario para seleccionar la entrada y realizar el pedido",
        "args": {
            "attraction_id": "ID del atractivo"
        },
        "returns": "Información del atractivo",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Obtener información del vuelo, que incluye ID del vuelo, número de vuelo, ciudad de salida, ciudad de llegada, ubicación del aeropuerto de salida, ubicación del aeropuerto de llegada, hora de salida, hora de llegada, etiquetas del vuelo y lista de tipos de asientos",
        "preconditions": "En el escenario de consulta y compra de vuelos, es necesario obtener la información detallada del vuelo",
        "postconditions": "Devolver la información detallada del vuelo, guiar al usuario para seleccionar el asiento y realizar el pedido",
        "args": {
            "flight_id": "ID del vuelo"
        },
        "returns": "Información del vuelo",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Obtener información del tren, incluyendo ID del tren, número de tren, ciudad de origen, ciudad de destino, estación de salida, estación de llegada, hora de salida, hora de llegada, etiquetas del tren y lista de tipos de asientos",
        "preconditions": "En el escenario de consulta y compra de boletos de tren, se necesita obtener la información detallada del tren",
        "postconditions": "Devolver la información detallada del tren, guiando al usuario a seleccionar un asiento y realizar el pedido",
        "args": {
            "train_id": "ID del tren"
        },
        "returns": "Información del tren",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "En el contexto de viajes y hostelería, recomienda opciones de hoteles adecuadas basándose en las necesidades de ubicación y preferencias del usuario, proporcionando información básica del hotel, que incluye ID del hotel, nombre, puntuación, categoría, dirección y etiquetas",
        "preconditions": "El usuario solicita reservar un hotel y proporciona palabras clave relacionadas con el hotel o una ubicación",
        "postconditions": "Devuelve una lista de hoteles que cumplen los criterios. Si se necesita ver los detalles del hotel (lista de habitaciones, precios, etc.), se debe usar la herramienta de consulta de detalles del hotel. Guía al usuario para seleccionar un hotel",
        "args": {
            "city_name": "Nombre de la ciudad",
            "key_words": "Palabras clave de búsqueda (coinciden con el nombre del hotel, la descripción del hotel, etc.)"
        },
        "returns": "Salida estructurada de la información básica del hotel",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Basado en las necesidades de ubicación y preferencias del usuario, recomienda opciones de atracciones adecuadas y proporciona información básica sobre las atracciones, incluyendo ID de la atracción, nombre, dirección, descripción, puntuación y horario de apertura.",
        "preconditions": "El usuario solicita reservar una atracción y proporciona palabras clave relacionadas con la atracción o la ubicación.",
        "postconditions": "Devuelve una lista de atracciones que cumplen los criterios. Si se necesita ver los detalles de la atracción (lista de entradas, precios, etc.), se debe usar la herramienta de consulta de detalles de la atracción. Guía al usuario para seleccionar una atracción.",
        "args": {
            "city_name": "Nombre de la ciudad",
            "key_words": "Palabras clave de búsqueda (coinciden con el nombre de la atracción, ubicación, dirección, características, etc.)"
        },
        "returns": "Salida estructurada de la información básica de la atracción",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Basado en las necesidades de ubicación y preferencias del usuario, recomienda opciones de vuelo adecuadas y proporciona información básica del vuelo, incluyendo ID de vuelo, número de vuelo, ciudad de origen, ciudad de destino, ubicación del aeropuerto de salida, ubicación del aeropuerto de llegada, hora de salida, hora de llegada y etiquetas de vuelo.",
        "preconditions": "El usuario solicita reservar un vuelo y proporciona palabras clave relacionadas con el vuelo o ubicaciones.",
        "postconditions": "Devuelve una lista de vuelos que cumplen con los criterios. Si se necesita ver los detalles del vuelo (lista de tipos de asientos, precio, fecha, etc.), se debe usar la herramienta de consulta de detalles de vuelo. Guía al usuario para seleccionar un vuelo.",
        "args": {
            "departure": "Ciudad de salida",
            "destination": "Ciudad de destino"
        },
        "returns": "Salida estructurada de la información básica del vuelo.",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Basado en las necesidades de ubicación y preferencias del usuario, recomienda opciones de tren adecuadas y proporciona información básica sobre los boletos de tren, que incluye ID del tren, número de tren, ciudad de origen, ciudad de destino, ubicación de la estación de origen, ubicación de la estación de destino, hora de salida, hora de llegada y etiquetas del tren.",
        "preconditions": "El usuario solicita reservar un tren y proporciona palabras clave relacionadas con el tren o ubicaciones.",
        "postconditions": "Devuelve una lista de boletos de tren que cumplen con los criterios. Si se necesita ver los detalles del boleto (lista de tipos de asientos, precio, fecha, etc.), se debe usar la herramienta de consulta de detalles de boletos de tren. Guía al usuario para seleccionar un boleto de tren.",
        "args": {
            "departure": "Ciudad de origen",
            "destination": "Ciudad de destino",
            "date": "Fecha de salida"
        },
        "returns": "Salida estructurada de la información básica del tren.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Cuando un usuario reserva un hotel, el sistema genera un pedido basándose en las necesidades del usuario (como el nombre del hotel, la fecha de entrada, el número de personas, etc.)",
        "preconditions": "El usuario ha iniciado sesión y proporcionado una identificación válida (user_id), el usuario ha proporcionado un nombre de hotel válido (hotel_name) y un tipo de habitación (room_type), el sistema tiene información sobre el hotel objetivo y el hotel tiene habitaciones disponibles en las fechas solicitadas",
        "postconditions": "Se genera el pedido y se solicita al usuario que confirme el pago",
        "args": {
            "hotel_id": "ID del hotel",
            "room_id": "ID de la habitación",
            "user_id": "ID del usuario"
        },
        "returns": "Salida de retroalimentación de la operación de creación de pedido",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "El usuario compra entradas según la atracción y la fecha; el sistema devuelve la información relevante de las entradas y realiza el pedido.",
        "preconditions": "En el escenario de turismo de atracciones, el usuario solicita reservar una atracción y proporciona la información necesaria relacionada con la reserva.",
        "postconditions": "Se genera el pedido y se solicita al usuario que confirme el pago.",
        "args": {
            "attraction_id": "ID de la atracción",
            "ticket_id": "ID de la entrada",
            "user_id": "ID del usuario",
            "date": "Fecha de visita, formato %Y-%m-%d",
            "quantity": "Cantidad"
        },
        "returns": "Salida de retroalimentación de la operación de creación de pedido.",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "El usuario compra billetes de avión basándose en el número de vuelo, la fecha, el tipo de asiento y la cantidad; el sistema devuelve la información relevante del billete y realiza el pedido.",
        "preconditions": "En el escenario de consulta y compra de billetes, el usuario solicita reservar un vuelo y proporciona la información necesaria relacionada con la reserva.",
        "postconditions": "Se genera el pedido y se solicita al usuario que confirme el pago.",
        "args": {
            "flight_id": "ID del vuelo",
            "seat_id": "ID del asiento",
            "user_id": "ID del usuario",
            "date": "Fecha de salida",
            "quantity": "Cantidad"
        },
        "returns": "Salida de retroalimentación de la operación de creación del pedido.",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "El usuario compra boletos de tren según el número del tren, la fecha, el tipo de asiento y la cantidad; el sistema devuelve la información relevante del boleto de tren y realiza el pedido.",
        "preconditions": "En el escenario de consulta y compra de boletos de tren, el usuario solicita reservar un tren y proporciona la información necesaria relacionada con la reserva.",
        "postconditions": "Se genera el pedido, se solicita al usuario que confirme el pago.",
        "args": {
            "train_id": "ID del tren",
            "seat_id": "ID del asiento",
            "user_id": "ID del usuario",
            "date": "Fecha de salida",
            "quantity": "Cantidad"
        },
        "returns": "Resultado de la operación de creación del pedido.",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "El usuario realiza el pago del pedido del hotel",
        "preconditions": "En el escenario de consulta y reserva de hoteles, el usuario solicita pagar el pedido del hotel y el ID del pedido se ha determinado previamente",
        "postconditions": "Confirmar el pago y actualizar el estado del pedido a pagado",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del resultado del pago",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "El usuario realiza el pago del pedido de entradas",
        "preconditions": "En el escenario de turismo en atracciones, el usuario solicita pagar el pedido de entradas de la atracción y el ID del pedido se ha determinado previamente.",
        "postconditions": "Se confirma el pago y se actualiza el estado del pedido a pagado.",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información sobre el resultado del pago",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "El usuario realiza el pago del pedido del billete de avión",
        "preconditions": "En el escenario de consulta y compra de billetes de avión, el usuario solicita pagar el pedido del vuelo y el ID del pedido se ha determinado anteriormente",
        "postconditions": "Confirmar el pago y actualizar el estado del pedido a pagado",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del resultado del pago",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "El usuario realiza el pago del pedido de billetes de tren",
        "preconditions": "En el escenario de consulta y compra de billetes de tren, el usuario solicita pagar el pedido de billetes de tren y el ID del pedido se ha determinado anteriormente",
        "postconditions": "Confirmar el pago y actualizar el estado del pedido a pagado",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Información del resultado del pago",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Según el ID de usuario, consulta los pedidos de hotel del usuario, devolviendo el ID del pedido, el tipo de pedido, el ID de usuario, el ID del hotel, el precio total del pedido, la fecha y hora del pedido, la fecha y hora de actualización y el estado del pedido.",
        "preconditions": "El usuario necesita consultar pedidos de hotel.",
        "postconditions": "Devuelve la información del pedido para facilitar su modificación o cancelación posterior.",
        "args": {
            "user_id": "ID de usuario",
            "date": "Fecha",
            "status": "Estado del pedido"
        },
        "returns": "Información de los pedidos de hotel del usuario especificado.",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Consulta los pedidos de entradas de atracciones del usuario según su ID, devolviendo el ID del pedido, el tipo de pedido, el ID de usuario, el ID de la atracción, el precio total del pedido, la hora del pedido, la hora de actualización y el estado del pedido.",
        "preconditions": "El usuario necesita consultar pedidos de entradas de atracciones.",
        "postconditions": "Devuelve la información del pedido para facilitar su modificación o cancelación posterior.",
        "args": {
            "user_id": "ID de usuario",
            "date": "Fecha",
            "status": "Estado del pedido"
        },
        "returns": "Información de los pedidos de entradas de atracciones del usuario especificado.",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Consulta los pedidos de boletos de avión del usuario según el ID de usuario, devolviendo el ID del pedido, el tipo de pedido, el ID de usuario, el ID del vuelo, el precio total del pedido, la hora del pedido, la hora de actualización y el estado del pedido.",
        "preconditions": "La necesidad del usuario es consultar pedidos de boletos de avión.",
        "postconditions": "Devuelve la información del pedido, facilitando su modificación o cancelación posterior.",
        "args": {
            "user_id": "ID de usuario",
            "date": "Fecha",
            "status": "Estado del pedido"
        },
        "returns": "Información de los pedidos de boletos de avión del usuario especificado.",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Consulta los pedidos de billetes de tren del usuario según el ID de usuario, devolviendo el ID del pedido, el tipo de pedido, el ID de usuario, el ID del tren, el precio total del pedido, la fecha de realización, la fecha de actualización y el estado del pedido.",
        "preconditions": "El usuario necesita consultar pedidos de billetes de tren.",
        "postconditions": "Devuelve la información del pedido, facilitando su modificación o cancelación posterior.",
        "args": {
            "user_id": "ID de usuario",
            "date": "Fecha",
            "status": "Estado del pedido"
        },
        "returns": "Información de los pedidos de billetes de tren del usuario especificado.",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Obtener detalles del pedido del hotel, incluyendo ID del pedido, tipo de pedido, ID del usuario, ID del hotel, precio total del pedido, hora del pedido, hora de actualización, estado del pedido e información detallada de la habitación del pedido (tipo de habitación, fecha de entrada, precio, ID de la habitación)",
        "preconditions": "El usuario solicita obtener los detalles del pedido del hotel y el ID del pedido se ha determinado en el contexto anterior",
        "postconditions": "Devolver detalles del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Detalles del pedido",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Obtener detalles del pedido de entradas para atracciones, incluyendo ID del pedido, tipo de pedido, ID de usuario, ID de atracción, precio total del pedido, hora del pedido, hora de actualización, estado del pedido e información detallada de la atracción del pedido (tipo de entrada, fecha, precio, ID de entrada)",
        "preconditions": "El usuario solicita obtener los detalles del pedido de entradas para atracciones, el ID del pedido se ha determinado anteriormente",
        "postconditions": "Devolver detalles del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Detalles del pedido",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Obtener detalles del pedido de billete de avión, incluyendo ID del pedido, tipo de pedido, ID de usuario, ID de vuelo, precio total del pedido, hora del pedido, hora de actualización, estado del pedido e información detallada del billete del pedido (tipo de asiento, fecha, precio, ID de asiento)",
        "preconditions": "El usuario solicita obtener los detalles del pedido del billete de avión y el ID del pedido se ha identificado previamente",
        "postconditions": "Devolver detalles del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Detalles del pedido",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Obtener detalles del pedido de billete de tren, incluyendo ID del pedido, tipo de pedido, ID de usuario, ID del tren, precio total del pedido, hora del pedido, hora de actualización, estado del pedido e información detallada del billete de tren del pedido (tipo de asiento, fecha, precio, ID de asiento)",
        "preconditions": "El usuario solicita obtener los detalles del pedido del billete de tren y el ID del pedido se ha determinado en el contexto anterior",
        "postconditions": "Devolver detalles del pedido",
        "args": {
            "order_id": "ID del pedido"
        },
        "returns": "Detalles del pedido",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Modifica el pedido de billetes de tren, permite cambiar la fecha de salida y gestiona automáticamente el pago o reembolso de la diferencia de precio.",
        "preconditions": "En el escenario de consulta y compra de billetes de tren, el usuario solicita modificar el pedido de billetes de tren y el ID del pedido se ha determinado en el contexto anterior.",
        "postconditions": "Modifica el pedido y actualiza el estado del pedido. Si es necesario pagar la diferencia, el estado del pedido cambia a unpaid; de lo contrario, mantiene el estado original. Si es necesario pagar la diferencia, se debe guiar al usuario para pagar este pedido.",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario",
            "new_date": "Nueva fecha de salida, formato %Y-%m-%d"
        },
        "returns": "(Contenido del pedido modificado, diferencia de precio, positivo indica pago de diferencia, negativo indica reembolso de diferencia)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Modifica el pedido del billete de avión, permite cambiar la fecha de salida y gestiona automáticamente el pago o reembolso de la diferencia de precio.",
        "preconditions": "En el escenario de consulta y compra de billetes de avión, el usuario solicita modificar el pedido del billete y el ID del pedido se ha determinado anteriormente.",
        "postconditions": "Modifica el pedido y actualiza el estado del pedido. Si se requiere pagar la diferencia, el estado del pedido cambia a unpaid; de lo contrario, mantiene el estado original. Si se requiere pagar la diferencia, se debe guiar al usuario para pagar este pedido.",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario",
            "new_date": "Nueva fecha de salida, formato %Y-%m-%d"
        },
        "returns": "(Contenido del pedido modificado, diferencia de precio, positivo indica pago de diferencia, negativo indica reembolso de diferencia)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "El usuario cancela un pedido de hotel ya confirmado",
        "preconditions": "En el escenario de consulta de reservas de hotel, el usuario solicita cancelar el pedido del hotel y el ID del pedido se ha determinado previamente",
        "postconditions": "Cancelar el pedido y actualizar el estado del pedido; si es necesario reembolsar la diferencia, simplemente informar al usuario",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario"
        },
        "returns": "El monto del reembolso por cancelar el pedido",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "El usuario cancela un pedido de entradas para atracciones previamente reservado",
        "preconditions": "El ID del pedido está en el historial del diálogo o ya se ha consultado el pedido, y el usuario tiene permiso para cancelar este pedido",
        "postconditions": "Si hay una diferencia a reembolsar, simplemente infórmelo al usuario",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario"
        },
        "returns": "Monto del reembolso por la cancelación del pedido",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "El usuario cancela un pedido de boleto de avión reservado",
        "preconditions": "Hay un ID de pedido en el historial de la conversación o ya se ha realizado una consulta de pedido, y el usuario tiene permiso para cancelar este pedido",
        "postconditions": "Si se reembolsa la diferencia, simplemente infórmelo al usuario",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario"
        },
        "returns": "Monto del reembolso por la cancelación del pedido",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "El usuario cancela un pedido de billete de tren ya reservado",
        "preconditions": "Existe un ID de pedido en el historial de conversación o ya se ha realizado una consulta del pedido, y el usuario tiene permiso para cancelarlo",
        "postconditions": "Si hay un reembolso por la diferencia, simplemente infórmelo al usuario",
        "args": {
            "order_id": "ID del pedido",
            "user_id": "ID del usuario"
        },
        "returns": "El monto del reembolso por cancelar el pedido",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Thai version
TOOL_DESCRIPTIONS_TH = {
    "get_ota_hotel_info": {
        "description": "ดึงข้อมูลโรงแรม รวมถึงรหัสโรงแรม ชื่อ คะแนนประเมิน ระดับดาว ที่อยู่ แท็ก และรายการห้อง",
        "preconditions": "ในบริบทการค้นหาและจองโรงแรม ต้องการดึงข้อมูลรายละเอียดของโรงแรม",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของโรงแรม และนำทางผู้ใช้ให้เลือกห้องและทำการจอง",
        "args": {
            "hotel_id": "รหัสโรงแรม"
        },
        "returns": "ข้อมูลโรงแรม",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "รับข้อมูลสถานที่ท่องเที่ยว ประกอบด้วยรหัสสถานที่ท่องเที่ยว ชื่อ ที่อยู่ คำอธิบาย คะแนน เวลาเปิดทำการ ราคาบัตรเข้าชม และรายการประเภทบัตร",
        "preconditions": "ในสถานการณ์การท่องเที่ยวสถานที่ท่องเที่ยว เมื่อต้องการรับข้อมูลรายละเอียดของสถานที่ท่องเที่ยว",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของสถานที่ท่องเที่ยว และแนะนำผู้ใช้ให้เลือกประเภทบัตรและดำเนินการสั่งซื้อ",
        "args": {
            "attraction_id": "รหัสสถานที่ท่องเที่ยว"
        },
        "returns": "ข้อมูลสถานที่ท่องเที่ยว",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "รับข้อมูลเที่ยวบิน ประกอบด้วย รหัสเที่ยวบิน, หมายเลขเที่ยวบิน, เมืองต้นทาง, เมืองปลายทาง, ตำแหน่งสนามบินต้นทาง, ตำแหน่งสนามบินปลายทาง, เวลาออกเดินทาง, เวลาถึงเดินทาง, แท็กเที่ยวบิน, รายการประเภทที่นั่ง",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วเครื่องบิน ที่ต้องการรับข้อมูลรายละเอียดของเที่ยวบิน",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของเที่ยวบิน และนำทางผู้ใช้ให้เลือกที่นั่งและทำการสั่งซื้อ",
        "args": {
            "flight_id": "รหัสเที่ยวบิน"
        },
        "returns": "ข้อมูลเที่ยวบิน",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "รับข้อมูลรถไฟ รวมถึงรหัสรถไฟ หมายเลขขบวนรถไฟ เมืองต้นทาง เมืองปลายทาง ตำแหน่งสถานีต้นทาง ตำแหน่งสถานีปลายทาง เวลาออกเดินทาง เวลาถึงปลายทาง แท็กรถไฟ และรายการประเภทรถนั่ง",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วรถไฟ จำเป็นต้องรับข้อมูลรายละเอียดของรถไฟ",
        "postconditions": "ส่งคืนข้อมูลรายละเอียดของรถไฟ นำทางผู้ใช้ให้เลือกที่นั่งและสั่งซื้อ",
        "args": {
            "train_id": "รหัสรถไฟ"
        },
        "returns": "ข้อมูลรถไฟ",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "ในบริบทของการเดินทางและที่พัก โดยอ้างอิงจากความต้องการสถานที่และความชอบของผู้ใช้ แนะนำตัวเลือกโรงแรมที่เหมาะสม พร้อมให้ข้อมูลพื้นฐานของโรงแรม ซึ่งรวมถึงรหัสโรงแรม ชื่อ คะแนน ระดับดาว ที่อยู่ และแท็ก",
        "preconditions": "ผู้ใช้ต้องการจองโรงแรม และระบุคำสำคัญหรือสถานที่ที่เกี่ยวข้องกับโรงแรม",
        "postconditions": "ส่งคืนรายการโรงแรมที่ตรงตามเงื่อนไข หากต้องการดูรายละเอียดโรงแรม (รายการห้อง ราคา ฯลฯ) จำเป็นต้องใช้เครื่องมือค้นหาข้อมูลรายละเอียดโรงแรม และแนะนำผู้ใช้ให้เลือกโรงแรม",
        "args": {
            "city_name": "ชื่อเมือง",
            "key_words": "คำสำคัญสำหรับการค้นหา (จับคู่ชื่อโรงแรม คำอธิบายโรงแรม ฯลฯ)"
        },
        "returns": "ผลลัพธ์เป็นข้อมูลพื้นฐานของโรงแรมแบบมีโครงสร้าง",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "แนะนำตัวเลือกสถานที่ท่องเที่ยวที่เหมาะสมตามความต้องการและความชอบเกี่ยวกับสถานที่ของผู้ใช้ ให้ข้อมูลพื้นฐานของสถานที่ท่องเที่ยว รวมถึงรหัสสถานที่ท่องเที่ยว ชื่อ ที่อยู่ คำอธิบาย คะแนน และเวลาเปิดทำการ",
        "preconditions": "ผู้ใช้ขอจองสถานที่ท่องเที่ยว และให้คำสำคัญหรือสถานที่ที่เกี่ยวข้องกับสถานที่ท่องเที่ยว",
        "postconditions": "ส่งคืนรายการสถานที่ท่องเที่ยวที่ตรงตามเงื่อนไข หากต้องการดูรายละเอียดสถานที่ท่องเที่ยว (รายการตั๋ว ราคา ฯลฯ) จำเป็นต้องใช้เครื่องมือค้นหาข้อมูลรายละเอียดสถานที่ท่องเที่ยว และแนะนำผู้ใช้ให้เลือกสถานที่ท่องเที่ยว",
        "args": {
            "city_name": "ชื่อเมือง",
            "key_words": "คำสำคัญสำหรับการค้นหา (จับคู่ชื่อสถานที่ท่องเที่ยว ตำแหน่ง ที่อยู่ ลักษณะพิเศษ ฯลฯ)"
        },
        "returns": "เอาต์พุตข้อมูลพื้นฐานของสถานที่ท่องเที่ยวแบบมีโครงสร้าง",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "แนะนำตัวเลือกเที่ยวบินที่เหมาะสมตามความต้องการและความชอบด้านสถานที่ของผู้ใช้ ให้ข้อมูลพื้นฐานของเที่ยวบิน ได้แก่ รหัสเที่ยวบิน หมายเลขเที่ยวบิน เมืองต้นทาง เมืองปลายทาง ตำแหน่งสนามบินต้นทาง ตำแหน่งสนามบินปลายทาง เวลาออกเดินทาง เวลาถึง และป้ายกำกับเที่ยวบิน",
        "preconditions": "ผู้ใช้ขอจองเที่ยวบิน และให้คำสำคัญหรือสถานที่ที่เกี่ยวข้องกับเที่ยวบิน",
        "postconditions": "ส่งคืนรายการเที่ยวบินที่ตรงตามเงื่อนไข หากต้องการดูรายละเอียดเที่ยวบิน (รายการประเภทที่นั่ง ราคา วันที่ ฯลฯ) จำเป็นต้องใช้เครื่องมือค้นหารายละเอียดเที่ยวบิน และแนะนำผู้ใช้ให้เลือกเที่ยวบิน",
        "args": {
            "departure": "เมืองต้นทาง",
            "destination": "เมืองปลายทาง"
        },
        "returns": "ผลลัพธ์ข้อมูลพื้นฐานของเที่ยวบินแบบมีโครงสร้าง",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "แนะนำตัวเลือกรถไฟที่เหมาะสมตามความต้องการและความชอบเกี่ยวกับสถานที่ของผู้ใช้ ให้ข้อมูลพื้นฐานของตั๋วรถไฟ รวมถึงรหัสรถไฟ หมายเลขขบวน เมืองต้นทาง เมืองปลายทาง ตำแหน่งสถานีต้นทาง ตำแหน่งสถานีปลายทาง เวลาออกเดินทาง เวลาถึง และป้ายกำกับรถไฟ",
        "preconditions": "ผู้ใช้ขอจองรถไฟ และให้คำสำคัญหรือสถานที่ที่เกี่ยวข้องกับรถไฟ",
        "postconditions": "ส่งคืนรายการตั๋วรถไฟที่ตรงตามเงื่อนไข หากต้องการดูรายละเอียดตั๋วรถไฟ (รายการประเภทที่นั่ง ราคา วันที่ ฯลฯ) จำเป็นต้องใช้เครื่องมือสอบถามรายละเอียดตั๋วรถไฟ และแนะนำผู้ใช้ให้เลือกตั๋วรถไฟ",
        "args": {
            "departure": "เมืองต้นทาง",
            "destination": "เมืองปลายทาง",
            "date": "วันที่ออกเดินทาง"
        },
        "returns": "ส่งออกข้อมูลพื้นฐานของรถไฟแบบมีโครงสร้าง",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "เมื่อผู้ใช้จองโรงแรม ระบบจะสร้างคำสั่งซื้อตามความต้องการของผู้ใช้ (เช่น ชื่อโรงแรม วันที่เช็คอิน จำนวนคน ฯลฯ)",
        "preconditions": "ผู้ใช้เข้าสู่ระบบแล้วและระบุตัวตนที่ถูกต้อง (user_id), ผู้ใช้ระบุชื่อโรงแรม (hotel_name) และประเภทห้อง (room_type) ที่ถูกต้อง, ระบบมีข้อมูลเกี่ยวกับโรงแรมเป้าหมาย และโรงแรมนั้นมีห้องว่างในวันที่ร้องขอ",
        "postconditions": "สร้างคำสั่งซื้อแล้ว, โปรดให้ผู้ใช้ยืนยันการชำระเงิน",
        "args": {
            "hotel_id": "รหัสโรงแรม",
            "room_id": "รหัสห้อง",
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "ผลลัพธ์การตอบกลับจากการดำเนินการสร้างคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "ผู้ใช้ซื้อตั๋วเข้าชมตามสถานที่ท่องเที่ยวและวันที่ ระบบจะส่งคืนข้อมูลเกี่ยวกับตั๋วและดำเนินการสร้างคำสั่งซื้อ",
        "preconditions": "ในสถานการณ์การท่องเที่ยวสถานที่ท่องเที่ยว ผู้ใช้ขอจองสถานที่ท่องเที่ยวและได้ระบุข้อมูลที่จำเป็นสำหรับการจอง",
        "postconditions": "สร้างคำสั่งซื้อ และขอให้ผู้ใช้ยืนยันการชำระเงิน",
        "args": {
            "attraction_id": "รหัสสถานที่ท่องเที่ยว",
            "ticket_id": "รหัสตั๋วเข้าชม",
            "user_id": "รหัสผู้ใช้",
            "date": "วันที่เข้าชม รูปแบบ %Y-%m-%d",
            "quantity": "จำนวน"
        },
        "returns": "ผลลัพธ์การตอบกลับจากการดำเนินการสร้างคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "ผู้ใช้ซื้อตั๋วเครื่องบินโดยระบุหมายเลขเที่ยวบิน วันที่ ประเภทที่นั่ง และจำนวน ระบบจะส่งคืนข้อมูลตั๋วเครื่องบินที่เกี่ยวข้องและดำเนินการสร้างคำสั่งซื้อ",
        "preconditions": "ในบริบทการค้นหาและซื้อตั๋วเครื่องบิน ผู้ใช้ต้องการจองเที่ยวบินและได้ให้ข้อมูลที่จำเป็นสำหรับการจองแล้ว",
        "postconditions": "สร้างคำสั่งซื้อแล้ว โปรดให้ผู้ใช้ยืนยันการชำระเงิน",
        "args": {
            "flight_id": "รหัสเที่ยวบิน",
            "seat_id": "รหัสที่นั่ง",
            "user_id": "รหัสผู้ใช้",
            "date": "วันที่ออกเดินทาง",
            "quantity": "จำนวน"
        },
        "returns": "ผลลัพธ์การตอบกลับจากการดำเนินการสร้างคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "ผู้ใช้ซื้อตั๋วรถไฟโดยระบุหมายเลขขบวน วันที่ ประเภทที่นั่ง และจำนวน ระบบจะส่งคืนข้อมูลเกี่ยวกับตั๋วรถไฟและดำเนินการสร้างคำสั่งซื้อ",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วรถไฟ ผู้ใช้ร้องขอการจองรถไฟและให้ข้อมูลที่จำเป็นที่เกี่ยวข้องกับการจอง",
        "postconditions": "สร้างคำสั่งซื้อแล้ว กรุณาให้ผู้ใช้ยืนยันการชำระเงิน",
        "args": {
            "train_id": "รหัสรถไฟ",
            "seat_id": "รหัสที่นั่ง",
            "user_id": "รหัสผู้ใช้",
            "date": "วันที่ออกเดินทาง",
            "quantity": "จำนวน"
        },
        "returns": "ผลลัพธ์การตอบกลับจากการดำเนินการสร้างคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "ผู้ใช้ดำเนินการชำระเงินสำหรับคำสั่งซื้อโรงแรม",
        "preconditions": "ในสถานการณ์การค้นหาและจองโรงแรม เมื่อผู้ใช้ขอชำระเงินสำหรับคำสั่งซื้อโรงแรม และมีการระบุรหัสคำสั่งซื้อแล้วในบริบทก่อนหน้า",
        "postconditions": "ยืนยันการชำระเงินและอัปเดตสถานะคำสั่งซื้อเป็นชำระแล้ว",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "ผู้ใช้ทำการชำระเงินคำสั่งซื้อตั๋ว",
        "preconditions": "ในสถานการณ์การท่องเที่ยวสถานที่ท่องเที่ยว ผู้ใช้ขอชำระเงินคำสั่งซื้อตั๋วสถานที่ท่องเที่ยว และบริบทก่อนหน้าได้ระบุรหัสคำสั่งซื้อแล้ว",
        "postconditions": "ยืนยันการชำระเงินและอัปเดตสถานะคำสั่งซื้อเป็นชำระเงินแล้ว",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "ผู้ใช้ทำการชำระเงินคำสั่งซื้อตั๋วเครื่องบิน",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วเครื่องบิน ผู้ใช้ขอชำระเงินคำสั่งซื้อเที่ยวบิน และรหัสคำสั่งซื้อได้ถูกกำหนดไว้ในบริบทก่อนหน้า",
        "postconditions": "ยืนยันการชำระเงินและอัปเดตสถานะคำสั่งซื้อเป็นชำระแล้ว",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "ผู้ใช้ทำการชำระเงินสำหรับคำสั่งซื้อตั๋วรถไฟ",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วรถไฟ ผู้ใช้ขอชำระเงินสำหรับคำสั่งซื้อตั๋วรถไฟ และรหัสคำสั่งซื้อได้รับการระบุไว้ในบริบทก่อนหน้า",
        "postconditions": "ยืนยันการชำระเงินและอัปเดตสถานะคำสั่งซื้อเป็นชำระเงินแล้ว",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "ข้อมูลผลการชำระเงิน",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "ค้นหาคำสั่งซื้อโรงแรมของผู้ใช้ตาม ID ผู้ใช้ โดยส่งคืนข้อมูลซึ่งรวมถึง ID คำสั่งซื้อ ประเภทคำสั่งซื้อ ID ผู้ใช้ ID โรงแรม ราคารวมคำสั่งซื้อ เวลาสั่งซื้อ เวลาอัปเดต และสถานะคำสั่งซื้อ",
        "preconditions": "ความต้องการของผู้ใช้คือการค้นหาคำสั่งซื้อโรงแรม",
        "postconditions": "ส่งคืนข้อมูลคำสั่งซื้อ เพื่อความสะดวกในการแก้ไข/ยกเลิกในภายหลัง",
        "args": {
            "user_id": "ID ผู้ใช้",
            "date": "วันที่",
            "status": "สถานะคำสั่งซื้อ"
        },
        "returns": "ข้อมูลคำสั่งซื้อโรงแรมของผู้ใช้ที่ระบุ",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "ตามรหัสผู้ใช้ ค้นหาคำสั่งซื้อตั๋วสถานที่ท่องเที่ยวของผู้ใช้ ส่งคืนข้อมูลที่มีรหัสคำสั่งซื้อ ประเภทคำสั่งซื้อ รหัสผู้ใช้ รหัสสถานที่ท่องเที่ยว ราคารวมของคำสั่งซื้อ เวลาสั่งซื้อ เวลาอัปเดต และสถานะคำสั่งซื้อ",
        "preconditions": "ความต้องการของผู้ใช้คือการค้นหาคำสั่งซื้อตั๋วสถานที่ท่องเที่ยว",
        "postconditions": "ส่งคืนข้อมูลคำสั่งซื้อ เพื่ออำนวยความสะดวกในการแก้ไขหรือยกเลิกในภายหลัง",
        "args": {
            "user_id": "รหัสผู้ใช้",
            "date": "วันที่",
            "status": "สถานะคำสั่งซื้อ"
        },
        "returns": "ข้อมูลคำสั่งซื้อตั๋วสถานที่ท่องเที่ยวของผู้ใช้ที่ระบุ",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "ค้นหาคำสั่งซื้อตั๋วเครื่องบินของผู้ใช้ตาม ID ผู้ใช้ ส่งคืนข้อมูลประกอบด้วย ID คำสั่งซื้อ, ประเภทคำสั่งซื้อ, ID ผู้ใช้, ID เที่ยวบิน, ยอดรวมคำสั่งซื้อ, เวลาสั่งซื้อ, เวลาแก้ไขล่าสุด และสถานะคำสั่งซื้อ",
        "preconditions": "ความต้องการของผู้ใช้คือการค้นหาคำสั่งซื้อตั๋วเครื่องบิน",
        "postconditions": "ส่งคืนข้อมูลคำสั่งซื้อ เพื่อความสะดวกในการแก้ไขหรือยกเลิกในภายหลัง",
        "args": {
            "user_id": "ID ผู้ใช้",
            "date": "วันที่",
            "status": "สถานะคำสั่งซื้อ"
        },
        "returns": "ข้อมูลคำสั่งซื้อตั๋วเครื่องบินของผู้ใช้ที่ระบุ",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "ค้นหาคำสั่งซื้อตั๋วรถไฟของผู้ใช้ตาม ID ผู้ใช้ โดยส่งคืนข้อมูลที่มี ID คำสั่งซื้อ, ประเภทคำสั่งซื้อ, ID ผู้ใช้, ID รถไฟ, ราคารวมของคำสั่งซื้อ, เวลาสั่งซื้อ, เวลาอัปเดต และสถานะคำสั่งซื้อ",
        "preconditions": "ความต้องการของผู้ใช้คือการค้นหาคำสั่งซื้อตั๋วรถไฟ",
        "postconditions": "ส่งคืนข้อมูลคำสั่งซื้อ เพื่อความสะดวกในการแก้ไขหรือยกเลิกในภายหลัง",
        "args": {
            "user_id": "ID ผู้ใช้",
            "date": "วันที่",
            "status": "สถานะคำสั่งซื้อ"
        },
        "returns": "ข้อมูลคำสั่งซื้อตั๋วรถไฟของผู้ใช้ที่ระบุ",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ดึงรายละเอียดคำสั่งซื้อโรงแรม ซึ่งรวมถึงรหัสคำสั่งซื้อ ประเภทคำสั่งซื้อ รหัสผู้ใช้ รหัสโรงแรม ราคารวมทั้งหมด เวลาสั่งซื้อ เวลาอัปเดต สถานะคำสั่งซื้อ และข้อมูลรายละเอียดห้อง (ประเภทห้อง วันที่เข้าพัก ราคา รหัสห้อง)",
        "preconditions": "ผู้ใช้ต้องการดูรายละเอียดคำสั่งซื้อโรงแรม และมีการระบุรหัสคำสั่งซื้อไปแล้วในบทสนทนาก่อนหน้า",
        "postconditions": "คืนค่ารายละเอียดคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "รายละเอียดคำสั่งซื้อ",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "รับรายละเอียดคำสั่งซื้อตั๋วสถานที่ท่องเที่ยว รวมถึงรหัสคำสั่งซื้อ ประเภทคำสั่งซื้อ รหัสผู้ใช้ รหัสสถานที่ท่องเที่ยว ราคารวมของคำสั่งซื้อ เวลาสั่งซื้อ เวลาอัปเดต สถานะคำสั่งซื้อ และข้อมูลรายละเอียดสถานที่ท่องเที่ยวของคำสั่งซื้อ (ประเภทตั๋ว วันที่ ราคา รหัสตั๋ว)",
        "preconditions": "ผู้ใช้ขอรับรายละเอียดคำสั่งซื้อตั๋วสถานที่ท่องเที่ยว และรหัสคำสั่งซื้อถูกกำหนดไว้ในบริบทก่อนหน้า",
        "postconditions": "ส่งคืนรายละเอียดคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "รายละเอียดคำสั่งซื้อ",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "เรียกดูรายละเอียดคำสั่งซื้อตั๋วเครื่องบิน รวมถึงรหัสคำสั่งซื้อ ประเภทคำสั่งซื้อ รหัสผู้ใช้ รหัสเที่ยวบิน ราคารวมของคำสั่งซื้อ เวลาที่สั่งซื้อ เวลาที่อัปเดต สถานะคำสั่งซื้อ และข้อมูลรายละเอียดตั๋วเครื่องบินของคำสั่งซื้อ (ประเภทที่นั่ง วันที่ ราคา รหัสที่นั่ง)",
        "preconditions": "ผู้ใช้ร้องขอเพื่อดูรายละเอียดคำสั่งซื้อตั๋วเครื่องบิน และรหัสคำสั่งซื้อถูกระบุไว้ในบริบทก่อนหน้า",
        "postconditions": "ส่งคืนรายละเอียดคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "รายละเอียดคำสั่งซื้อ",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ดึงรายละเอียดคำสั่งซื้อตั๋วรถไฟ ประกอบด้วยรหัสคำสั่งซื้อ ประเภทคำสั่งซื้อ รหัสผู้ใช้ รหัสรถไฟ ราคารวมของคำสั่งซื้อ เวลาที่สั่งซื้อ เวลาที่อัปเดต สถานะคำสั่งซื้อ และข้อมูลรายละเอียดตั๋วรถไฟของคำสั่งซื้อ (ประเภทที่นั่ง วันที่ ราคา รหัสที่นั่ง)",
        "preconditions": "ผู้ใช้ร้องขอเพื่อดึงรายละเอียดคำสั่งซื้อตั๋วรถไฟ และรหัสคำสั่งซื้อถูกกำหนดไว้ในบริบทก่อนหน้า",
        "postconditions": "ส่งคืนรายละเอียดคำสั่งซื้อ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ"
        },
        "returns": "รายละเอียดคำสั่งซื้อ",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "แก้ไขคำสั่งซื้อตั๋วรถไฟ รองรับการเปลี่ยนวันที่เดินทาง และจัดการส่วนต่างราคาหรือคืนส่วนต่างราคาโดยอัตโนมัติ",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วรถไฟ เมื่อผู้ใช้ขอแก้ไขคำสั่งซื้อตั๋วรถไฟ และมีการระบุรหัสคำสั่งซื้อในบริบทก่อนหน้า",
        "postconditions": "แก้ไขคำสั่งซื้อและอัปเดตสถานะคำสั่งซื้อ หากต้องชำระส่วนต่างราคา สถานะคำสั่งซื้อจะเปลี่ยนเป็น unpaid มิฉะนั้นคงสถานะเดิม หากต้องชำระส่วนต่างราคา ต้องแนะนำผู้ใช้ให้ชำระคำสั่งซื้อนี้",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้",
            "new_date": "วันที่เดินทางใหม่ รูปแบบ %Y-%m-%d"
        },
        "returns": "(เนื้อหาคำสั่งซื้อที่แก้ไขแล้ว, ส่วนต่างราคา, ค่าบวกหมายถึงต้องชำระส่วนต่าง, ค่าลบหมายถึงได้รับคืนส่วนต่าง)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "แก้ไขคำสั่งซื้อตั๋วเครื่องบิน รองรับการเปลี่ยนวันที่ออกเดินทาง และจัดการส่วนต่างราคาหรือคืนส่วนต่างราคาโดยอัตโนมัติ",
        "preconditions": "ในสถานการณ์การค้นหาและซื้อตั๋วเครื่องบิน เมื่อผู้ใช้ขอแก้ไขคำสั่งซื้อตั๋วเครื่องบิน และมีการระบุรหัสคำสั่งซื้อในบริบทก่อนหน้า",
        "postconditions": "แก้ไขคำสั่งซื้อและอัปเดตสถานะคำสั่งซื้อ หากต้องชำระส่วนต่างราคา สถานะคำสั่งซื้อจะเปลี่ยนเป็น unpaid มิฉะนั้นคงสถานะเดิม หากต้องชำระส่วนต่างราคา ต้องแนะนำผู้ใช้ให้ชำระคำสั่งซื้อนี้",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้",
            "new_date": "วันที่ออกเดินทางใหม่ รูปแบบ %Y-%m-%d"
        },
        "returns": "(เนื้อหาคำสั่งซื้อที่แก้ไขแล้ว, ส่วนต่างราคา, ค่าบวกหมายถึงต้องชำระส่วนต่างราคา, ค่าลบหมายถึงคืนส่วนต่างราคา)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งจองโรงแรมที่ได้จองไว้แล้ว",
        "preconditions": "ในสถานการณ์การค้นหาและจองโรงแรม เมื่อผู้ใช้ขอยกเลิกคำสั่งจองโรงแรม และมีการระบุรหัสคำสั่งซื้อไว้ในบริบทก่อนหน้า",
        "postconditions": "ยกเลิกคำสั่งซื้อและอัปเดตสถานะคำสั่งซื้อ หากจำเป็นต้องคืนเงินส่วนต่าง ให้แจ้งผู้ใช้ทราบ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "จำนวนเงินคืนจากการยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งซื้อตั๋วสถานที่ท่องเที่ยวที่จองไว้แล้ว",
        "preconditions": "มีรหัสคำสั่งซื้อในการสนทนาก่อนหน้า หรือมีการสอบถามคำสั่งซื้อแล้ว และผู้ใช้มีสิทธิ์ยกเลิกคำสั่งซื้อนี้",
        "postconditions": "หากมีการคืนเงินส่วนต่าง ให้แจ้งผู้ใช้ทราบ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "จำนวนเงินที่คืนจากการยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งซื้อตั๋วเครื่องบินที่จองไว้",
        "preconditions": "มีรหัสคำสั่งซื้อในการสนทนาก่อนหน้า หรือมีการสอบถามคำสั่งซื้อแล้ว และผู้ใช้มีสิทธิ์ยกเลิกคำสั่งซื้อนี้",
        "postconditions": "หากมีการคืนเงินส่วนต่าง ให้แจ้งผู้ใช้ทราบ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "จำนวนเงินคืนจากการยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "ผู้ใช้ยกเลิกคำสั่งซื้อตั๋วรถไฟที่จองไว้",
        "preconditions": "มีรหัสคำสั่งซื้อในการสนทนาก่อนหน้า หรือได้ทำการสอบถามคำสั่งซื้อแล้ว และผู้ใช้มีสิทธิ์ยกเลิกคำสั่งซื้อนี้",
        "postconditions": "หากมีการคืนเงินส่วนต่าง ให้แจ้งผู้ใช้ทราบ",
        "args": {
            "order_id": "รหัสคำสั่งซื้อ",
            "user_id": "รหัสผู้ใช้"
        },
        "returns": "จำนวนเงินคืนจากการยกเลิกคำสั่งซื้อ",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Hindi version
TOOL_DESCRIPTIONS_HI = {
    "get_ota_hotel_info": {
        "description": "होटल की जानकारी प्राप्त करें, जिसमें होटल आईडी, नाम, रेटिंग, स्टार रैंकिंग, पता, टैग और कमरों की सूची शामिल है।",
        "preconditions": "होटल खोज और बुकिंग परिदृश्य में, होटल की विस्तृत जानकारी प्राप्त करने की आवश्यकता है।",
        "postconditions": "होटल की विस्तृत जानकारी लौटाएं, उपयोगकर्ता को कमरा चुनने और ऑर्डर देने के लिए मार्गदर्शन करें।",
        "args": {
            "hotel_id": "होटल आईडी"
        },
        "returns": "होटल की जानकारी",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "आकर्षण जानकारी प्राप्त करें, जिसमें आकर्षण आईडी, नाम, पता, विवरण, रेटिंग, खुलने का समय, टिकट की कीमत, टिकट प्रकार की सूची शामिल है।",
        "preconditions": "आकर्षण पर्यटन परिदृश्य में, आकर्षण की विस्तृत जानकारी प्राप्त करने की आवश्यकता है।",
        "postconditions": "आकर्षण की विस्तृत जानकारी लौटाएं, उपयोगकर्ता को टिकट चुनने और ऑर्डर देने के लिए मार्गदर्शन करें।",
        "args": {
            "attraction_id": "आकर्षण आईडी"
        },
        "returns": "आकर्षण जानकारी",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "उड़ान जानकारी प्राप्त करें, जिसमें उड़ान आईडी, उड़ान संख्या, प्रस्थान शहर, आगमन शहर, प्रस्थान हवाई अड्डे का स्थान, आगमन हवाई अड्डे का स्थान, प्रस्थान समय, आगमन समय, उड़ान टैग, सीट प्रकार की सूची शामिल है।",
        "preconditions": "टिकट खोज और खरीद परिदृश्य में, उड़ान की विस्तृत जानकारी प्राप्त करने की आवश्यकता है।",
        "postconditions": "उड़ान की विस्तृत जानकारी लौटाएं, उपयोगकर्ता को सीट चुनने और ऑर्डर देने के लिए मार्गदर्शन करें।",
        "args": {
            "flight_id": "उड़ान आईडी"
        },
        "returns": "उड़ान जानकारी",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "ट्रेन की जानकारी प्राप्त करें, जिसमें ट्रेन आईडी, ट्रेन नंबर, प्रस्थान शहर, आगमन शहर, प्रस्थान स्टेशन का स्थान, आगमन स्टेशन का स्थान, प्रस्थान समय, आगमन समय, ट्रेन टैग, सीट प्रकार की सूची शामिल है।",
        "preconditions": "ट्रेन टिकट खोज और खरीद परिदृश्य में, ट्रेन की विस्तृत जानकारी प्राप्त करने की आवश्यक है।",
        "postconditions": "ट्रेन की विस्तृत जानकारी वापस करें, उपयोगकर्ता को सीट चुनने और ऑर्डर देने के लिए मार्गदर्शन करें।",
        "args": {
            "train_id": "ट्रेन आईडी"
        },
        "returns": "ट्रेन की जानकारी",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "यात्रा और होटल परिदृश्य में, उपयोगकर्ता की स्थान आवश्यकताओं और प्राथमिकताओं के आधार पर, उपयुक्त होटल विकल्पों की अनुशंसा करें, होटल की बुनियादी जानकारी प्रदान करें, जिसमें होटल आईडी, नाम, रेटिंग, स्टार रेटिंग, पता और टैग शामिल हैं।",
        "preconditions": "उपयोगकर्ता होटल बुक करने का अनुरोध करता है और होटल से संबंधित कीवर्ड या स्थान प्रदान करता है।",
        "postconditions": "शर्तों को पूरा करने वाले होटलों की सूची लौटाएं; यदि होटल विवरण (कमरे की सूची, कीमतें आदि) देखने की आवश्यकता है, तो होटल विवरण क्वेरी टूल का उपयोग करना होगा, और उपयोगकर्ता को होटल चुनने के लिए मार्गदर्शन करें।",
        "args": {
            "city_name": "शहर का नाम",
            "key_words": "खोज कीवर्ड (होटल नाम, होटल परिचय आदि से मेल खाता है)"
        },
        "returns": "होटल बुनियादी जानकारी का संरचित आउटपुट",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "उपयोगकर्ता की स्थान आवश्यकताओं और वरीयताओं के आधार पर, उपयुक्त पर्यटन स्थल विकल्पों की अनुशंसा करें, पर्यटन स्थल की बुनियादी जानकारी प्रदान करें, जिसमें स्थल आईडी, नाम, पता, विवरण, रेटिंग, संचालन समय शामिल है",
        "preconditions": "उपयोगकर्ता पर्यटन स्थल का आरक्षण करने का अनुरोध करता है, स्थल से संबंधित कीवर्ड या स्थान प्रदान करता है",
        "postconditions": "शर्तों को पूरा करने वाले पर्यटन स्थलों की सूची लौटाएं, यदि स्थल विवरण (टिकट सूची, कीमत आदि) देखने की आवश्यकता है तो स्थल विवरण क्वेरी टूल का उपयोग करना होगा, उपयोगकर्ता को स्थल चुनने के लिए मार्गदर्शन करें",
        "args": {
            "city_name": "शहर का नाम",
            "key_words": "खोज कीवर्ड (स्थल नाम, स्थान, पता, विशेषताएं आदि से मेल खाते हैं)"
        },
        "returns": "पर्यटन स्थल बुनियादी जानकारी का संरचित आउटपुट",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "उपयोगकर्ता की स्थान आवश्यकताओं और वरीयताओं के आधार पर, उपयुक्त उड़ान विकल्पों की अनुशंसा करें, उड़ान की बुनियादी जानकारी प्रदान करें, जिसमें उड़ान आईडी, उड़ान संख्या, प्रस्थान शहर, आगमन शहर, प्रस्थान हवाई अड्डे का स्थान, आगमन हवाई अड्डे का स्थान, प्रस्थान समय, आगमन समय, उड़ान टैग शामिल हैं।",
        "preconditions": "उपयोगकर्ता उड़ान बुक करने का अनुरोध करता है, उड़ान से संबंधित कीवर्ड या स्थान प्रदान करता है।",
        "postconditions": "शर्तों को पूरा करने वाली उड़ानों की सूची लौटाएं, यदि उड़ान विवरण (सीट प्रकार सूची, कीमत, तिथि आदि) देखने की आवश्यकता है तो उड़ान विवरण क्वेरी टूल का उपयोग करने की आवश्यकता है, उपयोगकर्ता को उड़ान चुनने के लिए मार्गदर्शन करें।",
        "args": {
            "departure": "प्रस्थान शहर",
            "destination": "गंतव्य शहर"
        },
        "returns": "उड़ान की बुनियादी जानकारी का संरचित आउटपुट",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "उपयोगकर्ता की स्थान आवश्यकताओं और वरीयताओं के आधार पर, उपयुक्त ट्रेन विकल्पों की अनुशंसा करें, ट्रेन टिकट की बुनियादी जानकारी प्रदान करें, जिसमें ट्रेन आईडी, ट्रेन नंबर, प्रस्थान शहर, आगमन शहर, प्रस्थान स्टेशन स्थान, आगमन स्टेशन स्थान, प्रस्थान समय, आगमन समय, ट्रेन टैग शामिल हैं।",
        "preconditions": "उपयोगकर्ता ट्रेन बुक करने का अनुरोध करता है, ट्रेन से संबंधित कीवर्ड या स्थान प्रदान करता है।",
        "postconditions": "शर्तों को पूरा करने वाली ट्रेन टिकटों की सूची लौटाएं, यदि ट्रेन टिकट विवरण (सीट प्रकार सूची, मूल्य, तिथि आदि) देखने की आवश्यकता है तो ट्रेन टिकट विवरण जाँच उपकरण का उपयोग करना होगा, उपयोगकर्ता को ट्रेन टिकट चुनने के लिए मार्गदर्शन करें।",
        "args": {
            "departure": "प्रस्थान शहर",
            "destination": "गंतव्य शहर",
            "date": "प्रस्थान तिथि"
        },
        "returns": "ट्रेन की बुनियादी जानकारी का संरचित आउटपुट।",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "जब उपयोगकर्ता होटल बुक करता है, तो सिस्टम उपयोगकर्ता की आवश्यकताओं (जैसे होटल का नाम, चेक-इन की तारीख, लोगों की संख्या आदि) के आधार पर ऑर्डर जनरेट करता है",
        "preconditions": "उपयोगकर्ता लॉग इन हो चुका है और एक मान्य पहचानकर्ता (user_id) प्रदान किया है, उपयोगकर्ता ने एक मान्य होटल का नाम (hotel_name) और कमरे का प्रकार (room_type) प्रदान किया है, सिस्टम के पास लक्षित होटल के बारे में जानकारी है, और उस होटल में अनुरोधित तारीखों पर कमरे उपलब्ध हैं",
        "postconditions": "ऑर्डर जनरेट करें, उपयोगकर्ता से भुगतान की पुष्टि करने के लिए कहें",
        "args": {
            "hotel_id": "होटल आईडी",
            "room_id": "कमरा आईडी",
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "ऑर्डर बनाने की ऑपरेशन की प्रतिक्रिया आउटपुट",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "उपयोगकर्ता आकर्षण और तिथि के आधार पर टिकट खरीदता है, सिस्टम टिकट की संबंधित जानकारी वापस करता है और ऑर्डर प्लेस करता है।",
        "preconditions": "आकर्षण पर्यटन परिदृश्य में, उपयोगकर्ता आकर्षण बुक करने का अनुरोध करता है और बुकिंग से संबंधित आवश्यक जानकारी प्रदान करता है।",
        "postconditions": "ऑर्डर जनरेट करें, उपयोगकर्ता से भुगतान की पुष्टि करने के लिए कहें।",
        "args": {
            "attraction_id": "आकर्षण आईडी",
            "ticket_id": "टिकट आईडी",
            "user_id": "उपयोगकर्ता आईडी",
            "date": "दर्शन की तारीख, प्रारूप %Y-%m-%d है",
            "quantity": "मात्रा"
        },
        "returns": "ऑर्डर बनाने की क्रिया के लिए प्रतिक्रिया आउटपुट",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "उपयोगकर्ता फ्लाइट नंबर, तिथि, सीट प्रकार और मात्रा के आधार पर हवाई टिकट खरीदता है, सिस्टम टिकट की संबंधित जानकारी लौटाता है और ऑर्डर प्लेस करता है",
        "preconditions": "टिकट खोज और खरीद परिदृश्य में, उपयोगकर्ता फ्लाइट बुक करने का अनुरोध करता है और बुकिंग से संबंधित आवश्यक जानकारी प्रदान करता है",
        "postconditions": "ऑर्डर जनरेट करें, उपयोगकर्ता को भुगतान की पुष्टि करने के लिए कहें",
        "args": {
            "flight_id": "फ्लाइट आईडी",
            "seat_id": "सीट आईडी",
            "user_id": "उपयोगकर्ता आईडी",
            "date": "प्रस्थान तिथि",
            "quantity": "मात्रा"
        },
        "returns": "ऑर्डर बनाने की क्रिया का फीडबैक आउटपुट",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "उपयोगकर्ता ट्रेन संख्या, तिथि, सीट प्रकार और मात्रा के आधार पर ट्रेन टिकट खरीदता है; सिस्टम ट्रेन टिकट की संबंधित जानकारी लौटाता है और ऑर्डर प्लेस करता है।",
        "preconditions": "ट्रेन टिकट खोज और खरीद परिदृश्य में, उपयोगकर्ता ट्रेन बुक करने का अनुरोध करता है और बुकिंग से संबंधित आवश्यक जानकारी प्रदान करता है।",
        "postconditions": "ऑर्डर जनरेट करें, उपयोगकर्ता से भुगतान की पुष्टि करने के लिए कहें।",
        "args": {
            "train_id": "ट्रेन आईडी",
            "seat_id": "सीट आईडी",
            "user_id": "उपयोगकर्ता आईडी",
            "date": "प्रस्थान की तारीख",
            "quantity": "मात्रा"
        },
        "returns": "ऑर्डर बनाने की ऑपरेशन की प्रतिक्रिया आउटपुट",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "उपयोगकर्ता होटल ऑर्डर का भुगतान करता है",
        "preconditions": "होटल बुकिंग खोज परिदृश्य में, उपयोगकर्ता होटल ऑर्डर का भुगतान करने का अनुरोध करता है, और पूर्व संदर्भ में ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "भुगतान की पुष्टि करें और ऑर्डर की स्थिति को भुगतान किया गया में अपडेट करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "उपयोगकर्ता टिकट ऑर्डर का भुगतान करता है",
        "preconditions": "पर्यटन स्थल के परिदृश्य में, उपयोगकर्ता स्थल के टिकट ऑर्डर का भुगतान करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "भुगतान की पुष्टि करें और ऑर्डर की स्थिति को भुगतान किया गया में अपडेट करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "उपयोगकर्ता हवाई टिकट ऑर्डर का भुगतान करता है",
        "preconditions": "हवाई टिकट खोज और खरीद परिदृश्य में, उपयोगकर्ता फ्लाइट ऑर्डर का भुगतान करने का अनुरोध करता है, और पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "भुगतान की पुष्टि करें और ऑर्डर की स्थिति को भुगतान किया गया में अपडेट करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "उपयोगकर्ता द्वारा ट्रेन टिकट ऑर्डर का भुगतान करना",
        "preconditions": "ट्रेन टिकट खोज और खरीद के परिदृश्य में, उपयोगकर्ता ट्रेन टिकट ऑर्डर का भुगतान करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "भुगतान की पुष्टि करें और ऑर्डर की स्थिति को भुगतान किया गया में अपडेट करें",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "भुगतान परिणाम जानकारी",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "उपयोगकर्ता आईडी के आधार पर उपयोगकर्ता के होटल ऑर्डर की जाँच करें, और ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, होटल आईडी, ऑर्डर कुल राशि, ऑर्डर करने का समय, अपडेट समय और ऑर्डर स्थिति सहित वापस लौटाएं।",
        "preconditions": "उपयोगकर्ता की आवश्यकता होटल ऑर्डर की जाँच करना है।",
        "postconditions": "ऑर्डर जानकारी वापस लौटाएं, जो बाद में संशोधन या रद्द करने में सुविधाजनक है।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "date": "तारीख",
            "status": "ऑर्डर स्थिति"
        },
        "returns": "निर्दिष्ट उपयोगकर्ता की होटल ऑर्डर जानकारी",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "उपयोगकर्ता आईडी के आधार पर उपयोगकर्ता के पर्यटन स्थल टिकट ऑर्डर की जांच करें, और ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, पर्यटन स्थल आईडी, ऑर्डर कुल राशि, ऑर्डर समय, अपडेट समय और ऑर्डर स्थिति सहित जानकारी लौटाएं।",
        "preconditions": "उपयोगकर्ता की आवश्यकता पर्यटन स्थल टिकट ऑर्डर की जांच करना है।",
        "postconditions": "ऑर्डर जानकारी लौटाएं, बाद में संशोधन/रद्द करने में सुविधा के लिए।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "date": "तारीख",
            "status": "ऑर्डर स्थिति"
        },
        "returns": "निर्दिष्ट उपयोगकर्ता की पर्यटन स्थल टिकट ऑर्डर जानकारी।",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "उपयोगकर्ता आईडी के आधार पर उपयोगकर्ता के हवाई टिकट आदेशों की जांच करें, जिसमें आदेश आईडी, आदेश प्रकार, उपयोगकर्ता आईडी, उड़ान आईडी, आदेश कुल मूल्य, आदेश समय, अपडेट समय और आदेश स्थिति शामिल है।",
        "preconditions": "उपयोगकर्ता की आवश्यकता हवाई टिकट आदेशों की जांच करने की है।",
        "postconditions": "आदेश जानकारी लौटाएं, बाद में संशोधन/रद्द करने में सुविधा के लिए।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "date": "तारीख",
            "status": "आदेश स्थिति"
        },
        "returns": "निर्दिष्ट उपयोगकर्ता की हवाई टिकट आदेश जानकारी।",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "उपयोगकर्ता आईडी के आधार पर उपयोगकर्ता के ट्रेन टिकट ऑर्डर क्वेरी करें, और ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, ट्रेन आईडी, ऑर्डर कुल मूल्य, ऑर्डर समय, अपडेट समय और ऑर्डर स्थिति सहित जानकारी लौटाएं।",
        "preconditions": "उपयोगकर्ता की आवश्यकता ट्रेन टिकट ऑर्डर क्वेरी करना है।",
        "postconditions": "ऑर्डर जानकारी लौटाएं, ताकि बाद में संशोधन या रद्द करना आसान हो।",
        "args": {
            "user_id": "उपयोगकर्ता आईडी",
            "date": "तारीख",
            "status": "ऑर्डर स्थिति"
        },
        "returns": "निर्दिष्ट उपयोगकर्ता की ट्रेन टिकट ऑर्डर जानकारी।",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "होटल ऑर्डर विवरण प्राप्त करें, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, होटल आईडी, ऑर्डर कुल कीमत, ऑर्डर समय, अपडेट समय, ऑर्डर स्थिति और ऑर्डर कमरे की विस्तृत जानकारी (कमरे का प्रकार, चेक-इन तिथि, कीमत, कमरा आईडी) शामिल है।",
        "preconditions": "उपयोगकर्ता होटल ऑर्डर विवरण प्राप्त करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है।",
        "postconditions": "ऑर्डर विवरण लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर विवरण",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "पर्यटन स्थल टिकट ऑर्डर का विवरण प्राप्त करें, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, पर्यटन स्थल आईडी, ऑर्डर की कुल कीमत, ऑर्डर करने का समय, अपडेट का समय, ऑर्डर की स्थिति और ऑर्डर से जुड़े पर्यटन स्थल की विस्तृत जानकारी (टिकट प्रकार, तिथि, कीमत, टिकट आईडी) शामिल है।",
        "preconditions": "उपयोगकर्ता पर्यटन स्थल टिकट ऑर्डर का विवरण प्राप्त करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है।",
        "postconditions": "ऑर्डर विवरण लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर विवरण",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "हवाई टिकट ऑर्डर विवरण प्राप्त करें, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, फ्लाइट आईडी, कुल ऑर्डर मूल्य, ऑर्डर समय, अपडेट समय, ऑर्डर स्थिति और ऑर्डर टिकट विस्तृत जानकारी (सीट प्रकार, तारीख, मूल्य, सीट आईडी) शामिल है।",
        "preconditions": "उपयोगकर्ता हवाई टिकट ऑर्डर विवरण प्राप्त करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है।",
        "postconditions": "ऑर्डर विवरण लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर विवरण",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "ट्रेन टिकट ऑर्डर विवरण प्राप्त करें, जिसमें ऑर्डर आईडी, ऑर्डर प्रकार, उपयोगकर्ता आईडी, ट्रेन आईडी, कुल ऑर्डर मूल्य, ऑर्डर समय, अपडेट समय, ऑर्डर स्थिति और ऑर्डर ट्रेन टिकट विस्तृत जानकारी (सीट प्रकार, तारीख, मूल्य, सीट आईडी) शामिल है।",
        "preconditions": "उपयोगकर्ता ट्रेन टिकट ऑर्डर विवरण प्राप्त करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है।",
        "postconditions": "ऑर्डर विवरण लौटाएं।",
        "args": {
            "order_id": "ऑर्डर आईडी"
        },
        "returns": "ऑर्डर विवरण",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "ट्रेन टिकट ऑर्डर में संशोधन करें, प्रस्थान तिथि बदलने का समर्थन करता है, और मूल्य अंतर के भुगतान या रिफंड को स्वचालित रूप से संभालता है।",
        "preconditions": "ट्रेन टिकट खोज और खरीद के परिदृश्य में, जब उपयोगकर्ता ट्रेन टिकट ऑर्डर संशोधित करने का अनुरोध करता है, और पिछले संदर्भ में ऑर्डर आईडी पहले ही निर्धारित हो चुकी है।",
        "postconditions": "ऑर्डर संशोधित करें और ऑर्डर स्थिति अपडेट करें, यदि मूल्य अंतर का भुगतान आवश्यक है, तो ऑर्डर स्थिति को unpaid में बदलें, अन्यथा मूल स्थिति बनाए रखें, यदि मूल्य अंतर का भुगतान आवश्यक है, तो उपयोगकर्ता को इस ऑर्डर का भुगतान करने के लिए मार्गदर्शन करें।",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी",
            "new_date": "नया प्रस्थान दिनांक, प्रारूप %Y-%m-%d है"
        },
        "returns": "(संशोधित ऑर्डर सामग्री, मूल्य अंतर, धनात्मक का अर्थ है अंतर का भुगतान करना है, ऋणात्मक का अर्थ है अंतर वापस करना है)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "हवाई टिकट ऑर्डर संशोधित करें, प्रस्थान दिनांक बदलने का समर्थन करता है, स्वचालित रूप से मूल्य अंतर भुगतान या रिफंड संभालता है।",
        "preconditions": "हवाई टिकट खोज और खरीद परिदृश्य में, उपयोगकर्ता हवाई टिकट ऑर्डर संशोधित करने का अनुरोध करता है, पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है।",
        "postconditions": "ऑर्डर संशोधित करें और ऑर्डर स्थिति अपडेट करें, यदि मूल्य अंतर का भुगतान करने की आवश्यकता है, तो ऑर्डर स्थिति को unpaid में बदलें, अन्यथा मूल स्थिति बनाए रखें, यदि मूल्य अंतर का भुगतान करने की आवश्यकता है, तो उपयोगकर्ता को इस ऑर्डर का भुगतान करने के लिए मार्गदर्शन करना होगा।",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी",
            "new_date": "नया प्रस्थान दिनांक, प्रारूप %Y-%m-%d है"
        },
        "returns": "(संशोधित ऑर्डर सामग्री, मूल्य अंतर, धनात्मक का अर्थ है अंतर का भुगतान करना है, ऋणात्मक का अर्थ है अंतर वापस किया जाएगा)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "उपयोगकर्ता द्वारा पहले से बुक की गई होटल ऑर्डर को रद्द करना",
        "preconditions": "होटल बुकिंग जांच परिदृश्य में, उपयोगकर्ता होटल ऑर्डर रद्द करने का अनुरोध करता है, और पिछले संदर्भ में ऑर्डर आईडी निर्धारित की गई है",
        "postconditions": "ऑर्डर को रद्द करें और ऑर्डर की स्थिति अपडेट करें; यदि धनवापसी की आवश्यकता है, तो उपयोगकर्ता को सूचित करें",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "ऑर्डर रद्द करने पर धनवापसी की राशि",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "उपयोगकर्ता द्वारा पहले से बुक की गई पर्यटन स्थल टिकट ऑर्डर को रद्द करना",
        "preconditions": "पिछली बातचीत में ऑर्डर आईडी मौजूद हो या पहले ही ऑर्डर जांच की जा चुकी हो, और उपयोगकर्ता के पास इस ऑर्डर को रद्द करने का अधिकार हो।",
        "postconditions": "यदि कोई अंतर राशि वापस की जाती है, तो बस उपयोगकर्ता को सूचित करें।",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "ऑर्डर रद्द करने की वापसी राशि",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "उपयोगकर्ता द्वारा पहले से बुकी गई फ्लाइट टिकट ऑर्डर को रद्द करना",
        "preconditions": "पिछली बातचीत में ऑर्डर आईडी मौजूद हो या पहले ही ऑर्डर क्वेरी की जा चुकी हो, और उपयोगकर्ता के पास इस ऑर्डर को रद्द करने का अधिकार हो",
        "postconditions": "यदि कोई मूल्य अंतर वापस किया जाता है, तो केवल उपयोगकर्ता को सूचित करें",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "ऑर्डर रद्द करने पर वापस की गई राशि",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "उपयोगकर्ता द्वारा पहले से बुकी गई ट्रेन टिकट ऑर्डर को रद्द करना",
        "preconditions": "पिछली बातचीत में ऑर्डर आईडी मौजूद होनी चाहिए या ऑर्डर क्वेरी पहले ही की जा चुकी होनी चाहिए, और उपयोगकर्ता के पास इस ऑर्डर को रद्द करने का अधिकार होना चाहिए।",
        "postconditions": "यदि अंतर राशि वापस की जाती है, तो केवल उपयोगकर्ता को सूचित करें।",
        "args": {
            "order_id": "ऑर्डर आईडी",
            "user_id": "उपयोगकर्ता आईडी"
        },
        "returns": "ऑर्डर रद्द करने पर वापस की गई राशि",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Arabic version
TOOL_DESCRIPTIONS_AR = {
    "get_ota_hotel_info": {
        "description": "الحصول على معلومات الفندق، تتضمن معرف الفندق، الاسم، التقييم، التصنيف النجمي، العنوان، العلامات، وقائمة الغرف",
        "preconditions": "في سياق البحث عن فندق وحجزه، يجب الحصول على المعلومات التفصيلية للفندق",
        "postconditions": "إرجاع المعلومات التفصيلية للفندق، وتوجيه المستخدم لاختيار الغرفة وإتمام الحجز",
        "args": {
            "hotel_id": "معرف الفندق"
        },
        "returns": "معلومات الفندق",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "الحصول على معلومات مكان الجذب، وتتضمن معرف مكان الجذب، والاسم، والعنوان، والوصف، والتقييم، وساعات الافتتاح، وسعر التذكرة، وقائمة أنواع التذاكر",
        "preconditions": "في سياق السياحة للمعالم، عند الحاجة إلى الحصول على معلومات تفصيلية عن مكان الجذب",
        "postconditions": "إرجاع المعلومات التفصيلية لمكان الجذب، وتوجيه المستخدم لاختيار التذاكر وإتمام الطلب",
        "args": {
            "attraction_id": "معرف مكان الجذب"
        },
        "returns": "معلومات مكان الجذب",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "الحصول على معلومات الرحلة، بما في ذلك معرف الرحلة، رقم الرحلة، مدينة المغادرة، مدينة الوصول، موقع مطار المغادرة، موقع مطار الوصول، وقت المغادرة، وقت الوصول، علامات الرحلة، قائمة أنواع المقاعد",
        "preconditions": "في سيناريو استعلام وشراء تذاكر الطيران، تحتاج إلى الحصول على معلومات مفصلة عن الرحلة",
        "postconditions": "إرجاع المعلومات التفصيلية للرحلة، وتوجيه المستخدم لاختيار المقعد وإتمام الطلب",
        "args": {
            "flight_id": "معرف الرحلة"
        },
        "returns": "معلومات الرحلة",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "الحصول على معلومات القطار، بما في ذلك معرف القطار، رقم الرحلة، مدينة المغادرة، مدينة الوصول، موقع محطة المغادرة، موقع محطة الوصول، وقت المغادرة، وقت الوصول، وسوم القطار، قائمة أنواع المقاعد",
        "preconditions": "في سيناريو استعلام وشراء تذاكر القطار، يلزم الحصول على المعلومات التفصيلية للقطار",
        "postconditions": "إرجاع المعلومات التفصيلية للقطار، وتوجيه المستخدم لاختيار المقعد وإتمام الطلب",
        "args": {
            "train_id": "معرف القطار"
        },
        "returns": "معلومات القطار",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "في سيناريو السفر والإقامة، وبناءً على احتياجات المستخدم للموقع وتفضيلاته، يوصي بخيارات فنادق مناسبة، ويوفر المعلومات الأساسية للفندق، بما في ذلك معرف الفندق، والاسم، والتقييم، وعدد النجوم، والعنوان، والعلامات",
        "preconditions": "يطلب المستخدم حجز فندق، ويقدم كلمات رئيسية تتعلق بالفندق أو موقعًا",
        "postconditions": "إرجاع قائمة بالفنادق التي تستوفي الشروط، وإذا لزم الأمر عرض تفاصيل الفندق (قائمة الغرف، الأسعار، إلخ) يجب استخدام أداة استعلام تفاصيل الفندق، وتوجيه المستخدم لاختيار الفندق",
        "args": {
            "city_name": "اسم المدينة",
            "key_words": "كلمات البحث الرئيسية (تطابق اسم الفندق، وصف الفندق، إلخ)"
        },
        "returns": "إخراج منظم للمعلومات الأساسية للفندق",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "بناءً على احتياجات المستخدم وتفضيلاته للموقع، يوصي بخيارات معالم سياحية مناسبة، ويوفر المعلومات الأساسية للمعالم، بما في ذلك معرف المعلم، والاسم، والعنوان، والوصف، والتقييم، وساعات العمل",
        "preconditions": "يطلب المستخدم حجز معلم سياحي، ويقدم كلمات رئيسية أو موقعًا مرتبطًا بالمعلم",
        "postconditions": "يعيد قائمة بالمعالم السياحية التي تستوفي الشروط، وإذا لزم الأمر عرض تفاصيل المعلم (قائمة التذاكر، الأسعار، إلخ) يجب استخدام أداة استعلام تفاصيل المعلم، وتوجيه المستخدم لاختيار المعلم",
        "args": {
            "city_name": "اسم المدينة",
            "key_words": "كلمات رئيسية للبحث (تطابق اسم المعلم، الموقع، العنوان، الميزات، إلخ)"
        },
        "returns": "إخراج منظم للمعلومات الأساسية للمعلم السياحي",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "بناءً على احتياجات المستخدم وتفضيلاته للموقع، يوصي بخيارات رحلات مناسبة، ويوفر المعلومات الأساسية للرحلة، بما في ذلك معرف الرحلة، رقم الرحلة، مدينة المغادرة، مدينة الوصول، موقع مطار المغادرة، موقع مطار الوصول، وقت المغادرة، وقت الوصول، وعلامات الرحلة",
        "preconditions": "يطلب المستخدم حجز رحلة، ويقدم كلمات رئيسية أو مواقع متعلقة بالرحلة",
        "postconditions": "إرجاع قائمة الرحلات التي تستوفي الشروط، وإذا لزم الأمر عرض تفاصيل الرحلة (قائمة أنواع المقاعد، الأسعار، التواريخ، إلخ) يجب استخدام أداة استعلام تفاصيل الرحلة، وتوجيه المستخدم لاختيار رحلة",
        "args": {
            "departure": "مدينة المغادرة",
            "destination": "مدينة الوجهة"
        },
        "returns": "إخراج معلومات أساسية للرحلة بشكل منظم",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "بناءً على احتياجات المستخدم وتفضيلاته للموقع، يوصي بخيارات قطارات مناسبة، ويوفر المعلومات الأساسية لتذاكر القطارات، بما في ذلك معرف القطار، رقم الرحلة، مدينة المغادرة، مدينة الوصول، موقع محطة المغادرة، موقع محطة الوصول، وقت المغادرة، وقت الوصول، ووسوم القطار",
        "preconditions": "يطلب المستخدم حجز قطار، ويقدم كلمات رئيسية أو مواقع تتعلق بالقطار",
        "postconditions": "يُرجع قائمة بتذاكر القطارات التي تستوفي الشروط، وإذا لزم الأمر عرض تفاصيل تذكرة القطار (قائمة أنواع المقاعد، السعر، التاريخ، إلخ) يجب استخدام أداة استعلام تفاصيل تذكرة القطار، وتوجيه المستخدم لاختيار تذكرة القطار",
        "args": {
            "departure": "مدينة المغادرة",
            "destination": "مدينة الوصول",
            "date": "تاريخ المغادرة"
        },
        "returns": "إخراج منظم للمعلومات الأساسية للقطار",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "عندما يقوم المستخدم بحجز فندق، يقوم النظام بإنشاء طلب بناءً على متطلبات المستخدم (مثل اسم الفندق، تاريخ تسجيل الوصول، عدد الأشخاص، وما إلى ذلك)",
        "preconditions": "يجب أن يكون المستخدم قد سجل الدخول وقدم معرف هوية صالح (user_id)، وقدم المستخدم اسم فندق صالح (hotel_name) ونوع غرفة (room_type)، ويمتلك النظام معلومات حول الفندق المستهدف، وتكون هناك غرف متاحة في هذا الفندق للتواريخ المطلوبة",
        "postconditions": "يتم إنشاء الطلب، ويُطلب من المستخدم تأكيد الدفع",
        "args": {
            "hotel_id": "معرف الفندق",
            "room_id": "معرف الغرفة",
            "user_id": "معرف المستخدم"
        },
        "returns": "مخرجات ردود الفعل لعملية إنشاء الطلب",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "يقوم المستخدم بشراء التذاكر بناءً على الموقع السياحي والتاريخ، ويعيد النظام المعلومات ذات الصلة بالتذكرة ويقوم بإنشاء الطلب",
        "preconditions": "في سيناريو زيارة المواقع السياحية، يطلب المستخدم حجز موقع، ويقدم المعلومات الضرورية المتعلقة بالحجز",
        "postconditions": "يتم إنشاء الطلب، ويُطلب من المستخدم تأكيد الدفع",
        "args": {
            "attraction_id": "معرف الموقع السياحي",
            "ticket_id": "معرف التذكرة",
            "user_id": "معرف المستخدم",
            "date": "تاريخ الزيارة، التنسيق %Y-%m-%d",
            "quantity": "الكمية"
        },
        "returns": "مخرجات التغذية الراجعة لعملية إنشاء الطلب",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "يقوم المستخدم بشراء تذاكر الطيران وفقًا لرقم الرحلة والتاريخ ونوع المقعد والكمية، ويقوم النظام بإرجاع المعلومات ذات الصلة بالتذكرة وإتمام الطلب",
        "preconditions": "في سيناريو البحث عن تذاكر الطيران وشراءها، يطلب المستخدم حجز رحلة ويقدم المعلومات الضرورية المتعلقة بالحجز",
        "postconditions": "يتم إنشاء الطلب، ويُطلب من المستخدم تأكيد الدفع",
        "args": {
            "flight_id": "معرف الرحلة",
            "seat_id": "معرف المقعد",
            "user_id": "معرف المستخدم",
            "date": "تاريخ المغادرة",
            "quantity": "الكمية"
        },
        "returns": "مخرجات التغذية الراجعة لعملية إنشاء الطلب",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "يقوم المستخدم بشراء تذاكر القطار بناءً على رقم القطار والتاريخ ونوع المقعد والكمية، ويعيد النظام المعلومات ذات الصلة بالتذكرة ويقوم بإنشاء الطلب",
        "preconditions": "في سيناريو الاستعلام وشراء تذاكر القطار، يطلب المستخدم حجز قطار وقدم المعلومات الضرورية المطلوبة للحجز",
        "postconditions": "يتم إنشاء الطلب، ويُطلب من المستخدم تأكيد الدفع",
        "args": {
            "train_id": "معرف القطار",
            "seat_id": "معرف المقعد",
            "user_id": "معرف المستخدم",
            "date": "تاريخ المغادرة",
            "quantity": "الكمية"
        },
        "returns": "ناتج التغذية الراجعة لعملية إنشاء الطلب",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "يقوم المستخدم بدفع طلب الفندق",
        "preconditions": "في سيناريو استعلام حجز الفندق، يطلب المستخدم دفع طلب الفندق، وقد تم تحديد معرف الطلب سابقًا",
        "postconditions": "تأكيد الدفع وتحديث حالة الطلب إلى مدفوع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "قيام المستخدم بدفع طلب تذكرة الدخول",
        "preconditions": "في سياق السياحة للمعالم، يطلب المستخدم دفع طلب تذكرة الدخول، وقد تم تحديد معرف الطلب في السياق السابق",
        "postconditions": "تأكيد الدفع وتحديث حالة الطلب إلى مدفوع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "يقوم المستخدم بدفع طلب تذكرة الطيران",
        "preconditions": "في سيناريو البحث وشراء تذاكر الطيران، يطلب المستخدم دفع طلب الرحلة، وقد تم تحديد معرف الطلب في السياق السابق",
        "postconditions": "تأكيد الدفع وتحديث حالة الطلب إلى مدفوع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "يقوم المستخدم بدفع طلب تذكرة القطار",
        "preconditions": "في سياق البحث وشراء تذاكر القطار، يطلب المستخدم دفع طلب تذكرة القطار، وقد تم تحديد معرف الطلب في السياق السابق",
        "postconditions": "تأكيد الدفع وتحديث حالة الطلب إلى مدفوع",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "معلومات نتيجة الدفع",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "الاستعلام عن طلبات الفندق الخاصة بالمستخدم بناءً على معرف المستخدم، وإرجاع معلومات تتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف الفندق، والسعر الإجمالي للطلب، ووقت الطلب، ووقت التحديث، وحالة الطلب",
        "preconditions": "حاجة المستخدم هي الاستعلام عن طلبات الفندق",
        "postconditions": "إرجاع معلومات الطلب لتسهيل التعديل أو الإلغاء لاحقًا",
        "args": {
            "user_id": "معرف المستخدم",
            "date": "التاريخ",
            "status": "حالة الطلب"
        },
        "returns": "معلومات طلبات الفندق للمستخدم المحدد",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "استعلام عن طلبات تذاكر المعالم السياحية للمستخدم بناءً على معرف المستخدم، وإرجاع بيانات تتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف المعلم السياحي، والسعر الإجمالي للطلب، ووقت تقديم الطلب، ووقت التحديث، وحالة الطلب",
        "preconditions": "حاجة المستخدم هي الاستعلام عن طلبات تذاكر المعالم السياحية",
        "postconditions": "إرجاع معلومات الطلب لتسهيل التعديل أو الإلغاء لاحقًا",
        "args": {
            "user_id": "معرف المستخدم",
            "date": "التاريخ",
            "status": "حالة الطلب"
        },
        "returns": "معلومات طلبات تذاكر المعالم السياحية للمستخدم المحدد",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "بناءً على معرف المستخدم، قم بالاستعلام عن طلبات تذاكر الطيران الخاصة بالمستخدم، وأعد معلومات تتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف الرحلة، والسعر الإجمالي للطلب، ووقت الطلب، ووقت التحديث، وحالة الطلب",
        "preconditions": "متطلب المستخدم هو الاستعلام عن طلبات تذاكر الطيران",
        "postconditions": "إرجاع معلومات الطلب لتسهيل التعديل أو الإلغاء لاحقًا",
        "args": {
            "user_id": "معرف المستخدم",
            "date": "التاريخ",
            "status": "حالة الطلب"
        },
        "returns": "معلومات طلبات تذاكر الطيران للمستخدم المحدد",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "الاستعلام عن طلبات تذاكر القطار للمستخدم بناءً على معرف المستخدم، وإرجاع بيانات تحتوي على معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف القطار، وإجمالي سعر الطلب، ووقت إنشاء الطلب، ووقت التحديث، وحالة الطلب",
        "preconditions": "حاجة المستخدم هي الاستعلام عن طلبات تذاكر القطار",
        "postconditions": "إرجاع معلومات الطلب لتسهيل التعديل أو الإلغاء لاحقاً",
        "args": {
            "user_id": "معرف المستخدم",
            "date": "التاريخ",
            "status": "حالة الطلب"
        },
        "returns": "معلومات طلبات تذاكر القطار للمستخدم المحدد",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "الحصول على تفاصيل طلب الفندق، وتتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف الفندق، والسعر الإجمالي للطلب، ووقت الطلب، ووقت التحديث، وحالة الطلب، ومعلومات الغرفة التفصيلية للطلب (نوع الغرفة، وتاريخ تسجيل الوصول، والسعر، ومعرف الغرفة)",
        "preconditions": "يطلب المستخدم الحصول على تفاصيل طلب الفندق، وقد تم تحديد معرف الطلب في السياق السابق",
        "postconditions": "إرجاع تفاصيل الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "تفاصيل الطلب",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "الحصول على تفاصيل طلب تذكرة الموقع السياحي، بما في ذلك معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف الموقع السياحي، والسعر الإجمالي للطلب، ووقت تقديم الطلب، ووقت التحديث، وحالة الطلب، ومعلومات تفصيلية عن موقع الطلب (نوع التذكرة، والتاريخ، والسعر، ومعرف التذكرة)",
        "preconditions": "يطلب المستخدم الحصول على تفاصيل طلب تذكرة الموقع السياحي، وتم تحديد معرف الطلب في السياق السابق",
        "postconditions": "إرجاع تفاصيل الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "تفاصيل الطلب",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "الحصول على تفاصيل طلب تذكرة الطيران، بما في ذلك معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف الرحلة، والسعر الإجمالي للطلب، ووقت الطلب، ووقت التحديث، وحالة الطلب، ومعلومات تفاصيل تذكرة الطلب (نوع المقعد، التاريخ، السعر، معرف المقعد)",
        "preconditions": "يطلب المستخدم الحصول على تفاصيل طلب تذكرة الطيران، وتم تحديد معرف الطلب في السياق السابق",
        "postconditions": "إرجاع تفاصيل الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "تفاصيل الطلب",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "الحصول على تفاصيل طلب تذكرة القطار، تتضمن معرف الطلب، ونوع الطلب، ومعرف المستخدم، ومعرف القطار، والسعر الإجمالي للطلب، ووقت الطلب، ووقت التحديث، وحالة الطلب، ومعلومات تفاصيل تذكرة القطار للطلب (نوع المقعد، التاريخ، السعر، معرف المقعد)",
        "preconditions": "يطلب المستخدم الحصول على تفاصيل طلب تذكرة القطار، وتم تحديد معرف الطلب في النص السابق",
        "postconditions": "إرجاع تفاصيل الطلب",
        "args": {
            "order_id": "معرف الطلب"
        },
        "returns": "تفاصيل الطلب",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "تعديل طلب تذكرة القطار، يدعم تغيير تاريخ المغادرة، ويعالج تلقائيًا فرق السعر سواء بالدفع أو الاسترداد.",
        "preconditions": "في سيناريو الاستعلام وشراء تذاكر القطار، يطلب المستخدم تعديل طلب تذكرة القطار، وتم تحديد معرف الطلب في السياق السابق.",
        "postconditions": "تعديل الطلب وتحديث حالة الطلب، إذا تطلب الأمر دفع فرق السعر، تتغير حالة الطلب إلى unpaid، وإلا تبقى الحالة الأصلية، وإذا تطلب الأمر دفع فرق السعر، يجب توجيه المستخدم لدفع هذا الطلب.",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم",
            "new_date": "تاريخ المغادرة الجديد، بالتنسيق %Y-%m-%d"
        },
        "returns": "(محتوى الطلب المعدل، فرق السعر، القيمة الموجبة تعني الحاجة لدفع فرق السعر، والقيمة السالبة تعني استرداد فرق السعر)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "تعديل طلب تذكرة الطيران، يدعم تغيير تاريخ المغادرة، والتعامل تلقائيًا مع فرق السعر سواء كان دفعًا إضافيًا أو استردادًا.",
        "preconditions": "في سيناريو البحث وشراء تذاكر الطيران، يطلب المستخدم تعديل طلب التذكرة، وتم تحديد معرف الطلب في السياق السابق.",
        "postconditions": "تعديل الطلب وتحديث حالة الطلب، إذا تطلب الأمر دفع فرق سعر، تتغير حالة الطلب إلى unpaid، وإلا تبقى الحالة الأصلية، وفي حال وجود فرق سعر مطلوب، يجب توجيه المستخدم لسداد هذا الطلب.",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم",
            "new_date": "تاريخ المغادرة الجديد، الصيغة %Y-%m-%d"
        },
        "returns": "(محتوى الطلب المُعدّل، فرق السعر، القيمة الموجبة تعني دفعًا إضافيًا، والقيمة السالبة تعني استردادًا)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "يقوم المستخدم بإلغاء حجز فندق مؤكد سابقًا",
        "preconditions": "في سياق الاستعلام عن حجز الفندق، يطلب المستخدم إلغاء الحجز، وقد تم تحديد معرف الطلب سابقًا",
        "postconditions": "يتم إلغاء الطلب وتحديث حالته، وفي حال وجود مبلغ مسترد، يتم إعلام المستخدم بذلك",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم"
        },
        "returns": "مبلغ الاسترداد الناتج عن إلغاء الطلب",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "يقوم المستخدم بإلغاء طلب تذاكر الدخول للموقع السياحي الذي تم حجزه مسبقًا",
        "preconditions": "وجود معرف الطلب في سجل المحادثات أو تم الاستعلام عن الطلب مسبقًا، وأن يكون لدى المستخدم صلاحية إلغاء هذا الطلب",
        "postconditions": "في حال وجود فرق في المبلغ المسترد، يكفي إعلام المستخدم",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم"
        },
        "returns": "مبلغ الاسترداد الخاص بإلغاء الطلب",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "يقوم المستخدم بإلغاء طلب حجز تذكرة طيران تم حجزه مسبقًا",
        "preconditions": "وجود معرف الطلب في المحادثة السابقة أو تم إجراء استعلام عن الطلب مسبقًا، ولدى المستخدم صلاحية إلغاء هذا الطلب",
        "postconditions": "في حال وجود فرق في المبلغ المسترد، يكفي إبلاغ المستخدم",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم"
        },
        "returns": "مبلغ الاسترداد لإلغاء الطلب",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "إلغاء المستخدم لطلب تذكرة القطار المحجوزة",
        "preconditions": "وجود معرف الطلب في سجل المحادثة أو تم الاستعلام عن الطلب مسبقًا، وأن يكون لدى المستخدم صلاحية إلغاء هذا الطلب",
        "postconditions": "في حال وجود فرق في المبلغ المسترد، يكفي إعلام المستخدم",
        "args": {
            "order_id": "معرف الطلب",
            "user_id": "معرف المستخدم"
        },
        "returns": "مبلغ الاسترداد لإلغاء الطلب",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Russian version
TOOL_DESCRIPTIONS_RU = {
    "get_ota_hotel_info": {
        "description": "Получение информации об отеле, включая ID отеля, название, рейтинг, звездность, адрес, теги и список номеров",
        "preconditions": "В сценарии поиска и бронирования отеля требуется получить подробную информацию об отеле",
        "postconditions": "Возвращает подробную информацию об отеле, направляя пользователя к выбору номера и оформлению заказа",
        "args": {
            "hotel_id": "ID отеля"
        },
        "returns": "Информация об отеле",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Получение информации о достопримечательности, включающей ID достопримечательности, название, адрес, описание, рейтинг, часы работы, стоимость билетов и список типов билетов",
        "preconditions": "В сценарии посещения достопримечательности, когда требуется получить подробную информацию о ней",
        "postconditions": "Возвращает подробную информацию о достопримечательности, направляя пользователя к выбору билета и оформлению заказа",
        "args": {
            "attraction_id": "ID достопримечательности"
        },
        "returns": "Информация о достопримечательности",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Получение информации о рейсе, включая ID рейса, номер рейса, город вылета, город прибытия, местоположение аэропорта вылета, местоположение аэропорта прибытия, время вылета, время прибытия, метки рейса, список типов мест",
        "preconditions": "В сценарии поиска и покупки авиабилетов требуется получить подробную информацию о рейсе",
        "postconditions": "Возвращает подробную информацию о рейсе, побуждая пользователя выбрать место и оформить заказ",
        "args": {
            "flight_id": "ID рейса"
        },
        "returns": "Информация о рейсе",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Получение информации о поезде, включая идентификатор поезда, номер поезда, город отправления, город прибытия, станцию отправления, станцию прибытия, время отправления, время прибытия, метки поезда, список типов мест",
        "preconditions": "В сценарии поиска и покупки билетов на поезд необходимо получить подробную информацию о поезде",
        "postconditions": "Возвращает подробную информацию о поезде, направляет пользователя к выбору места и оформлению заказа",
        "args": {
            "train_id": "Идентификатор поезда"
        },
        "returns": "Информация о поезде",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "В сценарии путешествий и отелей, на основе потребностей пользователя в местоположении и предпочтений, рекомендовать подходящие варианты отелей, предоставлять основную информацию об отеле, включая ID отеля, название, рейтинг, звездность, адрес, теги",
        "preconditions": "Пользователь запрашивает бронирование отеля, предоставил ключевые слова, связанные с отелем, или местоположение",
        "postconditions": "Возвращает список отелей, соответствующих условиям; если требуется просмотреть детали отеля (список номеров, цены и т. д.), необходимо использовать инструмент запроса деталей отеля, направлять пользователя к выбору отеля",
        "args": {
            "city_name": "Название города",
            "key_words": "Ключевые слова для поиска (соответствуют названию отеля, описанию отеля и т. д.)"
        },
        "returns": "Структурированный вывод основной информации об отеле",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Рекомендует подходящие варианты достопримечательностей на основе требований пользователя к местоположению и предпочтений, предоставляет базовую информацию о достопримечательностях, включая ID достопримечательности, название, адрес, описание, рейтинг, время работы",
        "preconditions": "Пользователь запрашивает бронирование достопримечательности, предоставил ключевые слова или местоположение, связанные с достопримечательностью",
        "postconditions": "Возвращает список достопримечательностей, соответствующих условиям. Если требуется просмотреть детали достопримечательности (список билетов, цены и т.д.), необходимо использовать инструмент запроса деталей достопримечательности. Направляет пользователя к выбору достопримечательности",
        "args": {
            "city_name": "Название города",
            "key_words": "Ключевые слова для поиска (соответствуют названию достопримечательности, местоположению, адресу, особенностям и т.д.)"
        },
        "returns": "Структурированный вывод базовой информации о достопримечательности",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Рекомендует подходящие варианты рейсов на основе требований к местоположению и предпочтений пользователя, предоставляя основную информацию о рейсе, включая ID рейса, номер рейса, город вылета, город прибытия, местоположение аэропорта вылета, местоположение аэропорта прибытия, время вылета, время прибытия и метки рейса",
        "preconditions": "Пользователь запрашивает бронирование рейса и указал ключевые слова или местоположения, связанные с рейсом",
        "postconditions": "Возвращает список рейсов, соответствующих условиям. Если необходимо просмотреть детали рейса (список типов мест, цена, дата и т.д.), следует использовать инструмент запроса деталей рейса. Направляет пользователя к выбору рейса",
        "args": {
            "departure": "Город вылета",
            "destination": "Город назначения"
        },
        "returns": "Структурированный вывод основной информации о рейсе",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "На основе требований пользователя к местоположению и предпочтений рекомендует подходящие варианты поездов и предоставляет базовую информацию о билетах на поезд, включая ID поезда, номер поезда, город отправления, город назначения, расположение станции отправления, расположение станции прибытия, время отправления, время прибытия и теги поезда.",
        "preconditions": "Пользователь запрашивает бронирование поезда и предоставил ключевые слова или местоположения, связанные с поездом.",
        "postconditions": "Возвращает список билетов на поезд, соответствующих условиям. Если необходимо просмотреть детали билета (список типов мест, цена, дата и т. д.), следует использовать инструмент запроса деталей билета на поезд. Направляет пользователя к выбору билета на поезд.",
        "args": {
            "departure": "Город отправления",
            "destination": "Город назначения",
            "date": "Дата отправления"
        },
        "returns": "Структурированный вывод базовой информации о поезде.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Когда пользователь бронирует отель, система создает заказ на основе запроса пользователя (например, название отеля, дата заезда, количество человек и т. д.)",
        "preconditions": "Пользователь авторизован и предоставил действительный идентификатор (user_id), пользователь предоставил действительное название отеля (hotel_name) и тип номера (room_type), система имеет информацию о целевом отеле, и в этом отеле есть номера на запрошенные даты",
        "postconditions": "Заказ создан, пользователю предлагается подтвердить оплату",
        "args": {
            "hotel_id": "ID отеля",
            "room_id": "ID номера",
            "user_id": "ID пользователя"
        },
        "returns": "Результат операции создания заказа",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "Пользователь покупает билеты на достопримечательность на определенную дату, система возвращает соответствующую информацию о билетах и оформляет заказ",
        "preconditions": "В сценарии посещения достопримечательности пользователь запрашивает бронирование и предоставляет необходимую информацию для бронирования",
        "postconditions": "Заказ создан, пользователя просят подтвердить оплату",
        "args": {
            "attraction_id": "ID достопримечательности",
            "ticket_id": "ID билета",
            "user_id": "ID пользователя",
            "date": "Дата посещения, формат %Y-%m-%d",
            "quantity": "Количество"
        },
        "returns": "Вывод результата операции создания заказа",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "Пользователь покупает авиабилет, указывая номер рейса, дату, тип места и количество; система возвращает соответствующую информацию о билете и оформляет заказ.",
        "preconditions": "В сценарии поиска и покупки авиабилетов пользователь запрашивает бронирование рейса и предоставляет необходимую информацию для бронирования.",
        "postconditions": "Заказ создан, пользователя просят подтвердить оплату.",
        "args": {
            "flight_id": "ID рейса",
            "seat_id": "ID места",
            "user_id": "ID пользователя",
            "date": "Дата вылета",
            "quantity": "Количество"
        },
        "returns": "Результат операции создания заказа.",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "Пользователь покупает железнодорожный билет на основе номера поезда, даты, типа места и количества; система возвращает соответствующую информацию о билете и оформляет заказ",
        "preconditions": "В сценарии поиска и покупки железнодорожных билетов пользователь запрашивает бронирование поезда и предоставил необходимую информацию для бронирования",
        "postconditions": "Заказ создан, пожалуйста, подтвердите оплату",
        "args": {
            "train_id": "ID поезда",
            "seat_id": "ID места",
            "user_id": "ID пользователя",
            "date": "Дата отправления",
            "quantity": "Количество"
        },
        "returns": "Результат операции создания заказа",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "Пользователь оплачивает заказ отеля",
        "preconditions": "В сценарии поиска и бронирования отеля пользователь запрашивает оплату заказа отеля, идентификатор заказа был определен ранее в контексте",
        "postconditions": "Подтвердить оплату и обновить статус заказа на «оплачено»",
        "args": {
            "order_id": "Идентификатор заказа"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "Пользователь оплачивает заказ на билеты",
        "preconditions": "В сценарии посещения достопримечательности пользователь запрашивает оплату заказа на входные билеты; идентификатор заказа уже был определен в предыдущем контексте",
        "postconditions": "Подтвердить оплату и обновить статус заказа на «оплачено»",
        "args": {
            "order_id": "Идентификатор заказа"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "Пользователь производит оплату заказа на авиабилет",
        "preconditions": "В сценарии поиска и покупки авиабилетов пользователь запрашивает оплату заказа на рейс; идентификатор заказа был определен в предыдущем контексте",
        "postconditions": "Подтверждение оплаты и обновление статуса заказа на «оплачено»",
        "args": {
            "order_id": "Идентификатор заказа"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "Оплата пользователем заказа на железнодорожные билеты",
        "preconditions": "В сценарии поиска и покупки железнодорожных билетов пользователь запрашивает оплату заказа; ID заказа был определен в предыдущем контексте.",
        "postconditions": "Подтверждение оплаты и обновление статуса заказа на «оплачено».",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Информация о результате оплаты",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "По идентификатору пользователя запрашивает заказы отеля, возвращая информацию, включающую идентификатор заказа, тип заказа, идентификатор пользователя, идентификатор отеля, общую стоимость заказа, время оформления заказа, время обновления и статус заказа.",
        "preconditions": "Пользователь хочет запросить информацию о заказах отеля.",
        "postconditions": "Возвращает информацию о заказе, чтобы облегчить последующее изменение или отмену.",
        "args": {
            "user_id": "Идентификатор пользователя",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Информация о заказах отеля для указанного пользователя.",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "По идентификатору пользователя запрашивает заказы на билеты в достопримечательности, возвращает информацию, включающую идентификатор заказа, тип заказа, идентификатор пользователя, идентификатор достопримечательности, общую сумму заказа, время оформления заказа, время обновления и статус заказа.",
        "preconditions": "Пользователь хочет запросить заказы на билеты в достопримечательности.",
        "postconditions": "Возвращает информацию о заказе для удобства последующего изменения или отмены.",
        "args": {
            "user_id": "Идентификатор пользователя",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Информация о заказах на билеты в достопримечательности для указанного пользователя.",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "По идентификатору пользователя запрашивает заказы на авиабилеты пользователя, возвращая информацию, включающую идентификатор заказа, тип заказа, идентификатор пользователя, идентификатор рейса, общую стоимость заказа, время размещения заказа, время обновления и статус заказа",
        "preconditions": "Пользователь хочет запросить информацию о заказе авиабилетов",
        "postconditions": "Возвращает информацию о заказе, чтобы облегчить последующее изменение или отмену",
        "args": {
            "user_id": "Идентификатор пользователя",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Информация о заказах на авиабилеты указанного пользователя",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "По идентификатору пользователя запрашивает заказы на железнодорожные билеты, возвращая данные, включающие идентификатор заказа, тип заказа, идентификатор пользователя, идентификатор поезда, общую стоимость заказа, время оформления заказа, время обновления и статус заказа",
        "preconditions": "Пользователь намерен запросить заказы на железнодорожные билеты",
        "postconditions": "Возвращает информацию о заказе для последующего изменения или отмены",
        "args": {
            "user_id": "Идентификатор пользователя",
            "date": "Дата",
            "status": "Статус заказа"
        },
        "returns": "Информация о заказах на железнодорожные билеты для указанного пользователя",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Получение подробной информации о заказе отеля, включая ID заказа, тип заказа, ID пользователя, ID отеля, общую сумму заказа, время размещения заказа, время обновления, статус заказа и подробную информацию о номерах заказа (тип номера, дата заезда, цена, ID номера)",
        "preconditions": "Пользователь запрашивает получение подробной информации о заказе отеля, ID заказа был определен ранее в контексте",
        "postconditions": "Возвращает подробную информацию о заказе",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Подробная информация о заказе",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Получение подробной информации о заказе билета на достопримечательность, включая ID заказа, тип заказа, ID пользователя, ID достопримечательности, общую стоимость заказа, время оформления заказа, время обновления, статус заказа и подробную информацию о достопримечательности в заказе (тип билета, дата, цена, ID билета)",
        "preconditions": "Пользователь запрашивает получение подробной информации о заказе билета на достопримечательность, ID заказа был определен в предыдущем контексте",
        "postconditions": "Возвращает подробную информацию о заказе",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Подробная информация о заказе",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Получение подробной информации о заказе авиабилета, включая ID заказа, тип заказа, ID пользователя, ID рейса, общую стоимость заказа, время оформления, время обновления, статус заказа и подробную информацию о билете (тип места, дата, цена, ID места)",
        "preconditions": "Пользователь запрашивает подробную информацию о заказе авиабилета, ID заказа был определен в предыдущем контексте",
        "postconditions": "Возвращает подробную информацию о заказе",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Подробная информация о заказе",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Получить детали заказа на железнодорожный билет, включая ID заказа, тип заказа, ID пользователя, ID поезда, общую стоимость заказа, время создания заказа, время обновления, статус заказа и подробную информацию о билете (тип места, дата, цена, ID места)",
        "preconditions": "Пользователь запрашивает детали заказа на железнодорожный билет, ID заказа был определен выше",
        "postconditions": "Возвращаются детали заказа",
        "args": {
            "order_id": "ID заказа"
        },
        "returns": "Детали заказа",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Изменение заказа на железнодорожный билет, поддержка изменения даты отправления, автоматическая обработка доплаты или возврата разницы в стоимости.",
        "preconditions": "В сценарии поиска и покупки железнодорожных билетов пользователь запрашивает изменение заказа на билет, ID заказа определен в предыдущем контексте",
        "postconditions": "Изменить заказ и обновить статус заказа, если требуется доплата, статус заказа меняется на unpaid, иначе остается исходный статус, если требуется доплата, необходимо направить пользователя на оплату данного заказа",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID пользователя",
            "new_date": "Новая дата отправления, формат %Y-%m-%d"
        },
        "returns": "(Содержимое измененного заказа, разница в стоимости, положительное значение означает необходимость доплаты, отрицательное — возврат разницы)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Изменение заказа на авиабилет: поддержка изменения даты вылета, автоматическая обработка доплаты или возврата разницы.",
        "preconditions": "В сценарии поиска и покупки авиабилетов пользователь запрашивает изменение заказа на авиабилет, ID заказа определен в предыдущем контексте.",
        "postconditions": "Заказ изменяется и статус обновляется. Если требуется доплата, статус заказа меняется на unpaid, иначе остается прежним. Если требуется доплата, необходимо направить пользователя к оплате этого заказа.",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID пользователя",
            "new_date": "Новая дата вылета, формат %Y-%m-%d"
        },
        "returns": "(Содержимое измененного заказа, разница в стоимости: положительное значение означает доплату, отрицательное — возврат)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "Пользователь отменяет ранее забронированный заказ отеля",
        "preconditions": "В сценарии поиска и бронирования отеля пользователь запрашивает отмену заказа отеля, идентификатор заказа был определен ранее",
        "postconditions": "Заказ отменяется и статус заказа обновляется; если требуется возврат разницы, просто сообщите пользователю",
        "args": {
            "order_id": "Идентификатор заказа",
            "user_id": "Идентификатор пользователя"
        },
        "returns": "Сумма возврата за отмену заказа",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "Пользователь отменяет ранее забронированный заказ на билеты в достопримечательность",
        "preconditions": "В истории диалога есть ID заказа или уже выполнялся поиск заказа, и у пользователя есть права на отмену этого заказа",
        "postconditions": "Если возвращается разница в стоимости, просто сообщите об этом пользователю",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID пользователя"
        },
        "returns": "Сумма возврата за отмену заказа",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "Пользователь отменяет заказ на ранее забронированный авиабилет",
        "preconditions": "В истории диалога присутствует ID заказа или уже выполнялся запрос по заказу, и у пользователя есть права на отмену данного заказа",
        "postconditions": "Если возвращается разница в стоимости, достаточно уведомить об этом пользователя",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID пользователя"
        },
        "returns": "Сумма возврата при отмене заказа",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "Пользователь отменяет заказ на ранее забронированный железнодорожный билет",
        "preconditions": "ID заказа присутствует в истории диалога, либо запрос заказа уже выполнялся, и у пользователя есть права на отмену данного заказа",
        "postconditions": "Если предусмотрен возврат разницы в стоимости, просто уведомите об этом пользователя",
        "args": {
            "order_id": "ID заказа",
            "user_id": "ID пользователя"
        },
        "returns": "Сумма возврата за отмену заказа",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - French version
# Tool descriptions - French version
TOOL_DESCRIPTIONS_FR = {
    "get_ota_hotel_info": {
        "description": "Récupère les informations de l'hôtel, incluant l'ID de l'hôtel, le nom, la note, le nombre d'étoiles, l'adresse, les étiquettes et la liste des chambres.",
        "preconditions": "Dans le contexte de recherche et de réservation d'hôtel, il est nécessaire d'obtenir les informations détaillées de l'hôtel.",
        "postconditions": "Retourne les informations détaillées de l'hôtel, guide l'utilisateur pour sélectionner une chambre et finaliser la réservation.",
        "args": {
            "hotel_id": "ID de l'hôtel"
        },
        "returns": "Informations de l'hôtel",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "Obtenir les informations sur l'attraction, incluant l'ID de l'attraction, le nom, l'adresse, la description, la note, les horaires d'ouverture, le prix des billets et la liste des types de billets",
        "preconditions": "Dans un scénario de visite d'attraction, lorsque les informations détaillées de l'attraction sont nécessaires",
        "postconditions": "Retourne les informations détaillées de l'attraction, guide l'utilisateur pour sélectionner un billet et passer commande",
        "args": {
            "attraction_id": "ID de l'attraction"
        },
        "returns": "Informations sur l'attraction",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "Récupérer les informations de vol, comprenant l'identifiant du vol, le numéro de vol, la ville de départ, la ville d'arrivée, l'emplacement de l'aéroport de départ, l'emplacement de l'aéroport d'arrivée, l'heure de départ, l'heure d'arrivée, les étiquettes de vol, la liste des types de sièges",
        "preconditions": "Dans le scénario de recherche et d'achat de billets d'avion, il est nécessaire d'obtenir les informations détaillées du vol",
        "postconditions": "Renvoyer les informations détaillées du vol, guider l'utilisateur pour sélectionner un siège et passer la commande",
        "args": {
            "flight_id": "Identifiant du vol"
        },
        "returns": "Informations de vol",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "Récupérer les informations sur le train, y compris l'identifiant du train, le numéro du train, la ville de départ, la ville d'arrivée, l'emplacement de la gare de départ, l'emplacement de la gare d'arrivée, l'heure de départ, l'heure d'arrivée, les étiquettes du train, la liste des types de sièges",
        "preconditions": "Dans le scénario de recherche et d'achat de billets de train, il est nécessaire d'obtenir les informations détaillées du train",
        "postconditions": "Retourne les informations détaillées du train, guide l'utilisateur pour sélectionner un siège et passer la commande",
        "args": {
            "train_id": "Identifiant du train"
        },
        "returns": "Informations sur le train",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "Dans le contexte des voyages et de l'hôtellerie, recommande des options d'hôtels appropriées en fonction des besoins de localisation et des préférences de l'utilisateur, et fournit les informations de base sur l'hôtel, y compris l'identifiant de l'hôtel, le nom, la note, le nombre d'étoiles, l'adresse et les étiquettes",
        "preconditions": "L'utilisateur demande de réserver un hôtel et fournit des mots-clés liés à l'hôtel ou un lieu",
        "postconditions": "Renvoie une liste d'hôtels correspondant aux critères. Si l'utilisateur souhaite consulter les détails de l'hôtel (liste des chambres, prix, etc.), il doit utiliser l'outil de recherche de détails d'hôtel. Guide l'utilisateur pour choisir un hôtel",
        "args": {
            "city_name": "Nom de la ville",
            "key_words": "Mots-clés de recherche (correspondance avec le nom de l'hôtel, la description de l'hôtel, etc.)"
        },
        "returns": "Sortie structurée des informations de base sur l'hôtel",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "Recommande des options de sites touristiques appropriées en fonction des besoins de localisation et des préférences de l'utilisateur, fournit les informations de base sur les sites, incluant l'ID du site, le nom, l'adresse, la description, la note et les horaires d'ouverture",
        "preconditions": "L'utilisateur demande de réserver un site touristique et a fourni des mots-clés ou un lieu liés au site",
        "postconditions": "Renvoie une liste de sites touristiques correspondant aux conditions, si besoin de consulter les détails du site (liste des billets, prix, etc.) il faut utiliser l'outil de requête de détails du site, guide l'utilisateur pour choisir un site",
        "args": {
            "city_name": "Nom de la ville",
            "key_words": "Mots-clés de recherche (correspondance avec le nom du site, la position, l'adresse, les caractéristiques, etc.)"
        },
        "returns": "Sortie structurée des informations de base sur les sites touristiques",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "Recommande des options de vol adaptées en fonction des besoins de destination et des préférences de l'utilisateur. Fournit les informations de base du vol, incluant l'ID du vol, le numéro de vol, la ville de départ, la ville d'arrivée, l'emplacement de l'aéroport de départ, l'emplacement de l'aéroport d'arrivée, l'heure de départ, l'heure d'arrivée et les étiquettes de vol.",
        "preconditions": "L'utilisateur demande la réservation d'un vol et a fourni des mots-clés ou des lieux liés au vol.",
        "postconditions": "Renvoie une liste de vols éligibles. Si l'utilisateur souhaite consulter les détails du vol (liste des types de sièges, prix, dates, etc.), l'outil de requête de détails de vol doit être utilisé. Guide l'utilisateur dans le choix du vol.",
        "args": {
            "departure": "Ville de départ",
            "destination": "Ville de destination"
        },
        "returns": "Sortie structurée des informations de base du vol.",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "Recommande des options de train appropriées en fonction des besoins de localisation et des préférences de l'utilisateur, fournit des informations de base sur les billets de train, incluant l'ID du train, le numéro de train, la ville de départ, la ville d'arrivée, l'emplacement de la gare de départ, l'emplacement de la gare d'arrivée, l'heure de départ, l'heure d'arrivée et les étiquettes du train.",
        "preconditions": "L'utilisateur demande de réserver un train et a fourni des mots-clés ou des lieux liés au train.",
        "postconditions": "Retourne une liste de billets de train correspondant aux conditions. Si l'utilisateur souhaite consulter les détails du billet (liste des types de sièges, prix, date, etc.), il doit utiliser l'outil de requête de détails des billets de train. Guide l'utilisateur pour choisir un billet de train.",
        "args": {
            "departure": "Ville de départ",
            "destination": "Ville de destination",
            "date": "Date de départ"
        },
        "returns": "Sortie structurée des informations de base sur le train.",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "Lorsque l'utilisateur réserve un hôtel, le système génère une commande en fonction de ses besoins (nom de l'hôtel, date d'arrivée, nombre de personnes, etc.)",
        "preconditions": "L'utilisateur est connecté et fournit un identifiant valide (user_id), l'utilisateur fournit un nom d'hôtel valide (hotel_name) et un type de chambre (room_type), le système dispose d'informations sur l'hôtel cible et cet hôtel a des chambres disponibles aux dates demandées.",
        "postconditions": "Génération de la commande, demande de confirmation de paiement à l'utilisateur.",
        "args": {
            "hotel_id": "ID de l'hôtel",
            "room_id": "ID de la chambre",
            "user_id": "ID de l'utilisateur"
        },
        "returns": "Sortie de rétroaction pour l'opération de création de commande.",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "L'utilisateur achète des billets en fonction de l'attraction et de la date, le système renvoie les informations relatives aux billets et passe la commande",
        "preconditions": "Dans le scénario de tourisme d'attraction, l'utilisateur demande de réserver une attraction et fournit les informations nécessaires à la réservation",
        "postconditions": "Une commande est générée, l'utilisateur est invité à confirmer le paiement",
        "args": {
            "attraction_id": "ID de l'attraction",
            "ticket_id": "ID du billet",
            "user_id": "ID de l'utilisateur",
            "date": "Date de visite, au format %Y-%m-%d",
            "quantity": "Quantité"
        },
        "returns": "Résultat de l'opération de création de commande",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "L'utilisateur achète des billets d'avion en fonction du numéro de vol, de la date, du type de siège et de la quantité ; le système renvoie les informations relatives au billet et passe la commande.",
        "preconditions": "Dans le scénario de recherche et d'achat de billets, l'utilisateur demande la réservation d'un vol et fournit les informations nécessaires à la réservation.",
        "postconditions": "La commande est générée ; invitez l'utilisateur à confirmer le paiement.",
        "args": {
            "flight_id": "ID du vol",
            "seat_id": "ID du siège",
            "user_id": "ID de l'utilisateur",
            "date": "Date de départ",
            "quantity": "Quantité"
        },
        "returns": "Retour d'information sur l'opération de création de commande.",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "L'utilisateur achète des billets de train en fonction du numéro de train, de la date, du type de siège et de la quantité. Le système renvoie les informations concernant le billet et effectue la commande.",
        "preconditions": "Dans le contexte de la recherche et de l'achat de billets de train, l'utilisateur demande la réservation d'un train et fournit les informations nécessaires à la réservation.",
        "postconditions": "La commande est générée et l'utilisateur est invité à confirmer le paiement.",
        "args": {
            "train_id": "ID du train",
            "seat_id": "ID du siège",
            "user_id": "ID de l'utilisateur",
            "date": "Date de départ",
            "quantity": "Quantité"
        },
        "returns": "Retour d'information sur l'opération de création de commande.",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "L'utilisateur effectue le paiement d'une commande d'hôtel",
        "preconditions": "Dans le scénario de recherche et de réservation d'hôtel, l'utilisateur demande le paiement de la commande d'hôtel, l'ID de la commande a été déterminé dans le contexte précédent.",
        "postconditions": "Confirmer le paiement et mettre à jour le statut de la commande à 'payé'.",
        "args": {
            "order_id": "ID de la commande"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "L'utilisateur effectue le paiement d'une commande de billets",
        "preconditions": "Dans un contexte de visite touristique, l'utilisateur demande le paiement d'une commande de billets d'entrée ; l'identifiant de la commande a été déterminé précédemment",
        "postconditions": "Le paiement est confirmé et le statut de la commande est mis à jour à 'payé'",
        "args": {
            "order_id": "Identifiant de la commande"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "L'utilisateur effectue le paiement d'une commande de billet d'avion",
        "preconditions": "Dans le contexte de la recherche et de l'achat de billets d'avion, l'utilisateur demande le paiement d'une commande de vol ; l'ID de commande a été déterminé dans les messages précédents",
        "postconditions": "Le paiement est confirmé et le statut de la commande est mis à jour à 'payé'",
        "args": {
            "order_id": "ID de commande"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "L'utilisateur effectue le paiement d'une commande de billet de train",
        "preconditions": "Dans le scénario de recherche et d'achat de billets de train, l'utilisateur demande le paiement d'une commande de billet de train, l'ID de la commande a été déterminé dans le contexte précédent",
        "postconditions": "Confirmer le paiement et mettre à jour le statut de la commande à payé",
        "args": {
            "order_id": "ID de la commande"
        },
        "returns": "Informations sur le résultat du paiement",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "Recherche les commandes d'hôtel d'un utilisateur en fonction de son ID utilisateur et renvoie les informations incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de l'hôtel, le prix total de la commande, la date de commande, la date de mise à jour et le statut de la commande",
        "preconditions": "L'utilisateur souhaite rechercher des commandes d'hôtel",
        "postconditions": "Retourne les informations de commande, facilitant une modification ou une annulation ultérieure",
        "args": {
            "user_id": "ID utilisateur",
            "date": "Date",
            "status": "Statut de la commande"
        },
        "returns": "Informations sur les commandes d'hôtel de l'utilisateur spécifié",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "Interroge les commandes de billets d'attraction d'un utilisateur en fonction de son ID utilisateur, et renvoie les informations incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de l'attraction, le prix total de la commande, l'heure de passation de la commande, l'heure de mise à jour et le statut de la commande.",
        "preconditions": "La demande de l'utilisateur est de consulter les commandes de billets d'attraction.",
        "postconditions": "Renvoie les informations de commande, facilitant les modifications ou annulations ultérieures.",
        "args": {
            "user_id": "ID utilisateur",
            "date": "Date",
            "status": "Statut de la commande"
        },
        "returns": "Informations sur les commandes de billets d'attraction pour l'utilisateur spécifié.",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "Interroge les commandes de billets d'avion d'un utilisateur en fonction de son ID utilisateur et renvoie les informations incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de vol, le montant total de la commande, l'heure de commande, l'heure de mise à jour et le statut de la commande.",
        "preconditions": "La demande de l'utilisateur est de rechercher des commandes de billets d'avion.",
        "postconditions": "Retourne les informations de commande, facilitant les modifications ou annulations ultérieures.",
        "args": {
            "user_id": "ID utilisateur",
            "date": "Date",
            "status": "Statut de la commande"
        },
        "returns": "Informations sur les commandes de billets d'avion de l'utilisateur spécifié.",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "Recherche les commandes de billets de train d'un utilisateur selon son ID utilisateur et renvoie les détails incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID du train, le montant total, la date de commande, la date de mise à jour et le statut de la commande.",
        "preconditions": "L'utilisateur souhaite consulter ses commandes de billets de train.",
        "postconditions": "Renvoie les informations de la commande pour faciliter une modification ou une annulation ultérieure.",
        "args": {
            "user_id": "ID utilisateur",
            "date": "Date",
            "status": "Statut de la commande"
        },
        "returns": "Informations concernant les commandes de billets de train de l'utilisateur spécifié.",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "Récupérer les détails de la commande d'hôtel, incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de l'hôtel, le prix total de la commande, l'heure de passation, l'heure de mise à jour, le statut de la commande et les informations détaillées sur la chambre (type de chambre, date d'arrivée, prix, ID de la chambre)",
        "preconditions": "L'utilisateur demande à obtenir les détails de la commande d'hôtel, l'ID de commande a été déterminé dans le contexte précédent",
        "postconditions": "Retourne les détails de la commande",
        "args": {
            "order_id": "ID de commande"
        },
        "returns": "Détails de la commande",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "Récupérer les détails de la commande de billets d'attraction, comprenant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de l'attraction, le prix total de la commande, l'heure de la commande, l'heure de mise à jour, le statut de la commande et les informations détaillées de l'attraction de la commande (type de billet, date, prix, ID de billet)",
        "preconditions": "L'utilisateur demande à obtenir les détails de la commande de billets d'attraction, l'ID de commande a été identifié précédemment",
        "postconditions": "Retourne les détails de la commande",
        "args": {
            "order_id": "ID de commande"
        },
        "returns": "Détails de la commande",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "Récupérer les détails de la commande de billet d'avion, incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID de vol, le prix total de la commande, l'heure de commande, l'heure de mise à jour, le statut de la commande et les informations détaillées du billet de la commande (type de siège, date, prix, ID de siège)",
        "preconditions": "L'utilisateur demande à obtenir les détails de la commande de billet d'avion, l'ID de commande a été déterminé dans le contexte précédent",
        "postconditions": "Retourne les détails de la commande",
        "args": {
            "order_id": "ID de commande"
        },
        "returns": "Détails de la commande",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "Récupérer les détails de la commande de billet de train, incluant l'ID de commande, le type de commande, l'ID utilisateur, l'ID du train, le prix total de la commande, l'heure de passation de la commande, l'heure de mise à jour, le statut de la commande et les informations détaillées du billet de train de la commande (type de siège, date, prix, ID de siège)",
        "preconditions": "L'utilisateur demande à obtenir les détails de la commande de billet de train, l'ID de commande a été déterminé dans le contexte précédent",
        "postconditions": "Retourne les détails de la commande",
        "args": {
            "order_id": "ID de commande"
        },
        "returns": "Détails de la commande",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "Modifier une commande de billet de train, permet de changer la date de départ et gère automatiquement le complément ou le remboursement de la différence de prix.",
        "preconditions": "Dans le contexte de recherche et d'achat de billets de train, l'utilisateur demande la modification d'une commande de billet de train, et l'ID de la commande a été identifié précédemment.",
        "postconditions": "Modifie la commande et met à jour son statut. Si un complément de prix est requis, le statut de la commande passe à 'unpaid', sinon il reste inchangé. En cas de complément, l'utilisateur doit être invité à payer cette commande.",
        "args": {
            "order_id": "ID de la commande",
            "user_id": "ID de l'utilisateur",
            "new_date": "Nouvelle date de départ, format %Y-%m-%d"
        },
        "returns": "(Contenu de la commande modifiée, différence de prix, positif pour un complément, négatif pour un remboursement)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "Modifier la commande de billet d'avion, prend en charge la modification de la date de départ et gère automatiquement les compléments ou remboursements de différence de prix.",
        "preconditions": "Dans le scénario de recherche et d'achat de billets d'avion, l'utilisateur demande de modifier la commande de billet d'avion et l'ID de commande a été déterminé dans le contexte précédent.",
        "postconditions": "Modifie la commande et met à jour son statut. Si un complément de prix est nécessaire, le statut de la commande passe à unpaid, sinon il reste inchangé. En cas de complément, l'utilisateur doit être invité à régler cette commande.",
        "args": {
            "order_id": "ID de la commande",
            "user_id": "ID de l'utilisateur",
            "new_date": "Nouvelle date de départ, format %Y-%m-%d"
        },
        "returns": "(Contenu de la commande modifiée, différence de prix, positif indique un complément à payer, négatif indique un remboursement)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "L'utilisateur annule une commande d'hôtel déjà réservée",
        "preconditions": "Dans le scénario de recherche de réservation d'hôtel, l'utilisateur demande l'annulation de la commande d'hôtel, et l'ID de la commande a été déterminé dans le contexte précédent",
        "postconditions": "Annuler la commande et mettre à jour le statut de la commande. Si un remboursement de la différence est nécessaire, il suffit d'informer l'utilisateur",
        "args": {
            "order_id": "ID de la commande",
            "user_id": "ID de l'utilisateur"
        },
        "returns": "Le montant du remboursement pour l'annulation de la commande",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "L'utilisateur annule une commande de billets d'attraction déjà réservée.",
        "preconditions": "L'ID de commande est présent dans l'historique de la conversation ou une recherche de commande a déjà été effectuée, et l'utilisateur est autorisé à annuler cette commande.",
        "postconditions": "En cas de remboursement de la différence, il suffit d'informer l'utilisateur.",
        "args": {
            "order_id": "ID de commande",
            "user_id": "ID de l'utilisateur"
        },
        "returns": "Le montant du remboursement pour l'annulation de la commande.",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "L'utilisateur annule une commande de billet d'avion déjà réservée",
        "preconditions": "L'ID de commande est présent dans l'historique de la conversation ou une recherche de commande a déjà été effectuée, et l'utilisateur est autorisé à annuler cette commande",
        "postconditions": "S'il y a un remboursement de la différence, informez simplement l'utilisateur",
        "args": {
            "order_id": "ID de la commande",
            "user_id": "ID de l'utilisateur"
        },
        "returns": "Le montant du remboursement pour l'annulation de la commande",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "L'utilisateur annule une commande de billet de train déjà réservée",
        "preconditions": "L'identifiant de la commande est présent dans l'historique de la conversation ou une recherche de commande a déjà été effectuée, et l'utilisateur est autorisé à annuler cette commande",
        "postconditions": "S'il y a un remboursement de la différence, il suffit d'en informer l'utilisateur",
        "args": {
            "order_id": "Identifiant de la commande",
            "user_id": "Identifiant de l'utilisateur"
        },
        "returns": "Montant du remboursement pour l'annulation de la commande",
        "tool_type": "WRITE"
    },
}

# Tool descriptions - Japanese version
TOOL_DESCRIPTIONS_JA = {
    "get_ota_hotel_info": {
        "description": "ホテル情報を取得します。ホテル ID、名称、評価、スターランク、住所、タグ、部屋リストを含みます。",
        "preconditions": "ホテルの検索および予約のシーンで、ホテルの詳細情報を取得する必要がある場合。",
        "postconditions": "ホテルの詳細情報を返し、ユーザーが部屋を選択して予約できるよう案内します。",
        "args": {
            "hotel_id": "ホテル ID"
        },
        "returns": "ホテル情報",
        "tool_type": "READ"
    },

    "get_ota_attraction_info": {
        "description": "観光名所情報を取得します。観光名所 ID、名称、住所、説明、評価、営業時間、入場料金、チケット種類のリストを含みます。",
        "preconditions": "観光名所観光のシーンにおいて、観光名所の詳細情報を取得する必要がある場合",
        "postconditions": "観光名所の詳細情報を返却し、ユーザーがチケットを選択して注文するよう誘導します。",
        "args": {
            "attraction_id": "観光名所 ID"
        },
        "returns": "観光名所情報",
        "tool_type": "READ"
    },

    "get_ota_flight_info": {
        "description": "フライト情報を取得し、フライト ID、フライト番号、出発都市、到着都市、出発空港所在地、到着空港所在地、出発時刻、到着時刻、フライトタグ、座席タイプリストを含みます",
        "preconditions": "航空券の検索・購入シーンで、フライトの詳細情報を取得する必要がある場合",
        "postconditions": "フライトの詳細情報を返却し、ユーザーに座席選択と注文を促します",
        "args": {
            "flight_id": "フライト ID"
        },
        "returns": "フライト情報",
        "tool_type": "READ"
    },

    "get_ota_train_info": {
        "description": "列車情報を取得します。列車 ID、列車番号、出発都市、到着都市、出発駅位置、到着駅位置、出発時間、到着時間、列車タグ、座席タイプリストを含みます。",
        "preconditions": "切符の検索および購入のシナリオにおいて、列車の詳細情報を取得する必要がある場合。",
        "postconditions": "列車の詳細情報を返却し、ユーザーが座席を選択して注文できるよう誘導します。",
        "args": {
            "train_id": "列車 ID"
        },
        "returns": "列車情報",
        "tool_type": "READ"
    },

    "hotel_search_recommend": {
        "description": "旅行・宿泊シーンにおいて、ユーザーの場所に関するニーズと好みに基づき、適切なホテルオプションを推薦し、ホテル ID、名称、評価、星評価、住所、タグなどの基本情報を提供します。",
        "preconditions": "ユーザーがホテルの予約をリクエストし、ホテルに関連するキーワードまたは場所を指定した場合。",
        "postconditions": "条件に合致するホテルのリストを返します。ホテルの詳細（部屋リスト、価格など）を確認する必要がある場合は、ホテル詳細検索ツールを使用し、ユーザーにホテルの選択を促します。",
        "args": {
            "city_name": "都市名",
            "key_words": "検索キーワード（ホテル名、ホテル紹介などにマッチ）"
        },
        "returns": "ホテルの基本情報を構造化して出力",
        "tool_type": "READ"
    },

    "attractions_search_recommend": {
        "description": "ユーザーの場所に関するニーズと好みに基づいて、適切な観光地を推薦し、観光地 ID、名称、住所、説明、評価、営業時間を含む基本情報を提供します。",
        "preconditions": "ユーザーが観光地の予約をリクエストし、観光地に関連するキーワードまたは場所を指定した場合。",
        "postconditions": "条件に合致する観光地リストを返します。観光地の詳細（チケットリスト、価格など）を確認する必要がある場合は、観光地詳細照会ツールを使用し、ユーザーに観光地の選択を促します。",
        "args": {
            "city_name": "都市名",
            "key_words": "検索キーワード（観光地名、位置、住所、特徴などに一致）"
        },
        "returns": "観光地の基本情報を構造化して出力",
        "tool_type": "READ"
    },

    "flight_search_recommend": {
        "description": "ユーザーの場所に関するニーズと好みに基づき、適切なフライトオプションを推奨し、フライトの基礎情報を提供します。フライト id、フライト番号、出発都市、到着都市、出発空港の位置、到着空港の位置、出発時間、到着時間、フライトタグを含みます。",
        "preconditions": "ユーザーがフライトの予約をリクエストし、フライトに関連するキーワードまたは場所を指定した場合。",
        "postconditions": "条件に合致するフライトのリストを返します。フライトの詳細（座席タイプリスト、価格、日付など）を確認する必要がある場合は、フライト詳細照会ツールを使用し、ユーザーにフライトの選択を促します。",
        "args": {
            "departure": "出発都市",
            "destination": "目的地都市"
        },
        "returns": "フライトの基礎情報を構造化して出力します。",
        "tool_type": "READ"
    },

    "train_ticket_search": {
        "description": "ユーザーの場所に関するニーズと好みに基づき、適切な列車オプションを推奨し、列車チケットの基礎情報を提供します。列車 ID、列車番号、出発都市、到着都市、出発駅位置、到着駅位置、出発時間、到着時間、列車タグを含みます。",
        "preconditions": "ユーザーが列車の予約をリクエストし、列車に関連するキーワードまたは場所を指定した場合。",
        "postconditions": "条件に合致する列車チケットのリストを返します。列車チケットの詳細（座席タイプリスト、価格、日付など）を確認する必要がある場合は、列車チケット詳細照会ツールを使用し、ユーザーに列車チケットの選択を誘導します。",
        "args": {
            "departure": "出発都市",
            "destination": "目的地都市",
            "date": "出発日"
        },
        "returns": "列車の基礎情報を構造化して出力します。",
        "tool_type": "READ"
    },

    "create_hotel_order": {
        "description": "ユーザーがホテルを予約する際、システムはユーザーのニーズ（ホテル名、チェックイン日、人数など）に基づいて注文を生成します",
        "preconditions": "ユーザーはログイン済みであり、有効なユーザー識別子（user_id）を提供していること。ユーザーは有効なホテル名（hotel_name）と部屋タイプ（room_type）を提供していること。システムは対象ホテルの情報を持っており、かつ該当ホテルがリクエストされた日に空室があること",
        "postconditions": "注文を生成し、ユーザーに支払いを確認してもらいます",
        "args": {
            "hotel_id": "ホテル ID",
            "room_id": "部屋 ID",
            "user_id": "ユーザー ID"
        },
        "returns": "注文作成操作のフィードバック出力",
        "tool_type": "WRITE"
    },

    "create_attraction_order": {
        "description": "ユーザーが観光スポットと日付を指定してチケットを購入し、システムがチケット情報を返して注文を行います。",
        "preconditions": "観光スポット観光のシーンにおいて、ユーザーがスポットの予約をリクエストし、予約に必要な情報を提供していること。",
        "postconditions": "注文が生成され、ユーザーに支払い確認を促します。",
        "args": {
            "attraction_id": "観光スポット ID",
            "ticket_id": "チケット ID",
            "user_id": "ユーザー ID",
            "date": "訪問日、形式は %Y-%m-%d",
            "quantity": "数量"
        },
        "returns": "注文作成操作のフィードバック出力",
        "tool_type": "WRITE"
    },

    "create_flight_order": {
        "description": "ユーザーがフライト番号、日付、座席タイプ、数量に基づいて航空券を購入し、システムが航空券の関連情報を返して注文処理を行います",
        "preconditions": "航空券の検索・購入シーンにおいて、ユーザーがフライトの予約をリクエストし、予約に必要な情報を提供している場合",
        "postconditions": "注文が生成され、ユーザーに支払いの確認を依頼します",
        "args": {
            "flight_id": "フライト ID",
            "seat_id": "座席 ID",
            "user_id": "ユーザー ID",
            "date": "出発日",
            "quantity": "数量"
        },
        "returns": "注文作成操作のフィードバック出力",
        "tool_type": "WRITE"
    },

    "create_train_order": {
        "description": "ユーザーは列車番号、日付、座席タイプ、数量に基づいて列車チケットを購入し、システムは列車チケットの関連情報を返して注文を行います",
        "preconditions": "列車チケットの検索および購入シーンにおいて、ユーザーが列車の予約をリクエストし、予約に必要な情報を提供していること",
        "postconditions": "注文が生成され、ユーザーに支払い確認を促します",
        "args": {
            "train_id": "列車 ID",
            "seat_id": "座席 ID",
            "user_id": "ユーザー ID",
            "date": "出発日",
            "quantity": "数量"
        },
        "returns": "注文作成操作のフィードバック出力",
        "tool_type": "WRITE"
    },

    "pay_hotel_order": {
        "description": "ユーザーがホテルの注文支払いを行う",
        "preconditions": "ホテルの検索・予約シーンで、ユーザーがホテル注文の支払いをリクエストし、前の文脈で注文 ID が確定されていること",
        "postconditions": "支払いを確認し、注文ステータスを「支払い済み」に更新する",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報",
        "tool_type": "WRITE"
    },

    "pay_attraction_order": {
        "description": "ユーザーがチケット注文の支払いを行う",
        "preconditions": "観光地のシナリオにおいて、ユーザーが観光チケットの注文の支払いをリクエストし、前の文脈で注文 ID が確定されていること",
        "postconditions": "支払いを確認し、注文ステータスを「支払い済み」に更新する",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報",
        "tool_type": "WRITE"
    },

    "pay_flight_order": {
        "description": "ユーザーが航空券の注文の支払いを行う",
        "preconditions": "航空券の検索・購入シーンにおいて、ユーザーがフライト注文の支払いをリクエストし、前述で注文 ID が確定していること",
        "postconditions": "支払いを確認し、注文ステータスを「支払い済み」に更新する",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報",
        "tool_type": "WRITE"
    },

    "pay_train_order": {
        "description": "ユーザーが鉄道切符の注文支払いを行う",
        "preconditions": "鉄道切符の検索・購入シーンにおいて、ユーザーが鉄道切符の注文支払いをリクエストし、前述で注文 ID が確定されていること",
        "postconditions": "支払いを確認し、注文ステータスを「支払い済み」に更新する",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "支払い結果情報",
        "tool_type": "WRITE"
    },

    "search_hotel_order": {
        "description": "ユーザー ID に基づいてユーザーのホテル注文を検索し、注文 ID、注文タイプ、ユーザー ID、ホテル ID、注文合計金額、注文時間、更新時間、注文ステータスを含む情報を返します",
        "preconditions": "ユーザーの要件がホテル注文の検索であること",
        "postconditions": "注文情報を返し、後での変更またはキャンセルを容易にします",
        "args": {
            "user_id": "ユーザー ID",
            "date": "日付",
            "status": "注文ステータス"
        },
        "returns": "指定されたユーザーのホテル注文情報",
        "tool_type": "READ"
    },

    "search_attraction_order": {
        "description": "ユーザー ID に基づいて、ユーザーの観光地チケット注文を検索し、注文 ID、注文タイプ、ユーザー ID、観光地 ID、注文合計金額、注文時間、更新時間、注文ステータスを含む情報を返します。",
        "preconditions": "ユーザーの要件が観光地チケット注文の検索であること。",
        "postconditions": "注文情報を返却し、後での修正またはキャンセルを容易にします。",
        "args": {
            "user_id": "ユーザー ID",
            "date": "日付",
            "status": "注文ステータス"
        },
        "returns": "指定されたユーザーの観光地チケット注文情報",
        "tool_type": "READ"
    },

    "search_flight_order": {
        "description": "ユーザー ID に基づいてユーザーの航空券注文を検索し、注文 ID、注文タイプ、ユーザー ID、フライト ID、注文総額、注文時間、更新時間、注文ステータスを含む情報を返します",
        "preconditions": "ユーザーの要件が航空券注文の検索であること",
        "postconditions": "注文情報を返し、後での変更またはキャンセルを容易にします",
        "args": {
            "user_id": "ユーザー ID",
            "date": "日付",
            "status": "注文ステータス"
        },
        "returns": "指定されたユーザーの航空券注文情報",
        "tool_type": "READ"
    },

    "search_train_order": {
        "description": "ユーザー ID に基づいてユーザーの列車切符注文を検索し、注文 ID、注文タイプ、ユーザー ID、列車 ID、注文合計金額、注文時間、更新時間、注文ステータスを含む情報を返します",
        "preconditions": "ユーザーの要件が列車切符注文の検索であること",
        "postconditions": "注文情報を返し、後での修正またはキャンセルを容易にします",
        "args": {
            "user_id": "ユーザー ID",
            "date": "日付",
            "status": "注文ステータス"
        },
        "returns": "指定されたユーザーの列車切符注文情報",
        "tool_type": "READ"
    },

    "get_hotel_order_detail": {
        "description": "ホテル注文詳細を取得します。注文 ID、注文タイプ、ユーザー ID、ホテル ID、注文合計金額、注文日時、更新日時、注文ステータス、および注文部屋の詳細情報（部屋タイプ、チェックイン日、価格、部屋 ID）を含みます。",
        "preconditions": "ユーザーがホテル注文詳細の取得を要求し、前の文脈で注文 ID が確定されていること。",
        "postconditions": "注文詳細を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文詳細",
        "tool_type": "READ"
    },

    "get_attraction_order_detail": {
        "description": "観光地チケットの注文詳細を取得します。注文 ID、注文タイプ、ユーザー ID、観光地 ID、注文合計金額、注文時間、更新時間、注文ステータス、および注文観光地の詳細情報（チケットタイプ、日付、価格、チケット ID）が含まれます。",
        "preconditions": "ユーザーが観光地チケットの注文詳細の取得をリクエストしており、前の文脈で注文 ID が確定されていること。",
        "postconditions": "注文詳細を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文詳細",
        "tool_type": "READ"
    },

    "get_flight_order_detail": {
        "description": "航空券の注文詳細を取得します。注文 ID、注文タイプ、ユーザー ID、フライト ID、注文合計金額、注文時間、更新時間、注文ステータス、および注文航空券の詳細情報（シートタイプ、日付、価格、シート ID）を含みます。",
        "preconditions": "ユーザーが航空券の注文詳細の取得を要求し、文脈内で注文 ID が確定されていること。",
        "postconditions": "注文詳細を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文詳細",
        "tool_type": "READ"
    },

    "get_train_order_detail": {
        "description": "鉄道チケットの注文詳細を取得します。注文 ID、注文タイプ、ユーザー ID、列車 ID、注文合計金額、注文時間、更新時間、注文ステータス、およびチケットの詳細情報（座席タイプ、日付、価格、座席 ID）が含まれます。",
        "preconditions": "ユーザーが鉄道チケットの注文詳細の取得をリクエストし、前の会話で注文 ID が確定されていること。",
        "postconditions": "注文詳細を返します。",
        "args": {
            "order_id": "注文 ID"
        },
        "returns": "注文詳細",
        "tool_type": "READ"
    },

    "modify_train_order": {
        "description": "鉄道切符の注文を変更し、出発日の変更をサポートし、差額の追加支払いまたは返金を自動的に処理します。",
        "preconditions": "鉄道切符の検索および購入のシナリオにおいて、ユーザーが鉄道切符の注文変更を請求し、前の会話で注文 ID が確定されていること",
        "postconditions": "注文を変更し、注文ステータスを更新します。差額追加支払いが必要な場合は注文ステータスを unpaid に変更し、そうでない場合は元のステータスを維持します。差額追加支払いが必要な場合、ユーザーに当該注文の支払いを案内する必要があります",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID",
            "new_date": "新しい出発日、フォーマットは %Y-%m-%d"
        },
        "returns": "(変更後の注文内容，差額，正は追加支払いが必要，負は返金)",
        "tool_type": "WRITE"
    },

    "modify_flight_order": {
        "description": "航空券注文を変更し、出発日の変更をサポートし、差額の追加支払いまたは返金を自動的に処理します。",
        "preconditions": "航空券検索・購入シーンにおいて、ユーザーが航空券注文の変更を要求し、前の会話で注文 ID が確定されていること。",
        "postconditions": "注文を変更し、注文ステータスを更新します。差額の追加支払いが必要な場合は注文ステータスを unpaid に変更し、そうでない場合は元のステータスを維持します。差額の追加支払いが必要な場合、ユーザーに当該注文の支払いを案内する必要があります。",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID",
            "new_date": "新しい出発日、フォーマットは %Y-%m-%d"
        },
        "returns": "(変更後の注文内容，差額，正は追加支払いが必要，負は返金)",
        "tool_type": "WRITE"
    },

    "cancel_hotel_order": {
        "description": "ユーザーが予約済みのホテル注文をキャンセルする",
        "preconditions": "ホテル予約照会のシーンで、ユーザーがホテル注文のキャンセルを依頼し、これまでの会話で注文 ID が特定されていること",
        "postconditions": "注文をキャンセルして注文ステータスを更新します。差額返金が必要な場合は、ユーザーにその旨を通知します",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID"
        },
        "returns": "注文キャンセル時の返金額",
        "tool_type": "WRITE"
    },

    "cancel_attraction_order": {
        "description": "ユーザーが予約済みの観光地チケットの注文をキャンセルする",
        "preconditions": "過去の会話に注文 ID があるか、すでに注文照会が行われており、ユーザーに該注文をキャンセルする権限があること",
        "postconditions": "差額返金がある場合は、ユーザーに通知するだけでよい",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID"
        },
        "returns": "注文キャンセルの返金額",
        "tool_type": "WRITE"
    },

    "cancel_flight_order": {
        "description": "ユーザーが予約済みの航空券注文をキャンセルする",
        "preconditions": "過去の会話に注文 ID がある、またはすでに注文照会が行われていること。ユーザーにはその注文をキャンセルする権限があること。",
        "postconditions": "差額返金がある場合は、ユーザーに通知するだけでよい。",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID"
        },
        "returns": "注文キャンセルによる返金金額",
        "tool_type": "WRITE"
    },

    "cancel_train_order": {
        "description": "ユーザーが予約済みの鉄道の切符の注文をキャンセルする",
        "preconditions": "過去の会話に注文 ID が存在する、またはすでに注文照会が行われており、ユーザーに該注文をキャンセルする権限があること",
        "postconditions": "差額返金がある場合は、ユーザーに告知するだけでよい",
        "args": {
            "order_id": "注文 ID",
            "user_id": "ユーザー ID"
        },
        "returns": "注文キャンセルの返金額",
        "tool_type": "WRITE"
    },
}

# Create OTA tool schema manager
_schema_manager = create_tool_schema_manager("ota", TOOL_DESCRIPTIONS_ZH, TOOL_DESCRIPTIONS_EN, japanese=TOOL_DESCRIPTIONS_JA, french=TOOL_DESCRIPTIONS_FR, russian=TOOL_DESCRIPTIONS_RU, arabic=TOOL_DESCRIPTIONS_AR, hindi=TOOL_DESCRIPTIONS_HI, thai=TOOL_DESCRIPTIONS_TH, spanish=TOOL_DESCRIPTIONS_ES, korean=TOOL_DESCRIPTIONS_KO, indonesian=TOOL_DESCRIPTIONS_ID, hebrew=TOOL_DESCRIPTIONS_HE, turkish=TOOL_DESCRIPTIONS_TR, vietnamese=TOOL_DESCRIPTIONS_VI, malay=TOOL_DESCRIPTIONS_MS, belarusian=TOOL_DESCRIPTIONS_BE, punjabi=TOOL_DESCRIPTIONS_PA, kazakh=TOOL_DESCRIPTIONS_KK, khmer=TOOL_DESCRIPTIONS_KM, burmese=TOOL_DESCRIPTIONS_MY, lao=TOOL_DESCRIPTIONS_LO, tamil=TOOL_DESCRIPTIONS_TA, telugu=TOOL_DESCRIPTIONS_TE)

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
