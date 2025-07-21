"""Decorator pattern implementations.

This module provides implementations of the Decorator pattern, demonstrating
how to add behavior to objects dynamically without altering their structure.
"""

import functools
import re
import time
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


class Component(ABC):
    """Abstract base class for components that can be decorated."""

    @abstractmethod
    def operation(self) -> str:
        """Perform the component's operation.

        Returns:
            Result of the operation
        """
        pass


class ConcreteComponent(Component):
    """Concrete component that provides basic functionality."""

    def operation(self) -> str:
        """Perform the basic operation.

        Returns:
            Result of the basic operation
        """
        return "ConcreteComponent"


class Decorator(Component):
    """Base decorator class that implements the Component interface."""

    def __init__(self, component: Component):
        """Initialize the decorator with a component.

        Args:
            component: The component to be decorated
        """
        self._component = component

    def operation(self) -> str:
        """Delegate the operation to the component.

        Returns:
            Result of the component's operation
        """
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """Concrete decorator that adds behavior A."""

    def operation(self) -> str:
        """Add behavior A to the component's operation.

        Returns:
            Enhanced result with behavior A
        """
        return f"ConcreteDecoratorA({self._component.operation()})"


class ConcreteDecoratorB(Decorator):
    """Concrete decorator that adds behavior B."""

    def operation(self) -> str:
        """Add behavior B to the component's operation.

        Returns:
            Enhanced result with behavior B
        """
        return f"ConcreteDecoratorB({self._component.operation()})"


# Beverage Example


class Beverage(ABC):
    """Abstract base class for beverages."""

    @abstractmethod
    def cost(self) -> float:
        """Calculate the cost of the beverage.

        Returns:
            Cost of the beverage
        """
        pass

    @abstractmethod
    def description(self) -> str:
        """Get the description of the beverage.

        Returns:
            Description of the beverage
        """
        pass


class Coffee(Beverage):
    """Basic coffee implementation."""

    def cost(self) -> float:
        """Get the cost of basic coffee.

        Returns:
            Cost of coffee
        """
        return 5.0

    def description(self) -> str:
        """Get the description of coffee.

        Returns:
            Description of coffee
        """
        return "Simple coffee"


class Tea(Beverage):
    """Basic tea implementation."""

    def cost(self) -> float:
        """Get the cost of basic tea.

        Returns:
            Cost of tea
        """
        return 3.0

    def description(self) -> str:
        """Get the description of tea.

        Returns:
            Description of tea
        """
        return "Simple tea"


class CondimentDecorator(Beverage):
    """Base decorator class for beverage condiments."""

    def __init__(self, beverage: Beverage):
        """Initialize the condiment decorator.

        Args:
            beverage: The beverage to be decorated
        """
        self._beverage = beverage

    def cost(self) -> float:
        """Get the cost of the decorated beverage.

        Returns:
            Cost of the beverage
        """
        return self._beverage.cost()

    def description(self) -> str:
        """Get the description of the decorated beverage.

        Returns:
            Description of the beverage
        """
        return self._beverage.description()


class Milk(CondimentDecorator):
    """Milk condiment decorator."""

    def cost(self) -> float:
        """Add milk cost to the beverage.

        Returns:
            Cost of beverage with milk
        """
        return self._beverage.cost() + 1.0

    def description(self) -> str:
        """Add milk to the beverage description.

        Returns:
            Description with milk
        """
        return self._beverage.description() + ", milk"


class Sugar(CondimentDecorator):
    """Sugar condiment decorator."""

    def cost(self) -> float:
        """Add sugar cost to the beverage.

        Returns:
            Cost of beverage with sugar
        """
        return self._beverage.cost() + 0.5

    def description(self) -> str:
        """Add sugar to the beverage description.

        Returns:
            Description with sugar
        """
        return self._beverage.description() + ", sugar"


