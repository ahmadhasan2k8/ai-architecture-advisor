"""Observer pattern implementations.

This module provides implementations of the Observer pattern, demonstrating
how to establish one-to-many dependency relationships between objects.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set


class Observer(ABC):
    """Abstract base class for observers.

    Objects that want to be notified when a subject changes should implement
    this interface.
    """

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Called when the subject notifies observers of a change.

        Args:
            *args: Variable positional arguments from the subject
            **kwargs: Variable keyword arguments from the subject
        """
        pass


class Subject(ABC):
    """Abstract base class for subjects (observables).

    Objects that want to be observed should implement this interface.
    """

    @abstractmethod
    def register_observer(self, observer: Observer) -> None:
        """Register an observer to be notified of changes.

        Args:
            observer: The observer to register
        """
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the notification list.

        Args:
            observer: The observer to remove
        """
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        """Notify all registered observers of a change."""
        pass


class ConcreteSubject(Subject):
    """Concrete implementation of the Subject interface.

    This class manages a list of observers and provides methods to add,
    remove, and notify them.
    """

    def __init__(self):
        """Initialize the subject with an empty observer list."""
        self._observers: Set[Observer] = set()
        self._state: Any = None

    def register_observer(self, observer: Observer) -> None:
        """Register an observer to be notified of changes.

        Args:
            observer: The observer to register
        """
        self._observers.add(observer)

    def remove_observer(self, observer: Observer) -> None:
        """Remove an observer from the notification list.

        Args:
            observer: The observer to remove
        """
        self._observers.discard(observer)

    def notify_observers(self) -> None:
        """Notify all registered observers of a change."""
        # Create a copy to avoid issues if observers modify the set during iteration
        for observer in list(self._observers):
            observer.update(self._state)

    def set_state(self, state: Any) -> None:
        """Set the subject's state and notify observers.

        Args:
            state: The new state
        """
        self._state = state
        self.notify_observers()

    def get_state(self) -> Any:
        """Get the current state of the subject.

        Returns:
            The current state
        """
        return self._state


class ConcreteObserver(Observer):
    """Concrete implementation of the Observer interface.

    This class demonstrates how to implement an observer that reacts
    to changes in a subject.
    """

    def __init__(self, name: str):
        """Initialize the observer with a name.

        Args:
            name: The name of the observer
        """
        self.name = name
        self._state: Any = None

    def update(self, state: Any) -> None:
        """Update the observer's state when notified by the subject.

        Args:
            state: The new state from the subject
        """
        self._state = state
        print(f"Observer {self.name} received state update: {state}")


# Weather Station Example (Push Model)


class WeatherObserver(Observer):
    """Abstract base class for weather observers."""

    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update the observer with weather data.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Atmospheric pressure in hPa
        """
        pass


class WeatherStation(Subject):
    """Weather station that notifies observers of weather changes."""

    def __init__(self):
        """Initialize the weather station."""
        self._observers: Set[WeatherObserver] = set()
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0

    def register_observer(self, observer: WeatherObserver) -> None:
        """Register a weather observer.

        Args:
            observer: The weather observer to register
        """
        self._observers.add(observer)

    def remove_observer(self, observer: WeatherObserver) -> None:
        """Remove a weather observer.

        Args:
            observer: The weather observer to remove
        """
        self._observers.discard(observer)

    def notify_observers(self) -> None:
        """Notify all observers of weather changes."""
        for observer in list(self._observers):
            observer.update(self._temperature, self._humidity, self._pressure)

    def set_measurements(
        self, temperature: float, humidity: float, pressure: float
    ) -> None:
        """Set new weather measurements and notify observers.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Atmospheric pressure in hPa
        """
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify_observers()

    def get_temperature(self) -> float:
        """Get the current temperature.

        Returns:
            Current temperature in Celsius
        """
        return self._temperature

    def get_humidity(self) -> float:
        """Get the current humidity.

        Returns:
            Current humidity percentage
        """
        return self._humidity

    def get_pressure(self) -> float:
        """Get the current pressure.

        Returns:
            Current atmospheric pressure in hPa
        """
        return self._pressure


