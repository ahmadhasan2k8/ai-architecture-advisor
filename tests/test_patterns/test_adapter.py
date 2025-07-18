"""Tests for adapter pattern implementations."""

from typing import Any, Dict, List
from unittest.mock import Mock, call, patch

import pytest

from src.patterns.adapter import (  # Target Interface; Adaptee Classes; Adapter Classes; Database Adapter Example; Payment Gateway Adapter Example; Object Adapter vs Class Adapter; Service Layer
    AudioPlayer,
    DatabaseConnection,
    LegacyRectangle,
    LegacyRectangleAdapter,
    MediaAdapter,
    MediaPlayer,
    Mp3Player,
    Mp4Player,
    MySQLAdapter,
    MySQLConnection,
    PaymentProcessor,
    PaymentService,
    PayPalAdapter,
    PayPalGateway,
    PostgreSQLAdapter,
    PostgreSQLConnection,
    Rectangle,
    StripeAdapter,
    StripeGateway,
    VlcPlayer,
)


class TestAdapteeClasses:
    """Test adaptee classes (Mp3Player, Mp4Player, VlcPlayer)."""

    def test_mp3_player(self, capsys):
        """Test Mp3Player functionality."""
        player = Mp3Player()

        player.play_mp3("song.mp3")

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out

    def test_mp4_player(self, capsys):
        """Test Mp4Player functionality."""
        player = Mp4Player()

        player.play_mp4("video.mp4")

        captured = capsys.readouterr()
        assert "Playing MP4 file: video.mp4" in captured.out

    def test_vlc_player(self, capsys):
        """Test VlcPlayer functionality."""
        player = VlcPlayer()

        player.play_vlc("movie.vlc")

        captured = capsys.readouterr()
        assert "Playing VLC file: movie.vlc" in captured.out

    def test_players_are_independent(self):
        """Test that players are independent classes."""
        mp3_player = Mp3Player()
        mp4_player = Mp4Player()
        vlc_player = VlcPlayer()

        # Each should have its own specific method
        assert hasattr(mp3_player, "play_mp3")
        assert not hasattr(mp3_player, "play_mp4")
        assert not hasattr(mp3_player, "play_vlc")

        assert hasattr(mp4_player, "play_mp4")
        assert not hasattr(mp4_player, "play_mp3")
        assert not hasattr(mp4_player, "play_vlc")

        assert hasattr(vlc_player, "play_vlc")
        assert not hasattr(vlc_player, "play_mp3")
        assert not hasattr(vlc_player, "play_mp4")


class TestMediaAdapter:
    """Test MediaAdapter implementation."""

    def test_adapter_creation_mp3(self):
        """Test creating adapter for MP3."""
        adapter = MediaAdapter("mp3")

        assert adapter.audio_type == "mp3"
        assert isinstance(adapter.player, Mp3Player)

    def test_adapter_creation_mp4(self):
        """Test creating adapter for MP4."""
        adapter = MediaAdapter("mp4")

        assert adapter.audio_type == "mp4"
        assert isinstance(adapter.player, Mp4Player)

    def test_adapter_creation_vlc(self):
        """Test creating adapter for VLC."""
        adapter = MediaAdapter("vlc")

        assert adapter.audio_type == "vlc"
        assert isinstance(adapter.player, VlcPlayer)

    def test_adapter_creation_unsupported(self):
        """Test creating adapter for unsupported format."""
        adapter = MediaAdapter("avi")

        assert adapter.audio_type == "avi"
        assert adapter.player is None

    def test_adapter_implements_media_player(self):
        """Test that adapter implements MediaPlayer interface."""
        adapter = MediaAdapter("mp3")

        assert isinstance(adapter, MediaPlayer)
        assert hasattr(adapter, "play")
        assert callable(adapter.play)

    def test_adapter_play_mp3(self, capsys):
        """Test adapter playing MP3 file."""
        adapter = MediaAdapter("mp3")

        adapter.play("mp3", "song.mp3")

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out

    def test_adapter_play_mp4(self, capsys):
        """Test adapter playing MP4 file."""
        adapter = MediaAdapter("mp4")

        adapter.play("mp4", "video.mp4")

        captured = capsys.readouterr()
        assert "Playing MP4 file: video.mp4" in captured.out

    def test_adapter_play_vlc(self, capsys):
        """Test adapter playing VLC file."""
        adapter = MediaAdapter("vlc")

        adapter.play("vlc", "movie.vlc")

        captured = capsys.readouterr()
        assert "Playing VLC file: movie.vlc" in captured.out

    def test_adapter_play_unsupported_format(self, capsys):
        """Test adapter with unsupported format."""
        adapter = MediaAdapter("avi")

        adapter.play("avi", "video.avi")

        captured = capsys.readouterr()
        assert "Media format avi not supported" in captured.out

    def test_adapter_play_wrong_type(self, capsys):
        """Test adapter with wrong audio type."""
        adapter = MediaAdapter("mp3")

        adapter.play("mp4", "video.mp4")

        captured = capsys.readouterr()
        assert "Media format mp4 not supported" in captured.out

    def test_adapter_play_none_player(self, capsys):
        """Test adapter with None player."""
        adapter = MediaAdapter("unsupported")

        adapter.play("unsupported", "file.unsupported")

        captured = capsys.readouterr()
        assert "Media format unsupported not supported" in captured.out


