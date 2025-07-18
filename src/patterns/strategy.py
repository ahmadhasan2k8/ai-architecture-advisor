"""Strategy pattern implementations.

This module provides implementations of the Strategy pattern, demonstrating
how to define a family of algorithms and make them interchangeable.
"""

import math
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union


class Strategy(ABC):
    """Abstract base class for strategies.
    
    This interface defines the contract that all concrete strategies must follow.
    """
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """Execute the strategy algorithm.
        
        Args:
            data: Input data for the algorithm
            
        Returns:
            Result of the algorithm execution
        """
        pass


class Context:
    """Context class that uses a strategy.
    
    The context maintains a reference to a strategy object and delegates
    work to it. The context doesn't know which concrete strategy it works with.
    """
    
    def __init__(self, strategy: Optional[Strategy] = None):
        """Initialize the context with an optional strategy.
        
        Args:
            strategy: The strategy to use
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: Strategy) -> None:
        """Set or change the strategy.
        
        Args:
            strategy: The new strategy to use
        """
        self._strategy = strategy
    
    def execute_strategy(self, data: Any) -> Any:
        """Execute the current strategy.
        
        Args:
            data: Input data for the strategy
            
        Returns:
            Result of the strategy execution
            
        Raises:
            ValueError: If no strategy is set
        """
        if self._strategy is None:
            raise ValueError("No strategy set")
        return self._strategy.execute(data)


# Payment Processing Example

class PaymentStrategy(ABC):
    """Abstract base class for payment strategies."""
    
    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment and return success status.
        
        Args:
            amount: Amount to pay
            
        Returns:
            True if payment successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_payment_details(self) -> str:
        """Get human-readable payment method details.
        
        Returns:
            Payment method description
        """
        pass


class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy."""
    
    def __init__(self, card_number: str, cardholder: str, cvv: str, expiry: str):
        """Initialize credit card payment.
        
        Args:
            card_number: Credit card number
            cardholder: Name on the card
            cvv: Security code
            expiry: Expiry date (MM/YY format)
        """
        self.card_number = card_number
        self.cardholder = cardholder
        self.cvv = cvv
        self.expiry = expiry
    
    def pay(self, amount: float) -> bool:
        """Process credit card payment.
        
        Args:
            amount: Amount to pay
            
        Returns:
            True if payment successful, False otherwise
        """
        # Validation
        if len(self.card_number) != 16 or not self.card_number.isdigit():
            print("❌ Invalid card number")
            return False
        
        if len(self.cvv) != 3 or not self.cvv.isdigit():
            print("❌ Invalid CVV")
            return False
        
        print(f"💳 Processing credit card payment of ${amount:.2f}")
        print(f"   Card: **** **** **** {self.card_number[-4:]}")
        print(f"   Cardholder: {self.cardholder}")
        print("✅ Credit card payment successful")
        return True
    
    def get_payment_details(self) -> str:
        """Get payment method details.
        
        Returns:
            Payment method description
        """
        return f"Credit Card ending in {self.card_number[-4:]}"


