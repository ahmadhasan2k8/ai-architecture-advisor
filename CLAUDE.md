# AI Assistant Rules for Python Development

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