class TestAudioPlayer:
    """Test AudioPlayer implementation."""

    def test_audio_player_creation(self):
        """Test creating audio player."""
        player = AudioPlayer()

        assert isinstance(player, AudioPlayer)
        assert isinstance(player, MediaPlayer)
        assert isinstance(player.adapters, dict)
        assert len(player.adapters) == 0

    def test_audio_player_play_mp3(self, capsys):
        """Test playing MP3 file (direct support)."""
        player = AudioPlayer()

        player.play("mp3", "song.mp3")

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out

    def test_audio_player_play_mp3_case_insensitive(self, capsys):
        """Test playing MP3 file with different case."""
        player = AudioPlayer()

        player.play("MP3", "song.mp3")

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out

    def test_audio_player_play_mp4(self, capsys):
        """Test playing MP4 file (via adapter)."""
        player = AudioPlayer()

        player.play("mp4", "video.mp4")

        captured = capsys.readouterr()
        assert "Playing MP4 file: video.mp4" in captured.out

        # Adapter should be created and stored
        assert "mp4" in player.adapters
        assert isinstance(player.adapters["mp4"], MediaAdapter)

    def test_audio_player_play_vlc(self, capsys):
        """Test playing VLC file (via adapter)."""
        player = AudioPlayer()

        player.play("vlc", "movie.vlc")

        captured = capsys.readouterr()
        assert "Playing VLC file: movie.vlc" in captured.out

        # Adapter should be created and stored
        assert "vlc" in player.adapters
        assert isinstance(player.adapters["vlc"], MediaAdapter)

    def test_audio_player_play_unsupported(self, capsys):
        """Test playing unsupported format."""
        player = AudioPlayer()

        player.play("avi", "video.avi")

        captured = capsys.readouterr()
        assert "Media format avi not supported" in captured.out

    def test_audio_player_adapter_reuse(self, capsys):
        """Test that adapters are reused."""
        player = AudioPlayer()

        # Play MP4 file twice
        player.play("mp4", "video1.mp4")
        player.play("mp4", "video2.mp4")

        # Should only create one adapter
        assert len(player.adapters) == 1
        assert "mp4" in player.adapters

        captured = capsys.readouterr()
        assert "Playing MP4 file: video1.mp4" in captured.out
        assert "Playing MP4 file: video2.mp4" in captured.out

    def test_audio_player_multiple_formats(self, capsys):
        """Test playing multiple formats."""
        player = AudioPlayer()

        player.play("mp3", "song.mp3")
        player.play("mp4", "video.mp4")
        player.play("vlc", "movie.vlc")

        # Should create adapters for mp4 and vlc
        assert len(player.adapters) == 2
        assert "mp4" in player.adapters
        assert "vlc" in player.adapters
        assert "mp3" not in player.adapters  # Direct support

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out
        assert "Playing MP4 file: video.mp4" in captured.out
        assert "Playing VLC file: movie.vlc" in captured.out


