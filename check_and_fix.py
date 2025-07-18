#!/usr/bin/env python3
"""
Automated CI/CD issue checker and fixer script.
This script checks for common issues that cause CI/CD failures and automatically fixes them.
"""

import os
import subprocess
import sys
import json
import tempfile
from pathlib import Path


def run_command(cmd, check=True, capture_output=True, text=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=capture_output, text=text)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return e


def check_formatting():
    """Check and fix code formatting issues."""
    print("🔍 Checking code formatting...")
    
    # Check Black formatting
    result = run_command("python3 -m black --check src tests", check=False)
    if result.returncode != 0:
        print("❌ Black formatting issues found. Fixing...")
        run_command("python3 -m black src tests --line-length 88")
        print("✅ Black formatting fixed")
        return True
    else:
        print("✅ Black formatting is correct")
    
    # Check isort
    result = run_command("python3 -m isort --check-only src tests", check=False)
    if result.returncode != 0:
        print("❌ Import ordering issues found. Fixing...")
        run_command("python3 -m isort src tests --line-length 88 --profile black")
        print("✅ Import ordering fixed")
        return True
    else:
        print("✅ Import ordering is correct")
    
    return False


def check_syntax():
    """Check for syntax errors."""
    print("🔍 Checking syntax errors...")
    
    result = run_command("python3 -m flake8 src tests --count --select=E9,F63,F7,F82 --show-source --statistics", check=False)
    if result.returncode != 0:
        print("❌ Syntax errors found:")
        print(result.stdout)
        return False
    else:
        print("✅ No syntax errors found")
        return True


def check_imports():
    """Check if all pattern modules can be imported."""
    print("🔍 Checking imports...")
    
    patterns = [
        "singleton", "factory", "observer", "strategy", "decorator", 
        "command", "repository", "builder", "adapter", "state"
    ]
    
    failed_imports = []
    for pattern in patterns:
        try:
            result = run_command(f"python3 -c 'import sys; sys.path.append(\"src\"); from patterns.{pattern} import *'", check=False)
            if result.returncode != 0:
                failed_imports.append(pattern)
                print(f"❌ Failed to import {pattern}: {result.stderr}")
            else:
                print(f"✅ {pattern} imports successfully")
        except Exception as e:
            failed_imports.append(pattern)
            print(f"❌ Failed to import {pattern}: {e}")
    
    return len(failed_imports) == 0


def check_notebooks():
    """Check notebook validity."""
    print("🔍 Checking notebooks...")
    
    notebooks_dir = Path("notebooks")
    expected_notebooks = [
        "01_singleton_pattern.ipynb",
        "02_factory_pattern.ipynb", 
        "03_observer_pattern.ipynb",
        "04_strategy_pattern.ipynb",
        "05_decorator_pattern.ipynb",
        "06_command_pattern.ipynb",
        "07_repository_pattern.ipynb",
        "08_builder_pattern.ipynb",
        "09_adapter_pattern.ipynb",
        "10_state_pattern.ipynb"
    ]
    
    all_valid = True
    for nb in expected_notebooks:
        path = notebooks_dir / nb
        if not path.exists():
            print(f"❌ {nb} missing")
            all_valid = False
        else:
            try:
                with open(path, 'r') as f:
                    json.load(f)
                print(f"✅ {nb} is valid")
            except json.JSONDecodeError as e:
                print(f"❌ {nb} has invalid JSON: {e}")
                all_valid = False
    
    return all_valid


def check_directories():
    """Check required directories exist."""
    print("🔍 Checking directories...")
    
    required_dirs = ["src", "tests", "notebooks", "docs", "data"]
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory {dir_name} exists")
        else:
            print(f"❌ Directory {dir_name} missing")
            all_exist = False
    
    return all_exist


def check_test_functionality():
    """Check if key functionality works."""
    print("🔍 Checking key functionality...")
    
    try:
        # Test SQLite repository
        result = run_command("""python3 -c "
import sys
sys.path.append('src')
from patterns.repository import SqliteUserRepository, User
repo = SqliteUserRepository(':memory:')
user = User(id=None, name='Test', email='test@example.com')
saved_user = repo.save(user)
assert saved_user.id == 1
print('SQLite repository works')
" """, check=False)
        
        if result.returncode != 0:
            print("❌ SQLite repository test failed")
            print(result.stderr)
            return False
        else:
            print("✅ SQLite repository works")
        
        # Test JsonFile repository
        result = run_command("""python3 -c "
import sys, tempfile, os, json
sys.path.append('src')
from patterns.repository import JsonFileUserRepository
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
    json.dump({'users': [], 'next_id': 1}, f)
    temp_path = f.name
try:
    repo = JsonFileUserRepository(temp_path)
    assert len(repo._users) == 0
    print('JsonFile repository works')
finally:
    os.unlink(temp_path)
" """, check=False)
        
        if result.returncode != 0:
            print("❌ JsonFile repository test failed")
            print(result.stderr)
            return False
        else:
            print("✅ JsonFile repository works")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False


def commit_and_push_fixes():
    """Commit and push any fixes that were made."""
    print("🔍 Checking for changes to commit...")
    
    result = run_command("git diff --name-only", check=False)
    if result.stdout.strip():
        print("📝 Changes detected. Committing...")
        run_command("git add -A")
        run_command('git commit -m "Auto-fix: Resolve formatting and code issues"')
        print("🚀 Pushing changes...")
        run_command("git push origin main")
        print("✅ Changes committed and pushed")
        return True
    else:
        print("✅ No changes to commit")
        return False


def main():
    """Main function to run all checks and fixes."""
    print("🤖 Starting automated CI/CD issue checker and fixer...")
    print("=" * 60)
    
    issues_found = False
    
    # Check directories first
    if not check_directories():
        print("❌ Directory structure issues found")
        issues_found = True
    
    # Check syntax
    if not check_syntax():
        print("❌ Syntax issues found")
        issues_found = True
    
    # Check and fix formatting
    if check_formatting():
        print("🔧 Formatting issues were fixed")
        issues_found = True
    
    # Check imports
    if not check_imports():
        print("❌ Import issues found")
        issues_found = True
    
    # Check notebooks
    if not check_notebooks():
        print("❌ Notebook issues found")
        issues_found = True
    
    # Check functionality
    if not check_test_functionality():
        print("❌ Functionality issues found")
        issues_found = True
    
    print("=" * 60)
    
    if issues_found:
        print("⚠️  Issues were found. Attempting to commit fixes...")
        if commit_and_push_fixes():
            print("✅ Fixes committed and pushed. CI/CD should retry.")
        else:
            print("❌ No automatic fixes were applied. Manual intervention required.")
    else:
        print("🎉 All checks passed! The repository should be ready for CI/CD.")
    
    print("=" * 60)
    print("🏁 Automated checker completed")


if __name__ == "__main__":
    main()