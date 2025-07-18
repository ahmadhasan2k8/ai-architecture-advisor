"""Adapter pattern implementations.

This module provides implementations of the Adapter pattern, demonstrating
how to make incompatible interfaces work together.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


# Target Interface

class MediaPlayer(ABC):
    """Target interface for media players."""
    
    @abstractmethod
    def play(self, audio_type: str, filename: str) -> None:
        """Play audio file.
        
        Args:
            audio_type: Type of audio file
            filename: Name of the file to play
        """
        pass


# Adaptee Classes (Incompatible interfaces)

class Mp3Player:
    """Legacy MP3 player with its own interface."""
    
    def play_mp3(self, filename: str) -> None:
        """Play MP3 file.
        
        Args:
            filename: MP3 file to play
        """
        print(f"Playing MP3 file: {filename}")


class Mp4Player:
    """Legacy MP4 player with its own interface."""
    
    def play_mp4(self, filename: str) -> None:
        """Play MP4 file.
        
        Args:
            filename: MP4 file to play
        """
        print(f"Playing MP4 file: {filename}")


class VlcPlayer:
    """VLC player with its own interface."""
    
    def play_vlc(self, filename: str) -> None:
        """Play VLC file.
        
        Args:
            filename: VLC file to play
        """
        print(f"Playing VLC file: {filename}")


# Adapter Classes

class MediaAdapter(MediaPlayer):
    """Adapter that makes different media players compatible."""
    
    def __init__(self, audio_type: str):
        """Initialize the adapter.
        
        Args:
            audio_type: Type of audio this adapter handles
        """
        self.audio_type = audio_type
        
        if audio_type == "mp3":
            self.player = Mp3Player()
        elif audio_type == "mp4":
            self.player = Mp4Player()
        elif audio_type == "vlc":
            self.player = VlcPlayer()
        else:
            self.player = None
    
    def play(self, audio_type: str, filename: str) -> None:
        """Play audio file using the appropriate player.
        
        Args:
            audio_type: Type of audio file
            filename: Name of the file to play
        """
        if audio_type == "mp3" and hasattr(self.player, 'play_mp3'):
            self.player.play_mp3(filename)
        elif audio_type == "mp4" and hasattr(self.player, 'play_mp4'):
            self.player.play_mp4(filename)
        elif audio_type == "vlc" and hasattr(self.player, 'play_vlc'):
            self.player.play_vlc(filename)
        else:
            print(f"Media format {audio_type} not supported")


class AudioPlayer(MediaPlayer):
    """Audio player that uses adapters for different formats."""
    
    def __init__(self):
        """Initialize the audio player."""
        self.adapters: Dict[str, MediaAdapter] = {}
    
    def play(self, audio_type: str, filename: str) -> None:
        """Play audio file.
        
        Args:
            audio_type: Type of audio file
            filename: Name of the file to play
        """
        audio_type = audio_type.lower()
        
        if audio_type == "mp3":
            # Direct support for MP3
            print(f"Playing MP3 file: {filename}")
        elif audio_type in ["mp4", "vlc"]:
            # Use adapter for other formats
            if audio_type not in self.adapters:
                self.adapters[audio_type] = MediaAdapter(audio_type)
            self.adapters[audio_type].play(audio_type, filename)
        else:
            print(f"Media format {audio_type} not supported")


# Database Adapter Example

class DatabaseConnection(ABC):
    """Target interface for database connections."""
    
    @abstractmethod
    def connect(self) -> None:
        """Connect to the database."""
        pass
    
    @abstractmethod
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the database connection."""
        pass


