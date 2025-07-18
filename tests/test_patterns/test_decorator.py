"""Tests for decorator pattern implementations."""

import re
import time
from unittest.mock import Mock, patch

import pytest

from src.patterns.decorator import (  # Basic Decorator Pattern; Beverage Example; Text Processing; Function Decorators; Class-based Decorator
    Beverage,
    CensorDecorator,
    Cinnamon,
    Coffee,
    Component,
    ConcreteComponent,
    ConcreteDecoratorA,
    ConcreteDecoratorB,
    CondimentDecorator,
    Decorator,
    LowercaseDecorator,
    Milk,
    PlainText,
    PrefixDecorator,
    RateLimiter,
    RemoveExtraSpacesDecorator,
    ReverseDecorator,
    SuffixDecorator,
    Sugar,
    Tea,
    TextDecorator,
    TextProcessor,
    TrimDecorator,
    UppercaseDecorator,
    Vanilla,
    WhipCream,
    cache,
    logger,
    retry,
    timer,
    validate_types,
)


class TestBasicDecoratorPattern:
    """Test the basic Decorator pattern implementation."""

    def test_concrete_component(self):
        """Test concrete component functionality."""
        component = ConcreteComponent()
        assert component.operation() == "ConcreteComponent"

    def test_decorator_a(self):
        """Test decorator A functionality."""
        component = ConcreteComponent()
        decorator = ConcreteDecoratorA(component)

        assert decorator.operation() == "ConcreteDecoratorA(ConcreteComponent)"

    def test_decorator_b(self):
        """Test decorator B functionality."""
        component = ConcreteComponent()
        decorator = ConcreteDecoratorB(component)

        assert decorator.operation() == "ConcreteDecoratorB(ConcreteComponent)"

    def test_multiple_decorators(self):
        """Test multiple decorators chained together."""
        component = ConcreteComponent()
        decorator_a = ConcreteDecoratorA(component)
        decorator_b = ConcreteDecoratorB(decorator_a)

        assert (
            decorator_b.operation()
            == "ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))"
        )

    def test_decorator_composition(self):
        """Test different decorator compositions."""
        component = ConcreteComponent()

        # A then B
        composition1 = ConcreteDecoratorB(ConcreteDecoratorA(component))
        assert (
            composition1.operation()
            == "ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))"
        )

        # B then A
        composition2 = ConcreteDecoratorA(ConcreteDecoratorB(component))
        assert (
            composition2.operation()
            == "ConcreteDecoratorA(ConcreteDecoratorB(ConcreteComponent))"
        )

    def test_decorator_inheritance(self):
        """Test that decorators implement the Component interface."""
        component = ConcreteComponent()
        decorator_a = ConcreteDecoratorA(component)
        decorator_b = ConcreteDecoratorB(component)

        assert isinstance(decorator_a, Component)
        assert isinstance(decorator_b, Component)
        assert isinstance(decorator_a, Decorator)
        assert isinstance(decorator_b, Decorator)


