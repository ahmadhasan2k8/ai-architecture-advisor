"""State pattern implementations.

This module provides implementations of the State pattern, demonstrating
how to allow an object to alter its behavior when its internal state changes.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


# Abstract State Interface

class State(ABC):
    """Abstract base class for states."""
    
    @abstractmethod
    def handle(self, context: 'Context') -> None:
        """Handle the state-specific behavior.
        
        Args:
            context: The context object
        """
        pass


class Context:
    """Context class that delegates behavior to the current state."""
    
    def __init__(self, initial_state: State):
        """Initialize the context with an initial state.
        
        Args:
            initial_state: The initial state
        """
        self._state = initial_state
    
    def set_state(self, state: State) -> None:
        """Change the current state.
        
        Args:
            state: The new state
        """
        self._state = state
    
    def get_state(self) -> State:
        """Get the current state.
        
        Returns:
            Current state
        """
        return self._state
    
    def request(self) -> None:
        """Handle a request by delegating to the current state."""
        self._state.handle(self)


# Vending Machine Example

class VendingMachineState(ABC):
    """Abstract base class for vending machine states."""
    
    @abstractmethod
    def insert_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin insertion.
        
        Args:
            machine: The vending machine
        """
        pass
    
    @abstractmethod
    def select_product(self, machine: 'VendingMachine', product: str) -> None:
        """Handle product selection.
        
        Args:
            machine: The vending machine
            product: Selected product
        """
        pass
    
    @abstractmethod
    def dispense(self, machine: 'VendingMachine') -> None:
        """Handle product dispensing.
        
        Args:
            machine: The vending machine
        """
        pass
    
    @abstractmethod
    def return_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin return.
        
        Args:
            machine: The vending machine
        """
        pass


class WaitingState(VendingMachineState):
    """State when machine is waiting for a coin."""
    
    def insert_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin insertion.
        
        Args:
            machine: The vending machine
        """
        print("Coin inserted. Please select a product.")
        machine.set_state(machine.coin_inserted_state)
    
    def select_product(self, machine: 'VendingMachine', product: str) -> None:
        """Handle product selection.
        
        Args:
            machine: The vending machine
            product: Selected product
        """
        print("Please insert a coin first.")
    
    def dispense(self, machine: 'VendingMachine') -> None:
        """Handle product dispensing.
        
        Args:
            machine: The vending machine
        """
        print("Please insert a coin first.")
    
    def return_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin return.
        
        Args:
            machine: The vending machine
        """
        print("No coin to return.")


class CoinInsertedState(VendingMachineState):
    """State when a coin has been inserted."""
    
    def insert_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin insertion.
        
        Args:
            machine: The vending machine
        """
        print("Coin already inserted. Please select a product.")
    
    def select_product(self, machine: 'VendingMachine', product: str) -> None:
        """Handle product selection.
        
        Args:
            machine: The vending machine
            product: Selected product
        """
        if product in machine.inventory and machine.inventory[product] > 0:
            print(f"Product '{product}' selected. Dispensing...")
            machine.selected_product = product
            machine.set_state(machine.dispensing_state)
        else:
            print(f"Product '{product}' not available. Returning coin.")
            machine.set_state(machine.waiting_state)
    
    def dispense(self, machine: 'VendingMachine') -> None:
        """Handle product dispensing.
        
        Args:
            machine: The vending machine
        """
        print("Please select a product first.")
    
    def return_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin return.
        
        Args:
            machine: The vending machine
        """
        print("Coin returned.")
        machine.set_state(machine.waiting_state)


class DispensingState(VendingMachineState):
    """State when machine is dispensing a product."""
    
    def insert_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin insertion.
        
        Args:
            machine: The vending machine
        """
        print("Please wait, dispensing product...")
    
    def select_product(self, machine: 'VendingMachine', product: str) -> None:
        """Handle product selection.
        
        Args:
            machine: The vending machine
            product: Selected product
        """
        print("Please wait, dispensing product...")
    
    def dispense(self, machine: 'VendingMachine') -> None:
        """Handle product dispensing.
        
        Args:
            machine: The vending machine
        """
        if machine.selected_product and machine.selected_product in machine.inventory:
            product = machine.selected_product
            machine.inventory[product] -= 1
            print(f"Product '{product}' dispensed. Thank you!")
            machine.selected_product = None
            
            if machine.inventory[product] == 0:
                print(f"Product '{product}' is now out of stock.")
            
            machine.set_state(machine.waiting_state)
        else:
            print("Error dispensing product. Returning coin.")
            machine.set_state(machine.waiting_state)
    
    def return_coin(self, machine: 'VendingMachine') -> None:
        """Handle coin return.
        
        Args:
            machine: The vending machine
        """
        print("Cannot return coin while dispensing.")


