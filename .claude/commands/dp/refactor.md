# /dp::refactor - Code Analysis for Pattern Opportunities

**Purpose**: Analyze existing code files for pattern implementation opportunities and anti-pattern detection

## Command Usage
```
/dp::refactor <file_path>
/dp::refactor <directory_path>
```

## Execution Strategy

You are a design pattern expert analyzing existing code for refactoring opportunities. Use the repository's code analysis tools when available, or perform manual analysis using file reading tools.

### Step 1: Determine Analysis Scope
- **Single File**: Detailed analysis of one file
- **Directory**: Overview analysis of multiple files
- **Large Directory** (>10 files): Summarized analysis with prioritized opportunities

### Step 2: Read and Analyze Code

#### For Single File Analysis:
1. **Read the file** using the Read tool
2. **Scan for pattern opportunities** using these indicators:
   - Long conditional chains (Strategy pattern)
   - Complex object creation (Factory/Builder pattern)
   - Manual notification loops (Observer pattern)
   - Repetitive similar classes (Strategy/Factory pattern)
   - Global state management (Singleton evaluation)
   - Complex parameter lists (Builder pattern)
   - Data access mixing with business logic (Repository pattern)
   - Incompatible interface usage (Adapter pattern)
   - Behavior addition through inheritance (Decorator pattern)
   - State-dependent behavior (State pattern)

#### For Directory Analysis:
1. **List files** in directory
2. **Read key files** (largest, most complex, or core business logic)
3. **Identify patterns** across multiple files
4. **Prioritize opportunities** by impact and effort

### Step 3: Pattern Opportunity Detection

#### Strategy Pattern Indicators:
```python
# Look for these patterns:
if condition == "type1":
    # 10+ lines of logic
elif condition == "type2":
    # 10+ lines of logic
elif condition == "type3":
    # 10+ lines of logic

# Or switch-like dictionaries:
handlers = {
    "type1": handler1,
    "type2": handler2,
    "type3": handler3,
}
```

#### Factory Pattern Indicators:
```python
# Look for complex creation logic:
def create_object(type_name, **kwargs):
    if type_name == "A":
        return ClassA(param1, param2, validation1())
    elif type_name == "B":
        return ClassB(param3, param4, validation2())

# Or multiple isinstance checks:
if isinstance(obj, TypeA):
    return ProcessorA(obj)
elif isinstance(obj, TypeB):
    return ProcessorB(obj)
```

#### Observer Pattern Indicators:
```python
# Look for manual notification loops:
for listener in self.listeners:
    listener.notify(event)

# Or callback management:
def add_callback(self, callback):
    self.callbacks.append(callback)

def notify_all(self, data):
    for callback in self.callbacks:
        callback(data)
```

#### Singleton Pattern Evaluation:
```python
# Look for global variables or class variables:
_instance = None

# Or module-level state:
current_user = None
app_config = {}

# Evaluate if singleton is appropriate or anti-pattern
```

#### Builder Pattern Indicators:
```python
# Look for functions/constructors with many parameters:
def __init__(self, param1, param2, param3, param4, param5, param6=None, param7=None):

# Or complex construction:
def create_report(title, data, format, styling, headers, footers, metadata):
```

#### Repository Pattern Indicators:
```python
# Look for mixed data access and business logic:
class UserService:
    def get_user(self, id):
        # Direct database access mixed with business logic
        user = db.execute("SELECT * FROM users WHERE id = ?", id)
        # Business logic here
        return processed_user
```

#### Anti-Pattern Detection:
- **Singleton for data models** (User, Product, Order classes)
- **God objects** (classes doing too many things)
- **Generic repository** (one repository for all entities)
- **Pattern overuse** (patterns where simple code would work)

### Step 4: Provide Structured Analysis

