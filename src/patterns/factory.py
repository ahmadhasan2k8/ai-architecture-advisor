"""Factory pattern implementations.

This module provides implementations of the Factory and Abstract Factory patterns,
demonstrating how to create objects without specifying their exact classes.
"""

import math
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type, TypeVar, Union

T = TypeVar("T")


class Product(ABC):
    """Abstract base class for products created by factories."""
    
    @abstractmethod
    def operation(self) -> str:
        """Perform the product's main operation.
        
        Returns:
            A string describing the operation performed.
        """
        pass


class ConcreteProductA(Product):
    """Concrete product A implementation."""
    
    def operation(self) -> str:
        """Return the result of the product A operation.
        
        Returns:
            A string describing product A's operation.
        """
        return "Result of the ConcreteProductA operation"


class ConcreteProductB(Product):
    """Concrete product B implementation."""
    
    def operation(self) -> str:
        """Return the result of the product B operation.
        
        Returns:
            A string describing product B's operation.
        """
        return "Result of the ConcreteProductB operation"


class Creator(ABC):
    """Abstract creator class defining the factory method pattern."""
    
    @abstractmethod
    def factory_method(self) -> Product:
        """Create a product instance.
        
        Returns:
            A Product instance.
        """
        pass
    
    def some_operation(self) -> str:
        """Perform some operation using the factory method.
        
        Returns:
            A string describing the operation and its result.
        """
        product = self.factory_method()
        result = product.operation()
        return f"Creator: Working with {result}"


class ConcreteCreatorA(Creator):
    """Concrete creator A that creates product A."""
    
    def factory_method(self) -> Product:
        """Create and return a ConcreteProductA instance.
        
        Returns:
            A ConcreteProductA instance.
        """
        return ConcreteProductA()


class ConcreteCreatorB(Creator):
    """Concrete creator B that creates product B."""
    
    def factory_method(self) -> Product:
        """Create and return a ConcreteProductB instance.
        
        Returns:
            A ConcreteProductB instance.
        """
        return ConcreteProductB()


class SimpleFactory:
    """Simple factory for creating products without inheritance."""
    
    @staticmethod
    def create_product(product_type: str) -> Product:
        """Create a product based on the specified type.
        
        Args:
            product_type: Type of product to create ("A" or "B")
            
        Returns:
            A Product instance of the specified type.
            
        Raises:
            ValueError: If the product type is not supported.
        """
        if product_type == "A":
            return ConcreteProductA()
        elif product_type == "B":
            return ConcreteProductB()
        else:
            raise ValueError(f"Unknown product type: {product_type}")
    
    @staticmethod
    def get_supported_types() -> list[str]:
        """Get a list of supported product types.
        
        Returns:
            List of supported product type strings.
        """
        return ["A", "B"]


# Notification System Example

class Notifier(ABC):
    """Abstract base class for notification services."""
    
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """Send a notification to a recipient.
        
        Args:
            recipient: The recipient of the notification
            message: The message to send
        """
        pass


class EmailNotifier(Notifier):
    """Email notification service."""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", 
                 username: str = "app@company.com", 
                 password: str = "secret"):
        """Initialize email notifier.
        
        Args:
            smtp_server: SMTP server address
            username: Email username
            password: Email password
        """
        self.smtp_server = smtp_server
        self.username = username
        self.password = password
    
    def send(self, recipient: str, message: str) -> None:
        """Send an email notification.
        
        Args:
            recipient: Email address of the recipient
            message: Message content
        """
        print(f"📧 Email sent to {recipient}: {message}")
        print(f"   Using SMTP server: {self.smtp_server}")


class SMSNotifier(Notifier):
    """SMS notification service."""
    
    def __init__(self, api_key: str = "default_key", 
                 service: str = "Twilio"):
        """Initialize SMS notifier.
        
        Args:
            api_key: API key for the SMS service
            service: Name of the SMS service provider
        """
        self.api_key = api_key
        self.service = service
    
    def send(self, recipient: str, message: str) -> None:
        """Send an SMS notification.
        
        Args:
            recipient: Phone number of the recipient
            message: Message content
        """
        print(f"📱 SMS sent to {recipient}: {message}")
        print(f"   Using service: {self.service}")