class TestDatabaseAdapters:
    """Test database adapter implementations."""

    def test_mysql_connection_creation(self):
        """Test creating MySQL connection."""
        conn = MySQLConnection("localhost", "user", "password", "mydb")

        assert conn.host == "localhost"
        assert conn.user == "user"
        assert conn.password == "password"
        assert conn.database == "mydb"
        assert conn.connected is False

    def test_mysql_connection_connect(self, capsys):
        """Test MySQL connection connect."""
        conn = MySQLConnection("localhost", "user", "password", "mydb")

        conn.mysql_connect()

        assert conn.connected is True
        captured = capsys.readouterr()
        assert "Connecting to MySQL database mydb on localhost" in captured.out

    def test_mysql_connection_query(self, capsys):
        """Test MySQL connection query."""
        conn = MySQLConnection("localhost", "user", "password", "mydb")
        conn.mysql_connect()

        results = conn.mysql_query("SELECT * FROM users")

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "John"}
        assert results[1] == {"id": 2, "name": "Jane"}

        captured = capsys.readouterr()
        assert "Executing MySQL query: SELECT * FROM users" in captured.out

    def test_mysql_connection_query_not_connected(self):
        """Test MySQL connection query when not connected."""
        conn = MySQLConnection("localhost", "user", "password", "mydb")

        with pytest.raises(RuntimeError) as exc_info:
            conn.mysql_query("SELECT * FROM users")

        assert "Not connected to MySQL database" in str(exc_info.value)

    def test_mysql_connection_disconnect(self, capsys):
        """Test MySQL connection disconnect."""
        conn = MySQLConnection("localhost", "user", "password", "mydb")
        conn.mysql_connect()

        conn.mysql_disconnect()

        assert conn.connected is False
        captured = capsys.readouterr()
        assert "Disconnecting from MySQL database" in captured.out

    def test_postgresql_connection_creation(self):
        """Test creating PostgreSQL connection."""
        conn = PostgreSQLConnection("localhost", "user", "password", "mydb")

        assert conn.host == "localhost"
        assert conn.user == "user"
        assert conn.password == "password"
        assert conn.database == "mydb"
        assert conn.connected is False

    def test_postgresql_connection_connect(self, capsys):
        """Test PostgreSQL connection connect."""
        conn = PostgreSQLConnection("localhost", "user", "password", "mydb")

        conn.pg_connect()

        assert conn.connected is True
        captured = capsys.readouterr()
        assert "Connecting to PostgreSQL database mydb on localhost" in captured.out

    def test_postgresql_connection_query(self, capsys):
        """Test PostgreSQL connection query."""
        conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
        conn.pg_connect()

        results = conn.pg_execute("SELECT * FROM users")

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "Alice"}
        assert results[1] == {"id": 2, "name": "Bob"}

        captured = capsys.readouterr()
        assert "Executing PostgreSQL query: SELECT * FROM users" in captured.out

    def test_postgresql_connection_query_not_connected(self):
        """Test PostgreSQL connection query when not connected."""
        conn = PostgreSQLConnection("localhost", "user", "password", "mydb")

        with pytest.raises(RuntimeError) as exc_info:
            conn.pg_execute("SELECT * FROM users")

        assert "Not connected to PostgreSQL database" in str(exc_info.value)

    def test_mysql_adapter_creation(self):
        """Test creating MySQL adapter."""
        mysql_conn = MySQLConnection("localhost", "user", "password", "mydb")
        adapter = MySQLAdapter(mysql_conn)

        assert adapter.mysql_connection is mysql_conn
        assert isinstance(adapter, DatabaseConnection)

    def test_mysql_adapter_connect(self, capsys):
        """Test MySQL adapter connect."""
        mysql_conn = MySQLConnection("localhost", "user", "password", "mydb")
        adapter = MySQLAdapter(mysql_conn)

        adapter.connect()

        assert mysql_conn.connected is True
        captured = capsys.readouterr()
        assert "Connecting to MySQL database mydb on localhost" in captured.out

    def test_mysql_adapter_query(self, capsys):
        """Test MySQL adapter query."""
        mysql_conn = MySQLConnection("localhost", "user", "password", "mydb")
        adapter = MySQLAdapter(mysql_conn)

        adapter.connect()
        results = adapter.query("SELECT * FROM users")

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "John"}

        captured = capsys.readouterr()
        assert "Executing MySQL query: SELECT * FROM users" in captured.out

    def test_mysql_adapter_close(self, capsys):
        """Test MySQL adapter close."""
        mysql_conn = MySQLConnection("localhost", "user", "password", "mydb")
        adapter = MySQLAdapter(mysql_conn)

        adapter.connect()
        adapter.close()

        assert mysql_conn.connected is False
        captured = capsys.readouterr()
        assert "Disconnecting from MySQL database" in captured.out

    def test_postgresql_adapter_creation(self):
        """Test creating PostgreSQL adapter."""
        pg_conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
        adapter = PostgreSQLAdapter(pg_conn)

        assert adapter.postgresql_connection is pg_conn
        assert isinstance(adapter, DatabaseConnection)

    def test_postgresql_adapter_connect(self, capsys):
        """Test PostgreSQL adapter connect."""
        pg_conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
        adapter = PostgreSQLAdapter(pg_conn)

        adapter.connect()

        assert pg_conn.connected is True
        captured = capsys.readouterr()
        assert "Connecting to PostgreSQL database mydb on localhost" in captured.out

    def test_postgresql_adapter_query(self, capsys):
        """Test PostgreSQL adapter query."""
        pg_conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
        adapter = PostgreSQLAdapter(pg_conn)

        adapter.connect()
        results = adapter.query("SELECT * FROM users")

        assert isinstance(results, list)
        assert len(results) == 2
        assert results[0] == {"id": 1, "name": "Alice"}

        captured = capsys.readouterr()
        assert "Executing PostgreSQL query: SELECT * FROM users" in captured.out

    def test_postgresql_adapter_close(self, capsys):
        """Test PostgreSQL adapter close."""
        pg_conn = PostgreSQLConnection("localhost", "user", "password", "mydb")
        adapter = PostgreSQLAdapter(pg_conn)

        adapter.connect()
        adapter.close()

        assert pg_conn.connected is False
        captured = capsys.readouterr()
        assert "Disconnecting from PostgreSQL database" in captured.out


