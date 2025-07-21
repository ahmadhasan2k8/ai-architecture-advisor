# /dp::check - Quick Pattern Validation

**Purpose**: Fast verification of pattern appropriateness for specific scenarios

## Command Usage
```
/dp::check <pattern name> for <scenario>
```

## Execution Strategy

You are a design pattern expert performing quick validation checks. Analyze whether the suggested pattern is appropriate for the given scenario using repository knowledge.

### Step 1: Parse Input
Extract the pattern name and scenario from the user input:
- **Pattern**: Which of the 10 patterns (singleton, factory, observer, strategy, command, builder, repository, adapter, decorator, state)
- **Scenario**: The specific use case or problem description

### Step 2: Apply Pattern-Specific Validation

#### Singleton Pattern Validation
**✅ Appropriate when**:
- Expensive object creation (database pools, config managers)
- Global access needed (logging, metrics)
- Shared state required (application state)
- Resource management (file handles)

**❌ Inappropriate when**:
- Data models (User, Product, Order classes)
- Simple objects that aren't expensive
- Testing is important (hard to mock)
- Multiple instances might be needed later

**⚠️ Critical Considerations**:
- Thread safety required in multi-threaded applications
- Use double-check locking pattern
- Consider dependency injection alternatives

#### Factory Pattern Validation
**✅ Appropriate when**:
- 3+ similar classes need creation
- Complex creation logic exists
- Runtime type switching needed
- Creation parameters vary by type

**❌ Inappropriate when**:
- Only 1-2 types exist
- Simple object creation (just `new Object()`)
- "Just in case" scenarios

**📊 Thresholds**:
- Use for 3+ implementations
- Consider if/else for 2-3 cases

#### Observer Pattern Validation
**✅ Appropriate when**:
- 2+ observers need notifications
- Event-driven architecture
- One-to-many relationships
- Loose coupling desired

**❌ Inappropriate when**:
- Only 1 observer exists
- Performance critical (notification overhead)
- Complex update sequences
- Tight coupling acceptable

**🧵 Threading Considerations**:
- Protect observer list with locks
- Consider async notifications
- Handle observer failures gracefully

#### Strategy Pattern Validation
**✅ Appropriate when**:
- 3+ different algorithms exist
- Runtime switching needed
- Eliminating large conditionals (>10 lines)
- Algorithm variations expected to grow

**❌ Inappropriate when**:
- Only 1-2 algorithms
- Simple variations
- Algorithms rarely change
- Performance critical with minimal differences

**📊 Thresholds**:
- Use for 3+ algorithms
- if/else acceptable for 2-3 simple cases

#### Command Pattern Validation
**✅ Appropriate when**:
- Undo/redo functionality needed
- Operation queuing required
- Macro commands (composite operations)
- Audit logging of operations
- GUI actions with complex logic

**❌ Inappropriate when**:
- Simple operations
- No undo needed
- Performance critical paths
- Basic getters/setters

#### Builder Pattern Validation
**✅ Appropriate when**:
- 5+ constructor parameters
- 3+ optional parameters
- Step-by-step construction needed
- Complex validation during construction
- Immutable objects with many fields

**❌ Inappropriate when**:
- Few parameters (<5)
- Simple construction
- No validation needed
- Dataclasses sufficient

**📊 Thresholds**:
- Consider for 5+ parameters
- Use dataclasses for simple cases

#### Repository Pattern Validation
**✅ Appropriate when**:
- Multiple data sources
- Complex queries
- Domain-driven design
- Abstracting data access layer
- Different storage strategies

**❌ Inappropriate when**:
- Simple CRUD operations
- ORM already provides abstraction
- Single data source
- Generic repository anti-pattern

#### Adapter Pattern Validation
**✅ Appropriate when**:
- Incompatible interfaces
- Cannot modify existing code
- Third-party integration
- Legacy system integration

**❌ Inappropriate when**:
- Can modify interfaces directly
- Interfaces already compatible
- Adaptation too complex

**💡 Note**: Simplest pattern when you can't change existing interfaces

#### Decorator Pattern Validation
**✅ Appropriate when**:
- 3+ optional features
- Multiple feature combinations
- Dynamic behavior addition
- Composable behaviors

**❌ Inappropriate when**:
- Fixed combinations
- Complex interfaces
- Simple objects
- Performance critical

