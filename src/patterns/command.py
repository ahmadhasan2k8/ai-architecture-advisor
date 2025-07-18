"""Command pattern implementations.

This module provides implementations of the Command pattern, demonstrating
how to encapsulate requests as objects to support undo operations, queuing,
and logging.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


class Command(ABC):
    """Abstract base class for commands.

    Commands encapsulate all information needed to perform an action or
    trigger an event at a later time.
    """

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Undo the command."""
        pass


class NoCommand(Command):
    """Null object implementation of Command.

    Used as a placeholder when no command is assigned to avoid null checks.
    """

    def execute(self) -> None:
        """Do nothing."""
        pass

    def undo(self) -> None:
        """Do nothing."""
        pass


# Receiver Classes


class Light:
    """Light device that can be turned on/off."""

    def __init__(self, location: str):
        """Initialize the light.

        Args:
            location: Location of the light (e.g., "Living Room")
        """
        self.location = location
        self.is_on = False

    def turn_on(self) -> None:
        """Turn the light on."""
        self.is_on = True
        print(f"{self.location} light is ON")

    def turn_off(self) -> None:
        """Turn the light off."""
        self.is_on = False
        print(f"{self.location} light is OFF")

    def get_state(self) -> bool:
        """Get the current state of the light.

        Returns:
            True if light is on, False otherwise
        """
        return self.is_on


class Fan:
    """Fan device with variable speed control."""

    def __init__(self, location: str):
        """Initialize the fan.

        Args:
            location: Location of the fan (e.g., "Ceiling")
        """
        self.location = location
        self.speed = 0  # 0 = off, 1 = low, 2 = medium, 3 = high

    def set_speed(self, speed: int) -> None:
        """Set the fan speed.

        Args:
            speed: Fan speed (0-3)
        """
        self.speed = max(0, min(3, speed))
        if self.speed == 0:
            print(f"{self.location} fan is OFF")
        elif self.speed == 1:
            print(f"{self.location} fan is on LOW speed")
        elif self.speed == 2:
            print(f"{self.location} fan is on MEDIUM speed")
        else:
            print(f"{self.location} fan is on HIGH speed")

    def off(self) -> None:
        """Turn the fan off."""
        self.set_speed(0)

    def low_speed(self) -> None:
        """Set fan to low speed."""
        self.set_speed(1)

    def medium_speed(self) -> None:
        """Set fan to medium speed."""
        self.set_speed(2)

    def high_speed(self) -> None:
        """Set fan to high speed."""
        self.set_speed(3)

    def get_speed(self) -> int:
        """Get the current fan speed.

        Returns:
            Current speed (0-3)
        """
        return self.speed


class Stereo:
    """Stereo device with volume control."""

    def __init__(self, location: str):
        """Initialize the stereo.

        Args:
            location: Location of the stereo (e.g., "Living Room")
        """
        self.location = location
        self.is_on = False
        self.volume = 0

    def turn_on(self) -> None:
        """Turn the stereo on."""
        self.is_on = True
        print(f"{self.location} stereo is ON")

    def turn_off(self) -> None:
        """Turn the stereo off."""
        self.is_on = False
        print(f"{self.location} stereo is OFF")

    def set_volume(self, volume: int) -> None:
        """Set the stereo volume.

        Args:
            volume: Volume level (0-100)
        """
        self.volume = max(0, min(100, volume))
        print(f"{self.location} stereo volume set to {self.volume}")

    def get_volume(self) -> int:
        """Get the current volume.

        Returns:
            Current volume level
        """
        return self.volume

    def is_powered_on(self) -> bool:
        """Check if stereo is on.

        Returns:
            True if stereo is on, False otherwise
        """
        return self.is_on


# Concrete Command Classes


class LightOnCommand(Command):
    """Command to turn a light on."""

    def __init__(self, light: Light):
        """Initialize the command.

        Args:
            light: Light to control
        """
        self.light = light

    def execute(self) -> None:
        """Turn the light on."""
        self.light.turn_on()

    def undo(self) -> None:
        """Turn the light off."""
        self.light.turn_off()


class LightOffCommand(Command):
    """Command to turn a light off."""

    def __init__(self, light: Light):
        """Initialize the command.

        Args:
            light: Light to control
        """
        self.light = light

    def execute(self) -> None:
        """Turn the light off."""
        self.light.turn_off()

    def undo(self) -> None:
        """Turn the light on."""
        self.light.turn_on()


class FanSpeedCommand(Command):
    """Command to set fan speed."""

    def __init__(self, fan: Fan, speed: int):
        """Initialize the command.

        Args:
            fan: Fan to control
            speed: Speed to set (0-3)
        """
        self.fan = fan
        self.speed = speed
        self.previous_speed = 0

    def execute(self) -> None:
        """Set the fan speed."""
        self.previous_speed = self.fan.get_speed()
        self.fan.set_speed(self.speed)

    def undo(self) -> None:
        """Restore the previous fan speed."""
        self.fan.set_speed(self.previous_speed)


