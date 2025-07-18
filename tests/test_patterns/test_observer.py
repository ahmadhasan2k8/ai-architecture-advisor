"""Tests for observer pattern implementations."""

import time
from datetime import datetime
from unittest.mock import Mock, call

import pytest

from src.patterns.observer import (  # Basic Observer Pattern; Weather Station Example; Stock Market Example; Event System
    AuditService,
    ConcreteObserver,
    ConcreteSubject,
    CurrentConditionsDisplay,
    EmailService,
    Event,
    EventManager,
    ForecastDisplay,
    Observer,
    StatisticsDisplay,
    Stock,
    StockDisplay,
    StockObserver,
    Subject,
    TradingBot,
    UserService,
    WeatherObserver,
    WeatherStation,
)


class TestBasicObserverPattern:
    """Test the basic Observer pattern implementation."""

    def test_concrete_observer_creation(self):
        """Test creating concrete observers."""
        observer = ConcreteObserver("TestObserver")
        assert observer.name == "TestObserver"
        assert observer._state is None

    def test_concrete_subject_creation(self):
        """Test creating concrete subjects."""
        subject = ConcreteSubject()
        assert len(subject._observers) == 0
        assert subject._state is None

    def test_observer_registration(self):
        """Test registering observers."""
        subject = ConcreteSubject()
        observer1 = ConcreteObserver("Observer1")
        observer2 = ConcreteObserver("Observer2")

        subject.register_observer(observer1)
        subject.register_observer(observer2)

        assert len(subject._observers) == 2
        assert observer1 in subject._observers
        assert observer2 in subject._observers

    def test_observer_deregistration(self):
        """Test removing observers."""
        subject = ConcreteSubject()
        observer1 = ConcreteObserver("Observer1")
        observer2 = ConcreteObserver("Observer2")

        subject.register_observer(observer1)
        subject.register_observer(observer2)

        subject.remove_observer(observer1)

        assert len(subject._observers) == 1
        assert observer1 not in subject._observers
        assert observer2 in subject._observers

    def test_removing_nonexistent_observer(self):
        """Test removing an observer that was never registered."""
        subject = ConcreteSubject()
        observer = ConcreteObserver("Observer")

        # Should not raise an exception
        subject.remove_observer(observer)
        assert len(subject._observers) == 0

    def test_duplicate_observer_registration(self):
        """Test registering the same observer multiple times."""
        subject = ConcreteSubject()
        observer = ConcreteObserver("Observer")

        subject.register_observer(observer)
        subject.register_observer(observer)  # Register again

        # Should only be registered once (using set)
        assert len(subject._observers) == 1
        assert observer in subject._observers

    def test_state_notification(self, capsys):
        """Test that observers are notified when state changes."""
        subject = ConcreteSubject()
        observer1 = ConcreteObserver("Observer1")
        observer2 = ConcreteObserver("Observer2")

        subject.register_observer(observer1)
        subject.register_observer(observer2)

        subject.set_state("new_state")

        # Check that observers received the update
        assert observer1._state == "new_state"
        assert observer2._state == "new_state"

        # Check console output
        captured = capsys.readouterr()
        assert "Observer Observer1 received state update: new_state" in captured.out
        assert "Observer Observer2 received state update: new_state" in captured.out

    def test_state_get_set(self):
        """Test getting and setting state."""
        subject = ConcreteSubject()

        assert subject.get_state() is None

        subject.set_state("test_state")
        assert subject.get_state() == "test_state"

    def test_notification_after_removal(self, capsys):
        """Test that removed observers don't receive notifications."""
        subject = ConcreteSubject()
        observer1 = ConcreteObserver("Observer1")
        observer2 = ConcreteObserver("Observer2")

        subject.register_observer(observer1)
        subject.register_observer(observer2)

        # Remove observer1
        subject.remove_observer(observer1)

        # Change state
        subject.set_state("test_state")

        # Only observer2 should receive the notification
        assert observer1._state is None
        assert observer2._state == "test_state"

        captured = capsys.readouterr()
        assert "Observer Observer1" not in captured.out
        assert "Observer Observer2 received state update: test_state" in captured.out


