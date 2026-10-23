"""
Hard Constraint Evaluation Module
Implements evaluation strategies for each hard constraint type
"""

from typing import Dict, Any, Tuple, List, Optional, Union
import re
import unicodedata


def _norm_name(value: Any) -> str:
    """Normalize an entity name for comparison.

    NFC-normalizes and strips. The rendered per-language DBs and the
    `meta_info` anchors are byte-frozen artifacts that can disagree on Unicode
    normalization form (e.g. the shipped `my`/`pa` anchors carry non-NFC
    sequences); the agent copies names verbatim from the DB, so a
    normalization-only mismatch is data noise, not a planning error. Both
    sides of every name comparison go through this helper.
    """
    if not isinstance(value, str):
        value = '' if value is None else str(value)
    return unicodedata.normalize('NFC', value).strip()


def _norm_mode(value: Any) -> str:
    """Normalize a transport `mode` word: NFC, casefold, collapse whitespace."""
    if not isinstance(value, str):
        value = '' if value is None else str(value)
    return ' '.join(unicodedata.normalize('NFC', value).casefold().split())


FLIGHT_MODE_WORDS = frozenset(_norm_mode(word) for word in [
    # en/zh canonical first, then per-language variants a converter may emit.
    'flight', '飞机', 'airplane', 'plane', 'aircraft',
    'vuelo', 'avión',  # Spanish
    'vol', 'avion',  # French
    'voo',  # Portuguese
    'volo', 'aereo',  # Italian
    'flug', 'flugzeug',  # German
    'penerbangan', 'pesawat', 'pesawat terbang',  # Indonesian / Malay
    'chuyến bay', 'máy bay',  # Vietnamese
    'uçuş', 'uçak',  # Turkish
    'рейс', 'авиарейс', 'самолёт', 'самолет',  # Russian
    'пераліт', 'самалёт',  # Belarusian
    'ұшу', 'ұшақ', 'әуе рейсі',  # Kazakh
    'טיסה', 'מטוס',  # Hebrew
    'رحلة', 'طيران', 'طائرة',  # Arabic
    'उड़ान', 'विमान', 'हवाई जहाज',  # Hindi
    'ਉਡਾਣ', 'ਜਹਾਜ਼', 'ਹਵਾਈ ਜਹਾਜ਼',  # Panjabi
    'เที่ยวบิน', 'เครื่องบิน',  # Thai
    'ការហោះហើរ', 'យន្តហោះ',  # Khmer
    'ການບິນ', 'ຖ້ຽວບິນ', 'ເຮືອບິນ',  # Lao
    'လေယာဉ်ခရီးစဉ်', 'လေယာဉ်',  # Burmese
    'フライト', '飛行機', '航空便',  # Japanese
    '항공편', '비행', '비행기', '항공기',  # Korean
    'விமானம்',  # Tamil
    'విమానం',  # Telugu
])

TRAIN_MODE_WORDS = frozenset(_norm_mode(word) for word in [
    # en/zh canonical first, then per-language variants a converter may emit.
    'train', '火车', 'railway', '高铁', 'gaotie', '动车',
    'high-speed train', 'high speed train', 'high-speed rail', 'bullet train',
    'tren',  # Spanish / Turkish
    'trem',  # Portuguese
    'treno',  # Italian
    'zug',  # German
    'kereta api', 'kereta',  # Indonesian / Malay
    'tàu hỏa', 'tàu', 'tàu cao tốc',  # Vietnamese
    'поезд',  # Russian
    'цягнік',  # Belarusian
    'пойыз',  # Kazakh
    'רכבת',  # Hebrew
    'قطار',  # Arabic
    'ट्रेन', 'रेल', 'रेलगाड़ी',  # Hindi
    'ਟ੍ਰੇਨ', 'ਰੇਲ',  # Panjabi
    'รถไฟ',  # Thai
    'រថភ្លើង',  # Khmer
    'ລົດໄຟ',  # Lao
    'ရထား',  # Burmese
    '電車', '列車', '新幹線',  # Japanese
    '기차', '열차', 'ktx',  # Korean
    'ரயில்',  # Tamil
    'రైలు',  # Telugu
])


