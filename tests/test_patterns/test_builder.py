"""Tests for builder pattern implementations."""

import pytest
from unittest.mock import Mock, patch

from src.patterns.builder import (
    # Product Classes
    Computer,
    House,
    Pizza,
    
    # Builder Classes
    Builder,
    ComputerBuilder,
    HouseBuilder,
    PizzaBuilder,
    SQLQueryBuilder,
    
    # Director Classes
    ComputerDirector,
    HouseDirector,
    PizzaDirector,
)


class TestProductClasses:
    """Test product classes (Computer, House, Pizza)."""
    
    def test_computer_creation(self):
        """Test creating a computer."""
        computer = Computer(
            cpu="Intel i7",
            memory="16GB",
            storage="512GB SSD",
            graphics_card="NVIDIA GTX 1080",
            operating_system="Windows 11"
        )
        
        assert computer.cpu == "Intel i7"
        assert computer.memory == "16GB"
        assert computer.storage == "512GB SSD"
        assert computer.graphics_card == "NVIDIA GTX 1080"
        assert computer.operating_system == "Windows 11"
        assert computer.bluetooth is False
        assert computer.wifi is False
        assert computer.case_color == "black"
    
    def test_computer_default_values(self):
        """Test computer with default values."""
        computer = Computer()
        
        assert computer.cpu == ""
        assert computer.memory == ""
        assert computer.storage == ""
        assert computer.graphics_card is None
        assert computer.sound_card is None
        assert computer.network_card is None
        assert computer.bluetooth is False
        assert computer.wifi is False
        assert computer.case_color == "black"
        assert computer.operating_system is None
        assert computer.monitor is None
        assert computer.keyboard is None
        assert computer.mouse is None
    
    def test_computer_string_representation(self):
        """Test computer string representation."""
        computer = Computer(
            cpu="Intel i7",
            memory="16GB",
            storage="512GB SSD",
            graphics_card="NVIDIA GTX 1080",
            operating_system="Windows 11"
        )
        
        str_repr = str(computer)
        assert "Computer: Intel i7, 16GB, 512GB SSD" in str_repr
        assert "NVIDIA GTX 1080" in str_repr
        assert "Windows 11" in str_repr
    
    def test_computer_string_minimal(self):
        """Test computer string representation with minimal specs."""
        computer = Computer(cpu="Intel i5", memory="8GB", storage="256GB SSD")
        
        str_repr = str(computer)
        assert str_repr == "Computer: Intel i5, 8GB, 256GB SSD"
    
    def test_house_creation(self):
        """Test creating a house."""
        house = House(
            foundation="Concrete",
            walls="Brick",
            roof="Tile",
            windows=10,
            doors=3,
            garage=True,
            garden=True,
            pool=False,
            floors=2
        )
        
        assert house.foundation == "Concrete"
        assert house.walls == "Brick"
        assert house.roof == "Tile"
        assert house.windows == 10
        assert house.doors == 3
        assert house.garage is True
        assert house.garden is True
        assert house.pool is False
        assert house.floors == 2
        assert house.rooms == []
    
    def test_house_default_values(self):
        """Test house with default values."""
        house = House()
        
        assert house.foundation == ""
        assert house.walls == ""
        assert house.roof == ""
        assert house.windows == 0
        assert house.doors == 0
        assert house.garage is False
        assert house.garden is False
        assert house.pool is False
        assert house.floors == 1
        assert house.rooms == []
    
    def test_house_with_rooms(self):
        """Test house with rooms."""
        house = House(rooms=["Living Room", "Kitchen", "Bedroom"])
        
        assert len(house.rooms) == 3
        assert "Living Room" in house.rooms
        assert "Kitchen" in house.rooms
        assert "Bedroom" in house.rooms
    
    def test_house_string_representation(self):
        """Test house string representation."""
        house = House(
            foundation="Concrete",
            walls="Brick",
            roof="Tile",
            floors=2,
            rooms=["Living Room", "Kitchen", "Bedroom"]
        )
        
        str_repr = str(house)
        expected = "House: Concrete foundation, Brick walls, Tile roof, 2 floor(s), 3 rooms"
        assert str_repr == expected
    
    def test_pizza_creation(self):
        """Test creating a pizza."""
        pizza = Pizza(
            size="large",
            crust="thin",
            sauce="tomato",
            cheese="mozzarella",
            toppings=["pepperoni", "mushrooms"],
            extra_cheese=True,
            gluten_free=False,
            spicy=True
        )
        
        assert pizza.size == "large"
        assert pizza.crust == "thin"
        assert pizza.sauce == "tomato"
        assert pizza.cheese == "mozzarella"
        assert pizza.toppings == ["pepperoni", "mushrooms"]
        assert pizza.extra_cheese is True
        assert pizza.gluten_free is False
        assert pizza.spicy is True
    
    def test_pizza_default_values(self):
        """Test pizza with default values."""
        pizza = Pizza()
        
        assert pizza.size == "medium"
        assert pizza.crust == "regular"
        assert pizza.sauce == "tomato"
        assert pizza.cheese == "mozzarella"
        assert pizza.toppings == []
        assert pizza.extra_cheese is False
        assert pizza.gluten_free is False
        assert pizza.spicy is False
    
    def test_pizza_string_representation(self):
        """Test pizza string representation."""
        pizza = Pizza(
            size="large",
            crust="thin",
            sauce="tomato",
            cheese="mozzarella",
            toppings=["pepperoni", "mushrooms"],
            extra_cheese=True,
            gluten_free=True,
            spicy=True
        )
        
        str_repr = str(pizza)
        assert "Large thin crust pizza" in str_repr
        assert "tomato sauce" in str_repr
        assert "mozzarella" in str_repr
        assert "pepperoni, mushrooms" in str_repr
        assert "extra cheese" in str_repr
        assert "(gluten-free)" in str_repr
        assert "(spicy)" in str_repr
    
    def test_pizza_string_minimal(self):
        """Test pizza string representation with minimal options."""
        pizza = Pizza(size="medium", crust="regular", sauce="tomato", cheese="mozzarella")
        
        str_repr = str(pizza)
        expected = "Medium regular crust pizza with tomato sauce and mozzarella"
        assert str_repr == expected