class TestWeatherStation:
    """Test the WeatherStation observer implementation."""

    def test_weather_station_creation(self):
        """Test creating a weather station."""
        station = WeatherStation()
        assert len(station._observers) == 0
        assert station._temperature == 0.0
        assert station._humidity == 0.0
        assert station._pressure == 0.0

    def test_weather_measurements(self):
        """Test getting weather measurements."""
        station = WeatherStation()

        station.set_measurements(25.5, 60.0, 1013.25)

        assert station.get_temperature() == 25.5
        assert station.get_humidity() == 60.0
        assert station.get_pressure() == 1013.25

    def test_current_conditions_display(self, capsys):
        """Test current conditions display."""
        station = WeatherStation()
        display = CurrentConditionsDisplay()

        station.register_observer(display)
        station.set_measurements(25.0, 65.0, 1013.2)

        captured = capsys.readouterr()
        assert "Current conditions: 25.0°C, 65.0% humidity, 1013.2 hPa" in captured.out

        # Check display state
        assert display._temperature == 25.0
        assert display._humidity == 65.0
        assert display._pressure == 1013.2

    def test_statistics_display(self, capsys):
        """Test statistics display."""
        station = WeatherStation()
        display = StatisticsDisplay()

        station.register_observer(display)

        # Add multiple measurements
        station.set_measurements(20.0, 60.0, 1010.0)
        station.set_measurements(25.0, 65.0, 1015.0)
        station.set_measurements(30.0, 70.0, 1020.0)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")

        # Check that statistics are calculated correctly
        assert "Statistics: Avg temp: 25.0°C, Min: 20.0°C, Max: 30.0°C" in lines[-1]

        # Check display state
        assert display._temperatures == [20.0, 25.0, 30.0]
        assert display._humidities == [60.0, 65.0, 70.0]
        assert display._pressures == [1010.0, 1015.0, 1020.0]

    def test_forecast_display(self, capsys):
        """Test forecast display."""
        station = WeatherStation()
        display = ForecastDisplay()

        station.register_observer(display)

        # First measurement
        station.set_measurements(25.0, 65.0, 1013.0)

        # Second measurement with higher pressure
        station.set_measurements(26.0, 66.0, 1016.0)

        # Third measurement with lower pressure
        station.set_measurements(24.0, 64.0, 1010.0)

        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")

        # Check forecasts
        assert "Forecast: More of the same" in lines[0]  # First measurement
        assert (
            "Forecast: Improving weather on the way!" in lines[1]
        )  # Pressure increased
        assert (
            "Forecast: Watch out for cooler, rainy weather" in lines[2]
        )  # Pressure decreased

    def test_multiple_displays(self, capsys):
        """Test multiple displays receiving updates."""
        station = WeatherStation()
        current = CurrentConditionsDisplay()
        stats = StatisticsDisplay()
        forecast = ForecastDisplay()

        station.register_observer(current)
        station.register_observer(stats)
        station.register_observer(forecast)

        station.set_measurements(25.0, 65.0, 1013.0)

        captured = capsys.readouterr()
        assert "Current conditions:" in captured.out
        assert "Statistics:" in captured.out
        assert "Forecast:" in captured.out

    def test_weather_observer_removal(self, capsys):
        """Test removing weather observers."""
        station = WeatherStation()
        current = CurrentConditionsDisplay()
        stats = StatisticsDisplay()

        station.register_observer(current)
        station.register_observer(stats)

        # Remove current display
        station.remove_observer(current)

        station.set_measurements(25.0, 65.0, 1013.0)

        captured = capsys.readouterr()
        assert "Current conditions:" not in captured.out
        assert "Statistics:" in captured.out


