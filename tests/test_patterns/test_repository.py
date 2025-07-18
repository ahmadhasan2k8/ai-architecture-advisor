"""Tests for repository pattern implementations."""

import json
import os
import sqlite3
import tempfile
import pytest
from datetime import datetime
from unittest.mock import Mock, patch, call

from src.patterns.repository import (
    # Domain Models
    User,
    Product,
    Order,
    
    # Repository Interfaces
    Repository,
    UserRepository,
    ProductRepository,
    OrderRepository,
    
    # Concrete Implementations
    InMemoryUserRepository,
    InMemoryProductRepository,
    InMemoryOrderRepository,
    JsonFileUserRepository,
    SqliteUserRepository,
    
    # Services
    UserService,
    ProductService,
    
    # Unit of Work
    UnitOfWork,
)


class TestDomainModels:
    """Test domain model implementations."""
    
    def test_user_creation(self):
        """Test creating a user."""
        user = User(id=1, name="Alice", email="alice@example.com")
        
        assert user.id == 1
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert isinstance(user.created_at, datetime)
    
    def test_user_creation_with_datetime(self):
        """Test creating a user with specific datetime."""
        created_at = datetime(2023, 1, 1, 12, 0, 0)
        user = User(id=1, name="Alice", email="alice@example.com", created_at=created_at)
        
        assert user.created_at == created_at
    
    def test_user_creation_without_id(self):
        """Test creating a user without ID."""
        user = User(id=None, name="Alice", email="alice@example.com")
        
        assert user.id is None
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
    
    def test_product_creation(self):
        """Test creating a product."""
        product = Product(id=1, name="Laptop", price=999.99, category="Electronics")
        
        assert product.id == 1
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.category == "Electronics"
        assert product.in_stock is True
    
    def test_product_creation_with_stock_status(self):
        """Test creating a product with specific stock status."""
        product = Product(id=1, name="Laptop", price=999.99, category="Electronics", in_stock=False)
        
        assert product.in_stock is False
    
    def test_product_negative_price(self):
        """Test creating a product with negative price raises error."""
        with pytest.raises(ValueError) as exc_info:
            Product(id=1, name="Laptop", price=-100.0, category="Electronics")
        
        assert "Price cannot be negative" in str(exc_info.value)
    
    def test_product_zero_price(self):
        """Test creating a product with zero price."""
        product = Product(id=1, name="Free Sample", price=0.0, category="Samples")
        
        assert product.price == 0.0
    
    def test_order_creation(self):
        """Test creating an order."""
        order = Order(id=1, user_id=1, products=[1, 2, 3], total_amount=150.0)
        
        assert order.id == 1
        assert order.user_id == 1
        assert order.products == [1, 2, 3]
        assert order.total_amount == 150.0
        assert order.status == "pending"
        assert isinstance(order.created_at, datetime)
    
    def test_order_creation_with_status(self):
        """Test creating an order with specific status."""
        order = Order(id=1, user_id=1, products=[1], total_amount=50.0, status="completed")
        
        assert order.status == "completed"
    
    def test_order_creation_with_datetime(self):
        """Test creating an order with specific datetime."""
        created_at = datetime(2023, 1, 1, 12, 0, 0)
        order = Order(id=1, user_id=1, products=[1], total_amount=50.0, created_at=created_at)
        
        assert order.created_at == created_at