class TestPaymentAdapters:
    """Test payment adapter implementations."""

    def test_paypal_gateway_creation(self):
        """Test creating PayPal gateway."""
        gateway = PayPalGateway()

        assert isinstance(gateway, PayPalGateway)
        assert hasattr(gateway, "make_payment")

    def test_paypal_gateway_make_payment(self, capsys):
        """Test PayPal gateway make payment."""
        gateway = PayPalGateway()

        result = gateway.make_payment(99.99, "customer@example.com")

        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert result["transaction_id"] == "PP123456"

        captured = capsys.readouterr()
        assert (
            "Processing PayPal payment of $99.99 for customer@example.com"
            in captured.out
        )

    def test_stripe_gateway_creation(self):
        """Test creating Stripe gateway."""
        gateway = StripeGateway()

        assert isinstance(gateway, StripeGateway)
        assert hasattr(gateway, "charge_card")

    def test_stripe_gateway_charge_card(self, capsys):
        """Test Stripe gateway charge card."""
        gateway = StripeGateway()

        result = gateway.charge_card(9999, "tok_1234")

        assert isinstance(result, dict)
        assert result["status"] == "succeeded"
        assert result["charge_id"] == "ch_123456"

        captured = capsys.readouterr()
        assert "Processing Stripe payment of $99.99 with token tok_1234" in captured.out

    def test_paypal_adapter_creation(self):
        """Test creating PayPal adapter."""
        gateway = PayPalGateway()
        adapter = PayPalAdapter(gateway, "customer@example.com")

        assert adapter.paypal_gateway is gateway
        assert adapter.email == "customer@example.com"
        assert isinstance(adapter, PaymentProcessor)

    def test_paypal_adapter_process_payment(self, capsys):
        """Test PayPal adapter process payment."""
        gateway = PayPalGateway()
        adapter = PayPalAdapter(gateway, "customer@example.com")

        result = adapter.process_payment(99.99, "1234567890123456")

        assert result is True
        captured = capsys.readouterr()
        assert (
            "Processing PayPal payment of $99.99 for customer@example.com"
            in captured.out
        )

    def test_stripe_adapter_creation(self):
        """Test creating Stripe adapter."""
        gateway = StripeGateway()
        adapter = StripeAdapter(gateway)

        assert adapter.stripe_gateway is gateway
        assert isinstance(adapter, PaymentProcessor)

    def test_stripe_adapter_process_payment(self, capsys):
        """Test Stripe adapter process payment."""
        gateway = StripeGateway()
        adapter = StripeAdapter(gateway)

        result = adapter.process_payment(99.99, "1234567890123456")

        assert result is True
        captured = capsys.readouterr()
        assert "Processing Stripe payment of $99.99 with token tok_3456" in captured.out

    def test_stripe_adapter_token_generation(self):
        """Test Stripe adapter token generation."""
        gateway = StripeGateway()
        adapter = StripeAdapter(gateway)

        # Mock the charge_card method to capture the token
        original_charge_card = gateway.charge_card

        def mock_charge_card(amount_cents, token):
            # Verify token is generated correctly
            assert token == "tok_3456"  # Last 4 digits of card
            assert amount_cents == 9999  # 99.99 * 100
            return original_charge_card(amount_cents, token)

        gateway.charge_card = mock_charge_card

        result = adapter.process_payment(99.99, "1234567890123456")
        assert result is True

    def test_payment_adapters_implement_interface(self):
        """Test that payment adapters implement PaymentProcessor interface."""
        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "test@example.com")

        stripe_gateway = StripeGateway()
        stripe_adapter = StripeAdapter(stripe_gateway)

        assert isinstance(paypal_adapter, PaymentProcessor)
        assert isinstance(stripe_adapter, PaymentProcessor)
        assert hasattr(paypal_adapter, "process_payment")
        assert hasattr(stripe_adapter, "process_payment")
        assert callable(paypal_adapter.process_payment)
        assert callable(stripe_adapter.process_payment)


