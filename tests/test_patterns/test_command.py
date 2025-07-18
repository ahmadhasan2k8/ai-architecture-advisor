"""Tests for command pattern implementations."""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from src.patterns.command import (
    # Basic Command Pattern
    Command,
    NoCommand,
    
    # Receiver Classes
    Light,
    Fan,
    Stereo,
    
    # Concrete Command Classes
    LightOnCommand,
    LightOffCommand,
    FanSpeedCommand,
    StereoOnWithVolumeCommand,
    StereoOffCommand,
    MacroCommand,
    
    # Invoker Classes
    RemoteControl,
    SimpleRemoteControl,
    
    # Command Queue and History
    CommandQueue,
    CommandHistory,
    CommandHistoryEntry,
    
    # Text Editor Example
    TextEditor,
    InsertTextCommand,
    DeleteTextCommand,
)


class TestBasicCommandPattern:
    """Test the basic Command pattern implementation."""
    
    def test_no_command(self):
        """Test NoCommand implementation."""
        no_command = NoCommand()
        
        # Should not raise any exceptions
        no_command.execute()
        no_command.undo()
        
        # Should be instance of Command
        assert isinstance(no_command, Command)


class TestReceiverClasses:
    """Test receiver classes (Light, Fan, Stereo)."""
    
    def test_light_creation(self):
        """Test creating a light."""
        light = Light("Living Room")
        
        assert light.location == "Living Room"
        assert light.is_on is False
    
    def test_light_turn_on(self, capsys):
        """Test turning light on."""
        light = Light("Kitchen")
        
        light.turn_on()
        
        assert light.is_on is True
        captured = capsys.readouterr()
        assert "Kitchen light is ON" in captured.out
    
    def test_light_turn_off(self, capsys):
        """Test turning light off."""
        light = Light("Bedroom")
        light.turn_on()  # Turn on first
        
        light.turn_off()
        
        assert light.is_on is False
        captured = capsys.readouterr()
        assert "Bedroom light is OFF" in captured.out
    
    def test_light_get_state(self):
        """Test getting light state."""
        light = Light("Office")
        
        assert light.get_state() is False
        
        light.turn_on()
        assert light.get_state() is True
        
        light.turn_off()
        assert light.get_state() is False
    
    def test_fan_creation(self):
        """Test creating a fan."""
        fan = Fan("Ceiling")
        
        assert fan.location == "Ceiling"
        assert fan.speed == 0
    
    def test_fan_set_speed(self, capsys):
        """Test setting fan speed."""
        fan = Fan("Living Room")
        
        fan.set_speed(2)
        assert fan.speed == 2
        captured = capsys.readouterr()
        assert "Living Room fan is on MEDIUM speed" in captured.out
    
    def test_fan_speed_bounds(self):
        """Test fan speed bounds."""
        fan = Fan("Office")
        
        # Test lower bound
        fan.set_speed(-1)
        assert fan.speed == 0
        
        # Test upper bound
        fan.set_speed(5)
        assert fan.speed == 3
    
    def test_fan_speed_methods(self, capsys):
        """Test fan speed convenience methods."""
        fan = Fan("Bedroom")
        
        fan.low_speed()
        assert fan.speed == 1
        
        fan.medium_speed()
        assert fan.speed == 2
        
        fan.high_speed()
        assert fan.speed == 3
        
        fan.off()
        assert fan.speed == 0
        
        captured = capsys.readouterr()
        assert "LOW speed" in captured.out
        assert "MEDIUM speed" in captured.out
        assert "HIGH speed" in captured.out
        assert "OFF" in captured.out
    
    def test_fan_get_speed(self):
        """Test getting fan speed."""
        fan = Fan("Kitchen")
        
        assert fan.get_speed() == 0
        
        fan.set_speed(2)
        assert fan.get_speed() == 2
    
    def test_stereo_creation(self):
        """Test creating a stereo."""
        stereo = Stereo("Living Room")
        
        assert stereo.location == "Living Room"
        assert stereo.is_on is False
        assert stereo.volume == 0
    
    def test_stereo_turn_on_off(self, capsys):
        """Test turning stereo on and off."""
        stereo = Stereo("Den")
        
        stereo.turn_on()
        assert stereo.is_on is True
        
        stereo.turn_off()
        assert stereo.is_on is False
        
        captured = capsys.readouterr()
        assert "Den stereo is ON" in captured.out
        assert "Den stereo is OFF" in captured.out
    
    def test_stereo_volume(self, capsys):
        """Test stereo volume control."""
        stereo = Stereo("Office")
        
        stereo.set_volume(50)
        assert stereo.volume == 50
        
        captured = capsys.readouterr()
        assert "Office stereo volume set to 50" in captured.out
    
    def test_stereo_volume_bounds(self):
        """Test stereo volume bounds."""
        stereo = Stereo("Kitchen")
        
        # Test lower bound
        stereo.set_volume(-10)
        assert stereo.volume == 0
        
        # Test upper bound
        stereo.set_volume(150)
        assert stereo.volume == 100
    
    def test_stereo_get_methods(self):
        """Test stereo getter methods."""
        stereo = Stereo("Garage")
        
        assert stereo.get_volume() == 0
        assert stereo.is_powered_on() is False
        
        stereo.turn_on()
        stereo.set_volume(75)
        
        assert stereo.get_volume() == 75
        assert stereo.is_powered_on() is True


