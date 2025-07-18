#!/usr/bin/env python3
"""
Comprehensive validation script for design patterns tutorial.
This script validates notebooks, source code, and tests.
"""

import json
import os
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def validate_notebooks() -> Tuple[bool, List[str]]:
    """Validate all Jupyter notebooks."""
    print("🔍 Validating Jupyter notebooks...")
    
    errors = []
    notebooks_dir = Path("notebooks")
    
    if not notebooks_dir.exists():
        errors.append("notebooks directory does not exist")
        return False, errors
    
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
    
    for notebook_file in expected_notebooks:
        notebook_path = notebooks_dir / notebook_file
        if not notebook_path.exists():
            errors.append(f"Missing notebook: {notebook_file}")
            continue
            
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Check required fields
            if 'cells' not in notebook:
                errors.append(f"{notebook_file}: Missing 'cells' field")
                continue
                
            # Check for title and TOC
            has_title = False
            has_toc = False
            
            for cell in notebook['cells']:
                if cell['cell_type'] == 'markdown':
                    source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
                    if source.startswith('# ') and 'Pattern Tutorial' in source:
                        has_title = True
                    if 'Table of Contents' in source:
                        has_toc = True
            
            if not has_title:
                errors.append(f"{notebook_file}: Missing proper title")
            if not has_toc:
                errors.append(f"{notebook_file}: Missing table of contents")
                
        except json.JSONDecodeError as e:
            errors.append(f"{notebook_file}: Invalid JSON - {e}")
        except Exception as e:
            errors.append(f"{notebook_file}: Error reading file - {e}")
    
    success = len(errors) == 0
    if success:
        print(f"✅ All {len(expected_notebooks)} notebooks are valid")
    else:
        print(f"❌ Found {len(errors)} notebook validation errors")
    
    return success, errors

def validate_source_code() -> Tuple[bool, List[str]]:
    """Validate source code implementations."""
    print("🔍 Validating source code implementations...")
    
    errors = []
    src_dir = Path("src")
    patterns_dir = src_dir / "patterns"
    
    if not patterns_dir.exists():
        errors.append("src/patterns directory does not exist")
        return False, errors
    
    expected_patterns = [
        "singleton.py",
        "factory.py",
        "observer.py", 
        "strategy.py",
        "decorator.py",
        "command.py",
        "repository.py",
        "builder.py",
        "adapter.py",
        "state.py"
    ]
    
    for pattern_file in expected_patterns:
        pattern_path = patterns_dir / pattern_file
        if not pattern_path.exists():
            errors.append(f"Missing pattern implementation: {pattern_file}")
            continue
            
        try:
            # Try to import the module
            spec = importlib.util.spec_from_file_location(
                f"patterns.{pattern_file[:-3]}", 
                pattern_path
            )
            if spec is None:
                errors.append(f"{pattern_file}: Could not create module spec")
                continue
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
        except Exception as e:
            errors.append(f"{pattern_file}: Import error - {e}")
    
    # Test basic functionality
    try:
        from patterns import Singleton, ComputerBuilder
        
        # Test singleton
        class TestSingleton(Singleton):
            pass
        
        s1 = TestSingleton()
        s2 = TestSingleton()
        if s1 is not s2:
            errors.append("Singleton pattern not working correctly")
        
        # Test builder
        computer = (ComputerBuilder()
                   .set_cpu("Intel i7")
                   .set_memory("16GB")
                   .build())
        if not hasattr(computer, 'cpu') or computer.cpu != "Intel i7":
            errors.append("Builder pattern not working correctly")
            
    except Exception as e:
        errors.append(f"Pattern functionality test failed: {e}")
    
    success = len(errors) == 0
    if success:
        print(f"✅ All {len(expected_patterns)} pattern implementations are valid")
    else:
        print(f"❌ Found {len(errors)} source code validation errors")
    
    return success, errors

