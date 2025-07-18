"""Tests for singleton pattern implementations."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

import pytest

from src.patterns.singleton import (
    ConfigurationManager,
    Logger,
    ResettableSingleton,
    Singleton,
    SingletonMeta,
    ThreadSafeSingleton,
    singleton,
)


class TestSingletonMeta:
    """Test the SingletonMeta metaclass implementation."""
    
    def test_singleton_instance(self):
        """Test that only one instance is created."""
        
        class TestClass(metaclass=SingletonMeta):
            def __init__(self, value: int):
                self.value = value
        
        obj1 = TestClass(42)
        obj2 = TestClass(100)
        
        assert obj1 is obj2
        assert obj1.value == 42  # First initialization wins
    
    def test_singleton_inheritance(self):
        """Test singleton behavior with inheritance."""
        
        class Base(metaclass=SingletonMeta):
            def __init__(self):
                self.name = "Base"
        
        class Child(Base):
            def __init__(self):
                super().__init__()
                self.name = "Child"
        
        base1 = Base()
        base2 = Base()
        child1 = Child()
        child2 = Child()
        
        assert base1 is base2
        assert child1 is child2
        assert base1 is not child1  # Different classes have different instances


class TestSingletonBase:
    """Test the Singleton base class."""
    
    def test_singleton_base_class(self):
        """Test classes inheriting from Singleton."""
        
        class MyService(Singleton):
            def __init__(self):
                super().__init__()
                if not hasattr(self, "initialized"):
                    self.initialized = True
                    self.counter = 0
            
            def increment(self) -> int:
                self.counter += 1
                return self.counter
        
        service1 = MyService()
        service2 = MyService()
        
        assert service1 is service2
        assert service1.increment() == 1
        assert service2.increment() == 2


class TestThreadSafeSingleton:
    """Test the ThreadSafeSingleton implementation."""
    
    def test_thread_safe_singleton(self):
        """Test basic thread-safe singleton functionality."""
        
        class Counter(ThreadSafeSingleton):
            def __init__(self):
                super().__init__()
                if not hasattr(self, "value"):
                    self.value = 0
        
        counter1 = Counter()
        counter2 = Counter()
        
        assert counter1 is counter2
        assert counter1.value == 0
    
    def test_concurrent_access(self, thread_pool):
        """Test thread safety under concurrent access."""
        
        class SharedResource(ThreadSafeSingleton):
            def __init__(self):
                super().__init__()
                if not hasattr(self, "counter"):
                    self.counter = 0
                    self.lock = threading.Lock()
            
            def increment(self):
                with self.lock:
                    current = self.counter
                    time.sleep(0.001)  # Simulate some processing
                    self.counter = current + 1
        
        resource = SharedResource()
        
        def worker():
            for _ in range(10):
                resource.increment()
        
        # Run multiple workers concurrently
        futures = [thread_pool.submit(worker) for _ in range(10)]
        for future in futures:
            future.result()
        
        # Should have exactly 100 increments (10 workers × 10 increments)
        assert resource.counter == 100


class TestSingletonDecorator:
    """Test the singleton decorator implementation."""
    
    def test_decorator_singleton(self):
        """Test basic decorator functionality."""
        
        @singleton
        class Database:
            def __init__(self, host: str = "localhost"):
                self.host = host
                self.connected = False
            
            def connect(self):
                self.connected = True
        
        db1 = Database()
        db2 = Database("remote.server")  # Different args ignored
        
        assert db1 is db2
        assert db1.host == "localhost"
        
        db1.connect()
        assert db2.connected is True
    
    def test_decorator_with_different_classes(self):
        """Test decorator with multiple classes."""
        
        @singleton
        class ServiceA:
            def __init__(self):
                self.name = "A"
        
        @singleton
        class ServiceB:
            def __init__(self):
                self.name = "B"
        
        a1 = ServiceA()
        a2 = ServiceA()
        b1 = ServiceB()
        b2 = ServiceB()
        
        assert a1 is a2
        assert b1 is b2
        assert a1 is not b1


class TestResettableSingleton:
    """Test the ResettableSingleton implementation."""
    
    def test_resettable_singleton(self, reset_singletons):
        """Test singleton reset functionality."""
        
        class TestService(ResettableSingleton):
            def __init__(self):
                super().__init__()
                if not hasattr(self, "value"):
                    self.value = "initial"
        
        # Create first instance
        service1 = TestService()
        service1.value = "modified"
        
        # Create second instance - should be same
        service2 = TestService()
        assert service1 is service2
        assert service2.value == "modified"
        
        # Reset and create new instance
        TestService.reset()
        service3 = TestService()
        assert service3 is not service1
        assert service3.value == "initial"


class TestPracticalExamples:
    """Test practical singleton implementations."""
    
    def test_logger_singleton(self):
        """Test the Logger singleton."""
        logger1 = Logger("AppLogger")
        logger2 = Logger("DifferentLogger")  # Name ignored
        
        assert logger1 is logger2
        assert logger1.name == "AppLogger"
        
        logger1.log("INFO", "Test message")
        assert len(logger2.logs) == 1
        assert logger2.logs[0][1] == "Test message"
    
    def test_configuration_manager(self):
        """Test the ConfigurationManager singleton."""
        config1 = ConfigurationManager()
        config2 = ConfigurationManager()
        
        assert config1 is config2
        
        # Test basic get/set
        config1.set("debug", True)
        assert config2.get("debug") is True
        
        # Test observer pattern
        changes: List[tuple] = []
        
        def on_change(key: str, old_value, new_value):
            changes.append((key, old_value, new_value))
        
        config1.subscribe(on_change)
        config2.set("debug", False)
        
        assert len(changes) == 1
        assert changes[0] == ("debug", True, False)


class TestSingletonEdgeCases:
    """Test edge cases and potential issues."""
    
    def test_singleton_with_init_exception(self):
        """Test behavior when __init__ raises an exception."""
        
        @singleton
        class FaultyService:
            def __init__(self):
                if not hasattr(self, "initialized"):
                    self.initialized = True
                    raise ValueError("Initialization failed")
        
        with pytest.raises(ValueError):
            FaultyService()
        
        # Subsequent attempts should raise the same error
        with pytest.raises(ValueError):
            FaultyService()
    
    def test_singleton_serialization(self):
        """Test singleton behavior with serialization."""
        import pickle
        
        @singleton
        class SerializableService:
            def __init__(self):
                self.data = "test"
        
        service1 = SerializableService()
        service1.data = "modified"
        
        # Serialize and deserialize
        serialized = pickle.dumps(service1)
        service2 = pickle.loads(serialized)
        
        # Note: Deserialized object is NOT the same singleton instance
        # This is a known limitation of the singleton pattern
        assert service2 is not service1
        assert service2.data == "modified"


class TestPerformance:
    """Test performance characteristics of singleton implementations."""
    
    def test_singleton_creation_performance(self):
        """Test that singleton creation is efficient."""
        import time
        
        @singleton
        class ExpensiveService:
            def __init__(self):
                time.sleep(0.1)  # Simulate expensive initialization
                self.initialized = True
        
        start = time.time()
        service1 = ExpensiveService()
        first_creation = time.time() - start
        
        start = time.time()
        service2 = ExpensiveService()
        second_creation = time.time() - start
        
        assert service1 is service2
        assert first_creation > 0.09  # Should take ~0.1 seconds
        assert second_creation < 0.01  # Should be almost instant