class CurrentConditionsDisplay(WeatherObserver):
    """Display showing current weather conditions."""

    def __init__(self):
        """Initialize the display."""
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0

    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update the display with current conditions.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Atmospheric pressure in hPa
        """
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        print(
            f"Current conditions: {temperature}°C, {humidity}% humidity, {pressure} hPa"
        )


class StatisticsDisplay(WeatherObserver):
    """Display showing weather statistics."""

    def __init__(self):
        """Initialize the statistics display."""
        self._temperatures: List[float] = []
        self._humidities: List[float] = []
        self._pressures: List[float] = []

    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update the statistics with new measurements.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Atmospheric pressure in hPa
        """
        self._temperatures.append(temperature)
        self._humidities.append(humidity)
        self._pressures.append(pressure)

        avg_temp = sum(self._temperatures) / len(self._temperatures)
        min_temp = min(self._temperatures)
        max_temp = max(self._temperatures)

        print(
            f"Statistics: Avg temp: {avg_temp:.1f}°C, Min: {min_temp}°C, Max: {max_temp}°C"
        )


class ForecastDisplay(WeatherObserver):
    """Display showing weather forecast."""

    def __init__(self):
        """Initialize the forecast display."""
        self._last_pressure: Optional[float] = None

    def update(self, temperature: float, humidity: float, pressure: float) -> None:
        """Update the forecast based on pressure changes.

        Args:
            temperature: Temperature in Celsius
            humidity: Humidity percentage
            pressure: Atmospheric pressure in hPa
        """
        if self._last_pressure is None:
            forecast = "More of the same"
        elif pressure > self._last_pressure:
            forecast = "Improving weather on the way!"
        elif pressure < self._last_pressure:
            forecast = "Watch out for cooler, rainy weather"
        else:
            forecast = "More of the same"

        print(f"Forecast: {forecast}")
        self._last_pressure = pressure


# Stock Market Example (Pull Model)


class StockObserver(Observer):
    """Abstract base class for stock observers."""

    @abstractmethod
    def update(self, stock: "Stock") -> None:
        """Update the observer with stock information.

        Args:
            stock: The stock subject that changed
        """
        pass


class Stock(Subject):
    """Stock that notifies observers of price changes."""

    def __init__(self, symbol: str, price: float):
        """Initialize the stock.

        Args:
            symbol: Stock symbol (e.g., "AAPL")
            price: Initial stock price
        """
        self._observers: Set[StockObserver] = set()
        self._symbol = symbol
        self._price = price

    def register_observer(self, observer: StockObserver) -> None:
        """Register a stock observer.

        Args:
            observer: The stock observer to register
        """
        self._observers.add(observer)

    def remove_observer(self, observer: StockObserver) -> None:
        """Remove a stock observer.

        Args:
            observer: The stock observer to remove
        """
        self._observers.discard(observer)

    def notify_observers(self) -> None:
        """Notify all observers of stock changes."""
        for observer in list(self._observers):
            observer.update(self)

    def set_price(self, price: float) -> None:
        """Set the stock price and notify observers.

        Args:
            price: New stock price
        """
        self._price = price
        self.notify_observers()

    def get_symbol(self) -> str:
        """Get the stock symbol.

        Returns:
            Stock symbol
        """
        return self._symbol

    def get_price(self) -> float:
        """Get the current stock price.

        Returns:
            Current stock price
        """
        return self._price


class StockDisplay(StockObserver):
    """Display showing stock information."""

    def __init__(self, name: str):
        """Initialize the stock display.

        Args:
            name: Name of the display
        """
        self.name = name

    def update(self, stock: Stock) -> None:
        """Update the display with stock information.

        Args:
            stock: The stock that changed
        """
        print(f"{self.name}: {stock.get_symbol()} is now ${stock.get_price():.2f}")


