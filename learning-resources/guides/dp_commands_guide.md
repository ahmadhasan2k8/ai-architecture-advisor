# Design Pattern Commands Guide

Complete guide to using the `dp::` namespaced commands for intelligent design pattern recommendations.

## Commands Overview

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/dp::analyze` | Comprehensive pattern analysis | Complex scenarios, multiple pattern candidates |
| `/dp::check` | Quick pattern validation | Verify specific pattern choice |
| `/dp::refactor` | Code analysis for opportunities | Existing code improvement |
| `/dp::validate` | Anti-pattern detection | Prevent pattern misuse |

---

## `/dp::analyze` - Comprehensive Pattern Analysis

**Purpose**: Deep analysis using sequential thinking for complex pattern decisions

### When to Use
- Multiple pattern candidates exist
- Unclear which pattern fits best
- Need detailed reasoning and trade-offs
- Complex scenarios with many factors

### Syntax
```
/dp::analyze <problem description>
```

### Examples

#### Example 1: General Problem Description
```
/dp::analyze I need a system where different UI components update when user data changes, and I want to support real-time notifications
```

**Expected Response**:
```
🧠 Analyzing using sequential thinking...

Thought 1: Problem Understanding
- Multiple UI components need updates
- Data change notifications required
- Real-time requirement suggests performance consideration

Thought 2: Complexity Assessment  
- One-to-many relationship (data → UI components)
- Dynamic subscription likely needed
- Real-time adds performance constraints

Thought 3: Pattern Candidates
- Observer Pattern: Strong match for one-to-many notifications
- Event Bus: Alternative for complex event routing
- Simple callbacks: Simpler but less flexible

Thought 4: Repository Knowledge Check
- Observer threshold: 2+ observers ✓
- Real-time considerations: async notifications recommended
- Thread safety: needed for real-time systems

Thought 5: Performance Analysis
- Observer adds notification overhead
- Real-time requirement favors efficient implementation
- Consider async notifications for non-critical updates

Recommendation: **Observer Pattern** (Confidence: HIGH)
- Implement with async notifications for performance
- Use typed events for better maintainability
- Consider event filtering to reduce unnecessary updates

Alternative: Event bus library if events become complex
```

#### Example 2: Specific Technical Scenario
```
/dp::analyze I have a payment processing system that needs to handle credit cards, PayPal, crypto, and bank transfers. Each has different fee structures and validation rules. We'll likely add more payment methods.
```

**Expected Response**:
```
🧠 Sequential Analysis: Payment Processing System

Thought 1: Problem Breakdown
- 4 payment methods with different logic
- Different fee structures and validation per method  
- Expected growth (more payment methods)

Thought 2: Complexity Indicators
- 4+ algorithms ✓ (exceeds Strategy threshold of 3)
- Runtime selection needed ✓
- Expected growth ✓
- Complex logic per method ✓

Thought 3: Pattern Evaluation
- Strategy Pattern: Perfect fit for algorithm families
- Factory Pattern: Could help with payment processor creation
- Simple if/else: Would work but hard to extend

Thought 4: Repository Guidance
- Strategy threshold: 3+ algorithms ✓
- Use case: "different payment processing" ✓
- Benefits: Easy to add new methods, separate testing

Thought 5: Advanced Considerations
- Consider Strategy + Factory combination
- Each strategy should be stateless for thread safety
- Validation can be part of each strategy

Recommendation: **Strategy Pattern** (Confidence: CRITICAL)
1. Create PaymentProcessor interface
2. Implement strategy for each payment method
3. Use PaymentService as context for strategy selection
4. Consider StrategyFactory for processor creation