class TestRectangleAdapter:
    """Test rectangle adapter implementation."""

    def test_rectangle_creation(self):
        """Test creating rectangle."""
        rect = Rectangle(100, 50)

        assert rect.width == 100
        assert rect.height == 50

    def test_rectangle_draw(self, capsys):
        """Test rectangle draw."""
        rect = Rectangle(100, 50)

        rect.draw(10, 20)

        captured = capsys.readouterr()
        assert "Drawing rectangle (100x50) at (10, 20)" in captured.out

    def test_legacy_rectangle_creation(self):
        """Test creating legacy rectangle."""
        legacy_rect = LegacyRectangle(10, 20, 110, 70)

        assert legacy_rect.x1 == 10
        assert legacy_rect.y1 == 20
        assert legacy_rect.x2 == 110
        assert legacy_rect.y2 == 70

    def test_legacy_rectangle_draw(self, capsys):
        """Test legacy rectangle draw."""
        legacy_rect = LegacyRectangle(10, 20, 110, 70)

        legacy_rect.old_draw()

        captured = capsys.readouterr()
        assert "Drawing legacy rectangle from (10, 20) to (110, 70)" in captured.out

    def test_legacy_rectangle_adapter_creation(self):
        """Test creating legacy rectangle adapter."""
        legacy_rect = LegacyRectangle(10, 20, 110, 70)
        adapter = LegacyRectangleAdapter(legacy_rect)

        assert adapter.legacy_rectangle is legacy_rect
        assert adapter.width == 100  # |110 - 10|
        assert adapter.height == 50  # |70 - 20|
        assert isinstance(adapter, Rectangle)

    def test_legacy_rectangle_adapter_draw(self, capsys):
        """Test legacy rectangle adapter draw."""
        legacy_rect = LegacyRectangle(0, 0, 100, 50)
        adapter = LegacyRectangleAdapter(legacy_rect)

        adapter.draw(10, 20)

        # Should update legacy rectangle coordinates
        assert legacy_rect.x1 == 10
        assert legacy_rect.y1 == 20
        assert legacy_rect.x2 == 110  # 10 + 100
        assert legacy_rect.y2 == 70  # 20 + 50

        captured = capsys.readouterr()
        assert "Drawing legacy rectangle from (10, 20) to (110, 70)" in captured.out

    def test_legacy_rectangle_adapter_negative_dimensions(self):
        """Test legacy rectangle adapter with negative dimensions."""
        legacy_rect = LegacyRectangle(110, 70, 10, 20)  # Reversed coordinates
        adapter = LegacyRectangleAdapter(legacy_rect)

        assert adapter.width == 100  # abs(10 - 110)
        assert adapter.height == 50  # abs(20 - 70)

    def test_legacy_rectangle_adapter_inheritance(self):
        """Test legacy rectangle adapter inheritance."""
        legacy_rect = LegacyRectangle(0, 0, 100, 50)
        adapter = LegacyRectangleAdapter(legacy_rect)

        # Should inherit from Rectangle
        assert isinstance(adapter, Rectangle)
        assert hasattr(adapter, "width")
        assert hasattr(adapter, "height")
        assert hasattr(adapter, "draw")
        assert callable(adapter.draw)