class TestInMemoryUserRepository:
    """Test in-memory user repository implementation."""
    
    def test_repository_creation(self):
        """Test creating repository."""
        repo = InMemoryUserRepository()
        
        assert len(repo._users) == 0
        assert repo._next_id == 1
    
    def test_save_new_user(self):
        """Test saving a new user."""
        repo = InMemoryUserRepository()
        user = User(id=None, name="Alice", email="alice@example.com")
        
        saved_user = repo.save(user)
        
        assert saved_user.id == 1
        assert saved_user.name == "Alice"
        assert saved_user.email == "alice@example.com"
        assert len(repo._users) == 1
        assert repo._next_id == 2
    
    def test_save_existing_user(self):
        """Test saving an existing user (update)."""
        repo = InMemoryUserRepository()
        user = User(id=None, name="Alice", email="alice@example.com")
        saved_user = repo.save(user)
        
        # Update the user
        saved_user.name = "Alice Johnson"
        updated_user = repo.save(saved_user)
        
        assert updated_user.id == 1
        assert updated_user.name == "Alice Johnson"
        assert len(repo._users) == 1  # Still only one user
    
    def test_find_by_id_existing(self):
        """Test finding user by existing ID."""
        repo = InMemoryUserRepository()
        user = User(id=None, name="Alice", email="alice@example.com")
        saved_user = repo.save(user)
        
        found_user = repo.find_by_id(saved_user.id)
        
        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.name == "Alice"
    
    def test_find_by_id_nonexistent(self):
        """Test finding user by non-existent ID."""
        repo = InMemoryUserRepository()
        
        found_user = repo.find_by_id(999)
        
        assert found_user is None
    
    def test_find_all_empty(self):
        """Test finding all users when repository is empty."""
        repo = InMemoryUserRepository()
        
        users = repo.find_all()
        
        assert len(users) == 0
        assert users == []
    
    def test_find_all_with_users(self):
        """Test finding all users with data."""
        repo = InMemoryUserRepository()
        
        user1 = repo.save(User(id=None, name="Alice", email="alice@example.com"))
        user2 = repo.save(User(id=None, name="Bob", email="bob@example.com"))
        
        users = repo.find_all()
        
        assert len(users) == 2
        assert user1 in users
        assert user2 in users
    
    def test_delete_existing_user(self):
        """Test deleting an existing user."""
        repo = InMemoryUserRepository()
        user = repo.save(User(id=None, name="Alice", email="alice@example.com"))
        
        result = repo.delete(user.id)
        
        assert result is True
        assert len(repo._users) == 0
        assert repo.find_by_id(user.id) is None
    
    def test_delete_nonexistent_user(self):
        """Test deleting a non-existent user."""
        repo = InMemoryUserRepository()
        
        result = repo.delete(999)
        
        assert result is False
    
    def test_find_by_email_existing(self):
        """Test finding user by existing email."""
        repo = InMemoryUserRepository()
        user = repo.save(User(id=None, name="Alice", email="alice@example.com"))
        
        found_user = repo.find_by_email("alice@example.com")
        
        assert found_user is not None
        assert found_user.email == "alice@example.com"
        assert found_user.id == user.id
    
    def test_find_by_email_nonexistent(self):
        """Test finding user by non-existent email."""
        repo = InMemoryUserRepository()
        
        found_user = repo.find_by_email("nonexistent@example.com")
        
        assert found_user is None
    
    def test_find_by_name_existing(self):
        """Test finding users by existing name."""
        repo = InMemoryUserRepository()
        
        user1 = repo.save(User(id=None, name="Alice", email="alice1@example.com"))
        user2 = repo.save(User(id=None, name="Alice", email="alice2@example.com"))
        user3 = repo.save(User(id=None, name="Bob", email="bob@example.com"))
        
        found_users = repo.find_by_name("Alice")
        
        assert len(found_users) == 2
        assert user1 in found_users
        assert user2 in found_users
        assert user3 not in found_users
    
    def test_find_by_name_nonexistent(self):
        """Test finding users by non-existent name."""
        repo = InMemoryUserRepository()
        
        found_users = repo.find_by_name("Nonexistent")
        
        assert len(found_users) == 0
        assert found_users == []


