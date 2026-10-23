"""Toolkit for the OTA domain."""

from typing import List, Optional, Union

from vita.domains.ota.data_model import (
    OTADB,
    Hotel, Attraction, Flight, Train, HotelProduct, AttractionProduct, FlightProduct,
    TrainProduct,
    OTAOrderStatus
)
from vita.data_model.tasks import Order
from vita.environment.toolkit import ToolKitBase, ToolType, is_tool
from vita.utils.utils import check_date_format, rerank, fuzzy_match


class OTATools(ToolKitBase):
    """All the tools for the OTA domain."""

    db: OTADB

    def __init__(self, db: OTADB) -> None:
        super().__init__(db)

    def _check_user(self, user_id: str) -> bool:
        """Check if the user is valid.
        Args:
            user_id: The user id
        Returns:
            bool: True if the user is valid, False otherwise
        """
        if user_id != self.db.user_id:
            return False
        return True

    def _get_hotel_tags(self, hotel_id: str) -> str:
        """Get the hotel tags for a specific hotel.
        Args:
            hotel_id: The hotel id
            
        Returns:
            str: hotel_name + ',' + tags
        """
        hotel = self.db.hotels[hotel_id]
        return hotel.hotel_name + ','.join(hotel.tags)

    def _get_attraction_tags(self, attraction_id: str) -> str:
        """Get the attraction tags for a specific attraction.
        Args:
            attraction_id: The attraction id
            
        Returns:
            str: attraction_name + ',' + description + ',' + location
        """
        attraction = self.db.attractions[attraction_id]
        return f"{attraction.attraction_name},{attraction.description},{attraction.location.address}"


    def _add_ota_order(self, order: Order) -> str:
        """Add order to both shared database and domain-specific database.
        
        Args:
            order: The order to add
            
        Returns:
            "done" if successful, error message otherwise
        """
        if order.order_id in self.db.orders:
            return "Order already exists"

        self.db.orders[order.order_id] = order

        return "done"

    def _modify_ota_order(self, order: Order) -> str:
        """Modify order in both shared database and domain-specific database.
        
        Args:
            order: The order to modify
            
        Returns:
            "done" if successful, error message otherwise
        """
        if order.order_id not in self.db.orders:
            return "Order not found"

        self.db.orders[order.order_id] = order

        return "done"

    def _get_ota_order(self, order_id: Optional[str] = None, scene: Optional[str] = None) -> Union[Order, List[Order]]:
        """Get the order from the database.

        Args:
            order_id: The order id
            scene: The scene of the order
        Returns:
            The order.

        Raises:
            ValueError: If the order is not found.
        """
        if scene:
            return [order for order in self.db.orders.values() if order.order_type == scene]
        elif order_id:
            if order_id not in self.db.orders:
                raise ValueError(f"Order {order_id} not found")
            return self.db.orders[order_id]
        else:
            return [order for order in self.db.orders.values() if order.order_type in ["hotel", "attraction", "flight", "train"]]

    def _get_hotel(self, hotel_id: Optional[str] = None) -> Union[Hotel, List[Hotel]]:
        """Get the hotel from the database.
        Args:
            hotel_id: The hotel id, such as '6086499569'.

        Returns:
            The hotel.
        """
        if hotel_id is None:
            return list(self.db.hotels.values())
        if hotel_id not in self.db.hotels:
            raise ValueError(f"hotel {hotel_id} not found")
        return self.db.hotels[hotel_id]

    def _get_attraction(self, attraction_id: Optional[str] = None) -> Union[Attraction, List[Attraction]]:
        """Get the attraction from the database.
        Args:
            attraction_id: The attraction id.

        Returns:
            The attraction.
        """
        if attraction_id is None:
            return list(self.db.attractions.values())
        if attraction_id not in self.db.attractions:
            raise ValueError(f"attraction {attraction_id} not found")
        return self.db.attractions[attraction_id]

    def _get_flight(self, flight_id: Optional[str] = None) -> Union[Flight, List[Flight]]:
        """Get the flight from the database.
        Args:
            flight_id: The flight id.

        Returns:
            The flight.
        """
        if flight_id is None:
            return list(self.db.flights.values())
        if flight_id not in self.db.flights:
            raise ValueError(f"flight {flight_id} not found")
        return self.db.flights[flight_id]

    def _get_train(self, train_id: Optional[str] = None) -> Union[Train, List[Train]]:
        """Get the train from the database.
        Args:
            train_id: The train id.

        Returns:
            The train.
        """
        if train_id is None:
            return list(self.db.trains.values())
        if train_id not in self.db.trains:
            raise ValueError(f"train {train_id} not found")
        return self.db.trains[train_id]

    @is_tool(ToolType.READ)
    def get_ota_hotel_info(self, hotel_id: str) -> str:

        assert hotel_id, "Hotel ID cannot be empty"

        try:
            hotel = self._get_hotel(hotel_id)
            return f"Hotel Info:\n{repr(hotel)}"
        except ValueError as e:
            return f"Error: {e}"

    @is_tool(ToolType.READ)
    def get_ota_attraction_info(self, attraction_id: str) -> str:

        assert attraction_id, "Attraction ID cannot be empty"

        try:
            attraction = self._get_attraction(attraction_id)
            return f"Attraction Info:\n{repr(attraction)}"
        except ValueError as e:
            return f"Error: {e}"

    @is_tool(ToolType.READ)
    def get_ota_flight_info(self, flight_id: str) -> str:

        assert flight_id, "Flight ID cannot be empty"

        try:
            flight = self._get_flight(flight_id)
            return f"Flight Info:\n{repr(flight)}"
        except ValueError as e:
            return f"Error: {e}"

    @is_tool(ToolType.READ)
    def get_ota_train_info(self, train_id: str) -> str:

        assert train_id, "Train ID cannot be empty"

        try:
            train = self._get_train(train_id)
            return f"Train Info:\n{repr(train)}"
        except ValueError as e:
            return f"Error: {e}"

    @is_tool(tool_type=ToolType.READ)
    def hotel_search_recommend(self,
                               city_name: str,
                               key_words: Optional[List[str]] = None) -> str:
        assert city_name, "City name cannot be empty"
        assert isinstance(city_name, str), "City name must be a string"
        
        if key_words is not None:
            assert isinstance(key_words, list), "Key words must be a list"
            assert all(isinstance(kw, str) and kw.strip() for kw in key_words), "All key words must be non-empty strings"

        try:
            target_hotels = []
            for hotel in self._get_hotel():
                if not fuzzy_match(city_name, hotel.location.address):
                    continue
                target_hotels.append(hotel)

            top_k = 50
            if not target_hotels:
                return "No hotels found matching the criteria."
            
            hotel_tag_dict = {}
            for hotel in target_hotels:
                hotel_tag_dict[hotel.hotel_id] = self._get_hotel_tags(hotel.hotel_id)
            
            keywords_str = "".join(key_words or [])
            assert keywords_str and keywords_str.strip(), "Keywords cannot be empty"
            id_candidates_sorted = rerank(keywords_str, hotel_tag_dict)
            selected_ids = [ic[0] for ic in id_candidates_sorted[:top_k]]
            
            if not selected_ids:
                return "No hotels found matching the keywords"
            
            selected_hotels = [str(self._get_hotel(hotel_id)) for hotel_id in selected_ids]
            selected_hotels_repr = "\n".join(selected_hotels)
            return selected_hotels_repr
        except Exception as e:
            return f"Error searching hotels: {e}"

    @is_tool(tool_type=ToolType.READ)
    def attractions_search_recommend(self, city_name: str, key_words: List[str]) -> str:
        assert city_name, "City name cannot be empty"
        assert isinstance(city_name, str), "City name must be a string"
        assert key_words, "Key words cannot be empty"
        assert isinstance(key_words, list), "Key words must be a list"
        assert all(isinstance(kw, str) and kw.strip() for kw in key_words), "All key words must be non-empty strings"

        try:
            target_attractions = []
            for attraction in self._get_attraction():
                if not fuzzy_match(city_name, attraction.location.address):
                    continue
                target_attractions.append(attraction)
            
            top_k = 50
            if not target_attractions:
                return "No attractions found matching the criteria."
            
            attraction_tag_dict = {}
            for attraction in target_attractions:
                attraction_tag_dict[attraction.attraction_id] = self._get_attraction_tags(attraction.attraction_id)
            
            keywords_str = "".join(key_words)
            assert keywords_str and keywords_str.strip(), "Keywords cannot be empty"
            id_candidates_sorted = rerank(keywords_str, attraction_tag_dict)
            selected_ids = [ic[0] for ic in id_candidates_sorted[:top_k]]
            
            if not selected_ids:
                return "No attractions found matching the keywords"
            
            selected_attractions = [str(self._get_attraction(attraction_id)) for attraction_id in selected_ids]
            selected_attractions_repr = "\n".join(selected_attractions)
            return selected_attractions_repr
        except Exception as e:
            return f"Error searching attractions: {e}"

    @is_tool(tool_type=ToolType.READ)
    def flight_search_recommend(self, departure: str, destination: str) -> str:
        assert departure, "Departure city cannot be empty"
        assert destination, "Destination city cannot be empty"
        assert isinstance(departure, str), "Departure city must be a string"
        assert isinstance(destination, str), "Destination city must be a string"
        
        try:
            target_flights = []
            for flight in self._get_flight():
                if not fuzzy_match(departure, flight.departure_city):
                    continue
                if not fuzzy_match(destination, flight.arrival_city):
                    continue
                target_flights.append(flight)
            
            if not target_flights:
                return "No flights found matching the criteria. Please check if the departure and destination cities are correct."
            
            flights_repr = "\n".join([str(flight) for flight in target_flights])
            return flights_repr
        except Exception as e:
            return f"Error searching flights: {e}"

    @is_tool(tool_type=ToolType.READ)
    def train_ticket_search(self, departure: str, destination: str, date: str) -> str:

        assert departure, "Departure city cannot be empty"
        assert destination, "Destination city cannot be empty"
        assert date, "Departure date cannot be empty"
        assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"

        target_trains = []
        for train in self._get_train():
            # Check if train's departure date is date, where date is in train's products class (TrainProduct), check fields and note implementation logic
            for product in train.products:
                if product.date == date:
                    if not fuzzy_match(departure, train.departure_city):
                        continue
                    if not fuzzy_match(destination, train.arrival_city):
                        continue
                    target_trains.append(train)
            
        if not target_trains:
            return "No trains found matching the criteria"
        
        trains_repr = "\n".join([str(train) for train in target_trains])
        return trains_repr

    @is_tool(tool_type=ToolType.WRITE)
    def create_hotel_order(self, hotel_id: str, room_id: str, user_id: str) -> str:
        assert hotel_id, "Hotel ID cannot be empty"
        assert room_id, "Room ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        try:
            hotel = self._get_hotel(hotel_id)
        except ValueError as e:
            return f"Error: {e}"

        ordered_rooms = []
        room_found = False
        for product in hotel.products:
            if product.product_id == room_id:
                room_found = True
                if product.quantity <= 0:
                    return f"No available rooms at the moment for room {room_id}"
                product.quantity = product.quantity - 1
                ordered_room = HotelProduct(
                    product_id=product.product_id,
                    price=product.price,
                    date=product.date,
                    quantity=1,
                    room_type=product.room_type
                )
                ordered_rooms.append(ordered_room)
                break
        
        if not room_found:
            return f"Room {room_id} not found in hotel {hotel_id}"

        order = Order(
            order_id=self.db.assign_order_id("hotel", user_id, hotel_id=hotel_id, product_id=room_id),
            order_type="hotel",
            user_id=user_id,
            store_id=hotel_id,
            total_price=sum([room.price for room in ordered_rooms]),
            update_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            create_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            status="unpaid",
            products=ordered_rooms
        )

        response = self._add_ota_order(order)
        if response == "done":
            return repr(order)
        else:
            return f"Failed to create order: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def create_attraction_order(self, attraction_id: str, ticket_id: str, user_id: str, date: str, quantity: int) -> str:
        assert attraction_id, "Attraction ID cannot be empty"
        assert ticket_id, "Ticket ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert date, "Date cannot be empty"
        assert isinstance(quantity, int), "Quantity must be an integer"
        assert quantity > 0, "Booking quantity must be greater than 0"
        assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"
        assert self._check_user(user_id), "User ID does not match"

        try:
            attraction = self._get_attraction(attraction_id)
        except ValueError as e:
            return f"Error: {e}"

        target_product = None
        for product in attraction.products:
            if product.date == date and product.product_id == ticket_id:
                target_product = product
                break
        
        if target_product is None:
            return f"The attraction {attraction_id} does not have ticket {ticket_id} on date {date}"
        
        if target_product.quantity < quantity:
            return f"Insufficient ticket inventory for the specified date {date}. Available: {target_product.quantity}, Requested: {quantity}"

        ordered_tickets = []
        target_product.quantity = target_product.quantity - quantity
        ordered_ticket = AttractionProduct(
            product_id=target_product.product_id,
            price=target_product.price,
            date=date,
            quantity=quantity,
            ticket_type=target_product.ticket_type
        )
        ordered_tickets.append(ordered_ticket)

        order = Order(
            order_id=self.db.assign_order_id("attraction", user_id),
            order_type="attraction",
            user_id=user_id,
            store_id=attraction_id,
            total_price=sum([ticket.price * ticket.quantity for ticket in ordered_tickets]),
            update_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            create_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            status="unpaid",
            products=ordered_tickets
        )

        response = self._add_ota_order(order)
        if response == "done":
            return repr(order)
        else:
            return f"Failed to create order: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def create_flight_order(self, flight_id: str, seat_id: str, user_id: str, date: str, quantity: int) -> str:
        assert flight_id, "Flight ID cannot be empty"
        assert seat_id, "Seat ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert date, "Date cannot be empty"
        assert isinstance(quantity, int), "Quantity must be an integer"
        assert quantity > 0, "Booking quantity must be greater than 0"
        assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"
        assert self._check_user(user_id), "User ID does not match"

        try:
            flight = self._get_flight(flight_id)
        except ValueError as e:
            return f"Error: {e}"

        target_product = None
        for product in flight.products:
            if product.date == date and product.product_id == seat_id:
                target_product = product
                break
        
        if target_product is None:
            return f"The flight {flight_id} does not have seat {seat_id} on date {date}"
        
        if target_product.quantity < quantity:
            return f"Insufficient seat inventory for the specified date {date}. Available: {target_product.quantity}, Requested: {quantity}"

        ordered_seats = []
        target_product.quantity = target_product.quantity - quantity
        ordered_seat = FlightProduct(
            product_id=target_product.product_id,
            price=target_product.price,
            date=date,
            quantity=quantity,
            seat_type=target_product.seat_type,
        )
        ordered_seats.append(ordered_seat)

        order = Order(
            order_id=self.db.assign_order_id("flight", user_id),
            order_type="flight",
            user_id=user_id,
            store_id=flight_id,
            total_price=sum([seat.price * seat.quantity for seat in ordered_seats]),
            update_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            create_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            status="unpaid",
            products=ordered_seats
        )

        response = self._add_ota_order(order)
        if response == "done":
            return repr(order)
        else:
            return f"Failed to create order: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def create_train_order(self, train_id: str, seat_id: str, user_id: str, date: str, quantity: int) -> str:
        assert train_id, "Train ID cannot be empty"
        assert seat_id, "Seat ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert date, "Date cannot be empty"
        assert isinstance(quantity, int), "Quantity must be an integer"
        assert quantity > 0, "Booking quantity must be greater than 0"
        assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"
        assert self._check_user(user_id), "User ID does not match"

        try:
            train = self._get_train(train_id)
        except ValueError as e:
            return f"Error: {e}"

        target_product = None
        for product in train.products:
            if product.date == date and product.product_id == seat_id:
                target_product = product
                break
        
        if target_product is None:
            return f"The train {train_id} does not have seat {seat_id} on date {date}"
        
        if target_product.quantity < quantity:
            return f"Insufficient seat inventory for the specified date {date}. Available: {target_product.quantity}, Requested: {quantity}"

        ordered_seats = []
        target_product.quantity = target_product.quantity - quantity
        ordered_seat = TrainProduct(
            product_id=target_product.product_id,
            price=target_product.price,
            date=date,
            quantity=quantity,
            seat_type=target_product.seat_type
        )
        ordered_seats.append(ordered_seat)

        order = Order(
            order_id=self.db.assign_order_id("train", user_id),
            order_type="train",
            user_id=user_id,
            store_id=train_id,
            total_price=sum([seat.price * seat.quantity for seat in ordered_seats]),
            update_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            create_time=self.get_now("%Y-%m-%d %H:%M:%S"),
            status="unpaid",
            products=ordered_seats
        )

        response = self._add_ota_order(order)
        if response == "done":
            return repr(order)
        else:
            return f"Failed to create order: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def pay_hotel_order(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "hotel":
            return f"Order {order_id} is not a hotel order"
        
        if order.status != "unpaid":
            return f"Order status must be unpaid. Current status: {order.status}"

        order.status = "paid"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return "Payment successful"
        else:
            return f"Payment failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def pay_attraction_order(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "attraction":
            return f"Order {order_id} is not an attraction order"
        
        if order.status != "unpaid":
            return f"Order status must be unpaid. Current status: {order.status}"

        order.status = "paid"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return "Payment successful"
        else:
            return f"Payment failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def pay_flight_order(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "flight":
            return f"Order {order_id} is not a flight order"
        
        if order.status != "unpaid":
            return f"Order status must be unpaid. Current status: {order.status}"

        order.status = "paid"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return "Payment successful"
        else:
            return f"Payment failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def pay_train_order(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "train":
            return f"Order {order_id} is not a train order"
        
        if order.status != "unpaid":
            return f"Order status must be unpaid. Current status: {order.status}"

        order.status = "paid"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return "Payment successful"
        else:
            return f"Payment failed: {response}"

    @is_tool(tool_type=ToolType.READ)
    def search_hotel_order(self, user_id: str, date: Optional[str] = None, status: Optional[OTAOrderStatus] = "paid") -> str:
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"
        
        if date:
            assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"

        try:
            hotel_orders = []
            for order in self._get_ota_order(scene="hotel"):
                order_selected = None
                if order.user_id == user_id:
                    order_selected = order
                if status and order.status != status:
                    order_selected = None
                if date and order_selected is not None:
                    if not hasattr(order_selected, 'products'):
                        order_selected = None
                    else:
                        has_date_product = False
                        for product in order_selected.products:
                            if hasattr(product, 'date') and product.date == date:
                                has_date_product = True
                                break
                        if not has_date_product:
                            order_selected = None
                if order_selected:
                    hotel_orders.append(order_selected)
            
            if not hotel_orders:
                date_filter = f" on date {date}" if date else ""
                status_filter = f" with status {status}" if status else ""
                return f"No hotel orders found for user {user_id}{date_filter}{status_filter}"
            
            orders_repr = "\n".join([str(order) for order in hotel_orders])
            return orders_repr
        except Exception as e:
            return f"Error searching hotel orders: {e}"

    @is_tool(tool_type=ToolType.READ)
    def search_attraction_order(self, user_id: str, date: Optional[str] = None,
                                status: Optional[OTAOrderStatus] = "paid") -> str:
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        if date:
            assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"

        try:
            attraction_orders = []
            for order in self._get_ota_order(scene="attraction"):
                order_selected = None
                if order.user_id == user_id:
                    order_selected = order
                if status and order.status != status:
                    order_selected = None
                if date and order_selected is not None:
                    if not hasattr(order_selected, 'products'):
                        order_selected = None
                    else:
                        has_date_product = False
                        for product in order_selected.products:
                            if hasattr(product, 'date') and product.date == date:
                                has_date_product = True
                                break
                        if not has_date_product:
                            order_selected = None
                if order_selected:
                    attraction_orders.append(order_selected)
            
            if not attraction_orders:
                date_filter = f" on date {date}" if date else ""
                status_filter = f" with status {status}" if status else ""
                return f"No attraction orders found for user {user_id}{date_filter}{status_filter}"
            
            orders_repr = "\n".join([str(order) for order in attraction_orders])
            return orders_repr
        except Exception as e:
            return f"Error searching attraction orders: {e}"

    @is_tool(tool_type=ToolType.READ)
    def search_flight_order(self, user_id: str, date: Optional[str] = None,
                            status: Optional[OTAOrderStatus] = "paid") -> str:
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        if date:
            assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"

        try:
            flight_orders = []
            for order in self._get_ota_order(scene="flight"):
                order_selected = None
                if order.user_id == user_id:
                    order_selected = order
                if status and order.status != status:
                    order_selected = None
                if date and order_selected is not None:
                    if not hasattr(order_selected, 'products'):
                        order_selected = None
                    else:
                        has_date_product = False
                        for product in order_selected.products:
                            if hasattr(product, 'date') and product.date == date:
                                has_date_product = True
                                break
                        if not has_date_product:
                            order_selected = None
                if order_selected:
                    flight_orders.append(order_selected)
            
            if not flight_orders:
                date_filter = f" on date {date}" if date else ""
                status_filter = f" with status {status}" if status else ""
                return f"No flight orders found for user {user_id}{date_filter}{status_filter}"
            
            orders_repr = "\n".join([str(order) for order in flight_orders])
            return orders_repr
        except Exception as e:
            return f"Error searching flight orders: {e}"


    @is_tool(tool_type=ToolType.READ)
    def search_train_order(self, user_id: str, date: Optional[str] = None,
                           status: Optional[OTAOrderStatus] = "paid") -> str:
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        if date:
            assert check_date_format(date), "Date format is incorrect, correct format is %Y-%m-%d"

        try:
            train_orders = []
            for order in self._get_ota_order(scene="train"):
                order_selected = None
                if order.user_id == user_id:
                    order_selected = order
                if status and order.status != status:
                    order_selected = None
                if date and order_selected is not None:
                    if not hasattr(order_selected, 'products'):
                        order_selected = None
                    else:
                        has_date_product = False    
                        for product in order_selected.products:
                            if hasattr(product, 'date') and product.date == date:
                                has_date_product = True
                                break
                        if not has_date_product:
                            order_selected = None
                if order_selected:
                    train_orders.append(order_selected)
            
            if not train_orders:
                date_filter = f" on date {date}" if date else ""
                status_filter = f" with status {status}" if status else ""
                return f"No train orders found for user {user_id}{date_filter}{status_filter}"
            
            orders_repr = "\n".join([str(order) for order in train_orders])
            return orders_repr
        except Exception as e:
            return f"Error searching train orders: {e}"

    @is_tool(tool_type=ToolType.READ)
    def get_hotel_order_detail(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "hotel":
            return f"Order {order_id} is not a hotel order"
        
        return repr(order)

    @is_tool(tool_type=ToolType.READ)
    def get_attraction_order_detail(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "attraction":
            return f"Order {order_id} is not an attraction order"
        
        return repr(order)

    @is_tool(tool_type=ToolType.READ)
    def get_flight_order_detail(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "flight":
            return f"Order {order_id} is not a flight order"
        
        return repr(order)

    @is_tool(tool_type=ToolType.READ)
    def get_train_order_detail(self, order_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        
        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "train":
            return f"Order {order_id} is not a train order"
        
        return repr(order)

    @is_tool(tool_type=ToolType.WRITE)
    def modify_train_order(self, order_id: str, user_id: str, new_date: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert new_date, "New departure date cannot be empty"
        assert self._check_user(user_id), "User ID does not match"
        assert check_date_format(new_date), "Date format is incorrect, correct format is %Y-%m-%d"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"

        if order.order_type != "train":
            return f"Order {order_id} is not a train order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status != "paid":
            return f"Only paid orders can be modified. Current status: {order.status}"

        if len(order.products) != 1:
            return "Only single train ticket order modification is supported"

        old_product = order.products[0]
        train_id = order.store_id
        
        try:
            train = self._get_train(train_id)
        except ValueError as e:
            return f"Error: {e}"
        
        seat_type = old_product.get("seat_type") if isinstance(old_product, dict) else old_product.seat_type
        quantity = old_product.get("quantity") if isinstance(old_product, dict) else old_product.quantity

        new_product = None
        for product in train.products:
            if product.date == new_date and product.seat_type == seat_type:
                new_product = product
                break
        
        if new_product is None:
            return f"New date {new_date} does not have {seat_type} type seats"
        
        if new_product.quantity < quantity:
            return f"Insufficient {seat_type} seat inventory for new date {new_date}. Available: {new_product.quantity}, Required: {quantity}"

        for product in train.products:
            old_date = old_product.get("date") if isinstance(old_product, dict) else old_product.date
            if product.date == old_date and product.seat_type == seat_type:
                product.quantity += quantity
                break

        new_product.quantity -= quantity

        old_price = old_product.get("price") if isinstance(old_product, dict) else old_product.price
        old_total = old_price * quantity
        new_total = new_product.price * quantity
        diff = new_total - old_total

        if diff > 0:
            order.status = "unpaid"

        order.products = [TrainProduct(
            product_id=new_product.product_id,
            price=new_product.price,
            date=new_date,
            seat_type=seat_type,
            quantity=quantity
        )]
        order.total_price = new_total
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            if diff > 0:
                return f"Modification successful, need to pay additional amount: {diff}."
            else:
                return f"Modification successful, price difference: {diff}, refunded."
        else:
            return f"Modification failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def modify_flight_order(self, order_id: str, user_id: str, new_date: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert new_date, "New departure date cannot be empty"
        assert check_date_format(new_date), "Date format is incorrect, correct format is %Y-%m-%d"
        assert self._check_user(user_id), "User ID does not match"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"

        if order.order_type != "flight":
            return f"Order {order_id} is not a flight order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status != "paid":
            return f"Only paid orders can be modified. Current status: {order.status}"

        if len(order.products) != 1:
            return "Only single flight ticket order modification is supported"

        old_product = order.products[0]
        flight_id = order.store_id
        
        try:
            flight = self._get_flight(flight_id)
        except ValueError as e:
            return f"Error: {e}"
        
        seat_type = old_product.get("seat_type") if isinstance(old_product, dict) else old_product.seat_type
        quantity = old_product.get("quantity") if isinstance(old_product, dict) else old_product.quantity

        new_product = None
        for product in flight.products:
            if product.date == new_date and product.seat_type == seat_type:
                new_product = product
                break
        
        if new_product is None:
            return f"New date {new_date} does not have {seat_type} type seats"
        
        if new_product.quantity < quantity:
            return f"Insufficient {seat_type} seat inventory for new date {new_date}. Available: {new_product.quantity}, Required: {quantity}"

        for product in flight.products:
            old_date = old_product.get("date") if isinstance(old_product, dict) else old_product.date
            if product.date == old_date and product.seat_type == seat_type:
                product.quantity += quantity
                break

        new_product.quantity -= quantity

        old_price = old_product.get("price") if isinstance(old_product, dict) else old_product.price
        old_total = old_price * quantity
        new_total = new_product.price * quantity
        diff = new_total - old_total

        if diff > 0:
            order.status = "unpaid"

        order.products = [FlightProduct(
            product_id=new_product.product_id,
            price=new_product.price,
            date=new_date,
            seat_type=seat_type,
            quantity=quantity
        )]
        order.total_price = new_total
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            if diff > 0:
                return f"Modification successful, need to pay additional amount: {diff}, please pay as soon as possible"
            else:
                return f"Modification successful, price difference: {diff}, refunded"
        else:
            return f"Modification failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def cancel_hotel_order(self, order_id: str, user_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "hotel":
            return f"Order {order_id} is not a hotel order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status in ["cancelled"]:
            return f"Order {order_id} is already cancelled"
        
        refund = 0
        if order.status == "paid":
            refund = order.total_price
        
        order.status = "cancelled"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return f"Cancellation successful, refund amount: {refund}"
        else:
            return f"Cancellation failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def cancel_attraction_order(self, order_id: str, user_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "attraction":
            return f"Order {order_id} is not an attraction order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status in ["cancelled"]:
            return f"Order {order_id} is already cancelled"
        
        refund = 0
        if order.status == "paid":
            refund = order.total_price
        
        order.status = "cancelled"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return f"Cancellation successful, refund amount: {refund}"
        else:
            return f"Cancellation failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def cancel_flight_order(self, order_id: str, user_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "flight":
            return f"Order {order_id} is not a flight order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status in ["cancelled"]:
            return f"Order {order_id} is already cancelled"
        
        refund = 0
        if order.status == "paid":
            refund = order.total_price
        
        order.status = "cancelled"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return f"Cancellation successful, refund amount: {refund}"
        else:
            return f"Cancellation failed: {response}"

    @is_tool(tool_type=ToolType.WRITE)
    def cancel_train_order(self, order_id: str, user_id: str) -> str:
        assert order_id, "Order ID cannot be empty"
        assert user_id, "User ID cannot be empty"
        assert self._check_user(user_id), "User ID does not match"

        try:
            order = self._get_ota_order(order_id=order_id)
        except ValueError as e:
            return f"Error: {e}"
        
        if order.order_type != "train":
            return f"Order {order_id} is not a train order"
        
        if order.user_id != user_id:
            return f"Order {order_id} does not belong to user {user_id}"
        
        if order.status in ["cancelled"]:
            return f"Order {order_id} is already cancelled"
        
        refund = 0
        if order.status == "paid":
            refund = order.total_price
        
        order.status = "cancelled"
        order.update_time = self.get_now("%Y-%m-%d %H:%M:%S")
        response = self._modify_ota_order(order)
        if response == "done":
            return f"Cancellation successful, refund amount: {refund}"
        else:
            return f"Cancellation failed: {response}"