Expected ROI: High - Easy addition of new payment methods
```

### Advanced Usage Tips

1. **Be Specific**: Include requirements, constraints, and context
2. **Mention Scale**: "handles 1000 requests/second" affects recommendations
3. **Include Growth Plans**: "will add more X later" influences pattern choice
4. **Specify Constraints**: "team is junior" or "performance critical" matters

---

## `/dp::check` - Quick Pattern Validation

**Purpose**: Fast verification of pattern appropriateness for specific scenarios

### When to Use
- You have a pattern in mind
- Need quick validation
- Want threshold-based assessment
- Checking for anti-patterns

### Syntax
```
/dp::check <pattern name> for <scenario>
```

### Examples

#### Example 1: Singleton Validation
```
/dp::check singleton for database connection pool in multi-threaded web application
```

**Expected Response**:
```
✅ Singleton Pattern Assessment

Scenario Analysis:
- Database connection pool ✓ (appropriate use case)
- Multi-threaded application ✓ (thread safety needed)
- Expensive resource ✓ (database connections)

Validation Result: **APPROPRIATE** 
Confidence: HIGH

Requirements Met:
✓ Expensive object creation
✓ Global access needed  
✓ Single instance logical

Thread Safety Note: ⚠️ CRITICAL
- Must implement double-check locking
- Protect connection pool operations
- Consider connection pool library

Implementation Guidance:
- Use thread-safe singleton implementation
- Initialize pool lazily or eagerly based on usage
- Add connection health checks
- Implement proper cleanup

Repository Reference: See notebooks/01_singleton_pattern.ipynb for thread-safe implementation
```

#### Example 2: Anti-Pattern Detection
```
/dp::check singleton for User model class to avoid multiple instances
```

**Expected Response**:
```
❌ ANTI-PATTERN DETECTED

⚠️ Critical Issue: Singleton for Data Model
This is a well-known anti-pattern that should be avoided.

Problems:
- User entities should have multiple instances (multiple users exist)
- Makes testing extremely difficult
- Violates single responsibility principle
- Creates hidden global dependencies

Better Alternatives:
1. **Regular Class**: Use normal User class with multiple instances
2. **Repository Pattern**: Centralize user data access logic
3. **Identity Map**: Prevent duplicate loading of same user
4. **Dependency Injection**: Pass user instances explicitly

Example:
```python
# ❌ DON'T DO THIS
class User(metaclass=SingletonMeta): ...

# ✅ DO THIS
class User:
    def __init__(self, id, name, email): ...

class UserRepository:
    def find_by_id(self, user_id): ...
```

Confidence: CRITICAL - This is definitely an anti-pattern
```

#### Example 3: Borderline Case
```
/dp::check strategy for handling 2 different export formats (PDF and Excel)
```

**Expected Response**:
```
⚠️ Borderline Pattern Usage

Scenario Analysis:
- 2 export formats (below Strategy threshold of 3)
- Different algorithms ✓
- Potential for growth ?

Assessment: **CONSIDER ALTERNATIVES**
Confidence: MEDIUM

Threshold Analysis:
❌ Below 3 algorithm threshold (current: 2)
✓ Different implementations per format
? Growth potential unclear

Recommendations:

**If no growth expected:**
```python
def export_report(data, format_type):
    if format_type == 'pdf':
        return export_to_pdf(data)
    elif format_type == 'excel':
        return export_to_excel(data)
    else:
        raise ValueError(f"Unknown format: {format_type}")
```

**If growth likely (adding Word, CSV, etc.):**
- Implement Strategy pattern now for future expansion
- Strategy becomes valuable at 3+ formats

Decision Factors:
1. Will you add more formats? → Use Strategy
2. Is export logic complex (>10 lines each)? → Use Strategy  
3. Need runtime format switching? → Use Strategy
4. Simple one-line library calls? → Keep simple

Repository Reference: See strategy pattern examples for export systems
```

---

## `/dp::refactor` - Code Analysis for Pattern Opportunities

**Purpose**: Analyze existing code files for pattern implementation opportunities

### When to Use
- Reviewing existing codebase
- Looking for refactoring opportunities
- Code quality improvement
- Technical debt reduction

### Syntax
```
/dp::refactor <file_path>
/dp::refactor <directory_path>
```

### Examples

#### Example 1: Single File Analysis
```
/dp::refactor src/payment_processor.py
```

**Expected Response**:
```
🔍 Code Analysis: src/payment_processor.py