class TestComputerBuilder:
    """Test computer builder implementation."""
    
    def test_builder_creation(self):
        """Test creating computer builder."""
        builder = ComputerBuilder()
        
        assert builder._computer is not None
        assert isinstance(builder._computer, Computer)
    
    def test_builder_reset(self):
        """Test resetting builder."""
        builder = ComputerBuilder()
        
        # Build something
        builder.set_cpu("Intel i7").set_memory("16GB")
        
        # Reset
        result = builder.reset()
        
        assert result is builder  # Should return self
        assert builder._computer.cpu == ""
        assert builder._computer.memory == ""
    
    def test_set_cpu(self):
        """Test setting CPU."""
        builder = ComputerBuilder()
        
        result = builder.set_cpu("Intel i9")
        
        assert result is builder  # Should return self for chaining
        assert builder._computer.cpu == "Intel i9"
    
    def test_set_memory(self):
        """Test setting memory."""
        builder = ComputerBuilder()
        
        result = builder.set_memory("32GB DDR5")
        
        assert result is builder
        assert builder._computer.memory == "32GB DDR5"
    
    def test_set_storage(self):
        """Test setting storage."""
        builder = ComputerBuilder()
        
        result = builder.set_storage("1TB NVMe SSD")
        
        assert result is builder
        assert builder._computer.storage == "1TB NVMe SSD"
    
    def test_set_graphics_card(self):
        """Test setting graphics card."""
        builder = ComputerBuilder()
        
        result = builder.set_graphics_card("NVIDIA RTX 4080")
        
        assert result is builder
        assert builder._computer.graphics_card == "NVIDIA RTX 4080"
    
    def test_set_sound_card(self):
        """Test setting sound card."""
        builder = ComputerBuilder()
        
        result = builder.set_sound_card("Creative Sound Blaster")
        
        assert result is builder
        assert builder._computer.sound_card == "Creative Sound Blaster"
    
    def test_set_network_card(self):
        """Test setting network card."""
        builder = ComputerBuilder()
        
        result = builder.set_network_card("Killer Ethernet")
        
        assert result is builder
        assert builder._computer.network_card == "Killer Ethernet"
    
    def test_enable_bluetooth(self):
        """Test enabling Bluetooth."""
        builder = ComputerBuilder()
        
        result = builder.enable_bluetooth()
        
        assert result is builder
        assert builder._computer.bluetooth is True
    
    def test_enable_wifi(self):
        """Test enabling WiFi."""
        builder = ComputerBuilder()
        
        result = builder.enable_wifi()
        
        assert result is builder
        assert builder._computer.wifi is True
    
    def test_set_case_color(self):
        """Test setting case color."""
        builder = ComputerBuilder()
        
        result = builder.set_case_color("RGB")
        
        assert result is builder
        assert builder._computer.case_color == "RGB"
    
    def test_set_operating_system(self):
        """Test setting operating system."""
        builder = ComputerBuilder()
        
        result = builder.set_operating_system("Windows 11 Pro")
        
        assert result is builder
        assert builder._computer.operating_system == "Windows 11 Pro"
    
    def test_set_monitor(self):
        """Test setting monitor."""
        builder = ComputerBuilder()
        
        result = builder.set_monitor("4K Gaming Monitor")
        
        assert result is builder
        assert builder._computer.monitor == "4K Gaming Monitor"
    
    def test_set_keyboard(self):
        """Test setting keyboard."""
        builder = ComputerBuilder()
        
        result = builder.set_keyboard("Mechanical RGB")
        
        assert result is builder
        assert builder._computer.keyboard == "Mechanical RGB"
    
    def test_set_mouse(self):
        """Test setting mouse."""
        builder = ComputerBuilder()
        
        result = builder.set_mouse("High-DPI Gaming")
        
        assert result is builder
        assert builder._computer.mouse == "High-DPI Gaming"
    
    def test_build(self):
        """Test building computer."""
        builder = ComputerBuilder()
        
        computer = (builder
                   .set_cpu("Intel i7")
                   .set_memory("16GB")
                   .set_storage("512GB SSD")
                   .enable_wifi()
                   .set_case_color("Black")
                   .build())
        
        assert isinstance(computer, Computer)
        assert computer.cpu == "Intel i7"
        assert computer.memory == "16GB"
        assert computer.storage == "512GB SSD"
        assert computer.wifi is True
        assert computer.case_color == "Black"
    
    def test_method_chaining(self):
        """Test method chaining."""
        builder = ComputerBuilder()
        
        # Should be able to chain all methods
        computer = (builder
                   .set_cpu("Intel i9")
                   .set_memory("32GB")
                   .set_storage("1TB SSD")
                   .set_graphics_card("RTX 4080")
                   .set_sound_card("Creative")
                   .set_network_card("Killer")
                   .enable_bluetooth()
                   .enable_wifi()
                   .set_case_color("RGB")
                   .set_operating_system("Windows 11")
                   .set_monitor("4K")
                   .set_keyboard("Mechanical")
                   .set_mouse("Gaming")
                   .build())
        
        assert computer.cpu == "Intel i9"
        assert computer.memory == "32GB"
        assert computer.storage == "1TB SSD"
        assert computer.graphics_card == "RTX 4080"
        assert computer.sound_card == "Creative"
        assert computer.network_card == "Killer"
        assert computer.bluetooth is True
        assert computer.wifi is True
        assert computer.case_color == "RGB"
        assert computer.operating_system == "Windows 11"
        assert computer.monitor == "4K"
        assert computer.keyboard == "Mechanical"
        assert computer.mouse == "Gaming"
    
    def test_multiple_builds(self):
        """Test building multiple computers with same builder."""
        builder = ComputerBuilder()
        
        # Build first computer
        computer1 = (builder
                    .set_cpu("Intel i5")
                    .set_memory("8GB")
                    .build())
        
        # Build second computer (should be different)
        computer2 = (builder.reset()
                    .set_cpu("Intel i7")
                    .set_memory("16GB")
                    .build())
        
        assert computer1.cpu == "Intel i5"
        assert computer1.memory == "8GB"
        assert computer2.cpu == "Intel i7"
        assert computer2.memory == "16GB"
        assert computer1 is not computer2


