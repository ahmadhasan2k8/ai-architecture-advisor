# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Design Patterns Tutorial** repository teaching 10 essential design patterns through interactive Jupyter notebooks with production-ready Python implementations.

## Common Development Commands

### Running Tests
```bash
# Docker (recommended for consistency)
docker compose --profile test up test-runner

# Local development
pytest                              # Run all tests
pytest tests/test_singleton.py      # Run specific test file
pytest -k "test_thread_safety"      # Run tests matching pattern
pytest -m "not slow"                # Skip slow tests
```

### Code Quality & Validation
```bash
# Full validation (run before committing)
python validate.py

# Individual tools
black src tests                     # Format code
isort src tests                     # Sort imports
mypy src                           # Type checking
flake8 src tests                   # Linting
bandit -r src                      # Security checks
radon cc src -a                    # Complexity analysis
```

### Running Notebooks
```bash
# Docker (recommended)
docker compose up --build
# Access at: http://localhost:8888/tree?token=design-patterns-2025

# Local
jupyter lab notebooks/
```

### Testing Notebooks
```bash
python test_notebooks.py            # Validate notebook structure
```

## Design Pattern Recommendation System

This repository includes an intelligent pattern recommendation system that helps users choose appropriate design patterns based on their specific needs and prevents anti-pattern usage.

### Custom Commands (dp:: namespace)

#### `/dp::analyze` - Comprehensive Pattern Analysis
Performs deep analysis of problem descriptions using sequential thinking to:
- Identify potential design patterns that fit the scenario
- Evaluate complexity vs. benefit trade-offs
- Consider advanced scenarios (threading, performance, testing)
- Provide confidence scores and reasoning
- Suggest simpler alternatives when patterns are overkill

**Usage:**
```
/dp::analyze I need a system where multiple UI components update when the user data changes
```

#### `/dp::check` - Quick Pattern Suitability Check  
Fast assessment of whether a specific pattern is appropriate:
- Validates pattern choice against repository knowledge
- Checks for anti-pattern indicators
- Provides threshold-based recommendations
- Suggests optimization strategies

**Usage:**
```
/dp::check singleton for database connection in multi-threaded app
```

#### `/dp::refactor` - Code Analysis for Pattern Opportunities
Analyzes existing code to identify refactoring opportunities:
- Scans for pattern implementation opportunities
- Detects anti-patterns in current code
- Prioritizes refactoring suggestions by ROI
- Provides before/after examples

**Usage:**
```
/dp::refactor payment_processor.py
```

#### `/dp::validate` - Anti-Pattern Detection
Proactively detects and warns about pattern misuse:
- Identifies overengineering scenarios
- Warns about inappropriate pattern usage
- Suggests simpler alternatives
- Prevents common pattern mistakes

**Usage:**
```
/dp::validate making all model classes singletons
```

### Pattern Recognition Framework

When users describe problems, automatically analyze for pattern indicators:

#### Trigger Phrases for Pattern Recognition:
- **Singleton**: "single instance", "only one", "global access", "shared state"
- **Factory**: "create different types", "multiple implementations", "switch creation"
- **Observer**: "subscribe", "notify", "listen", "event", "update", "broadcast"
- **Strategy**: "multiple algorithms", "different ways", "switch algorithm", "runtime selection"
- **Command**: "undo", "redo", "queue", "macro", "log operations"
- **Builder**: "complex construction", "many parameters", "step by step", "fluent interface"
- **Adapter**: "incompatible interfaces", "third-party integration", "legacy system"
- **Decorator**: "add responsibilities", "multiple features", "composable behaviors"
- **State**: "behavior depends on state", "finite state machine", "state transitions"
- **Repository**: "data access", "multiple data sources", "centralize queries"

#### Sequential Thinking Analysis Process:
When processing pattern requests, use this systematic approach:

1. **Understand the Problem**
   - What exactly is the user trying to achieve?
   - What are the constraints and requirements?
   - What's the expected complexity and scale?