class TestConcreteCommands:
    """Test concrete command implementations."""
    
    def test_light_on_command(self, capsys):
        """Test light on command."""
        light = Light("Test Room")
        command = LightOnCommand(light)
        
        command.execute()
        
        assert light.is_on is True
        captured = capsys.readouterr()
        assert "Test Room light is ON" in captured.out
    
    def test_light_on_command_undo(self, capsys):
        """Test light on command undo."""
        light = Light("Test Room")
        command = LightOnCommand(light)
        
        command.execute()
        command.undo()
        
        assert light.is_on is False
        captured = capsys.readouterr()
        assert "Test Room light is OFF" in captured.out
    
    def test_light_off_command(self, capsys):
        """Test light off command."""
        light = Light("Test Room")
        light.turn_on()  # Start with light on
        command = LightOffCommand(light)
        
        command.execute()
        
        assert light.is_on is False
        captured = capsys.readouterr()
        assert "Test Room light is OFF" in captured.out
    
    def test_light_off_command_undo(self, capsys):
        """Test light off command undo."""
        light = Light("Test Room")
        command = LightOffCommand(light)
        
        command.execute()
        command.undo()
        
        assert light.is_on is True
        captured = capsys.readouterr()
        assert "Test Room light is ON" in captured.out
    
    def test_fan_speed_command(self, capsys):
        """Test fan speed command."""
        fan = Fan("Test Room")
        command = FanSpeedCommand(fan, 2)
        
        command.execute()
        
        assert fan.speed == 2
        captured = capsys.readouterr()
        assert "MEDIUM speed" in captured.out
    
    def test_fan_speed_command_undo(self, capsys):
        """Test fan speed command undo."""
        fan = Fan("Test Room")
        fan.set_speed(1)  # Start at low speed
        command = FanSpeedCommand(fan, 3)
        
        command.execute()
        assert fan.speed == 3
        
        command.undo()
        assert fan.speed == 1  # Should return to previous speed
    
    def test_stereo_on_with_volume_command(self, capsys):
        """Test stereo on with volume command."""
        stereo = Stereo("Test Room")
        command = StereoOnWithVolumeCommand(stereo, 75)
        
        command.execute()
        
        assert stereo.is_on is True
        assert stereo.volume == 75
        captured = capsys.readouterr()
        assert "Test Room stereo is ON" in captured.out
        assert "volume set to 75" in captured.out
    
    def test_stereo_on_with_volume_command_undo(self, capsys):
        """Test stereo on with volume command undo."""
        stereo = Stereo("Test Room")
        stereo.turn_on()
        stereo.set_volume(50)
        command = StereoOnWithVolumeCommand(stereo, 75)
        
        command.execute()
        command.undo()
        
        assert stereo.volume == 50  # Should restore previous volume
        assert stereo.is_on is True  # Should remain on since it was on before
    
    def test_stereo_on_command_undo_when_was_off(self, capsys):
        """Test stereo on command undo when stereo was initially off."""
        stereo = Stereo("Test Room")
        command = StereoOnWithVolumeCommand(stereo, 60)
        
        command.execute()
        command.undo()
        
        assert stereo.is_on is False  # Should turn off since it was off initially
    
    def test_stereo_off_command(self, capsys):
        """Test stereo off command."""
        stereo = Stereo("Test Room")
        stereo.turn_on()
        stereo.set_volume(50)
        command = StereoOffCommand(stereo)
        
        command.execute()
        
        assert stereo.is_on is False
        captured = capsys.readouterr()
        assert "Test Room stereo is OFF" in captured.out
    
    def test_stereo_off_command_undo(self, capsys):
        """Test stereo off command undo."""
        stereo = Stereo("Test Room")
        stereo.turn_on()
        stereo.set_volume(60)
        command = StereoOffCommand(stereo)
        
        command.execute()
        command.undo()
        
        assert stereo.is_on is True
        assert stereo.volume == 60  # Should restore previous volume
    
    def test_macro_command(self, capsys):
        """Test macro command."""
        light = Light("Living Room")
        fan = Fan("Ceiling")
        stereo = Stereo("Living Room")
        
        commands = [
            LightOnCommand(light),
            FanSpeedCommand(fan, 2),
            StereoOnWithVolumeCommand(stereo, 70)
        ]
        
        macro = MacroCommand(commands)
        macro.execute()
        
        assert light.is_on is True
        assert fan.speed == 2
        assert stereo.is_on is True
        assert stereo.volume == 70
    
    def test_macro_command_undo(self, capsys):
        """Test macro command undo."""
        light = Light("Living Room")
        fan = Fan("Ceiling")
        
        commands = [
            LightOnCommand(light),
            FanSpeedCommand(fan, 2)
        ]
        
        macro = MacroCommand(commands)
        macro.execute()
        macro.undo()
        
        assert light.is_on is False
        assert fan.speed == 0
    
    def test_command_interface_compliance(self):
        """Test that all commands implement the Command interface."""
        light = Light("Test")
        fan = Fan("Test")
        stereo = Stereo("Test")
        
        commands = [
            LightOnCommand(light),
            LightOffCommand(light),
            FanSpeedCommand(fan, 1),
            StereoOnWithVolumeCommand(stereo),
            StereoOffCommand(stereo),
            MacroCommand([LightOnCommand(light)]),
            NoCommand()
        ]
        
        for command in commands:
            assert isinstance(command, Command)
            # Should have execute and undo methods
            assert hasattr(command, 'execute')
            assert hasattr(command, 'undo')
            assert callable(command.execute)
            assert callable(command.undo)


