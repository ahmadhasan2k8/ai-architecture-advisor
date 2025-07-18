"""Builder pattern implementations.

This module provides implementations of the Builder pattern, demonstrating
how to construct complex objects step by step with a fluent interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


# Product Classes

@dataclass
class Computer:
    """Computer product built by the builder."""
    cpu: str = ""
    memory: str = ""
    storage: str = ""
    graphics_card: Optional[str] = None
    sound_card: Optional[str] = None
    network_card: Optional[str] = None
    bluetooth: bool = False
    wifi: bool = False
    case_color: str = "black"
    operating_system: Optional[str] = None
    monitor: Optional[str] = None
    keyboard: Optional[str] = None
    mouse: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of the computer.
        
        Returns:
            Computer description
        """
        specs = f"Computer: {self.cpu}, {self.memory}, {self.storage}"
        if self.graphics_card:
            specs += f", {self.graphics_card}"
        if self.operating_system:
            specs += f", {self.operating_system}"
        return specs


@dataclass
class House:
    """House product built by the builder."""
    foundation: str = ""
    walls: str = ""
    roof: str = ""
    windows: int = 0
    doors: int = 0
    garage: bool = False
    garden: bool = False
    pool: bool = False
    floors: int = 1
    rooms: List[str] = None
    
    def __post_init__(self):
        """Initialize rooms list if not provided."""
        if self.rooms is None:
            self.rooms = []
    
    def __str__(self) -> str:
        """String representation of the house.
        
        Returns:
            House description
        """
        return (f"House: {self.foundation} foundation, {self.walls} walls, "
                f"{self.roof} roof, {self.floors} floor(s), {len(self.rooms)} rooms")


@dataclass
class Pizza:
    """Pizza product built by the builder."""
    size: str = "medium"
    crust: str = "regular"
    sauce: str = "tomato"
    cheese: str = "mozzarella"
    toppings: List[str] = None
    extra_cheese: bool = False
    gluten_free: bool = False
    spicy: bool = False
    
    def __post_init__(self):
        """Initialize toppings list if not provided."""
        if self.toppings is None:
            self.toppings = []
    
    def __str__(self) -> str:
        """String representation of the pizza.
        
        Returns:
            Pizza description
        """
        desc = f"{self.size.title()} {self.crust} crust pizza with {self.sauce} sauce and {self.cheese}"
        if self.toppings:
            desc += f", topped with {', '.join(self.toppings)}"
        if self.extra_cheese:
            desc += ", extra cheese"
        if self.gluten_free:
            desc += " (gluten-free)"
        if self.spicy:
            desc += " (spicy)"
        return desc


# Abstract Builder Interface

class Builder(ABC):
    """Abstract builder interface."""
    
    @abstractmethod
    def reset(self) -> None:
        """Reset the builder to initial state."""
        pass
    
    @abstractmethod
    def build(self) -> Any:
        """Build and return the final product."""
        pass


# Computer Builder