Found 3 Pattern Opportunities:

## 1. Strategy Pattern (Priority: 0.85)
**Lines 34-67**: Long if/elif chain for payment processing
- **Current**: 15-line conditional with 4 payment types
- **Issue**: Hard to add new payment methods
- **Impact**: High | **Effort**: Medium

**Refactoring Suggestion**:
```python
# Before (current code)
def process_payment(type, amount):
    if type == "credit_card":
        # 15 lines of processing
    elif type == "paypal":
        # 12 lines of processing

# After (strategy pattern)  
class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount): pass

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        # Focused credit card logic
```

**Migration Steps**:
1. Extract each payment type to separate class
2. Create PaymentProcessor interface
3. Update client code to use strategy selection
4. Add new payment types as separate strategies

## 2. Factory Pattern (Priority: 0.65)
**Lines 89-103**: Object creation based on configuration
- **Current**: Multiple isinstance() checks
- **Benefit**: Centralized creation logic

## 3. Builder Pattern (Priority: 0.45)  
**Lines 23-31**: PaymentConfig constructor with 8 parameters
- **Current**: Long parameter list in constructor
- **Benefit**: More readable configuration setup

**Next Steps**:
1. Start with Strategy pattern (highest impact)
2. Implement Factory for processor creation
3. Consider Builder for complex configurations

**Estimated Effort**: 4-6 hours for Strategy implementation
**ROI**: High - Easy to add new payment methods
```

#### Example 2: Directory Analysis
```
/dp::refactor src/
```

**Expected Response**:
```
📊 Repository Analysis: src/

**Overview**:
- Files analyzed: 12
- Total opportunities: 8
- High priority: 3
- Anti-patterns detected: 1

## Anti-Pattern Alert ⚠️
**src/models/user.py:15** - Singleton for User model
- **Issue**: Data models should not be singletons
- **Fix**: Convert to regular class
- **Priority**: CRITICAL

## High-Priority Opportunities

### 1. Strategy Pattern in PaymentProcessor
**File**: src/services/payment.py:34
**Confidence**: HIGH | **ROI**: High
- Replace 4-way conditional with strategy classes
- Easy to add new payment methods

### 2. Observer Pattern in NotificationService  
**File**: src/services/notification.py:67
**Confidence**: MEDIUM | **ROI**: Medium
- Manual notification loops suggest Observer pattern
- Better for event-driven architecture

### 3. Factory Pattern in ReportGenerator
**File**: src/reports/generator.py:45
**Confidence**: MEDIUM | **ROI**: Medium
- Multiple report types suggest factory pattern

## Architectural Insights

**Complexity Assessment**: Medium
- 8 pattern opportunities suggest active development
- Anti-pattern needs immediate attention
- Focus on high-ROI improvements first

**Recommendations**:
1. Fix User singleton anti-pattern immediately
2. Implement Strategy pattern for payments (highest ROI)
3. Consider Observer for notification system
4. Review other opportunities after main fixes

**Effort Estimate**: 2-3 days for top priorities
```

---

## `/dp::validate` - Anti-Pattern Detection

**Purpose**: Detect and prevent common pattern misuse and overengineering

### When to Use
- Reviewing pattern proposals
- Checking for overengineering
- Validating architectural decisions
- Before implementing patterns

### Syntax
```
/dp::validate <pattern usage description>
```

### Examples

#### Example 1: Catching Overengineering
```
/dp::validate I want to implement the Factory pattern for creating User objects because it's a best practice
```

**Expected Response**:
```
⚠️ Potential Overengineering Detected

**Issue**: Factory pattern for simple object creation
**Risk Level**: MEDIUM

