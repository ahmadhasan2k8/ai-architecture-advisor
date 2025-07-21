"""
Design Pattern Knowledge Base for Intelligent Recommendations

This module contains structured knowledge extracted from the design patterns
tutorial notebooks to power intelligent pattern recommendations.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class ComplexityLevel(Enum):
    """Complexity levels for pattern usage scenarios"""

    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"


class PatternConfidence(Enum):
    """Confidence levels for pattern recommendations"""

    LOW = "low"  # 0-40% - Pattern might help but alternatives exist
    MEDIUM = "medium"  # 40-70% - Pattern is a good fit
    HIGH = "high"  # 70-90% - Pattern strongly recommended
    CRITICAL = "critical"  # 90%+ - Pattern is essential for this scenario


@dataclass
class PatternCriteria:
    """Criteria for when to use a pattern"""

    minimum_complexity: ComplexityLevel
    indicators: List[str]  # Phrases/scenarios that suggest this pattern
    thresholds: Dict[str, int]  # Numeric thresholds (e.g., "algorithms": 3)
    use_cases: List[str]
    benefits: List[str]


@dataclass
class AntiPatternCriteria:
    """Criteria for when NOT to use a pattern"""

    red_flags: List[str]  # Phrases that indicate pattern misuse
    scenarios_to_avoid: List[str]
    better_alternatives: List[str]
    common_mistakes: List[str]


@dataclass
class AdvancedScenarios:
    """Advanced scenarios and optimizations for patterns"""

    threading_considerations: Optional[str]
    performance_implications: Optional[str]
    testing_challenges: Optional[str]
    optimization_tips: Optional[str]
    enterprise_considerations: Optional[str]


@dataclass
class PatternKnowledge:
    """Complete knowledge about a design pattern"""

    name: str
    category: str  # creational, structural, behavioral
    description: str
    when_to_use: PatternCriteria
    when_not_to_use: AntiPatternCriteria
    advanced: AdvancedScenarios
    alternatives: List[str]
    complexity_score: int  # 1-10, how complex the pattern is to implement
    learning_difficulty: int  # 1-10, how hard it is to understand


# Knowledge Base - Structured data from extracted notebook analysis
PATTERN_KNOWLEDGE: Dict[str, PatternKnowledge] = {
    "singleton": PatternKnowledge(
        name="Singleton Pattern",
        category="creational",
        description="Ensures a class has only one instance with global access",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "single instance",
                "only one",
                "global access",
                "shared state",
                "database connection",
                "configuration",
                "logging",
                "cache",
            ],
            thresholds={
                "expensive_creation": 1,  # If object creation is expensive
                "global_access_points": 2,  # If accessed from 2+ places
            },
            use_cases=[
                "Database connections - expensive to create, should be shared",
                "Configuration settings - one source of truth needed",
                "Logging systems - centralized logging required",
                "Caching mechanisms - shared cache across application",
            ],
            benefits=[
                "Controlled access to sole instance",
                "Reduced memory footprint",
                "Global access point",
                "Lazy initialization",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "just want global variables",
                "testing is important",
                "multiple instances later",
                "simple objects",
                "data models",
                "user objects",
                "entity classes",
            ],
            scenarios_to_avoid=[
                "You just want global variables - Use modules instead",
                "Testing is important - Singletons are hard to test and mock",
                "You might need multiple instances later - Don't paint yourself into a corner",
                "Simple objects - Don't over-engineer basic data structures",
                "Data models - User, Product, Order should NOT be singletons",
            ],
            better_alternatives=[
                "Module-level variables for simple global state",
                "Dependency injection for better testability",
                "Configuration objects passed as parameters",
                "Context managers for resource control",
            ],
            common_mistakes=[
                "Not handling thread safety in concurrent environments",
                "Using for data objects (User, Product entities)",
                "Overuse - creating singletons when regular classes suffice",
                "Making everything singleton for 'consistency'",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            Use threading.Lock() for multi-threaded applications:
            - Double-check locking pattern: Check instance exists, acquire lock, check again
            - Performance consideration: First check without lock for efficiency
            - Separate locks for different operations if needed
            """,
            performance_implications="""
            - Lazy initialization can improve startup time
            - Thread-safe versions have small locking overhead
            - Consider eager initialization for heavily used singletons
            """,
            testing_challenges="""
            - Hard to mock for unit testing
            - State pollution between tests
            - Consider dependency injection alternatives
            - Use setUp/tearDown to reset singleton state
            """,
            optimization_tips="""
            - Use __new__ method for instance control
            - Consider metaclass approach for cleaner syntax
            - Implement proper __init__ guard with hasattr check
            """,
            enterprise_considerations="""
            - Document singleton lifecycle clearly
            - Consider configuration-driven creation
            - Plan for distributed systems (singletons don't scale across processes)
            """,
        ),
        alternatives=[
            "Module-level variables",
            "Dependency injection",
            "Monostate pattern",
            "Registry pattern",
        ],
        complexity_score=6,
        learning_difficulty=4,
    ),
    "factory": PatternKnowledge(
        name="Factory Pattern",
        category="creational",
        description="Creates objects without specifying their exact classes",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "create different types",
                "multiple classes",
                "configuration-driven",
                "switch implementations",
                "object creation",
                "similar classes",
            ],
            thresholds={
                "similar_classes": 3,  # 3+ similar classes doing same job
                "creation_complexity": 5,  # If creation logic > 5 lines
            },
            use_cases=[
                "3+ similar classes that do the same job differently",
                "Complex object creation requiring multiple steps or decisions",
                "Configuration-driven creation - object type depends on config",
                "Need to switch implementations at runtime",
            ],
            benefits=[
                "Decouples object creation from usage",
                "Easy to add new types without changing client code",
                "Centralizes creation logic",
                "Supports polymorphism",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "only one class",
                "simple object creation",
                "over-engineering",
                "performance critical",
                "just in case",
            ],
            scenarios_to_avoid=[
                "Only one class - Don't create factory for just one type",
                "Simple object creation - If MyClass() is simple enough",
                "Over-engineering - Don't add factories 'just in case'",
                "Performance critical sections - Factories add small overhead",
            ],
            better_alternatives=[
                "Function parameters for small variations",
                "Enums with switch statements for fixed options",
                "Configuration files for simple behavior changes",
                "Direct instantiation for simple cases",
            ],
            common_mistakes=[
                "Creating factory for single class",
                "Adding factory complexity before it's needed",
                "Not using polymorphism effectively",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Factory methods should be thread-safe if called concurrently
            - Consider caching created objects with proper synchronization
            - Abstract Factory pattern needs thread-safe family switching
            """,
            performance_implications="""
            - Small overhead from factory method calls
            - Consider object pooling for expensive objects
            - Cache factories themselves if creation is expensive
            """,
            testing_challenges="""
            - Mock factory for testing client code
            - Test each factory method separately
            - Verify correct type is created for each input
            """,
            optimization_tips="""
            - Use Simple Factory for basic object creation
            - Factory Method when subclasses decide what to create
            - Abstract Factory for families of related products
            """,
            enterprise_considerations="""
            - Document which factory to use for each scenario
            - Consider plugin architecture with factory registration
            - Plan for dependency injection integration
            """,
        ),
        alternatives=[
            "Direct instantiation",
            "Builder pattern for complex construction",
            "Prototype pattern for cloning",
            "Service locator pattern",
        ],
        complexity_score=5,
        learning_difficulty=3,
    ),
    "observer": PatternKnowledge(
        name="Observer Pattern",
        category="behavioral",
        description="Defines one-to-many dependency between objects for automatic notifications",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "subscribe",
                "notify",
                "listen",
                "event",
                "update",
                "broadcast",
                "model-view",
                "real-time",
                "multiple listeners",
                "one-to-many",
            ],
            thresholds={
                "observers": 2,  # 2+ objects need to be notified
                "event_types": 1,  # Any event-driven scenario
                "update_frequency": 1,  # Regular updates needed
            },
            use_cases=[
                "Model-View architectures - views update when model changes",
                "Event-driven systems - user actions, system events",
                "Real-time updates - stock prices, chat, live dashboards",
                "One-to-many relationships - one subject, many observers",
            ],
            benefits=[
                "Loose coupling between subject and observers",
                "Dynamic relationships - add/remove observers at runtime",
                "Broadcast communication",
                "Supports event-driven architectures",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "simple data binding",
                "performance critical",
                "complex update sequences",
                "only one observer",
                "order dependencies",
            ],
            scenarios_to_avoid=[
                "Simple data binding - direct references might be simpler",
                "Performance critical code - observer pattern adds notification overhead",
                "Complex update sequences - order dependencies make it confusing",
                "Only one observer - direct method calls are clearer",
            ],
            better_alternatives=[
                "Direct method calls for single observer",
                "Callback functions for simple notifications",
                "Event queues for decoupled async communication",
                "Property setters for simple data binding",
            ],
            common_mistakes=[
                "Forgetting to unsubscribe - leads to memory leaks",
                "Circular dependencies - Observer A updates Observer B which updates A",
                "Complex update chains - hard to debug event propagation",
                "Not considering notification order",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Thread-safe notifications: protect observer list with locks
            - Separate lock for data: don't block notifications while updating
            - Async event handling: consider event queues for complex scenarios
            - Weak references to prevent memory leaks in threaded environments
            """,
            performance_implications="""
            - Push vs Pull models: Push is efficient, Pull is flexible
            - Large observer lists: consider asynchronous notifications
            - Memory leaks: ensure observers are properly removed
            - Event filtering to reduce unnecessary notifications
            """,
            testing_challenges="""
            - Mock observers for testing subject behavior
            - Test observer registration/unregistration
            - Verify notification order if it matters
            - Test memory cleanup (no lingering references)
            """,
            optimization_tips="""
            - Use weak references to prevent memory leaks
            - Implement event filtering for performance
            - Consider async notifications for non-critical updates
            - Batch notifications when possible
            """,
            enterprise_considerations="""
            - Document event contracts and data structures
            - Consider event sourcing for audit trails
            - Plan for distributed observers (message queues)
            - Implement proper error handling in notifications
            """,
        ),
        alternatives=[
            "Callback functions",
            "Event queues/message brokers",
            "Reactive programming (RxPY)",
            "Signals/slots mechanism",
        ],
        complexity_score=6,
        learning_difficulty=5,
    ),
    "strategy": PatternKnowledge(
        name="Strategy Pattern",
        category="behavioral",
        description="Defines family of algorithms and makes them interchangeable",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "multiple algorithms",
                "different ways",
                "switch algorithm",
                "runtime selection",
                "eliminate conditionals",
                "A/B testing",
            ],
            thresholds={
                "algorithms": 3,  # 3+ algorithms for same problem
                "conditional_lines": 10,  # Replace if/elif chains >10 lines
                "algorithm_complexity": 5,  # Each algorithm >5 lines
            },
            use_cases=[
                "3+ algorithms for the same problem (sorting, compression)",
                "Runtime algorithm switching based on data or user preference",
                "Eliminating conditionals - replace long if/else chains",
                "A/B testing - easily switch between implementations",
            ],
            benefits=[
                "Easy to add new algorithms",
                "Runtime algorithm selection",
                "Eliminates conditional statements",
                "Each algorithm can be tested separately",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "only one algorithm",
                "simple variations",
                "algorithms rarely change",
                "performance critical",
                "two simple cases",
            ],
            scenarios_to_avoid=[
                "Only one algorithm - don't create strategies for single implementations",
                "Simple variations - use parameters instead of separate strategies",
                "Algorithms rarely change - if you'll never switch, don't add overhead",
                "Performance critical - strategy pattern adds method call overhead",
            ],
            better_alternatives=[
                "Function parameters for small variations",
                "Configuration objects for behavior customization",
                "Template methods for algorithms with similar structure",
                "Simple if/else for 2-3 cases",
            ],
            common_mistakes=[
                "Creating strategy for single algorithm",
                "Not making strategies truly interchangeable",
                "Over-engineering simple conditional logic",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Strategies should be stateless for thread safety
            - If state needed, ensure proper synchronization
            - Strategy selection logic must be thread-safe
            """,
            performance_implications="""
            - Small overhead from strategy method calls
            - Consider caching strategy instances
            - Profile different strategies for performance comparison
            """,
            testing_challenges="""
            - Test each strategy individually
            - Mock strategies for testing context
            - Test strategy selection logic
            - Performance testing for strategy comparison
            """,
            optimization_tips="""
            - Data-driven selection: choose based on input characteristics
            - Smart strategy selection: automatic choice based on context
            - Combine with Factory pattern for strategy creation
            """,
            enterprise_considerations="""
            - Document strategy selection criteria
            - Consider configuration-driven strategy selection
            - Plan for strategy versioning and backwards compatibility
            """,
        ),
        alternatives=[
            "Function pointers/higher-order functions",
            "Template method pattern",
            "State pattern for behavior changes",
            "Command pattern for action selection",
        ],
        complexity_score=4,
        learning_difficulty=3,
    ),
    "command": PatternKnowledge(
        name="Command Pattern",
        category="behavioral",
        description="Encapsulates requests as objects to parameterize and queue operations",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "undo",
                "redo",
                "queue",
                "macro",
                "log operations",
                "parameterize objects",
                "decouple invoker",
                "store operations",
            ],
            thresholds={
                "operations_to_track": 1,  # Any operation that needs undo/logging
                "macro_commands": 2,  # 2+ commands to combine
                "queue_size": 1,  # Any queuing requirement
            },
            use_cases=[
                "Undo/redo operations - commands store state for reversal",
                "Macro recording - combine multiple commands",
                "Queue operations - store commands for later execution",
                "Logging and auditing - track all operations performed",
            ],
            benefits=[
                "Decouples invoker from receiver",
                "Commands can be stored and queued",
                "Supports undo/redo functionality",
                "Easy to create macro commands",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "simple operations",
                "no undo needed",
                "performance critical",
                "tight coupling acceptable",
                "basic getters",
            ],
            scenarios_to_avoid=[
                "Simple operations - don't create commands for basic method calls",
                "No undo needed - if operations are irreversible and logging not needed",
                "Performance critical - command objects add overhead",
                "Tight coupling acceptable - when invoker can directly call receiver",
            ],
            better_alternatives=[
                "Direct method calls for simple operations",
                "Function pointers for parameterization",
                "Event systems for decoupling",
                "Transaction objects for complex operations",
            ],
            common_mistakes=[
                "Creating commands for every operation",
                "Not implementing proper undo logic",
                "Making commands too granular",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Commands should be immutable for thread safety
            - Command queues need proper synchronization
            - Undo stack access must be thread-safe
            """,
            performance_implications="""
            - Command objects add memory overhead
            - Consider object pooling for frequently used commands
            - Limit undo history size to prevent memory issues
            """,
            testing_challenges="""
            - Test command execution and undo separately
            - Mock receivers for testing command logic
            - Test macro command composition
            """,
            optimization_tips="""
            - Use for complex operations that need undo/redo
            - Overkill for simple actions like getters/setters
            - Valuable for GUI applications with menu/button actions
            """,
            enterprise_considerations="""
            - Document command contracts and side effects
            - Consider command versioning for system evolution
            - Plan for command serialization and persistence
            """,
        ),
        alternatives=[
            "Direct method calls",
            "Function objects/lambdas",
            "Event sourcing",
            "Transaction scripts",
        ],
        complexity_score=6,
        learning_difficulty=5,
    ),
    "builder": PatternKnowledge(
        name="Builder Pattern",
        category="creational",
        description="Constructs complex objects step by step with fluent interface",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "complex construction",
                "many parameters",
                "optional parameters",
                "step by step",
                "fluent interface",
                "validation during construction",
            ],
            thresholds={
                "constructor_parameters": 5,  # 5+ constructor parameters
                "optional_parameters": 3,  # 3+ optional parameters
                "construction_steps": 3,  # 3+ construction steps
            },
            use_cases=[
                "Objects with many optional parameters (5+ parameters)",
                "Step-by-step construction with validation at each step",
                "Immutable objects that need complex construction",
                "Objects where construction order matters",
            ],
            benefits=[
                "Readable object construction",
                "Handles optional parameters elegantly",
                "Validates during construction",
                "Supports fluent interface",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "few properties",
                "simple construction",
                "no variation in process",
                "performance critical",
                "immutable not needed",
            ],
            scenarios_to_avoid=[
                "Few properties - don't use builder for 2-3 simple parameters",
                "Simple construction - regular constructor is clearer",
                "No variation in process - builder adds unnecessary complexity",
                "Performance critical - builder adds method call overhead",
            ],
            better_alternatives=[
                "Regular constructors for simple objects",
                "Dataclasses with defaults for data containers",
                "Factory methods for complex creation logic",
                "Keyword arguments for optional parameters",
            ],
            common_mistakes=[
                "Using builder for simple objects",
                "Not validating during construction",
                "Making builder mutable when building immutable objects",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Builders should not be shared between threads
            - Built objects can be immutable for thread safety
            - Consider builder pools for performance
            """,
            performance_implications="""
            - Method chaining adds small overhead
            - Consider direct construction for performance-critical paths
            - Builder object creation adds memory overhead
            """,
            testing_challenges="""
            - Test builder validation at each step
            - Test different construction paths
            - Verify immutability of built objects
            """,
            optimization_tips="""
            - Use for complex objects with validation requirements
            - Consider fluent interface for better readability
            - Implement proper validation and error handling
            """,
            enterprise_considerations="""
            - Document required vs optional construction steps
            - Consider builder inheritance for object families
            - Plan for configuration-driven object construction
            """,
        ),
        alternatives=[
            "Dataclasses with defaults",
            "Factory methods",
            "Keyword arguments",
            "Configuration objects",
        ],
        complexity_score=5,
        learning_difficulty=4,
    ),
    "adapter": PatternKnowledge(
        name="Adapter Pattern",
        category="structural",
        description="Allows incompatible interfaces to work together",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.SIMPLE,
            indicators=[
                "incompatible interfaces",
                "third-party integration",
                "legacy system",
                "cannot modify",
                "interface mismatch",
                "wrapper needed",
            ],
            thresholds={
                "interface_differences": 1,  # Any interface incompatibility
                "modification_restrictions": 1,  # Cannot modify existing code
            },
            use_cases=[
                "Incompatible interfaces between existing classes",
                "Third-party library integration with different interface",
                "Legacy system integration without modifying old code",
                "Making old interface work with new system",
            ],
            benefits=[
                "Reuses existing code without modification",
                "Separates interface concerns from business logic",
                "Allows incompatible classes to work together",
                "Follows open/closed principle",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "interfaces already compatible",
                "can modify existing classes",
                "too complex adaptation",
                "performance critical",
            ],
            scenarios_to_avoid=[
                "Interfaces already compatible - no adapter needed",
                "Can modify existing classes - direct modification is simpler",
                "Too complex adaptation - consider redesigning interfaces",
                "Performance critical - adapter adds indirection overhead",
            ],
            better_alternatives=[
                "Direct interface modification if possible",
                "Interface inheritance for compatible types",
                "Composition for simple wrapping",
                "Facade pattern for complex subsystem integration",
            ],
            common_mistakes=[
                "Over-adapting simple interface differences",
                "Not handling all methods of adapted interface",
                "Making adapter do too much business logic",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Adapter should delegate threading concerns to adaptee
            - Consider thread-safe adaptation if adaptee is not thread-safe
            - Synchronization needed if adapter maintains state
            """,
            performance_implications="""
            - Adds one level of indirection
            - Consider caching adapted results if expensive
            - Object adapter vs class adapter performance trade-offs
            """,
            testing_challenges="""
            - Test adapter with mock adaptee
            - Verify all interface methods are properly adapted
            - Test error handling and edge cases
            """,
            optimization_tips="""
            - Keep adapter thin - delegate to adaptee
            - Consider two-way adapters for bidirectional compatibility
            - Object adapter for runtime flexibility, class adapter for compile-time
            """,
            enterprise_considerations="""
            - Document adaptation contracts and limitations
            - Consider adapter versioning for API evolution
            - Plan for multiple adapter implementations
            """,
        ),
        alternatives=[
            "Direct interface modification",
            "Facade pattern",
            "Wrapper functions",
            "Interface inheritance",
        ],
        complexity_score=3,
        learning_difficulty=2,
    ),
    "decorator": PatternKnowledge(
        name="Decorator Pattern",
        category="structural",
        description="Adds behavior to objects dynamically without altering structure",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "add responsibilities",
                "multiple features",
                "transparent enhancement",
                "composable behaviors",
                "avoid inheritance explosion",
            ],
            thresholds={
                "optional_features": 3,  # 3+ optional features to add
                "feature_combinations": 4,  # 4+ possible combinations
                "inheritance_levels": 3,  # Would need 3+ inheritance levels
            },
            use_cases=[
                "Add responsibilities dynamically without inheritance",
                "Multiple feature combinations - avoid class explosion",
                "Transparent enhancement - client doesn't know about decoration",
                "Composable behaviors - stack multiple decorators",
            ],
            benefits=[
                "More flexible than inheritance",
                "Adds responsibilities at runtime",
                "Supports composition of behaviors",
                "Follows single responsibility principle",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "component interface too complex",
                "fixed combinations",
                "performance critical",
                "simple objects",
            ],
            scenarios_to_avoid=[
                "Component interface is too complex - decorators need to implement all methods",
                "Fixed set of combinations - regular inheritance might be simpler",
                "Performance critical - each decorator adds indirection layer",
                "Simple objects - don't over-engineer basic data",
            ],
            better_alternatives=[
                "Inheritance for fixed combinations",
                "Composition for simple wrapping",
                "Mixins for multiple inheritance languages",
                "Strategy pattern for algorithmic variations",
            ],
            common_mistakes=[
                "Making decorators too complex",
                "Not maintaining component interface properly",
                "Using for simple feature additions",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Decorators should be thread-safe if component is thread-safe
            - Consider decorator state synchronization
            - Nested decorators may need coordinated locking
            """,
            performance_implications="""
            - Each decorator level adds method call overhead
            - Consider decorator ordering for performance
            - May increase memory usage with deep nesting
            """,
            testing_challenges="""
            - Test individual decorators separately
            - Test decorator combinations and stacking
            - Mock underlying components for isolation
            """,
            optimization_tips="""
            - 3+ optional features make decorator valuable
            - Avoid for simple objects with basic decorations
            - Consider inheritance for 2-3 features
            """,
            enterprise_considerations="""
            - Document decorator composition rules
            - Consider decorator registration/discovery mechanisms
            - Plan for decorator configuration and ordering
            """,
        ),
        alternatives=[
            "Inheritance hierarchies",
            "Composition",
            "Mixins",
            "Aspect-oriented programming",
        ],
        complexity_score=7,
        learning_difficulty=6,
    ),
    "state": PatternKnowledge(
        name="State Pattern",
        category="behavioral",
        description="Allows object to alter behavior when internal state changes",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "behavior depends on state",
                "finite state machine",
                "state transitions",
                "workflow",
                "different behavior",
                "state-dependent",
            ],
            thresholds={
                "states": 3,  # 3+ distinct states
                "state_transitions": 3,  # 3+ possible transitions
                "behavior_differences": 5,  # Significant behavior differences
            },
            use_cases=[
                "Behavior depends on object state (game character abilities)",
                "Complex conditionals based on state - replace if/else chains",
                "Finite state machines - clear states and transitions",
                "Workflow systems - document approval, order processing",
            ],
            benefits=[
                "Eliminates complex conditional statements",
                "Makes state transitions explicit",
                "Easy to add new states",
                "Each state encapsulates its behavior",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "few states",
                "simple behavior",
                "rare state changes",
                "simple logic",
                "performance critical",
            ],
            scenarios_to_avoid=[
                "Few states with simple behavior - enum + match might be simpler",
                "Rare state changes - overhead not justified",
                "Simple logic - don't over-engineer basic conditionals",
                "Performance critical - state objects add overhead",
            ],
            better_alternatives=[
                "Enum + match statements for simple states",
                "Strategy pattern for algorithmic variations",
                "Simple boolean flags for binary states",
                "Command pattern for action-based behavior",
            ],
            common_mistakes=[
                "Using for simple boolean states",
                "Not handling all state transitions properly",
                "Making states too granular",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - State transitions must be atomic in concurrent environments
            - Consider state change notifications for observers
            - Guard state access with proper synchronization
            """,
            performance_implications="""
            - State object creation overhead
            - Consider state object pooling
            - Method delegation adds small overhead
            """,
            testing_challenges="""
            - Test each state behavior individually
            - Test state transitions and edge cases
            - Verify invalid transition handling
            """,
            optimization_tips="""
            - Use when you have 3+ states with different behaviors
            - Consider if/else for 2-3 simple states
            - Valuable for game entities, workflow systems
            """,
            enterprise_considerations="""
            - Document state machine diagrams
            - Consider state persistence and restoration
            - Plan for state machine configuration and validation
            """,
        ),
        alternatives=[
            "Enum + match statements",
            "Strategy pattern",
            "Boolean flags",
            "Finite state machine libraries",
        ],
        complexity_score=7,
        learning_difficulty=6,
    ),
    "repository": PatternKnowledge(
        name="Repository Pattern",
        category="behavioral",
        description="Centralizes data access logic and provides uniform interface",
        when_to_use=PatternCriteria(
            minimum_complexity=ComplexityLevel.MODERATE,
            indicators=[
                "data access",
                "multiple data sources",
                "testability",
                "domain logic",
                "centralize queries",
                "abstract storage",
            ],
            thresholds={
                "data_sources": 1,  # Any data access needs
                "complex_queries": 3,  # 3+ different query types
                "entities": 2,  # 2+ entity types with data access
            },
            use_cases=[
                "Centralizing data access logic across application",
                "Supporting multiple data sources (database, file, API)",
                "Improving testability by abstracting data layer",
                "Domain-driven design - isolate domain from infrastructure",
            ],
            benefits=[
                "Centralizes data access logic",
                "Easy to switch data sources",
                "Improves testability with mock repositories",
                "Separates domain logic from data access",
            ],
        ),
        when_not_to_use=AntiPatternCriteria(
            red_flags=[
                "simple applications",
                "ORM already provides abstraction",
                "unjustified overhead",
                "single data source",
            ],
            scenarios_to_avoid=[
                "Simple applications - CRUD operations don't need repository layer",
                "ORM already provides abstraction - don't add another layer",
                "Unjustified overhead - repositories add complexity",
                "Single data source with no switching plans",
            ],
            better_alternatives=[
                "Direct ORM usage for simple applications",
                "Data Access Objects (DAO) for simple CRUD",
                "Active Record pattern for simple models",
                "Query builders for dynamic queries",
            ],
            common_mistakes=[
                "Making repository too generic (generic repository anti-pattern)",
                "Putting business logic in repository",
                "Not using Unit of Work pattern with repositories",
            ],
        ),
        advanced=AdvancedScenarios(
            threading_considerations="""
            - Repository implementations must be thread-safe
            - Consider connection pooling for database repositories
            - Cache synchronization across threads
            """,
            performance_implications="""
            - Additional abstraction layer overhead
            - Consider caching strategies within repository
            - Bulk operations for better performance
            """,
            testing_challenges="""
            - Mock repositories for unit testing
            - Integration tests with real data sources
            - Test data consistency and transactions
            """,
            optimization_tips="""
            - Use for complex queries and multiple data sources
            - Consider Unit of Work pattern for transaction management
            - Implement proper caching strategies
            """,
            enterprise_considerations="""
            - Document repository contracts and capabilities
            - Consider repository composition for complex scenarios
            - Plan for distributed data sources and eventual consistency
            """,
        ),
        alternatives=[
            "Direct ORM usage",
            "Data Access Objects (DAO)",
            "Active Record pattern",
            "Query builders",
        ],
        complexity_score=6,
        learning_difficulty=5,
    ),
}