**📊 Thresholds**:
- Valuable for 3+ features
- Consider inheritance for 2-3 features

#### State Pattern Validation
**✅ Appropriate when**:
- 3+ states with different behaviors
- Complex state transitions
- Finite state machines
- State-dependent behavior

**❌ Inappropriate when**:
- Simple boolean states
- 2-3 simple states
- Performance critical
- Simple conditional logic sufficient

**💡 Alternative**: Consider enum + match for simple state logic

### Step 3: Provide Validation Response

Format response based on validation result:

#### ✅ APPROPRIATE Pattern Usage
```
✅ **[Pattern] Pattern Assessment**

**Scenario Analysis**:
- [Key requirement 1] ✓ (meets threshold)
- [Key requirement 2] ✓ (appropriate use case)
- [Key requirement 3] ✓ (expected benefit)

**Validation Result**: **APPROPRIATE**
**Confidence**: [LOW/MEDIUM/HIGH/CRITICAL]

**Requirements Met**:
✓ [Specific criteria from pattern]
✓ [Threshold exceeded]
✓ [Use case match]

**Implementation Guidance**:
- [Key design decisions]
- [Performance considerations]
- [Thread safety if applicable]
- [Testing implications]

**Repository Reference**: `notebooks/[XX]_[pattern]_pattern.ipynb`
```

#### ❌ INAPPROPRIATE Pattern Usage / Anti-Pattern
```
❌ **ANTI-PATTERN DETECTED**

⚠️ **Critical Issue**: [Specific problem]
**Risk Level**: [LOW/MEDIUM/HIGH/CRITICAL]

**Problems**:
- [Specific issue 1]
- [Specific issue 2]
- [Testing/maintenance concerns]

**Better Alternatives**:
1. **[Alternative 1]**: [Description and benefits]
2. **[Alternative 2]**: [Description and benefits]

**Example**:
```python
# ❌ DON'T DO THIS
[Bad example]

# ✅ DO THIS
[Good alternative]
```

**Confidence**: [HIGH/CRITICAL] - This is definitely problematic
```

#### ⚠️ BORDERLINE Pattern Usage
```
⚠️ **Borderline Pattern Usage**

**Scenario Analysis**:
- [Requirement 1] [✓/❌/?] (threshold status)
- [Requirement 2] [✓/❌/?] (appropriateness)
- [Growth potential] ? (unclear)

**Assessment**: **CONSIDER ALTERNATIVES**
**Confidence**: [LOW/MEDIUM]

**Threshold Analysis**:
❌ [Below threshold] (current: X, threshold: Y)
✓ [Meets criteria]
? [Unclear factor]

**Decision Factors**:
1. [Question 1]? → [Pattern recommendation]
2. [Question 2]? → [Alternative recommendation]

**Recommendations**:
- **If [condition]**: [Use pattern]
- **If [condition]**: [Use alternative]

**Repository Reference**: See pattern examples for similar scenarios
```

### Step 4: Handle Special Cases

#### Unknown Pattern
If pattern not in our 10 patterns:
```
❓ **Unknown Pattern**: [Pattern Name]

This repository focuses on 10 essential design patterns:
- Singleton, Factory, Observer, Strategy, Command
- Builder, Repository, Adapter, Decorator, State

Did you mean one of these patterns? Please clarify and I'll provide validation.
```

#### Vague Scenario
If scenario is too vague:
```
🔍 **Need More Context**

To provide accurate validation, please specify:
- What problem are you trying to solve?
- What's the expected scale/complexity?
- Are there performance requirements?
- What's the team's experience level?

Example: `/dp::check singleton for database connection pool in multi-threaded web application`
```

## Quality Standards

### High-Quality Validation Response:
- **Specific**: References exact thresholds and criteria
- **Evidence-Based**: Uses repository knowledge and examples
- **Actionable**: Provides clear next steps
- **Contextual**: Considers threading, performance, testing
- **Alternative-Aware**: Suggests better approaches when appropriate

### Validation Confidence Levels:
- **CRITICAL**: Definitely right/wrong based on clear criteria
- **HIGH**: Strong evidence for recommendation
- **MEDIUM**: Likely appropriate but depends on context
- **LOW**: Borderline case requiring more information

Remember: Favor simplicity over patterns when complexity isn't justified.