class WhipCream(CondimentDecorator):
    """Whip cream condiment decorator."""

    def cost(self) -> float:
        """Add whip cream cost to the beverage.

        Returns:
            Cost of beverage with whip cream
        """
        return self._beverage.cost() + 1.5

    def description(self) -> str:
        """Add whip cream to the beverage description.

        Returns:
            Description with whip cream
        """
        return self._beverage.description() + ", whip cream"


class Cinnamon(CondimentDecorator):
    """Cinnamon condiment decorator."""

    def cost(self) -> float:
        """Add cinnamon cost to the beverage.

        Returns:
            Cost of beverage with cinnamon
        """
        return self._beverage.cost() + 0.3

    def description(self) -> str:
        """Add cinnamon to the beverage description.

        Returns:
            Description with cinnamon
        """
        return self._beverage.description() + ", cinnamon"


class Vanilla(CondimentDecorator):
    """Vanilla condiment decorator."""

    def cost(self) -> float:
        """Add vanilla cost to the beverage.

        Returns:
            Cost of beverage with vanilla
        """
        return self._beverage.cost() + 0.7

    def description(self) -> str:
        """Add vanilla to the beverage description.

        Returns:
            Description with vanilla
        """
        return self._beverage.description() + ", vanilla"


# Text Processing Example


class TextProcessor(ABC):
    """Abstract base class for text processors."""

    @abstractmethod
    def process(self, text: str) -> str:
        """Process the text.

        Args:
            text: Text to process

        Returns:
            Processed text
        """
        pass


class PlainText(TextProcessor):
    """Plain text processor that returns text as-is."""

    def process(self, text: str) -> str:
        """Return text without processing.

        Args:
            text: Text to process

        Returns:
            Unprocessed text
        """
        return text


class TextDecorator(TextProcessor):
    """Base decorator class for text processing."""

    def __init__(self, processor: TextProcessor):
        """Initialize the text decorator.

        Args:
            processor: The text processor to be decorated
        """
        self._processor = processor

    def process(self, text: str) -> str:
        """Process text using the decorated processor.

        Args:
            text: Text to process

        Returns:
            Processed text
        """
        return self._processor.process(text)