class TestHouseBuilder:
    """Test house builder implementation."""
    
    def test_builder_creation(self):
        """Test creating house builder."""
        builder = HouseBuilder()
        
        assert builder._house is not None
        assert isinstance(builder._house, House)
    
    def test_builder_reset(self):
        """Test resetting builder."""
        builder = HouseBuilder()
        
        # Build something
        builder.set_foundation("Concrete").set_walls("Brick")
        
        # Reset
        result = builder.reset()
        
        assert result is builder
        assert builder._house.foundation == ""
        assert builder._house.walls == ""
    
    def test_set_foundation(self):
        """Test setting foundation."""
        builder = HouseBuilder()
        
        result = builder.set_foundation("Concrete Slab")
        
        assert result is builder
        assert builder._house.foundation == "Concrete Slab"
    
    def test_set_walls(self):
        """Test setting walls."""
        builder = HouseBuilder()
        
        result = builder.set_walls("Brick")
        
        assert result is builder
        assert builder._house.walls == "Brick"
    
    def test_set_roof(self):
        """Test setting roof."""
        builder = HouseBuilder()
        
        result = builder.set_roof("Tile")
        
        assert result is builder
        assert builder._house.roof == "Tile"
    
    def test_set_windows(self):
        """Test setting windows."""
        builder = HouseBuilder()
        
        result = builder.set_windows(10)
        
        assert result is builder
        assert builder._house.windows == 10
    
    def test_set_doors(self):
        """Test setting doors."""
        builder = HouseBuilder()
        
        result = builder.set_doors(3)
        
        assert result is builder
        assert builder._house.doors == 3
    
    def test_add_garage(self):
        """Test adding garage."""
        builder = HouseBuilder()
        
        result = builder.add_garage()
        
        assert result is builder
        assert builder._house.garage is True
    
    def test_add_garden(self):
        """Test adding garden."""
        builder = HouseBuilder()
        
        result = builder.add_garden()
        
        assert result is builder
        assert builder._house.garden is True
    
    def test_add_pool(self):
        """Test adding pool."""
        builder = HouseBuilder()
        
        result = builder.add_pool()
        
        assert result is builder
        assert builder._house.pool is True
    
    def test_set_floors(self):
        """Test setting floors."""
        builder = HouseBuilder()
        
        result = builder.set_floors(2)
        
        assert result is builder
        assert builder._house.floors == 2
    
    def test_add_room(self):
        """Test adding room."""
        builder = HouseBuilder()
        
        result = builder.add_room("Living Room")
        
        assert result is builder
        assert "Living Room" in builder._house.rooms
    
    def test_add_multiple_rooms(self):
        """Test adding multiple rooms."""
        builder = HouseBuilder()
        
        house = (builder
                .add_room("Living Room")
                .add_room("Kitchen")
                .add_room("Bedroom")
                .build())
        
        assert len(house.rooms) == 3
        assert "Living Room" in house.rooms
        assert "Kitchen" in house.rooms
        assert "Bedroom" in house.rooms
    
    def test_build(self):
        """Test building house."""
        builder = HouseBuilder()
        
        house = (builder
                .set_foundation("Concrete")
                .set_walls("Brick")
                .set_roof("Tile")
                .set_windows(12)
                .set_doors(4)
                .add_garage()
                .add_garden()
                .set_floors(2)
                .add_room("Living Room")
                .add_room("Kitchen")
                .build())
        
        assert isinstance(house, House)
        assert house.foundation == "Concrete"
        assert house.walls == "Brick"
        assert house.roof == "Tile"
        assert house.windows == 12
        assert house.doors == 4
        assert house.garage is True
        assert house.garden is True
        assert house.floors == 2
        assert len(house.rooms) == 2