class PushNotifier(Notifier):
    """Push notification service."""
    
    def __init__(self, app_id: str = "com.company.app", 
                 service: str = "Firebase"):
        """Initialize push notifier.
        
        Args:
            app_id: Application ID
            service: Push notification service provider
        """
        self.app_id = app_id
        self.service = service
    
    def send(self, recipient: str, message: str) -> None:
        """Send a push notification.
        
        Args:
            recipient: User ID or device token
            message: Message content
        """
        print(f"🔔 Push notification sent to {recipient}: {message}")
        print(f"   Using service: {self.service}")


class NotificationFactory:
    """Factory for creating notification services."""
    
    @staticmethod
    def create_notifier(notification_type: str, **kwargs) -> Notifier:
        """Create a notifier based on the specified type.
        
        Args:
            notification_type: Type of notification service to create
            **kwargs: Additional parameters for the notifier
            
        Returns:
            A Notifier instance of the specified type.
            
        Raises:
            ValueError: If the notification type is not supported.
        """
        notification_type = notification_type.lower()
        
        if notification_type == "email":
            return EmailNotifier(**kwargs)
        elif notification_type == "sms":
            return SMSNotifier(**kwargs)
        elif notification_type == "push":
            return PushNotifier(**kwargs)
        else:
            supported = NotificationFactory.get_supported_types()
            raise ValueError(f"Unknown notification type: {notification_type}. "
                           f"Supported types: {supported}")
    
    @staticmethod
    def get_supported_types() -> list[str]:
        """Get a list of supported notification types.
        
        Returns:
            List of supported notification type strings.
        """
        return ["email", "sms", "push"]


# Shape Factory Example

class Shape(ABC):
    """Abstract base class for geometric shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape.
        
        Returns:
            The area of the shape.
        """
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate the perimeter of the shape.
        
        Returns:
            The perimeter of the shape.
        """
        pass


class Circle(Shape):
    """Circle shape implementation."""
    
    def __init__(self, radius: float):
        """Initialize a circle.
        
        Args:
            radius: The radius of the circle
            
        Raises:
            ValueError: If radius is not positive
        """
        if radius <= 0:
            raise ValueError("Radius must be positive")
        self.radius = radius
    
    def area(self) -> float:
        """Calculate the area of the circle.
        
        Returns:
            The area of the circle.
        """
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        """Calculate the perimeter (circumference) of the circle.
        
        Returns:
            The perimeter of the circle.
        """
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    """Rectangle shape implementation."""
    
    def __init__(self, width: float, height: float):
        """Initialize a rectangle.
        
        Args:
            width: The width of the rectangle
            height: The height of the rectangle
            
        Raises:
            ValueError: If width or height is not positive
        """
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        """Calculate the area of the rectangle.
        
        Returns:
            The area of the rectangle.
        """
        return self.width * self.height
    
    def perimeter(self) -> float:
        """Calculate the perimeter of the rectangle.
        
        Returns:
            The perimeter of the rectangle.
        """
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Equilateral triangle shape implementation."""
    
    def __init__(self, side: float):
        """Initialize an equilateral triangle.
        
        Args:
            side: The length of each side
            
        Raises:
            ValueError: If side length is not positive
        """
        if side <= 0:
            raise ValueError("Side length must be positive")
        self.side = side
    
    def area(self) -> float:
        """Calculate the area of the equilateral triangle.
        
        Returns:
            The area of the triangle.
        """
        return (math.sqrt(3) / 4) * self.side ** 2
    
    def perimeter(self) -> float:
        """Calculate the perimeter of the triangle.
        
        Returns:
            The perimeter of the triangle.
        """
        return 3 * self.side