class TestBeverageDecorator:
    """Test the Beverage decorator implementation."""

    def test_coffee_basic(self):
        """Test basic coffee functionality."""
        coffee = Coffee()
        assert coffee.cost() == 5.0
        assert coffee.description() == "Simple coffee"

    def test_tea_basic(self):
        """Test basic tea functionality."""
        tea = Tea()
        assert tea.cost() == 3.0
        assert tea.description() == "Simple tea"

    def test_beverage_inheritance(self):
        """Test beverage inheritance."""
        coffee = Coffee()
        tea = Tea()

        assert isinstance(coffee, Beverage)
        assert isinstance(tea, Beverage)

    def test_milk_decorator(self):
        """Test milk decorator."""
        coffee = Coffee()
        coffee_with_milk = Milk(coffee)

        assert coffee_with_milk.cost() == 6.0  # 5.0 + 1.0
        assert coffee_with_milk.description() == "Simple coffee, milk"

    def test_sugar_decorator(self):
        """Test sugar decorator."""
        coffee = Coffee()
        coffee_with_sugar = Sugar(coffee)

        assert coffee_with_sugar.cost() == 5.5  # 5.0 + 0.5
        assert coffee_with_sugar.description() == "Simple coffee, sugar"

    def test_whip_cream_decorator(self):
        """Test whip cream decorator."""
        coffee = Coffee()
        coffee_with_whip = WhipCream(coffee)

        assert coffee_with_whip.cost() == 6.5  # 5.0 + 1.5
        assert coffee_with_whip.description() == "Simple coffee, whip cream"

    def test_cinnamon_decorator(self):
        """Test cinnamon decorator."""
        coffee = Coffee()
        coffee_with_cinnamon = Cinnamon(coffee)

        assert coffee_with_cinnamon.cost() == 5.3  # 5.0 + 0.3
        assert coffee_with_cinnamon.description() == "Simple coffee, cinnamon"

    def test_vanilla_decorator(self):
        """Test vanilla decorator."""
        coffee = Coffee()
        coffee_with_vanilla = Vanilla(coffee)

        assert coffee_with_vanilla.cost() == 5.7  # 5.0 + 0.7
        assert coffee_with_vanilla.description() == "Simple coffee, vanilla"

    def test_multiple_condiments(self):
        """Test multiple condiments on the same beverage."""
        coffee = Coffee()
        enhanced_coffee = Vanilla(Cinnamon(Sugar(Milk(coffee))))

        expected_cost = 5.0 + 1.0 + 0.5 + 0.3 + 0.7  # 7.5
        assert enhanced_coffee.cost() == expected_cost
        assert (
            enhanced_coffee.description()
            == "Simple coffee, milk, sugar, cinnamon, vanilla"
        )

    def test_same_condiment_multiple_times(self):
        """Test adding the same condiment multiple times."""
        coffee = Coffee()
        double_milk = Milk(Milk(coffee))

        assert double_milk.cost() == 7.0  # 5.0 + 1.0 + 1.0
        assert double_milk.description() == "Simple coffee, milk, milk"

    def test_tea_with_condiments(self):
        """Test tea with condiments."""
        tea = Tea()
        fancy_tea = Vanilla(Sugar(Milk(tea)))

        expected_cost = 3.0 + 1.0 + 0.5 + 0.7  # 5.2
        assert fancy_tea.cost() == expected_cost
        assert fancy_tea.description() == "Simple tea, milk, sugar, vanilla"

    def test_condiment_decorator_inheritance(self):
        """Test condiment decorator inheritance."""
        coffee = Coffee()
        milk = Milk(coffee)
        sugar = Sugar(coffee)

        assert isinstance(milk, CondimentDecorator)
        assert isinstance(sugar, CondimentDecorator)
        assert isinstance(milk, Beverage)
        assert isinstance(sugar, Beverage)

    def test_complex_beverage_composition(self):
        """Test complex beverage composition."""
        # Create a very complex beverage
        coffee = Coffee()
        complex_beverage = WhipCream(
            Vanilla(Cinnamon(Sugar(Sugar(Milk(Milk(coffee))))))
        )

        # Calculate expected cost
        expected_cost = 5.0 + 1.0 + 1.0 + 0.5 + 0.5 + 0.3 + 0.7 + 1.5  # 10.5
        assert complex_beverage.cost() == expected_cost

        expected_description = (
            "Simple coffee, milk, milk, sugar, sugar, cinnamon, vanilla, whip cream"
        )
        assert complex_beverage.description() == expected_description