class TestPizzaBuilder:
    """Test pizza builder implementation."""
    
    def test_builder_creation(self):
        """Test creating pizza builder."""
        builder = PizzaBuilder()
        
        assert builder._pizza is not None
        assert isinstance(builder._pizza, Pizza)
    
    def test_builder_reset(self):
        """Test resetting builder."""
        builder = PizzaBuilder()
        
        # Build something
        builder.set_size("large").set_crust("thin")
        
        # Reset
        result = builder.reset()
        
        assert result is builder
        assert builder._pizza.size == "medium"  # Default value
        assert builder._pizza.crust == "regular"  # Default value
    
    def test_set_size(self):
        """Test setting size."""
        builder = PizzaBuilder()
        
        result = builder.set_size("large")
        
        assert result is builder
        assert builder._pizza.size == "large"
    
    def test_set_crust(self):
        """Test setting crust."""
        builder = PizzaBuilder()
        
        result = builder.set_crust("thin")
        
        assert result is builder
        assert builder._pizza.crust == "thin"
    
    def test_set_sauce(self):
        """Test setting sauce."""
        builder = PizzaBuilder()
        
        result = builder.set_sauce("pesto")
        
        assert result is builder
        assert builder._pizza.sauce == "pesto"
    
    def test_set_cheese(self):
        """Test setting cheese."""
        builder = PizzaBuilder()
        
        result = builder.set_cheese("cheddar")
        
        assert result is builder
        assert builder._pizza.cheese == "cheddar"
    
    def test_add_topping(self):
        """Test adding single topping."""
        builder = PizzaBuilder()
        
        result = builder.add_topping("pepperoni")
        
        assert result is builder
        assert "pepperoni" in builder._pizza.toppings
    
    def test_add_multiple_toppings_individually(self):
        """Test adding multiple toppings individually."""
        builder = PizzaBuilder()
        
        pizza = (builder
                .add_topping("pepperoni")
                .add_topping("mushrooms")
                .add_topping("bell peppers")
                .build())
        
        assert len(pizza.toppings) == 3
        assert "pepperoni" in pizza.toppings
        assert "mushrooms" in pizza.toppings
        assert "bell peppers" in pizza.toppings
    
    def test_add_toppings_list(self):
        """Test adding list of toppings."""
        builder = PizzaBuilder()
        
        result = builder.add_toppings(["pepperoni", "sausage", "mushrooms"])
        
        assert result is builder
        assert len(builder._pizza.toppings) == 3
        assert "pepperoni" in builder._pizza.toppings
        assert "sausage" in builder._pizza.toppings
        assert "mushrooms" in builder._pizza.toppings
    
    def test_add_extra_cheese(self):
        """Test adding extra cheese."""
        builder = PizzaBuilder()
        
        result = builder.add_extra_cheese()
        
        assert result is builder
        assert builder._pizza.extra_cheese is True
    
    def test_make_gluten_free(self):
        """Test making gluten-free."""
        builder = PizzaBuilder()
        
        result = builder.make_gluten_free()
        
        assert result is builder
        assert builder._pizza.gluten_free is True
    
    def test_make_spicy(self):
        """Test making spicy."""
        builder = PizzaBuilder()
        
        result = builder.make_spicy()
        
        assert result is builder
        assert builder._pizza.spicy is True
    
    def test_build(self):
        """Test building pizza."""
        builder = PizzaBuilder()
        
        pizza = (builder
                .set_size("large")
                .set_crust("thin")
                .set_sauce("pesto")
                .set_cheese("goat cheese")
                .add_toppings(["spinach", "sun-dried tomatoes"])
                .add_extra_cheese()
                .make_gluten_free()
                .make_spicy()
                .build())
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "large"
        assert pizza.crust == "thin"
        assert pizza.sauce == "pesto"
        assert pizza.cheese == "goat cheese"
        assert len(pizza.toppings) == 2
        assert pizza.extra_cheese is True
        assert pizza.gluten_free is True
        assert pizza.spicy is True