class ShapeFactory:
    """Factory for creating geometric shapes."""
    
    @staticmethod
    def create_shape(shape_type: str, **kwargs) -> Shape:
        """Create a shape based on the specified type and parameters.
        
        Args:
            shape_type: Type of shape to create
            **kwargs: Parameters for the shape (radius, width, height, side)
            
        Returns:
            A Shape instance of the specified type.
            
        Raises:
            ValueError: If the shape type is not supported or required parameters are missing.
        """
        shape_type = shape_type.lower()
        
        if shape_type == "circle":
            if 'radius' not in kwargs:
                raise ValueError("Circle requires 'radius' parameter")
            return Circle(kwargs['radius'])
        
        elif shape_type == "rectangle":
            if 'width' not in kwargs or 'height' not in kwargs:
                raise ValueError("Rectangle requires 'width' and 'height' parameters")
            return Rectangle(kwargs['width'], kwargs['height'])
        
        elif shape_type == "triangle":
            if 'side' not in kwargs:
                raise ValueError("Triangle requires 'side' parameter")
            return Triangle(kwargs['side'])
        
        else:
            supported = ShapeFactory.get_supported_shapes()
            raise ValueError(f"Unknown shape type: {shape_type}. "
                           f"Supported types: {supported}")
    
    @staticmethod
    def get_supported_shapes() -> list[str]:
        """Get a list of supported shape types.
        
        Returns:
            List of supported shape type strings.
        """
        return ["circle", "rectangle", "triangle"]


# Abstract Factory Example

class AbstractFactory(ABC):
    """Abstract factory interface for creating families of related objects."""
    
    @abstractmethod
    def create_button(self) -> "Button":
        """Create a button component.
        
        Returns:
            A Button instance.
        """
        pass
    
    @abstractmethod
    def create_checkbox(self) -> "Checkbox":
        """Create a checkbox component.
        
        Returns:
            A Checkbox instance.
        """
        pass


class Button(ABC):
    """Abstract button component."""
    
    @abstractmethod
    def paint(self) -> str:
        """Paint the button.
        
        Returns:
            A string describing the button's appearance.
        """
        pass


class Checkbox(ABC):
    """Abstract checkbox component."""
    
    @abstractmethod
    def paint(self) -> str:
        """Paint the checkbox.
        
        Returns:
            A string describing the checkbox's appearance.
        """
        pass


class WindowsButton(Button):
    """Windows-style button implementation."""
    
    def paint(self) -> str:
        """Paint the Windows button.
        
        Returns:
            A string describing the Windows button's appearance.
        """
        return "Windows button with flat design"


class WindowsCheckbox(Checkbox):
    """Windows-style checkbox implementation."""
    
    def paint(self) -> str:
        """Paint the Windows checkbox.
        
        Returns:
            A string describing the Windows checkbox's appearance.
        """
        return "Windows checkbox with square design"


class MacOSButton(Button):
    """macOS-style button implementation."""
    
    def paint(self) -> str:
        """Paint the macOS button.
        
        Returns:
            A string describing the macOS button's appearance.
        """
        return "macOS button with rounded corners"


class MacOSCheckbox(Checkbox):
    """macOS-style checkbox implementation."""
    
    def paint(self) -> str:
        """Paint the macOS checkbox.
        
        Returns:
            A string describing the macOS checkbox's appearance.
        """
        return "macOS checkbox with rounded design"


class WindowsFactory(AbstractFactory):
    """Concrete factory for Windows UI components."""
    
    def create_button(self) -> Button:
        """Create a Windows button.
        
        Returns:
            A WindowsButton instance.
        """
        return WindowsButton()
    
    def create_checkbox(self) -> Checkbox:
        """Create a Windows checkbox.
        
        Returns:
            A WindowsCheckbox instance.
        """
        return WindowsCheckbox()


class MacOSFactory(AbstractFactory):
    """Concrete factory for macOS UI components."""
    
    def create_button(self) -> Button:
        """Create a macOS button.
        
        Returns:
            A MacOSButton instance.
        """
        return MacOSButton()
    
    def create_checkbox(self) -> Checkbox:
        """Create a macOS checkbox.
        
        Returns:
            A MacOSCheckbox instance.
        """
        return MacOSCheckbox()