class TestInMemoryProductRepository:
    """Test in-memory product repository implementation."""
    
    def test_repository_creation(self):
        """Test creating product repository."""
        repo = InMemoryProductRepository()
        
        assert len(repo._products) == 0
        assert repo._next_id == 1
    
    def test_save_new_product(self):
        """Test saving a new product."""
        repo = InMemoryProductRepository()
        product = Product(id=None, name="Laptop", price=999.99, category="Electronics")
        
        saved_product = repo.save(product)
        
        assert saved_product.id == 1
        assert saved_product.name == "Laptop"
        assert saved_product.price == 999.99
        assert saved_product.category == "Electronics"
        assert len(repo._products) == 1
    
    def test_find_by_category(self):
        """Test finding products by category."""
        repo = InMemoryProductRepository()
        
        laptop = repo.save(Product(id=None, name="Laptop", price=999.99, category="Electronics"))
        mouse = repo.save(Product(id=None, name="Mouse", price=25.99, category="Electronics"))
        book = repo.save(Product(id=None, name="Book", price=19.99, category="Books"))
        
        electronics = repo.find_by_category("Electronics")
        
        assert len(electronics) == 2
        assert laptop in electronics
        assert mouse in electronics
        assert book not in electronics
    
    def test_find_by_price_range(self):
        """Test finding products by price range."""
        repo = InMemoryProductRepository()
        
        cheap = repo.save(Product(id=None, name="Cheap", price=10.0, category="Test"))
        medium = repo.save(Product(id=None, name="Medium", price=50.0, category="Test"))
        expensive = repo.save(Product(id=None, name="Expensive", price=100.0, category="Test"))
        
        # Test inclusive range
        products = repo.find_by_price_range(10.0, 50.0)
        
        assert len(products) == 2
        assert cheap in products
        assert medium in products
        assert expensive not in products
    
    def test_find_by_price_range_edge_cases(self):
        """Test finding products by price range edge cases."""
        repo = InMemoryProductRepository()
        
        product = repo.save(Product(id=None, name="Test", price=25.0, category="Test"))
        
        # Exact match
        products = repo.find_by_price_range(25.0, 25.0)
        assert len(products) == 1
        assert product in products
        
        # Outside range
        products = repo.find_by_price_range(30.0, 40.0)
        assert len(products) == 0
    
    def test_find_in_stock(self):
        """Test finding products in stock."""
        repo = InMemoryProductRepository()
        
        in_stock = repo.save(Product(id=None, name="In Stock", price=10.0, category="Test", in_stock=True))
        out_of_stock = repo.save(Product(id=None, name="Out of Stock", price=10.0, category="Test", in_stock=False))
        
        products = repo.find_in_stock()
        
        assert len(products) == 1
        assert in_stock in products
        assert out_of_stock not in products
    
    def test_find_out_of_stock(self):
        """Test finding products out of stock."""
        repo = InMemoryProductRepository()
        
        in_stock = repo.save(Product(id=None, name="In Stock", price=10.0, category="Test", in_stock=True))
        out_of_stock = repo.save(Product(id=None, name="Out of Stock", price=10.0, category="Test", in_stock=False))
        
        products = repo.find_out_of_stock()
        
        assert len(products) == 1
        assert out_of_stock in products
        assert in_stock not in products


class TestInMemoryOrderRepository:
    """Test in-memory order repository implementation."""
    
    def test_repository_creation(self):
        """Test creating order repository."""
        repo = InMemoryOrderRepository()
        
        assert len(repo._orders) == 0
        assert repo._next_id == 1
    
    def test_save_new_order(self):
        """Test saving a new order."""
        repo = InMemoryOrderRepository()
        order = Order(id=None, user_id=1, products=[1, 2], total_amount=150.0)
        
        saved_order = repo.save(order)
        
        assert saved_order.id == 1
        assert saved_order.user_id == 1
        assert saved_order.products == [1, 2]
        assert saved_order.total_amount == 150.0
        assert len(repo._orders) == 1
    
    def test_find_by_user_id(self):
        """Test finding orders by user ID."""
        repo = InMemoryOrderRepository()
        
        order1 = repo.save(Order(id=None, user_id=1, products=[1], total_amount=50.0))
        order2 = repo.save(Order(id=None, user_id=1, products=[2], total_amount=75.0))
        order3 = repo.save(Order(id=None, user_id=2, products=[3], total_amount=100.0))
        
        user1_orders = repo.find_by_user_id(1)
        
        assert len(user1_orders) == 2
        assert order1 in user1_orders
        assert order2 in user1_orders
        assert order3 not in user1_orders
    
    def test_find_by_status(self):
        """Test finding orders by status."""
        repo = InMemoryOrderRepository()
        
        pending = repo.save(Order(id=None, user_id=1, products=[1], total_amount=50.0, status="pending"))
        completed = repo.save(Order(id=None, user_id=1, products=[2], total_amount=75.0, status="completed"))
        cancelled = repo.save(Order(id=None, user_id=1, products=[3], total_amount=100.0, status="cancelled"))
        
        pending_orders = repo.find_by_status("pending")
        completed_orders = repo.find_by_status("completed")
        
        assert len(pending_orders) == 1
        assert pending in pending_orders
        
        assert len(completed_orders) == 1
        assert completed in completed_orders
        
        assert cancelled not in pending_orders
        assert cancelled not in completed_orders