class TestPaymentService:
    """Test payment service implementation."""

    def test_payment_service_creation(self):
        """Test creating payment service."""
        service = PaymentService()

        assert isinstance(service.processors, dict)
        assert len(service.processors) == 0

    def test_payment_service_add_processor(self):
        """Test adding payment processor."""
        service = PaymentService()

        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "test@example.com")

        service.add_processor("paypal", paypal_adapter)

        assert "paypal" in service.processors
        assert service.processors["paypal"] is paypal_adapter

    def test_payment_service_process_payment_success(self, capsys):
        """Test successful payment processing."""
        service = PaymentService()

        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "test@example.com")
        service.add_processor("paypal", paypal_adapter)

        result = service.process_payment("paypal", 99.99, "1234567890123456")

        assert result is True
        captured = capsys.readouterr()
        assert (
            "Processing PayPal payment of $99.99 for test@example.com" in captured.out
        )

    def test_payment_service_process_payment_unknown_processor(self, capsys):
        """Test payment processing with unknown processor."""
        service = PaymentService()

        result = service.process_payment("unknown", 99.99, "1234567890123456")

        assert result is False
        captured = capsys.readouterr()
        assert "Payment processor unknown not available" in captured.out

    def test_payment_service_multiple_processors(self):
        """Test payment service with multiple processors."""
        service = PaymentService()

        # Add PayPal processor
        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "test@example.com")
        service.add_processor("paypal", paypal_adapter)

        # Add Stripe processor
        stripe_gateway = StripeGateway()
        stripe_adapter = StripeAdapter(stripe_gateway)
        service.add_processor("stripe", stripe_adapter)

        assert len(service.processors) == 2
        assert "paypal" in service.processors
        assert "stripe" in service.processors

    def test_payment_service_process_different_processors(self, capsys):
        """Test processing payments with different processors."""
        service = PaymentService()

        # Add processors
        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "test@example.com")
        service.add_processor("paypal", paypal_adapter)

        stripe_gateway = StripeGateway()
        stripe_adapter = StripeAdapter(stripe_gateway)
        service.add_processor("stripe", stripe_adapter)

        # Process PayPal payment
        result1 = service.process_payment("paypal", 99.99, "1234567890123456")
        assert result1 is True

        # Process Stripe payment
        result2 = service.process_payment("stripe", 149.99, "1234567890123456")
        assert result2 is True

        captured = capsys.readouterr()
        assert (
            "Processing PayPal payment of $99.99 for test@example.com" in captured.out
        )
        assert (
            "Processing Stripe payment of $149.99 with token tok_3456" in captured.out
        )


