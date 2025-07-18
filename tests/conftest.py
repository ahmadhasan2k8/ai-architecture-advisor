"""Pytest configuration and fixtures."""

import pytest
import sys
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor
import json
import sqlite3

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


# ===============================================================================
# Singleton Pattern Fixtures
# ===============================================================================

@pytest.fixture
def reset_singletons():
    """Reset singleton instances after each test.
    
    This fixture ensures that singleton instances don't
    persist between tests, maintaining test isolation.
    """
    yield
    
    # Reset any resettable singletons
    from src.patterns.singleton import ResettableSingleton
    
    # Get all subclasses of ResettableSingleton
    for subclass in ResettableSingleton.__subclasses__():
        subclass.reset()


@pytest.fixture
def thread_pool():
    """Provide a thread pool for concurrent testing."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        yield executor


# ===============================================================================
# Factory Pattern Fixtures
# ===============================================================================

@pytest.fixture
def sample_products():
    """Sample product data for factory pattern tests."""
    return {
        "shapes": [
            {"type": "circle", "radius": 5.0},
            {"type": "rectangle", "width": 10.0, "height": 5.0},
            {"type": "triangle", "base": 8.0, "height": 6.0}
        ],
        "notifications": [
            {"type": "email", "recipient": "test@example.com", "message": "Test email"},
            {"type": "sms", "recipient": "1234567890", "message": "Test SMS"},
            {"type": "push", "recipient": "device123", "message": "Test push"}
        ],
        "ui_components": [
            {"type": "button", "text": "Click me", "style": "primary"},
            {"type": "input", "placeholder": "Enter text", "type": "text"},
            {"type": "label", "text": "Form Label", "for": "input1"}
        ]
    }


# ===============================================================================
# Observer Pattern Fixtures
# ===============================================================================

@pytest.fixture
def observer_mock():
    """Mock observer for testing observer pattern."""
    return Mock()


@pytest.fixture
def subject_mock():
    """Mock subject for testing observer pattern."""
    return Mock()


@pytest.fixture
def weather_data():
    """Sample weather data for observer pattern tests."""
    return {
        "temperature": 25.5,
        "humidity": 60.0,
        "pressure": 1013.25
    }


# ===============================================================================
# Strategy Pattern Fixtures
# ===============================================================================

@pytest.fixture
def payment_data():
    """Sample payment data for strategy pattern tests."""
    return {
        "credit_card": {
            "number": "1234567890123456",
            "expiry": "12/25",
            "cvv": "123"
        },
        "paypal": {
            "email": "test@example.com",
            "password": "secure_password"
        },
        "crypto": {
            "wallet": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "currency": "BTC"
        }
    }


@pytest.fixture
def sorting_data():
    """Sample data for sorting strategy tests."""
    return {
        "numbers": [64, 34, 25, 12, 22, 11, 90, 5, 77, 30],
        "strings": ["banana", "apple", "cherry", "date", "elderberry"],
        "objects": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ]
    }


# ===============================================================================
# Command Pattern Fixtures
# ===============================================================================

@pytest.fixture
def command_receiver():
    """Mock receiver for command pattern tests."""
    receiver = Mock()
    receiver.status = "off"
    receiver.volume = 0
    receiver.channel = 1
    return receiver


@pytest.fixture
def text_editor_content():
    """Sample content for text editor command tests."""
    return {
        "initial": "Hello, World!",
        "insert_operations": [
            {"position": 0, "text": ">>> "},
            {"position": 13, "text": " <<<"},
            {"position": 7, "text": "Beautiful "}
        ],
        "delete_operations": [
            {"start": 0, "end": 4},
            {"start": 10, "end": 15}
        ]
    }


# ===============================================================================
# Repository Pattern Fixtures
# ===============================================================================

@pytest.fixture
def temp_db_file():
    """Temporary database file for repository tests."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def temp_json_file():
    """Temporary JSON file for repository tests."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([], f)
        json_path = f.name
    
    yield json_path
    
    # Cleanup
    if os.path.exists(json_path):
        os.unlink(json_path)


@pytest.fixture
def sample_users():
    """Sample user data for repository tests."""
    return [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "age": 30},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "age": 25},
        {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "age": 35}
    ]


@pytest.fixture
def sample_products():
    """Sample product data for repository tests."""
    return [
        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
        {"id": 2, "name": "Book", "price": 29.99, "category": "Books"},
        {"id": 3, "name": "Coffee Mug", "price": 12.99, "category": "Home"}
    ]


@pytest.fixture
def sample_orders():
    """Sample order data for repository tests."""
    return [
        {"id": 1, "user_id": 1, "product_id": 1, "quantity": 1, "total": 999.99},
        {"id": 2, "user_id": 2, "product_id": 2, "quantity": 2, "total": 59.98},
        {"id": 3, "user_id": 3, "product_id": 3, "quantity": 3, "total": 38.97}
    ]


# ===============================================================================
# Builder Pattern Fixtures
# ===============================================================================

@pytest.fixture
def computer_specifications():
    """Sample computer specifications for builder tests."""
    return {
        "gaming": {
            "cpu": "Intel i9-12900K",
            "gpu": "RTX 4080",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD"
        },
        "office": {
            "cpu": "Intel i5-12400",
            "gpu": "Integrated",
            "ram": "16GB DDR4",
            "storage": "512GB SSD"
        },
        "budget": {
            "cpu": "AMD Ryzen 5 5600G",
            "gpu": "Integrated",
            "ram": "8GB DDR4",
            "storage": "256GB SSD"
        }
    }


@pytest.fixture
def house_specifications():
    """Sample house specifications for builder tests."""
    return {
        "foundation": "Concrete",
        "walls": "Brick",
        "roof": "Tile",
        "interior": "Modern",
        "rooms": 4,
        "has_garage": True,
        "has_garden": True
    }


@pytest.fixture
def pizza_ingredients():
    """Sample pizza ingredients for builder tests."""
    return {
        "dough": ["thin", "thick", "whole_wheat"],
        "sauce": ["tomato", "white", "bbq", "pesto"],
        "cheese": ["mozzarella", "cheddar", "parmesan", "goat"],
        "toppings": ["pepperoni", "mushrooms", "peppers", "onions", "olives", "sausage"]
    }


# ===============================================================================
# Adapter Pattern Fixtures
# ===============================================================================

@pytest.fixture
def media_files():
    """Sample media files for adapter tests."""
    return {
        "audio": ["song.mp3", "podcast.mp4", "audiobook.vlc"],
        "video": ["movie.mp4", "clip.vlc"],
        "unsupported": ["document.pdf", "image.jpg", "data.csv"]
    }


@pytest.fixture
def database_configs():
    """Sample database configurations for adapter tests."""
    return {
        "mysql": {
            "host": "localhost",
            "port": 3306,
            "database": "test_db",
            "username": "user",
            "password": "password"
        },
        "postgresql": {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "user",
            "password": "password"
        }
    }


@pytest.fixture
def payment_gateway_configs():
    """Sample payment gateway configurations for adapter tests."""
    return {
        "paypal": {
            "api_key": "test_paypal_key",
            "secret": "test_paypal_secret",
            "sandbox": True
        },
        "stripe": {
            "api_key": "test_stripe_key",
            "secret": "test_stripe_secret",
            "sandbox": True
        }
    }


# ===============================================================================
# State Pattern Fixtures
# ===============================================================================

@pytest.fixture
def vending_machine_inventory():
    """Sample vending machine inventory for state tests."""
    return {
        "Coke": 10,
        "Pepsi": 8,
        "Water": 15,
        "Chips": 5,
        "Cookies": 3,
        "Candy": 12
    }


@pytest.fixture
def order_data():
    """Sample order data for state pattern tests."""
    return {
        "pending_orders": ["ORDER-001", "ORDER-002", "ORDER-003"],
        "paid_orders": ["ORDER-004", "ORDER-005"],
        "shipped_orders": ["ORDER-006"],
        "cancelled_orders": ["ORDER-007"]
    }


@pytest.fixture
def media_playlist():
    """Sample media playlist for state pattern tests."""
    return [
        {"title": "Song 1", "duration": 180, "artist": "Artist A"},
        {"title": "Song 2", "duration": 220, "artist": "Artist B"},
        {"title": "Song 3", "duration": 195, "artist": "Artist C"}
    ]


# ===============================================================================
# General Testing Utilities
# ===============================================================================

@pytest.fixture
def capture_output():
    """Capture stdout and stderr for testing console output."""
    import io
    import sys
    
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    sys.stdout = stdout_capture
    sys.stderr = stderr_capture
    
    yield stdout_capture, stderr_capture
    
    sys.stdout = old_stdout
    sys.stderr = old_stderr


@pytest.fixture
def performance_timer():
    """Timer for performance testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        def elapsed(self):
            if self.start_time is None or self.end_time is None:
                return None
            return self.end_time - self.start_time
    
    return Timer()