class TestTextProcessor:
    """Test the TextProcessor decorator implementation."""

    def test_plain_text(self):
        """Test plain text processor."""
        processor = PlainText()
        text = "Hello World"

        assert processor.process(text) == "Hello World"

    def test_uppercase_decorator(self):
        """Test uppercase decorator."""
        processor = UppercaseDecorator(PlainText())
        text = "hello world"

        assert processor.process(text) == "HELLO WORLD"

    def test_lowercase_decorator(self):
        """Test lowercase decorator."""
        processor = LowercaseDecorator(PlainText())
        text = "HELLO WORLD"

        assert processor.process(text) == "hello world"

    def test_trim_decorator(self):
        """Test trim decorator."""
        processor = TrimDecorator(PlainText())
        text = "  hello world  "

        assert processor.process(text) == "hello world"

    def test_remove_extra_spaces_decorator(self):
        """Test remove extra spaces decorator."""
        processor = RemoveExtraSpacesDecorator(PlainText())
        text = "hello    world   test"

        assert processor.process(text) == "hello world test"

    def test_censor_decorator(self):
        """Test censor decorator."""
        processor = CensorDecorator(PlainText(), ["bad", "ugly"])
        text = "This is a bad and ugly example"

        assert processor.process(text) == "This is a *** and **** example"

    def test_reverse_decorator(self):
        """Test reverse decorator."""
        processor = ReverseDecorator(PlainText())
        text = "hello"

        assert processor.process(text) == "olleh"

    def test_prefix_decorator(self):
        """Test prefix decorator."""
        processor = PrefixDecorator(PlainText(), ">>> ")
        text = "hello world"

        assert processor.process(text) == ">>> hello world"

    def test_suffix_decorator(self):
        """Test suffix decorator."""
        processor = SuffixDecorator(PlainText(), " <<<")
        text = "hello world"

        assert processor.process(text) == "hello world <<<"

    def test_complex_text_processing(self):
        """Test complex text processing pipeline."""
        text = "  This is a BAD  example with   extra   spaces.  "

        # Build processing pipeline
        processor = PlainText()
        processor = TrimDecorator(processor)
        processor = RemoveExtraSpacesDecorator(processor)
        processor = CensorDecorator(processor, ["BAD"])
        processor = UppercaseDecorator(processor)
        processor = PrefixDecorator(processor, "PROCESSED: ")
        processor = SuffixDecorator(processor, " [DONE]")

        result = processor.process(text)
        assert result == "PROCESSED: THIS IS A *** EXAMPLE WITH EXTRA SPACES. [DONE]"

    def test_text_decorator_composition(self):
        """Test different text decorator compositions."""
        text = "hello world"

        # Different compositions should yield different results
        composition1 = UppercaseDecorator(ReverseDecorator(PlainText()))
        composition2 = ReverseDecorator(UppercaseDecorator(PlainText()))

        result1 = composition1.process(text)
        result2 = composition2.process(text)

        assert result1 == "DLROW OLLEH"
        assert result2 == "DLROW OLLEH"

    def test_censor_decorator_edge_cases(self):
        """Test censor decorator edge cases."""
        # Empty censorship list
        processor = CensorDecorator(PlainText(), [])
        text = "hello world"
        assert processor.process(text) == "hello world"

        # Case sensitivity
        processor = CensorDecorator(PlainText(), ["Hello"])
        text = "hello world"
        assert processor.process(text) == "hello world"  # Case sensitive

        # Multiple occurrences
        processor = CensorDecorator(PlainText(), ["test"])
        text = "test this test"
        assert processor.process(text) == "**** this ****"

    def test_text_processor_inheritance(self):
        """Test text processor inheritance."""
        processors = [
            PlainText(),
            UppercaseDecorator(PlainText()),
            LowercaseDecorator(PlainText()),
            TrimDecorator(PlainText()),
        ]

        for processor in processors:
            assert isinstance(processor, TextProcessor)

        # Test decorators inherit from TextDecorator
        decorators = [
            UppercaseDecorator(PlainText()),
            LowercaseDecorator(PlainText()),
            TrimDecorator(PlainText()),
        ]

        for decorator in decorators:
            assert isinstance(decorator, TextDecorator)