class TradingBot(StockObserver):
    """Automated trading bot that reacts to stock price changes."""

    def __init__(self, name: str, buy_threshold: float, sell_threshold: float):
        """Initialize the trading bot.

        Args:
            name: Name of the bot
            buy_threshold: Price below which to buy
            sell_threshold: Price above which to sell
        """
        self.name = name
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def update(self, stock: Stock) -> None:
        """React to stock price changes.

        Args:
            stock: The stock that changed
        """
        price = stock.get_price()
        symbol = stock.get_symbol()

        if price <= self.buy_threshold:
            print(f"{self.name}: BUY signal for {symbol} at ${price:.2f}")
        elif price >= self.sell_threshold:
            print(f"{self.name}: SELL signal for {symbol} at ${price:.2f}")
        else:
            print(f"{self.name}: HOLD {symbol} at ${price:.2f}")


# Event System Example


@dataclass
class Event:
    """Represents an event with type, data, and timestamp."""

    event_type: str
    data: Dict[str, Any]
    timestamp: datetime
    source: str


class EventManager:
    """Event manager that supports multiple event types and listeners."""

    def __init__(self):
        """Initialize the event manager."""
        self._listeners: Dict[str, List[Callable[[Event], None]]] = {}
        self._event_history: List[Event] = []

    def subscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Subscribe to events of a specific type.

        Args:
            event_type: Type of events to subscribe to
            callback: Function to call when event occurs
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable[[Event], None]) -> None:
        """Unsubscribe from events of a specific type.

        Args:
            event_type: Type of events to unsubscribe from
            callback: Function to remove from listeners
        """
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(callback)
            except ValueError:
                pass  # Callback not in list

    def emit(
        self, event_type: str, data: Dict[str, Any], source: str = "unknown"
    ) -> None:
        """Emit an event to all subscribed listeners.

        Args:
            event_type: Type of event to emit
            data: Event data
            source: Source of the event
        """
        event = Event(
            event_type=event_type, data=data, timestamp=datetime.now(), source=source
        )

        self._event_history.append(event)

        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event callback: {e}")

    def get_event_history(self, event_type: Optional[str] = None) -> List[Event]:
        """Get the history of events.

        Args:
            event_type: Optional filter by event type

        Returns:
            List of events, optionally filtered by type
        """
        if event_type:
            return [e for e in self._event_history if e.event_type == event_type]
        return self._event_history.copy()

    def clear_history(self) -> None:
        """Clear the event history."""
        self._event_history.clear()


# Example application using the event system


class UserService:
    """Service for managing users with event notifications."""

    def __init__(self, event_manager: EventManager):
        """Initialize the user service.

        Args:
            event_manager: Event manager to use for notifications
        """
        self.event_manager = event_manager
        self.users: Dict[int, Dict[str, Any]] = {}

    def register_user(self, user_id: int, name: str, email: str) -> None:
        """Register a new user and emit an event.

        Args:
            user_id: Unique user ID
            name: User's name
            email: User's email address
        """
        user_data = {"user_id": user_id, "name": name, "email": email}
        self.users[user_id] = user_data

        self.event_manager.emit("user_registered", user_data, "user_service")

    def update_user_email(self, user_id: int, new_email: str) -> None:
        """Update a user's email and emit an event.

        Args:
            user_id: User ID
            new_email: New email address
        """
        if user_id in self.users:
            old_email = self.users[user_id]["email"]
            self.users[user_id]["email"] = new_email

            self.event_manager.emit(
                "user_email_updated",
                {"user_id": user_id, "old_email": old_email, "new_email": new_email},
                "user_service",
            )


class EmailService:
    """Service for handling email-related events."""

    def __init__(self, event_manager: EventManager):
        """Initialize the email service.

        Args:
            event_manager: Event manager to subscribe to
        """
        self.event_manager = event_manager
        self._setup_listeners()

    def _setup_listeners(self) -> None:
        """Set up event listeners."""
        self.event_manager.subscribe("user_registered", self._send_welcome_email)
        self.event_manager.subscribe(
            "user_email_updated", self._send_email_confirmation
        )

    def _send_welcome_email(self, event: Event) -> None:
        """Send welcome email to new users.

        Args:
            event: User registration event
        """
        user_data = event.data
        print(
            f"📧 Sending welcome email to {user_data['name']} at {user_data['email']}"
        )

    def _send_email_confirmation(self, event: Event) -> None:
        """Send email confirmation when email is updated.

        Args:
            event: Email update event
        """
        data = event.data
        print(
            f"📧 Sending confirmation email to {data['new_email']} for user {data['user_id']}"
        )


