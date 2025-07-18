"""Repository pattern implementations.

This module provides implementations of the Repository pattern, demonstrating
how to encapsulate data access logic and provide a uniform interface for
accessing data from various sources.
"""

import json
import os
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol


@dataclass
class User:
    """User domain model."""

    id: Optional[int]
    name: str
    email: str
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Product:
    """Product domain model."""

    id: Optional[int]
    name: str
    price: float
    category: str
    in_stock: bool = True

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Order:
    """Order domain model."""

    id: Optional[int]
    user_id: int
    products: List[int]  # Product IDs
    total_amount: float
    status: str = "pending"
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


# Repository Interfaces


class Repository(ABC):
    """Generic repository interface."""

    @abstractmethod
    def save(self, entity: Any) -> Any:
        """Save an entity.

        Args:
            entity: Entity to save

        Returns:
            Saved entity with ID assigned
        """
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Optional[Any]:
        """Find entity by ID.

        Args:
            entity_id: ID of entity to find

        Returns:
            Entity if found, None otherwise
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Any]:
        """Find all entities.

        Returns:
            List of all entities
        """
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete entity by ID.

        Args:
            entity_id: ID of entity to delete

        Returns:
            True if deleted, False if not found
        """
        pass


class UserRepository(Repository):
    """Repository interface for User entities."""

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email.

        Args:
            email: Email address to search for

        Returns:
            User if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> List[User]:
        """Find users by name.

        Args:
            name: Name to search for

        Returns:
            List of users with matching name
        """
        pass


class ProductRepository(Repository):
    """Repository interface for Product entities."""

    @abstractmethod
    def find_by_category(self, category: str) -> List[Product]:
        """Find products by category.

        Args:
            category: Category to search for

        Returns:
            List of products in the category
        """
        pass

    @abstractmethod
    def find_in_stock(self) -> List[Product]:
        """Find products that are in stock.

        Returns:
            List of products in stock
        """
        pass

    @abstractmethod
    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Find products within a price range.

        Args:
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of products within the price range
        """
        pass


class OrderRepository(Repository):
    """Repository interface for Order entities."""

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Order]:
        """Find orders by user ID.

        Args:
            user_id: User ID to search for

        Returns:
            List of orders for the user
        """
        pass

    @abstractmethod
    def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status.

        Args:
            status: Status to search for

        Returns:
            List of orders with the status
        """
        pass


# In-Memory Repository Implementations