class TestAdapterPatternIntegration:
    """Test integration scenarios with adapter pattern."""

    def test_complete_media_system(self, capsys):
        """Test complete media system with multiple adapters."""
        player = AudioPlayer()

        # Play different formats
        media_files = [
            ("mp3", "song.mp3"),
            ("mp4", "video.mp4"),
            ("vlc", "movie.vlc"),
            ("mp3", "another_song.mp3"),
            ("mp4", "another_video.mp4"),
        ]

        for audio_type, filename in media_files:
            player.play(audio_type, filename)

        # Should create adapters for mp4 and vlc only
        assert len(player.adapters) == 2
        assert "mp4" in player.adapters
        assert "vlc" in player.adapters

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out
        assert "Playing MP4 file: video.mp4" in captured.out
        assert "Playing VLC file: movie.vlc" in captured.out
        assert "Playing MP3 file: another_song.mp3" in captured.out
        assert "Playing MP4 file: another_video.mp4" in captured.out

    def test_complete_database_system(self, capsys):
        """Test complete database system with multiple adapters."""
        # Create connections
        mysql_conn = MySQLConnection("mysql-host", "user", "password", "mydb")
        pg_conn = PostgreSQLConnection("pg-host", "user", "password", "mydb")

        # Create adapters
        mysql_adapter = MySQLAdapter(mysql_conn)
        pg_adapter = PostgreSQLAdapter(pg_conn)

        # Use both adapters with same interface
        adapters = [mysql_adapter, pg_adapter]

        for adapter in adapters:
            adapter.connect()
            results = adapter.query("SELECT * FROM users")
            assert isinstance(results, list)
            assert len(results) == 2
            adapter.close()

        captured = capsys.readouterr()
        assert "Connecting to MySQL database mydb on mysql-host" in captured.out
        assert "Connecting to PostgreSQL database mydb on pg-host" in captured.out
        assert "Executing MySQL query: SELECT * FROM users" in captured.out
        assert "Executing PostgreSQL query: SELECT * FROM users" in captured.out
        assert "Disconnecting from MySQL database" in captured.out
        assert "Disconnecting from PostgreSQL database" in captured.out

    def test_complete_payment_system(self, capsys):
        """Test complete payment system with multiple adapters."""
        service = PaymentService()

        # Add multiple payment processors
        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "customer@example.com")
        service.add_processor("paypal", paypal_adapter)

        stripe_gateway = StripeGateway()
        stripe_adapter = StripeAdapter(stripe_gateway)
        service.add_processor("stripe", stripe_adapter)

        # Process multiple payments
        payments = [
            ("paypal", 99.99, "1234567890123456"),
            ("stripe", 149.99, "1234567890123456"),
            ("paypal", 49.99, "1234567890123456"),
            ("unknown", 199.99, "1234567890123456"),
        ]

        results = []
        for processor, amount, card in payments:
            result = service.process_payment(processor, amount, card)
            results.append(result)

        assert results == [True, True, True, False]

        captured = capsys.readouterr()
        assert (
            "Processing PayPal payment of $99.99 for customer@example.com"
            in captured.out
        )
        assert (
            "Processing Stripe payment of $149.99 with token tok_3456" in captured.out
        )
        assert (
            "Processing PayPal payment of $49.99 for customer@example.com"
            in captured.out
        )
        assert "Payment processor unknown not available" in captured.out

    def test_mixed_rectangle_system(self, capsys):
        """Test mixed rectangle system with adapters."""
        # Create different rectangle types
        modern_rect = Rectangle(100, 50)
        legacy_rect = LegacyRectangle(0, 0, 120, 60)
        adapted_rect = LegacyRectangleAdapter(legacy_rect)

        # Use them with same interface
        rectangles = [modern_rect, adapted_rect]

        for i, rect in enumerate(rectangles):
            rect.draw(i * 10, i * 20)

        captured = capsys.readouterr()
        assert "Drawing rectangle (100x50) at (0, 0)" in captured.out
        assert "Drawing legacy rectangle from (10, 20) to (130, 80)" in captured.out

    def test_adapter_composition(self, capsys):
        """Test composing multiple adapters."""
        # Create a system that uses multiple types of adapters

        # Media system
        media_player = AudioPlayer()
        media_player.play("mp4", "presentation.mp4")

        # Database system
        db_conn = MySQLConnection("localhost", "user", "password", "testdb")
        db_adapter = MySQLAdapter(db_conn)
        db_adapter.connect()
        db_adapter.query("SELECT * FROM media_files")
        db_adapter.close()

        # Payment system
        payment_service = PaymentService()
        paypal_gateway = PayPalGateway()
        paypal_adapter = PayPalAdapter(paypal_gateway, "user@example.com")
        payment_service.add_processor("paypal", paypal_adapter)
        payment_service.process_payment("paypal", 29.99, "1234567890123456")

        captured = capsys.readouterr()
        assert "Playing MP4 file: presentation.mp4" in captured.out
        assert "Connecting to MySQL database testdb on localhost" in captured.out
        assert "Executing MySQL query: SELECT * FROM media_files" in captured.out
        assert "Disconnecting from MySQL database" in captured.out
        assert (
            "Processing PayPal payment of $29.99 for user@example.com" in captured.out
        )