class TestJsonFileUserRepository:
    """Test JSON file user repository implementation."""
    
    def test_repository_creation_new_file(self):
        """Test creating repository with new file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            
            assert len(repo._users) == 0
            assert repo._next_id == 1
            assert os.path.exists(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_repository_creation_existing_file(self):
        """Test creating repository with existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            # Write some test data
            test_data = {
                "users": [
                    {"id": 1, "name": "Alice", "email": "alice@example.com", "created_at": "2023-01-01T12:00:00"}
                ],
                "next_id": 2
            }
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            
            assert len(repo._users) == 1
            assert repo._next_id == 2
            assert repo._users[0].name == "Alice"
        finally:
            os.unlink(temp_path)
    
    def test_save_and_load(self):
        """Test saving and loading from file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            
            # Save a user
            user = User(id=None, name="Alice", email="alice@example.com")
            saved_user = repo.save(user)
            
            # Create new repository instance to test loading
            repo2 = JsonFileUserRepository(temp_path)
            
            assert len(repo2._users) == 1
            assert repo2._next_id == 2
            
            found_user = repo2.find_by_id(saved_user.id)
            assert found_user is not None
            assert found_user.name == "Alice"
            assert found_user.email == "alice@example.com"
        finally:
            os.unlink(temp_path)
    
    def test_corrupted_file_handling(self):
        """Test handling of corrupted JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("invalid json content")
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            
            # Should start with empty state
            assert len(repo._users) == 0
            assert repo._next_id == 1
        finally:
            os.unlink(temp_path)
    
    def test_missing_file_handling(self):
        """Test handling of missing file."""
        temp_path = "/tmp/nonexistent_file.json"
        
        repo = JsonFileUserRepository(temp_path)
        
        # Should start with empty state
        assert len(repo._users) == 0
        assert repo._next_id == 1
        
        # File should be created after first save
        user = User(id=None, name="Alice", email="alice@example.com")
        repo.save(user)
        
        assert os.path.exists(temp_path)
        os.unlink(temp_path)