class VendingMachine:
    """Vending machine that uses the State pattern."""
    
    def __init__(self):
        """Initialize the vending machine."""
        # Initialize states
        self.waiting_state = WaitingState()
        self.coin_inserted_state = CoinInsertedState()
        self.dispensing_state = DispensingState()
        
        # Set initial state
        self._state = self.waiting_state
        
        # Initialize inventory
        self.inventory = {
            "Coke": 5,
            "Pepsi": 3,
            "Water": 10,
            "Chips": 2
        }
        
        self.selected_product: Optional[str] = None
    
    def set_state(self, state: VendingMachineState) -> None:
        """Change the current state.
        
        Args:
            state: The new state
        """
        self._state = state
    
    def get_state(self) -> VendingMachineState:
        """Get the current state.
        
        Returns:
            Current state
        """
        return self._state
    
    def insert_coin(self) -> None:
        """Insert a coin."""
        self._state.insert_coin(self)
    
    def select_product(self, product: str) -> None:
        """Select a product.
        
        Args:
            product: Product name
        """
        self._state.select_product(self, product)
    
    def dispense(self) -> None:
        """Dispense the selected product."""
        self._state.dispense(self)
    
    def return_coin(self) -> None:
        """Return the inserted coin."""
        self._state.return_coin(self)
    
    def show_inventory(self) -> None:
        """Display current inventory."""
        print("Current inventory:")
        for product, quantity in self.inventory.items():
            print(f"  {product}: {quantity}")


# Traffic Light Example

class TrafficLightState(ABC):
    """Abstract base class for traffic light states."""
    
    @abstractmethod
    def change(self, light: 'TrafficLight') -> None:
        """Change to the next state.
        
        Args:
            light: The traffic light
        """
        pass
    
    @abstractmethod
    def get_color(self) -> str:
        """Get the current light color.
        
        Returns:
            Color of the light
        """
        pass


class RedState(TrafficLightState):
    """Red light state."""
    
    def change(self, light: 'TrafficLight') -> None:
        """Change to green light.
        
        Args:
            light: The traffic light
        """
        print("Red light -> Green light")
        light.set_state(light.green_state)
    
    def get_color(self) -> str:
        """Get the current light color.
        
        Returns:
            Color of the light
        """
        return "Red"


class YellowState(TrafficLightState):
    """Yellow light state."""
    
    def change(self, light: 'TrafficLight') -> None:
        """Change to red light.
        
        Args:
            light: The traffic light
        """
        print("Yellow light -> Red light")
        light.set_state(light.red_state)
    
    def get_color(self) -> str:
        """Get the current light color.
        
        Returns:
            Color of the light
        """
        return "Yellow"


class GreenState(TrafficLightState):
    """Green light state."""
    
    def change(self, light: 'TrafficLight') -> None:
        """Change to yellow light.
        
        Args:
            light: The traffic light
        """
        print("Green light -> Yellow light")
        light.set_state(light.yellow_state)
    
    def get_color(self) -> str:
        """Get the current light color.
        
        Returns:
            Color of the light
        """
        return "Green"


class TrafficLight:
    """Traffic light that uses the State pattern."""
    
    def __init__(self):
        """Initialize the traffic light."""
        # Initialize states
        self.red_state = RedState()
        self.yellow_state = YellowState()
        self.green_state = GreenState()
        
        # Set initial state
        self._state = self.red_state
    
    def set_state(self, state: TrafficLightState) -> None:
        """Change the current state.
        
        Args:
            state: The new state
        """
        self._state = state
    
    def get_state(self) -> TrafficLightState:
        """Get the current state.
        
        Returns:
            Current state
        """
        return self._state
    
    def change(self) -> None:
        """Change to the next state."""
        self._state.change(self)
    
    def get_color(self) -> str:
        """Get the current light color.
        
        Returns:
            Color of the light
        """
        return self._state.get_color()


# Media Player Example

class MediaPlayerState(ABC):
    """Abstract base class for media player states."""
    
    @abstractmethod
    def play(self, player: 'MediaPlayer') -> None:
        """Handle play action.
        
        Args:
            player: The media player
        """
        pass
    
    @abstractmethod
    def pause(self, player: 'MediaPlayer') -> None:
        """Handle pause action.
        
        Args:
            player: The media player
        """
        pass
    
    @abstractmethod
    def stop(self, player: 'MediaPlayer') -> None:
        """Handle stop action.
        
        Args:
            player: The media player
        """
        pass


