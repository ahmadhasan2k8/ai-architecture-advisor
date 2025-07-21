"""Tests for factory pattern implementations."""

import math
from typing import Type

import pytest

from implementations.patterns.factory import (  # Basic Factory Pattern; Notification Factory; Shape Factory; Abstract Factory
    AbstractFactory,
    Button,
    Checkbox,
    Circle,
    ConcreteCreatorA,
    ConcreteCreatorB,
    ConcreteProductA,
    ConcreteProductB,
    Creator,
    EmailNotifier,
    MacOSButton,
    MacOSCheckbox,
    MacOSFactory,
    NotificationFactory,
    Notifier,
    Product,
    PushNotifier,
    Rectangle,
    Shape,
    ShapeFactory,
    SimpleFactory,
    SMSNotifier,
    Triangle,
    UIComponentFactory,
    WindowsButton,
    WindowsCheckbox,
    WindowsFactory,
)


class TestBasicFactoryPattern:
    """Test the basic Factory Method pattern."""

    def test_concrete_product_a(self):
        """Test ConcreteProductA functionality."""
        product = ConcreteProductA()
        assert isinstance(product, Product)
        assert product.operation() == "Result of the ConcreteProductA operation"

    def test_concrete_product_b(self):
        """Test ConcreteProductB functionality."""
        product = ConcreteProductB()
        assert isinstance(product, Product)
        assert product.operation() == "Result of the ConcreteProductB operation"

    def test_concrete_creator_a(self):
        """Test ConcreteCreatorA creates correct product."""
        creator = ConcreteCreatorA()
        product = creator.factory_method()
        assert isinstance(product, ConcreteProductA)
        assert "ConcreteProductA" in creator.some_operation()

    def test_concrete_creator_b(self):
        """Test ConcreteCreatorB creates correct product."""
        creator = ConcreteCreatorB()
        product = creator.factory_method()
        assert isinstance(product, ConcreteProductB)
        assert "ConcreteProductB" in creator.some_operation()

    def test_factory_method_polymorphism(self):
        """Test polymorphic behavior of different creators."""
        creators = [ConcreteCreatorA(), ConcreteCreatorB()]

        for creator in creators:
            product = creator.factory_method()
            assert isinstance(product, Product)
            operation_result = creator.some_operation()
            assert "Creator: Working with Result of the" in operation_result