class InMemoryUserRepository(UserRepository):
    """In-memory implementation of UserRepository."""

    def __init__(self):
        """Initialize the repository."""
        self._users: Dict[int, User] = {}
        self._next_id = 1

    def save(self, user: User) -> User:
        """Save a user.

        Args:
            user: User to save

        Returns:
            Saved user with ID assigned
        """
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1

        # Check for duplicate email
        existing_user = self.find_by_email(user.email)
        if existing_user and existing_user.id != user.id:
            raise ValueError(f"User with email {user.email} already exists")

        self._users[user.id] = user
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID.

        Args:
            user_id: User ID to find

        Returns:
            User if found, None otherwise
        """
        return self._users.get(user_id)

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email.

        Args:
            email: Email to search for

        Returns:
            User if found, None otherwise
        """
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def find_by_name(self, name: str) -> List[User]:
        """Find users by name.

        Args:
            name: Name to search for

        Returns:
            List of users with matching name
        """
        return [user for user in self._users.values() if user.name == name]

    def find_all(self) -> List[User]:
        """Find all users.

        Returns:
            List of all users
        """
        return list(self._users.values())

    def delete(self, user_id: int) -> bool:
        """Delete user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of ProductRepository."""

    def __init__(self):
        """Initialize the repository."""
        self._products: Dict[int, Product] = {}
        self._next_id = 1

    def save(self, product: Product) -> Product:
        """Save a product.

        Args:
            product: Product to save

        Returns:
            Saved product with ID assigned
        """
        if product.id is None:
            product.id = self._next_id
            self._next_id += 1

        self._products[product.id] = product
        return product

    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Find product by ID.

        Args:
            product_id: Product ID to find

        Returns:
            Product if found, None otherwise
        """
        return self._products.get(product_id)

    def find_by_category(self, category: str) -> List[Product]:
        """Find products by category.

        Args:
            category: Category to search for

        Returns:
            List of products in the category
        """
        return [
            product
            for product in self._products.values()
            if product.category.lower() == category.lower()
        ]

    def find_in_stock(self) -> List[Product]:
        """Find products that are in stock.

        Returns:
            List of products in stock
        """
        return [product for product in self._products.values() if product.in_stock]

    def find_out_of_stock(self) -> List[Product]:
        """Find products that are out of stock.

        Returns:
            List of products out of stock
        """
        return [product for product in self._products.values() if not product.in_stock]

    def find_by_price_range(self, min_price: float, max_price: float) -> List[Product]:
        """Find products within a price range.

        Args:
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of products within the price range
        """
        return [
            product
            for product in self._products.values()
            if min_price <= product.price <= max_price
        ]

    def find_all(self) -> List[Product]:
        """Find all products.

        Returns:
            List of all products
        """
        return list(self._products.values())

    def delete(self, product_id: int) -> bool:
        """Delete product by ID.

        Args:
            product_id: Product ID to delete

        Returns:
            True if deleted, False if not found
        """
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False


class InMemoryOrderRepository(OrderRepository):
    """In-memory implementation of OrderRepository."""

    def __init__(self):
        """Initialize the repository."""
        self._orders: Dict[int, Order] = {}
        self._next_id = 1

    def save(self, order: Order) -> Order:
        """Save an order.

        Args:
            order: Order to save

        Returns:
            Saved order with ID assigned
        """
        if order.id is None:
            order.id = self._next_id
            self._next_id += 1

        self._orders[order.id] = order
        return order

    def find_by_id(self, order_id: int) -> Optional[Order]:
        """Find order by ID.

        Args:
            order_id: Order ID to find

        Returns:
            Order if found, None otherwise
        """
        return self._orders.get(order_id)

    def find_by_user_id(self, user_id: int) -> List[Order]:
        """Find orders by user ID.

        Args:
            user_id: User ID to search for

        Returns:
            List of orders for the user
        """
        return [order for order in self._orders.values() if order.user_id == user_id]

    def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status.

        Args:
            status: Status to search for

        Returns:
            List of orders with the status
        """
        return [
            order
            for order in self._orders.values()
            if order.status.lower() == status.lower()
        ]

    def find_all(self) -> List[Order]:
        """Find all orders.

        Returns:
            List of all orders
        """
        return list(self._orders.values())

    def delete(self, order_id: int) -> bool:
        """Delete order by ID.

        Args:
            order_id: Order ID to delete

        Returns:
            True if deleted, False if not found
        """
        if order_id in self._orders:
            del self._orders[order_id]
            return True
        return False


# JSON File Repository Implementations


