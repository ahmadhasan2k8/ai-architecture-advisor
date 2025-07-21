# AI Architecture Advisor - Setup Guide

## Overview

This guide explains how to properly set up the AI Architecture Advisor's design pattern commands (`dp::` commands) for use with Claude Code.

## Quick Setup (2 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/ahmadhasan2k8/ai-architecture-advisor.git
cd ai-architecture-advisor

# 2. Make dp commands available to Claude Code
cp -r commands .claude/

# 3. Open Claude Code in the project directory
claude .

# 4. Test that commands work
# Try: /dp::analyze I need a system to handle multiple payment methods
```

## How the dp Commands Work

### Command Structure
The repository contains four design pattern commands in the `commands/` directory:
- `analyze.md` - Comprehensive pattern analysis using sequential thinking
- `check.md` - Quick pattern validation
- `refactor.md` - Code analysis for pattern opportunities  
- `validate.md` - Anti-pattern detection

**Important**: These are instruction files for Claude AI, not executable scripts. They tell Claude how to analyze your code using AI reasoning.

### Claude Code Integration
Claude Code automatically detects and loads commands from:
- `.claude/commands/` directory in the project root
- Each `.md` file becomes a callable command
- Commands use the `/dp::` namespace

### How Analysis Works
When you run a dp command:
1. Claude reads the instructions from the command file
2. Claude uses its AI capabilities to analyze your code/problem
3. Claude applies the pattern knowledge embedded in the instructions
4. You get AI-powered recommendations based on best practices

**Note**: The Python files in `ai-engine/` are separate analysis tools that can be run independently. The dp commands don't call these Python files - they work entirely through Claude's AI.

### Command Flow
```
Repository Structure          →  Claude Code Structure
commands/                        .claude/commands/
├── analyze.md                   ├── analyze.md  → /dp::analyze
├── check.md                     ├── check.md    → /dp::check
├── refactor.md                  ├── refactor.md → /dp::refactor
└── validate.md                  └── validate.md → /dp::validate
```

## Manual Setup Steps

If the quick setup doesn't work, follow these steps:

### 1. Verify Prerequisites
```bash
# Check Claude Code is installed
claude --version

# Should output version number
# If not, install from: https://claude.ai/code
```

### 2. Set Up Command Directory
```bash
# From the ai-architecture-advisor directory
mkdir -p .claude/commands

# Copy the dp commands
cp commands/*.md .claude/commands/
```

### 3. Verify Setup
```bash
# List the commands
ls -la .claude/commands/

# Should show:
# analyze.md
# check.md
# refactor.md
# validate.md
```

### 4. Test Commands
Open Claude Code in the project directory:
```bash
claude .
```

Then test each command:
```bash
# Test analyze
/dp::analyze I need to manage user sessions

# Test check  
/dp::check singleton for database connection

# Test refactor
/dp::refactor src/main.py

# Test validate
/dp::validate making all classes singleton
```

## Troubleshooting

### "Command not found"
1. Ensure you're in the project root directory
2. Check `.claude/commands/` exists and contains the `.md` files
3. Restart Claude Code

### "Commands not working properly"
1. Verify the command files were copied correctly
2. Check file permissions: `chmod 644 .claude/commands/*.md`
3. Ensure no syntax errors in command files

### "Can't find .claude directory"
The `.claude` directory might be hidden. Use:
```bash
ls -la | grep .claude
```

## Command Reference

### `/dp::analyze <problem description>`
Performs deep architectural analysis using sequential thinking AI to evaluate pattern options.

**Example:**
```
/dp::analyze Payment processing system with credit cards, PayPal, and crypto
```

### `/dp::check <pattern> for <scenario>`
Quick validation of whether a specific pattern fits your use case.

**Example:**
```
/dp::check strategy for handling 2 export formats
```

### `/dp::refactor <file or directory>`
Analyzes existing code to find pattern opportunities and anti-patterns.

**Example:**
```
/dp::refactor src/services/payment_handler.py
```

### `/dp::validate <pattern usage description>`
Checks for overengineering and pattern misuse.

**Example:**
```
/dp::validate using factory pattern for creating user objects
```

## For Repository Maintainers

To ensure the commands work for all users:

1. Keep commands in the `commands/` directory as the source of truth
2. Add `.claude/` to `.gitignore` (users create it locally)
3. Document the setup process in README.md
4. Consider adding a setup script:

```bash
#!/bin/bash
# setup.sh - Set up dp commands for Claude Code

echo "Setting up AI Architecture Advisor..."

# Create .claude directory structure
mkdir -p .claude/commands

# Copy commands
cp commands/*.md .claude/commands/

echo "✅ Setup complete! You can now use dp:: commands in Claude Code"
echo "Try: /dp::analyze your architecture problem"
```

## Next Steps

After setup, see:
- [QUICK_START.md](QUICK_START.md) - Learn how to use the commands effectively
- [dp_commands_guide.md](learning-resources/guides/dp_commands_guide.md) - Detailed command documentation
- [README.md](README.md) - Project overview and capabilities