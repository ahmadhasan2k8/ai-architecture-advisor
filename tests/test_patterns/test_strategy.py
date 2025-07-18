"""Tests for strategy pattern implementations."""

import time
from unittest.mock import Mock, patch

import pytest

from src.patterns.strategy import (  # Basic Strategy Pattern; Payment Processing; Sorting Algorithms; Discount Calculation
    BubbleSort,
    BuyOneGetOneDiscount,
    Context,
    CreditCardPayment,
    CryptocurrencyPayment,
    DataSorter,
    DiscountStrategy,
    FixedAmountDiscount,
    MergeSort,
    PaymentStrategy,
    PayPalPayment,
    PercentageDiscount,
    PriceCalculator,
    QuickSort,
    ShoppingCart,
    SortingStrategy,
    Strategy,
)


class TestBasicStrategyPattern:
    """Test the basic Strategy pattern implementation."""

    def test_context_creation(self):
        """Test creating a context."""
        context = Context()
        assert context._strategy is None

    def test_context_with_strategy(self):
        """Test creating a context with a strategy."""
        strategy = Mock(spec=Strategy)
        context = Context(strategy)
        assert context._strategy is strategy

    def test_set_strategy(self):
        """Test setting a strategy."""
        context = Context()
        strategy = Mock(spec=Strategy)

        context.set_strategy(strategy)
        assert context._strategy is strategy

    def test_execute_strategy(self):
        """Test executing a strategy."""
        strategy = Mock(spec=Strategy)
        strategy.execute.return_value = "result"

        context = Context(strategy)
        result = context.execute_strategy("test_data")

        assert result == "result"
        strategy.execute.assert_called_once_with("test_data")

    def test_execute_without_strategy(self):
        """Test executing without a strategy raises error."""
        context = Context()

        with pytest.raises(ValueError) as exc_info:
            context.execute_strategy("test_data")

        assert "No strategy set" in str(exc_info.value)

    def test_strategy_change(self):
        """Test changing strategies."""
        strategy1 = Mock(spec=Strategy)
        strategy2 = Mock(spec=Strategy)
        strategy1.execute.return_value = "result1"
        strategy2.execute.return_value = "result2"

        context = Context(strategy1)

        result1 = context.execute_strategy("data")
        assert result1 == "result1"

        context.set_strategy(strategy2)
        result2 = context.execute_strategy("data")
        assert result2 == "result2"