class MySQLConnection:
    """Legacy MySQL connection class."""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        """Initialize MySQL connection.
        
        Args:
            host: Database host
            user: Username
            password: Password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connected = False
    
    def mysql_connect(self) -> None:
        """Connect to MySQL database."""
        print(f"Connecting to MySQL database {self.database} on {self.host}")
        self.connected = True
    
    def mysql_query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute MySQL query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results
        """
        if not self.connected:
            raise RuntimeError("Not connected to MySQL database")
        
        print(f"Executing MySQL query: {sql}")
        # Simulate results
        return [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
    
    def mysql_disconnect(self) -> None:
        """Disconnect from MySQL database."""
        print("Disconnecting from MySQL database")
        self.connected = False


class PostgreSQLConnection:
    """Legacy PostgreSQL connection class."""
    
    def __init__(self, host: str, user: str, password: str, database: str):
        """Initialize PostgreSQL connection.
        
        Args:
            host: Database host
            user: Username
            password: Password
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connected = False
    
    def pg_connect(self) -> None:
        """Connect to PostgreSQL database."""
        print(f"Connecting to PostgreSQL database {self.database} on {self.host}")
        self.connected = True
    
    def pg_execute(self, sql: str) -> List[Dict[str, Any]]:
        """Execute PostgreSQL query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results
        """
        if not self.connected:
            raise RuntimeError("Not connected to PostgreSQL database")
        
        print(f"Executing PostgreSQL query: {sql}")
        # Simulate results
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    
    def pg_disconnect(self) -> None:
        """Disconnect from PostgreSQL database."""
        print("Disconnecting from PostgreSQL database")
        self.connected = False


class MySQLAdapter(DatabaseConnection):
    """Adapter for MySQL connection."""
    
    def __init__(self, mysql_connection: MySQLConnection):
        """Initialize the adapter.
        
        Args:
            mysql_connection: MySQL connection instance
        """
        self.mysql_connection = mysql_connection
    
    def connect(self) -> None:
        """Connect to the database."""
        self.mysql_connection.mysql_connect()
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results
        """
        return self.mysql_connection.mysql_query(sql)
    
    def close(self) -> None:
        """Close the database connection."""
        self.mysql_connection.mysql_disconnect()


class PostgreSQLAdapter(DatabaseConnection):
    """Adapter for PostgreSQL connection."""
    
    def __init__(self, postgresql_connection: PostgreSQLConnection):
        """Initialize the adapter.
        
        Args:
            postgresql_connection: PostgreSQL connection instance
        """
        self.postgresql_connection = postgresql_connection
    
    def connect(self) -> None:
        """Connect to the database."""
        self.postgresql_connection.pg_connect()
    
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute a query.
        
        Args:
            sql: SQL query string
            
        Returns:
            Query results
        """
        return self.postgresql_connection.pg_execute(sql)
    
    def close(self) -> None:
        """Close the database connection."""
        self.postgresql_connection.pg_disconnect()


# Payment Gateway Adapter Example

class PaymentProcessor(ABC):
    """Target interface for payment processing."""
    
    @abstractmethod
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Process a payment.
        
        Args:
            amount: Payment amount
            card_number: Credit card number
            
        Returns:
            True if payment successful, False otherwise
        """
        pass


class PayPalGateway:
    """Legacy PayPal gateway with its own interface."""
    
    def make_payment(self, amount: float, email: str) -> Dict[str, Any]:
        """Make a PayPal payment.
        
        Args:
            amount: Payment amount
            email: PayPal email
            
        Returns:
            Payment result
        """
        print(f"Processing PayPal payment of ${amount} for {email}")
        return {"status": "success", "transaction_id": "PP123456"}


class StripeGateway:
    """Legacy Stripe gateway with its own interface."""
    
    def charge_card(self, amount_cents: int, token: str) -> Dict[str, Any]:
        """Charge a credit card via Stripe.
        
        Args:
            amount_cents: Amount in cents
            token: Stripe token
            
        Returns:
            Charge result
        """
        print(f"Processing Stripe payment of ${amount_cents/100} with token {token}")
        return {"status": "succeeded", "charge_id": "ch_123456"}


class PayPalAdapter(PaymentProcessor):
    """Adapter for PayPal gateway."""
    
    def __init__(self, paypal_gateway: PayPalGateway, email: str):
        """Initialize the adapter.
        
        Args:
            paypal_gateway: PayPal gateway instance
            email: PayPal email
        """
        self.paypal_gateway = paypal_gateway
        self.email = email
    
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Process a payment via PayPal.
        
        Args:
            amount: Payment amount
            card_number: Credit card number (not used for PayPal)
            
        Returns:
            True if payment successful, False otherwise
        """
        result = self.paypal_gateway.make_payment(amount, self.email)
        return result["status"] == "success"


class StripeAdapter(PaymentProcessor):
    """Adapter for Stripe gateway."""
    
    def __init__(self, stripe_gateway: StripeGateway):
        """Initialize the adapter.
        
        Args:
            stripe_gateway: Stripe gateway instance
        """
        self.stripe_gateway = stripe_gateway
    
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Process a payment via Stripe.
        
        Args:
            amount: Payment amount
            card_number: Credit card number
            
        Returns:
            True if payment successful, False otherwise
        """
        # Convert card number to Stripe token (simplified)
        token = f"tok_{card_number[-4:]}"
        amount_cents = int(amount * 100)
        
        result = self.stripe_gateway.charge_card(amount_cents, token)
        return result["status"] == "succeeded"


# Object Adapter vs Class Adapter

class Rectangle:
    """Rectangle class with its own interface."""
    
    def __init__(self, width: float, height: float):
        """Initialize rectangle.
        
        Args:
            width: Rectangle width
            height: Rectangle height
        """
        self.width = width
        self.height = height
    
    def draw(self, x: int, y: int) -> None:
        """Draw rectangle at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        print(f"Drawing rectangle ({self.width}x{self.height}) at ({x}, {y})")


class LegacyRectangle:
    """Legacy rectangle class with different interface."""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        """Initialize legacy rectangle.
        
        Args:
            x1: Top-left X coordinate
            y1: Top-left Y coordinate
            x2: Bottom-right X coordinate
            y2: Bottom-right Y coordinate
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def old_draw(self) -> None:
        """Draw rectangle using legacy interface."""
        print(f"Drawing legacy rectangle from ({self.x1}, {self.y1}) to ({self.x2}, {self.y2})")


class LegacyRectangleAdapter(Rectangle):
    """Object adapter for legacy rectangle."""
    
    def __init__(self, legacy_rectangle: LegacyRectangle):
        """Initialize the adapter.
        
        Args:
            legacy_rectangle: Legacy rectangle instance
        """
        self.legacy_rectangle = legacy_rectangle
        
        # Calculate width and height from coordinates
        width = abs(legacy_rectangle.x2 - legacy_rectangle.x1)
        height = abs(legacy_rectangle.y2 - legacy_rectangle.y1)
        
        super().__init__(width, height)
    
    def draw(self, x: int, y: int) -> None:
        """Draw rectangle using legacy interface.
        
        Args:
            x: X coordinate
            y: Y coordinate
        """
        # Adapt the interface
        self.legacy_rectangle.x1 = x
        self.legacy_rectangle.y1 = y
        self.legacy_rectangle.x2 = x + self.width
        self.legacy_rectangle.y2 = y + self.height
        
        self.legacy_rectangle.old_draw()


# Service Layer using Multiple Adapters

class PaymentService:
    """Service that can use multiple payment processors."""
    
    def __init__(self):
        """Initialize the payment service."""
        self.processors: Dict[str, PaymentProcessor] = {}
    
    def add_processor(self, name: str, processor: PaymentProcessor) -> None:
        """Add a payment processor.
        
        Args:
            name: Processor name
            processor: Payment processor instance
        """
        self.processors[name] = processor
    
    def process_payment(self, processor_name: str, amount: float, card_number: str) -> bool:
        """Process a payment using specified processor.
        
        Args:
            processor_name: Name of the processor to use
            amount: Payment amount
            card_number: Credit card number
            
        Returns:
            True if payment successful, False otherwise
        """
        if processor_name not in self.processors:
            print(f"Payment processor {processor_name} not available")
            return False
        
        processor = self.processors[processor_name]
        return processor.process_payment(amount, card_number)


# Example usage functions

def demonstrate_media_adapter():
    """Demonstrate media adapter pattern."""
    print("=== Media Adapter Demo ===")
    
    player = AudioPlayer()
    
    # Test different formats
    player.play("mp3", "song.mp3")
    player.play("mp4", "video.mp4")
    player.play("vlc", "movie.vlc")
    player.play("avi", "video.avi")  # Unsupported format


def demonstrate_database_adapter():
    """Demonstrate database adapter pattern."""
    print("\n=== Database Adapter Demo ===")
    
    # MySQL connection
    mysql_conn = MySQLConnection("localhost", "user", "password", "mydb")
    mysql_adapter = MySQLAdapter(mysql_conn)
    
    mysql_adapter.connect()
    results = mysql_adapter.query("SELECT * FROM users")
    print(f"MySQL results: {results}")
    mysql_adapter.close()
    
    # PostgreSQL connection
    pg_conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
    pg_adapter = PostgreSQLAdapter(pg_conn)
    
    pg_adapter.connect()
    results = pg_adapter.query("SELECT * FROM users")
    print(f"PostgreSQL results: {results}")
    pg_adapter.close()


def demonstrate_payment_adapter():
    """Demonstrate payment adapter pattern."""
    print("\n=== Payment Adapter Demo ===")
    
    # Create payment service
    payment_service = PaymentService()
    
    # Add different payment processors via adapters
    paypal_gateway = PayPalGateway()
    paypal_adapter = PayPalAdapter(paypal_gateway, "customer@example.com")
    payment_service.add_processor("paypal", paypal_adapter)
    
    stripe_gateway = StripeGateway()
    stripe_adapter = StripeAdapter(stripe_gateway)
    payment_service.add_processor("stripe", stripe_adapter)
    
    # Process payments
    success = payment_service.process_payment("paypal", 99.99, "1234567890123456")
    print(f"PayPal payment success: {success}")
    
    success = payment_service.process_payment("stripe", 149.99, "1234567890123456")
    print(f"Stripe payment success: {success}")


def demonstrate_rectangle_adapter():
    """Demonstrate rectangle adapter pattern."""
    print("\n=== Rectangle Adapter Demo ===")
    
    # Regular rectangle
    rect = Rectangle(100, 50)
    rect.draw(10, 20)
    
    # Legacy rectangle adapted
    legacy_rect = LegacyRectangle(0, 0, 100, 50)
    adapted_rect = LegacyRectangleAdapter(legacy_rect)
    adapted_rect.draw(10, 20)


if __name__ == "__main__":
    demonstrate_media_adapter()
    demonstrate_database_adapter()
    demonstrate_payment_adapter()
    demonstrate_rectangle_adapter()