**Analysis**:
❌ "Because it's a best practice" is not a valid reason
❌ User objects typically don't need factory pattern
❌ Adds complexity without clear benefit

**Questions to Consider**:
1. Do you have multiple User types that need different creation logic?
2. Is User creation complex enough to warrant abstraction?  
3. Will you need to switch User implementations at runtime?

**If answers are NO**: Use direct instantiation
```python
# ✅ SIMPLE AND CLEAR
user = User(name="John", email="john@example.com")

# ❌ UNNECESSARY COMPLEXITY  
user = UserFactory.create("standard", name="John", email="john@example.com")
```

**When Factory WOULD be appropriate for Users**:
- Multiple user types (AdminUser, RegularUser, GuestUser)
- Complex validation/setup logic
- User type determined by external data
- Integration with external systems

**Recommendation**: Stick with direct instantiation unless you have specific complexity that justifies a factory.
```

#### Example 2: Singleton Misuse Detection
```
/dp::validate Using singleton pattern for all my service classes to ensure consistency across the application
```

**Expected Response**:
```
🚨 CRITICAL ANTI-PATTERN DETECTED

**Issue**: Singleton overuse for "consistency"
**Risk Level**: HIGH

**Major Problems**:
1. **Testing Nightmare**: Singletons make unit testing extremely difficult
2. **Hidden Dependencies**: Services can't be mocked or replaced
3. **Tight Coupling**: Creates implicit global dependencies
4. **Concurrency Issues**: Shared state across all operations

**"Consistency" is NOT a valid reason for Singleton**

**Better Alternatives**:

**1. Dependency Injection**:
```python
class OrderService:
    def __init__(self, payment_service: PaymentService, 
                 email_service: EmailService):
        self.payment_service = payment_service
        self.email_service = email_service

# Consistent instance management through DI container
services = ServiceContainer()
order_service = services.get(OrderService)
```

**2. Service Registry**:
```python
class ServiceRegistry:
    def __init__(self):
        self._services = {}
    
    def register(self, service_type, instance):
        self._services[service_type] = instance
    
    def get(self, service_type):
        return self._services[service_type]
```

**3. Module-Level Instances**:
```python
# services.py
payment_service = PaymentService()
email_service = EmailService()

# Other modules import and use
from services import payment_service
```

**Valid Singleton Use Cases**:
- Database connection pools
- Configuration managers
- Logging systems
- Resource managers (file handles, etc.)

**Rule of Thumb**: If you can imagine needing two instances for testing, don't use Singleton.
```

#### Example 3: Complexity Validation
```
/dp::validate Implementing Command pattern, Strategy pattern, Factory pattern, and Observer pattern in a simple todo application
```

**Expected Response**:
```
🚨 SEVERE OVERENGINEERING ALERT

**Issue**: Multiple complex patterns for simple application
**Risk Level**: CRITICAL

**Analysis**:
Todo applications are typically simple CRUD operations that don't justify complex patterns.

**Pattern Overuse Indicators**:
❌ 4 patterns for simple domain
❌ Patterns solving imaginary problems
❌ Complexity exceeds business requirements
❌ Following patterns "because they're good"

**Reality Check Questions**:
1. **Command Pattern**: Do you really need undo/redo for todos?
2. **Strategy Pattern**: How many todo algorithms do you have?
3. **Factory Pattern**: Are you creating many different todo types?
4. **Observer Pattern**: Do many systems need todo notifications?

**Recommended Simple Approach**:
```python
# Simple, clear, maintainable
class Todo:
    def __init__(self, title: str, description: str = ""):
        self.title = title
        self.description = description
        self.completed = False
        self.created_at = datetime.now()

class TodoService:
    def __init__(self):
        self.todos = []
    
    def add_todo(self, title: str, description: str = "") -> Todo:
        todo = Todo(title, description)
        self.todos.append(todo)
        return todo
    
    def complete_todo(self, todo_id: int) -> bool:
        # Simple completion logic
        pass
```