class JsonFileUserRepository(UserRepository):
    """JSON file implementation of UserRepository."""

    def __init__(self, file_path: str):
        """Initialize the repository.

        Args:
            file_path: Path to the JSON file
        """
        self.file_path = file_path
        self._ensure_file_exists()
        # Load initial data to populate attributes expected by tests
        data = self._load_data()
        self._users = {user["id"]: self._user_from_dict(user) for user in data["users"]}
        self._next_id = data["next_id"]

    def _ensure_file_exists(self):
        """Ensure the JSON file exists."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({"users": [], "next_id": 1}, f)
        else:
            # Check if file is empty and initialize if needed
            try:
                with open(self.file_path, "r") as f:
                    content = f.read().strip()
                    if not content:
                        with open(self.file_path, "w") as f:
                            json.dump({"users": [], "next_id": 1}, f)
            except (json.JSONDecodeError, IOError):
                # File is corrupted or empty, reinitialize
                with open(self.file_path, "w") as f:
                    json.dump({"users": [], "next_id": 1}, f)

    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file.

        Returns:
            Data dictionary
        """
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save_data(self, data: Dict[str, Any]):
        """Save data to JSON file.

        Args:
            data: Data to save
        """
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def _user_from_dict(self, user_dict: Dict[str, Any]) -> User:
        """Create User from dictionary.

        Args:
            user_dict: User data dictionary

        Returns:
            User instance
        """
        created_at = None
        if user_dict.get("created_at"):
            created_at = datetime.fromisoformat(user_dict["created_at"])

        return User(
            id=user_dict["id"],
            name=user_dict["name"],
            email=user_dict["email"],
            created_at=created_at,
        )

    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert User to dictionary.

        Args:
            user: User instance

        Returns:
            User data dictionary
        """
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }

    def save(self, user: User) -> User:
        """Save a user.

        Args:
            user: User to save

        Returns:
            Saved user with ID assigned
        """
        data = self._load_data()

        if user.id is None:
            user.id = data["next_id"]
            data["next_id"] += 1
            self._next_id = data["next_id"]
            data["users"].append(self._user_to_dict(user))
        else:
            # Update existing user
            for i, u in enumerate(data["users"]):
                if u["id"] == user.id:
                    data["users"][i] = self._user_to_dict(user)
                    break

        self._save_data(data)
        # Update in-memory attributes
        self._users[user.id] = user
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID.

        Args:
            user_id: User ID to find

        Returns:
            User if found, None otherwise
        """
        data = self._load_data()
        for user_dict in data["users"]:
            if user_dict["id"] == user_id:
                return self._user_from_dict(user_dict)
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email.

        Args:
            email: Email to search for

        Returns:
            User if found, None otherwise
        """
        data = self._load_data()
        for user_dict in data["users"]:
            if user_dict["email"] == email:
                return self._user_from_dict(user_dict)
        return None

    def find_by_name(self, name: str) -> List[User]:
        """Find users by name.

        Args:
            name: Name to search for

        Returns:
            List of users with matching name
        """
        data = self._load_data()
        return [
            self._user_from_dict(user_dict)
            for user_dict in data["users"]
            if user_dict["name"] == name
        ]

    def find_all(self) -> List[User]:
        """Find all users.

        Returns:
            List of all users
        """
        data = self._load_data()
        return [self._user_from_dict(user_dict) for user_dict in data["users"]]

    def delete(self, user_id: int) -> bool:
        """Delete user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        data = self._load_data()
        for i, user_dict in enumerate(data["users"]):
            if user_dict["id"] == user_id:
                del data["users"][i]
                self._save_data(data)
                # Update in-memory attributes
                if user_id in self._users:
                    del self._users[user_id]
                return True
        return False


# SQLite Repository Implementation