2. **Analyze Complexity Indicators** 
   - Number of variations/algorithms/types involved
   - Expected growth and change frequency
   - Team expertise and maintenance considerations
   - Performance and threading requirements

3. **Evaluate Pattern Candidates**
   - Which patterns could solve this problem?
   - What are the trade-offs of each approach?
   - Check against repository knowledge base

4. **Consider Simpler Alternatives**
   - Could a non-pattern approach work better?
   - What would the simple Python solution look like?
   - Is the complexity justified?

5. **Anti-Pattern Check**
   - Is this overengineering for the scenario?
   - Are we solving a problem that doesn't exist?
   - Check against known anti-pattern indicators

6. **Make Recommendation**
   - Primary recommendation with confidence score
   - Alternative approaches with pros/cons
   - Implementation guidance from repository examples
   - Link to relevant notebook sections

### Complexity Thresholds for Pattern Usage

Use these specific thresholds from repository knowledge:

#### Singleton Pattern:
- ✅ Use when: Expensive object creation, global access needed, shared state required
- ❌ Avoid when: Simple objects, testing important, might need multiple instances later
- 🧵 Thread safety: Required for multi-threaded applications (use double-check locking)

#### Factory Pattern:
- ✅ Use when: 3+ similar classes, complex creation logic, runtime type switching
- ❌ Avoid when: Only 1-2 types, simple object creation, "just in case" scenarios
- 📊 Threshold: Valuable at 3+ implementations, consider if/else for 2-3 cases

#### Observer Pattern:
- ✅ Use when: 2+ observers, event-driven architecture, one-to-many relationships
- ❌ Avoid when: Only 1 observer, performance critical, complex update sequences
- 🧵 Thread safety: Protect observer list with locks, consider async notifications

#### Strategy Pattern:
- ✅ Use when: 3+ algorithms, runtime switching, eliminating conditionals >10 lines
- ❌ Avoid when: Only 1-2 algorithms, simple variations, algorithms rarely change
- 📊 Threshold: Use for 3+ algorithms, if/else acceptable for 2-3 cases

#### Command Pattern:
- ✅ Use when: Undo/redo needed, operation queuing, macro commands, audit logging
- ❌ Avoid when: Simple operations, no undo needed, performance critical paths
- 💡 Complexity: Valuable for GUI apps, overkill for basic getters/setters

#### Builder Pattern:
- ✅ Use when: 5+ constructor parameters, 3+ optional parameters, step-by-step construction
- ❌ Avoid when: Few parameters, simple construction, no validation needed
- 📊 Threshold: Consider for 5+ parameters, use dataclasses for simple cases

#### Repository Pattern:
- ✅ Use when: Multiple data sources, complex queries, domain-driven design
- ❌ Avoid when: Simple CRUD, ORM already abstracts, single data source
- 💡 Note: Avoid generic repository anti-pattern

#### Adapter Pattern:
- ✅ Use when: Incompatible interfaces, cannot modify existing code, third-party integration
- ❌ Avoid when: Can modify interfaces, interfaces already compatible, too complex adaptation
- 🎯 Simplest pattern: Use when you cannot change existing interfaces

#### Decorator Pattern:
- ✅ Use when: 3+ optional features, multiple combinations, dynamic behavior addition
- ❌ Avoid when: Fixed combinations, complex interfaces, simple objects
- 📊 Threshold: Valuable for 3+ features, consider inheritance for 2-3 features

#### State Pattern:
- ✅ Use when: 3+ states, different behaviors per state, finite state machines
- ❌ Avoid when: Simple boolean states, 2-3 simple states, performance critical
- 💡 Alternative: Consider enum + match for simple state logic

### Anti-Pattern Detection Rules

Automatically warn users about these common mistakes:

#### Red Flags:
- **Singleton overuse**: "make all classes singleton", "singleton for data models"
- **Pattern overkill**: "use pattern for 2 simple cases", "add pattern just in case"
- **Inappropriate usage**: "singleton for User/Product entities", "factory for one class"
- **Performance ignorance**: "use in performance critical path without consideration"
- **Testing hostility**: "pattern makes testing much harder"

