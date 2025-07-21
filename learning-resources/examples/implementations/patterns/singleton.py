"""Singleton pattern implementations.

This module provides various implementations of the Singleton pattern,
including thread-safe versions and decorator-based approaches.
"""

import threading
from functools import wraps
from typing import Any, Callable, Dict, Optional, Type, TypeVar

T = TypeVar("T")


class SingletonMeta(type):
    """Metaclass that creates singleton instances.

    This metaclass ensures that only one instance of a class exists
    by storing instances in a class-level dictionary.
    """

    _instances: Dict[Type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        """Control instance creation.

        Args:
            *args: Positional arguments for the class constructor
            **kwargs: Keyword arguments for the class constructor

        Returns:
            The singleton instance of the class
        """
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """Base singleton class using metaclass.

    Classes inheriting from this will automatically be singletons.

    Example:
        >>> class MyClass(Singleton):
        ...     def __init__(self, value):
        ...         self.value = value
        >>> obj1 = MyClass(42)
        >>> obj2 = MyClass(100)
        >>> assert obj1 is obj2
        >>> assert obj1.value == 42  # First initialization wins
    """

    def __init__(self):
        """Initialize the singleton instance."""
        pass


class ThreadSafeSingleton:
    """Thread-safe singleton implementation using __new__.

    This implementation uses double-checked locking to ensure
    thread safety while minimizing synchronization overhead.
    """

    _instance: Optional["ThreadSafeSingleton"] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls) -> "ThreadSafeSingleton":
        """Create or return the singleton instance.

        Returns:
            The singleton instance
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the singleton instance only once."""
        if not hasattr(self, "_initialized"):
            self._initialized = True


def singleton(cls: Type[T]) -> Callable[..., T]:
    """Decorator that transforms a class into a singleton.

    This decorator maintains a single instance of the decorated class
    and returns it for all instantiation attempts.

    Args:
        cls: The class to transform into a singleton

    Returns:
        A wrapper function that manages the singleton instance

    Example:
        >>> @singleton
        ... class Database:
        ...     def __init__(self, host="localhost"):
        ...         self.host = host
        >>> db1 = Database()
        >>> db2 = Database("remote.host")
        >>> assert db1 is db2
        >>> assert db1.host == "localhost"
    """
    instances: Dict[Type, Any] = {}
    lock = threading.Lock()

    @wraps(cls)
    def get_instance(*args, **kwargs) -> T:
        """Get or create the singleton instance.

        Args:
            *args: Positional arguments for the class constructor
            **kwargs: Keyword arguments for the class constructor

        Returns:
            The singleton instance
        """
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


class ResettableSingleton(ThreadSafeSingleton):
    """Singleton that can be reset (useful for testing).

    This implementation allows resetting the singleton instance,
    which is particularly useful in testing scenarios.
    """

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance.

        This method should be used with caution, primarily for testing.
        """
        with cls._lock:
            cls._instance = None


# Example implementations for common use cases


@singleton
class Logger:
    """Singleton logger implementation.

    Provides a global logging facility with a single instance.
    """

    def __init__(self, name: str = "AppLogger"):
        """Initialize the logger.

        Args:
            name: The logger name
        """
        self.name = name
        self.logs: list[tuple[str, str]] = []

    def log(self, level: str, message: str) -> None:
        """Log a message.

        Args:
            level: The log level (e.g., "INFO", "ERROR")
            message: The message to log
        """
        from datetime import datetime

        timestamp = datetime.now().isoformat()
        self.logs.append((f"{timestamp} [{level}]", message))
        print(f"{timestamp} [{level}] {message}")


class ConfigurationManager(Singleton):
    """Singleton configuration manager.

    Manages application configuration with a single global instance.
    """

    def __init__(self):
        """Initialize the configuration manager."""
        super().__init__()
        if not hasattr(self, "_config"):
            self._config: Dict[str, Any] = {}
            self._observers: list[Callable[[str, Any, Any], None]] = []

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: The configuration key
            default: Default value if key not found

        Returns:
            The configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: The configuration key
            value: The value to set
        """
        old_value = self._config.get(key)
        self._config[key] = value

        for observer in self._observers:
            observer(key, old_value, value)

    def subscribe(self, callback: Callable[[str, Any, Any], None]) -> None:
        """Subscribe to configuration changes.

        Args:
            callback: Function called when configuration changes
        """
        self._observers.append(callback)