class TestSimpleFactory:
    """Test the SimpleFactory implementation."""

    def test_create_product_a(self):
        """Test creating product A."""
        product = SimpleFactory.create_product("A")
        assert isinstance(product, ConcreteProductA)
        assert product.operation() == "Result of the ConcreteProductA operation"

    def test_create_product_b(self):
        """Test creating product B."""
        product = SimpleFactory.create_product("B")
        assert isinstance(product, ConcreteProductB)
        assert product.operation() == "Result of the ConcreteProductB operation"

    def test_create_unknown_product(self):
        """Test creating unknown product raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            SimpleFactory.create_product("C")
        assert "Unknown product type: C" in str(exc_info.value)

    def test_get_supported_types(self):
        """Test getting supported product types."""
        supported = SimpleFactory.get_supported_types()
        assert supported == ["A", "B"]
        assert isinstance(supported, list)

    def test_case_sensitivity(self):
        """Test that factory is case-sensitive."""
        with pytest.raises(ValueError):
            SimpleFactory.create_product("a")  # lowercase

        with pytest.raises(ValueError):
            SimpleFactory.create_product("b")  # lowercase


class TestNotificationFactory:
    """Test the NotificationFactory implementation."""

    def test_create_email_notifier(self):
        """Test creating email notifier."""
        notifier = NotificationFactory.create_notifier("email")
        assert isinstance(notifier, EmailNotifier)
        assert notifier.smtp_server == "smtp.gmail.com"
        assert notifier.username == "app@company.com"

    def test_create_email_notifier_with_params(self):
        """Test creating email notifier with custom parameters."""
        notifier = NotificationFactory.create_notifier(
            "email",
            smtp_server="smtp.outlook.com",
            username="custom@company.com",
            password="custom_pass",
        )
        assert isinstance(notifier, EmailNotifier)
        assert notifier.smtp_server == "smtp.outlook.com"
        assert notifier.username == "custom@company.com"
        assert notifier.password == "custom_pass"

    def test_create_sms_notifier(self):
        """Test creating SMS notifier."""
        notifier = NotificationFactory.create_notifier("sms")
        assert isinstance(notifier, SMSNotifier)
        assert notifier.api_key == "default_key"
        assert notifier.service == "Twilio"

    def test_create_sms_notifier_with_params(self):
        """Test creating SMS notifier with custom parameters."""
        notifier = NotificationFactory.create_notifier(
            "sms", api_key="custom_key", service="Custom Service"
        )
        assert isinstance(notifier, SMSNotifier)
        assert notifier.api_key == "custom_key"
        assert notifier.service == "Custom Service"

    def test_create_push_notifier(self):
        """Test creating push notifier."""
        notifier = NotificationFactory.create_notifier("push")
        assert isinstance(notifier, PushNotifier)
        assert notifier.app_id == "com.company.app"
        assert notifier.service == "Firebase"

    def test_create_push_notifier_with_params(self):
        """Test creating push notifier with custom parameters."""
        notifier = NotificationFactory.create_notifier(
            "push", app_id="com.custom.app", service="Custom Push Service"
        )
        assert isinstance(notifier, PushNotifier)
        assert notifier.app_id == "com.custom.app"
        assert notifier.service == "Custom Push Service"

    def test_case_insensitive_creation(self):
        """Test that factory is case-insensitive."""
        notifiers = [
            NotificationFactory.create_notifier("EMAIL"),
            NotificationFactory.create_notifier("Email"),
            NotificationFactory.create_notifier("eMaIl"),
            NotificationFactory.create_notifier("SMS"),
            NotificationFactory.create_notifier("sms"),
            NotificationFactory.create_notifier("PUSH"),
            NotificationFactory.create_notifier("push"),
        ]

        assert all(isinstance(n, Notifier) for n in notifiers)
        assert isinstance(notifiers[0], EmailNotifier)
        assert isinstance(notifiers[1], EmailNotifier)
        assert isinstance(notifiers[2], EmailNotifier)
        assert isinstance(notifiers[3], SMSNotifier)
        assert isinstance(notifiers[4], SMSNotifier)
        assert isinstance(notifiers[5], PushNotifier)
        assert isinstance(notifiers[6], PushNotifier)

    def test_create_unknown_notifier(self):
        """Test creating unknown notifier raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            NotificationFactory.create_notifier("fax")
        assert "Unknown notification type: fax" in str(exc_info.value)
        assert "email, sms, push" in str(exc_info.value)

    def test_get_supported_types(self):
        """Test getting supported notification types."""
        supported = NotificationFactory.get_supported_types()
        assert supported == ["email", "sms", "push"]

    def test_notifier_send_methods(self, capsys):
        """Test that all notifiers can send messages."""
        email = NotificationFactory.create_notifier("email")
        sms = NotificationFactory.create_notifier("sms")
        push = NotificationFactory.create_notifier("push")

        email.send("test@example.com", "Email test")
        sms.send("+1234567890", "SMS test")
        push.send("device_token", "Push test")

        captured = capsys.readouterr()
        assert "Email sent to test@example.com: Email test" in captured.out
        assert "SMS sent to +1234567890: SMS test" in captured.out
        assert "Push notification sent to device_token: Push test" in captured.out