class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy."""
    
    def __init__(self, email: str, password: str):
        """Initialize PayPal payment.
        
        Args:
            email: PayPal account email
            password: PayPal account password
        """
        self.email = email
        self.password = password
    
    def pay(self, amount: float) -> bool:
        """Process PayPal payment.
        
        Args:
            amount: Amount to pay
            
        Returns:
            True if payment successful, False otherwise
        """
        # Validation
        if "@" not in self.email or "." not in self.email:
            print("❌ Invalid email address")
            return False
        
        if len(self.password) < 6:
            print("❌ Password too short")
            return False
        
        print(f"🅿️ Processing PayPal payment of ${amount:.2f}")
        print(f"   Account: {self.email}")
        print("✅ PayPal payment successful")
        return True
    
    def get_payment_details(self) -> str:
        """Get payment method details.
        
        Returns:
            Payment method description
        """
        return f"PayPal ({self.email})"


class CryptocurrencyPayment(PaymentStrategy):
    """Cryptocurrency payment strategy."""
    
    def __init__(self, wallet_address: str, private_key: str, currency: str = "Bitcoin"):
        """Initialize cryptocurrency payment.
        
        Args:
            wallet_address: Wallet address
            private_key: Private key for transaction signing
            currency: Type of cryptocurrency
        """
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.currency = currency
    
    def pay(self, amount: float) -> bool:
        """Process cryptocurrency payment.
        
        Args:
            amount: Amount to pay
            
        Returns:
            True if payment successful, False otherwise
        """
        # Validation
        if len(self.wallet_address) < 26:
            print("❌ Invalid wallet address")
            return False
        
        print(f"₿ Processing {self.currency} payment of ${amount:.2f}")
        print(f"   Wallet: {self.wallet_address[:10]}...{self.wallet_address[-6:]}")
        print(f"   Broadcasting transaction to {self.currency} network...")
        print("✅ Cryptocurrency payment successful")
        return True
    
    def get_payment_details(self) -> str:
        """Get payment method details.
        
        Returns:
            Payment method description
        """
        return f"{self.currency} Wallet ({self.wallet_address[:10]}...)"


class ShoppingCart:
    """Shopping cart that can use different payment strategies."""
    
    def __init__(self):
        """Initialize the shopping cart."""
        self.items: List[Dict[str, Union[str, float]]] = []
        self.payment_strategy: Optional[PaymentStrategy] = None
    
    def add_item(self, name: str, price: float) -> None:
        """Add an item to the cart.
        
        Args:
            name: Item name
            price: Item price
        """
        self.items.append({"name": name, "price": price})
        print(f"Added {name} (${price:.2f}) to cart")
    
    def get_total(self) -> float:
        """Calculate total price of items in cart.
        
        Returns:
            Total price
        """
        return sum(item["price"] for item in self.items)
    
    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Set the payment strategy.
        
        Args:
            strategy: Payment strategy to use
        """
        self.payment_strategy = strategy
        print(f"Payment method set to: {strategy.get_payment_details()}")
    
    def checkout(self) -> bool:
        """Process checkout using the selected payment strategy.
        
        Returns:
            True if checkout successful, False otherwise
        """
        if not self.payment_strategy:
            print("❌ No payment method selected")
            return False
        
        if not self.items:
            print("❌ Cart is empty")
            return False
        
        total = self.get_total()
        print(f"\n🛒 Checkout: {len(self.items)} items, Total: ${total:.2f}")
        
        if self.payment_strategy.pay(total):
            print("📦 Order confirmed and will be shipped!")
            return True
        else:
            print("❌ Payment failed - order cancelled")
            return False


# Sorting Algorithm Example

class SortingStrategy(ABC):
    """Abstract base class for sorting strategies."""
    
    @abstractmethod
    def sort(self, data: List[Any]) -> List[Any]:
        """Sort the data using this strategy.
        
        Args:
            data: List of items to sort
            
        Returns:
            Sorted list
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get the name of this sorting algorithm.
        
        Returns:
            Algorithm name
        """
        pass
    
    @abstractmethod
    def get_time_complexity(self) -> str:
        """Get the time complexity of this algorithm.
        
        Returns:
            Time complexity in Big O notation
        """
        pass


class BubbleSort(SortingStrategy):
    """Bubble sort implementation - simple but inefficient."""
    
    def sort(self, data: List[Any]) -> List[Any]:
        """Sort using bubble sort algorithm.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        data = data.copy()  # Don't modify original
        n = len(data)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        
        return data
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            Algorithm name
        """
        return "Bubble Sort"
    
    def get_time_complexity(self) -> str:
        """Get time complexity.
        
        Returns:
            Time complexity
        """
        return "O(n²)"


