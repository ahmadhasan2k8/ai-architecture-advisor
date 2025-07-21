#!/bin/bash
# AI Architecture Advisor - Setup Script
# Sets up dp:: commands globally for Claude Code

set -e  # Exit on error

echo "🚀 Setting up AI Architecture Advisor globally for Claude Code..."
echo

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "commands" ]; then
    echo "❌ Error: Please run this script from the ai-architecture-advisor root directory"
    exit 1
fi

# Get the absolute path of the repository
REPO_PATH=$(pwd)
echo "📍 Repository path: $REPO_PATH"
echo

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "⚠️  Warning: Claude Code CLI not found"
    echo "   Please install from: https://claude.ai/code"
    echo "   Continuing with setup anyway..."
    echo
fi

# Create global .claude/commands directory
echo "📁 Creating global ~/.claude/commands directory..."
mkdir -p ~/.claude/commands

# Create a config file to store the repository path
echo "📝 Saving repository path for global commands..."
echo "AI_ARCHITECTURE_ADVISOR_PATH=\"$REPO_PATH\"" > ~/.claude/ai-architecture-advisor.conf

# Copy dp commands with proper prefix to global location
echo "📋 Installing dp commands globally..."
cp -v commands/analyze.md ~/.claude/commands/dp-analyze.md
cp -v commands/check.md ~/.claude/commands/dp-check.md
cp -v commands/refactor.md ~/.claude/commands/dp-refactor.md
cp -v commands/validate.md ~/.claude/commands/dp-validate.md

# Verify setup
echo
echo "✅ Verifying global installation..."
if [ -f "$HOME/.claude/commands/dp-analyze.md" ] && \
   [ -f "$HOME/.claude/commands/dp-check.md" ] && \
   [ -f "$HOME/.claude/commands/dp-refactor.md" ] && \
   [ -f "$HOME/.claude/commands/dp-validate.md" ] && \
   [ -f "$HOME/.claude/ai-architecture-advisor.conf" ]; then
    echo "✅ All commands installed globally!"
else
    echo "❌ Error: Some commands may not have been installed"
    exit 1
fi

# Success message
echo
echo "🎉 Global setup complete!"
echo
echo "You can now use the dp:: commands from ANY directory in Claude Code:"
echo "  /dp::analyze - Deep pattern analysis with AI reasoning"
echo "  /dp::check   - Quick pattern validation"
echo "  /dp::refactor - Find pattern opportunities in code"
echo "  /dp::validate - Detect anti-patterns and overengineering"
echo
echo "📖 Next steps:"
echo "  1. Open Claude Code from any project: claude /path/to/your/project"
echo "  2. Try: /dp::analyze I need a payment processing system"
echo "  3. Try: /dp::refactor main.py (from your project directory)"
echo "  4. See QUICK_START.md for more examples"
echo
echo "📍 Repository location: $REPO_PATH"
echo "   (Commands will reference pattern knowledge from this location)"
echo

# Make script executable for future runs
chmod +x setup.sh 2>/dev/null || true