class TestPaymentStrategies:
    """Test payment strategy implementations."""

    def test_credit_card_payment_creation(self):
        """Test creating credit card payment."""
        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")

        assert payment.card_number == "1234567890123456"
        assert payment.cardholder == "John Doe"
        assert payment.cvv == "123"
        assert payment.expiry == "12/25"

    def test_credit_card_payment_success(self, capsys):
        """Test successful credit card payment."""
        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")

        result = payment.pay(100.0)

        assert result is True
        captured = capsys.readouterr()
        assert "Processing credit card payment of $100.00" in captured.out
        assert "Card: **** **** **** 3456" in captured.out
        assert "Cardholder: John Doe" in captured.out
        assert "Credit card payment successful" in captured.out

    def test_credit_card_invalid_number(self, capsys):
        """Test credit card with invalid number."""
        payment = CreditCardPayment(
            "123456789012345", "John Doe", "123", "12/25"
        )  # 15 digits

        result = payment.pay(100.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid card number" in captured.out

    def test_credit_card_invalid_cvv(self, capsys):
        """Test credit card with invalid CVV."""
        payment = CreditCardPayment(
            "1234567890123456", "John Doe", "12", "12/25"
        )  # 2 digits

        result = payment.pay(100.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid CVV" in captured.out

    def test_credit_card_non_numeric_number(self, capsys):
        """Test credit card with non-numeric number."""
        payment = CreditCardPayment("123456789012345a", "John Doe", "123", "12/25")

        result = payment.pay(100.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid card number" in captured.out

    def test_credit_card_non_numeric_cvv(self, capsys):
        """Test credit card with non-numeric CVV."""
        payment = CreditCardPayment("1234567890123456", "John Doe", "12a", "12/25")

        result = payment.pay(100.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid CVV" in captured.out

    def test_credit_card_get_payment_details(self):
        """Test credit card payment details."""
        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")

        details = payment.get_payment_details()
        assert details == "Credit Card ending in 3456"

    def test_paypal_payment_creation(self):
        """Test creating PayPal payment."""
        payment = PayPalPayment("user@example.com", "password123")

        assert payment.email == "user@example.com"
        assert payment.password == "password123"

    def test_paypal_payment_success(self, capsys):
        """Test successful PayPal payment."""
        payment = PayPalPayment("user@example.com", "password123")

        result = payment.pay(75.0)

        assert result is True
        captured = capsys.readouterr()
        assert "Processing PayPal payment of $75.00" in captured.out
        assert "Account: user@example.com" in captured.out
        assert "PayPal payment successful" in captured.out

    def test_paypal_invalid_email(self, capsys):
        """Test PayPal with invalid email."""
        payment = PayPalPayment("invalid_email", "password123")

        result = payment.pay(75.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid email address" in captured.out

    def test_paypal_short_password(self, capsys):
        """Test PayPal with short password."""
        payment = PayPalPayment("user@example.com", "123")

        result = payment.pay(75.0)

        assert result is False
        captured = capsys.readouterr()
        assert "Password too short" in captured.out

    def test_paypal_get_payment_details(self):
        """Test PayPal payment details."""
        payment = PayPalPayment("user@example.com", "password123")

        details = payment.get_payment_details()
        assert details == "PayPal (user@example.com)"

    def test_cryptocurrency_payment_creation(self):
        """Test creating cryptocurrency payment."""
        payment = CryptocurrencyPayment(
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key", "Bitcoin"
        )

        assert payment.wallet_address == "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        assert payment.private_key == "private_key"
        assert payment.currency == "Bitcoin"

    def test_cryptocurrency_payment_success(self, capsys):
        """Test successful cryptocurrency payment."""
        payment = CryptocurrencyPayment(
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key", "Bitcoin"
        )

        result = payment.pay(0.001)

        assert result is True
        captured = capsys.readouterr()
        assert "Processing Bitcoin payment of $0.00" in captured.out
        assert "Wallet: 1A1zP1eP5Q...DivfNa" in captured.out
        assert "Broadcasting transaction to Bitcoin network" in captured.out
        assert "Cryptocurrency payment successful" in captured.out

    def test_cryptocurrency_invalid_wallet(self, capsys):
        """Test cryptocurrency with invalid wallet address."""
        payment = CryptocurrencyPayment("short_address", "private_key", "Bitcoin")

        result = payment.pay(0.001)

        assert result is False
        captured = capsys.readouterr()
        assert "Invalid wallet address" in captured.out

    def test_cryptocurrency_get_payment_details(self):
        """Test cryptocurrency payment details."""
        payment = CryptocurrencyPayment(
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key", "Bitcoin"
        )

        details = payment.get_payment_details()
        assert details == "Bitcoin Wallet (1A1zP1eP5Q...)"

    def test_cryptocurrency_default_currency(self):
        """Test cryptocurrency with default currency."""
        payment = CryptocurrencyPayment(
            "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key"
        )

        assert payment.currency == "Bitcoin"


class TestShoppingCart:
    """Test shopping cart implementation."""

    def test_shopping_cart_creation(self):
        """Test creating a shopping cart."""
        cart = ShoppingCart()

        assert len(cart.items) == 0
        assert cart.payment_strategy is None

    def test_add_item(self, capsys):
        """Test adding items to cart."""
        cart = ShoppingCart()

        cart.add_item("Laptop", 999.99)
        cart.add_item("Mouse", 25.99)

        assert len(cart.items) == 2
        assert cart.items[0]["name"] == "Laptop"
        assert cart.items[0]["price"] == 999.99
        assert cart.items[1]["name"] == "Mouse"
        assert cart.items[1]["price"] == 25.99

        captured = capsys.readouterr()
        assert "Added Laptop ($999.99) to cart" in captured.out
        assert "Added Mouse ($25.99) to cart" in captured.out

    def test_get_total(self):
        """Test calculating cart total."""
        cart = ShoppingCart()

        cart.add_item("Laptop", 999.99)
        cart.add_item("Mouse", 25.99)
        cart.add_item("Keyboard", 75.50)

        total = cart.get_total()
        assert total == pytest.approx(1101.48, rel=1e-9)

    def test_set_payment_strategy(self, capsys):
        """Test setting payment strategy."""
        cart = ShoppingCart()
        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")

        cart.set_payment_strategy(payment)

        assert cart.payment_strategy is payment
        captured = capsys.readouterr()
        assert "Payment method set to: Credit Card ending in 3456" in captured.out

    def test_checkout_success(self, capsys):
        """Test successful checkout."""
        cart = ShoppingCart()
        cart.add_item("Laptop", 999.99)

        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")
        cart.set_payment_strategy(payment)

        result = cart.checkout()

        assert result is True
        captured = capsys.readouterr()
        assert "Checkout: 1 items, Total: $999.99" in captured.out
        assert "Order confirmed and will be shipped!" in captured.out

    def test_checkout_no_payment_method(self, capsys):
        """Test checkout without payment method."""
        cart = ShoppingCart()
        cart.add_item("Laptop", 999.99)

        result = cart.checkout()

        assert result is False
        captured = capsys.readouterr()
        assert "No payment method selected" in captured.out

    def test_checkout_empty_cart(self, capsys):
        """Test checkout with empty cart."""
        cart = ShoppingCart()
        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")
        cart.set_payment_strategy(payment)

        result = cart.checkout()

        assert result is False
        captured = capsys.readouterr()
        assert "Cart is empty" in captured.out

    def test_checkout_payment_failure(self, capsys):
        """Test checkout with payment failure."""
        cart = ShoppingCart()
        cart.add_item("Laptop", 999.99)

        # Invalid payment method
        payment = CreditCardPayment("123", "John Doe", "123", "12/25")
        cart.set_payment_strategy(payment)

        result = cart.checkout()

        assert result is False
        captured = capsys.readouterr()
        assert "Payment failed - order cancelled" in captured.out


class TestSortingStrategies:
    """Test sorting strategy implementations."""

    def test_bubble_sort(self):
        """Test bubble sort implementation."""
        sorter = BubbleSort()

        data = [64, 34, 25, 12, 22, 11, 90]
        sorted_data = sorter.sort(data)

        assert sorted_data == [11, 12, 22, 25, 34, 64, 90]
        assert data == [64, 34, 25, 12, 22, 11, 90]  # Original unchanged

    def test_bubble_sort_info(self):
        """Test bubble sort information."""
        sorter = BubbleSort()

        assert sorter.get_name() == "Bubble Sort"
        assert sorter.get_time_complexity() == "O(n²)"

    def test_quick_sort(self):
        """Test quick sort implementation."""
        sorter = QuickSort()

        data = [64, 34, 25, 12, 22, 11, 90]
        sorted_data = sorter.sort(data)

        assert sorted_data == [11, 12, 22, 25, 34, 64, 90]
        assert data == [64, 34, 25, 12, 22, 11, 90]  # Original unchanged

    def test_quick_sort_info(self):
        """Test quick sort information."""
        sorter = QuickSort()

        assert sorter.get_name() == "Quick Sort"
        assert sorter.get_time_complexity() == "O(n log n)"

    def test_merge_sort(self):
        """Test merge sort implementation."""
        sorter = MergeSort()

        data = [64, 34, 25, 12, 22, 11, 90]
        sorted_data = sorter.sort(data)

        assert sorted_data == [11, 12, 22, 25, 34, 64, 90]
        assert data == [64, 34, 25, 12, 22, 11, 90]  # Original unchanged

    def test_merge_sort_info(self):
        """Test merge sort information."""
        sorter = MergeSort()

        assert sorter.get_name() == "Merge Sort"
        assert sorter.get_time_complexity() == "O(n log n)"

    def test_sorting_empty_list(self):
        """Test sorting empty list."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]

        for sorter in sorters:
            result = sorter.sort([])
            assert result == []

    def test_sorting_single_element(self):
        """Test sorting single element."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]

        for sorter in sorters:
            result = sorter.sort([42])
            assert result == [42]

    def test_sorting_already_sorted(self):
        """Test sorting already sorted list."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]
        data = [1, 2, 3, 4, 5]

        for sorter in sorters:
            result = sorter.sort(data)
            assert result == [1, 2, 3, 4, 5]

    def test_sorting_reverse_sorted(self):
        """Test sorting reverse sorted list."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]
        data = [5, 4, 3, 2, 1]

        for sorter in sorters:
            result = sorter.sort(data)
            assert result == [1, 2, 3, 4, 5]

    def test_sorting_duplicates(self):
        """Test sorting list with duplicates."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5]

        for sorter in sorters:
            result = sorter.sort(data)
            assert result == [1, 1, 2, 3, 4, 5, 5, 6, 9]

    def test_sorting_strings(self):
        """Test sorting strings."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]
        data = ["banana", "apple", "cherry", "date"]

        for sorter in sorters:
            result = sorter.sort(data)
            assert result == ["apple", "banana", "cherry", "date"]


class TestDataSorter:
    """Test data sorter implementation."""

    def test_data_sorter_creation(self):
        """Test creating data sorter."""
        sorter = DataSorter()

        assert sorter.strategy is None
        assert len(sorter.data) == 0

    def test_data_sorter_with_strategy(self):
        """Test creating data sorter with strategy."""
        strategy = BubbleSort()
        sorter = DataSorter(strategy)

        assert sorter.strategy is strategy

    def test_set_strategy(self):
        """Test setting strategy."""
        sorter = DataSorter()
        strategy = QuickSort()

        sorter.set_strategy(strategy)
        assert sorter.strategy is strategy

    def test_add_data(self):
        """Test adding data."""
        sorter = DataSorter()

        sorter.add_data([3, 1, 4])
        sorter.add_data([1, 5, 9])

        assert sorter.data == [3, 1, 4, 1, 5, 9]

    def test_sort_data(self, capsys):
        """Test sorting data."""
        sorter = DataSorter()
        sorter.set_strategy(QuickSort())
        sorter.add_data([3, 1, 4, 1, 5, 9, 2, 6, 5])

        result = sorter.sort_data()

        assert result == [1, 1, 2, 3, 4, 5, 5, 6, 9]
        captured = capsys.readouterr()
        assert "Sorting 9 items using Quick Sort" in captured.out
        assert "Time complexity: O(n log n)" in captured.out
        assert "Sorting completed in" in captured.out

    def test_sort_data_no_strategy(self):
        """Test sorting data without strategy."""
        sorter = DataSorter()
        sorter.add_data([3, 1, 4])

        with pytest.raises(ValueError) as exc_info:
            sorter.sort_data()

        assert "No sorting strategy set" in str(exc_info.value)

    def test_sort_empty_data(self):
        """Test sorting empty data."""
        sorter = DataSorter()
        sorter.set_strategy(QuickSort())

        result = sorter.sort_data()
        assert result == []

    def test_benchmark_strategies(self):
        """Test benchmarking different strategies."""
        sorter = DataSorter()
        sorter.add_data([3, 1, 4, 1, 5, 9, 2, 6, 5])

        strategies = [BubbleSort(), QuickSort(), MergeSort()]
        results = sorter.benchmark_strategies(strategies)

        assert len(results) == 3
        assert "Bubble Sort" in results
        assert "Quick Sort" in results
        assert "Merge Sort" in results

        # All times should be positive
        for time_ms in results.values():
            assert time_ms >= 0


class TestDiscountStrategies:
    """Test discount strategy implementations."""

    def test_percentage_discount(self):
        """Test percentage discount."""
        discount = PercentageDiscount(20)

        assert discount.percentage == 20
        assert discount.calculate_discount(100) == 20
        assert discount.get_description() == "20% off"

    def test_percentage_discount_bounds(self):
        """Test percentage discount bounds."""
        # Test negative percentage
        discount = PercentageDiscount(-10)
        assert discount.percentage == 0

        # Test percentage over 100
        discount = PercentageDiscount(150)
        assert discount.percentage == 100

        # Test valid percentage
        discount = PercentageDiscount(50)
        assert discount.percentage == 50

    def test_fixed_amount_discount(self):
        """Test fixed amount discount."""
        discount = FixedAmountDiscount(15)

        assert discount.amount == 15
        assert discount.calculate_discount(100) == 15
        assert discount.get_description() == "$15.00 off"

    def test_fixed_amount_discount_bounds(self):
        """Test fixed amount discount bounds."""
        # Test negative amount
        discount = FixedAmountDiscount(-10)
        assert discount.amount == 0

        # Test discount larger than total
        discount = FixedAmountDiscount(150)
        assert discount.calculate_discount(100) == 100  # Cannot exceed total

        # Test valid amount
        discount = FixedAmountDiscount(50)
        assert discount.calculate_discount(100) == 50

    def test_buy_one_get_one_discount(self):
        """Test buy one get one discount."""
        discount = BuyOneGetOneDiscount(25)

        assert discount.item_price == 25
        assert discount.get_description() == "Buy one get one free ($25.00 items)"

    def test_bogo_discount_calculation(self):
        """Test BOGO discount calculation."""
        discount = BuyOneGetOneDiscount(25)

        # Not enough for BOGO
        assert discount.calculate_discount(25) == 0

        # Exactly 2 items - 1 free
        assert discount.calculate_discount(50) == 25

        # 3 items - 1 free
        assert discount.calculate_discount(75) == 25

        # 4 items - 2 free
        assert discount.calculate_discount(100) == 50

        # 5 items - 2 free
        assert discount.calculate_discount(125) == 50

    def test_bogo_discount_edge_cases(self):
        """Test BOGO discount edge cases."""
        discount = BuyOneGetOneDiscount(25)

        # Less than item price
        assert discount.calculate_discount(20) == 0

        # Exactly item price
        assert discount.calculate_discount(25) == 0

        # Just under 2 items
        assert discount.calculate_discount(49) == 0


class TestPriceCalculator:
    """Test price calculator implementation."""

    def test_price_calculator_creation(self):
        """Test creating price calculator."""
        calculator = PriceCalculator()

        assert calculator.discount_strategy is None

    def test_set_discount_strategy(self):
        """Test setting discount strategy."""
        calculator = PriceCalculator()
        discount = PercentageDiscount(20)

        calculator.set_discount_strategy(discount)
        assert calculator.discount_strategy is discount

    def test_calculate_final_price_no_discount(self):
        """Test calculating price without discount."""
        calculator = PriceCalculator()

        original, discount, final = calculator.calculate_final_price(100)

        assert original == 100
        assert discount == 0
        assert final == 100

    def test_calculate_final_price_with_discount(self):
        """Test calculating price with discount."""
        calculator = PriceCalculator()
        calculator.set_discount_strategy(PercentageDiscount(20))

        original, discount, final = calculator.calculate_final_price(100)

        assert original == 100
        assert discount == 20
        assert final == 80

    def test_print_price_breakdown_no_discount(self, capsys):
        """Test printing price breakdown without discount."""
        calculator = PriceCalculator()

        calculator.print_price_breakdown(100)

        captured = capsys.readouterr()
        assert "Price Breakdown:" in captured.out
        assert "Original Price: $100.00" in captured.out
        assert "Discount: -$0.00" in captured.out
        assert "Final Price: $100.00" in captured.out

    def test_print_price_breakdown_with_discount(self, capsys):
        """Test printing price breakdown with discount."""
        calculator = PriceCalculator()
        calculator.set_discount_strategy(PercentageDiscount(20))

        calculator.print_price_breakdown(100)

        captured = capsys.readouterr()
        assert "Price Breakdown:" in captured.out
        assert "Original Price: $100.00" in captured.out
        assert "Discount (20% off): -$20.00" in captured.out
        assert "Final Price: $80.00" in captured.out
        assert "You save: $20.00 (20.0%)" in captured.out


class TestStrategyPatternIntegration:
    """Test integration scenarios with strategy pattern."""

    def test_complete_shopping_system(self, capsys):
        """Test complete shopping system with different payment methods."""
        # Create cart and add items
        cart = ShoppingCart()
        cart.add_item("Laptop", 999.99)
        cart.add_item("Mouse", 25.99)

        # Test different payment methods
        payment_methods = [
            CreditCardPayment("1234567890123456", "John Doe", "123", "12/25"),
            PayPalPayment("user@example.com", "password123"),
            CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key"),
        ]

        for payment in payment_methods:
            cart.set_payment_strategy(payment)
            result = cart.checkout()
            assert result is True

        captured = capsys.readouterr()
        assert "Credit card payment successful" in captured.out
        assert "PayPal payment successful" in captured.out
        assert "Cryptocurrency payment successful" in captured.out

    def test_sorting_algorithm_comparison(self):
        """Test comparing different sorting algorithms."""
        data = [64, 34, 25, 12, 22, 11, 90, 88, 76, 50, 42]
        expected = [11, 12, 22, 25, 34, 42, 50, 64, 76, 88, 90]

        sorter = DataSorter()
        sorter.add_data(data)

        # Test all algorithms produce the same result
        algorithms = [BubbleSort(), QuickSort(), MergeSort()]

        for algorithm in algorithms:
            sorter.set_strategy(algorithm)
            result = sorter.sort_data()
            assert result == expected

    def test_discount_system_integration(self, capsys):
        """Test discount system with different discount types."""
        calculator = PriceCalculator()
        original_price = 100.0

        # Test different discount strategies
        discounts = [
            PercentageDiscount(20),
            FixedAmountDiscount(15),
            BuyOneGetOneDiscount(25),
        ]

        expected_results = [
            (100.0, 20.0, 80.0),
            (100.0, 15.0, 85.0),
            (100.0, 50.0, 50.0),  # 4 items of $25 each
        ]

        for discount, expected in zip(discounts, expected_results):
            calculator.set_discount_strategy(discount)
            result = calculator.calculate_final_price(original_price)
            assert result == expected

    def test_dynamic_strategy_switching(self, capsys):
        """Test dynamic strategy switching during runtime."""
        # Payment strategy switching
        cart = ShoppingCart()
        cart.add_item("Product", 100.0)

        # Start with credit card
        payment1 = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")
        cart.set_payment_strategy(payment1)

        # Switch to PayPal
        payment2 = PayPalPayment("user@example.com", "password123")
        cart.set_payment_strategy(payment2)

        result = cart.checkout()
        assert result is True

        captured = capsys.readouterr()
        assert "PayPal payment successful" in captured.out
        assert "Credit card payment successful" not in captured.out

    def test_strategy_pattern_with_lambda(self):
        """Test strategy pattern with lambda functions."""

        # Create a simple strategy using lambda
        class LambdaStrategy:
            def __init__(self, func):
                self.func = func

            def execute(self, data):
                return self.func(data)

        # Test with different lambda strategies
        double_strategy = LambdaStrategy(lambda x: x * 2)
        square_strategy = LambdaStrategy(lambda x: x**2)

        context = Context()

        context.set_strategy(double_strategy)
        assert context.execute_strategy(5) == 10

        context.set_strategy(square_strategy)
        assert context.execute_strategy(5) == 25


class TestStrategyPatternEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_amount_payments(self):
        """Test payment strategies with zero amount."""
        payments = [
            CreditCardPayment("1234567890123456", "John Doe", "123", "12/25"),
            PayPalPayment("user@example.com", "password123"),
            CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key"),
        ]

        for payment in payments:
            result = payment.pay(0.0)
            assert result is True  # Zero amount should succeed

    def test_negative_amount_payments(self):
        """Test payment strategies with negative amount."""
        payments = [
            CreditCardPayment("1234567890123456", "John Doe", "123", "12/25"),
            PayPalPayment("user@example.com", "password123"),
            CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key"),
        ]

        for payment in payments:
            result = payment.pay(-10.0)
            assert result is True  # Implementation doesn't validate negative amounts

    def test_sorting_with_none_values(self):
        """Test sorting strategies with None values."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]

        for sorter in sorters:
            with pytest.raises(TypeError):
                sorter.sort([1, None, 3])

    def test_sorting_mixed_types(self):
        """Test sorting strategies with mixed types."""
        sorters = [BubbleSort(), QuickSort(), MergeSort()]

        for sorter in sorters:
            with pytest.raises(TypeError):
                sorter.sort([1, "string", 3])

    def test_discount_with_zero_price(self):
        """Test discount strategies with zero price."""
        discounts = [
            PercentageDiscount(20),
            FixedAmountDiscount(15),
            BuyOneGetOneDiscount(25),
        ]

        for discount in discounts:
            result = discount.calculate_discount(0)
            assert result == 0

    def test_discount_with_negative_price(self):
        """Test discount strategies with negative price."""
        discounts = [
            PercentageDiscount(20),
            FixedAmountDiscount(15),
            BuyOneGetOneDiscount(25),
        ]

        for discount in discounts:
            result = discount.calculate_discount(-100)
            # Results may vary, but should not raise exceptions
            assert isinstance(result, (int, float))


class TestStrategyPatternPerformance:
    """Test performance characteristics of strategy pattern."""

    def test_sorting_performance_comparison(self):
        """Test performance comparison of sorting algorithms."""
        import random

        # Generate test data
        data = [random.randint(1, 1000) for _ in range(100)]

        sorter = DataSorter()
        sorter.add_data(data)

        # Test different algorithms
        algorithms = [BubbleSort(), QuickSort(), MergeSort()]
        results = sorter.benchmark_strategies(algorithms)

        # QuickSort and MergeSort should be faster than BubbleSort for larger datasets
        assert results["Bubble Sort"] >= results["Quick Sort"]
        assert results["Bubble Sort"] >= results["Merge Sort"]

    def test_strategy_switching_overhead(self):
        """Test overhead of strategy switching."""
        import time

        context = Context()
        strategies = [Mock(spec=Strategy) for _ in range(100)]

        # Configure mocks
        for strategy in strategies:
            strategy.execute.return_value = "result"

        # Measure time for strategy switching
        start = time.time()
        for strategy in strategies:
            context.set_strategy(strategy)
            context.execute_strategy("data")
        end = time.time()

        # Should be very fast
        assert (end - start) < 0.1

    def test_payment_processing_efficiency(self):
        """Test efficiency of payment processing."""
        import time

        cart = ShoppingCart()
        cart.add_item("Product", 100.0)

        payment = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")
        cart.set_payment_strategy(payment)

        # Measure checkout time
        start = time.time()
        for _ in range(100):
            cart.checkout()
        end = time.time()

        # Should be efficient
        assert (end - start) < 1.0
