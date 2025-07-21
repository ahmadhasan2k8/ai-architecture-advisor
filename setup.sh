#!/bin/bash
# AI Architecture Advisor - Setup Script
# Sets up dp:: commands for Claude Code

set -e  # Exit on error

echo "🚀 Setting up AI Architecture Advisor for Claude Code..."
echo

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "commands" ]; then
    echo "❌ Error: Please run this script from the ai-architecture-advisor root directory"
    exit 1
fi

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo "⚠️  Warning: Claude Code CLI not found"
    echo "   Please install from: https://claude.ai/code"
    echo "   Continuing with setup anyway..."
    echo
fi

# Create .claude/commands directory
echo "📁 Creating .claude/commands directory..."
mkdir -p .claude/commands

# Copy dp commands
echo "📋 Copying dp commands..."
cp -v commands/*.md .claude/commands/

# Verify setup
echo
echo "✅ Verifying setup..."
if [ -f ".claude/commands/analyze.md" ] && \
   [ -f ".claude/commands/check.md" ] && \
   [ -f ".claude/commands/refactor.md" ] && \
   [ -f ".claude/commands/validate.md" ]; then
    echo "✅ All commands copied successfully!"
else
    echo "❌ Error: Some commands may not have been copied"
    exit 1
fi

# Success message
echo
echo "🎉 Setup complete!"
echo
echo "You can now use the dp:: commands in Claude Code:"
echo "  /dp::analyze - Deep pattern analysis with AI reasoning"
echo "  /dp::check   - Quick pattern validation"
echo "  /dp::refactor - Find pattern opportunities in code"
echo "  /dp::validate - Detect anti-patterns and overengineering"
echo
echo "📖 Next steps:"
echo "  1. Open Claude Code: claude ."
echo "  2. Try: /dp::analyze I need a payment processing system"
echo "  3. See QUICK_START.md for more examples"
echo

# Make script executable for future runs
chmod +x setup.sh 2>/dev/null || true