class SqliteUserRepository(UserRepository):
    """SQLite implementation of UserRepository."""

    def __init__(self, db_path: str):
        """Initialize the repository.

        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        conn.close()

    def _user_from_row(self, row: tuple) -> User:
        """Create User from database row.

        Args:
            row: Database row tuple

        Returns:
            User instance
        """
        created_at = None
        if row[3]:
            created_at = datetime.fromisoformat(row[3])

        return User(id=row[0], name=row[1], email=row[2], created_at=created_at)

    def save(self, user: User) -> User:
        """Save a user.

        Args:
            user: User to save

        Returns:
            Saved user with ID assigned
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if user.id is None:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
                (
                    user.name,
                    user.email,
                    user.created_at.isoformat() if user.created_at else None,
                ),
            )
            user.id = cursor.lastrowid
        else:
            # Update existing user
            cursor.execute(
                "UPDATE users SET name = ?, email = ?, created_at = ? WHERE id = ?",
                (
                    user.name,
                    user.email,
                    user.created_at.isoformat() if user.created_at else None,
                    user.id,
                ),
            )

        conn.commit()
        conn.close()
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID.

        Args:
            user_id: User ID to find

        Returns:
            User if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._user_from_row(row)
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email.

        Args:
            email: Email to search for

        Returns:
            User if found, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._user_from_row(row)
        return None

    def find_by_name(self, name: str) -> List[User]:
        """Find users by name.

        Args:
            name: Name to search for

        Returns:
            List of users with matching name
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        rows = cursor.fetchall()
        conn.close()

        return [self._user_from_row(row) for row in rows]

    def find_all(self) -> List[User]:
        """Find all users.

        Returns:
            List of all users
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()

        return [self._user_from_row(row) for row in rows]

    def delete(self, user_id: int) -> bool:
        """Delete user by ID.

        Args:
            user_id: User ID to delete

        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted


# Service Layer


class UserService:
    """Service layer for user operations."""

    def __init__(self, user_repository: UserRepository):
        """Initialize the service.

        Args:
            user_repository: Repository for user data access
        """
        self.user_repository = user_repository

    def register_user(self, name: str, email: str) -> Optional[User]:
        """Register a new user.

        Args:
            name: User's name
            email: User's email address

        Returns:
            Created user, or None if validation fails

        Raises:
            ValueError: If validation fails
        """
        # Business logic validation
        if not name.strip():
            raise ValueError("Name cannot be empty")

        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")

        # Check if email already exists
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            return None  # Return None instead of raising exception for duplicate email

        # Create and save user
        user = User(None, name.strip(), email.lower())
        return self.user_repository.save(user)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: Email address

        Returns:
            User if found, None otherwise
        """
        return self.user_repository.find_by_email(email.lower())

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User if found, None otherwise
        """
        return self.user_repository.find_by_id(user_id)

    def update_user(
        self, user_id: int, name: str = None, email: str = None
    ) -> Optional[User]:
        """Update user information.

        Args:
            user_id: User ID
            name: New name (optional)
            email: New email (optional)

        Returns:
            Updated user if found, None otherwise

        Raises:
            ValueError: If validation fails
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            user.name = name.strip()

        if email is not None:
            if "@" not in email or "." not in email:
                raise ValueError("Invalid email format")

            # Check if email already exists for another user
            existing_user = self.user_repository.find_by_email(email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already exists")

            user.email = email.lower()

        return self.user_repository.save(user)

    def delete_user(self, user_id: int) -> bool:
        """Delete user.

        Args:
            user_id: User ID

        Returns:
            True if deleted, False if not found
        """
        return self.user_repository.delete(user_id)

    def get_all_users(self) -> List[User]:
        """Get all users.

        Returns:
            List of all users
        """
        return self.user_repository.find_all()

    def search_users_by_name(self, name: str) -> List[User]:
        """Search users by name.

        Args:
            name: Name to search for

        Returns:
            List of users with matching name
        """
        return self.user_repository.find_by_name(name)


class ProductService:
    """Service layer for product operations."""

    def __init__(self, product_repository: ProductRepository):
        """Initialize the service.

        Args:
            product_repository: Repository for product data access
        """
        self.product_repository = product_repository

    def add_product(
        self, name: str, price: float, category: str, in_stock: bool = True
    ) -> Optional[Product]:
        """Add a new product.

        Args:
            name: Product name
            price: Product price
            category: Product category
            in_stock: Whether product is in stock

        Returns:
            Created product, or None if validation fails

        Raises:
            ValueError: If validation fails
        """
        if not name.strip():
            raise ValueError("Product name cannot be empty")

        if price < 0:
            return None  # Return None instead of raising exception for negative price

        if not category.strip():
            raise ValueError("Category cannot be empty")

        product = Product(None, name.strip(), price, category.strip(), in_stock)
        return self.product_repository.save(product)

    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product by ID.

        Args:
            product_id: Product ID

        Returns:
            Product if found, None otherwise
        """
        return self.product_repository.find_by_id(product_id)

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category.

        Args:
            category: Category name

        Returns:
            List of products in the category
        """
        return self.product_repository.find_by_category(category)

    def get_products_in_stock(self) -> List[Product]:
        """Get products that are in stock.

        Returns:
            List of products in stock
        """
        return self.product_repository.find_in_stock()

    def get_products_by_price_range(
        self, min_price: float, max_price: float
    ) -> List[Product]:
        """Get products within a price range.

        Args:
            min_price: Minimum price
            max_price: Maximum price

        Returns:
            List of products within the price range
        """
        return self.product_repository.find_by_price_range(min_price, max_price)

    def update_stock_status(self, product_id: int, in_stock: bool) -> Optional[Product]:
        """Update product stock status.

        Args:
            product_id: Product ID
            in_stock: New stock status

        Returns:
            Updated product if found, None otherwise
        """
        product = self.product_repository.find_by_id(product_id)
        if not product:
            return None

        product.in_stock = in_stock
        return self.product_repository.save(product)


# Unit of Work Pattern


class UnitOfWork:
    """Unit of Work pattern implementation."""

    def __init__(self):
        """Initialize the Unit of Work."""
        self._new_objects: List[Any] = []
        self._dirty_objects: List[Any] = []
        self._removed_objects: List[Any] = []

    def register_new(self, obj: Any) -> None:
        """Register a new object.

        Args:
            obj: Object to register as new
        """
        self._new_objects.append(obj)

    def register_dirty(self, obj: Any) -> None:
        """Register a dirty object.

        Args:
            obj: Object to register as dirty
        """
        if obj not in self._dirty_objects:
            self._dirty_objects.append(obj)

    def register_removed(self, obj: Any) -> None:
        """Register a removed object.

        Args:
            obj: Object to register as removed
        """
        self._removed_objects.append(obj)

    def commit(self) -> None:
        """Commit all changes."""
        try:
            # In a real implementation, you would start a database transaction here
            print("Starting Unit of Work transaction...")

            # Process new objects
            for obj in self._new_objects:
                print(f"Inserting new object: {obj}")

            # Process dirty objects
            for obj in self._dirty_objects:
                print(f"Updating dirty object: {obj}")

            # Process removed objects
            for obj in self._removed_objects:
                print(f"Deleting removed object: {obj}")

            print("Unit of Work transaction committed successfully")
            self._clear()

        except Exception as e:
            print(f"Unit of Work transaction failed: {e}")
            print("Rolling back changes...")
            self._clear()
            raise

    def _clear(self) -> None:
        """Clear all tracked objects."""
        self._new_objects.clear()
        self._dirty_objects.clear()
        self._removed_objects.clear()


# Example usage functions


def demonstrate_basic_repository():
    """Demonstrate basic repository usage."""
    print("=== Basic Repository Demo ===")

    # Create repository and service
    user_repo = InMemoryUserRepository()
    user_service = UserService(user_repo)

    # Register users
    user1 = user_service.register_user("Alice Johnson", "alice@example.com")
    user2 = user_service.register_user("Bob Smith", "bob@example.com")

    print(f"Registered: {user1}")
    print(f"Registered: {user2}")

    # Find users
    found_user = user_service.get_user_by_email("alice@example.com")
    print(f"Found by email: {found_user}")

    # Update user
    updated_user = user_service.update_user(user1.id, name="Alice Johnson-Smith")
    print(f"Updated: {updated_user}")

    # List all users
    all_users = user_service.get_all_users()
    print(f"All users: {len(all_users)}")
    for user in all_users:
        print(f"  {user}")


def demonstrate_multiple_implementations():
    """Demonstrate multiple repository implementations."""
    print("\n=== Multiple Repository Implementations Demo ===")

    # Test in-memory repository
    print("--- In-Memory Repository ---")
    memory_repo = InMemoryUserRepository()
    memory_service = UserService(memory_repo)

    user = memory_service.register_user("Memory User", "memory@example.com")
    print(f"Created in memory: {user}")

    # Test JSON file repository
    print("--- JSON File Repository ---")
    json_repo = JsonFileUserRepository("/tmp/test_users.json")
    json_service = UserService(json_repo)

    user = json_service.register_user("JSON User", "json@example.com")
    print(f"Created in JSON: {user}")

    # Test SQLite repository
    print("--- SQLite Repository ---")
    sqlite_repo = SqliteUserRepository(":memory:")
    sqlite_service = UserService(sqlite_repo)

    user = sqlite_service.register_user("SQLite User", "sqlite@example.com")
    print(f"Created in SQLite: {user}")


def demonstrate_product_service():
    """Demonstrate product service with repository."""
    print("\n=== Product Service Demo ===")

    # Create product repository and service
    product_repo = InMemoryProductRepository()
    product_service = ProductService(product_repo)

    # Add products
    laptop = product_service.add_product("Laptop", 999.99, "Electronics")
    mouse = product_service.add_product("Mouse", 25.99, "Electronics")
    book = product_service.add_product("Python Book", 49.99, "Books")

    print(f"Added products: {len(product_service.product_repository.find_all())}")

    # Find products by category
    electronics = product_service.get_products_by_category("Electronics")
    print(f"Electronics products: {len(electronics)}")

    # Find products by price range
    affordable = product_service.get_products_by_price_range(0, 50)
    print(f"Affordable products (≤$50): {len(affordable)}")

    # Update stock status
    product_service.update_stock_status(laptop.id, False)
    in_stock = product_service.get_products_in_stock()
    print(f"Products in stock: {len(in_stock)}")


def demonstrate_unit_of_work():
    """Demonstrate Unit of Work pattern."""
    print("\n=== Unit of Work Demo ===")

    uow = UnitOfWork()

    # Register operations
    user1 = User(1, "Alice", "alice@example.com")
    user2 = User(2, "Bob", "bob@example.com")
    user3 = User(3, "Charlie", "charlie@example.com")

    uow.register_new(user1)
    uow.register_dirty(user2)
    uow.register_removed(user3)

    # Commit all changes
    uow.commit()


if __name__ == "__main__":
    demonstrate_basic_repository()
    demonstrate_multiple_implementations()
    demonstrate_product_service()
    demonstrate_unit_of_work()