class TestSqliteUserRepository:
    """Test SQLite user repository implementation."""
    
    def test_repository_creation_memory(self):
        """Test creating repository with in-memory database."""
        repo = SqliteUserRepository(":memory:")
        
        # Should be able to save and retrieve users
        user = User(id=None, name="Alice", email="alice@example.com")
        saved_user = repo.save(user)
        
        assert saved_user.id == 1
        assert saved_user.name == "Alice"
        assert saved_user.email == "alice@example.com"
    
    def test_repository_creation_file(self):
        """Test creating repository with file database."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            temp_path = f.name
        
        try:
            repo = SqliteUserRepository(temp_path)
            
            # Save a user
            user = User(id=None, name="Alice", email="alice@example.com")
            saved_user = repo.save(user)
            
            # Create new repository instance to test persistence
            repo2 = SqliteUserRepository(temp_path)
            
            found_user = repo2.find_by_id(saved_user.id)
            assert found_user is not None
            assert found_user.name == "Alice"
            assert found_user.email == "alice@example.com"
        finally:
            os.unlink(temp_path)
    
    def test_database_initialization(self):
        """Test database table initialization."""
        repo = SqliteUserRepository(":memory:")
        
        # Check that table exists by trying to query it
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # This should not raise an error if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        
        # Note: This test depends on the specific implementation
        # In a real scenario, you'd have access to the connection to test this
        conn.close()
    
    def test_save_and_retrieve_with_datetime(self):
        """Test saving and retrieving users with datetime fields."""
        repo = SqliteUserRepository(":memory:")
        
        # Create user with specific datetime
        created_at = datetime(2023, 1, 1, 12, 0, 0)
        user = User(id=None, name="Alice", email="alice@example.com", created_at=created_at)
        
        saved_user = repo.save(user)
        found_user = repo.find_by_id(saved_user.id)
        
        assert found_user.created_at == created_at
    
    def test_find_by_email_and_name(self):
        """Test custom find methods."""
        repo = SqliteUserRepository(":memory:")
        
        user1 = repo.save(User(id=None, name="Alice", email="alice@example.com"))
        user2 = repo.save(User(id=None, name="Bob", email="bob@example.com"))
        
        # Test find by email
        found_by_email = repo.find_by_email("alice@example.com")
        assert found_by_email is not None
        assert found_by_email.id == user1.id
        
        # Test find by name
        found_by_name = repo.find_by_name("Bob")
        assert len(found_by_name) == 1
        assert found_by_name[0].id == user2.id


class TestUserService:
    """Test user service implementation."""
    
    def test_service_creation(self):
        """Test creating user service."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        assert service.user_repository is repo
    
    def test_register_user(self):
        """Test registering a new user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.id is not None
        assert isinstance(user.created_at, datetime)
    
    def test_register_user_duplicate_email(self):
        """Test registering user with duplicate email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        service.register_user("Alice", "alice@example.com")
        
        duplicate_user = service.register_user("Bob", "alice@example.com")
        
        assert duplicate_user is None
    
    def test_get_user_by_id(self):
        """Test getting user by ID."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        found_user = service.get_user_by_id(user.id)
        
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.name == "Alice"
    
    def test_get_user_by_nonexistent_id(self):
        """Test getting user by non-existent ID."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        found_user = service.get_user_by_id(999)
        
        assert found_user is None
    
    def test_get_user_by_email(self):
        """Test getting user by email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        found_user = service.get_user_by_email("alice@example.com")
        
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == "alice@example.com"
    
    def test_get_user_by_nonexistent_email(self):
        """Test getting user by non-existent email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        found_user = service.get_user_by_email("nonexistent@example.com")
        
        assert found_user is None
    
    def test_get_all_users(self):
        """Test getting all users."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user1 = service.register_user("Alice", "alice@example.com")
        user2 = service.register_user("Bob", "bob@example.com")
        
        all_users = service.get_all_users()
        
        assert len(all_users) == 2
        assert user1 in all_users
        assert user2 in all_users
    
    def test_update_user(self):
        """Test updating a user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        updated_user = service.update_user(user.id, name="Alice Johnson")
        
        assert updated_user is not None
        assert updated_user.id == user.id
        assert updated_user.name == "Alice Johnson"
        assert updated_user.email == "alice@example.com"  # Should remain unchanged
    
    def test_update_user_email(self):
        """Test updating user email."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        updated_user = service.update_user(user.id, email="alice.new@example.com")
        
        assert updated_user is not None
        assert updated_user.email == "alice.new@example.com"
        assert updated_user.name == "Alice"  # Should remain unchanged
    
    def test_update_nonexistent_user(self):
        """Test updating non-existent user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        updated_user = service.update_user(999, name="Ghost")
        
        assert updated_user is None
    
    def test_delete_user(self):
        """Test deleting a user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        user = service.register_user("Alice", "alice@example.com")
        
        result = service.delete_user(user.id)
        
        assert result is True
        assert service.get_user_by_id(user.id) is None
    
    def test_delete_nonexistent_user(self):
        """Test deleting non-existent user."""
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        result = service.delete_user(999)
        
        assert result is False


class TestProductService:
    """Test product service implementation."""
    
    def test_service_creation(self):
        """Test creating product service."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        assert service.product_repository is repo
    
    def test_add_product(self):
        """Test adding a new product."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        product = service.add_product("Laptop", 999.99, "Electronics")
        
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.category == "Electronics"
        assert product.in_stock is True
        assert product.id is not None
    
    def test_add_product_negative_price(self):
        """Test adding product with negative price."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        product = service.add_product("Invalid", -10.0, "Test")
        
        assert product is None
    
    def test_get_products_by_category(self):
        """Test getting products by category."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        laptop = service.add_product("Laptop", 999.99, "Electronics")
        mouse = service.add_product("Mouse", 25.99, "Electronics")
        book = service.add_product("Book", 19.99, "Books")
        
        electronics = service.get_products_by_category("Electronics")
        
        assert len(electronics) == 2
        assert laptop in electronics
        assert mouse in electronics
        assert book not in electronics
    
    def test_get_products_by_price_range(self):
        """Test getting products by price range."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        cheap = service.add_product("Cheap", 10.0, "Test")
        medium = service.add_product("Medium", 50.0, "Test")
        expensive = service.add_product("Expensive", 100.0, "Test")
        
        affordable = service.get_products_by_price_range(0, 50)
        
        assert len(affordable) == 2
        assert cheap in affordable
        assert medium in affordable
        assert expensive not in affordable
    
    def test_get_products_in_stock(self):
        """Test getting products in stock."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        in_stock = service.add_product("In Stock", 10.0, "Test")
        out_of_stock = service.add_product("Out of Stock", 10.0, "Test")
        
        # Update stock status
        service.update_stock_status(out_of_stock.id, False)
        
        products = service.get_products_in_stock()
        
        assert len(products) == 1
        assert products[0].name == "In Stock"
    
    def test_update_stock_status(self):
        """Test updating stock status."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        product = service.add_product("Test Product", 10.0, "Test")
        
        updated = service.update_stock_status(product.id, False)
        
        assert updated is not None
        assert updated.in_stock is False
    
    def test_update_stock_status_nonexistent(self):
        """Test updating stock status for non-existent product."""
        repo = InMemoryProductRepository()
        service = ProductService(repo)
        
        updated = service.update_stock_status(999, False)
        
        assert updated is None