def eval_hard(plan: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Tuple[Optional[bool], Optional[str]]]:
    """
    Evaluate hard constraint satisfaction
    
    Args:
        plan: Parsed travel plan JSON (contains daily_plans and budget_summary)
        meta: Query metadata (contains hard_constraints field)
    
    Returns:
        Dict[str, Tuple[bool, str]]: constraint_name -> (is_satisfied, error_message)
    """
    res: Dict[str, Tuple[Optional[bool], Optional[str]]] = {}
    
    # If no hard_constraints field, return default result
    if 'hard_constraints' not in meta:
        return res
    
    hard_constraints = meta['hard_constraints']
    
    # Iterate through all hard constraints and dispatch to corresponding evaluation functions
    for constraint_key, constraint_data in hard_constraints.items():
        try:
            # Dispatch based on constraint type
            if constraint_key.startswith('flight_'):
                result = _eval_flight_constraint(constraint_key, constraint_data, plan, meta)
            elif constraint_key.startswith('train_'):
                result = _eval_train_constraint(constraint_key, constraint_data, plan, meta)
            elif constraint_key.startswith('hotel_'):
                result = _eval_hotel_constraint(constraint_key, constraint_data, plan, meta)
            elif constraint_key.startswith('restaurant_'):
                result = _eval_restaurant_constraint(constraint_key, constraint_data, plan, meta)
            elif constraint_key.startswith('attraction_'):
                result = _eval_attraction_constraint(constraint_key, constraint_data, plan, meta)
            elif constraint_key == 'budget_constraint':
                result = _eval_budget_constraint(constraint_data, plan, meta)
            else:
                result = (None, f"Unknown constraint type: {constraint_key}")
            
            res[constraint_key] = result
        except Exception as e:
            res[constraint_key] = (False, f"Evaluation error: {str(e)}")
    
    
    
    return res


# ============================================================================
# Flight Constraints
# ============================================================================

