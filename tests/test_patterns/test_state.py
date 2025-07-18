"""Test suite for the State pattern implementation."""

import sys
from io import StringIO
from typing import Any, Dict, List, Optional
from unittest.mock import Mock, patch

import pytest

from src.patterns.state import (  # Abstract classes; Vending Machine implementations; Traffic Light implementations; Media Player implementations; Order Processing implementations; Demo functions
    CancelledState,
    CoinInsertedState,
    Context,
    DispensingState,
    GreenState,
    MediaPlayer,
    MediaPlayerState,
    Order,
    OrderState,
    PaidState,
    PausedState,
    PendingState,
    PlayingState,
    RedState,
    ShippedState,
    State,
    StoppedState,
    TrafficLight,
    TrafficLightState,
    VendingMachine,
    VendingMachineState,
    WaitingState,
    YellowState,
    demonstrate_media_player,
    demonstrate_order_processing,
    demonstrate_traffic_light,
    demonstrate_vending_machine,
)


class TestBasicStatePattern:
    """Test the basic State pattern implementation."""

    def test_context_initialization(self):
        """Test context initialization with initial state."""
        initial_state = Mock(spec=State)
        context = Context(initial_state)

        assert context.get_state() == initial_state

    def test_context_state_change(self):
        """Test context state changes."""
        initial_state = Mock(spec=State)
        new_state = Mock(spec=State)

        context = Context(initial_state)
        context.set_state(new_state)

        assert context.get_state() == new_state

    def test_context_request_delegation(self):
        """Test context delegates requests to current state."""
        state = Mock(spec=State)
        context = Context(state)

        context.request()

        state.handle.assert_called_once_with(context)

    def test_context_state_change_during_request(self):
        """Test state can change during request handling."""
        initial_state = Mock(spec=State)
        new_state = Mock(spec=State)

        def change_state(ctx):
            ctx.set_state(new_state)

        initial_state.handle = change_state
        context = Context(initial_state)

        context.request()

        assert context.get_state() == new_state


