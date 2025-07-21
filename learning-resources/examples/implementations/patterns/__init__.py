"""Design patterns implementations.

This package provides clean, documented implementations of common design patterns
with proper type hints and example usage.
"""

# Adapter Pattern
from .adapter import DatabaseConnection, MediaPlayer, PaymentProcessor

# Builder Pattern
from .builder import ComputerBuilder, HouseBuilder, PizzaBuilder

# Command Pattern
from .command import Command, CommandHistory, NoCommand, RemoteControl

# Decorator Pattern
from .decorator import Component, ConcreteComponent, Decorator

# Factory Pattern
from .factory import (
    ConcreteProductA,
    ConcreteProductB,
    NotificationFactory,
    ShapeFactory,
    SimpleFactory,
    UIComponentFactory,
)

# Observer Pattern
from .observer import ConcreteObserver, ConcreteSubject, Observer, Subject

# Repository Pattern
from .repository import InMemoryUserRepository, Repository, UserRepository

# Singleton Pattern
from .singleton import Singleton, ThreadSafeSingleton, singleton

# State Pattern
from .state import MediaPlayer as StateMediaPlayer
from .state import State, TrafficLight, VendingMachine

# Strategy Pattern
from .strategy import Context, PaymentStrategy, SortingStrategy, Strategy

__all__ = [
    # Singleton
    "Singleton",
    "ThreadSafeSingleton",
    "singleton",
    # Factory
    "SimpleFactory",
    "ConcreteProductA",
    "ConcreteProductB",
    "NotificationFactory",
    "ShapeFactory",
    "UIComponentFactory",
    # Observer
    "Observer",
    "Subject",
    "ConcreteObserver",
    "ConcreteSubject",
    # Strategy
    "Strategy",
    "Context",
    "PaymentStrategy",
    "SortingStrategy",
    # Decorator
    "Component",
    "ConcreteComponent",
    "Decorator",
    # Command
    "Command",
    "NoCommand",
    "RemoteControl",
    "CommandHistory",
    # Repository
    "Repository",
    "UserRepository",
    "InMemoryUserRepository",
    # Builder
    "ComputerBuilder",
    "HouseBuilder",
    "PizzaBuilder",
    # Adapter
    "MediaPlayer",
    "DatabaseConnection",
    "PaymentProcessor",
    # State
    "State",
    "VendingMachine",
    "TrafficLight",
    "StateMediaPlayer",
]
