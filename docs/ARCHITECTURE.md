# AI Architecture Advisor - Architecture Documentation

## System Components

The AI Architecture Advisor consists of two main systems that work independently:

### 1. Claude Code Commands (`/dp::` commands)
**Location**: `commands/` directory  
**Purpose**: Instructions for Claude AI to analyze design patterns  
**How it works**: 
- These are markdown files that tell Claude how to respond to dp commands
- Claude uses its built-in tools (Read, Grep, etc.) to analyze code
- No Python code is executed - it's all AI-driven analysis

### 2. Python Analysis Engine (Optional)
**Location**: `ai-engine/` directory  
**Purpose**: Standalone Python tools for code analysis  
**Components**:
- `pattern_knowledge.py` - Pattern decision criteria and thresholds
- `code_analyzer.py` - AST-based Python code analysis
- `repo_analyzer.py` - Repository-wide pattern detection
- `refactoring_templates.py` - Code transformation templates

## How They Work Together (Or Don't)

**Important**: The dp commands and Python engine are **separate systems**:

1. **dp commands** work entirely through Claude AI:
   - You type `/dp::analyze <problem>`
   - Claude reads the instructions from `commands/analyze.md`
   - Claude analyzes using its AI capabilities and knowledge
   - No Python code is executed

2. **Python engine** is for standalone analysis:
   - Can be run separately: `python -m ai-engine.code_analyzer <file>`
   - Provides programmatic pattern detection
   - Not currently integrated with dp commands

## Why This Design?

- **Simplicity**: dp commands work immediately without Python setup
- **Flexibility**: Claude can analyze any language, not just Python
- **Power**: Claude's AI understanding goes beyond static analysis
- **Optional complexity**: Python tools available for those who need them

## Future Integration Possibilities

The commands could potentially call the Python engine in the future:
```python
# Hypothetical future integration
/dp::refactor file.py --use-python-engine
```

But currently, they operate independently for maximum simplicity and compatibility.