def validate_tests() -> Tuple[bool, List[str]]:
    """Validate test files."""
    print("🔍 Validating test files...")
    
    errors = []
    tests_dir = Path("tests") / "test_patterns"
    
    if not tests_dir.exists():
        errors.append("tests/test_patterns directory does not exist")
        return False, errors
    
    expected_tests = [
        "test_singleton.py",
        "test_factory.py",
        "test_observer.py",
        "test_strategy.py", 
        "test_decorator.py",
        "test_command.py",
        "test_repository.py",
        "test_builder.py",
        "test_adapter.py",
        "test_state.py"
    ]
    
    for test_file in expected_tests:
        test_path = tests_dir / test_file
        if not test_path.exists():
            errors.append(f"Missing test file: {test_file}")
            continue
            
        try:
            # Check if file contains test functions
            with open(test_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'def test_' not in content:
                errors.append(f"{test_file}: No test functions found")
                
        except Exception as e:
            errors.append(f"{test_file}: Error reading file - {e}")
    
    success = len(errors) == 0
    if success:
        print(f"✅ All {len(expected_tests)} test files are present")
    else:
        print(f"❌ Found {len(errors)} test validation errors")
    
    return success, errors

def validate_docker() -> Tuple[bool, List[str]]:
    """Validate Docker configuration."""
    print("🔍 Validating Docker configuration...")
    
    errors = []
    
    # Check Dockerfile exists
    dockerfile_path = Path("Dockerfile")
    if not dockerfile_path.exists():
        errors.append("Dockerfile does not exist")
    
    # Check docker-compose.yml exists  
    compose_path = Path("docker-compose.yml")
    if not compose_path.exists():
        errors.append("docker-compose.yml does not exist")
    
    # Check requirements files exist
    req_path = Path("requirements.txt")
    if not req_path.exists():
        errors.append("requirements.txt does not exist")
        
    req_dev_path = Path("requirements-dev.txt")
    if not req_dev_path.exists():
        errors.append("requirements-dev.txt does not exist")
    
    success = len(errors) == 0
    if success:
        print("✅ Docker configuration is valid")
    else:
        print(f"❌ Found {len(errors)} Docker configuration errors")
    
    return success, errors

def validate_project_structure() -> Tuple[bool, List[str]]:
    """Validate overall project structure."""
    print("🔍 Validating project structure...")
    
    errors = []
    
    expected_dirs = [
        "src",
        "src/patterns", 
        "tests",
        "tests/test_patterns",
        "notebooks",
        "docs",
        "data"
    ]
    
    for dir_path in expected_dirs:
        if not Path(dir_path).exists():
            errors.append(f"Missing directory: {dir_path}")
    
    expected_files = [
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "Dockerfile",
        "docker-compose.yml",
        "CLAUDE.md",
        "src/__init__.py",
        "src/patterns/__init__.py",
        "tests/__init__.py",
        "tests/conftest.py"
    ]
    
    for file_path in expected_files:
        if not Path(file_path).exists():
            errors.append(f"Missing file: {file_path}")
    
    success = len(errors) == 0
    if success:
        print("✅ Project structure is valid")
    else:
        print(f"❌ Found {len(errors)} project structure errors")
    
    return success, errors

def main():
    """Run comprehensive validation."""
    print("🚀 Starting comprehensive validation of Design Patterns Tutorial")
    print("=" * 60)
    
    all_success = True
    all_errors = []
    
    # Run all validations
    validations = [
        ("Project Structure", validate_project_structure),
        ("Notebooks", validate_notebooks),
        ("Source Code", validate_source_code),
        ("Tests", validate_tests),
        ("Docker", validate_docker)
    ]
    
    for name, validation_func in validations:
        success, errors = validation_func()
        if not success:
            all_success = False
            all_errors.extend([f"{name}: {error}" for error in errors])
        print()
    
    # Summary
    print("=" * 60)
    if all_success:
        print("🎉 All validations passed! The tutorial is ready to use.")
        print("\nNext steps:")
        print("1. Run tests: docker compose --profile test up test-runner")
        print("2. Start Jupyter: docker compose up jupyter")
        print("3. Access at: http://localhost:8888/tree?token=design-patterns-2025")
    else:
        print("❌ Validation failed with the following errors:")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()