class TestAdapterPatternEdgeCases:
    """Test edge cases and error conditions."""

    def test_adapter_with_null_adaptee(self):
        """Test adapter with null adaptee."""
        # Create adapter with unsupported type
        adapter = MediaAdapter("unsupported")

        assert adapter.player is None

        # Should handle gracefully
        adapter.play("unsupported", "file.unsupported")

    def test_database_adapter_connection_error(self):
        """Test database adapter with connection error."""
        # Mock connection that fails
        mock_conn = Mock()
        mock_conn.mysql_connect.side_effect = RuntimeError("Connection failed")

        adapter = MySQLAdapter(mock_conn)

        with pytest.raises(RuntimeError):
            adapter.connect()

    def test_payment_adapter_gateway_error(self):
        """Test payment adapter with gateway error."""
        # Mock gateway that fails
        mock_gateway = Mock()
        mock_gateway.make_payment.return_value = {"status": "failure"}

        adapter = PayPalAdapter(mock_gateway, "test@example.com")

        result = adapter.process_payment(100.0, "1234567890123456")
        assert result is False

    def test_rectangle_adapter_zero_dimensions(self):
        """Test rectangle adapter with zero dimensions."""
        legacy_rect = LegacyRectangle(10, 20, 10, 20)  # Zero dimensions
        adapter = LegacyRectangleAdapter(legacy_rect)

        assert adapter.width == 0
        assert adapter.height == 0

    def test_audio_player_empty_filename(self, capsys):
        """Test audio player with empty filename."""
        player = AudioPlayer()

        player.play("mp3", "")

        captured = capsys.readouterr()
        assert "Playing MP3 file:" in captured.out

    def test_audio_player_none_filename(self, capsys):
        """Test audio player with None filename."""
        player = AudioPlayer()

        player.play("mp3", None)

        captured = capsys.readouterr()
        assert "Playing MP3 file: None" in captured.out

    def test_payment_service_replace_processor(self):
        """Test replacing a payment processor."""
        service = PaymentService()

        # Add first processor
        paypal_gateway1 = PayPalGateway()
        paypal_adapter1 = PayPalAdapter(paypal_gateway1, "user1@example.com")
        service.add_processor("paypal", paypal_adapter1)

        # Replace with second processor
        paypal_gateway2 = PayPalGateway()
        paypal_adapter2 = PayPalAdapter(paypal_gateway2, "user2@example.com")
        service.add_processor("paypal", paypal_adapter2)

        # Should have the second processor
        assert len(service.processors) == 1
        assert service.processors["paypal"] is paypal_adapter2

    def test_media_adapter_case_sensitivity(self, capsys):
        """Test media adapter case sensitivity."""
        adapter = MediaAdapter("mp3")

        # Should work with lowercase
        adapter.play("mp3", "song.mp3")

        # Should not work with uppercase (different from AudioPlayer)
        adapter.play("MP3", "song.mp3")

        captured = capsys.readouterr()
        assert "Playing MP3 file: song.mp3" in captured.out
        assert "Media format MP3 not supported" in captured.out


class TestAdapterPatternPerformance:
    """Test performance characteristics of adapter pattern."""

    def test_adapter_creation_performance(self):
        """Test performance of adapter creation."""
        import time

        # Test creating many adapters
        start = time.time()
        adapters = []
        for i in range(1000):
            adapter = MediaAdapter("mp3")
            adapters.append(adapter)
        end = time.time()

        creation_time = end - start
        assert creation_time < 0.1  # Should be fast
        assert len(adapters) == 1000

    def test_audio_player_adapter_caching(self):
        """Test that AudioPlayer caches adapters efficiently."""
        import time

        player = AudioPlayer()

        # First call - should create adapter
        start = time.time()
        player.play("mp4", "video1.mp4")
        first_call_time = time.time() - start

        # Second call - should reuse adapter
        start = time.time()
        player.play("mp4", "video2.mp4")
        second_call_time = time.time() - start

        # Second call should be faster (no adapter creation)
        assert second_call_time <= first_call_time
        assert len(player.adapters) == 1

    def test_payment_service_performance(self):
        """Test payment service performance with many processors."""
        import time

        service = PaymentService()

        # Add many processors
        for i in range(100):
            gateway = PayPalGateway()
            adapter = PayPalAdapter(gateway, f"user{i}@example.com")
            service.add_processor(f"paypal{i}", adapter)

        # Process payments
        start = time.time()
        for i in range(100):
            service.process_payment(f"paypal{i}", 10.0, "1234567890123456")
        end = time.time()

        processing_time = end - start
        assert processing_time < 1.0  # Should complete quickly

    def test_large_scale_adaptation(self):
        """Test large-scale adaptation scenario."""
        import time

        # Create many legacy rectangles
        legacy_rectangles = []
        for i in range(1000):
            legacy_rect = LegacyRectangle(i, i, i + 10, i + 10)
            legacy_rectangles.append(legacy_rect)

        # Adapt them all
        start = time.time()
        adapted_rectangles = []
        for legacy_rect in legacy_rectangles:
            adapter = LegacyRectangleAdapter(legacy_rect)
            adapted_rectangles.append(adapter)
        end = time.time()

        adaptation_time = end - start
        assert adaptation_time < 0.5  # Should be efficient
        assert len(adapted_rectangles) == 1000
        assert all(isinstance(r, Rectangle) for r in adapted_rectangles)