class TestSQLQueryBuilder:
    """Test SQL query builder implementation."""
    
    def test_builder_creation(self):
        """Test creating SQL query builder."""
        builder = SQLQueryBuilder()
        
        assert builder._query_parts is not None
        assert isinstance(builder._query_parts, dict)
    
    def test_builder_reset(self):
        """Test resetting builder."""
        builder = SQLQueryBuilder()
        
        # Build something
        builder.select("name").from_table("users")
        
        # Reset
        result = builder.reset()
        
        assert result is builder
        assert builder._query_parts['select'] == []
        assert builder._query_parts['from'] == ''
    
    def test_select_single_column(self):
        """Test selecting single column."""
        builder = SQLQueryBuilder()
        
        result = builder.select("name")
        
        assert result is builder
        assert "name" in builder._query_parts['select']
    
    def test_select_multiple_columns(self):
        """Test selecting multiple columns."""
        builder = SQLQueryBuilder()
        
        result = builder.select("name", "email", "age")
        
        assert result is builder
        assert len(builder._query_parts['select']) == 3
        assert "name" in builder._query_parts['select']
        assert "email" in builder._query_parts['select']
        assert "age" in builder._query_parts['select']
    
    def test_from_table(self):
        """Test setting FROM table."""
        builder = SQLQueryBuilder()
        
        result = builder.from_table("users")
        
        assert result is builder
        assert builder._query_parts['from'] == "users"
    
    def test_join(self):
        """Test adding JOIN clause."""
        builder = SQLQueryBuilder()
        
        result = builder.join("orders", "users.id = orders.user_id")
        
        assert result is builder
        assert "INNER JOIN orders ON users.id = orders.user_id" in builder._query_parts['joins']
    
    def test_join_with_type(self):
        """Test adding JOIN with specific type."""
        builder = SQLQueryBuilder()
        
        result = builder.join("orders", "users.id = orders.user_id", "LEFT")
        
        assert result is builder
        assert "LEFT JOIN orders ON users.id = orders.user_id" in builder._query_parts['joins']
    
    def test_where_single_condition(self):
        """Test adding WHERE condition."""
        builder = SQLQueryBuilder()
        
        result = builder.where("active = 1")
        
        assert result is builder
        assert "active = 1" in builder._query_parts['where']
    
    def test_where_multiple_conditions(self):
        """Test adding multiple WHERE conditions."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .where("active = 1")
                .where("age > 18")
                .build())
        
        assert "WHERE active = 1 AND age > 18" in query
    
    def test_group_by(self):
        """Test GROUP BY clause."""
        builder = SQLQueryBuilder()
        
        result = builder.group_by("department", "role")
        
        assert result is builder
        assert "department" in builder._query_parts['group_by']
        assert "role" in builder._query_parts['group_by']
    
    def test_having(self):
        """Test HAVING clause."""
        builder = SQLQueryBuilder()
        
        result = builder.having("COUNT(*) > 1")
        
        assert result is builder
        assert "COUNT(*) > 1" in builder._query_parts['having']
    
    def test_order_by_default(self):
        """Test ORDER BY with default direction."""
        builder = SQLQueryBuilder()
        
        result = builder.order_by("name")
        
        assert result is builder
        assert "name ASC" in builder._query_parts['order_by']
    
    def test_order_by_with_direction(self):
        """Test ORDER BY with specific direction."""
        builder = SQLQueryBuilder()
        
        result = builder.order_by("created_at", "DESC")
        
        assert result is builder
        assert "created_at DESC" in builder._query_parts['order_by']
    
    def test_limit(self):
        """Test LIMIT clause."""
        builder = SQLQueryBuilder()
        
        result = builder.limit(10)
        
        assert result is builder
        assert builder._query_parts['limit'] == 10
    
    def test_build_simple_query(self):
        """Test building simple query."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .select("name", "email")
                .from_table("users")
                .where("active = 1")
                .build())
        
        expected = "SELECT name, email FROM users WHERE active = 1"
        assert query == expected
    
    def test_build_select_all(self):
        """Test building query with SELECT *."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .from_table("users")
                .build())
        
        expected = "SELECT * FROM users"
        assert query == expected
    
    def test_build_complex_query(self):
        """Test building complex query."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .select("u.name", "u.email", "COUNT(o.id) as order_count")
                .from_table("users u")
                .join("orders o", "u.id = o.user_id", "LEFT")
                .where("u.active = 1")
                .where("u.created_at > '2023-01-01'")
                .group_by("u.id", "u.name", "u.email")
                .having("COUNT(o.id) > 0")
                .order_by("order_count", "DESC")
                .limit(10)
                .build())
        
        # Check that all parts are present
        assert "SELECT u.name, u.email, COUNT(o.id) as order_count" in query
        assert "FROM users u" in query
        assert "LEFT JOIN orders o ON u.id = o.user_id" in query
        assert "WHERE u.active = 1 AND u.created_at > '2023-01-01'" in query
        assert "GROUP BY u.id, u.name, u.email" in query
        assert "HAVING COUNT(o.id) > 0" in query
        assert "ORDER BY order_count DESC" in query
        assert "LIMIT 10" in query
    
    def test_build_empty_query(self):
        """Test building query with no conditions."""
        builder = SQLQueryBuilder()
        
        query = builder.build()
        
        assert query == "SELECT *"
    
    def test_multiple_builds(self):
        """Test building multiple queries with same builder."""
        builder = SQLQueryBuilder()
        
        # Build first query
        query1 = (builder
                 .select("name")
                 .from_table("users")
                 .build())
        
        # Build second query (should be different)
        query2 = (builder.reset()
                 .select("id", "email")
                 .from_table("customers")
                 .build())
        
        assert query1 == "SELECT name FROM users"
        assert query2 == "SELECT id, email FROM customers"