class StereoOnWithVolumeCommand(Command):
    """Command to turn stereo on with specific volume."""

    def __init__(self, stereo: Stereo, volume: int = 50):
        """Initialize the command.

        Args:
            stereo: Stereo to control
            volume: Volume to set (0-100)
        """
        self.stereo = stereo
        self.volume = volume
        self.previous_volume = 0
        self.was_on = False

    def execute(self) -> None:
        """Turn stereo on and set volume."""
        self.was_on = self.stereo.is_powered_on()
        self.previous_volume = self.stereo.get_volume()
        self.stereo.turn_on()
        self.stereo.set_volume(self.volume)

    def undo(self) -> None:
        """Restore previous stereo state."""
        self.stereo.set_volume(self.previous_volume)
        if not self.was_on:
            self.stereo.turn_off()


class StereoOffCommand(Command):
    """Command to turn stereo off."""

    def __init__(self, stereo: Stereo):
        """Initialize the command.

        Args:
            stereo: Stereo to control
        """
        self.stereo = stereo
        self.previous_volume = 0
        self.was_on = False

    def execute(self) -> None:
        """Turn the stereo off."""
        self.was_on = self.stereo.is_powered_on()
        self.previous_volume = self.stereo.get_volume()
        self.stereo.turn_off()

    def undo(self) -> None:
        """Restore previous stereo state."""
        if self.was_on:
            self.stereo.turn_on()
            self.stereo.set_volume(self.previous_volume)


class MacroCommand(Command):
    """Command that executes multiple commands."""

    def __init__(self, commands: List[Command]):
        """Initialize the macro command.

        Args:
            commands: List of commands to execute
        """
        self.commands = commands

    def execute(self) -> None:
        """Execute all commands in order."""
        for command in self.commands:
            command.execute()

    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self.commands):
            command.undo()


# Invoker Classes


class RemoteControl:
    """Remote control that can execute commands."""

    def __init__(self, slots: int = 7):
        """Initialize the remote control.

        Args:
            slots: Number of command slots
        """
        no_command = NoCommand()
        self.on_commands = [no_command] * slots
        self.off_commands = [no_command] * slots
        self.undo_command = no_command

    def set_command(self, slot: int, on_command: Command, off_command: Command) -> None:
        """Set commands for a specific slot.

        Args:
            slot: Slot number
            on_command: Command to execute when "on" button is pressed
            off_command: Command to execute when "off" button is pressed
        """
        if 0 <= slot < len(self.on_commands):
            self.on_commands[slot] = on_command
            self.off_commands[slot] = off_command

    def on_button_pressed(self, slot: int) -> None:
        """Press the "on" button for a specific slot.

        Args:
            slot: Slot number
        """
        if 0 <= slot < len(self.on_commands):
            self.on_commands[slot].execute()
            self.undo_command = self.on_commands[slot]

    def off_button_pressed(self, slot: int) -> None:
        """Press the "off" button for a specific slot.

        Args:
            slot: Slot number
        """
        if 0 <= slot < len(self.off_commands):
            self.off_commands[slot].execute()
            self.undo_command = self.off_commands[slot]

    def undo_button_pressed(self) -> None:
        """Press the undo button."""
        self.undo_command.undo()

    def __str__(self) -> str:
        """String representation of the remote control.

        Returns:
            String showing all configured commands
        """
        result = "\n------ Remote Control ------\n"
        for i in range(len(self.on_commands)):
            result += f"[slot {i}] {self.on_commands[i].__class__.__name__}    "
            result += f"{self.off_commands[i].__class__.__name__}\n"
        result += f"[undo] {self.undo_command.__class__.__name__}\n"
        return result


class SimpleRemoteControl:
    """Simple remote control with one command slot."""

    def __init__(self):
        """Initialize the simple remote control."""
        self.command: Optional[Command] = None

    def set_command(self, command: Command) -> None:
        """Set the command to execute.

        Args:
            command: Command to set
        """
        self.command = command

    def button_pressed(self) -> None:
        """Press the button to execute the command."""
        if self.command:
            self.command.execute()


# Command Queue and History


class CommandQueue:
    """Queue for storing and executing commands."""

    def __init__(self):
        """Initialize the command queue."""
        self.commands: List[Command] = []

    def add_command(self, command: Command) -> None:
        """Add a command to the queue.

        Args:
            command: Command to add
        """
        self.commands.append(command)

    def execute_all(self) -> None:
        """Execute all commands in the queue."""
        for command in self.commands:
            command.execute()
        self.commands.clear()

    def clear(self) -> None:
        """Clear all commands from the queue."""
        self.commands.clear()

    def size(self) -> int:
        """Get the number of commands in the queue.

        Returns:
            Number of commands
        """
        return len(self.commands)