#### Automatic Warnings:
When detecting anti-pattern indicators, provide:
1. **Specific warning** about the anti-pattern
2. **Why it's problematic** with concrete examples
3. **Better alternatives** for the specific scenario
4. **Repository examples** showing correct usage

### Integration with Repository Knowledge

All recommendations are based on extracted knowledge from the 10 pattern notebooks:
- **Specific use cases** and real-world examples
- **Threading considerations** for concurrent applications  
- **Performance implications** and optimization tips
- **Testing strategies** and challenges
- **Advanced scenarios** and enterprise considerations

Reference the repository's `src/patterns/pattern_knowledge.py` for complete decision criteria and the `docs/extracted_pattern_knowledge.md` for detailed guidance extracted from notebooks.

### Sequential Thinking Integration

Use the `mcp__sequential-thinking__sequentialthinking` tool for complex pattern analysis to ensure thorough, systematic decision-making:

#### When to Use Sequential Thinking:
- Complex pattern selection with multiple candidates
- Scenarios requiring careful trade-off analysis
- Anti-pattern detection and prevention
- Advanced scenarios (threading, performance, architecture)
- Controversial or borderline pattern usage
- Cross-pattern comparisons and combinations

#### Sequential Thinking Template for Pattern Analysis:

```markdown
## Pattern Analysis Using Sequential Thinking

**Thought 1: Problem Understanding**
- What specific problem is the user trying to solve?
- What are the constraints, requirements, and context?
- What's the expected scale and complexity?

**Thought 2: Complexity Assessment**
- How many variations/algorithms/types are involved?
- What's the growth potential and change frequency?
- What are the performance and threading requirements?
- What's the team's expertise level?

**Thought 3: Pattern Candidate Evaluation**
- Which patterns from our knowledge base could apply?
- What are the specific threshold criteria each pattern requires?
- How do the candidates compare against our complexity thresholds?

**Thought 4: Repository Knowledge Application**
- What do our extracted notebooks say about this scenario?
- Are there specific use cases or examples that match?
- What are the threading/performance considerations?

**Thought 5: Simple Alternative Analysis**
- Could a non-pattern approach solve this effectively?
- What would the simple Python solution look like?
- Would the pattern add real value or just complexity?

**Thought 6: Anti-Pattern Detection**
- Do I see any red flags from our anti-pattern knowledge?
- Is this a case of overengineering or premature optimization?
- Are there better architectural approaches?

**Thought 7: Advanced Scenario Considerations**
- Does this require thread-safety considerations?
- What are the testing implications?
- Are there performance trade-offs to consider?
- How does this fit into larger architectural patterns?

**Thought 8: Confidence and Recommendation**
- What's my confidence level in the recommendation?
- What are the key deciding factors?
- What alternatives should be mentioned?
- What implementation guidance should I provide?
```

#### Example Sequential Thinking Application:

**User Request**: "I need different export formats for reports - PDF, Excel, CSV, and maybe Word later"

**Sequential Analysis**:
1. **Problem**: Multiple export algorithms with potential for growth
2. **Complexity**: 3+ confirmed formats, 1 potential, likely different implementation approaches
3. **Pattern Candidates**: Strategy (algorithms), Factory (object creation), or simple if/else
4. **Repository Check**: Strategy threshold is 3+ algorithms ✓, expects growth ✓
5. **Simple Alternative**: if/else could work for fixed 3-4 formats
6. **Anti-Pattern Check**: Not overengineering if export logic is substantial
7. **Advanced Considerations**: Thread-safety needs, performance of different formats
8. **Recommendation**: Strategy Pattern with HIGH confidence due to growth potential and algorithm complexity

#### Decision Flow Integration:

For each dp:: command, follow this enhanced decision process:

1. **Trigger Sequential Thinking** when:
   - Multiple patterns could apply
   - User asks about controversial patterns (Singleton, Repository)
   - Advanced scenarios involving threading/performance
   - Anti-pattern prevention needed
   - Complex architectural decisions