def get_pattern_by_name(pattern_name: str) -> Optional[PatternKnowledge]:
    """Get pattern knowledge by name (case-insensitive)"""
    return PATTERN_KNOWLEDGE.get(pattern_name.lower())


def get_patterns_by_category(category: str) -> List[PatternKnowledge]:
    """Get all patterns in a specific category"""
    return [p for p in PATTERN_KNOWLEDGE.values() if p.category == category]


def find_patterns_by_indicators(indicators: List[str]) -> List[Tuple[str, float]]:
    """
    Find patterns that match given indicators with confidence scores
    Returns list of (pattern_name, confidence_score) tuples
    """
    results = []

    for pattern_name, knowledge in PATTERN_KNOWLEDGE.items():
        score = 0.0
        total_indicators = len(knowledge.when_to_use.indicators)

        for indicator in indicators:
            indicator_lower = indicator.lower()
            for pattern_indicator in knowledge.when_to_use.indicators:
                if indicator_lower in pattern_indicator.lower():
                    score += 1.0 / total_indicators

        if score > 0:
            results.append((pattern_name, min(score, 1.0)))

    return sorted(results, key=lambda x: x[1], reverse=True)


def check_anti_patterns(description: str) -> List[Tuple[str, str]]:
    """
    Check for anti-pattern indicators in problem description
    Returns list of (pattern_name, warning_message) tuples
    """
    warnings = []
    description_lower = description.lower()

    for pattern_name, knowledge in PATTERN_KNOWLEDGE.items():
        for red_flag in knowledge.when_not_to_use.red_flags:
            if red_flag.lower() in description_lower:
                warning = (
                    f"⚠️ Potential {pattern_name} anti-pattern detected: {red_flag}"
                )
                warnings.append((pattern_name, warning))

    return warnings


def get_complexity_recommendation(
    pattern_name: str, scenario_complexity: ComplexityLevel
) -> str:
    """Get recommendation based on scenario complexity vs pattern requirements"""
    knowledge = get_pattern_by_name(pattern_name)
    if not knowledge:
        return "Pattern not found"

    if scenario_complexity.value < knowledge.when_to_use.minimum_complexity.value:
        return f"⚠️ {knowledge.name} might be overkill for {scenario_complexity.value} scenarios"
    else:
        return f"✅ {knowledge.name} is appropriate for {scenario_complexity.value} scenarios"
