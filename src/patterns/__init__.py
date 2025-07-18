"""Design patterns implementations.

This package provides clean, documented implementations of common design patterns
with proper type hints and example usage.
"""

# Singleton Pattern
from .singleton import Singleton, ThreadSafeSingleton, singleton

# Factory Pattern
from .factory import (
    SimpleFactory, ConcreteProductA, ConcreteProductB,
    NotificationFactory, ShapeFactory, UIComponentFactory
)

# Observer Pattern
from .observer import Observer, Subject, ConcreteObserver, ConcreteSubject

# Strategy Pattern
from .strategy import Strategy, Context, PaymentStrategy, SortingStrategy

# Decorator Pattern
from .decorator import Component, ConcreteComponent, Decorator

# Command Pattern
from .command import Command, NoCommand, RemoteControl, CommandHistory

# Repository Pattern
from .repository import Repository, UserRepository, InMemoryUserRepository

# Builder Pattern
from .builder import ComputerBuilder, HouseBuilder, PizzaBuilder

# Adapter Pattern
from .adapter import MediaPlayer, DatabaseConnection, PaymentProcessor

# State Pattern
from .state import State, VendingMachine, TrafficLight, MediaPlayer as StateMediaPlayer

__all__ = [
    # Singleton
    "Singleton", "ThreadSafeSingleton", "singleton",
    
    # Factory
    "SimpleFactory", "ConcreteProductA", "ConcreteProductB",
    "NotificationFactory", "ShapeFactory", "UIComponentFactory",
    
    # Observer
    "Observer", "Subject", "ConcreteObserver", "ConcreteSubject",
    
    # Strategy
    "Strategy", "Context", "PaymentStrategy", "SortingStrategy",
    
    # Decorator
    "Component", "ConcreteComponent", "Decorator",
    
    # Command
    "Command", "NoCommand", "RemoteControl", "CommandHistory",
    
    # Repository
    "Repository", "UserRepository", "InMemoryUserRepository",
    
    # Builder
    "ComputerBuilder", "HouseBuilder", "PizzaBuilder",
    
    # Adapter
    "MediaPlayer", "DatabaseConnection", "PaymentProcessor",
    
    # State
    "State", "VendingMachine", "TrafficLight", "StateMediaPlayer",
]