# Pattern Decision Guide

A comprehensive guide for choosing the right design pattern based on real-world scenarios and requirements.

## Quick Pattern Selection

### Start Here: What Are You Trying To Do?

#### 🏗️ Creating Objects
- **One instance needed globally?** → [Singleton Pattern](#singleton-pattern)
- **Multiple similar objects?** → [Factory Pattern](#factory-pattern)  
- **Complex object construction?** → [Builder Pattern](#builder-pattern)

#### 🔄 Managing Behavior
- **Multiple algorithms for same task?** → [Strategy Pattern](#strategy-pattern)
- **Behavior changes based on state?** → [State Pattern](#state-pattern)
- **Need undo/redo functionality?** → [Command Pattern](#command-pattern)

#### 🔗 Connecting Components
- **Incompatible interfaces?** → [Adapter Pattern](#adapter-pattern)
- **Add features dynamically?** → [Decorator Pattern](#decorator-pattern)
- **One-to-many notifications?** → [Observer Pattern](#observer-pattern)

#### 💾 Data Access
- **Centralize data access logic?** → [Repository Pattern](#repository-pattern)

---

## Detailed Decision Trees

### Singleton Pattern

```
Do you need exactly ONE instance of a class?
├─ YES
│  ├─ Is it expensive to create? (database connections, file handles)
│  │  ├─ YES → ✅ Use Singleton
│  │  └─ NO → Is global access truly needed?
│  │     ├─ YES → ✅ Use Singleton (with caution)
│  │     └─ NO → ❌ Use regular class or module-level variable
│  └─ NO → ❌ DON'T use Singleton
│
Special Cases:
├─ Configuration data → ✅ Singleton is good
├─ Logging system → ✅ Singleton is good  
├─ User/Product/Order entities → ❌ NEVER use Singleton
└─ "For consistency" → ❌ Bad reason for Singleton
```

**Complexity Threshold**: Use when object creation is expensive OR truly global access needed
**Thread Safety**: Required for multi-threaded apps (use double-check locking)

### Factory Pattern

```
Are you creating objects based on some criteria?
├─ YES
│  ├─ How many different types? 
│  │  ├─ 1-2 types → ❌ Simple if/else is better
│  │  ├─ 3+ types → ✅ Factory Pattern
│  │  └─ Many related families → ✅ Abstract Factory
│  └─ Is creation logic complex?
│     ├─ YES (>5 lines) → ✅ Factory Pattern
│     └─ NO → ❌ Direct instantiation is fine
└─ NO → ❌ Don't use Factory
```

**Complexity Threshold**: 3+ similar classes OR complex creation logic
**When NOT to use**: Single class, simple creation, "just in case" scenarios

### Strategy Pattern

```
Do you have multiple ways to do the same thing?
├─ YES
│  ├─ How many algorithms/approaches?
│  │  ├─ 1-2 → ❌ Simple if/else or parameters
│  │  ├─ 3+ → ✅ Strategy Pattern
│  │  └─ Need runtime switching? → ✅ Strategy Pattern
│  └─ Are algorithms likely to change/grow?
│     ├─ YES → ✅ Strategy Pattern  
│     └─ NO → ❌ Simple conditionals OK
└─ NO → ❌ Don't use Strategy
```

**Complexity Threshold**: 3+ algorithms OR runtime algorithm selection needed
**Signs**: Long if/elif chains, "switch algorithm based on data" requirements

### Observer Pattern  

```
Do multiple objects need to know about changes?
├─ YES
│  ├─ How many observers?
│  │  ├─ 1 → ❌ Direct method call is simpler
│  │  ├─ 2+ → ✅ Observer Pattern
│  │  └─ Dynamic add/remove needed? → ✅ Observer Pattern
│  └─ Is loose coupling important?
│     ├─ YES → ✅ Observer Pattern
│     └─ NO → ❌ Direct coupling might be OK
└─ NO → ❌ Don't use Observer
```

**Complexity Threshold**: 2+ observers OR dynamic subscription needed
**Performance Note**: Adds notification overhead - consider for non-critical paths

### Builder Pattern

```
Does object construction have many parameters?
├─ YES
│  ├─ How many constructor parameters?
│  │  ├─ <5 → ❌ Regular constructor OK
│  │  ├─ 5-7 → ✅ Consider Builder
│  │  └─ 8+ → ✅ Definitely use Builder
│  └─ Are many parameters optional?
│     ├─ YES (3+ optional) → ✅ Builder Pattern
│     └─ NO → ❌ Regular constructor with defaults
└─ NO → ❌ Don't use Builder
```

**Complexity Threshold**: 5+ constructor parameters OR complex validation needed
**Alternative**: Dataclasses with defaults for simple cases

### Command Pattern

```
Do you need to do more than just execute an operation?
├─ YES
│  ├─ Need undo functionality? → ✅ Command Pattern
│  ├─ Need to queue operations? → ✅ Command Pattern  
│  ├─ Need to log operations? → ✅ Command Pattern
│  └─ Need macro recording? → ✅ Command Pattern
└─ NO → ❌ Direct method calls are simpler
```

**Complexity Threshold**: Any undo/redo, queuing, or operation logging needs
**Overkill for**: Simple getters/setters, basic operations

---

## Real-World Scenarios

### E-Commerce System

**Scenario**: Building an online store

**Pattern Recommendations**:
- **User Management**: Regular classes (NOT Singleton)
- **Product Catalog**: Factory for different product types
- **Shopping Cart**: Observer for cart change notifications
- **Payment Processing**: Strategy for different payment methods
- **Order Processing**: Command for undo/tracking
- **Data Access**: Repository for product/order data

### Game Development

**Scenario**: Building a role-playing game

**Pattern Recommendations**:
- **Game Settings**: Singleton for global configuration
- **Character Creation**: Builder for complex character setup
- **Character Abilities**: Strategy for different skill sets
- **Character States**: State pattern (combat/stealth/exploration)
- **UI Updates**: Observer for character stat changes
- **Actions**: Command for undo/macro support

### Web Application

**Scenario**: Building a web service

**Pattern Recommendations**:
- **Database Connection**: Singleton (thread-safe)
- **API Response Formats**: Strategy for JSON/XML/CSV
- **Authentication**: Decorator for adding auth to endpoints
- **Data Access**: Repository for clean data layer
- **Event Notifications**: Observer for user actions
- **Request Processing**: Chain of responsibility

---

## Anti-Pattern Detection

### 🚨 Red Flags - When NOT to Use Patterns

#### Singleton Anti-Patterns
```python
# ❌ BAD: Data models as singletons
class User(metaclass=SingletonMeta):
    def __init__(self, name, email):
        self.name = name
        self.email = email

# ✅ GOOD: Regular class
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

#### Factory Anti-Patterns
```python
# ❌ BAD: Factory for single class
class UserFactory:
    @staticmethod
    def create_user(name, email):
        return User(name, email)

# ✅ GOOD: Direct instantiation
user = User(name, email)
```

#### Strategy Anti-Patterns
```python
# ❌ BAD: Strategy for 2 simple cases
class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, amount): pass

class USStrategy(TaxStrategy):
    def calculate(self, amount): return amount * 0.08

class EUStrategy(TaxStrategy):
    def calculate(self, amount): return amount * 0.20

# ✅ GOOD: Simple function
def calculate_tax(amount, region):
    return amount * (0.08 if region == 'US' else 0.20)
```

### When to Prefer Simple Solutions

1. **2-3 variations**: Use if/else instead of Strategy/Factory
2. **Simple objects**: Use regular constructors instead of Builder
3. **Single observer**: Use direct method calls instead of Observer
4. **No undo needed**: Use direct operations instead of Command
5. **Can modify interfaces**: Use direct inheritance instead of Adapter

---

## Pattern Combinations

### Common Pattern Combinations

#### Factory + Strategy
```python
# Create strategies through factory
strategy = StrategyFactory.create(algorithm_type)
result = strategy.execute(data)
```

#### Observer + Command  
```python
# Event sourcing: commands create events, observers handle them
command = CreateOrderCommand(order_data)
command.execute()  # Triggers observers via events
```

#### Repository + Factory
```python
# Repository creates domain objects via factory
user_repo = UserRepository()
user = user_repo.find_by_id(123)  # Uses factory internally
```

#### Builder + Strategy
```python
# Complex objects with algorithmic variations
query = (QueryBuilder()
         .select("*")
         .from_table("users")
         .with_strategy(OptimizedStrategy())
         .build())
```

---

## Performance Considerations

### Pattern Overhead

| Pattern | Performance Impact | When to Worry |
|---------|-------------------|---------------|
| Singleton | Minimal (after creation) | High-frequency access |
| Factory | Small method call overhead | Object creation in tight loops |
| Strategy | Small delegation overhead | CPU-intensive algorithms |
| Observer | Notification loop overhead | Many observers or frequent updates |
| Command | Object creation overhead | Simple operations in hot paths |
| Builder | Method chaining overhead | Simple object creation |

### Optimization Strategies

1. **Singleton**: Use eager initialization for frequently accessed singletons
2. **Factory**: Cache created objects when possible
3. **Strategy**: Profile algorithm performance differences
4. **Observer**: Use async notifications for non-critical updates
5. **Command**: Implement object pooling for frequently used commands
6. **Builder**: Consider fluent interfaces only for complex objects

---

## Testing Implications

### Testing Challenges by Pattern

#### Singleton
- **Problem**: Global state makes tests interdependent
- **Solution**: Reset mechanism or dependency injection
- **Test**: Verify singleton property, thread safety

#### Factory  
- **Problem**: Testing all creation paths
- **Solution**: Mock factory for client testing
- **Test**: Each factory method, error conditions

#### Strategy
- **Problem**: Testing strategy selection logic
- **Solution**: Test strategies individually, then context
- **Test**: Each strategy, selection algorithm

#### Observer
- **Problem**: Testing notification sequences
- **Solution**: Mock observers, verify notification order
- **Test**: Registration, notification, cleanup

#### Command
- **Problem**: Testing undo/redo sequences
- **Solution**: Test execute/undo separately
- **Test**: Command execution, undo logic, history management

#### Builder
- **Problem**: Testing all construction paths
- **Solution**: Test required vs optional parameters
- **Test**: Validation, different build sequences

---

## Decision Checklist

Before implementing any pattern, ask:

### ✅ Pre-Implementation Checklist

1. **Complexity Justified?**
   - [ ] Problem meets pattern's complexity threshold
   - [ ] Simple solution considered and rejected
   - [ ] Pattern adds real value, not just structure

2. **Requirements Match?**
   - [ ] Current requirements align with pattern benefits
   - [ ] Future requirements likely to benefit from pattern
   - [ ] Pattern doesn't solve imaginary future problems

3. **Team Ready?**
   - [ ] Team understands the pattern
   - [ ] Documentation and examples available
   - [ ] Maintenance plan in place

4. **Performance Acceptable?**
   - [ ] Pattern overhead measured and acceptable
   - [ ] Alternative solutions compared
   - [ ] Performance requirements still met

5. **Testing Feasible?**
   - [ ] Pattern can be properly unit tested
   - [ ] Mocking strategy identified
   - [ ] Integration testing plan exists

### 🚫 Stop Signs - Don't Implement If:

- [ ] "We might need it later" is the main justification
- [ ] Pattern makes simple code complex without clear benefit
- [ ] Team doesn't understand the pattern well
- [ ] No clear way to test the implementation
- [ ] Simpler solution would work just as well
- [ ] Pattern is being used "for consistency" without benefit

---

## Quick Reference

### Pattern Selection Flowchart

```
Start Here: What's Your Main Goal?
│
├─ Create Objects
│  ├─ One global instance → Singleton
│  ├─ Choose type at runtime → Factory  
│  └─ Complex construction → Builder
│
├─ Manage Behavior
│  ├─ Multiple algorithms → Strategy
│  ├─ State-dependent behavior → State
│  └─ Need undo/redo → Command
│
├─ Connect Components  
│  ├─ Incompatible interfaces → Adapter
│  ├─ Add features dynamically → Decorator
│  └─ Notify multiple objects → Observer
│
└─ Access Data
   └─ Centralize data logic → Repository

Remember: When in doubt, choose the simpler solution!
```