class TestRemoteControl:
    """Test remote control implementation."""
    
    def test_remote_control_creation(self):
        """Test creating remote control."""
        remote = RemoteControl()
        
        assert len(remote.on_commands) == 7
        assert len(remote.off_commands) == 7
        assert isinstance(remote.undo_command, NoCommand)
        
        # All slots should be initialized with NoCommand
        for i in range(7):
            assert isinstance(remote.on_commands[i], NoCommand)
            assert isinstance(remote.off_commands[i], NoCommand)
    
    def test_remote_control_custom_slots(self):
        """Test creating remote control with custom number of slots."""
        remote = RemoteControl(5)
        
        assert len(remote.on_commands) == 5
        assert len(remote.off_commands) == 5
    
    def test_set_command(self):
        """Test setting commands on remote control."""
        remote = RemoteControl()
        light = Light("Living Room")
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        
        remote.set_command(0, on_command, off_command)
        
        assert remote.on_commands[0] is on_command
        assert remote.off_commands[0] is off_command
    
    def test_set_command_invalid_slot(self):
        """Test setting command on invalid slot."""
        remote = RemoteControl(3)
        light = Light("Test")
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        
        # Should not raise exception, just ignore
        remote.set_command(5, on_command, off_command)
        
        # Commands should not be set (still NoCommand)
        assert isinstance(remote.on_commands[2], NoCommand)
    
    def test_on_button_pressed(self, capsys):
        """Test pressing on button."""
        remote = RemoteControl()
        light = Light("Living Room")
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        remote.set_command(0, on_command, off_command)
        
        remote.on_button_pressed(0)
        
        assert light.is_on is True
        assert remote.undo_command is on_command
        captured = capsys.readouterr()
        assert "Living Room light is ON" in captured.out
    
    def test_off_button_pressed(self, capsys):
        """Test pressing off button."""
        remote = RemoteControl()
        light = Light("Living Room")
        light.turn_on()  # Start with light on
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        remote.set_command(0, on_command, off_command)
        
        remote.off_button_pressed(0)
        
        assert light.is_on is False
        assert remote.undo_command is off_command
        captured = capsys.readouterr()
        assert "Living Room light is OFF" in captured.out
    
    def test_undo_button_pressed(self, capsys):
        """Test pressing undo button."""
        remote = RemoteControl()
        light = Light("Living Room")
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        remote.set_command(0, on_command, off_command)
        
        # Turn light on
        remote.on_button_pressed(0)
        assert light.is_on is True
        
        # Undo should turn it off
        remote.undo_button_pressed()
        assert light.is_on is False
    
    def test_invalid_slot_button_press(self):
        """Test pressing button for invalid slot."""
        remote = RemoteControl(3)
        
        # Should not raise exception, just do nothing
        remote.on_button_pressed(5)
        remote.off_button_pressed(5)
    
    def test_remote_control_string_representation(self):
        """Test string representation of remote control."""
        remote = RemoteControl(2)
        light = Light("Living Room")
        
        on_command = LightOnCommand(light)
        off_command = LightOffCommand(light)
        remote.set_command(0, on_command, off_command)
        
        string_repr = str(remote)
        
        assert "------ Remote Control ------" in string_repr
        assert "LightOnCommand" in string_repr
        assert "LightOffCommand" in string_repr
        assert "NoCommand" in string_repr
        assert "[undo]" in string_repr