class TestComputerDirector:
    """Test computer director implementation."""
    
    def test_director_creation(self):
        """Test creating computer director."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        assert director.builder is builder
    
    def test_build_gaming_computer(self):
        """Test building gaming computer."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        computer = director.build_gaming_computer()
        
        assert isinstance(computer, Computer)
        assert "Intel Core i9" in computer.cpu
        assert "32GB" in computer.memory
        assert "1TB" in computer.storage
        assert "RTX 4080" in computer.graphics_card
        assert computer.bluetooth is True
        assert computer.wifi is True
        assert computer.case_color == "RGB"
        assert "Windows 11" in computer.operating_system
        assert computer.monitor is not None
        assert computer.keyboard is not None
        assert computer.mouse is not None
    
    def test_build_office_computer(self):
        """Test building office computer."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        computer = director.build_office_computer()
        
        assert isinstance(computer, Computer)
        assert "Intel Core i5" in computer.cpu
        assert "16GB" in computer.memory
        assert "512GB" in computer.storage
        assert "Integrated Graphics" in computer.graphics_card
        assert computer.wifi is True
        assert computer.case_color == "Black"
        assert "Windows 11" in computer.operating_system
    
    def test_build_budget_computer(self):
        """Test building budget computer."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        computer = director.build_budget_computer()
        
        assert isinstance(computer, Computer)
        assert "AMD Ryzen 3" in computer.cpu
        assert "8GB" in computer.memory
        assert "256GB" in computer.storage
        assert "Integrated Graphics" in computer.graphics_card
        assert computer.wifi is True
        assert computer.case_color == "Black"
        assert "Windows 11" in computer.operating_system
    
    def test_multiple_builds(self):
        """Test building multiple computers."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        gaming = director.build_gaming_computer()
        office = director.build_office_computer()
        budget = director.build_budget_computer()
        
        # Should be different computers
        assert gaming is not office
        assert office is not budget
        assert gaming is not budget
        
        # Should have different specifications
        assert gaming.cpu != office.cpu
        assert office.cpu != budget.cpu
        assert gaming.memory != budget.memory


class TestHouseDirector:
    """Test house director implementation."""
    
    def test_director_creation(self):
        """Test creating house director."""
        builder = HouseBuilder()
        director = HouseDirector(builder)
        
        assert director.builder is builder
    
    def test_build_luxury_house(self):
        """Test building luxury house."""
        builder = HouseBuilder()
        director = HouseDirector(builder)
        
        house = director.build_luxury_house()
        
        assert isinstance(house, House)
        assert "Concrete" in house.foundation
        assert house.walls == "Brick"
        assert "Slate" in house.roof
        assert house.windows == 20
        assert house.doors == 8
        assert house.garage is True
        assert house.garden is True
        assert house.pool is True
        assert house.floors == 3
        assert len(house.rooms) == 8
        assert "Master Bedroom" in house.rooms
        assert "Home Theater" in house.rooms
    
    def test_build_family_house(self):
        """Test building family house."""
        builder = HouseBuilder()
        director = HouseDirector(builder)
        
        house = director.build_family_house()
        
        assert isinstance(house, House)
        assert "Concrete Slab" in house.foundation
        assert "Wood Frame" in house.walls
        assert "Asphalt" in house.roof
        assert house.windows == 12
        assert house.doors == 4
        assert house.garage is True
        assert house.garden is True
        assert house.pool is False
        assert house.floors == 2
        assert len(house.rooms) == 5
        assert "Master Bedroom" in house.rooms
        assert "Children's Bedroom" in house.rooms
    
    def test_build_starter_house(self):
        """Test building starter house."""
        builder = HouseBuilder()
        director = HouseDirector(builder)
        
        house = director.build_starter_house()
        
        assert isinstance(house, House)
        assert "Concrete Slab" in house.foundation
        assert "Wood Frame" in house.walls
        assert "Asphalt" in house.roof
        assert house.windows == 8
        assert house.doors == 2
        assert house.garage is False
        assert house.garden is False
        assert house.pool is False
        assert house.floors == 1
        assert len(house.rooms) == 3
        assert "Bedroom" in house.rooms
        assert "Living Room" in house.rooms
        assert "Kitchen" in house.rooms


class TestPizzaDirector:
    """Test pizza director implementation."""
    
    def test_director_creation(self):
        """Test creating pizza director."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        assert director.builder is builder
    
    def test_build_margherita(self):
        """Test building Margherita pizza."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        pizza = director.build_margherita()
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "medium"
        assert pizza.crust == "thin"
        assert pizza.sauce == "tomato"
        assert pizza.cheese == "mozzarella"
        assert "fresh basil" in pizza.toppings
        assert "tomato slices" in pizza.toppings
    
    def test_build_pepperoni(self):
        """Test building pepperoni pizza."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        pizza = director.build_pepperoni()
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "large"
        assert pizza.crust == "regular"
        assert pizza.sauce == "tomato"
        assert pizza.cheese == "mozzarella"
        assert "pepperoni" in pizza.toppings
    
    def test_build_supreme(self):
        """Test building supreme pizza."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        pizza = director.build_supreme()
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "large"
        assert pizza.crust == "thick"
        assert pizza.sauce == "tomato"
        assert pizza.cheese == "mozzarella"
        assert len(pizza.toppings) == 6
        assert "pepperoni" in pizza.toppings
        assert "sausage" in pizza.toppings
        assert "mushrooms" in pizza.toppings
        assert "bell peppers" in pizza.toppings
        assert "onions" in pizza.toppings
        assert "black olives" in pizza.toppings
        assert pizza.extra_cheese is True
    
    def test_build_veggie_deluxe(self):
        """Test building veggie deluxe pizza."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        pizza = director.build_veggie_deluxe()
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "medium"
        assert pizza.crust == "thin"
        assert pizza.sauce == "pesto"
        assert pizza.cheese == "goat cheese"
        assert len(pizza.toppings) == 6
        assert "spinach" in pizza.toppings
        assert "sun-dried tomatoes" in pizza.toppings
        assert "artichokes" in pizza.toppings
        assert pizza.gluten_free is True