class StoppedState(MediaPlayerState):
    """State when media player is stopped."""
    
    def play(self, player: 'MediaPlayer') -> None:
        """Handle play action.
        
        Args:
            player: The media player
        """
        print("Starting playback...")
        player.set_state(player.playing_state)
    
    def pause(self, player: 'MediaPlayer') -> None:
        """Handle pause action.
        
        Args:
            player: The media player
        """
        print("Player is stopped. Cannot pause.")
    
    def stop(self, player: 'MediaPlayer') -> None:
        """Handle stop action.
        
        Args:
            player: The media player
        """
        print("Player is already stopped.")


class PlayingState(MediaPlayerState):
    """State when media player is playing."""
    
    def play(self, player: 'MediaPlayer') -> None:
        """Handle play action.
        
        Args:
            player: The media player
        """
        print("Already playing.")
    
    def pause(self, player: 'MediaPlayer') -> None:
        """Handle pause action.
        
        Args:
            player: The media player
        """
        print("Pausing playback...")
        player.set_state(player.paused_state)
    
    def stop(self, player: 'MediaPlayer') -> None:
        """Handle stop action.
        
        Args:
            player: The media player
        """
        print("Stopping playback...")
        player.set_state(player.stopped_state)


class PausedState(MediaPlayerState):
    """State when media player is paused."""
    
    def play(self, player: 'MediaPlayer') -> None:
        """Handle play action.
        
        Args:
            player: The media player
        """
        print("Resuming playback...")
        player.set_state(player.playing_state)
    
    def pause(self, player: 'MediaPlayer') -> None:
        """Handle pause action.
        
        Args:
            player: The media player
        """
        print("Already paused.")
    
    def stop(self, player: 'MediaPlayer') -> None:
        """Handle stop action.
        
        Args:
            player: The media player
        """
        print("Stopping playback...")
        player.set_state(player.stopped_state)


class MediaPlayer:
    """Media player that uses the State pattern."""
    
    def __init__(self):
        """Initialize the media player."""
        # Initialize states
        self.stopped_state = StoppedState()
        self.playing_state = PlayingState()
        self.paused_state = PausedState()
        
        # Set initial state
        self._state = self.stopped_state
    
    def set_state(self, state: MediaPlayerState) -> None:
        """Change the current state.
        
        Args:
            state: The new state
        """
        self._state = state
    
    def get_state(self) -> MediaPlayerState:
        """Get the current state.
        
        Returns:
            Current state
        """
        return self._state
    
    def play(self) -> None:
        """Play media."""
        self._state.play(self)
    
    def pause(self) -> None:
        """Pause media."""
        self._state.pause(self)
    
    def stop(self) -> None:
        """Stop media."""
        self._state.stop(self)
    
    def get_status(self) -> str:
        """Get current player status.
        
        Returns:
            Current status
        """
        return self._state.__class__.__name__.replace("State", "")


# Order Processing Example

class OrderState(ABC):
    """Abstract base class for order states."""
    
    @abstractmethod
    def pay(self, order: 'Order') -> None:
        """Handle payment.
        
        Args:
            order: The order
        """
        pass
    
    @abstractmethod
    def ship(self, order: 'Order') -> None:
        """Handle shipping.
        
        Args:
            order: The order
        """
        pass
    
    @abstractmethod
    def cancel(self, order: 'Order') -> None:
        """Handle cancellation.
        
        Args:
            order: The order
        """
        pass


class PendingState(OrderState):
    """State when order is pending payment."""
    
    def pay(self, order: 'Order') -> None:
        """Handle payment.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} payment received. Processing...")
        order.set_state(order.paid_state)
    
    def ship(self, order: 'Order') -> None:
        """Handle shipping.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} cannot be shipped. Payment required.")
    
    def cancel(self, order: 'Order') -> None:
        """Handle cancellation.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} cancelled.")
        order.set_state(order.cancelled_state)


class PaidState(OrderState):
    """State when order is paid."""
    
    def pay(self, order: 'Order') -> None:
        """Handle payment.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is already paid.")
    
    def ship(self, order: 'Order') -> None:
        """Handle shipping.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} shipped.")
        order.set_state(order.shipped_state)
    
    def cancel(self, order: 'Order') -> None:
        """Handle cancellation.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} cancelled. Processing refund...")
        order.set_state(order.cancelled_state)