2. **Use Repository Knowledge** systematically:
   - Reference specific thresholds and criteria
   - Apply extracted notebook guidance
   - Consider advanced scenarios from pattern knowledge
   - Check against anti-pattern indicators

3. **Provide Transparent Reasoning**:
   - Show the thinking process to users
   - Explain why certain patterns were considered/rejected
   - Reference specific repository examples
   - Include confidence levels and alternatives

#### Pattern-Specific Sequential Thinking Triggers:

**Singleton Requests** → Always use sequential thinking to check:
- Is this really a single instance scenario?
- Are there testing implications?
- Is thread-safety needed?
- Could dependency injection be better?

**Factory Requests** → Use sequential thinking when:
- Unclear how many types will be created
- User mentions "extensibility" or "future types"
- Complex creation logic involved

**Observer Requests** → Use sequential thinking for:
- Performance-critical scenarios
- Complex update sequences
- Threading considerations
- Event ordering requirements

**Strategy Requests** → Use sequential thinking when:
- Algorithm count is borderline (2-3 algorithms)
- Performance differences between strategies
- Runtime selection complexity

### Advanced Pattern Guidance Integration

#### Multi-Pattern Scenarios:
When patterns might be combined, use sequential thinking to evaluate:
- **Builder + Strategy**: Complex objects with algorithmic variations
- **Factory + Strategy**: Creating strategy instances
- **Observer + Command**: Event systems with undo/redo
- **Repository + Strategy**: Data access with different storage strategies

#### Enterprise Architecture Considerations:
Use sequential thinking for larger architectural decisions:
- Microservices boundary definitions
- Cross-service communication patterns
- Data consistency patterns
- Scalability and distributed system implications

#### Performance-Critical Scenarios:
Apply systematic analysis for:
- High-throughput systems
- Real-time processing requirements
- Memory-constrained environments
- Latency-sensitive applications

#### Testing and Maintainability Focus:
Consider through sequential thinking:
- Test complexity and mockability
- Code maintainability over time
- Team onboarding and knowledge transfer
- Documentation and debugging requirements

## Architecture & Key Components

### Pattern Implementations (`src/patterns/`)
- **Singleton**: Thread-safe metaclass implementation with double-check locking
- **Factory/Builder**: Clean interfaces for object creation
- **Observer**: Event system with type-safe subscriptions
- **Strategy**: Pluggable algorithms with clear interfaces
- **Repository**: Data abstraction with SQLite and JSON backends
- Each pattern uses full type hints and follows modern Python practices

### Testing Strategy (`tests/`)
- **Fixtures**: Extensive pytest fixtures in `conftest.py` for each pattern
- **Markers**: `slow`, `integration`, `unit`, `performance` for test categorization
- **Thread Safety**: Concurrent access tests for singleton patterns
- **Coverage**: Strict 90% requirement enforced by CI/CD

### Key Implementation Details
1. **Metaclass Singleton**: Uses `SingletonMeta` for automatic singleton behavior
2. **Thread Safety**: Double-check locking pattern for concurrent environments
3. **Type Safety**: Full typing with mypy strict mode validation
4. **Repository Pattern**: Abstract base with concrete SQLite/JSON implementations

## Response Quality

- **No Fabrication**: Never invent functions, APIs, or features that don't exist
- **Factual Only**: All information must be verifiable from codebase or documentation  
- **Admit Ignorance**: Say "I don't know" instead of guessing
- **Stay Relevant**: Address only what's asked, no tangential information

## Code Generation

- **Minimal Changes**: Modify only what's necessary to solve the problem
- **Follow Project Style**: Match existing naming, formatting, and patterns exactly
- **Complete Solutions**: No TODOs, placeholders, or incomplete implementations
- **Context Aware**: Read related files before suggesting changes

## Communication Style

- **Direct Instructions**: Be concise, avoid apologizing or explaining obvious things
- **Step-by-Step**: Break complex tasks into clear sequential steps
- **Structured Output**: Use bullet points, numbered lists, and code blocks with syntax highlighting
- **Ask for Clarification**: When requirements are ambiguous, ask specific questions

## Error Handling