class TestSimpleRemoteControl:
    """Test simple remote control implementation."""
    
    def test_simple_remote_creation(self):
        """Test creating simple remote control."""
        remote = SimpleRemoteControl()
        
        assert remote.command is None
    
    def test_set_command(self):
        """Test setting command on simple remote."""
        remote = SimpleRemoteControl()
        light = Light("Test")
        command = LightOnCommand(light)
        
        remote.set_command(command)
        
        assert remote.command is command
    
    def test_button_pressed(self, capsys):
        """Test pressing button on simple remote."""
        remote = SimpleRemoteControl()
        light = Light("Test")
        command = LightOnCommand(light)
        
        remote.set_command(command)
        remote.button_pressed()
        
        assert light.is_on is True
        captured = capsys.readouterr()
        assert "Test light is ON" in captured.out
    
    def test_button_pressed_no_command(self):
        """Test pressing button when no command is set."""
        remote = SimpleRemoteControl()
        
        # Should not raise exception
        remote.button_pressed()


class TestCommandQueue:
    """Test command queue implementation."""
    
    def test_command_queue_creation(self):
        """Test creating command queue."""
        queue = CommandQueue()
        
        assert len(queue.commands) == 0
        assert queue.size() == 0
    
    def test_add_command(self):
        """Test adding commands to queue."""
        queue = CommandQueue()
        light = Light("Test")
        command = LightOnCommand(light)
        
        queue.add_command(command)
        
        assert queue.size() == 1
        assert queue.commands[0] is command
    
    def test_execute_all(self, capsys):
        """Test executing all commands in queue."""
        queue = CommandQueue()
        light = Light("Test")
        fan = Fan("Test")
        
        queue.add_command(LightOnCommand(light))
        queue.add_command(FanSpeedCommand(fan, 2))
        
        queue.execute_all()
        
        assert light.is_on is True
        assert fan.speed == 2
        assert queue.size() == 0  # Queue should be empty after execution
        
        captured = capsys.readouterr()
        assert "Test light is ON" in captured.out
        assert "MEDIUM speed" in captured.out
    
    def test_clear(self):
        """Test clearing command queue."""
        queue = CommandQueue()
        light = Light("Test")
        
        queue.add_command(LightOnCommand(light))
        queue.add_command(LightOffCommand(light))
        
        assert queue.size() == 2
        
        queue.clear()
        
        assert queue.size() == 0
        assert len(queue.commands) == 0
    
    def test_multiple_execute_all(self, capsys):
        """Test multiple execute_all calls."""
        queue = CommandQueue()
        light = Light("Test")
        
        # First batch
        queue.add_command(LightOnCommand(light))
        queue.execute_all()
        assert light.is_on is True
        assert queue.size() == 0
        
        # Second batch
        queue.add_command(LightOffCommand(light))
        queue.execute_all()
        assert light.is_on is False
        assert queue.size() == 0