class ShippedState(OrderState):
    """State when order is shipped."""
    
    def pay(self, order: 'Order') -> None:
        """Handle payment.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is already paid and shipped.")
    
    def ship(self, order: 'Order') -> None:
        """Handle shipping.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is already shipped.")
    
    def cancel(self, order: 'Order') -> None:
        """Handle cancellation.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is already shipped. Cannot cancel.")


class CancelledState(OrderState):
    """State when order is cancelled."""
    
    def pay(self, order: 'Order') -> None:
        """Handle payment.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is cancelled. Cannot process payment.")
    
    def ship(self, order: 'Order') -> None:
        """Handle shipping.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is cancelled. Cannot ship.")
    
    def cancel(self, order: 'Order') -> None:
        """Handle cancellation.
        
        Args:
            order: The order
        """
        print(f"Order {order.id} is already cancelled.")


class Order:
    """Order that uses the State pattern."""
    
    def __init__(self, order_id: str):
        """Initialize the order.
        
        Args:
            order_id: Order ID
        """
        self.id = order_id
        
        # Initialize states
        self.pending_state = PendingState()
        self.paid_state = PaidState()
        self.shipped_state = ShippedState()
        self.cancelled_state = CancelledState()
        
        # Set initial state
        self._state = self.pending_state
    
    def set_state(self, state: OrderState) -> None:
        """Change the current state.
        
        Args:
            state: The new state
        """
        self._state = state
    
    def get_state(self) -> OrderState:
        """Get the current state.
        
        Returns:
            Current state
        """
        return self._state
    
    def pay(self) -> None:
        """Process payment."""
        self._state.pay(self)
    
    def ship(self) -> None:
        """Ship the order."""
        self._state.ship(self)
    
    def cancel(self) -> None:
        """Cancel the order."""
        self._state.cancel(self)
    
    def get_status(self) -> str:
        """Get current order status.
        
        Returns:
            Current status
        """
        return self._state.__class__.__name__.replace("State", "")


# Example usage functions

def demonstrate_vending_machine():
    """Demonstrate vending machine state pattern."""
    print("=== Vending Machine State Demo ===")
    
    machine = VendingMachine()
    machine.show_inventory()
    
    print("\n1. Try to select product without coin:")
    machine.select_product("Coke")
    
    print("\n2. Insert coin and select product:")
    machine.insert_coin()
    machine.select_product("Coke")
    machine.dispense()
    
    print("\n3. Insert coin and return it:")
    machine.insert_coin()
    machine.return_coin()
    
    print("\n4. Try to select out of stock product:")
    machine.insert_coin()
    machine.select_product("Chips")
    machine.dispense()
    machine.insert_coin()
    machine.select_product("Chips")
    machine.dispense()
    machine.insert_coin()
    machine.select_product("Chips")  # Out of stock


def demonstrate_traffic_light():
    """Demonstrate traffic light state pattern."""
    print("\n=== Traffic Light State Demo ===")
    
    light = TrafficLight()
    
    print(f"Initial state: {light.get_color()}")
    
    for i in range(6):
        light.change()
        print(f"Current state: {light.get_color()}")


def demonstrate_media_player():
    """Demonstrate media player state pattern."""
    print("\n=== Media Player State Demo ===")
    
    player = MediaPlayer()
    
    print(f"Initial status: {player.get_status()}")
    
    player.play()
    print(f"Status: {player.get_status()}")
    
    player.pause()
    print(f"Status: {player.get_status()}")
    
    player.play()
    print(f"Status: {player.get_status()}")
    
    player.stop()
    print(f"Status: {player.get_status()}")
    
    player.pause()  # Should show error


def demonstrate_order_processing():
    """Demonstrate order processing state pattern."""
    print("\n=== Order Processing State Demo ===")
    
    order = Order("ORD-001")
    
    print(f"Order {order.id} status: {order.get_status()}")
    
    order.ship()  # Should fail
    
    order.pay()
    print(f"Order {order.id} status: {order.get_status()}")
    
    order.ship()
    print(f"Order {order.id} status: {order.get_status()}")
    
    order.cancel()  # Should fail (already shipped)
    
    # Test cancellation
    order2 = Order("ORD-002")
    order2.pay()
    order2.cancel()
    print(f"Order {order2.id} status: {order2.get_status()}")


if __name__ == "__main__":
    demonstrate_vending_machine()
    demonstrate_traffic_light()
    demonstrate_media_player()
    demonstrate_order_processing()