class TestStockObserver:
    """Test the Stock observer implementation."""

    def test_stock_creation(self):
        """Test creating a stock."""
        stock = Stock("AAPL", 150.0)
        assert stock.get_symbol() == "AAPL"
        assert stock.get_price() == 150.0
        assert len(stock._observers) == 0

    def test_stock_price_update(self):
        """Test updating stock price."""
        stock = Stock("AAPL", 150.0)

        stock.set_price(155.0)
        assert stock.get_price() == 155.0

    def test_stock_display(self, capsys):
        """Test stock display observer."""
        stock = Stock("AAPL", 150.0)
        display = StockDisplay("Portfolio Display")

        stock.register_observer(display)
        stock.set_price(155.0)

        captured = capsys.readouterr()
        assert "Portfolio Display: AAPL is now $155.00" in captured.out

    def test_trading_bot_signals(self, capsys):
        """Test trading bot signals."""
        stock = Stock("AAPL", 150.0)
        bot = TradingBot("AlgoBot", buy_threshold=140.0, sell_threshold=160.0)

        stock.register_observer(bot)

        # Test hold signal
        stock.set_price(150.0)
        captured = capsys.readouterr()
        assert "AlgoBot: HOLD AAPL at $150.00" in captured.out

        # Test buy signal
        stock.set_price(135.0)
        captured = capsys.readouterr()
        assert "AlgoBot: BUY signal for AAPL at $135.00" in captured.out

        # Test sell signal
        stock.set_price(165.0)
        captured = capsys.readouterr()
        assert "AlgoBot: SELL signal for AAPL at $165.00" in captured.out

    def test_trading_bot_edge_cases(self, capsys):
        """Test trading bot at threshold boundaries."""
        stock = Stock("AAPL", 150.0)
        bot = TradingBot("AlgoBot", buy_threshold=140.0, sell_threshold=160.0)

        stock.register_observer(bot)

        # Test exact buy threshold
        stock.set_price(140.0)
        captured = capsys.readouterr()
        assert "AlgoBot: BUY signal for AAPL at $140.00" in captured.out

        # Test exact sell threshold
        stock.set_price(160.0)
        captured = capsys.readouterr()
        assert "AlgoBot: SELL signal for AAPL at $160.00" in captured.out

    def test_multiple_stock_observers(self, capsys):
        """Test multiple observers on the same stock."""
        stock = Stock("AAPL", 150.0)
        display1 = StockDisplay("Display 1")
        display2 = StockDisplay("Display 2")
        bot = TradingBot("Bot", buy_threshold=140.0, sell_threshold=160.0)

        stock.register_observer(display1)
        stock.register_observer(display2)
        stock.register_observer(bot)

        stock.set_price(165.0)

        captured = capsys.readouterr()
        assert "Display 1: AAPL is now $165.00" in captured.out
        assert "Display 2: AAPL is now $165.00" in captured.out
        assert "Bot: SELL signal for AAPL at $165.00" in captured.out


class TestEventSystem:
    """Test the Event system implementation."""

    def test_event_creation(self):
        """Test creating events."""
        data = {"user_id": 123, "name": "John"}
        event = Event("user_registered", data, datetime.now(), "user_service")

        assert event.event_type == "user_registered"
        assert event.data == data
        assert event.source == "user_service"
        assert isinstance(event.timestamp, datetime)

    def test_event_manager_creation(self):
        """Test creating event manager."""
        manager = EventManager()
        assert len(manager._listeners) == 0
        assert len(manager._event_history) == 0

    def test_event_subscription(self):
        """Test subscribing to events."""
        manager = EventManager()

        def callback(event):
            pass

        manager.subscribe("test_event", callback)
        assert "test_event" in manager._listeners
        assert callback in manager._listeners["test_event"]

    def test_event_unsubscription(self):
        """Test unsubscribing from events."""
        manager = EventManager()

        def callback(event):
            pass

        manager.subscribe("test_event", callback)
        manager.unsubscribe("test_event", callback)

        assert len(manager._listeners["test_event"]) == 0

    def test_unsubscribe_nonexistent_callback(self):
        """Test unsubscribing a callback that was never subscribed."""
        manager = EventManager()

        def callback(event):
            pass

        # Should not raise an exception
        manager.unsubscribe("test_event", callback)
        assert "test_event" not in manager._listeners

    def test_event_emission(self):
        """Test emitting events."""
        manager = EventManager()
        received_events = []

        def callback(event):
            received_events.append(event)

        manager.subscribe("test_event", callback)
        manager.emit("test_event", {"key": "value"}, "test_source")

        assert len(received_events) == 1
        event = received_events[0]
        assert event.event_type == "test_event"
        assert event.data == {"key": "value"}
        assert event.source == "test_source"
        assert isinstance(event.timestamp, datetime)

    def test_event_history(self):
        """Test event history tracking."""
        manager = EventManager()

        manager.emit("event1", {"data": 1}, "source1")
        manager.emit("event2", {"data": 2}, "source2")

        history = manager.get_event_history()
        assert len(history) == 2
        assert history[0].event_type == "event1"
        assert history[1].event_type == "event2"

    def test_event_history_filtering(self):
        """Test filtering event history by type."""
        manager = EventManager()

        manager.emit("event1", {"data": 1}, "source1")
        manager.emit("event2", {"data": 2}, "source2")
        manager.emit("event1", {"data": 3}, "source1")

        event1_history = manager.get_event_history("event1")
        assert len(event1_history) == 2
        assert all(e.event_type == "event1" for e in event1_history)

        event2_history = manager.get_event_history("event2")
        assert len(event2_history) == 1
        assert event2_history[0].event_type == "event2"

    def test_clear_event_history(self):
        """Test clearing event history."""
        manager = EventManager()

        manager.emit("event1", {"data": 1}, "source1")
        manager.emit("event2", {"data": 2}, "source2")

        assert len(manager.get_event_history()) == 2

        manager.clear_history()
        assert len(manager.get_event_history()) == 0

    def test_multiple_callbacks(self):
        """Test multiple callbacks for the same event."""
        manager = EventManager()
        received_events = []

        def callback1(event):
            received_events.append(f"callback1: {event.event_type}")

        def callback2(event):
            received_events.append(f"callback2: {event.event_type}")

        manager.subscribe("test_event", callback1)
        manager.subscribe("test_event", callback2)

        manager.emit("test_event", {"data": "test"}, "test_source")

        assert len(received_events) == 2
        assert "callback1: test_event" in received_events
        assert "callback2: test_event" in received_events

    def test_callback_exception_handling(self, capsys):
        """Test that callback exceptions don't break the system."""
        manager = EventManager()

        def failing_callback(event):
            raise ValueError("Callback error")

        def working_callback(event):
            print(f"Working callback received: {event.event_type}")

        manager.subscribe("test_event", failing_callback)
        manager.subscribe("test_event", working_callback)

        manager.emit("test_event", {"data": "test"}, "test_source")

        captured = capsys.readouterr()
        assert "Error in event callback: Callback error" in captured.out
        assert "Working callback received: test_event" in captured.out