class TestVendingMachine:
    """Test the VendingMachine state pattern implementation."""

    @pytest.fixture
    def vending_machine(self):
        """Create a vending machine for testing."""
        return VendingMachine()

    def test_vending_machine_initialization(self, vending_machine):
        """Test vending machine initialization."""
        assert isinstance(vending_machine.get_state(), WaitingState)
        assert vending_machine.inventory == {
            "Coke": 5,
            "Pepsi": 3,
            "Water": 10,
            "Chips": 2,
        }
        assert vending_machine.selected_product is None

    def test_waiting_state_insert_coin(self, vending_machine, capsys):
        """Test coin insertion in waiting state."""
        vending_machine.insert_coin()
        captured = capsys.readouterr()

        assert "Coin inserted. Please select a product." in captured.out
        assert isinstance(vending_machine.get_state(), CoinInsertedState)

    def test_waiting_state_select_product(self, vending_machine, capsys):
        """Test product selection in waiting state."""
        vending_machine.select_product("Coke")
        captured = capsys.readouterr()

        assert "Please insert a coin first." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_waiting_state_dispense(self, vending_machine, capsys):
        """Test dispensing in waiting state."""
        vending_machine.dispense()
        captured = capsys.readouterr()

        assert "Please insert a coin first." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_waiting_state_return_coin(self, vending_machine, capsys):
        """Test coin return in waiting state."""
        vending_machine.return_coin()
        captured = capsys.readouterr()

        assert "No coin to return." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_coin_inserted_state_insert_coin(self, vending_machine, capsys):
        """Test coin insertion in coin inserted state."""
        vending_machine.insert_coin()  # Move to coin inserted state
        vending_machine.insert_coin()  # Try to insert another coin
        captured = capsys.readouterr()

        assert "Coin already inserted. Please select a product." in captured.out
        assert isinstance(vending_machine.get_state(), CoinInsertedState)

    def test_coin_inserted_state_select_available_product(
        self, vending_machine, capsys
    ):
        """Test selecting available product in coin inserted state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        captured = capsys.readouterr()

        assert "Product 'Coke' selected. Dispensing..." in captured.out
        assert isinstance(vending_machine.get_state(), DispensingState)
        assert vending_machine.selected_product == "Coke"

    def test_coin_inserted_state_select_unavailable_product(
        self, vending_machine, capsys
    ):
        """Test selecting unavailable product in coin inserted state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Invalid")
        captured = capsys.readouterr()

        assert "Product 'Invalid' not available. Returning coin." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_coin_inserted_state_select_out_of_stock_product(
        self, vending_machine, capsys
    ):
        """Test selecting out of stock product in coin inserted state."""
        vending_machine.inventory["Coke"] = 0
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        captured = capsys.readouterr()

        assert "Product 'Coke' not available. Returning coin." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_coin_inserted_state_dispense(self, vending_machine, capsys):
        """Test dispensing in coin inserted state."""
        vending_machine.insert_coin()
        vending_machine.dispense()
        captured = capsys.readouterr()

        assert "Please select a product first." in captured.out
        assert isinstance(vending_machine.get_state(), CoinInsertedState)

    def test_coin_inserted_state_return_coin(self, vending_machine, capsys):
        """Test coin return in coin inserted state."""
        vending_machine.insert_coin()
        vending_machine.return_coin()
        captured = capsys.readouterr()

        assert "Coin returned." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_dispensing_state_insert_coin(self, vending_machine, capsys):
        """Test coin insertion in dispensing state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        vending_machine.insert_coin()
        captured = capsys.readouterr()

        assert "Please wait, dispensing product..." in captured.out
        assert isinstance(vending_machine.get_state(), DispensingState)

    def test_dispensing_state_select_product(self, vending_machine, capsys):
        """Test product selection in dispensing state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        vending_machine.select_product("Pepsi")
        captured = capsys.readouterr()

        assert "Please wait, dispensing product..." in captured.out
        assert isinstance(vending_machine.get_state(), DispensingState)

    def test_dispensing_state_dispense_success(self, vending_machine, capsys):
        """Test successful dispensing in dispensing state."""
        initial_coke_count = vending_machine.inventory["Coke"]
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        vending_machine.dispense()
        captured = capsys.readouterr()

        assert "Product 'Coke' dispensed. Thank you!" in captured.out
        assert vending_machine.inventory["Coke"] == initial_coke_count - 1
        assert vending_machine.selected_product is None
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_dispensing_state_dispense_last_item(self, vending_machine, capsys):
        """Test dispensing the last item of a product."""
        vending_machine.inventory["Chips"] = 1
        vending_machine.insert_coin()
        vending_machine.select_product("Chips")
        vending_machine.dispense()
        captured = capsys.readouterr()

        assert "Product 'Chips' dispensed. Thank you!" in captured.out
        assert "Product 'Chips' is now out of stock." in captured.out
        assert vending_machine.inventory["Chips"] == 0

    def test_dispensing_state_dispense_error(self, vending_machine, capsys):
        """Test dispensing error in dispensing state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        vending_machine.selected_product = None  # Simulate error
        vending_machine.dispense()
        captured = capsys.readouterr()

        assert "Error dispensing product. Returning coin." in captured.out
        assert isinstance(vending_machine.get_state(), WaitingState)

    def test_dispensing_state_return_coin(self, vending_machine, capsys):
        """Test coin return in dispensing state."""
        vending_machine.insert_coin()
        vending_machine.select_product("Coke")
        vending_machine.return_coin()
        captured = capsys.readouterr()

        assert "Cannot return coin while dispensing." in captured.out
        assert isinstance(vending_machine.get_state(), DispensingState)

    def test_show_inventory(self, vending_machine, capsys):
        """Test inventory display."""
        vending_machine.show_inventory()
        captured = capsys.readouterr()

        assert "Current inventory:" in captured.out
        assert "Coke: 5" in captured.out
        assert "Pepsi: 3" in captured.out
        assert "Water: 10" in captured.out
        assert "Chips: 2" in captured.out


class TestTrafficLight:
    """Test the TrafficLight state pattern implementation."""

    @pytest.fixture
    def traffic_light(self):
        """Create a traffic light for testing."""
        return TrafficLight()

    def test_traffic_light_initialization(self, traffic_light):
        """Test traffic light initialization."""
        assert isinstance(traffic_light.get_state(), RedState)
        assert traffic_light.get_color() == "Red"

    def test_red_state_change(self, traffic_light, capsys):
        """Test changing from red state."""
        traffic_light.change()
        captured = capsys.readouterr()

        assert "Red light -> Green light" in captured.out
        assert isinstance(traffic_light.get_state(), GreenState)
        assert traffic_light.get_color() == "Green"

    def test_green_state_change(self, traffic_light, capsys):
        """Test changing from green state."""
        traffic_light.change()  # Red -> Green
        traffic_light.change()  # Green -> Yellow
        captured = capsys.readouterr()

        assert "Green light -> Yellow light" in captured.out
        assert isinstance(traffic_light.get_state(), YellowState)
        assert traffic_light.get_color() == "Yellow"

    def test_yellow_state_change(self, traffic_light, capsys):
        """Test changing from yellow state."""
        traffic_light.change()  # Red -> Green
        traffic_light.change()  # Green -> Yellow
        traffic_light.change()  # Yellow -> Red
        captured = capsys.readouterr()

        assert "Yellow light -> Red light" in captured.out
        assert isinstance(traffic_light.get_state(), RedState)
        assert traffic_light.get_color() == "Red"

    def test_traffic_light_cycle(self, traffic_light):
        """Test complete traffic light cycle."""
        # Initial state
        assert traffic_light.get_color() == "Red"

        # Complete cycle
        traffic_light.change()  # Red -> Green
        assert traffic_light.get_color() == "Green"

        traffic_light.change()  # Green -> Yellow
        assert traffic_light.get_color() == "Yellow"

        traffic_light.change()  # Yellow -> Red
        assert traffic_light.get_color() == "Red"

    def test_multiple_cycles(self, traffic_light):
        """Test multiple traffic light cycles."""
        colors = []
        for _ in range(9):  # 3 complete cycles
            colors.append(traffic_light.get_color())
            traffic_light.change()

        expected_colors = ["Red", "Green", "Yellow"] * 3
        assert colors == expected_colors


class TestMediaPlayer:
    """Test the MediaPlayer state pattern implementation."""

    @pytest.fixture
    def media_player(self):
        """Create a media player for testing."""
        return MediaPlayer()

    def test_media_player_initialization(self, media_player):
        """Test media player initialization."""
        assert isinstance(media_player.get_state(), StoppedState)
        assert media_player.get_status() == "Stopped"

    def test_stopped_state_play(self, media_player, capsys):
        """Test play action in stopped state."""
        media_player.play()
        captured = capsys.readouterr()

        assert "Starting playback..." in captured.out
        assert isinstance(media_player.get_state(), PlayingState)
        assert media_player.get_status() == "Playing"

    def test_stopped_state_pause(self, media_player, capsys):
        """Test pause action in stopped state."""
        media_player.pause()
        captured = capsys.readouterr()

        assert "Player is stopped. Cannot pause." in captured.out
        assert isinstance(media_player.get_state(), StoppedState)

    def test_stopped_state_stop(self, media_player, capsys):
        """Test stop action in stopped state."""
        media_player.stop()
        captured = capsys.readouterr()

        assert "Player is already stopped." in captured.out
        assert isinstance(media_player.get_state(), StoppedState)

    def test_playing_state_play(self, media_player, capsys):
        """Test play action in playing state."""
        media_player.play()  # Start playing
        media_player.play()  # Try to play again
        captured = capsys.readouterr()

        assert "Already playing." in captured.out
        assert isinstance(media_player.get_state(), PlayingState)

    def test_playing_state_pause(self, media_player, capsys):
        """Test pause action in playing state."""
        media_player.play()  # Start playing
        media_player.pause()  # Pause
        captured = capsys.readouterr()

        assert "Pausing playback..." in captured.out
        assert isinstance(media_player.get_state(), PausedState)
        assert media_player.get_status() == "Paused"

    def test_playing_state_stop(self, media_player, capsys):
        """Test stop action in playing state."""
        media_player.play()  # Start playing
        media_player.stop()  # Stop
        captured = capsys.readouterr()

        assert "Stopping playback..." in captured.out
        assert isinstance(media_player.get_state(), StoppedState)

    def test_paused_state_play(self, media_player, capsys):
        """Test play action in paused state."""
        media_player.play()  # Start playing
        media_player.pause()  # Pause
        media_player.play()  # Resume
        captured = capsys.readouterr()

        assert "Resuming playback..." in captured.out
        assert isinstance(media_player.get_state(), PlayingState)

    def test_paused_state_pause(self, media_player, capsys):
        """Test pause action in paused state."""
        media_player.play()  # Start playing
        media_player.pause()  # Pause
        media_player.pause()  # Try to pause again
        captured = capsys.readouterr()

        assert "Already paused." in captured.out
        assert isinstance(media_player.get_state(), PausedState)

    def test_paused_state_stop(self, media_player, capsys):
        """Test stop action in paused state."""
        media_player.play()  # Start playing
        media_player.pause()  # Pause
        media_player.stop()  # Stop
        captured = capsys.readouterr()

        assert "Stopping playback..." in captured.out
        assert isinstance(media_player.get_state(), StoppedState)

    def test_media_player_workflow(self, media_player):
        """Test complete media player workflow."""
        # Start stopped
        assert media_player.get_status() == "Stopped"

        # Play
        media_player.play()
        assert media_player.get_status() == "Playing"

        # Pause
        media_player.pause()
        assert media_player.get_status() == "Paused"

        # Resume
        media_player.play()
        assert media_player.get_status() == "Playing"

        # Stop
        media_player.stop()
        assert media_player.get_status() == "Stopped"


class TestOrderProcessing:
    """Test the Order state pattern implementation."""

    @pytest.fixture
    def order(self):
        """Create an order for testing."""
        return Order("TEST-001")

    def test_order_initialization(self, order):
        """Test order initialization."""
        assert order.id == "TEST-001"
        assert isinstance(order.get_state(), PendingState)
        assert order.get_status() == "Pending"

    def test_pending_state_pay(self, order, capsys):
        """Test payment in pending state."""
        order.pay()
        captured = capsys.readouterr()

        assert "Order TEST-001 payment received. Processing..." in captured.out
        assert isinstance(order.get_state(), PaidState)
        assert order.get_status() == "Paid"

    def test_pending_state_ship(self, order, capsys):
        """Test shipping in pending state."""
        order.ship()
        captured = capsys.readouterr()

        assert "Order TEST-001 cannot be shipped. Payment required." in captured.out
        assert isinstance(order.get_state(), PendingState)

    def test_pending_state_cancel(self, order, capsys):
        """Test cancellation in pending state."""
        order.cancel()
        captured = capsys.readouterr()

        assert "Order TEST-001 cancelled." in captured.out
        assert isinstance(order.get_state(), CancelledState)
        assert order.get_status() == "Cancelled"

    def test_paid_state_pay(self, order, capsys):
        """Test payment in paid state."""
        order.pay()  # Move to paid state
        order.pay()  # Try to pay again
        captured = capsys.readouterr()

        assert "Order TEST-001 is already paid." in captured.out
        assert isinstance(order.get_state(), PaidState)

    def test_paid_state_ship(self, order, capsys):
        """Test shipping in paid state."""
        order.pay()  # Move to paid state
        order.ship()  # Ship order
        captured = capsys.readouterr()

        assert "Order TEST-001 shipped." in captured.out
        assert isinstance(order.get_state(), ShippedState)
        assert order.get_status() == "Shipped"

    def test_paid_state_cancel(self, order, capsys):
        """Test cancellation in paid state."""
        order.pay()  # Move to paid state
        order.cancel()  # Cancel order
        captured = capsys.readouterr()

        assert "Order TEST-001 cancelled. Processing refund..." in captured.out
        assert isinstance(order.get_state(), CancelledState)

    def test_shipped_state_pay(self, order, capsys):
        """Test payment in shipped state."""
        order.pay()  # Move to paid state
        order.ship()  # Move to shipped state
        order.pay()  # Try to pay again
        captured = capsys.readouterr()

        assert "Order TEST-001 is already paid and shipped." in captured.out
        assert isinstance(order.get_state(), ShippedState)

    def test_shipped_state_ship(self, order, capsys):
        """Test shipping in shipped state."""
        order.pay()  # Move to paid state
        order.ship()  # Move to shipped state
        order.ship()  # Try to ship again
        captured = capsys.readouterr()

        assert "Order TEST-001 is already shipped." in captured.out
        assert isinstance(order.get_state(), ShippedState)

    def test_shipped_state_cancel(self, order, capsys):
        """Test cancellation in shipped state."""
        order.pay()  # Move to paid state
        order.ship()  # Move to shipped state
        order.cancel()  # Try to cancel
        captured = capsys.readouterr()

        assert "Order TEST-001 is already shipped. Cannot cancel." in captured.out
        assert isinstance(order.get_state(), ShippedState)

    def test_cancelled_state_pay(self, order, capsys):
        """Test payment in cancelled state."""
        order.cancel()  # Move to cancelled state
        order.pay()  # Try to pay
        captured = capsys.readouterr()

        assert "Order TEST-001 is cancelled. Cannot process payment." in captured.out
        assert isinstance(order.get_state(), CancelledState)

    def test_cancelled_state_ship(self, order, capsys):
        """Test shipping in cancelled state."""
        order.cancel()  # Move to cancelled state
        order.ship()  # Try to ship
        captured = capsys.readouterr()

        assert "Order TEST-001 is cancelled. Cannot ship." in captured.out
        assert isinstance(order.get_state(), CancelledState)

    def test_cancelled_state_cancel(self, order, capsys):
        """Test cancellation in cancelled state."""
        order.cancel()  # Move to cancelled state
        order.cancel()  # Try to cancel again
        captured = capsys.readouterr()

        assert "Order TEST-001 is already cancelled." in captured.out
        assert isinstance(order.get_state(), CancelledState)

    def test_order_workflow_success(self, order):
        """Test successful order workflow."""
        # Start pending
        assert order.get_status() == "Pending"

        # Pay
        order.pay()
        assert order.get_status() == "Paid"

        # Ship
        order.ship()
        assert order.get_status() == "Shipped"

    def test_order_workflow_cancel_before_payment(self, order):
        """Test order cancellation before payment."""
        # Start pending
        assert order.get_status() == "Pending"

        # Cancel
        order.cancel()
        assert order.get_status() == "Cancelled"

    def test_order_workflow_cancel_after_payment(self, order):
        """Test order cancellation after payment."""
        # Start pending
        assert order.get_status() == "Pending"

        # Pay
        order.pay()
        assert order.get_status() == "Paid"

        # Cancel
        order.cancel()
        assert order.get_status() == "Cancelled"


class TestIntegrationScenarios:
    """Test integration scenarios with multiple state machines."""

    def test_vending_machine_complete_transaction(self, capsys):
        """Test complete vending machine transaction flow."""
        machine = VendingMachine()

        # Complete successful transaction
        machine.insert_coin()
        machine.select_product("Coke")
        machine.dispense()

        captured = capsys.readouterr()
        assert "Coin inserted" in captured.out
        assert "Product 'Coke' selected" in captured.out
        assert "Product 'Coke' dispensed" in captured.out
        assert machine.inventory["Coke"] == 4
        assert isinstance(machine.get_state(), WaitingState)

    def test_multiple_orders_workflow(self, capsys):
        """Test multiple orders with different workflows."""
        order1 = Order("ORDER-001")
        order2 = Order("ORDER-002")
        order3 = Order("ORDER-003")

        # Order 1: Complete workflow
        order1.pay()
        order1.ship()
        assert order1.get_status() == "Shipped"

        # Order 2: Cancel before payment
        order2.cancel()
        assert order2.get_status() == "Cancelled"

        # Order 3: Cancel after payment
        order3.pay()
        order3.cancel()
        assert order3.get_status() == "Cancelled"

    def test_media_player_complex_workflow(self, capsys):
        """Test complex media player workflow."""
        player = MediaPlayer()

        # Complex workflow
        player.play()
        player.pause()
        player.play()
        player.pause()
        player.stop()

        captured = capsys.readouterr()
        assert "Starting playback" in captured.out
        assert "Pausing playback" in captured.out
        assert "Resuming playback" in captured.out
        assert "Stopping playback" in captured.out
        assert player.get_status() == "Stopped"

    def test_traffic_light_timing_simulation(self):
        """Test traffic light timing simulation."""
        light = TrafficLight()

        # Simulate 24 state changes (8 complete cycles)
        states = []
        for _ in range(24):
            states.append(light.get_color())
            light.change()

        # Should have 8 complete cycles of Red -> Green -> Yellow
        expected_pattern = ["Red", "Green", "Yellow"] * 8
        assert states == expected_pattern


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_vending_machine_empty_inventory(self, capsys):
        """Test vending machine with empty inventory."""
        machine = VendingMachine()
        machine.inventory = {}

        machine.insert_coin()
        machine.select_product("Coke")
        captured = capsys.readouterr()

        assert "Product 'Coke' not available" in captured.out
        assert isinstance(machine.get_state(), WaitingState)

    def test_vending_machine_none_selected_product(self, capsys):
        """Test vending machine with None selected product."""
        machine = VendingMachine()
        machine.insert_coin()
        machine.select_product("Coke")

        # Simulate error condition
        machine.selected_product = None
        machine.dispense()
        captured = capsys.readouterr()

        assert "Error dispensing product" in captured.out
        assert isinstance(machine.get_state(), WaitingState)

    def test_order_invalid_state_transition(self):
        """Test order with invalid state transitions."""
        order = Order("INVALID-001")

        # Try to ship before payment
        order.ship()
        assert order.get_status() == "Pending"

        # Try operations on cancelled order
        order.cancel()
        assert order.get_status() == "Cancelled"

        order.pay()
        assert order.get_status() == "Cancelled"

    def test_state_machine_with_custom_states(self):
        """Test state machine with custom state implementations."""

        class CustomState(State):
            def __init__(self, name):
                self.name = name

            def handle(self, context):
                context.handled_by = self.name

        state1 = CustomState("State1")
        state2 = CustomState("State2")

        context = Context(state1)
        context.request()
        assert context.handled_by == "State1"

        context.set_state(state2)
        context.request()
        assert context.handled_by == "State2"

    def test_empty_order_id(self):
        """Test order with empty ID."""
        order = Order("")
        assert order.id == ""
        assert isinstance(order.get_state(), PendingState)

    def test_special_characters_in_product_name(self, capsys):
        """Test vending machine with special characters in product names."""
        machine = VendingMachine()
        machine.inventory["Coke™"] = 1

        machine.insert_coin()
        machine.select_product("Coke™")
        machine.dispense()

        captured = capsys.readouterr()
        assert "Product 'Coke™' selected" in captured.out
        assert "Product 'Coke™' dispensed" in captured.out


class TestPerformanceAndStress:
    """Test performance and stress scenarios."""

    def test_rapid_state_changes(self):
        """Test rapid state changes."""
        light = TrafficLight()

        # Perform 1000 state changes
        for _ in range(1000):
            light.change()

        # Should end in the expected state (1000 % 3 = 1, so Green)
        assert light.get_color() == "Green"

    def test_large_inventory_vending_machine(self):
        """Test vending machine with large inventory."""
        machine = VendingMachine()

        # Add 1000 different products
        for i in range(1000):
            machine.inventory[f"Product{i}"] = 100

        machine.insert_coin()
        machine.select_product("Product500")
        machine.dispense()

        assert machine.inventory["Product500"] == 99
        assert isinstance(machine.get_state(), WaitingState)

    def test_many_orders_processing(self):
        """Test processing many orders simultaneously."""
        orders = [Order(f"ORDER-{i:04d}") for i in range(100)]

        # Process all orders
        for order in orders:
            order.pay()
            order.ship()

        # All orders should be shipped
        for order in orders:
            assert order.get_status() == "Shipped"

    def test_media_player_extended_session(self):
        """Test media player extended session."""
        player = MediaPlayer()

        # Simulate 1000 random actions
        import random

        actions = [player.play, player.pause, player.stop]

        for _ in range(1000):
            action = random.choice(actions)
            action()

        # Player should be in a valid state
        assert player.get_status() in ["Stopped", "Playing", "Paused"]


class TestDemonstrationFunctions:
    """Test the demonstration functions."""

    def test_demonstrate_vending_machine(self, capsys):
        """Test vending machine demonstration."""
        demonstrate_vending_machine()
        captured = capsys.readouterr()

        assert "=== Vending Machine State Demo ===" in captured.out
        assert "Current inventory:" in captured.out
        assert "Please insert a coin first" in captured.out
        assert "Coin inserted" in captured.out
        assert "dispensed" in captured.out

    def test_demonstrate_traffic_light(self, capsys):
        """Test traffic light demonstration."""
        demonstrate_traffic_light()
        captured = capsys.readouterr()

        assert "=== Traffic Light State Demo ===" in captured.out
        assert "Initial state: Red" in captured.out
        assert "Current state:" in captured.out
        assert "Green" in captured.out
        assert "Yellow" in captured.out

    def test_demonstrate_media_player(self, capsys):
        """Test media player demonstration."""
        demonstrate_media_player()
        captured = capsys.readouterr()

        assert "=== Media Player State Demo ===" in captured.out
        assert "Initial status: Stopped" in captured.out
        assert "Status: Playing" in captured.out
        assert "Status: Paused" in captured.out
        assert "Player is stopped. Cannot pause." in captured.out

    def test_demonstrate_order_processing(self, capsys):
        """Test order processing demonstration."""
        demonstrate_order_processing()
        captured = capsys.readouterr()

        assert "=== Order Processing State Demo ===" in captured.out
        assert "Order ORD-001 status:" in captured.out
        assert "cannot be shipped" in captured.out
        assert "payment received" in captured.out
        assert "shipped" in captured.out
        assert "already shipped" in captured.out


class TestStateMachineConsistency:
    """Test state machine consistency and invariants."""

    def test_vending_machine_state_consistency(self):
        """Test vending machine maintains consistent state."""
        machine = VendingMachine()

        # Test all possible state transitions
        assert isinstance(machine.get_state(), WaitingState)

        machine.insert_coin()
        assert isinstance(machine.get_state(), CoinInsertedState)

        machine.select_product("Coke")
        assert isinstance(machine.get_state(), DispensingState)

        machine.dispense()
        assert isinstance(machine.get_state(), WaitingState)

    def test_order_state_consistency(self):
        """Test order maintains consistent state."""
        order = Order("CONSISTENCY-001")

        # Test valid state transitions
        assert isinstance(order.get_state(), PendingState)

        order.pay()
        assert isinstance(order.get_state(), PaidState)

        order.ship()
        assert isinstance(order.get_state(), ShippedState)

    def test_media_player_state_consistency(self):
        """Test media player maintains consistent state."""
        player = MediaPlayer()

        # Test all valid state transitions
        assert isinstance(player.get_state(), StoppedState)

        player.play()
        assert isinstance(player.get_state(), PlayingState)

        player.pause()
        assert isinstance(player.get_state(), PausedState)

        player.play()
        assert isinstance(player.get_state(), PlayingState)

        player.stop()
        assert isinstance(player.get_state(), StoppedState)

    def test_traffic_light_state_consistency(self):
        """Test traffic light maintains consistent state."""
        light = TrafficLight()

        # Test cyclic state transitions
        assert isinstance(light.get_state(), RedState)

        light.change()
        assert isinstance(light.get_state(), GreenState)

        light.change()
        assert isinstance(light.get_state(), YellowState)

        light.change()
        assert isinstance(light.get_state(), RedState)


if __name__ == "__main__":
    pytest.main([__file__])