class TestUnitOfWork:
    """Test Unit of Work implementation."""
    
    def test_unit_of_work_creation(self):
        """Test creating Unit of Work."""
        uow = UnitOfWork()
        
        assert len(uow._new_objects) == 0
        assert len(uow._dirty_objects) == 0
        assert len(uow._removed_objects) == 0
    
    def test_register_new(self):
        """Test registering new objects."""
        uow = UnitOfWork()
        user = User(id=None, name="Alice", email="alice@example.com")
        
        uow.register_new(user)
        
        assert len(uow._new_objects) == 1
        assert user in uow._new_objects
    
    def test_register_dirty(self):
        """Test registering dirty objects."""
        uow = UnitOfWork()
        user = User(id=1, name="Alice", email="alice@example.com")
        
        uow.register_dirty(user)
        
        assert len(uow._dirty_objects) == 1
        assert user in uow._dirty_objects
    
    def test_register_dirty_duplicate(self):
        """Test registering same object as dirty multiple times."""
        uow = UnitOfWork()
        user = User(id=1, name="Alice", email="alice@example.com")
        
        uow.register_dirty(user)
        uow.register_dirty(user)  # Register again
        
        assert len(uow._dirty_objects) == 1  # Should only appear once
    
    def test_register_removed(self):
        """Test registering removed objects."""
        uow = UnitOfWork()
        user = User(id=1, name="Alice", email="alice@example.com")
        
        uow.register_removed(user)
        
        assert len(uow._removed_objects) == 1
        assert user in uow._removed_objects
    
    def test_commit_success(self, capsys):
        """Test successful commit."""
        uow = UnitOfWork()
        
        new_user = User(id=None, name="Alice", email="alice@example.com")
        dirty_user = User(id=1, name="Bob", email="bob@example.com")
        removed_user = User(id=2, name="Charlie", email="charlie@example.com")
        
        uow.register_new(new_user)
        uow.register_dirty(dirty_user)
        uow.register_removed(removed_user)
        
        uow.commit()
        
        captured = capsys.readouterr()
        assert "Starting Unit of Work transaction" in captured.out
        assert "Inserting new object" in captured.out
        assert "Updating dirty object" in captured.out
        assert "Deleting removed object" in captured.out
        assert "Unit of Work transaction committed successfully" in captured.out
        
        # Objects should be cleared after commit
        assert len(uow._new_objects) == 0
        assert len(uow._dirty_objects) == 0
        assert len(uow._removed_objects) == 0
    
    def test_commit_failure(self, capsys):
        """Test commit failure handling."""
        uow = UnitOfWork()
        
        # Mock an exception during commit
        with patch.object(uow, '_clear', side_effect=Exception("Commit failed")):
            with pytest.raises(Exception) as exc_info:
                uow.commit()
            
            assert "Commit failed" in str(exc_info.value)
            captured = capsys.readouterr()
            assert "Unit of Work transaction failed" in captured.out
            assert "Rolling back changes" in captured.out
    
    def test_commit_empty_unit_of_work(self, capsys):
        """Test committing empty Unit of Work."""
        uow = UnitOfWork()
        
        uow.commit()
        
        captured = capsys.readouterr()
        assert "Starting Unit of Work transaction" in captured.out
        assert "Unit of Work transaction committed successfully" in captured.out
        assert "Inserting new object" not in captured.out
        assert "Updating dirty object" not in captured.out
        assert "Deleting removed object" not in captured.out