class TestUserService:
    """Test the UserService implementation."""

    def test_user_service_creation(self):
        """Test creating user service."""
        manager = EventManager()
        service = UserService(manager)

        assert service.event_manager is manager
        assert len(service.users) == 0

    def test_user_registration(self):
        """Test user registration."""
        manager = EventManager()
        service = UserService(manager)

        service.register_user(1, "Alice", "alice@example.com")

        assert 1 in service.users
        user = service.users[1]
        assert user["name"] == "Alice"
        assert user["email"] == "alice@example.com"

        # Check event was emitted
        history = manager.get_event_history("user_registered")
        assert len(history) == 1
        assert history[0].data["user_id"] == 1
        assert history[0].data["name"] == "Alice"

    def test_user_email_update(self):
        """Test updating user email."""
        manager = EventManager()
        service = UserService(manager)

        # Register user first
        service.register_user(1, "Alice", "alice@example.com")

        # Update email
        service.update_user_email(1, "alice.new@example.com")

        assert service.users[1]["email"] == "alice.new@example.com"

        # Check event was emitted
        history = manager.get_event_history("user_email_updated")
        assert len(history) == 1
        event = history[0]
        assert event.data["user_id"] == 1
        assert event.data["old_email"] == "alice@example.com"
        assert event.data["new_email"] == "alice.new@example.com"

    def test_update_nonexistent_user(self):
        """Test updating email for nonexistent user."""
        manager = EventManager()
        service = UserService(manager)

        # Should not raise exception, just do nothing
        service.update_user_email(999, "new@example.com")

        # No event should be emitted
        history = manager.get_event_history("user_email_updated")
        assert len(history) == 0


class TestEmailService:
    """Test the EmailService implementation."""

    def test_email_service_creation(self):
        """Test creating email service."""
        manager = EventManager()
        service = EmailService(manager)

        assert service.event_manager is manager
        # Check that listeners are set up
        assert "user_registered" in manager._listeners
        assert "user_email_updated" in manager._listeners

    def test_welcome_email_on_registration(self, capsys):
        """Test welcome email is sent on user registration."""
        manager = EventManager()
        email_service = EmailService(manager)

        # Emit user registration event
        manager.emit(
            "user_registered",
            {"user_id": 1, "name": "Alice", "email": "alice@example.com"},
            "user_service",
        )

        captured = capsys.readouterr()
        assert "Sending welcome email to Alice at alice@example.com" in captured.out

    def test_confirmation_email_on_email_update(self, capsys):
        """Test confirmation email is sent on email update."""
        manager = EventManager()
        email_service = EmailService(manager)

        # Emit email update event
        manager.emit(
            "user_email_updated",
            {
                "user_id": 1,
                "old_email": "alice@example.com",
                "new_email": "alice.new@example.com",
            },
            "user_service",
        )

        captured = capsys.readouterr()
        assert (
            "Sending confirmation email to alice.new@example.com for user 1"
            in captured.out
        )