@dataclass
class CommandHistoryEntry:
    """Entry in command history."""

    command: Command
    executed_at: datetime
    description: str = ""


class CommandHistory:
    """History of executed commands with undo/redo support."""

    def __init__(self, max_size: int = 100):
        """Initialize the command history.

        Args:
            max_size: Maximum number of commands to keep in history
        """
        self.history: List[CommandHistoryEntry] = []
        self.current_position = -1
        self.max_size = max_size

    def execute_command(self, command: Command, description: str = "") -> None:
        """Execute a command and add it to history.

        Args:
            command: Command to execute
            description: Optional description of the command
        """
        # Remove any commands after current position (for redo functionality)
        self.history = self.history[: self.current_position + 1]

        # Execute the command
        command.execute()

        # Add to history
        entry = CommandHistoryEntry(
            command=command, executed_at=datetime.now(), description=description
        )
        self.history.append(entry)
        self.current_position += 1

        # Limit history size
        if len(self.history) > self.max_size:
            self.history.pop(0)
            self.current_position -= 1

    def undo(self) -> bool:
        """Undo the last command.

        Returns:
            True if undo was successful, False otherwise
        """
        if self.current_position >= 0:
            entry = self.history[self.current_position]
            entry.command.undo()
            self.current_position -= 1
            return True
        return False

    def redo(self) -> bool:
        """Redo the next command.

        Returns:
            True if redo was successful, False otherwise
        """
        if self.current_position < len(self.history) - 1:
            self.current_position += 1
            entry = self.history[self.current_position]
            entry.command.execute()
            return True
        return False

    def can_undo(self) -> bool:
        """Check if undo is possible.

        Returns:
            True if undo is possible, False otherwise
        """
        return self.current_position >= 0

    def can_redo(self) -> bool:
        """Check if redo is possible.

        Returns:
            True if redo is possible, False otherwise
        """
        return self.current_position < len(self.history) - 1

    def get_history(self) -> List[CommandHistoryEntry]:
        """Get the command history.

        Returns:
            List of command history entries
        """
        return self.history.copy()

    def clear(self) -> None:
        """Clear the command history."""
        self.history.clear()
        self.current_position = -1


# Text Editor Example


class TextEditor:
    """Simple text editor with undo/redo support."""

    def __init__(self):
        """Initialize the text editor."""
        self.content = ""
        self.history = CommandHistory()

    def insert_text(self, text: str, position: int) -> None:
        """Insert text at a specific position.

        Args:
            text: Text to insert
            position: Position to insert at
        """
        command = InsertTextCommand(self, text, position)
        self.history.execute_command(command, f"Insert '{text}' at position {position}")

    def delete_text(self, start: int, length: int) -> None:
        """Delete text from a specific position.

        Args:
            start: Start position
            length: Number of characters to delete
        """
        command = DeleteTextCommand(self, start, length)
        self.history.execute_command(
            command, f"Delete {length} characters from position {start}"
        )

    def undo(self) -> bool:
        """Undo the last operation.

        Returns:
            True if undo was successful, False otherwise
        """
        return self.history.undo()

    def redo(self) -> bool:
        """Redo the next operation.

        Returns:
            True if redo was successful, False otherwise
        """
        return self.history.redo()

    def get_content(self) -> str:
        """Get the current content.

        Returns:
            Current text content
        """
        return self.content

    def set_content(self, content: str) -> None:
        """Set the content.

        Args:
            content: New content
        """
        self.content = content


class InsertTextCommand(Command):
    """Command to insert text into a text editor."""

    def __init__(self, editor: TextEditor, text: str, position: int):
        """Initialize the command.

        Args:
            editor: Text editor to modify
            text: Text to insert
            position: Position to insert at
        """
        self.editor = editor
        self.text = text
        self.position = position

    def execute(self) -> None:
        """Insert the text."""
        content = self.editor.get_content()
        new_content = content[: self.position] + self.text + content[self.position :]
        self.editor.set_content(new_content)

    def undo(self) -> None:
        """Remove the inserted text."""
        content = self.editor.get_content()
        new_content = (
            content[: self.position] + content[self.position + len(self.text) :]
        )
        self.editor.set_content(new_content)