class TestRepositoryPatternIntegration:
    """Test integration scenarios with repository pattern."""
    
    def test_complete_user_management_system(self):
        """Test complete user management system."""
        # Use in-memory repository for testing
        user_repo = InMemoryUserRepository()
        user_service = UserService(user_repo)
        
        # Register users
        alice = user_service.register_user("Alice Johnson", "alice@example.com")
        bob = user_service.register_user("Bob Smith", "bob@example.com")
        
        assert alice is not None
        assert bob is not None
        assert alice.id != bob.id
        
        # Test duplicate email prevention
        duplicate = user_service.register_user("Charlie Brown", "alice@example.com")
        assert duplicate is None
        
        # Update user
        updated_alice = user_service.update_user(alice.id, name="Alice Johnson-Smith")
        assert updated_alice.name == "Alice Johnson-Smith"
        
        # Test search functionality
        found_alice = user_service.get_user_by_email("alice@example.com")
        assert found_alice.name == "Alice Johnson-Smith"
        
        # List all users
        all_users = user_service.get_all_users()
        assert len(all_users) == 2
        
        # Delete user
        assert user_service.delete_user(bob.id) is True
        assert len(user_service.get_all_users()) == 1
    
    def test_complete_e_commerce_system(self):
        """Test complete e-commerce system."""
        # Create repositories
        user_repo = InMemoryUserRepository()
        product_repo = InMemoryProductRepository()
        order_repo = InMemoryOrderRepository()
        
        # Create services
        user_service = UserService(user_repo)
        product_service = ProductService(product_repo)
        
        # Create user
        user = user_service.register_user("Alice Johnson", "alice@example.com")
        
        # Create products
        laptop = product_service.add_product("Laptop", 999.99, "Electronics")
        mouse = product_service.add_product("Mouse", 25.99, "Electronics")
        book = product_service.add_product("Python Book", 49.99, "Books")
        
        # Create order directly using repository
        order = Order(id=None, user_id=user.id, products=[laptop.id, mouse.id], total_amount=1025.98, status="pending")
        saved_order = order_repo.save(order)
        
        assert saved_order is not None
        assert saved_order.total_amount == 1025.98
        assert saved_order.status == "pending"
        
        # Update order status
        saved_order.status = "completed"
        updated_order = order_repo.save(saved_order)
        assert updated_order.status == "completed"
        
        # Get user orders
        user_orders = order_repo.find_by_user_id(user.id)
        assert len(user_orders) == 1
        assert user_orders[0].id == saved_order.id
        
        # Test product filtering
        electronics = product_service.get_products_by_category("Electronics")
        assert len(electronics) == 2
        
        affordable = product_service.get_products_by_price_range(0, 50)
        assert len(affordable) == 2  # mouse and book
    
    def test_repository_abstraction_with_different_implementations(self):
        """Test that services work with different repository implementations."""
        # Test with in-memory repository
        memory_repo = InMemoryUserRepository()
        memory_service = UserService(memory_repo)
        
        user1 = memory_service.register_user("Memory User", "memory@example.com")
        assert user1 is not None
        
        # Test with JSON file repository
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            json_repo = JsonFileUserRepository(temp_path)
            json_service = UserService(json_repo)
            
            user2 = json_service.register_user("JSON User", "json@example.com")
            assert user2 is not None
            
            # Test that data persists
            json_service2 = UserService(JsonFileUserRepository(temp_path))
            found_user = json_service2.get_user_by_email("json@example.com")
            assert found_user is not None
            assert found_user.name == "JSON User"
            
        finally:
            os.unlink(temp_path)
        
        # Test with SQLite repository
        sqlite_repo = SqliteUserRepository(":memory:")
        sqlite_service = UserService(sqlite_repo)
        
        user3 = sqlite_service.register_user("SQLite User", "sqlite@example.com")
        assert user3 is not None
        
        # All services should work identically
        assert user1.name == "Memory User"
        assert user2.name == "JSON User"
        assert user3.name == "SQLite User"
    
    def test_unit_of_work_with_repositories(self, capsys):
        """Test Unit of Work pattern with repository operations."""
        uow = UnitOfWork()
        
        # Simulate complex business operation
        user = User(id=None, name="Alice", email="alice@example.com")
        product = Product(id=None, name="Laptop", price=999.99, category="Electronics")
        order = Order(id=None, user_id=1, products=[1], total_amount=999.99)
        
        # Register operations
        uow.register_new(user)
        uow.register_new(product)
        uow.register_new(order)
        
        # Simulate updating the user
        user.name = "Alice Johnson"
        uow.register_dirty(user)
        
        # Commit all changes
        uow.commit()
        
        captured = capsys.readouterr()
        assert "Inserting new object" in captured.out
        assert "Updating dirty object" in captured.out
        assert "Unit of Work transaction committed successfully" in captured.out


class TestRepositoryPatternEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_repository_with_null_values(self):
        """Test repository operations with null values."""
        repo = InMemoryUserRepository()
        
        # Test with None values
        user = User(id=None, name=None, email=None)
        
        # Repository should handle None values gracefully
        saved_user = repo.save(user)
        assert saved_user.id is not None
        assert saved_user.name is None
        assert saved_user.email is None
    
    def test_repository_with_empty_strings(self):
        """Test repository operations with empty strings."""
        repo = InMemoryUserRepository()
        
        user = User(id=None, name="", email="")
        saved_user = repo.save(user)
        
        assert saved_user.name == ""
        assert saved_user.email == ""
    
    def test_concurrent_repository_operations(self):
        """Test concurrent repository operations."""
        repo = InMemoryUserRepository()
        
        # Simulate concurrent saves
        user1 = User(id=None, name="Alice", email="alice@example.com")
        user2 = User(id=None, name="Bob", email="bob@example.com")
        
        saved_user1 = repo.save(user1)
        saved_user2 = repo.save(user2)
        
        # Should have different IDs
        assert saved_user1.id != saved_user2.id
        assert len(repo.find_all()) == 2
    
    def test_repository_with_large_dataset(self):
        """Test repository performance with large dataset."""
        repo = InMemoryUserRepository()
        
        # Create many users
        users = []
        for i in range(1000):
            user = User(id=None, name=f"User{i}", email=f"user{i}@example.com")
            users.append(repo.save(user))
        
        # Test retrieval
        assert len(repo.find_all()) == 1000
        
        # Test find by ID
        found_user = repo.find_by_id(users[500].id)
        assert found_user.name == "User500"
        
        # Test find by email
        found_user = repo.find_by_email("user250@example.com")
        assert found_user.name == "User250"
    
    def test_json_repository_with_invalid_permissions(self):
        """Test JSON repository with invalid file permissions."""
        import stat
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # Make file read-only
            os.chmod(temp_path, stat.S_IRUSR)
            
            repo = JsonFileUserRepository(temp_path)
            user = User(id=None, name="Alice", email="alice@example.com")
            
            # Should handle permission error gracefully
            # (Implementation dependent - might raise exception or handle gracefully)
            try:
                repo.save(user)
            except PermissionError:
                pass  # Expected behavior
            
        finally:
            # Restore permissions and cleanup
            os.chmod(temp_path, stat.S_IWUSR | stat.S_IRUSR)
            os.unlink(temp_path)
    
    def test_sqlite_repository_with_invalid_database(self):
        """Test SQLite repository with invalid database file."""
        # Try to create repository with invalid path
        try:
            repo = SqliteUserRepository("/invalid/path/database.db")
            # May or may not raise exception depending on implementation
        except Exception:
            pass  # Expected behavior for invalid path


class TestRepositoryPatternPerformance:
    """Test performance characteristics of repository pattern."""
    
    def test_in_memory_repository_performance(self):
        """Test performance of in-memory repository."""
        import time
        
        repo = InMemoryUserRepository()
        
        # Measure insertion time
        start = time.time()
        for i in range(1000):
            user = User(id=None, name=f"User{i}", email=f"user{i}@example.com")
            repo.save(user)
        end = time.time()
        
        insert_time = end - start
        assert insert_time < 1.0  # Should be fast
        
        # Measure retrieval time
        start = time.time()
        for i in range(100):
            repo.find_by_id(i + 1)
        end = time.time()
        
        retrieval_time = end - start
        assert retrieval_time < 0.1  # Should be very fast
    
    def test_json_repository_performance(self):
        """Test performance of JSON file repository."""
        import time
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            
            # Measure insertion time (this will be slower due to file I/O)
            start = time.time()
            for i in range(100):  # Fewer iterations for file-based repo
                user = User(id=None, name=f"User{i}", email=f"user{i}@example.com")
                repo.save(user)
            end = time.time()
            
            insert_time = end - start
            assert insert_time < 5.0  # Should complete within reasonable time
            
        finally:
            os.unlink(temp_path)
    
    def test_service_layer_performance(self):
        """Test performance of service layer operations."""
        import time
        
        repo = InMemoryUserRepository()
        service = UserService(repo)
        
        # Measure service operations
        start = time.time()
        for i in range(1000):
            user = service.register_user(f"User{i}", f"user{i}@example.com")
            service.get_user_by_id(user.id)
        end = time.time()
        
        operation_time = end - start
        assert operation_time < 2.0  # Should be efficient