class QuickSort(SortingStrategy):
    """Quick sort implementation - efficient divide-and-conquer algorithm."""
    
    def sort(self, data: List[Any]) -> List[Any]:
        """Sort using quick sort algorithm.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        return self._quicksort(data.copy())
    
    def _quicksort(self, data: List[Any]) -> List[Any]:
        """Recursive quicksort implementation.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        if len(data) <= 1:
            return data
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self._quicksort(left) + middle + self._quicksort(right)
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            Algorithm name
        """
        return "Quick Sort"
    
    def get_time_complexity(self) -> str:
        """Get time complexity.
        
        Returns:
            Time complexity
        """
        return "O(n log n)"


class MergeSort(SortingStrategy):
    """Merge sort implementation - stable and efficient."""
    
    def sort(self, data: List[Any]) -> List[Any]:
        """Sort using merge sort algorithm.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        return self._mergesort(data.copy())
    
    def _mergesort(self, data: List[Any]) -> List[Any]:
        """Recursive merge sort implementation.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self._mergesort(data[:mid])
        right = self._mergesort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[Any], right: List[Any]) -> List[Any]:
        """Merge two sorted lists.
        
        Args:
            left: Left sorted list
            right: Right sorted list
            
        Returns:
            Merged sorted list
        """
        result = []
        i, j = 0, 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def get_name(self) -> str:
        """Get algorithm name.
        
        Returns:
            Algorithm name
        """
        return "Merge Sort"
    
    def get_time_complexity(self) -> str:
        """Get time complexity.
        
        Returns:
            Time complexity
        """
        return "O(n log n)"


class DataSorter:
    """Data sorter that can use different sorting strategies."""
    
    def __init__(self, strategy: Optional[SortingStrategy] = None):
        """Initialize the data sorter.
        
        Args:
            strategy: Sorting strategy to use
        """
        self.strategy = strategy
        self.data: List[Any] = []
    
    def set_strategy(self, strategy: SortingStrategy) -> None:
        """Set the sorting strategy.
        
        Args:
            strategy: Sorting strategy to use
        """
        self.strategy = strategy
    
    def add_data(self, data: List[Any]) -> None:
        """Add data to be sorted.
        
        Args:
            data: Data to add
        """
        self.data.extend(data)
    
    def sort_data(self) -> List[Any]:
        """Sort the data using the current strategy.
        
        Returns:
            Sorted data
            
        Raises:
            ValueError: If no strategy is set
        """
        if not self.strategy:
            raise ValueError("No sorting strategy set")
        
        if not self.data:
            return []
        
        print(f"Sorting {len(self.data)} items using {self.strategy.get_name()}")
        print(f"Time complexity: {self.strategy.get_time_complexity()}")
        
        start_time = time.time()
        sorted_data = self.strategy.sort(self.data)
        end_time = time.time()
        
        print(f"Sorting completed in {(end_time - start_time) * 1000:.2f}ms")
        return sorted_data
    
    def benchmark_strategies(self, strategies: List[SortingStrategy]) -> Dict[str, float]:
        """Benchmark different sorting strategies.
        
        Args:
            strategies: List of strategies to benchmark
            
        Returns:
            Dictionary mapping strategy names to execution times
        """
        results = {}
        
        for strategy in strategies:
            self.set_strategy(strategy)
            
            start_time = time.time()
            self.sort_data()
            end_time = time.time()
            
            execution_time = (end_time - start_time) * 1000
            results[strategy.get_name()] = execution_time
        
        return results


# Discount Calculation Example

class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""
    
    @abstractmethod
    def calculate_discount(self, amount: float) -> float:
        """Calculate discount amount.
        
        Args:
            amount: Original amount
            
        Returns:
            Discount amount
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get discount description.
        
        Returns:
            Discount description
        """
        pass


class PercentageDiscount(DiscountStrategy):
    """Percentage-based discount strategy."""
    
    def __init__(self, percentage: float):
        """Initialize percentage discount.
        
        Args:
            percentage: Discount percentage (0-100)
        """
        self.percentage = max(0, min(100, percentage))
    
    def calculate_discount(self, amount: float) -> float:
        """Calculate percentage discount.
        
        Args:
            amount: Original amount
            
        Returns:
            Discount amount
        """
        return amount * (self.percentage / 100)
    
    def get_description(self) -> str:
        """Get discount description.
        
        Returns:
            Discount description
        """
        return f"{self.percentage}% off"


class FixedAmountDiscount(DiscountStrategy):
    """Fixed amount discount strategy."""
    
    def __init__(self, amount: float):
        """Initialize fixed amount discount.
        
        Args:
            amount: Fixed discount amount
        """
        self.amount = max(0, amount)
    
    def calculate_discount(self, amount: float) -> float:
        """Calculate fixed amount discount.
        
        Args:
            amount: Original amount
            
        Returns:
            Discount amount
        """
        return min(self.amount, amount)  # Don't discount more than the total
    
    def get_description(self) -> str:
        """Get discount description.
        
        Returns:
            Discount description
        """
        return f"${self.amount:.2f} off"


class BuyOneGetOneDiscount(DiscountStrategy):
    """Buy one get one discount strategy."""
    
    def __init__(self, item_price: float):
        """Initialize BOGO discount.
        
        Args:
            item_price: Price of the item for BOGO calculation
        """
        self.item_price = item_price
    
    def calculate_discount(self, amount: float) -> float:
        """Calculate BOGO discount.
        
        Args:
            amount: Original amount
            
        Returns:
            Discount amount
        """
        if amount < self.item_price * 2:
            return 0  # Need at least 2 items for BOGO
        
        # Number of free items (every second item is free)
        num_items = amount // self.item_price
        free_items = num_items // 2
        
        return free_items * self.item_price
    
    def get_description(self) -> str:
        """Get discount description.
        
        Returns:
            Discount description
        """
        return f"Buy one get one free (${self.item_price:.2f} items)"


class PriceCalculator:
    """Price calculator that can use different discount strategies."""
    
    def __init__(self):
        """Initialize the price calculator."""
        self.discount_strategy: Optional[DiscountStrategy] = None
    
    def set_discount_strategy(self, strategy: DiscountStrategy) -> None:
        """Set the discount strategy.
        
        Args:
            strategy: Discount strategy to use
        """
        self.discount_strategy = strategy
    
    def calculate_final_price(self, original_price: float) -> Tuple[float, float, float]:
        """Calculate final price with discount.
        
        Args:
            original_price: Original price before discount
            
        Returns:
            Tuple of (original_price, discount_amount, final_price)
        """
        if not self.discount_strategy:
            return original_price, 0.0, original_price
        
        discount_amount = self.discount_strategy.calculate_discount(original_price)
        final_price = original_price - discount_amount
        
        return original_price, discount_amount, final_price
    
    def print_price_breakdown(self, original_price: float) -> None:
        """Print detailed price breakdown.
        
        Args:
            original_price: Original price before discount
        """
        original, discount, final = self.calculate_final_price(original_price)
        
        print(f"Price Breakdown:")
        print(f"  Original Price: ${original:.2f}")
        
        if self.discount_strategy:
            print(f"  Discount ({self.discount_strategy.get_description()}): -${discount:.2f}")
        else:
            print(f"  Discount: -${discount:.2f}")
        
        print(f"  Final Price: ${final:.2f}")
        
        if discount > 0:
            savings_percent = (discount / original) * 100
            print(f"  You save: ${discount:.2f} ({savings_percent:.1f}%)")


# Example usage functions

def demonstrate_payment_strategies():
    """Demonstrate different payment strategies."""
    print("=== Payment Strategy Demo ===")
    
    # Create shopping cart
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 25.99)
    cart.add_item("Keyboard", 75.50)
    
    # Try different payment methods
    print("\n--- Credit Card Payment ---")
    credit_card = CreditCardPayment("1234567890123456", "John Doe", "123", "12/25")
    cart.set_payment_strategy(credit_card)
    cart.checkout()
    
    print("\n--- PayPal Payment ---")
    paypal = PayPalPayment("john.doe@email.com", "password123")
    cart.set_payment_strategy(paypal)
    cart.checkout()
    
    print("\n--- Cryptocurrency Payment ---")
    crypto = CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key_123")
    cart.set_payment_strategy(crypto)
    cart.checkout()


def demonstrate_sorting_strategies():
    """Demonstrate different sorting strategies."""
    print("\n=== Sorting Strategy Demo ===")
    
    # Create data sorter
    sorter = DataSorter()
    import random
    data = [random.randint(1, 100) for _ in range(20)]
    sorter.add_data(data)
    
    print(f"Original data: {data}")
    
    # Try different sorting algorithms
    strategies = [BubbleSort(), QuickSort(), MergeSort()]
    
    for strategy in strategies:
        print(f"\n--- {strategy.get_name()} ---")
        sorter.set_strategy(strategy)
        sorted_data = sorter.sort_data()
        print(f"Sorted data: {sorted_data[:10]}...")  # Show first 10 items
    
    # Benchmark strategies
    print("\n--- Benchmark Results ---")
    results = sorter.benchmark_strategies(strategies)
    for name, time_ms in results.items():
        print(f"{name}: {time_ms:.2f}ms")


def demonstrate_discount_strategies():
    """Demonstrate different discount strategies."""
    print("\n=== Discount Strategy Demo ===")
    
    calculator = PriceCalculator()
    original_price = 100.00
    
    # Try different discount strategies
    strategies = [
        PercentageDiscount(20),
        FixedAmountDiscount(15.00),
        BuyOneGetOneDiscount(25.00)
    ]
    
    for strategy in strategies:
        print(f"\n--- {strategy.get_description()} ---")
        calculator.set_discount_strategy(strategy)
        calculator.print_price_breakdown(original_price)


if __name__ == "__main__":
    demonstrate_payment_strategies()
    demonstrate_sorting_strategies()
    demonstrate_discount_strategies()