class TestBuilderPatternIntegration:
    """Test integration scenarios with builder pattern."""
    
    def test_complete_computer_configuration_system(self):
        """Test complete computer configuration system."""
        builder = ComputerBuilder()
        director = ComputerDirector(builder)
        
        # Build different computer types
        gaming = director.build_gaming_computer()
        office = director.build_office_computer()
        budget = director.build_budget_computer()
        
        # Custom configuration
        custom = (builder.reset()
                 .set_cpu("Custom CPU")
                 .set_memory("Custom Memory")
                 .set_storage("Custom Storage")
                 .enable_wifi()
                 .build())
        
        computers = [gaming, office, budget, custom]
        
        # All should be valid computers
        assert all(isinstance(c, Computer) for c in computers)
        assert all(c.cpu != "" for c in computers)
        assert all(c.memory != "" for c in computers)
        assert all(c.storage != "" for c in computers)
        
        # Each should be unique
        assert len(set(id(c) for c in computers)) == 4
    
    def test_complex_sql_query_building(self):
        """Test building complex SQL queries."""
        builder = SQLQueryBuilder()
        
        # Build multiple different queries
        queries = []
        
        # Simple query
        query1 = (builder.reset()
                 .select("name", "email")
                 .from_table("users")
                 .where("active = 1")
                 .build())
        queries.append(query1)
        
        # Query with joins
        query2 = (builder.reset()
                 .select("u.name", "p.title")
                 .from_table("users u")
                 .join("posts p", "u.id = p.user_id")
                 .where("p.published = 1")
                 .order_by("p.created_at", "DESC")
                 .build())
        queries.append(query2)
        
        # Aggregation query
        query3 = (builder.reset()
                 .select("department", "COUNT(*) as count")
                 .from_table("employees")
                 .group_by("department")
                 .having("COUNT(*) > 5")
                 .order_by("count", "DESC")
                 .build())
        queries.append(query3)
        
        # All should be valid SQL queries
        assert all(isinstance(q, str) for q in queries)
        assert all(len(q) > 0 for q in queries)
        assert all("SELECT" in q for q in queries)
        assert all("FROM" in q for q in queries)
    
    def test_pizza_ordering_system(self):
        """Test pizza ordering system."""
        builder = PizzaBuilder()
        director = PizzaDirector(builder)
        
        # Create menu pizzas
        menu_pizzas = [
            director.build_margherita(),
            director.build_pepperoni(),
            director.build_supreme(),
            director.build_veggie_deluxe()
        ]
        
        # Create custom pizzas
        custom_pizzas = [
            (builder.reset()
             .set_size("small")
             .set_crust("thin")
             .add_topping("cheese")
             .build()),
            (builder.reset()
             .set_size("extra-large")
             .set_crust("stuffed")
             .add_toppings(["pepperoni", "sausage", "bacon"])
             .add_extra_cheese()
             .make_spicy()
             .build())
        ]
        
        all_pizzas = menu_pizzas + custom_pizzas
        
        # All should be valid pizzas
        assert all(isinstance(p, Pizza) for p in all_pizzas)
        assert all(p.size in ["small", "medium", "large", "extra-large"] for p in all_pizzas)
        assert all(p.crust != "" for p in all_pizzas)
        assert all(p.sauce != "" for p in all_pizzas)
        assert all(p.cheese != "" for p in all_pizzas)
    
    def test_builder_reusability(self):
        """Test that builders can be reused."""
        # Test computer builder reuse
        computer_builder = ComputerBuilder()
        
        computers = []
        for i in range(5):
            computer = (computer_builder.reset()
                       .set_cpu(f"CPU {i}")
                       .set_memory(f"{8 * (i + 1)}GB")
                       .build())
            computers.append(computer)
        
        # Each computer should be different
        assert len(set(c.cpu for c in computers)) == 5
        assert len(set(c.memory for c in computers)) == 5
        
        # Test SQL builder reuse
        sql_builder = SQLQueryBuilder()
        
        queries = []
        for i in range(3):
            query = (sql_builder.reset()
                    .select("*")
                    .from_table(f"table_{i}")
                    .build())
            queries.append(query)
        
        # Each query should be different
        assert len(set(queries)) == 3
        assert all(f"table_{i}" in queries[i] for i in range(3))
    
    def test_director_pattern_with_different_builders(self):
        """Test director pattern with different builders."""
        # Create multiple builders
        builder1 = ComputerBuilder()
        builder2 = ComputerBuilder()
        
        # Create directors with different builders
        director1 = ComputerDirector(builder1)
        director2 = ComputerDirector(builder2)
        
        # Build same type with different directors
        gaming1 = director1.build_gaming_computer()
        gaming2 = director2.build_gaming_computer()
        
        # Should be different objects but same specification
        assert gaming1 is not gaming2
        assert gaming1.cpu == gaming2.cpu
        assert gaming1.memory == gaming2.memory
        assert gaming1.storage == gaming2.storage


class TestBuilderPatternEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_computer_build(self):
        """Test building computer with no specifications."""
        builder = ComputerBuilder()
        
        computer = builder.build()
        
        assert isinstance(computer, Computer)
        assert computer.cpu == ""
        assert computer.memory == ""
        assert computer.storage == ""
        assert computer.graphics_card is None
        assert computer.bluetooth is False
        assert computer.wifi is False
    
    def test_empty_house_build(self):
        """Test building house with no specifications."""
        builder = HouseBuilder()
        
        house = builder.build()
        
        assert isinstance(house, House)
        assert house.foundation == ""
        assert house.walls == ""
        assert house.roof == ""
        assert house.windows == 0
        assert house.doors == 0
        assert house.garage is False
        assert house.rooms == []
    
    def test_empty_pizza_build(self):
        """Test building pizza with no specifications."""
        builder = PizzaBuilder()
        
        pizza = builder.build()
        
        assert isinstance(pizza, Pizza)
        assert pizza.size == "medium"  # Default
        assert pizza.crust == "regular"  # Default
        assert pizza.sauce == "tomato"  # Default
        assert pizza.cheese == "mozzarella"  # Default
        assert pizza.toppings == []
        assert pizza.extra_cheese is False
    
    def test_sql_query_without_from_clause(self):
        """Test building SQL query without FROM clause."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .select("1", "2", "3")
                .build())
        
        assert query == "SELECT 1, 2, 3"
    
    def test_builder_with_none_values(self):
        """Test builder with None values."""
        builder = ComputerBuilder()
        
        # This should not raise an error
        computer = (builder
                   .set_cpu(None)
                   .set_memory(None)
                   .build())
        
        assert computer.cpu is None
        assert computer.memory is None
    
    def test_builder_with_empty_strings(self):
        """Test builder with empty strings."""
        builder = ComputerBuilder()
        
        computer = (builder
                   .set_cpu("")
                   .set_memory("")
                   .build())
        
        assert computer.cpu == ""
        assert computer.memory == ""
    
    def test_pizza_with_empty_toppings_list(self):
        """Test pizza with empty toppings list."""
        builder = PizzaBuilder()
        
        pizza = (builder
                .add_toppings([])
                .build())
        
        assert pizza.toppings == []
    
    def test_house_with_negative_values(self):
        """Test house with negative values."""
        builder = HouseBuilder()
        
        house = (builder
                .set_windows(-5)
                .set_doors(-2)
                .set_floors(-1)
                .build())
        
        # Builder should accept these values (validation is not its responsibility)
        assert house.windows == -5
        assert house.doors == -2
        assert house.floors == -1
    
    def test_sql_builder_with_empty_conditions(self):
        """Test SQL builder with empty conditions."""
        builder = SQLQueryBuilder()
        
        query = (builder
                .where("")
                .having("")
                .build())
        
        # Should include empty conditions
        assert "WHERE" in query
        assert "HAVING" in query


class TestBuilderPatternPerformance:
    """Test performance characteristics of builder pattern."""
    
    def test_builder_performance_with_many_operations(self):
        """Test builder performance with many operations."""
        import time
        
        builder = ComputerBuilder()
        
        start = time.time()
        for i in range(1000):
            computer = (builder.reset()
                       .set_cpu(f"CPU {i}")
                       .set_memory(f"{i}GB")
                       .set_storage(f"{i}TB")
                       .enable_wifi()
                       .enable_bluetooth()
                       .build())
        end = time.time()
        
        execution_time = end - start
        assert execution_time < 1.0  # Should complete quickly
    
    def test_sql_builder_performance(self):
        """Test SQL builder performance."""
        import time
        
        builder = SQLQueryBuilder()
        
        start = time.time()
        for i in range(1000):
            query = (builder.reset()
                    .select("*")
                    .from_table(f"table_{i}")
                    .where(f"id = {i}")
                    .build())
        end = time.time()
        
        execution_time = end - start
        assert execution_time < 1.0  # Should complete quickly
    
    def test_complex_builder_chains(self):
        """Test performance with complex builder chains."""
        import time
        
        builder = PizzaBuilder()
        
        start = time.time()
        for i in range(100):
            pizza = (builder.reset()
                    .set_size("large")
                    .set_crust("thick")
                    .set_sauce("tomato")
                    .set_cheese("mozzarella")
                    .add_topping("pepperoni")
                    .add_topping("sausage")
                    .add_topping("mushrooms")
                    .add_topping("bell peppers")
                    .add_topping("onions")
                    .add_extra_cheese()
                    .make_spicy()
                    .build())
        end = time.time()
        
        execution_time = end - start
        assert execution_time < 0.5  # Should complete quickly