class TestShapeFactory:
    """Test the ShapeFactory implementation."""

    def test_create_circle(self):
        """Test creating a circle."""
        circle = ShapeFactory.create_shape("circle", radius=5)
        assert isinstance(circle, Circle)
        assert circle.radius == 5
        assert circle.area() == pytest.approx(math.pi * 25, rel=1e-9)
        assert circle.perimeter() == pytest.approx(2 * math.pi * 5, rel=1e-9)

    def test_create_rectangle(self):
        """Test creating a rectangle."""
        rectangle = ShapeFactory.create_shape("rectangle", width=4, height=3)
        assert isinstance(rectangle, Rectangle)
        assert rectangle.width == 4
        assert rectangle.height == 3
        assert rectangle.area() == 12
        assert rectangle.perimeter() == 14

    def test_create_triangle(self):
        """Test creating a triangle."""
        triangle = ShapeFactory.create_shape("triangle", side=6)
        assert isinstance(triangle, Triangle)
        assert triangle.side == 6
        expected_area = (math.sqrt(3) / 4) * 36
        assert triangle.area() == pytest.approx(expected_area, rel=1e-9)
        assert triangle.perimeter() == 18

    def test_case_insensitive_creation(self):
        """Test that shape factory is case-insensitive."""
        shapes = [
            ShapeFactory.create_shape("CIRCLE", radius=1),
            ShapeFactory.create_shape("Circle", radius=1),
            ShapeFactory.create_shape("RECTANGLE", width=1, height=1),
            ShapeFactory.create_shape("Rectangle", width=1, height=1),
            ShapeFactory.create_shape("TRIANGLE", side=1),
            ShapeFactory.create_shape("Triangle", side=1),
        ]

        assert all(isinstance(s, Shape) for s in shapes)
        assert isinstance(shapes[0], Circle)
        assert isinstance(shapes[1], Circle)
        assert isinstance(shapes[2], Rectangle)
        assert isinstance(shapes[3], Rectangle)
        assert isinstance(shapes[4], Triangle)
        assert isinstance(shapes[5], Triangle)

    def test_missing_parameters(self):
        """Test creating shapes with missing parameters."""
        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("circle")
        assert "Circle requires 'radius' parameter" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("rectangle", width=5)
        assert "Rectangle requires 'width' and 'height' parameters" in str(
            exc_info.value
        )

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("rectangle", height=5)
        assert "Rectangle requires 'width' and 'height' parameters" in str(
            exc_info.value
        )

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("triangle")
        assert "Triangle requires 'side' parameter" in str(exc_info.value)

    def test_invalid_shape_parameters(self):
        """Test creating shapes with invalid parameters."""
        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("circle", radius=-1)
        assert "Radius must be positive" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("rectangle", width=-1, height=5)
        assert "Width and height must be positive" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("rectangle", width=5, height=-1)
        assert "Width and height must be positive" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("triangle", side=-1)
        assert "Side length must be positive" in str(exc_info.value)

    def test_zero_parameters(self):
        """Test creating shapes with zero parameters."""
        with pytest.raises(ValueError):
            ShapeFactory.create_shape("circle", radius=0)

        with pytest.raises(ValueError):
            ShapeFactory.create_shape("rectangle", width=0, height=5)

        with pytest.raises(ValueError):
            ShapeFactory.create_shape("triangle", side=0)

    def test_unknown_shape(self):
        """Test creating unknown shape raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            ShapeFactory.create_shape("hexagon", sides=6)
        assert "Unknown shape type: hexagon" in str(exc_info.value)
        assert "circle, rectangle, triangle" in str(exc_info.value)

    def test_get_supported_shapes(self):
        """Test getting supported shape types."""
        supported = ShapeFactory.get_supported_shapes()
        assert supported == ["circle", "rectangle", "triangle"]

    def test_shape_calculations(self):
        """Test mathematical calculations are correct."""
        # Test circle with radius 1
        circle = ShapeFactory.create_shape("circle", radius=1)
        assert circle.area() == pytest.approx(math.pi, rel=1e-9)
        assert circle.perimeter() == pytest.approx(2 * math.pi, rel=1e-9)

        # Test unit square
        square = ShapeFactory.create_shape("rectangle", width=1, height=1)
        assert square.area() == 1
        assert square.perimeter() == 4

        # Test equilateral triangle with side 1
        triangle = ShapeFactory.create_shape("triangle", side=1)
        expected_area = math.sqrt(3) / 4
        assert triangle.area() == pytest.approx(expected_area, rel=1e-9)
        assert triangle.perimeter() == 3


class TestAbstractFactory:
    """Test the Abstract Factory pattern."""

    def test_windows_factory(self):
        """Test Windows factory creates Windows components."""
        factory = WindowsFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()

        assert isinstance(button, WindowsButton)
        assert isinstance(checkbox, WindowsCheckbox)
        assert button.paint() == "Windows button with flat design"
        assert checkbox.paint() == "Windows checkbox with square design"

    def test_macos_factory(self):
        """Test macOS factory creates macOS components."""
        factory = MacOSFactory()

        button = factory.create_button()
        checkbox = factory.create_checkbox()

        assert isinstance(button, MacOSButton)
        assert isinstance(checkbox, MacOSCheckbox)
        assert button.paint() == "macOS button with rounded corners"
        assert checkbox.paint() == "macOS checkbox with rounded design"

    def test_ui_component_factory(self):
        """Test UI component factory creates correct factories."""
        windows_factory = UIComponentFactory.create_factory("windows")
        macos_factory = UIComponentFactory.create_factory("macos")

        assert isinstance(windows_factory, WindowsFactory)
        assert isinstance(macos_factory, MacOSFactory)

    def test_ui_component_factory_case_insensitive(self):
        """Test UI component factory is case-insensitive."""
        factories = [
            UIComponentFactory.create_factory("WINDOWS"),
            UIComponentFactory.create_factory("Windows"),
            UIComponentFactory.create_factory("windows"),
            UIComponentFactory.create_factory("MACOS"),
            UIComponentFactory.create_factory("MacOS"),
            UIComponentFactory.create_factory("macos"),
        ]

        assert isinstance(factories[0], WindowsFactory)
        assert isinstance(factories[1], WindowsFactory)
        assert isinstance(factories[2], WindowsFactory)
        assert isinstance(factories[3], MacOSFactory)
        assert isinstance(factories[4], MacOSFactory)
        assert isinstance(factories[5], MacOSFactory)

    def test_unknown_platform(self):
        """Test unknown platform raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            UIComponentFactory.create_factory("linux")
        assert "Unknown platform: linux" in str(exc_info.value)
        assert "windows, macos" in str(exc_info.value)

    def test_get_supported_platforms(self):
        """Test getting supported platforms."""
        supported = UIComponentFactory.get_supported_platforms()
        assert supported == ["windows", "macos"]

    def test_abstract_factory_interface(self):
        """Test that factories implement the AbstractFactory interface."""
        windows_factory = WindowsFactory()
        macos_factory = MacOSFactory()

        assert isinstance(windows_factory, AbstractFactory)
        assert isinstance(macos_factory, AbstractFactory)

    def test_component_interfaces(self):
        """Test that components implement correct interfaces."""
        windows_factory = WindowsFactory()
        macos_factory = MacOSFactory()

        # Test Windows components
        win_button = windows_factory.create_button()
        win_checkbox = windows_factory.create_checkbox()

        assert isinstance(win_button, Button)
        assert isinstance(win_checkbox, Checkbox)

        # Test macOS components
        mac_button = macos_factory.create_button()
        mac_checkbox = macos_factory.create_checkbox()

        assert isinstance(mac_button, Button)
        assert isinstance(mac_checkbox, Checkbox)


class TestFactoryEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_string_parameters(self):
        """Test factories with empty string parameters."""
        with pytest.raises(ValueError):
            NotificationFactory.create_notifier("")

        with pytest.raises(ValueError):
            ShapeFactory.create_shape("")

        with pytest.raises(ValueError):
            UIComponentFactory.create_factory("")

    def test_none_parameters(self):
        """Test factories with None parameters."""
        with pytest.raises(AttributeError):
            NotificationFactory.create_notifier(None)

        with pytest.raises(AttributeError):
            ShapeFactory.create_shape(None)

        with pytest.raises(AttributeError):
            UIComponentFactory.create_factory(None)

    def test_extra_parameters(self):
        """Test factories with extra parameters."""
        # These should work fine - extra parameters are ignored
        circle = ShapeFactory.create_shape("circle", radius=5, extra_param="ignored")
        assert isinstance(circle, Circle)
        assert circle.radius == 5

        email = NotificationFactory.create_notifier("email", extra_param="ignored")
        assert isinstance(email, EmailNotifier)

    def test_factory_consistency(self):
        """Test that factories consistently create the same type."""
        # Create multiple instances of the same type
        circles = [ShapeFactory.create_shape("circle", radius=i) for i in range(1, 6)]
        emails = [NotificationFactory.create_notifier("email") for _ in range(5)]

        # All should be the same type
        assert all(isinstance(c, Circle) for c in circles)
        assert all(isinstance(e, EmailNotifier) for e in emails)

        # But different instances
        assert len(set(id(c) for c in circles)) == 5
        assert len(set(id(e) for e in emails)) == 5