**When patterns WOULD be justified**:
- **Command**: If building collaborative todo app with undo/redo
- **Strategy**: If multiple todo sorting/filtering algorithms
- **Factory**: If todos have complex types (TaskTodo, EventTodo, etc.)
- **Observer**: If real-time sync across multiple clients

**Golden Rule**: Solve real problems, not imaginary ones.
Start simple. Add patterns when you hit actual limitations.

**Complexity Budget**: Simple apps should use 0-1 patterns maximum.
```

---

## Best Practices for Using dp:: Commands

### 1. Progressive Analysis
```
# Start simple
/dp::check strategy for payment processing

# If unclear, go deeper  
/dp::analyze payment processing system with multiple algorithms

# Check for problems
/dp::validate using strategy pattern for 2 payment types
```

### 2. Context Matters
Include relevant details:
- Team experience level
- Performance requirements  
- Growth expectations
- Current pain points

### 3. Validate Before Implementing
```
# Before implementing
/dp::validate implementing singleton for user session management

# During implementation
/dp::check singleton implementation for thread safety

# After implementation
/dp::refactor src/auth/session.py
```

### 4. Use Sequential Thinking for Complex Decisions
When multiple patterns could apply:
```
/dp::analyze I need a system that creates different types of reports, handles multiple output formats, and tracks generation history
```

This triggers sequential thinking to evaluate Factory + Strategy + Command combinations.

---

## Common Command Patterns

### Pattern Selection Workflow
1. **Quick Check**: `/dp::check <pattern> for <scenario>`
2. **If Uncertain**: `/dp::analyze <detailed problem description>`  
3. **Validate Decision**: `/dp::validate <proposed implementation>`
4. **Review Code**: `/dp::refactor <file/directory>`

### Anti-Pattern Prevention Workflow  
1. **Before Design**: `/dp::validate <architectural plan>`
2. **During Implementation**: `/dp::check <specific pattern decisions>`
3. **After Implementation**: `/dp::refactor <implemented code>`
4. **Periodic Review**: `/dp::refactor <entire codebase>`

### Learning Workflow
1. **Understand Problem**: `/dp::analyze <problem without suggesting pattern>`
2. **Learn Reasoning**: Review sequential thinking output
3. **Validate Understanding**: `/dp::check <pattern> for <your scenario>`
4. **Practice Recognition**: `/dp::refactor <existing code>`

---

## Integration with Repository Examples

All commands reference the repository's notebook examples:

- **Singleton**: `notebooks/01_singleton_pattern.ipynb`
- **Factory**: `notebooks/02_factory_pattern.ipynb`  
- **Observer**: `notebooks/03_observer_pattern.ipynb`
- **Strategy**: `notebooks/04_strategy_pattern.ipynb`
- **Decorator**: `notebooks/05_decorator_pattern.ipynb`
- **Command**: `notebooks/06_command_pattern.ipynb`
- **Repository**: `notebooks/07_repository_pattern.ipynb`
- **Builder**: `notebooks/08_builder_pattern.ipynb`
- **Adapter**: `notebooks/09_adapter_pattern.ipynb`
- **State**: `notebooks/10_state_pattern.ipynb`

Commands will provide links to relevant notebook sections for implementation details and examples.

---

## Troubleshooting

### Command Not Working?
1. Check command syntax: `/dp::command_name description`
2. Ensure repository knowledge is loaded
3. Provide sufficient context in description

### Unexpected Recommendations?
1. Use `/dp::validate` to double-check
2. Provide more specific requirements
3. Mention constraints (performance, team experience, etc.)

### Need More Detail?
1. Use `/dp::analyze` for complex scenarios
2. Ask for specific aspects: "focus on performance implications"
3. Reference repository examples for implementation details

Remember: These commands are designed to prevent overengineering while ensuring you don't miss beneficial pattern opportunities. When in doubt, they'll recommend the simpler solution.