class TestAuditService:
    """Test the AuditService implementation."""

    def test_audit_service_creation(self):
        """Test creating audit service."""
        manager = EventManager()
        service = AuditService(manager)

        assert service.event_manager is manager
        assert len(service.audit_log) == 0

    def test_audit_user_registration(self, capsys):
        """Test auditing user registration."""
        manager = EventManager()
        audit_service = AuditService(manager)

        # Emit user registration event
        manager.emit(
            "user_registered",
            {"user_id": 1, "name": "Alice", "email": "alice@example.com"},
            "user_service",
        )

        captured = capsys.readouterr()
        assert "AUDIT: User 1 (Alice) registered at" in captured.out
        assert len(audit_service.audit_log) == 1
        assert "User 1 (Alice) registered at" in audit_service.audit_log[0]

    def test_audit_email_update(self, capsys):
        """Test auditing email update."""
        manager = EventManager()
        audit_service = AuditService(manager)

        # Emit email update event
        manager.emit(
            "user_email_updated",
            {
                "user_id": 1,
                "old_email": "alice@example.com",
                "new_email": "alice.new@example.com",
            },
            "user_service",
        )

        captured = capsys.readouterr()
        assert (
            "AUDIT: User 1 changed email from alice@example.com to alice.new@example.com at"
            in captured.out
        )
        assert len(audit_service.audit_log) == 1
        assert (
            "User 1 changed email from alice@example.com to alice.new@example.com at"
            in audit_service.audit_log[0]
        )


class TestObserverPatternIntegration:
    """Test integration scenarios with observer pattern."""

    def test_complete_event_driven_system(self, capsys):
        """Test a complete event-driven system."""
        # Create event manager and services
        manager = EventManager()
        user_service = UserService(manager)
        email_service = EmailService(manager)
        audit_service = AuditService(manager)

        # Register a user
        user_service.register_user(1, "Alice", "alice@example.com")

        # Update user email
        user_service.update_user_email(1, "alice.new@example.com")

        # Check console output
        captured = capsys.readouterr()
        assert "Sending welcome email to Alice at alice@example.com" in captured.out
        assert (
            "Sending confirmation email to alice.new@example.com for user 1"
            in captured.out
        )
        assert "AUDIT: User 1 (Alice) registered at" in captured.out
        assert (
            "AUDIT: User 1 changed email from alice@example.com to alice.new@example.com at"
            in captured.out
        )

        # Check event history
        history = manager.get_event_history()
        assert len(history) == 2
        assert history[0].event_type == "user_registered"
        assert history[1].event_type == "user_email_updated"

        # Check audit log
        assert len(audit_service.audit_log) == 2

    def test_weather_station_integration(self, capsys):
        """Test complete weather station system."""
        station = WeatherStation()
        current = CurrentConditionsDisplay()
        stats = StatisticsDisplay()
        forecast = ForecastDisplay()

        # Register all displays
        station.register_observer(current)
        station.register_observer(stats)
        station.register_observer(forecast)

        # Update weather multiple times
        measurements = [
            (20.0, 60.0, 1010.0),
            (25.0, 65.0, 1015.0),
            (30.0, 70.0, 1020.0),
        ]

        for temp, humidity, pressure in measurements:
            station.set_measurements(temp, humidity, pressure)

        captured = capsys.readouterr()

        # Check all displays received updates
        assert captured.out.count("Current conditions:") == 3
        assert captured.out.count("Statistics:") == 3
        assert captured.out.count("Forecast:") == 3

        # Check final statistics
        assert "Statistics: Avg temp: 25.0°C, Min: 20.0°C, Max: 30.0°C" in captured.out

    def test_stock_trading_system(self, capsys):
        """Test complete stock trading system."""
        # Create multiple stocks
        stocks = [Stock("AAPL", 150.0), Stock("GOOGL", 2800.0), Stock("MSFT", 300.0)]

        # Create trading bots with different strategies
        conservative_bot = TradingBot("Conservative", 140.0, 160.0)
        aggressive_bot = TradingBot("Aggressive", 145.0, 155.0)

        # Create portfolio display
        portfolio = StockDisplay("Portfolio")

        # Register observers
        for stock in stocks:
            stock.register_observer(conservative_bot)
            stock.register_observer(aggressive_bot)
            stock.register_observer(portfolio)

        # Update stock prices
        stocks[0].set_price(135.0)  # AAPL - should trigger buy for both bots
        stocks[1].set_price(2750.0)  # GOOGL - should trigger conservative buy only
        stocks[2].set_price(310.0)  # MSFT - should trigger aggressive sell only

        captured = capsys.readouterr()

        # Check portfolio display
        assert "Portfolio: AAPL is now $135.00" in captured.out
        assert "Portfolio: GOOGL is now $2750.00" in captured.out
        assert "Portfolio: MSFT is now $310.00" in captured.out

        # Check trading signals
        assert "Conservative: BUY signal for AAPL at $135.00" in captured.out
        assert "Aggressive: BUY signal for AAPL at $135.00" in captured.out