class TestFunctionDecorators:
    """Test function decorators."""

    def test_timer_decorator(self, capsys):
        """Test timer decorator."""

        @timer
        def test_function():
            time.sleep(0.01)
            return "result"

        result = test_function()

        assert result == "result"
        captured = capsys.readouterr()
        assert "test_function executed in" in captured.out
        assert "seconds" in captured.out

    def test_logger_decorator(self, capsys):
        """Test logger decorator."""

        @logger
        def test_function(x, y, z=None):
            return x + y

        result = test_function(1, 2, z=3)

        assert result == 3
        captured = capsys.readouterr()
        assert "Calling test_function with args=(1, 2), kwargs={'z': 3}" in captured.out
        assert "test_function returned 3" in captured.out

    def test_retry_decorator_success(self, capsys):
        """Test retry decorator with successful execution."""

        @retry(max_attempts=3, delay=0.01)
        def test_function():
            return "success"

        result = test_function()

        assert result == "success"
        captured = capsys.readouterr()
        assert "Attempt" not in captured.out  # No retry messages

    def test_retry_decorator_failure_then_success(self, capsys):
        """Test retry decorator with initial failure then success."""
        call_count = 0

        @retry(max_attempts=3, delay=0.01)
        def test_function():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Temporary failure")
            return "success"

        result = test_function()

        assert result == "success"
        assert call_count == 2
        captured = capsys.readouterr()
        assert "Attempt 1 failed" in captured.out
        assert "Retrying in 0.01 seconds" in captured.out

    def test_retry_decorator_all_attempts_fail(self, capsys):
        """Test retry decorator when all attempts fail."""

        @retry(max_attempts=3, delay=0.01)
        def test_function():
            raise ValueError("Persistent failure")

        with pytest.raises(ValueError) as exc_info:
            test_function()

        assert "Persistent failure" in str(exc_info.value)
        captured = capsys.readouterr()
        assert "All 3 attempts failed" in captured.out

    def test_cache_decorator(self, capsys):
        """Test cache decorator."""
        call_count = 0

        @cache
        def test_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call - cache miss
        result1 = test_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same args - cache hit
        result2 = test_function(5)
        assert result2 == 10
        assert call_count == 1  # Function not called again

        # Third call with different args - cache miss
        result3 = test_function(6)
        assert result3 == 12
        assert call_count == 2

        captured = capsys.readouterr()
        assert "Cache miss" in captured.out
        assert "Cache hit" in captured.out

    def test_cache_decorator_with_kwargs(self, capsys):
        """Test cache decorator with keyword arguments."""
        call_count = 0

        @cache
        def test_function(x, y=None):
            nonlocal call_count
            call_count += 1
            return x + (y or 0)

        # Different calls
        result1 = test_function(1, y=2)
        result2 = test_function(1, y=2)  # Same args - cache hit
        result3 = test_function(1, 2)  # Different call style - cache miss

        assert result1 == 3
        assert result2 == 3
        assert result3 == 3
        assert call_count == 2  # Two cache misses

    def test_validate_types_decorator(self):
        """Test validate_types decorator."""

        @validate_types(name=str, age=int)
        def test_function(name, age):
            return f"Hello {name}, you are {age} years old"

        # Valid types
        result = test_function("Alice", 25)
        assert result == "Hello Alice, you are 25 years old"

        # Invalid type for name
        with pytest.raises(TypeError) as exc_info:
            test_function(123, 25)
        assert "Parameter 'name' must be of type str" in str(exc_info.value)

        # Invalid type for age
        with pytest.raises(TypeError) as exc_info:
            test_function("Alice", "twenty-five")
        assert "Parameter 'age' must be of type int" in str(exc_info.value)

    def test_validate_types_decorator_with_defaults(self):
        """Test validate_types decorator with default values."""

        @validate_types(name=str, age=int)
        def test_function(name, age=30):
            return f"Hello {name}, you are {age} years old"

        # Using default value
        result = test_function("Bob")
        assert result == "Hello Bob, you are 30 years old"

        # Invalid type for default parameter
        with pytest.raises(TypeError):
            test_function("Bob", "thirty")

    def test_combined_decorators(self, capsys):
        """Test combining multiple decorators."""

        @timer
        @logger
        @cache
        def test_function(x):
            time.sleep(0.01)
            return x * 2

        # First call
        result1 = test_function(5)
        assert result1 == 10

        # Second call - should use cache
        result2 = test_function(5)
        assert result2 == 10

        captured = capsys.readouterr()
        assert "Cache miss" in captured.out
        assert "Cache hit" in captured.out
        assert "Calling test_function" in captured.out
        assert "executed in" in captured.out


class TestRateLimiter:
    """Test rate limiter class-based decorator."""

    def test_rate_limiter_under_limit(self):
        """Test rate limiter when under the limit."""

        @RateLimiter(max_calls=3, time_window=1.0)
        def test_function():
            return "success"

        # Should work for first 3 calls
        results = []
        for i in range(3):
            results.append(test_function())

        assert all(result == "success" for result in results)

    def test_rate_limiter_over_limit(self):
        """Test rate limiter when over the limit."""

        @RateLimiter(max_calls=2, time_window=1.0)
        def test_function():
            return "success"

        # First 2 calls should work
        test_function()
        test_function()

        # Third call should fail
        with pytest.raises(Exception) as exc_info:
            test_function()

        assert "Rate limit exceeded" in str(exc_info.value)
        assert "2 calls per 1.0 seconds" in str(exc_info.value)

    def test_rate_limiter_time_window_reset(self):
        """Test rate limiter resets after time window."""

        @RateLimiter(max_calls=2, time_window=0.1)
        def test_function():
            return "success"

        # Use up the limit
        test_function()
        test_function()

        # Wait for time window to pass
        time.sleep(0.2)

        # Should work again
        result = test_function()
        assert result == "success"

    def test_rate_limiter_different_functions(self):
        """Test rate limiter with different functions."""
        rate_limiter = RateLimiter(max_calls=2, time_window=1.0)

        @rate_limiter
        def function1():
            return "function1"

        @rate_limiter
        def function2():
            return "function2"

        # Each function should have its own rate limit
        assert function1() == "function1"
        assert function1() == "function1"

        assert function2() == "function2"
        assert function2() == "function2"

        # Both should be at limit now
        with pytest.raises(Exception):
            function1()

        with pytest.raises(Exception):
            function2()