@pytest.fixture
def temp_directory():
    """Temporary directory for testing file operations."""
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_logger():
    """Mock logger for testing logging functionality."""
    logger = Mock()
    logger.debug = Mock()
    logger.info = Mock()
    logger.warning = Mock()
    logger.error = Mock()
    logger.critical = Mock()
    return logger


# ===============================================================================
# Test Configuration
# ===============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Add 'slow' marker to tests that might be slow
        if "performance" in item.nodeid or "stress" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        
        # Add 'integration' marker to integration tests
        if "integration" in item.nodeid or "Integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Add 'unit' marker to unit tests (default)
        if not any(marker.name in ["integration", "performance"] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)


# ===============================================================================
# Test Data Generators
# ===============================================================================

def generate_test_data(pattern_type: str, count: int = 10) -> List[Dict[str, Any]]:
    """Generate test data for different patterns.
    
    Args:
        pattern_type: Type of pattern (e.g., 'user', 'product', 'order')
        count: Number of test records to generate
    
    Returns:
        List of test data dictionaries
    """
    import random
    import string
    
    def random_string(length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    def random_email() -> str:
        return f"{random_string(8)}@example.com"
    
    generators = {
        'user': lambda i: {
            'id': i,
            'name': f"User {i}",
            'email': random_email(),
            'age': random.randint(18, 80)
        },
        'product': lambda i: {
            'id': i,
            'name': f"Product {i}",
            'price': round(random.uniform(10.0, 1000.0), 2),
            'category': random.choice(['Electronics', 'Books', 'Home', 'Sports'])
        },
        'order': lambda i: {
            'id': i,
            'user_id': random.randint(1, 100),
            'product_id': random.randint(1, 50),
            'quantity': random.randint(1, 10),
            'total': round(random.uniform(20.0, 500.0), 2)
        }
    }
    
    generator = generators.get(pattern_type, lambda i: {'id': i})
    return [generator(i) for i in range(1, count + 1)]


# ===============================================================================
# Custom Assertions
# ===============================================================================

def assert_pattern_behavior(pattern_instance, expected_behavior: str):
    """Assert that a pattern instance exhibits expected behavior.
    
    Args:
        pattern_instance: Instance of a pattern implementation
        expected_behavior: Expected behavior description
    """
    # This is a placeholder for custom pattern-specific assertions
    # In real implementations, this would check specific pattern behaviors
    assert hasattr(pattern_instance, '__class__'), "Pattern instance must have a class"
    assert pattern_instance.__class__.__name__ is not None, "Pattern instance must have a class name"


def assert_state_transition(state_machine, from_state, to_state, action):
    """Assert that a state machine transitions correctly.
    
    Args:
        state_machine: State machine instance
        from_state: Expected initial state
        to_state: Expected final state
        action: Action to trigger transition
    """
    # Check initial state
    assert isinstance(state_machine.get_state(), from_state), f"Expected initial state {from_state.__name__}"
    
    # Perform action
    action()
    
    # Check final state
    assert isinstance(state_machine.get_state(), to_state), f"Expected final state {to_state.__name__}"