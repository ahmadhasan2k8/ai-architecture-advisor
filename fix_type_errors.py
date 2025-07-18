#!/usr/bin/env python3
"""Script to fix common type annotation errors."""

import re
import sys
from pathlib import Path

def fix_missing_return_type_none(file_path: Path) -> int:
    """Fix functions missing -> None return type annotation."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    original_content = content
    fixes = 0
    
    # Pattern to find functions without return type that likely return None
    # Matches: def function_name(args):
    # But not: def function_name(args) -> something:
    pattern = r'(def\s+\w+\s*\([^)]*\))(\s*:)'
    
    def check_and_fix(match):
        nonlocal fixes
        full_match = match.group(0)
        func_def = match.group(1)
        colon = match.group(2)
        
        # Check if this already has a return type
        if '->' in full_match:
            return full_match
        
        # Check the function name to guess if it should return None
        func_name = re.search(r'def\s+(\w+)', func_def).group(1)
        
        # Common patterns that usually return None
        none_patterns = [
            '__init__', '__del__', 'set_', 'update', 'delete', 'remove',
            'add_', 'register', 'unregister', 'notify', 'save', 'load',
            'print', 'log', 'write', 'clear', 'reset', 'close', 'open'
        ]
        
        for pattern in none_patterns:
            if pattern in func_name.lower():
                fixes += 1
                return f"{func_def} -> None{colon}"
        
        return full_match
    
    content = re.sub(pattern, check_and_fix, content)
    
    if content != original_content:
        with open(file_path, 'w') as f:
            f.write(content)
    
    return fixes

def main():
    """Fix type errors in pattern files."""
    pattern_files = list(Path('src/patterns').glob('*.py'))
    
    total_fixes = 0
    for file_path in pattern_files:
        if file_path.name == '__init__.py':
            continue
        
        fixes = fix_missing_return_type_none(file_path)
        if fixes > 0:
            print(f"Fixed {fixes} missing return type annotations in {file_path}")
            total_fixes += fixes
    
    print(f"\nTotal fixes: {total_fixes}")
    return 0 if total_fixes > 0 else 1

if __name__ == '__main__':
    sys.exit(main())