class UppercaseDecorator(TextDecorator):
    """Decorator that converts text to uppercase."""

    def process(self, text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: Text to process

        Returns:
            Uppercase text
        """
        return self._processor.process(text).upper()


class LowercaseDecorator(TextDecorator):
    """Decorator that converts text to lowercase."""

    def process(self, text: str) -> str:
        """Convert text to lowercase.

        Args:
            text: Text to process

        Returns:
            Lowercase text
        """
        return self._processor.process(text).lower()


class TrimDecorator(TextDecorator):
    """Decorator that trims whitespace from text."""

    def process(self, text: str) -> str:
        """Trim whitespace from text.

        Args:
            text: Text to process

        Returns:
            Trimmed text
        """
        return self._processor.process(text).strip()


class RemoveExtraSpacesDecorator(TextDecorator):
    """Decorator that removes extra spaces from text."""

    def process(self, text: str) -> str:
        """Remove extra spaces from text.

        Args:
            text: Text to process

        Returns:
            Text with extra spaces removed
        """
        processed = self._processor.process(text)
        return re.sub(r"\s+", " ", processed)


class CensorDecorator(TextDecorator):
    """Decorator that censors specified words in text."""

    def __init__(self, processor: TextProcessor, words_to_censor: List[str]):
        """Initialize the censor decorator.

        Args:
            processor: The text processor to be decorated
            words_to_censor: List of words to censor
        """
        super().__init__(processor)
        self.words_to_censor = words_to_censor

    def process(self, text: str) -> str:
        """Censor specified words in text.

        Args:
            text: Text to process

        Returns:
            Text with censored words
        """
        processed = self._processor.process(text)
        for word in self.words_to_censor:
            processed = processed.replace(word, "*" * len(word))
        return processed


class ReverseDecorator(TextDecorator):
    """Decorator that reverses text."""

    def process(self, text: str) -> str:
        """Reverse the text.

        Args:
            text: Text to process

        Returns:
            Reversed text
        """
        return self._processor.process(text)[::-1]


class PrefixDecorator(TextDecorator):
    """Decorator that adds a prefix to text."""

    def __init__(self, processor: TextProcessor, prefix: str):
        """Initialize the prefix decorator.

        Args:
            processor: The text processor to be decorated
            prefix: Prefix to add
        """
        super().__init__(processor)
        self.prefix = prefix

    def process(self, text: str) -> str:
        """Add prefix to text.

        Args:
            text: Text to process

        Returns:
            Text with prefix
        """
        processed = self._processor.process(text)
        return f"{self.prefix}{processed}"


class SuffixDecorator(TextDecorator):
    """Decorator that adds a suffix to text."""

    def __init__(self, processor: TextProcessor, suffix: str):
        """Initialize the suffix decorator.

        Args:
            processor: The text processor to be decorated
            suffix: Suffix to add
        """
        super().__init__(processor)
        self.suffix = suffix

    def process(self, text: str) -> str:
        """Add suffix to text.

        Args:
            text: Text to process

        Returns:
            Text with suffix
        """
        processed = self._processor.process(text)
        return f"{processed}{self.suffix}"


# Function Decorators


def timer(func: F) -> F:
    """Decorator that measures execution time of a function.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result

    return wrapper


def logger(func: F) -> F:
    """Decorator that logs function calls.

    Args:
        func: Function to decorate

    Returns:
        Decorated function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator that retries a function on failure.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds

    Returns:
        Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        print(
                            f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    else:
                        print(f"All {max_attempts} attempts failed.")

            raise last_exception

        return wrapper

    return decorator


def cache(func: F) -> F:
    """Decorator that caches function results.

    Args:
        func: Function to decorate

    Returns:
        Decorated function with caching
    """
    cache_dict = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a cache key from arguments
        key = str(args) + str(sorted(kwargs.items()))

        if key in cache_dict:
            print(f"Cache hit for {func.__name__}")
            return cache_dict[key]

        print(f"Cache miss for {func.__name__}")
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result

    return wrapper


def validate_types(**type_checks):
    """Decorator that validates function argument types.

    Args:
        **type_checks: Keyword arguments mapping parameter names to expected types

    Returns:
        Decorator function
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate types
            for param_name, expected_type in type_checks.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Parameter '{param_name}' must be of type {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# Class-based Decorator


class RateLimiter:
    """Class-based decorator that implements rate limiting."""

    def __init__(self, max_calls: int, time_window: float):
        """Initialize the rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []

    def __call__(self, func: F) -> F:
        """Make the instance callable as a decorator.

        Args:
            func: Function to decorate

        Returns:
            Decorated function
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()

            # Remove old calls outside the time window
            self.calls = [
                call_time
                for call_time in self.calls
                if current_time - call_time < self.time_window
            ]

            # Check if we've exceeded the rate limit
            if len(self.calls) >= self.max_calls:
                raise Exception(
                    f"Rate limit exceeded: {self.max_calls} calls per {self.time_window} seconds"
                )

            # Record this call
            self.calls.append(current_time)

            return func(*args, **kwargs)

        return wrapper


# Example usage functions


def demonstrate_basic_decorator():
    """Demonstrate basic decorator pattern."""
    print("=== Basic Decorator Pattern Demo ===")

    # Create a simple component
    component = ConcreteComponent()
    print(f"Simple component: {component.operation()}")

    # Decorate it
    decorated = ConcreteDecoratorA(component)
    print(f"Decorated with A: {decorated.operation()}")

    # Decorate with multiple decorators
    double_decorated = ConcreteDecoratorB(decorated)
    print(f"Decorated with A and B: {double_decorated.operation()}")


def demonstrate_beverage_decorator():
    """Demonstrate beverage decorator pattern."""
    print("\n=== Beverage Decorator Demo ===")

    # Simple coffee
    coffee = Coffee()
    print(f"{coffee.description()}: ${coffee.cost():.2f}")

    # Coffee with milk
    coffee_with_milk = Milk(coffee)
    print(f"{coffee_with_milk.description()}: ${coffee_with_milk.cost():.2f}")

    # Coffee with milk and sugar
    coffee_with_milk_and_sugar = Sugar(coffee_with_milk)
    print(
        f"{coffee_with_milk_and_sugar.description()}: ${coffee_with_milk_and_sugar.cost():.2f}"
    )

    # Complex beverage
    complex_beverage = WhipCream(Vanilla(Cinnamon(Sugar(Milk(Coffee())))))
    print(f"{complex_beverage.description()}: ${complex_beverage.cost():.2f}")

    # Tea with different condiments
    tea = Tea()
    fancy_tea = Cinnamon(Sugar(Milk(tea)))
    print(f"{fancy_tea.description()}: ${fancy_tea.cost():.2f}")


def demonstrate_text_processor():
    """Demonstrate text processor decorator pattern."""
    print("\n=== Text Processor Demo ===")

    text = "  Hello   World!  This is a BAD  example.  "
    print(f"Original: '{text}'")

    # Build a processing pipeline
    processor = PlainText()
    processor = TrimDecorator(processor)
    processor = RemoveExtraSpacesDecorator(processor)
    processor = CensorDecorator(processor, ["BAD", "bad"])
    processor = UppercaseDecorator(processor)

    result = processor.process(text)
    print(f"Processed: '{result}'")

    # Different pipeline
    processor2 = PlainText()
    processor2 = PrefixDecorator(processor2, ">>> ")
    processor2 = SuffixDecorator(processor2, " <<<")
    processor2 = TrimDecorator(processor2)

    result2 = processor2.process("Hello World")
    print(f"With prefix/suffix: '{result2}'")


def demonstrate_function_decorators():
    """Demonstrate function decorators."""
    print("\n=== Function Decorators Demo ===")

    @timer
    @logger
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    # This will be slow due to no caching
    print("Without caching:")
    result = fibonacci(10)
    print(f"Fibonacci(10) = {result}")

    # Now with caching
    @cache
    @timer
    def fibonacci_cached(n):
        if n <= 1:
            return n
        return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

    print("\nWith caching:")
    result = fibonacci_cached(10)
    print(f"Fibonacci(10) = {result}")

    # Demonstrate retry decorator
    @retry(max_attempts=3, delay=0.1)
    def unreliable_function():
        import random

        if random.random() < 0.7:  # 70% chance of failure
            raise Exception("Random failure")
        return "Success!"

    print("\nTesting retry decorator:")
    try:
        result = unreliable_function()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final failure: {e}")

    # Demonstrate type validation
    @validate_types(name=str, age=int)
    def greet_person(name, age):
        return f"Hello {name}, you are {age} years old"

    print("\nTesting type validation:")
    try:
        result = greet_person("Alice", 25)
        print(result)
        # This will raise a TypeError
        greet_person("Bob", "thirty")
    except TypeError as e:
        print(f"Type error: {e}")


def demonstrate_rate_limiter():
    """Demonstrate rate limiter decorator."""
    print("\n=== Rate Limiter Demo ===")

    @RateLimiter(max_calls=3, time_window=2.0)
    def api_call(data):
        return f"Processing {data}"

    # This should work for the first 3 calls
    for i in range(5):
        try:
            result = api_call(f"request_{i}")
            print(f"Call {i}: {result}")
            time.sleep(0.1)
        except Exception as e:
            print(f"Call {i}: {e}")


if __name__ == "__main__":
    demonstrate_basic_decorator()
    demonstrate_beverage_decorator()
    demonstrate_text_processor()
    demonstrate_function_decorators()
    demonstrate_rate_limiter()