class TestCommandHistory:
    """Test command history implementation."""
    
    def test_command_history_creation(self):
        """Test creating command history."""
        history = CommandHistory()
        
        assert len(history.history) == 0
        assert history.current_position == -1
        assert history.max_size == 100
    
    def test_command_history_custom_size(self):
        """Test creating command history with custom size."""
        history = CommandHistory(50)
        
        assert history.max_size == 50
    
    def test_execute_command(self, capsys):
        """Test executing command through history."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        history.execute_command(command, "Turn on test light")
        
        assert light.is_on is True
        assert len(history.history) == 1
        assert history.current_position == 0
        
        entry = history.history[0]
        assert entry.command is command
        assert entry.description == "Turn on test light"
        assert isinstance(entry.executed_at, datetime)
    
    def test_undo(self, capsys):
        """Test undo functionality."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        history.execute_command(command)
        assert light.is_on is True
        
        result = history.undo()
        assert result is True
        assert light.is_on is False
        assert history.current_position == -1
    
    def test_undo_empty_history(self):
        """Test undo with empty history."""
        history = CommandHistory()
        
        result = history.undo()
        assert result is False
    
    def test_undo_at_beginning(self):
        """Test undo when already at beginning."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        history.execute_command(command)
        history.undo()
        
        # Second undo should return False
        result = history.undo()
        assert result is False
    
    def test_redo(self, capsys):
        """Test redo functionality."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        history.execute_command(command)
        history.undo()
        assert light.is_on is False
        
        result = history.redo()
        assert result is True
        assert light.is_on is True
        assert history.current_position == 0
    
    def test_redo_empty_history(self):
        """Test redo with empty history."""
        history = CommandHistory()
        
        result = history.redo()
        assert result is False
    
    def test_redo_at_end(self):
        """Test redo when already at end."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        history.execute_command(command)
        
        # Redo should return False when at end
        result = history.redo()
        assert result is False
    
    def test_can_undo_redo(self):
        """Test can_undo and can_redo methods."""
        history = CommandHistory()
        light = Light("Test")
        command = LightOnCommand(light)
        
        # Initially should not be able to undo or redo
        assert history.can_undo() is False
        assert history.can_redo() is False
        
        history.execute_command(command)
        
        # After execution, can undo but not redo
        assert history.can_undo() is True
        assert history.can_redo() is False
        
        history.undo()
        
        # After undo, can't undo more but can redo
        assert history.can_undo() is False
        assert history.can_redo() is True
        
        history.redo()
        
        # After redo, can undo again but not redo
        assert history.can_undo() is True
        assert history.can_redo() is False
    
    def test_execute_command_clears_redo_history(self):
        """Test that executing a new command clears redo history."""
        history = CommandHistory()
        light = Light("Test")
        
        command1 = LightOnCommand(light)
        command2 = LightOffCommand(light)
        
        history.execute_command(command1)
        history.undo()
        
        # Should be able to redo
        assert history.can_redo() is True
        
        # Execute new command
        history.execute_command(command2)
        
        # Should no longer be able to redo
        assert history.can_redo() is False
        assert len(history.history) == 1  # Only the new command
    
    def test_max_size_limit(self):
        """Test maximum size limit."""
        history = CommandHistory(3)
        light = Light("Test")
        
        # Add more commands than max size
        for i in range(5):
            command = LightOnCommand(light) if i % 2 == 0 else LightOffCommand(light)
            history.execute_command(command, f"Command {i}")
        
        # Should only keep the last 3 commands
        assert len(history.history) == 3
        assert history.current_position == 2
        
        # Should have the last 3 commands
        descriptions = [entry.description for entry in history.history]
        assert descriptions == ["Command 2", "Command 3", "Command 4"]
    
    def test_get_history(self):
        """Test getting history."""
        history = CommandHistory()
        light = Light("Test")
        
        command1 = LightOnCommand(light)
        command2 = LightOffCommand(light)
        
        history.execute_command(command1, "First")
        history.execute_command(command2, "Second")
        
        history_copy = history.get_history()
        
        assert len(history_copy) == 2
        assert history_copy[0].description == "First"
        assert history_copy[1].description == "Second"
        
        # Should be a copy, not the original
        assert history_copy is not history.history
    
    def test_clear_history(self):
        """Test clearing history."""
        history = CommandHistory()
        light = Light("Test")
        
        history.execute_command(LightOnCommand(light))
        history.execute_command(LightOffCommand(light))
        
        assert len(history.history) == 2
        
        history.clear()
        
        assert len(history.history) == 0
        assert history.current_position == -1
        assert history.can_undo() is False
        assert history.can_redo() is False


class TestTextEditor:
    """Test text editor implementation."""
    
    def test_text_editor_creation(self):
        """Test creating text editor."""
        editor = TextEditor()
        
        assert editor.content == ""
        assert isinstance(editor.history, CommandHistory)
    
    def test_insert_text(self):
        """Test inserting text."""
        editor = TextEditor()
        
        editor.insert_text("Hello", 0)
        
        assert editor.get_content() == "Hello"
    
    def test_insert_text_at_position(self):
        """Test inserting text at specific position."""
        editor = TextEditor()
        editor.set_content("Hello World")
        
        editor.insert_text(" Beautiful", 5)
        
        assert editor.get_content() == "Hello Beautiful World"
    
    def test_delete_text(self):
        """Test deleting text."""
        editor = TextEditor()
        editor.set_content("Hello World")
        
        editor.delete_text(6, 5)  # Delete "World"
        
        assert editor.get_content() == "Hello "
    
    def test_delete_text_at_beginning(self):
        """Test deleting text at beginning."""
        editor = TextEditor()
        editor.set_content("Hello World")
        
        editor.delete_text(0, 6)  # Delete "Hello "
        
        assert editor.get_content() == "World"
    
    def test_text_editor_undo(self):
        """Test text editor undo."""
        editor = TextEditor()
        
        editor.insert_text("Hello", 0)
        editor.insert_text(" World", 5)
        
        assert editor.get_content() == "Hello World"
        
        # Undo last insertion
        result = editor.undo()
        assert result is True
        assert editor.get_content() == "Hello"
        
        # Undo first insertion
        result = editor.undo()
        assert result is True
        assert editor.get_content() == ""
    
    def test_text_editor_redo(self):
        """Test text editor redo."""
        editor = TextEditor()
        
        editor.insert_text("Hello", 0)
        editor.undo()
        
        assert editor.get_content() == ""
        
        result = editor.redo()
        assert result is True
        assert editor.get_content() == "Hello"
    
    def test_text_editor_complex_operations(self):
        """Test complex text editor operations."""
        editor = TextEditor()
        
        # Build up some text
        editor.insert_text("Hello", 0)
        editor.insert_text(" World", 5)
        editor.insert_text("!", 11)
        
        assert editor.get_content() == "Hello World!"
        
        # Delete some text
        editor.delete_text(5, 6)  # Delete " World"
        
        assert editor.get_content() == "Hello!"
        
        # Undo delete
        editor.undo()
        assert editor.get_content() == "Hello World!"
        
        # Undo insert
        editor.undo()
        assert editor.get_content() == "Hello World"
    
    def test_insert_text_command_directly(self):
        """Test InsertTextCommand directly."""
        editor = TextEditor()
        editor.set_content("Hello World")
        
        command = InsertTextCommand(editor, " Beautiful", 5)
        command.execute()
        
        assert editor.get_content() == "Hello Beautiful World"
        
        command.undo()
        assert editor.get_content() == "Hello World"
    
    def test_delete_text_command_directly(self):
        """Test DeleteTextCommand directly."""
        editor = TextEditor()
        editor.set_content("Hello Beautiful World")
        
        command = DeleteTextCommand(editor, 5, 10)  # Delete " Beautiful"
        command.execute()
        
        assert editor.get_content() == "Hello World"
        
        command.undo()
        assert editor.get_content() == "Hello Beautiful World"
    
    def test_delete_text_command_remembers_deleted_text(self):
        """Test that DeleteTextCommand remembers deleted text."""
        editor = TextEditor()
        editor.set_content("Hello World")
        
        command = DeleteTextCommand(editor, 0, 5)  # Delete "Hello"
        
        # Before execution, deleted_text should be empty
        assert command.deleted_text == ""
        
        command.execute()
        
        # After execution, deleted_text should contain the deleted text
        assert command.deleted_text == "Hello"
        assert editor.get_content() == " World"
        
        command.undo()
        assert editor.get_content() == "Hello World"


class TestCommandPatternIntegration:
    """Test integration scenarios with command pattern."""
    
    def test_complete_home_automation_system(self, capsys):
        """Test complete home automation system."""
        # Create devices
        living_room_light = Light("Living Room")
        kitchen_light = Light("Kitchen")
        ceiling_fan = Fan("Ceiling")
        stereo = Stereo("Living Room")
        
        # Create commands
        living_room_on = LightOnCommand(living_room_light)
        living_room_off = LightOffCommand(living_room_light)
        kitchen_on = LightOnCommand(kitchen_light)
        kitchen_off = LightOffCommand(kitchen_light)
        fan_high = FanSpeedCommand(ceiling_fan, 3)
        fan_off = FanSpeedCommand(ceiling_fan, 0)
        stereo_on = StereoOnWithVolumeCommand(stereo, 80)
        stereo_off = StereoOffCommand(stereo)
        
        # Create macro commands
        party_mode = MacroCommand([living_room_on, kitchen_on, fan_high, stereo_on])
        sleep_mode = MacroCommand([living_room_off, kitchen_off, fan_off, stereo_off])
        
        # Set up remote
        remote = RemoteControl()
        remote.set_command(0, living_room_on, living_room_off)
        remote.set_command(1, kitchen_on, kitchen_off)
        remote.set_command(2, fan_high, fan_off)
        remote.set_command(3, stereo_on, stereo_off)
        remote.set_command(4, party_mode, sleep_mode)
        
        # Test party mode
        remote.on_button_pressed(4)
        
        assert living_room_light.is_on is True
        assert kitchen_light.is_on is True
        assert ceiling_fan.speed == 3
        assert stereo.is_on is True
        assert stereo.volume == 80
        
        # Test undo (should activate sleep mode)
        remote.undo_button_pressed()
        
        assert living_room_light.is_on is False
        assert kitchen_light.is_on is False
        assert ceiling_fan.speed == 0
        assert stereo.is_on is False
    
    def test_command_queue_batch_processing(self, capsys):
        """Test batch processing with command queue."""
        # Create devices
        lights = [Light(f"Room {i}") for i in range(1, 4)]
        fans = [Fan(f"Fan {i}") for i in range(1, 3)]
        
        # Create command queue
        queue = CommandQueue()
        
        # Add commands to queue
        for light in lights:
            queue.add_command(LightOnCommand(light))
        
        for fan in fans:
            queue.add_command(FanSpeedCommand(fan, 2))
        
        # Execute all at once
        queue.execute_all()
        
        # Verify all devices are in correct state
        for light in lights:
            assert light.is_on is True
        
        for fan in fans:
            assert fan.speed == 2
    
    def test_complex_text_editor_workflow(self):
        """Test complex text editor workflow."""
        editor = TextEditor()
        
        # Create a document
        editor.insert_text("Chapter 1: Introduction", 0)
        editor.insert_text("\n\nThis is the introduction.", 24)
        editor.insert_text("\n\nChapter 2: Main Content", 49)
        
        content = editor.get_content()
        assert "Chapter 1: Introduction" in content
        assert "This is the introduction." in content
        assert "Chapter 2: Main Content" in content
        
        # Make some edits
        editor.delete_text(0, 9)  # Delete "Chapter 1"
        editor.insert_text("Section 1", 0)
        
        # Undo some changes
        editor.undo()  # Undo insert
        editor.undo()  # Undo delete
        
        # Should be back to original
        assert "Chapter 1: Introduction" in editor.get_content()
        
        # Redo the changes
        editor.redo()  # Redo delete
        editor.redo()  # Redo insert
        
        content = editor.get_content()
        assert "Section 1: Introduction" in content
        assert "Chapter 1" not in content
    
    def test_command_history_with_branching(self):
        """Test command history with branching operations."""
        history = CommandHistory()
        light = Light("Test")
        
        # Create a sequence of commands
        command1 = LightOnCommand(light)
        command2 = LightOffCommand(light)
        command3 = LightOnCommand(light)
        
        history.execute_command(command1, "Turn on")
        history.execute_command(command2, "Turn off")
        history.execute_command(command3, "Turn on again")
        
        # Undo back to beginning
        history.undo()  # Undo command3
        history.undo()  # Undo command2
        
        # Create a new branch
        new_command = LightOnCommand(light)
        history.execute_command(new_command, "New branch")
        
        # Should not be able to redo old commands
        assert history.can_redo() is False
        assert len(history.history) == 2  # command1 and new_command
        
        # But can undo the new command
        assert history.can_undo() is True
        history.undo()
        assert light.is_on is False


class TestCommandPatternEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_command_with_null_receiver(self):
        """Test command with null receiver."""
        # This should not happen in practice, but test defensive programming
        try:
            command = LightOnCommand(None)
            command.execute()
            assert False, "Should have raised an exception"
        except AttributeError:
            pass  # Expected
    
    def test_empty_macro_command(self):
        """Test macro command with empty command list."""
        macro = MacroCommand([])
        
        # Should not raise exception
        macro.execute()
        macro.undo()
    
    def test_macro_command_with_failing_command(self):
        """Test macro command with a failing command."""
        light = Light("Test")
        
        # Create a command that will fail
        class FailingCommand(Command):
            def execute(self):
                raise ValueError("Command failed")
            
            def undo(self):
                pass
        
        commands = [
            LightOnCommand(light),
            FailingCommand(),
            LightOffCommand(light)
        ]
        
        macro = MacroCommand(commands)
        
        # Should raise exception and not execute remaining commands
        with pytest.raises(ValueError):
            macro.execute()
        
        # Light should still be on (first command executed)
        assert light.is_on is True
    
    def test_command_queue_with_failing_command(self):
        """Test command queue with a failing command."""
        queue = CommandQueue()
        light = Light("Test")
        
        class FailingCommand(Command):
            def execute(self):
                raise ValueError("Command failed")
            
            def undo(self):
                pass
        
        queue.add_command(LightOnCommand(light))
        queue.add_command(FailingCommand())
        queue.add_command(LightOffCommand(light))
        
        # Should raise exception and not execute remaining commands
        with pytest.raises(ValueError):
            queue.execute_all()
        
        # Light should still be on (first command executed)
        assert light.is_on is True
    
    def test_text_editor_out_of_bounds_operations(self):
        """Test text editor with out of bounds operations."""
        editor = TextEditor()
        editor.set_content("Hello")
        
        # Insert beyond end of string
        editor.insert_text(" World", 10)
        # Should handle gracefully (behavior depends on implementation)
        content = editor.get_content()
        assert "Hello" in content
        
        # Delete beyond end of string
        editor.delete_text(0, 100)
        # Should handle gracefully
        content = editor.get_content()
        assert isinstance(content, str)
    
    def test_command_history_size_edge_cases(self):
        """Test command history with edge case sizes."""
        # Size 0 should work
        history = CommandHistory(0)
        light = Light("Test")
        
        history.execute_command(LightOnCommand(light))
        assert len(history.history) == 0  # Should not store any commands
        
        # Size 1 should work
        history = CommandHistory(1)
        history.execute_command(LightOnCommand(light))
        history.execute_command(LightOffCommand(light))
        
        assert len(history.history) == 1  # Should only store the last command
    
    def test_stereo_command_with_extreme_volume(self):
        """Test stereo command with extreme volume values."""
        stereo = Stereo("Test")
        
        # Test with very high volume
        command = StereoOnWithVolumeCommand(stereo, 1000)
        command.execute()
        
        # Should be clamped to maximum
        assert stereo.volume == 100
        
        # Test with negative volume
        command = StereoOnWithVolumeCommand(stereo, -50)
        command.execute()
        
        # Should be clamped to minimum
        assert stereo.volume == 0


class TestCommandPatternPerformance:
    """Test performance characteristics of command pattern."""
    
    def test_large_command_queue_performance(self):
        """Test performance with large command queue."""
        import time
        
        queue = CommandQueue()
        lights = [Light(f"Light {i}") for i in range(100)]
        
        # Add many commands
        for light in lights:
            queue.add_command(LightOnCommand(light))
        
        # Measure execution time
        start = time.time()
        queue.execute_all()
        end = time.time()
        
        # Should complete quickly
        assert (end - start) < 0.1
        
        # All lights should be on
        assert all(light.is_on for light in lights)
    
    def test_command_history_performance(self):
        """Test performance of command history."""
        import time
        
        history = CommandHistory(1000)
        light = Light("Test")
        
        # Execute many commands
        start = time.time()
        for i in range(500):
            command = LightOnCommand(light) if i % 2 == 0 else LightOffCommand(light)
            history.execute_command(command, f"Command {i}")
        end = time.time()
        
        # Should complete in reasonable time
        assert (end - start) < 1.0
        
        # Test undo performance
        start = time.time()
        while history.can_undo():
            history.undo()
        end = time.time()
        
        # Should complete quickly
        assert (end - start) < 0.1
    
    def test_macro_command_performance(self):
        """Test performance of macro command with many sub-commands."""
        import time
        
        # Create many devices
        lights = [Light(f"Light {i}") for i in range(50)]
        fans = [Fan(f"Fan {i}") for i in range(50)]
        
        # Create macro command with many sub-commands
        commands = []
        for light in lights:
            commands.append(LightOnCommand(light))
        for fan in fans:
            commands.append(FanSpeedCommand(fan, 2))
        
        macro = MacroCommand(commands)
        
        # Measure execution time
        start = time.time()
        macro.execute()
        end = time.time()
        
        # Should complete quickly
        assert (end - start) < 0.1
        
        # Test undo performance
        start = time.time()
        macro.undo()
        end = time.time()
        
        # Should complete quickly
        assert (end - start) < 0.1