- **Fix, Don't Apologize**: Correct errors immediately without lengthy explanations
- **Explicit Validation**: Include input validation for public APIs
- **Meaningful Messages**: Provide clear, actionable error descriptions
- **Fail Fast**: Handle edge cases early in functions

## Code Quality

- **Type Safety**: Use type hints for all functions and methods
- **Memory Efficiency**: Consider memory usage with large datasets
- **Modern Python**: Use Python 3.11+ features appropriately
- **Design Patterns**: Apply appropriate patterns without over-engineering

## Build Awareness

- **Dependency Impact**: Consider requirements.txt and pyproject.toml when suggesting changes
- **Breaking Changes**: Mention potential compatibility issues
- **Cross-Platform**: Consider portability implications

## Performance Focus

- **Algorithm Efficiency**: Consider time and space complexity
- **Optimization Opportunities**: Mention when caching or vectorization could help
- **Memory vs Speed**: Consider trade-offs and ask for priorities

---

# Python Coding Standards (PEP 8 + Modern Best Practices)

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables/Functions | `snake_case` | `calculate_total()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Classes | `PascalCase` | `DataProcessor` |
| Private attributes | Leading underscore | `_internal_state` |
| Protected attributes | Single underscore | `_protected_var` |
| Module private | Leading underscore | `_private_function()` |

## Code Style & Quality

- **Line Length**: Max 88 characters (Black default)
- **Indentation**: 4 spaces (no tabs)
- **Imports**: 
  - Standard library first
  - Third-party packages second
  - Local imports last
  - Alphabetically sorted within groups
- **Type Hints**: Required for all function signatures
- **Docstrings**: Google style for all public functions/classes

## Modern Python Best Practices

```python
# Use type hints
def process_data(items: list[str]) -> dict[str, int]:
    """Process data items and return counts.
    
    Args:
        items: List of string items to process
        
    Returns:
        Dictionary mapping items to their counts
    """
    pass

# Use dataclasses for data containers
from dataclasses import dataclass

@dataclass
class Config:
    host: str
    port: int = 8080
    debug: bool = False

# Use context managers for resources
from contextlib import contextmanager

@contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    finally:
        release_resource(resource)

# Use pathlib for file operations
from pathlib import Path

config_path = Path.home() / ".config" / "app.json"

# Use f-strings for formatting
name = "world"
message = f"Hello, {name}!"

# Use match statements (Python 3.10+)
match command:
    case "start":
        start_process()
    case "stop":
        stop_process()
    case _:
        print("Unknown command")
```

## Error Handling & Logging

- Use specific exception types
- Provide context in error messages
- Use logging instead of print statements
- Handle exceptions at appropriate levels

```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def safe_divide(a: float, b: float) -> Optional[float]:
    """Safely divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division or None if b is zero
    """
    try:
        return a / b
    except ZeroDivisionError:
        logger.warning(f"Division by zero attempted: {a} / {b}")
        return None
```

## Testing Standards

- Use pytest for all tests
- Aim for >90% code coverage
- Use fixtures for test data
- Parametrize tests for multiple cases
- Mock external dependencies

```python
import pytest
from unittest.mock import Mock

@pytest.fixture
def sample_data():
    return {"key": "value"}

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

## Documentation Standards

- Every module needs a docstring
- Public functions/classes need docstrings
- Complex logic needs inline comments
- Use type hints as documentation
- Examples in docstrings for complex functions

## Performance Guidelines

- Profile before optimizing
- Use generators for large datasets
- Consider using `functools.lru_cache` for expensive computations
- Use appropriate data structures (sets for membership, deque for queues)
- Avoid premature optimization

## Security Best Practices

- Never hardcode credentials
- Validate all inputs
- Use `secrets` module for cryptographic randomness
- Be careful with pickle/eval
- Sanitize user inputs for SQL/command injection

## Jupyter Notebook Standards

- Clear markdown headers for sections
- Explanatory text before code cells
- Clean up outputs before committing
- Use meaningful variable names
- Include visualizations where helpful
- Test notebooks with "Restart & Run All"