class ComputerBuilder:
    """Builder for Computer objects with a fluent interface."""
    
    def __init__(self):
        """Initialize the computer builder."""
        self.reset()
    
    def reset(self) -> 'ComputerBuilder':
        """Reset the builder to initial state.
        
        Returns:
            Self for method chaining
        """
        self._computer = Computer()
        return self
    
    def set_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Set the CPU.
        
        Args:
            cpu: CPU model
            
        Returns:
            Self for method chaining
        """
        self._computer.cpu = cpu
        return self
    
    def set_memory(self, memory: str) -> 'ComputerBuilder':
        """Set the memory.
        
        Args:
            memory: Memory specification
            
        Returns:
            Self for method chaining
        """
        self._computer.memory = memory
        return self
    
    def set_storage(self, storage: str) -> 'ComputerBuilder':
        """Set the storage.
        
        Args:
            storage: Storage specification
            
        Returns:
            Self for method chaining
        """
        self._computer.storage = storage
        return self
    
    def set_graphics_card(self, graphics_card: str) -> 'ComputerBuilder':
        """Set the graphics card.
        
        Args:
            graphics_card: Graphics card model
            
        Returns:
            Self for method chaining
        """
        self._computer.graphics_card = graphics_card
        return self
    
    def set_sound_card(self, sound_card: str) -> 'ComputerBuilder':
        """Set the sound card.
        
        Args:
            sound_card: Sound card model
            
        Returns:
            Self for method chaining
        """
        self._computer.sound_card = sound_card
        return self
    
    def set_network_card(self, network_card: str) -> 'ComputerBuilder':
        """Set the network card.
        
        Args:
            network_card: Network card model
            
        Returns:
            Self for method chaining
        """
        self._computer.network_card = network_card
        return self
    
    def enable_bluetooth(self) -> 'ComputerBuilder':
        """Enable Bluetooth.
        
        Returns:
            Self for method chaining
        """
        self._computer.bluetooth = True
        return self
    
    def enable_wifi(self) -> 'ComputerBuilder':
        """Enable WiFi.
        
        Returns:
            Self for method chaining
        """
        self._computer.wifi = True
        return self
    
    def set_case_color(self, color: str) -> 'ComputerBuilder':
        """Set the case color.
        
        Args:
            color: Case color
            
        Returns:
            Self for method chaining
        """
        self._computer.case_color = color
        return self
    
    def set_operating_system(self, os: str) -> 'ComputerBuilder':
        """Set the operating system.
        
        Args:
            os: Operating system name
            
        Returns:
            Self for method chaining
        """
        self._computer.operating_system = os
        return self
    
    def set_monitor(self, monitor: str) -> 'ComputerBuilder':
        """Set the monitor.
        
        Args:
            monitor: Monitor specification
            
        Returns:
            Self for method chaining
        """
        self._computer.monitor = monitor
        return self
    
    def set_keyboard(self, keyboard: str) -> 'ComputerBuilder':
        """Set the keyboard.
        
        Args:
            keyboard: Keyboard type
            
        Returns:
            Self for method chaining
        """
        self._computer.keyboard = keyboard
        return self
    
    def set_mouse(self, mouse: str) -> 'ComputerBuilder':
        """Set the mouse.
        
        Args:
            mouse: Mouse type
            
        Returns:
            Self for method chaining
        """
        self._computer.mouse = mouse
        return self
    
    def build(self) -> Computer:
        """Build and return the computer.
        
        Returns:
            Constructed computer
        """
        return self._computer


# House Builder

class HouseBuilder:
    """Builder for House objects with a fluent interface."""
    
    def __init__(self):
        """Initialize the house builder."""
        self.reset()
    
    def reset(self) -> 'HouseBuilder':
        """Reset the builder to initial state.
        
        Returns:
            Self for method chaining
        """
        self._house = House()
        return self
    
    def set_foundation(self, foundation: str) -> 'HouseBuilder':
        """Set the foundation type.
        
        Args:
            foundation: Foundation type
            
        Returns:
            Self for method chaining
        """
        self._house.foundation = foundation
        return self
    
    def set_walls(self, walls: str) -> 'HouseBuilder':
        """Set the wall material.
        
        Args:
            walls: Wall material
            
        Returns:
            Self for method chaining
        """
        self._house.walls = walls
        return self
    
    def set_roof(self, roof: str) -> 'HouseBuilder':
        """Set the roof type.
        
        Args:
            roof: Roof type
            
        Returns:
            Self for method chaining
        """
        self._house.roof = roof
        return self
    
    def set_windows(self, count: int) -> 'HouseBuilder':
        """Set the number of windows.
        
        Args:
            count: Number of windows
            
        Returns:
            Self for method chaining
        """
        self._house.windows = count
        return self
    
    def set_doors(self, count: int) -> 'HouseBuilder':
        """Set the number of doors.
        
        Args:
            count: Number of doors
            
        Returns:
            Self for method chaining
        """
        self._house.doors = count
        return self
    
    def add_garage(self) -> 'HouseBuilder':
        """Add a garage.
        
        Returns:
            Self for method chaining
        """
        self._house.garage = True
        return self
    
    def add_garden(self) -> 'HouseBuilder':
        """Add a garden.
        
        Returns:
            Self for method chaining
        """
        self._house.garden = True
        return self
    
    def add_pool(self) -> 'HouseBuilder':
        """Add a pool.
        
        Returns:
            Self for method chaining
        """
        self._house.pool = True
        return self
    
    def set_floors(self, floors: int) -> 'HouseBuilder':
        """Set the number of floors.
        
        Args:
            floors: Number of floors
            
        Returns:
            Self for method chaining
        """
        self._house.floors = floors
        return self
    
    def add_room(self, room: str) -> 'HouseBuilder':
        """Add a room.
        
        Args:
            room: Room type
            
        Returns:
            Self for method chaining
        """
        self._house.rooms.append(room)
        return self
    
    def build(self) -> House:
        """Build and return the house.
        
        Returns:
            Constructed house
        """
        return self._house


# Pizza Builder

class PizzaBuilder:
    """Builder for Pizza objects with a fluent interface."""
    
    def __init__(self):
        """Initialize the pizza builder."""
        self.reset()
    
    def reset(self) -> 'PizzaBuilder':
        """Reset the builder to initial state.
        
        Returns:
            Self for method chaining
        """
        self._pizza = Pizza()
        return self
    
    def set_size(self, size: str) -> 'PizzaBuilder':
        """Set the pizza size.
        
        Args:
            size: Pizza size (small, medium, large, extra-large)
            
        Returns:
            Self for method chaining
        """
        self._pizza.size = size
        return self
    
    def set_crust(self, crust: str) -> 'PizzaBuilder':
        """Set the crust type.
        
        Args:
            crust: Crust type (thin, regular, thick, stuffed)
            
        Returns:
            Self for method chaining
        """
        self._pizza.crust = crust
        return self
    
    def set_sauce(self, sauce: str) -> 'PizzaBuilder':
        """Set the sauce type.
        
        Args:
            sauce: Sauce type
            
        Returns:
            Self for method chaining
        """
        self._pizza.sauce = sauce
        return self
    
    def set_cheese(self, cheese: str) -> 'PizzaBuilder':
        """Set the cheese type.
        
        Args:
            cheese: Cheese type
            
        Returns:
            Self for method chaining
        """
        self._pizza.cheese = cheese
        return self
    
    def add_topping(self, topping: str) -> 'PizzaBuilder':
        """Add a topping.
        
        Args:
            topping: Topping to add
            
        Returns:
            Self for method chaining
        """
        self._pizza.toppings.append(topping)
        return self
    
    def add_toppings(self, toppings: List[str]) -> 'PizzaBuilder':
        """Add multiple toppings.
        
        Args:
            toppings: List of toppings to add
            
        Returns:
            Self for method chaining
        """
        self._pizza.toppings.extend(toppings)
        return self
    
    def add_extra_cheese(self) -> 'PizzaBuilder':
        """Add extra cheese.
        
        Returns:
            Self for method chaining
        """
        self._pizza.extra_cheese = True
        return self
    
    def make_gluten_free(self) -> 'PizzaBuilder':
        """Make the pizza gluten-free.
        
        Returns:
            Self for method chaining
        """
        self._pizza.gluten_free = True
        return self
    
    def make_spicy(self) -> 'PizzaBuilder':
        """Make the pizza spicy.
        
        Returns:
            Self for method chaining
        """
        self._pizza.spicy = True
        return self
    
    def build(self) -> Pizza:
        """Build and return the pizza.
        
        Returns:
            Constructed pizza
        """
        return self._pizza


# Director Classes

class ComputerDirector:
    """Director that uses ComputerBuilder to construct specific computer types."""
    
    def __init__(self, builder: ComputerBuilder):
        """Initialize the director.
        
        Args:
            builder: Computer builder instance
        """
        self.builder = builder
    
    def build_gaming_computer(self) -> Computer:
        """Build a gaming computer.
        
        Returns:
            Gaming computer configuration
        """
        return (self.builder.reset()
                .set_cpu("Intel Core i9-13900K")
                .set_memory("32GB DDR5")
                .set_storage("1TB NVMe SSD")
                .set_graphics_card("NVIDIA RTX 4080")
                .set_sound_card("Creative Sound Blaster AE-9")
                .set_network_card("Killer Ethernet E3100")
                .enable_bluetooth()
                .enable_wifi()
                .set_case_color("RGB")
                .set_operating_system("Windows 11 Pro")
                .set_monitor("32-inch 4K Gaming Monitor")
                .set_keyboard("Mechanical RGB Keyboard")
                .set_mouse("High-DPI Gaming Mouse")
                .build())
    
    def build_office_computer(self) -> Computer:
        """Build an office computer.
        
        Returns:
            Office computer configuration
        """
        return (self.builder.reset()
                .set_cpu("Intel Core i5-13400")
                .set_memory("16GB DDR4")
                .set_storage("512GB SSD")
                .set_graphics_card("Integrated Graphics")
                .set_network_card("Standard Ethernet")
                .enable_wifi()
                .set_case_color("Black")
                .set_operating_system("Windows 11 Pro")
                .set_monitor("24-inch 1080p Monitor")
                .set_keyboard("Standard Keyboard")
                .set_mouse("Optical Mouse")
                .build())
    
    def build_budget_computer(self) -> Computer:
        """Build a budget computer.
        
        Returns:
            Budget computer configuration
        """
        return (self.builder.reset()
                .set_cpu("AMD Ryzen 3 4300G")
                .set_memory("8GB DDR4")
                .set_storage("256GB SSD")
                .set_graphics_card("Integrated Graphics")
                .enable_wifi()
                .set_case_color("Black")
                .set_operating_system("Windows 11 Home")
                .build())


class HouseDirector:
    """Director that uses HouseBuilder to construct specific house types."""
    
    def __init__(self, builder: HouseBuilder):
        """Initialize the director.
        
        Args:
            builder: House builder instance
        """
        self.builder = builder
    
    def build_luxury_house(self) -> House:
        """Build a luxury house.
        
        Returns:
            Luxury house configuration
        """
        return (self.builder.reset()
                .set_foundation("Reinforced Concrete")
                .set_walls("Brick")
                .set_roof("Slate Tile")
                .set_windows(20)
                .set_doors(8)
                .add_garage()
                .add_garden()
                .add_pool()
                .set_floors(3)
                .add_room("Master Bedroom")
                .add_room("Guest Bedroom")
                .add_room("Study")
                .add_room("Living Room")
                .add_room("Dining Room")
                .add_room("Kitchen")
                .add_room("Home Theater")
                .add_room("Gym")
                .build())
    
    def build_family_house(self) -> House:
        """Build a family house.
        
        Returns:
            Family house configuration
        """
        return (self.builder.reset()
                .set_foundation("Concrete Slab")
                .set_walls("Wood Frame")
                .set_roof("Asphalt Shingles")
                .set_windows(12)
                .set_doors(4)
                .add_garage()
                .add_garden()
                .set_floors(2)
                .add_room("Master Bedroom")
                .add_room("Children's Bedroom")
                .add_room("Living Room")
                .add_room("Kitchen")
                .add_room("Dining Room")
                .build())
    
    def build_starter_house(self) -> House:
        """Build a starter house.
        
        Returns:
            Starter house configuration
        """
        return (self.builder.reset()
                .set_foundation("Concrete Slab")
                .set_walls("Wood Frame")
                .set_roof("Asphalt Shingles")
                .set_windows(8)
                .set_doors(2)
                .set_floors(1)
                .add_room("Bedroom")
                .add_room("Living Room")
                .add_room("Kitchen")
                .build())


class PizzaDirector:
    """Director that uses PizzaBuilder to construct specific pizza types."""
    
    def __init__(self, builder: PizzaBuilder):
        """Initialize the director.
        
        Args:
            builder: Pizza builder instance
        """
        self.builder = builder
    
    def build_margherita(self) -> Pizza:
        """Build a Margherita pizza.
        
        Returns:
            Margherita pizza
        """
        return (self.builder.reset()
                .set_size("medium")
                .set_crust("thin")
                .set_sauce("tomato")
                .set_cheese("mozzarella")
                .add_topping("fresh basil")
                .add_topping("tomato slices")
                .build())
    
    def build_pepperoni(self) -> Pizza:
        """Build a pepperoni pizza.
        
        Returns:
            Pepperoni pizza
        """
        return (self.builder.reset()
                .set_size("large")
                .set_crust("regular")
                .set_sauce("tomato")
                .set_cheese("mozzarella")
                .add_topping("pepperoni")
                .build())
    
    def build_supreme(self) -> Pizza:
        """Build a supreme pizza.
        
        Returns:
            Supreme pizza
        """
        return (self.builder.reset()
                .set_size("large")
                .set_crust("thick")
                .set_sauce("tomato")
                .set_cheese("mozzarella")
                .add_toppings(["pepperoni", "sausage", "mushrooms", 
                              "bell peppers", "onions", "black olives"])
                .add_extra_cheese()
                .build())
    
    def build_veggie_deluxe(self) -> Pizza:
        """Build a veggie deluxe pizza.
        
        Returns:
            Veggie deluxe pizza
        """
        return (self.builder.reset()
                .set_size("medium")
                .set_crust("thin")
                .set_sauce("pesto")
                .set_cheese("goat cheese")
                .add_toppings(["spinach", "sun-dried tomatoes", "artichokes",
                              "bell peppers", "red onions", "pine nuts"])
                .make_gluten_free()
                .build())


# SQL Query Builder Example

class SQLQueryBuilder:
    """Builder for constructing SQL queries."""
    
    def __init__(self):
        """Initialize the SQL query builder."""
        self.reset()
    
    def reset(self) -> 'SQLQueryBuilder':
        """Reset the builder to initial state.
        
        Returns:
            Self for method chaining
        """
        self._query_parts = {
            'select': [],
            'from': '',
            'joins': [],
            'where': [],
            'group_by': [],
            'having': [],
            'order_by': [],
            'limit': None
        }
        return self
    
    def select(self, *columns: str) -> 'SQLQueryBuilder':
        """Add SELECT columns.
        
        Args:
            *columns: Column names to select
            
        Returns:
            Self for method chaining
        """
        self._query_parts['select'].extend(columns)
        return self
    
    def from_table(self, table: str) -> 'SQLQueryBuilder':
        """Set the FROM table.
        
        Args:
            table: Table name
            
        Returns:
            Self for method chaining
        """
        self._query_parts['from'] = table
        return self
    
    def join(self, table: str, on_condition: str, join_type: str = 'INNER') -> 'SQLQueryBuilder':
        """Add a JOIN clause.
        
        Args:
            table: Table to join
            on_condition: JOIN condition
            join_type: Type of join (INNER, LEFT, RIGHT, FULL)
            
        Returns:
            Self for method chaining
        """
        self._query_parts['joins'].append(f"{join_type} JOIN {table} ON {on_condition}")
        return self
    
    def where(self, condition: str) -> 'SQLQueryBuilder':
        """Add a WHERE condition.
        
        Args:
            condition: WHERE condition
            
        Returns:
            Self for method chaining
        """
        self._query_parts['where'].append(condition)
        return self
    
    def group_by(self, *columns: str) -> 'SQLQueryBuilder':
        """Add GROUP BY columns.
        
        Args:
            *columns: Column names to group by
            
        Returns:
            Self for method chaining
        """
        self._query_parts['group_by'].extend(columns)
        return self
    
    def having(self, condition: str) -> 'SQLQueryBuilder':
        """Add a HAVING condition.
        
        Args:
            condition: HAVING condition
            
        Returns:
            Self for method chaining
        """
        self._query_parts['having'].append(condition)
        return self
    
    def order_by(self, column: str, direction: str = 'ASC') -> 'SQLQueryBuilder':
        """Add an ORDER BY clause.
        
        Args:
            column: Column to order by
            direction: Sort direction (ASC or DESC)
            
        Returns:
            Self for method chaining
        """
        self._query_parts['order_by'].append(f"{column} {direction}")
        return self
    
    def limit(self, count: int) -> 'SQLQueryBuilder':
        """Add a LIMIT clause.
        
        Args:
            count: Number of rows to limit
            
        Returns:
            Self for method chaining
        """
        self._query_parts['limit'] = count
        return self
    
    def build(self) -> str:
        """Build and return the SQL query.
        
        Returns:
            SQL query string
        """
        query_parts = []
        
        # SELECT
        if self._query_parts['select']:
            query_parts.append(f"SELECT {', '.join(self._query_parts['select'])}")
        else:
            query_parts.append("SELECT *")
        
        # FROM
        if self._query_parts['from']:
            query_parts.append(f"FROM {self._query_parts['from']}")
        
        # JOINs
        for join in self._query_parts['joins']:
            query_parts.append(join)
        
        # WHERE
        if self._query_parts['where']:
            query_parts.append(f"WHERE {' AND '.join(self._query_parts['where'])}")
        
        # GROUP BY
        if self._query_parts['group_by']:
            query_parts.append(f"GROUP BY {', '.join(self._query_parts['group_by'])}")
        
        # HAVING
        if self._query_parts['having']:
            query_parts.append(f"HAVING {' AND '.join(self._query_parts['having'])}")
        
        # ORDER BY
        if self._query_parts['order_by']:
            query_parts.append(f"ORDER BY {', '.join(self._query_parts['order_by'])}")
        
        # LIMIT
        if self._query_parts['limit']:
            query_parts.append(f"LIMIT {self._query_parts['limit']}")
        
        return ' '.join(query_parts)


# Example usage functions

def demonstrate_computer_builder():
    """Demonstrate computer builder pattern."""
    print("=== Computer Builder Demo ===")
    
    # Manual building
    builder = ComputerBuilder()
    
    gaming_pc = (builder
                  .set_cpu("Intel Core i9-13900K")
                  .set_memory("32GB DDR5")
                  .set_storage("1TB NVMe SSD")
                  .set_graphics_card("NVIDIA RTX 4080")
                  .enable_wifi()
                  .enable_bluetooth()
                  .set_case_color("RGB")
                  .set_operating_system("Windows 11 Pro")
                  .build())
    
    print(f"Gaming PC: {gaming_pc}")
    
    # Using director
    director = ComputerDirector(builder)
    
    office_pc = director.build_office_computer()
    print(f"Office PC: {office_pc}")
    
    budget_pc = director.build_budget_computer()
    print(f"Budget PC: {budget_pc}")


def demonstrate_house_builder():
    """Demonstrate house builder pattern."""
    print("\n=== House Builder Demo ===")
    
    builder = HouseBuilder()
    director = HouseDirector(builder)
    
    luxury_house = director.build_luxury_house()
    print(f"Luxury House: {luxury_house}")
    
    family_house = director.build_family_house()
    print(f"Family House: {family_house}")
    
    starter_house = director.build_starter_house()
    print(f"Starter House: {starter_house}")


def demonstrate_pizza_builder():
    """Demonstrate pizza builder pattern."""
    print("\n=== Pizza Builder Demo ===")
    
    builder = PizzaBuilder()
    director = PizzaDirector(builder)
    
    margherita = director.build_margherita()
    print(f"Margherita: {margherita}")
    
    pepperoni = director.build_pepperoni()
    print(f"Pepperoni: {pepperoni}")
    
    supreme = director.build_supreme()
    print(f"Supreme: {supreme}")
    
    veggie = director.build_veggie_deluxe()
    print(f"Veggie Deluxe: {veggie}")
    
    # Custom pizza
    custom_pizza = (builder.reset()
                    .set_size("extra-large")
                    .set_crust("stuffed")
                    .set_sauce("bbq")
                    .set_cheese("cheddar")
                    .add_toppings(["chicken", "bacon", "red onions"])
                    .make_spicy()
                    .build())
    
    print(f"Custom Pizza: {custom_pizza}")


def demonstrate_sql_builder():
    """Demonstrate SQL query builder."""
    print("\n=== SQL Query Builder Demo ===")
    
    builder = SQLQueryBuilder()
    
    # Simple query
    query1 = (builder.reset()
              .select("name", "email")
              .from_table("users")
              .where("active = 1")
              .order_by("name")
              .build())
    
    print(f"Simple Query: {query1}")
    
    # Complex query
    query2 = (builder.reset()
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
    
    print(f"Complex Query: {query2}")


if __name__ == "__main__":
    demonstrate_computer_builder()
    demonstrate_house_builder()
    demonstrate_pizza_builder()
    demonstrate_sql_builder()