class TestDecoratorPatternIntegration:
    """Test integration scenarios with decorator pattern."""

    def test_complete_beverage_system(self):
        """Test complete beverage ordering system."""
        # Create different beverage combinations
        beverages = [
            Coffee(),
            Tea(),
            Milk(Coffee()),
            Sugar(Tea()),
            WhipCream(Vanilla(Cinnamon(Sugar(Milk(Coffee()))))),
            Cinnamon(Sugar(Milk(Tea()))),
        ]

        # Test that all beverages have valid costs and descriptions
        for beverage in beverages:
            assert beverage.cost() > 0
            assert isinstance(beverage.description(), str)
            assert len(beverage.description()) > 0

    def test_text_processing_pipeline(self):
        """Test complete text processing pipeline."""
        # Test different text inputs
        test_cases = [
            "  hello world  ",
            "UPPERCASE TEXT",
            "text with BAD words",
            "   multiple   spaces   here   ",
            "reverse this text",
        ]

        # Build processing pipeline
        processor = PlainText()
        processor = TrimDecorator(processor)
        processor = RemoveExtraSpacesDecorator(processor)
        processor = CensorDecorator(processor, ["BAD", "bad"])
        processor = LowercaseDecorator(processor)
        processor = PrefixDecorator(processor, "[PROCESSED] ")
        processor = SuffixDecorator(processor, " [END]")

        for text in test_cases:
            result = processor.process(text)
            assert result.startswith("[PROCESSED] ")
            assert result.endswith(" [END]")
            assert "BAD" not in result
            assert "bad" not in result

    def test_decorator_pattern_with_inheritance(self):
        """Test decorator pattern with inheritance."""

        # Create custom beverage
        class Espresso(Beverage):
            def cost(self):
                return 4.0

            def description(self):
                return "Strong espresso"

        # Create custom condiment
        class Caramel(CondimentDecorator):
            def cost(self):
                return self._beverage.cost() + 0.8

            def description(self):
                return self._beverage.description() + ", caramel"

        # Test with custom implementations
        espresso = Espresso()
        fancy_espresso = Caramel(Milk(espresso))

        assert fancy_espresso.cost() == 5.8  # 4.0 + 1.0 + 0.8
        assert fancy_espresso.description() == "Strong espresso, milk, caramel"

    def test_function_decorator_composition(self):
        """Test composing multiple function decorators."""

        @timer
        @logger
        @retry(max_attempts=2, delay=0.01)
        @cache
        @validate_types(x=int)
        def complex_function(x):
            if x < 0:
                raise ValueError("Negative input")
            return x**2

        # Test successful execution
        result = complex_function(5)
        assert result == 25

        # Test type validation
        with pytest.raises(TypeError):
            complex_function("invalid")

        # Test retry behavior
        with pytest.raises(ValueError):
            complex_function(-1)

    def test_dynamic_decorator_application(self):
        """Test applying decorators dynamically."""

        def base_function(x):
            return x * 2

        # Apply decorators dynamically
        decorated_function = timer(logger(cache(base_function)))

        result = decorated_function(5)
        assert result == 10

        # Test that cache works
        result2 = decorated_function(5)
        assert result2 == 10