class AuditService:
    """Service for auditing user actions."""

    def __init__(self, event_manager: EventManager):
        """Initialize the audit service.

        Args:
            event_manager: Event manager to subscribe to
        """
        self.event_manager = event_manager
        self.audit_log: List[str] = []
        self._setup_listeners()

    def _setup_listeners(self) -> None:
        """Set up event listeners."""
        self.event_manager.subscribe("user_registered", self._log_user_registration)
        self.event_manager.subscribe("user_email_updated", self._log_email_update)

    def _log_user_registration(self, event: Event) -> None:
        """Log user registration events.

        Args:
            event: User registration event
        """
        user_data = event.data
        log_entry = f"User {user_data['user_id']} ({user_data['name']}) registered at {event.timestamp}"
        self.audit_log.append(log_entry)
        print(f"📋 AUDIT: {log_entry}")

    def _log_email_update(self, event: Event) -> None:
        """Log email update events.

        Args:
            event: Email update event
        """
        data = event.data
        log_entry = f"User {data['user_id']} changed email from {data['old_email']} to {data['new_email']} at {event.timestamp}"
        self.audit_log.append(log_entry)
        print(f"📋 AUDIT: {log_entry}")


# Example usage functions


def demonstrate_basic_observer():
    """Demonstrate basic observer pattern."""
    print("=== Basic Observer Pattern Demo ===")

    # Create subject and observers
    subject = ConcreteSubject()
    observer1 = ConcreteObserver("Observer1")
    observer2 = ConcreteObserver("Observer2")

    # Register observers
    subject.register_observer(observer1)
    subject.register_observer(observer2)

    # Change state - both observers are notified
    subject.set_state("New State")

    # Remove an observer
    subject.remove_observer(observer1)

    # Change state again - only observer2 is notified
    subject.set_state("Another State")


def demonstrate_weather_station():
    """Demonstrate weather station observer pattern."""
    print("\n=== Weather Station Demo ===")

    # Create weather station and displays
    weather_station = WeatherStation()
    current_display = CurrentConditionsDisplay()
    stats_display = StatisticsDisplay()
    forecast_display = ForecastDisplay()

    # Register displays
    weather_station.register_observer(current_display)
    weather_station.register_observer(stats_display)
    weather_station.register_observer(forecast_display)

    # Update weather measurements
    weather_station.set_measurements(25.0, 65.0, 1013.2)
    print()
    weather_station.set_measurements(27.0, 70.0, 1015.1)
    print()
    weather_station.set_measurements(23.0, 60.0, 1010.5)


def demonstrate_stock_observer():
    """Demonstrate stock observer pattern."""
    print("\n=== Stock Observer Demo ===")

    # Create stock and observers
    apple_stock = Stock("AAPL", 150.00)
    display = StockDisplay("Portfolio Display")
    bot = TradingBot("AlgoBot", buy_threshold=140.00, sell_threshold=160.00)

    # Register observers
    apple_stock.register_observer(display)
    apple_stock.register_observer(bot)

    # Update stock price
    apple_stock.set_price(155.00)
    apple_stock.set_price(165.00)  # Trigger sell signal
    apple_stock.set_price(135.00)  # Trigger buy signal


def demonstrate_event_system():
    """Demonstrate event-driven system."""
    print("\n=== Event-Driven System Demo ===")

    # Create event manager and services
    event_manager = EventManager()
    user_service = UserService(event_manager)
    email_service = EmailService(event_manager)
    audit_service = AuditService(event_manager)

    # Perform user actions
    user_service.register_user(1, "Alice Johnson", "alice@example.com")
    print()
    user_service.update_user_email(1, "alice.johnson@example.com")

    # Show event history
    print(f"\n📊 Total events: {len(event_manager.get_event_history())}")
    for event in event_manager.get_event_history():
        print(f"  - {event.event_type} from {event.source}")


if __name__ == "__main__":
    demonstrate_basic_observer()
    demonstrate_weather_station()
    demonstrate_stock_observer()
    demonstrate_event_system()