class TestObserverPatternEdgeCases:
    """Test edge cases and error conditions."""

    def test_observer_modifying_during_notification(self):
        """Test behavior when observers modify the subject during notification."""
        subject = ConcreteSubject()

        class ModifyingObserver(Observer):
            def __init__(self, subject, name):
                self.subject = subject
                self.name = name
                self.updates = []

            def update(self, state):
                self.updates.append(state)
                # Try to modify subject during notification
                if state == "trigger":
                    self.subject.set_state("modified")

        observer = ModifyingObserver(subject, "Modifier")
        subject.register_observer(observer)

        # This should not cause infinite recursion
        subject.set_state("trigger")

        # Check that both states were recorded
        assert len(observer.updates) >= 1
        assert "trigger" in observer.updates

    def test_observer_removing_itself_during_notification(self):
        """Test behavior when an observer removes itself during notification."""
        subject = ConcreteSubject()

        class SelfRemovingObserver(Observer):
            def __init__(self, subject, name):
                self.subject = subject
                self.name = name
                self.updates = []

            def update(self, state):
                self.updates.append(state)
                # Remove self during notification
                self.subject.remove_observer(self)

        observer = SelfRemovingObserver(subject, "SelfRemover")
        subject.register_observer(observer)

        # First update should work and remove the observer
        subject.set_state("first")
        assert len(observer.updates) == 1
        assert observer not in subject._observers

        # Second update should not reach the observer
        subject.set_state("second")
        assert len(observer.updates) == 1  # Still only one update

    def test_notification_with_no_observers(self):
        """Test notification when no observers are registered."""
        subject = ConcreteSubject()

        # Should not raise any exceptions
        subject.set_state("test")
        assert subject.get_state() == "test"

    def test_circular_observer_references(self):
        """Test handling of circular observer references."""
        subject1 = ConcreteSubject()
        subject2 = ConcreteSubject()

        class CrossObserver(Observer):
            def __init__(self, other_subject, name):
                self.other_subject = other_subject
                self.name = name
                self.updates = []

            def update(self, state):
                self.updates.append(state)
                # Don't create infinite loop
                if len(self.updates) < 2:
                    self.other_subject.set_state(f"response_{state}")

        observer1 = CrossObserver(subject2, "Observer1")
        observer2 = CrossObserver(subject1, "Observer2")

        subject1.register_observer(observer1)
        subject2.register_observer(observer2)

        # Trigger the chain
        subject1.set_state("start")

        # Both observers should have received updates
        assert len(observer1.updates) >= 1
        assert len(observer2.updates) >= 1
        assert "start" in observer1.updates
        assert "response_start" in observer2.updates


class TestObserverPatternPerformance:
    """Test performance characteristics of observer pattern."""

    def test_many_observers_performance(self):
        """Test performance with many observers."""
        import time

        subject = ConcreteSubject()

        # Create many observers
        observers = [ConcreteObserver(f"Observer_{i}") for i in range(1000)]

        # Register all observers
        for observer in observers:
            subject.register_observer(observer)

        # Measure notification time
        start = time.time()
        subject.set_state("test")
        end = time.time()

        notification_time = end - start

        # Should be reasonably fast
        assert notification_time < 1.0

        # All observers should have received the update
        assert all(obs._state == "test" for obs in observers)

    def test_frequent_updates_performance(self):
        """Test performance with frequent updates."""
        import time

        subject = ConcreteSubject()
        observer = ConcreteObserver("PerfObserver")
        subject.register_observer(observer)

        # Measure time for many updates
        start = time.time()
        for i in range(10000):
            subject.set_state(f"state_{i}")
        end = time.time()

        update_time = end - start

        # Should be reasonably fast
        assert update_time < 2.0

        # Final state should be correct
        assert observer._state == "state_9999"