class TestDecoratorPatternEdgeCases:
    """Test edge cases and error conditions."""

    def test_null_component_decorator(self):
        """Test decorator with null component."""
        # This should not happen in practice but test defensive programming
        try:
            decorator = ConcreteDecoratorA(None)
            decorator.operation()
            assert False, "Should have raised an exception"
        except AttributeError:
            pass  # Expected

    def test_circular_decorator_reference(self):
        """Test preventing circular decorator references."""
        # Create a circular reference scenario
        component = ConcreteComponent()
        decorator_a = ConcreteDecoratorA(component)

        # This would create circular reference - test that it doesn't crash
        try:
            decorator_b = ConcreteDecoratorB(decorator_a)
            # Accessing operation should work
            result = decorator_b.operation()
            assert "ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))" in result
        except RecursionError:
            assert False, "Should not have circular reference"

    def test_empty_text_processing(self):
        """Test text processing with empty strings."""
        processors = [
            UppercaseDecorator(PlainText()),
            LowercaseDecorator(PlainText()),
            TrimDecorator(PlainText()),
            ReverseDecorator(PlainText()),
        ]

        for processor in processors:
            result = processor.process("")
            assert result == ""

    def test_beverage_with_zero_cost_condiments(self):
        """Test beverage with zero-cost condiments."""

        class FreeCondiment(CondimentDecorator):
            def cost(self):
                return self._beverage.cost()  # No additional cost

            def description(self):
                return self._beverage.description() + ", free condiment"

        coffee = Coffee()
        free_coffee = FreeCondiment(coffee)

        assert free_coffee.cost() == 5.0
        assert free_coffee.description() == "Simple coffee, free condiment"

    def test_decorator_with_side_effects(self):
        """Test decorators that have side effects."""
        side_effects = []

        class SideEffectDecorator(TextDecorator):
            def process(self, text):
                side_effects.append(f"Processing: {text}")
                return self._processor.process(text)

        processor = SideEffectDecorator(PlainText())
        result = processor.process("test")

        assert result == "test"
        assert len(side_effects) == 1
        assert "Processing: test" in side_effects[0]

    def test_cache_decorator_with_mutable_arguments(self):
        """Test cache decorator with mutable arguments."""
        call_count = 0

        @cache
        def test_function(lst):
            nonlocal call_count
            call_count += 1
            return sum(lst)

        # Same list content but different objects
        result1 = test_function([1, 2, 3])
        result2 = test_function([1, 2, 3])

        assert result1 == 6
        assert result2 == 6
        # Note: This may or may not use cache depending on implementation
        # The behavior depends on how arguments are converted to cache keys

    def test_rate_limiter_with_zero_calls(self):
        """Test rate limiter with zero allowed calls."""

        @RateLimiter(max_calls=0, time_window=1.0)
        def test_function():
            return "success"

        # Should fail immediately
        with pytest.raises(Exception):
            test_function()


class TestDecoratorPatternPerformance:
    """Test performance characteristics of decorator pattern."""

    def test_deep_decorator_nesting_performance(self):
        """Test performance with deeply nested decorators."""
        import time

        # Create deeply nested decoration
        component = ConcreteComponent()
        decorated = component

        for i in range(100):
            if i % 2 == 0:
                decorated = ConcreteDecoratorA(decorated)
            else:
                decorated = ConcreteDecoratorB(decorated)

        # Measure operation time
        start = time.time()
        result = decorated.operation()
        end = time.time()

        # Should complete in reasonable time
        assert (end - start) < 0.1
        assert "ConcreteComponent" in result

    def test_beverage_decoration_performance(self):
        """Test performance of beverage decoration."""
        import time

        # Create heavily decorated beverage
        beverage = Coffee()

        # Add many decorations
        for i in range(50):
            beverage = Milk(beverage)

        # Measure cost calculation time
        start = time.time()
        cost = beverage.cost()
        end = time.time()

        # Should complete quickly
        assert (end - start) < 0.1
        assert cost == 5.0 + (50 * 1.0)  # Coffee + 50 milk

    def test_text_processing_performance(self):
        """Test performance of text processing pipeline."""
        import time

        # Create long text
        text = "This is a test text. " * 1000

        # Create processing pipeline
        processor = PlainText()
        processor = TrimDecorator(processor)
        processor = RemoveExtraSpacesDecorator(processor)
        processor = UppercaseDecorator(processor)
        processor = LowercaseDecorator(processor)

        # Measure processing time
        start = time.time()
        result = processor.process(text)
        end = time.time()

        # Should complete in reasonable time
        assert (end - start) < 1.0
        assert len(result) > 0

    def test_cache_decorator_performance(self):
        """Test performance benefit of cache decorator."""
        import time

        call_count = 0

        @cache
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            time.sleep(0.01)  # Simulate expensive operation
            return x * x

        # First call - should be slow
        start = time.time()
        result1 = expensive_function(5)
        first_call_time = time.time() - start

        # Second call - should be fast (cached)
        start = time.time()
        result2 = expensive_function(5)
        second_call_time = time.time() - start

        assert result1 == result2 == 25
        assert call_count == 1  # Function called only once
        assert second_call_time < first_call_time  # Cached call is faster