class UIComponentFactory:
    """Factory for creating UI component factories based on platform."""
    
    @staticmethod
    def create_factory(platform: str) -> AbstractFactory:
        """Create a UI component factory for the specified platform.
        
        Args:
            platform: The target platform ("windows" or "macos")
            
        Returns:
            An AbstractFactory instance for the specified platform.
            
        Raises:
            ValueError: If the platform is not supported.
        """
        platform = platform.lower()
        
        if platform == "windows":
            return WindowsFactory()
        elif platform == "macos":
            return MacOSFactory()
        else:
            raise ValueError(f"Unknown platform: {platform}. "
                           f"Supported platforms: {UIComponentFactory.get_supported_platforms()}")
    
    @staticmethod
    def get_supported_platforms() -> list[str]:
        """Get a list of supported platforms.
        
        Returns:
            List of supported platform strings.
        """
        return ["windows", "macos"]


# Example client code
def client_code(creator: Creator) -> None:
    """Client code that works with creators through the base interface.
    
    Args:
        creator: A Creator instance
    """
    print(f"Client: I'm not aware of the creator's class, but it still works.")
    print(creator.some_operation())


# Example usage functions
def demonstrate_factory_method():
    """Demonstrate the Factory Method pattern."""
    print("=== Factory Method Pattern Demo ===")
    
    print("App: Launched with ConcreteCreatorA.")
    client_code(ConcreteCreatorA())
    
    print("\nApp: Launched with ConcreteCreatorB.")
    client_code(ConcreteCreatorB())


def demonstrate_simple_factory():
    """Demonstrate the Simple Factory pattern."""
    print("\n=== Simple Factory Pattern Demo ===")
    
    factory = SimpleFactory()
    
    # Create different products
    for product_type in factory.get_supported_types():
        product = factory.create_product(product_type)
        print(f"Created product {product_type}: {product.operation()}")
    
    # Try to create an unknown product
    try:
        unknown_product = factory.create_product("C")
    except ValueError as e:
        print(f"Error: {e}")


def demonstrate_notification_factory():
    """Demonstrate the Notification Factory pattern."""
    print("\n=== Notification Factory Demo ===")
    
    notifications = [
        ("email", "user@example.com", "Welcome to our service!"),
        ("sms", "+1234567890", "Your verification code is 123456"),
        ("push", "user_device_token", "You have a new message")
    ]
    
    for notif_type, recipient, message in notifications:
        try:
            notifier = NotificationFactory.create_notifier(notif_type)
            notifier.send(recipient, message)
            print()
        except ValueError as e:
            print(f"Error: {e}")


def demonstrate_shape_factory():
    """Demonstrate the Shape Factory pattern."""
    print("\n=== Shape Factory Demo ===")
    
    shapes = [
        ("circle", {"radius": 5}),
        ("rectangle", {"width": 4, "height": 3}),
        ("triangle", {"side": 6})
    ]
    
    for shape_type, params in shapes:
        try:
            shape = ShapeFactory.create_shape(shape_type, **params)
            print(f"{shape_type.title()} {params}: Area = {shape.area():.2f}, "
                  f"Perimeter = {shape.perimeter():.2f}")
        except ValueError as e:
            print(f"Error: {e}")


def demonstrate_abstract_factory():
    """Demonstrate the Abstract Factory pattern."""
    print("\n=== Abstract Factory Demo ===")
    
    platforms = ["windows", "macos"]
    
    for platform in platforms:
        try:
            factory = UIComponentFactory.create_factory(platform)
            button = factory.create_button()
            checkbox = factory.create_checkbox()
            
            print(f"{platform.title()} UI Components:")
            print(f"  Button: {button.paint()}")
            print(f"  Checkbox: {checkbox.paint()}")
            print()
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    demonstrate_factory_method()
    demonstrate_simple_factory()
    demonstrate_notification_factory()
    demonstrate_shape_factory()
    demonstrate_abstract_factory()