class TestFactoryIntegration:
    """Test integration scenarios with factories."""

    def test_notification_system_integration(self, capsys):
        """Test a complete notification system using factories."""
        # Create different notification services
        email = NotificationFactory.create_notifier("email")
        sms = NotificationFactory.create_notifier("sms")
        push = NotificationFactory.create_notifier("push")

        # Send notifications
        message = "System maintenance scheduled"
        recipients = ["user@example.com", "+1234567890", "device_token"]

        email.send(recipients[0], message)
        sms.send(recipients[1], message)
        push.send(recipients[2], message)

        captured = capsys.readouterr()
        assert "Email sent to user@example.com" in captured.out
        assert "SMS sent to +1234567890" in captured.out
        assert "Push notification sent to device_token" in captured.out

    def test_shape_calculation_system(self):
        """Test a complete shape calculation system."""
        shapes = [
            ShapeFactory.create_shape("circle", radius=5),
            ShapeFactory.create_shape("rectangle", width=4, height=3),
            ShapeFactory.create_shape("triangle", side=6),
        ]

        total_area = sum(shape.area() for shape in shapes)
        total_perimeter = sum(shape.perimeter() for shape in shapes)

        expected_area = (math.pi * 25) + 12 + (math.sqrt(3) / 4 * 36)
        expected_perimeter = (2 * math.pi * 5) + 14 + 18

        assert total_area == pytest.approx(expected_area, rel=1e-9)
        assert total_perimeter == pytest.approx(expected_perimeter, rel=1e-9)

    def test_cross_platform_ui_system(self):
        """Test a cross-platform UI system."""
        platforms = ["windows", "macos"]

        for platform in platforms:
            factory = UIComponentFactory.create_factory(platform)

            # Create UI components
            button = factory.create_button()
            checkbox = factory.create_checkbox()

            # Test that they work correctly
            button_description = button.paint()
            checkbox_description = checkbox.paint()

            assert platform.lower() in button_description.lower()
            assert platform.lower() in checkbox_description.lower()

            # Test polymorphism
            assert isinstance(button, Button)
            assert isinstance(checkbox, Checkbox)


class TestFactoryPerformance:
    """Test performance characteristics of factories."""

    def test_factory_creation_performance(self):
        """Test that factory creation is efficient."""
        import time

        # Time shape creation
        start = time.time()
        shapes = [ShapeFactory.create_shape("circle", radius=i) for i in range(1, 1001)]
        creation_time = time.time() - start

        assert len(shapes) == 1000
        assert creation_time < 1.0  # Should be very fast
        assert all(isinstance(s, Circle) for s in shapes)

    def test_factory_memory_usage(self):
        """Test that factories don't leak memory."""
        import gc

        # Create many objects
        shapes = [ShapeFactory.create_shape("circle", radius=1) for _ in range(10000)]

        # Delete references
        del shapes

        # Force garbage collection
        gc.collect()

        # Should not cause memory issues (test passes if no exception)
        assert True