class DeleteTextCommand(Command):
    """Command to delete text from a text editor."""

    def __init__(self, editor: TextEditor, start: int, length: int):
        """Initialize the command.

        Args:
            editor: Text editor to modify
            start: Start position
            length: Number of characters to delete
        """
        self.editor = editor
        self.start = start
        self.length = length
        self.deleted_text = ""

    def execute(self) -> None:
        """Delete the text."""
        content = self.editor.get_content()
        self.deleted_text = content[self.start : self.start + self.length]
        new_content = content[: self.start] + content[self.start + self.length :]
        self.editor.set_content(new_content)

    def undo(self) -> None:
        """Restore the deleted text."""
        content = self.editor.get_content()
        new_content = content[: self.start] + self.deleted_text + content[self.start :]
        self.editor.set_content(new_content)


# Example usage functions


def demonstrate_remote_control():
    """Demonstrate the remote control example."""
    print("=== Remote Control Demo ===")

    # Create devices
    living_room_light = Light("Living Room")
    kitchen_light = Light("Kitchen")
    ceiling_fan = Fan("Ceiling")
    stereo = Stereo("Living Room")

    # Create commands
    living_room_light_on = LightOnCommand(living_room_light)
    living_room_light_off = LightOffCommand(living_room_light)
    kitchen_light_on = LightOnCommand(kitchen_light)
    kitchen_light_off = LightOffCommand(kitchen_light)
    ceiling_fan_high = FanSpeedCommand(ceiling_fan, 3)
    ceiling_fan_off = FanSpeedCommand(ceiling_fan, 0)
    stereo_on = StereoOnWithVolumeCommand(stereo, 75)
    stereo_off = StereoOffCommand(stereo)

    # Create remote control
    remote = RemoteControl()

    # Set commands
    remote.set_command(0, living_room_light_on, living_room_light_off)
    remote.set_command(1, kitchen_light_on, kitchen_light_off)
    remote.set_command(2, ceiling_fan_high, ceiling_fan_off)
    remote.set_command(3, stereo_on, stereo_off)

    # Test remote control
    print("Testing remote control:")
    remote.on_button_pressed(0)  # Turn on living room light
    remote.on_button_pressed(1)  # Turn on kitchen light
    remote.on_button_pressed(2)  # Turn on ceiling fan
    remote.on_button_pressed(3)  # Turn on stereo

    print("\nTesting undo:")
    remote.undo_button_pressed()  # Undo stereo
    remote.undo_button_pressed()  # Undo fan

    print("\nTesting off commands:")
    remote.off_button_pressed(0)  # Turn off living room light
    remote.off_button_pressed(1)  # Turn off kitchen light


def demonstrate_macro_command():
    """Demonstrate macro commands."""
    print("\n=== Macro Command Demo ===")

    # Create devices
    living_room_light = Light("Living Room")
    stereo = Stereo("Living Room")
    ceiling_fan = Fan("Ceiling")

    # Create commands for party mode
    light_on = LightOnCommand(living_room_light)
    stereo_on = StereoOnWithVolumeCommand(stereo, 80)
    fan_on = FanSpeedCommand(ceiling_fan, 2)

    # Create macro command
    party_mode = MacroCommand([light_on, stereo_on, fan_on])

    print("Activating party mode:")
    party_mode.execute()

    print("\nDeactivating party mode:")
    party_mode.undo()


def demonstrate_command_queue():
    """Demonstrate command queuing."""
    print("\n=== Command Queue Demo ===")

    # Create devices
    light = Light("Bedroom")
    fan = Fan("Bedroom")

    # Create command queue
    queue = CommandQueue()

    # Add commands to queue
    queue.add_command(LightOnCommand(light))
    queue.add_command(FanSpeedCommand(fan, 2))
    queue.add_command(LightOffCommand(light))

    print(f"Commands in queue: {queue.size()}")

    print("Executing all commands:")
    queue.execute_all()

    print(f"Commands in queue after execution: {queue.size()}")


def demonstrate_text_editor():
    """Demonstrate text editor with undo/redo."""
    print("\n=== Text Editor Demo ===")

    editor = TextEditor()

    print(f"Initial content: '{editor.get_content()}'")

    editor.insert_text("Hello", 0)
    print(f"After insert: '{editor.get_content()}'")

    editor.insert_text(" World", 5)
    print(f"After insert: '{editor.get_content()}'")

    editor.insert_text("!", 11)
    print(f"After insert: '{editor.get_content()}'")

    print("\nTesting undo:")
    editor.undo()
    print(f"After undo: '{editor.get_content()}'")

    editor.undo()
    print(f"After undo: '{editor.get_content()}'")

    print("\nTesting redo:")
    editor.redo()
    print(f"After redo: '{editor.get_content()}'")

    print("\nTesting delete:")
    editor.delete_text(0, 5)  # Delete "Hello"
    print(f"After delete: '{editor.get_content()}'")

    editor.undo()
    print(f"After undo delete: '{editor.get_content()}'")


if __name__ == "__main__":
    demonstrate_remote_control()
    demonstrate_macro_command()
    demonstrate_command_queue()
    demonstrate_text_editor()