#### Single File Analysis Format:
```
🔍 **Code Analysis**: [file_path]

**Overview**:
- Lines of code: [number]
- Complexity: [Low/Medium/High]
- Pattern opportunities: [count]

## Pattern Opportunities

### 1. [Pattern Name] (Priority: [0.0-1.0])
**Location**: Lines [start-end]
**Current Issue**: [Description of problem]
**Impact**: [Low/Medium/High] | **Effort**: [Low/Medium/High]

**Code Snippet**:
```python
# Current problematic code
[relevant code section]
```

**Refactoring Suggestion**:
```python
# Improved pattern-based solution
[pattern implementation]
```

**Benefits**:
- [Specific improvement 1]
- [Specific improvement 2]
- [Maintenance benefit]

**Migration Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 2. [Next Pattern] (Priority: [0.0-1.0])
[Similar format...]

## Anti-Patterns Detected
[If any found, list with warnings]

## Recommendations
1. **Priority 1**: [Highest impact change]
2. **Priority 2**: [Next most important]
3. **Future**: [Consider when [condition]]

**Estimated Effort**: [time estimate]
**Expected ROI**: [benefit description]
```

#### Directory Analysis Format:
```
📊 **Repository Analysis**: [directory_path]

**Overview**:
- Files analyzed: [count]
- Total opportunities: [count]
- High priority: [count]
- Anti-patterns detected: [count]

## Anti-Pattern Alerts ⚠️
[List critical issues first]

## High-Priority Opportunities

### 1. [Pattern] in [File]
**Confidence**: [HIGH/MEDIUM/LOW] | **ROI**: [High/Medium/Low]
**Lines**: [location]
**Issue**: [Brief description]

### 2. [Pattern] in [File]
[Similar format...]

## Medium-Priority Opportunities
[Shorter descriptions of secondary opportunities]

## Architectural Insights
**Complexity Assessment**: [Overall assessment]
**Common Patterns**: [Patterns that appear multiple times]
**Technical Debt**: [Areas needing attention]

**Recommendations**:
1. [Most important change]
2. [Second priority]
3. [Future considerations]

**Effort Estimate**: [Overall time for top priorities]
```

### Step 5: Priority Scoring Algorithm

Calculate priority scores (0.0-1.0) based on:

#### Impact Factors (60% of score):
- **Code complexity reduced**: High conditionals = +0.3
- **Maintainability improved**: Easier to extend = +0.2
- **Bug reduction potential**: Common error patterns = +0.1

#### Effort Factors (40% of score):
- **Implementation difficulty**: 
  - Simple refactor = +0.2
  - Moderate changes = +0.1
  - Complex restructure = 0.0
- **Risk level**:
  - Low risk = +0.2
  - Medium risk = +0.1
  - High risk = 0.0

#### Priority Thresholds:
- **0.8-1.0**: Critical - implement immediately
- **0.6-0.8**: High - next sprint/iteration
- **0.4-0.6**: Medium - future planning
- **0.0-0.4**: Low - consider if time permits

### Step 6: Handle Different Code Types

#### Python Code Analysis:
- Look for type hints and modern Python features
- Consider dataclasses vs. Builder pattern
- Analyze async/await usage for Observer pattern
- Check for proper exception handling

#### Mixed Language Projects:
- Focus on architecture patterns across languages
- Look for interface/API design patterns
- Consider serialization and communication patterns

#### Legacy Code:
- Identify modernization opportunities
- Suggest incremental refactoring approaches
- Consider backward compatibility

### Step 7: Integration with Repository Tools

If available, use the repository's analysis tools:
```python
# Try to import and use existing analysis tools
from src.patterns.code_analyzer import analyze_file
from src.patterns.repo_analyzer import analyze_directory

# Fall back to manual analysis if not available
```

## Quality Standards

### High-Quality Analysis Features:
- **Specific line references** for all opportunities
- **Before/after code examples** for major suggestions
- **Effort estimation** based on actual code complexity
- **Risk assessment** for each refactoring
- **Repository-specific knowledge** integration

### Avoid These Common Mistakes:
- Suggesting patterns for their own sake
- Ignoring existing code quality and style
- Recommending complex refactors without clear benefits
- Missing anti-pattern detection
- Providing vague or general suggestions

Remember: The goal is to improve code quality and maintainability, not to use patterns everywhere. Always consider whether the refactoring truly adds value.