def _eval_flight_constraint(constraint_key: str, constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate flight-related constraints (unified logic)
    
    All flight constraints check if required flight numbers are in the plan.
    This unified approach:
    - Extracts flight list only once (performance optimization)
    - Uses set lookup for O(1) search instead of O(n)
    - Eliminates code duplication across multiple similar functions
    
    Supported constraints:
    - flight_seat_class: Check both outbound and inbound flights
    - flight_seat_status: Check both outbound and inbound flights
    - flight_cheapest_airline_direct: Check outbound flight only
    - flight_cheapest_direct: Check outbound flight only
    - flight_earliest_departure_direct: Check outbound flight only
    - flight_cheapest_manufacturer_direct: Check outbound flight only
    - flight_shortest_duration_direct: Check outbound or inbound flight (NEW)
    - flight_earliest_airline_direct: Check outbound flight only (NEW)
    - flight_departure_time_range: Check outbound flight only (NEW)
    - flight_arrival_time_range: Check inbound flight only (NEW)
    """
    # Extract flights from plan once (performance optimization)
    flights = _extract_flights_from_plan(plan)
    flight_numbers = {flight['flight_no'] for flight in flights}
    
    # Collect required flight numbers based on constraint data
    required_flights = []
    
    # Check for outbound flight
    if 'outbound_flight_no' in constraint_data:
        required_flights.append(('outbound', constraint_data['outbound_flight_no']))
    
    # Check for inbound flight
    if 'inbound_flight_no' in constraint_data:
        required_flights.append(('inbound', constraint_data['inbound_flight_no']))
    
    # Validate all required flights are present
    for direction, flight_no in required_flights:
        if flight_no not in flight_numbers:
            return (False, f"Required {direction} flight not found: {flight_no}")
    
    return (True, None)


# ============================================================================
# Train Constraints
# ============================================================================

def _eval_train_constraint(constraint_key: str, constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate train-related constraints (unified logic)
    
    All train constraints check if required train numbers are in the plan.
    This unified approach:
    - Extracts train list only once (performance optimization)
    - Uses set lookup for O(1) search instead of O(n)
    - Eliminates code duplication across multiple similar functions
    
    Supported constraints:
    - train_seat_class: Check both outbound and inbound trains
    - train_seat_status: Check both outbound and inbound trains
    - train_shortest_duration_direct: Check outbound or inbound train (NEW)
    - train_cheapest_direct: Check outbound or inbound train (NEW)
    - train_earliest_departure_direct: Check outbound train only (NEW)
    - train_latest_arrival_direct: Check inbound train only (NEW)
    - train_cheapest_train_type: Check outbound train only (NEW)
    - train_departure_time_range: Check outbound train only (NEW)
    """
    # Extract trains from plan once (performance optimization)
    trains = _extract_trains_from_plan(plan)
    train_numbers = {train['train_no'] for train in trains}
    
    # Collect required train numbers based on constraint data
    required_trains = []
    
    # Check for outbound train
    if 'outbound_train_no' in constraint_data:
        required_trains.append(('outbound', constraint_data['outbound_train_no']))
    
    # Check for inbound train
    if 'inbound_train_no' in constraint_data:
        required_trains.append(('inbound', constraint_data['inbound_train_no']))
    
    # Validate all required trains are present
    for direction, train_no in required_trains:
        if train_no not in train_numbers:
            return (False, f"Required {direction} train not found: {train_no}")
    
    return (True, None)


# ============================================================================
# Hotel Constraints
# ============================================================================

def _eval_hotel_constraint(constraint_key: str, constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate hotel-related constraints (unified logic)
    
    All hotel constraints check if the required hotel name is in the plan.
    This unified approach:
    - Extracts hotel list only once (performance optimization)
    - Uses set lookup for O(1) search instead of O(n)
    - Eliminates code duplication across multiple similar functions
    
    Supported constraints:
    - hotel_cheapest_brand: Check if cheapest hotel of specified brand is used
    - hotel_highest_rated: Check if highest rated hotel is used
    - hotel_cheapest_star: Check if cheapest hotel of specified star rating is used
    - hotel_newest_decoration: Check if hotel with newest decoration is used (NEW)
    - hotel_brand_highest_rated: Check if highest rated hotel within brand is used (NEW)
    - hotel_star_highest_rated: Check if highest rated hotel within star level is used (NEW)
    - hotel_price_range: Check if hotel within price range is used (NEW)
    - hotel_star_service_required: Check if hotel with specified star and service is used (NEW)
    """
    # Extract hotels from plan once (performance optimization)
    hotels = _extract_hotels_from_plan(plan)
    hotel_names = {_norm_name(hotel['name']) for hotel in hotels}

    # Get required hotel name from constraint data
    required_hotel_name = constraint_data.get('hotel_name')

    if not required_hotel_name:
        return (False, "No hotel name specified in constraint data")

    # Check if required hotel is in the plan
    if _norm_name(required_hotel_name) not in hotel_names:
        # Generate appropriate error message based on constraint type
        if constraint_key == 'hotel_cheapest_brand':
            brand = constraint_data.get('brand', 'specified')
            return (False, f"Required {brand} brand hotel not found: {required_hotel_name}")
        elif constraint_key == 'hotel_highest_rated':
            return (False, f"Required highest rated hotel not found: {required_hotel_name}")
        elif constraint_key == 'hotel_cheapest_star':
            star = constraint_data.get('hotel_star', 'specified')
            return (False, f"Required {star}-star hotel not found: {required_hotel_name}")
        elif constraint_key == 'hotel_newest_decoration':
            return (False, f"Required hotel with newest decoration not found: {required_hotel_name}")
        elif constraint_key == 'hotel_brand_highest_rated':
            brand = constraint_data.get('brand', 'specified')
            return (False, f"Required highest rated {brand} hotel not found: {required_hotel_name}")
        elif constraint_key == 'hotel_star_highest_rated':
            star = constraint_data.get('hotel_star', 'specified')
            return (False, f"Required highest rated {star}-star hotel not found: {required_hotel_name}")
        elif constraint_key == 'hotel_price_range':
            price_range = constraint_data.get('price_range', 'specified')
            return (False, f"Required hotel in price range {price_range} not found: {required_hotel_name}")
        elif constraint_key == 'hotel_star_service_required':
            star = constraint_data.get('hotel_star', 'specified')
            service = constraint_data.get('required_service_cn', 'specified service')
            return (False, f"Required {star}-star hotel with {service} not found: {required_hotel_name}")
        else:
            return (False, f"Required hotel not found: {required_hotel_name}")
    
    return (True, None)


# ============================================================================
# Restaurant Constraints
# ============================================================================

def _eval_restaurant_constraint(constraint_key: str, constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate restaurant-related constraints (unified logic)
    
    All restaurant constraints check if the required restaurant name is in the plan.
    This unified approach:
    - Extracts restaurant list only once (performance optimization)
    - Uses set lookup for O(1) search instead of O(n)
    - Eliminates code duplication across multiple similar functions
    
    Supported constraints:
    - restaurant_cheapest_nearby_attraction: Check if cheapest restaurant near attraction is used
    - restaurant_highest_rated: Check if highest rated restaurant near attraction is used
    - restaurant_must_eat_named: Check if must-eat named restaurant is used
    - restaurant_closest_to_attraction: Check if closest restaurant to attraction is used
    - restaurant_specific_cuisine_nearby: Check if specific cuisine restaurant near attraction is used (NEW)
    - restaurant_specific_tag_nearby: Check if restaurant with specific tag near attraction is used (NEW)
    """
    # Extract restaurants from plan once (performance optimization)
    restaurants = _extract_restaurants_from_plan(plan)
    restaurant_names = {_norm_name(restaurant['name']) for restaurant in restaurants}

    # Get required restaurant name from constraint data
    required_restaurant = constraint_data.get('restaurant_name')

    if not required_restaurant:
        return (False, "No restaurant name specified in constraint data")

    # Check if required restaurant is in the plan
    if _norm_name(required_restaurant) not in restaurant_names:
        # Generate appropriate error message based on constraint type
        if constraint_key == 'restaurant_cheapest_nearby_attraction':
            attraction = constraint_data.get('attraction_name', 'specified attraction')
            return (False, f"Required restaurant near {attraction} not found: {required_restaurant}")
        elif constraint_key == 'restaurant_highest_rated':
            attraction = constraint_data.get('attraction_name', 'specified attraction')
            return (False, f"Required highly rated restaurant near {attraction} not found: {required_restaurant}")
        elif constraint_key == 'restaurant_must_eat_named':
            return (False, f"Required must-eat restaurant not found: {required_restaurant}")
        elif constraint_key == 'restaurant_closest_to_attraction':
            attraction = constraint_data.get('attraction_name', 'specified attraction')
            return (False, f"Required closest restaurant to {attraction} not found: {required_restaurant}")
        elif constraint_key == 'restaurant_specific_cuisine_nearby':
            attraction = constraint_data.get('attraction_name', 'specified attraction')
            cuisine = constraint_data.get('cuisine_type', 'specified cuisine')
            return (False, f"Required {cuisine} restaurant near {attraction} not found: {required_restaurant}")
        elif constraint_key == 'restaurant_specific_tag_nearby':
            attraction = constraint_data.get('attraction_name', 'specified attraction')
            tag = constraint_data.get('required_tag_cn', 'specified tag')
            return (False, f"Required restaurant with {tag} near {attraction} not found: {required_restaurant}")
        else:
            return (False, f"Required restaurant not found: {required_restaurant}")
    
    return (True, None)


# ============================================================================
# Attraction Constraints
# ============================================================================

def _eval_attraction_constraint(constraint_key: str, constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate attraction-related constraints (unified logic)
    
    All attraction constraints check if required attraction names are in the plan.
    This unified approach:
    - Extracts attraction list only once (performance optimization)
    - Uses set lookup for O(1) search instead of O(n)
    - Eliminates code duplication across multiple similar functions
    - All constraints use 'attraction_names' list format (even single-item constraints)
    
    Supported constraints:
    - attraction_must_visit_named: Check if all must-visit named attractions are included
    - attraction_all_of_type: Check if all attractions of specified type are included
    - attraction_top_rated_must_visit: Check if top 3 rated attractions are included (NEW)
    - attraction_all_free_attractions: Check if all free attractions are included (NEW)
    - attraction_type_highest_rated: Check if highest rated attraction of specific type is included (NEW)
    
    Note: All constraints now return 'attraction_names' as a list, even if only one attraction.
    """
    # Extract attractions from plan once (performance optimization)
    attractions = _extract_attractions_from_plan(plan)
    attraction_names = {_norm_name(attr['name']) for attr in attractions}

    # All attraction constraints now use 'attraction_names' list (unified format)
    required_attractions = constraint_data.get('attraction_names', [])

    if not required_attractions:
        return (False, "No attraction names specified in constraint data")

    # Check if all required attractions are in the plan
    missing_attractions = []
    for required_attraction in required_attractions:
        if _norm_name(required_attraction) not in attraction_names:
            missing_attractions.append(required_attraction)
    
    if missing_attractions:
        # Generate appropriate error message based on constraint type
        if constraint_key == 'attraction_must_visit_named':
            return (False, f"Missing required attractions: {', '.join(missing_attractions)}")
        elif constraint_key == 'attraction_all_of_type':
            attraction_type = constraint_data.get('attraction_type', 'specified')
            return (False, f"Missing {attraction_type} type attractions: {', '.join(missing_attractions)}")
        elif constraint_key == 'attraction_top_rated_must_visit':
            return (False, f"Missing top rated attractions: {', '.join(missing_attractions)}")
        elif constraint_key == 'attraction_all_free_attractions':
            return (False, f"Missing free attractions: {', '.join(missing_attractions)}")
        elif constraint_key == 'attraction_type_highest_rated':
            attraction_type = constraint_data.get('attraction_type', 'specified')
            return (False, f"Required highest rated {attraction_type} attraction not found: {', '.join(missing_attractions)}")
        else:
            return (False, f"Missing attractions: {', '.join(missing_attractions)}")
    
    return (True, None)


# ============================================================================
# Helper Functions - Extract information from plan
# ============================================================================

def _extract_flights_from_plan(plan: Dict) -> List[Dict]:
    """Extract all flight information from plan"""
    flights = []
    
    if 'daily_plans' not in plan:
        return flights
    
    for day_plan in plan['daily_plans']:
        if 'activities' not in day_plan:
            continue
        
        for activity in day_plan['activities']:
            if activity.get('type') == 'travel_intercity_public':
                details = activity.get('details', {})
                mode = _norm_mode(details.get('mode', ''))
                if mode in FLIGHT_MODE_WORDS:
                    flights.append({
                        'flight_no': details.get('number', ''),
                        'airline': details.get('number', ''),  # Airline usually in flight number
                    })
    
    return flights


def _extract_trains_from_plan(plan: Dict) -> List[Dict]:
    """Extract all train information from plan"""
    trains = []
    
    if 'daily_plans' not in plan:
        return trains
    
    for day_plan in plan['daily_plans']:
        if 'activities' not in day_plan:
            continue
        
        for activity in day_plan['activities']:
            if activity.get('type') == 'travel_intercity_public':
                details = activity.get('details', {})
                mode = _norm_mode(details.get('mode', ''))
                if mode in TRAIN_MODE_WORDS:
                    trains.append({
                        'train_no': details.get('number', ''),
                    })
    
    return trains


def _extract_hotels_from_plan(plan: Dict) -> List[Dict]:
    """Extract all hotel information from plan"""
    hotels = []
    
    if 'daily_plans' not in plan:
        return hotels
    
    for day_plan in plan['daily_plans']:
        accommodation = day_plan.get('accommodation')
        if accommodation:
            hotels.append({
                'name': accommodation.get('name', ''),
            })
    
    return hotels


def _extract_restaurants_from_plan(plan: Dict) -> List[Dict]:
    """Extract all restaurant information from plan"""
    restaurants = []
    
    if 'daily_plans' not in plan:
        return restaurants
    
    for day_plan in plan['daily_plans']:
        if 'activities' not in day_plan:
            continue
        
        for activity in day_plan['activities']:
            if activity.get('type') == 'meal':
                details = activity.get('details', {})
                restaurants.append({
                    'name': details.get('name', ''),
                })
    
    return restaurants


def _extract_attractions_from_plan(plan: Dict) -> List[Dict]:
    """Extract all attraction information from plan"""
    attractions = []
    
    if 'daily_plans' not in plan:
        return attractions
    
    for day_plan in plan['daily_plans']:
        if 'activities' not in day_plan:
            continue
        
        for activity in day_plan['activities']:
            if activity.get('type') == 'attraction':
                details = activity.get('details', {})
                attractions.append({
                    'name': details.get('name', ''),
                })
    
    return attractions


# ============================================================================
# Budget Constraints
# ============================================================================

def _eval_budget_constraint(constraint_data: Dict, plan: Dict, meta: Dict) -> Tuple[bool, Optional[str]]:
    """
    Evaluate budget constraint
    
    Check if the calculated actual budget does not exceed the maximum budget constraint.
    Uses the same calculation logic as check_budget_accuracy in constraints_commonsense.py
    
    Args:
        constraint_data: Budget constraint data containing:
            - max_budget: Maximum allowed budget
        plan: Travel plan containing daily_plans
        meta: Query metadata containing people_number and room_number
    
    Returns:
        (True, None) if actual budget is within limit
        (False, error_message) if budget exceeds limit or data is missing
    """
    max_budget = constraint_data.get('max_budget')
    
    if max_budget is None:
        return (False, "Budget constraint missing max_budget value")
    
    try:
        max_budget = float(max_budget)
    except (ValueError, TypeError):
        return (False, f"Invalid max_budget value: {max_budget}")
    
    # Get daily plans
    daily_plans = plan.get('daily_plans', [])
    if not daily_plans:
        return (False, "Plan missing daily_plans")
    
    # Get meta info
    people_number = int(meta.get("people_number", 1))
    room_number = int(meta.get("room_number", 1))
    
    # Calculate actual costs (same logic as check_budget_accuracy)
    transportation_cost = 0.0
    accommodation_cost = 0.0
    meals_cost = 0.0
    attractions_cost = 0.0
    
    # 1. Calculate transportation costs (intercity)
    for day_idx, day in enumerate(daily_plans):
        # For transfers (multiple intercity in same day), each segment shows total price
        # So we only count the FIRST one to avoid double counting
        day_intercity_cost = 0.0
        found_first = False
        for act in day.get("activities", []) or []:
            if act.get("type") == "travel_intercity_public" and not found_first:
                details = act.get("details") or {}
                cost = details.get("cost", 0)
                try:
                    day_intercity_cost = float(cost)
                    found_first = True
                except:
                    pass
        
        # Multiply by people number
        if day_intercity_cost > 0:
            transportation_cost += day_intercity_cost * people_number
    
    # 2. Calculate accommodation costs
    for day_idx, day in enumerate(daily_plans[:-1]):  # Except last day
        accom = day.get("accommodation")
        if isinstance(accom, dict):
            price = accom.get("price") or accom.get("price_per_night") or accom.get("cost")
            if price:
                try:
                    accommodation_cost += float(price) * room_number
                except:
                    pass
    
    # 3. Calculate meals costs
    for day in daily_plans:
        for act in day.get("activities", []) or []:
            if act.get("type") == "meal":
                details = act.get("details") or {}
                cost = details.get("cost")
                if cost:
                    try:
                        meals_cost += float(cost) * people_number
                    except:
                        pass
    
    # 4. Calculate attraction costs
    for day in daily_plans:
        for act in day.get("activities", []) or []:
            if act.get("type") == "attraction":
                details = act.get("details") or {}
                cost = details.get("cost")
                if cost:
                    try:
                        attractions_cost += float(cost) * people_number
                    except:
                        pass
    
    # 5. Calculate city transportation costs (taxis)
    taxis_needed = max(1, (people_number + 3) // 4)
    for day in daily_plans:
        for act in day.get("activities", []) or []:
            if act.get("type") == "travel_city":
                details = act.get("details") or {}
                cost = details.get("cost")
                if cost:
                    try:
                        transportation_cost += float(cost) * taxis_needed
                    except:
                        pass
    
    # Calculate total actual budget
    calculated_total = transportation_cost + accommodation_cost + meals_cost + attractions_cost
    
    # Check if budget is within limit
    if calculated_total <= max_budget:
        return (True, None)
    else:
        breakdown = (
            f"Actual budget exceeds limit: {calculated_total:.2f} > {max_budget:.2f} "
            f"(exceeded by {calculated_total - max_budget:.2f}). "
            f"Breakdown: Transportation={transportation_cost:.2f}, "
            f"Accommodation={accommodation_cost:.2f}, "
            f"Meals={meals_cost:.2f}, "
            f"Attractions={attractions_cost:.2f}"
        )
        return (False, breakdown)
