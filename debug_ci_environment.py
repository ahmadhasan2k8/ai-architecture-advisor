#!/usr/bin/env python3
"""
Debug script to identify CI environment issues.
This script runs comprehensive checks to identify differences between local and CI environments.
"""

import sys
import os
import subprocess
import json
import traceback
from pathlib import Path


def run_command(cmd, check=False):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return e


def check_python_environment():
    """Check Python environment details."""
    print("🐍 Python Environment Check")
    print("=" * 40)
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Python path: {sys.path}")
    
    # Check installed packages
    result = run_command("python3 -m pip list")
    if result.returncode == 0:
        print("📦 Installed packages:")
        for line in result.stdout.split('\n')[:10]:  # Show first 10 packages
            if line.strip():
                print(f"  {line}")
        print("  ...")
    else:
        print(f"❌ Failed to list packages: {result.stderr}")
    
    print()


def check_file_system():
    """Check file system and permissions."""
    print("📁 File System Check")
    print("=" * 40)
    
    # Check current directory
    print(f"Current directory: {os.getcwd()}")
    
    # Check important files exist
    important_files = [
        "src/patterns/singleton.py",
        "src/patterns/repository.py", 
        "requirements.txt",
        "requirements-dev.txt",
        "notebooks/01_singleton_pattern.ipynb"
    ]
    
    for file_path in important_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
    
    # Check Python path setup
    src_path = os.path.join(os.getcwd(), 'src')
    if src_path in sys.path:
        print(f"✅ {src_path} is in Python path")
    else:
        print(f"❌ {src_path} not in Python path")
        sys.path.insert(0, src_path)
        print(f"🔧 Added {src_path} to Python path")
    
    print()


def check_imports():
    """Check if critical imports work."""
    print("📥 Import Check")
    print("=" * 40)
    
    import_tests = [
        ("sqlite3", "import sqlite3"),
        ("json", "import json"),
        ("tempfile", "import tempfile"),
        ("patterns.singleton", "from patterns.singleton import singleton"),
        ("patterns.repository", "from patterns.repository import User, SqliteUserRepository, JsonFileUserRepository"),
        ("patterns.factory", "from patterns.factory import ShapeFactory"),
        ("patterns.observer", "from patterns.observer import WeatherStation"),
    ]
    
    for name, import_stmt in import_tests:
        try:
            exec(import_stmt)
            print(f"✅ {name} imports successfully")
        except Exception as e:
            print(f"❌ {name} import failed: {e}")
            traceback.print_exc()
    
    print()


def check_repository_functionality():
    """Check repository pattern functionality in detail."""
    print("🗄️ Repository Functionality Check")
    print("=" * 40)
    
    try:
        # Import required modules
        from patterns.repository import User, SqliteUserRepository, JsonFileUserRepository
        
        # Test SQLite repository
        print("Testing SQLite repository...")
        sqlite_repo = SqliteUserRepository(':memory:')
        test_user = User(id=None, name='Test User', email='test@example.com')
        saved_user = sqlite_repo.save(test_user)
        
        print(f"✅ SQLite: User saved with ID {saved_user.id}")
        
        found_user = sqlite_repo.find_by_id(saved_user.id)
        if found_user:
            print(f"✅ SQLite: User found - {found_user.name}")
        else:
            print("❌ SQLite: User not found")
        
        # Test JSON file repository with new file
        print("Testing JSON file repository (new file)...")
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            json_repo = JsonFileUserRepository(temp_path)
            print(f"✅ JSON: Repository created, users count: {len(json_repo._users)}")
            
            saved_user2 = json_repo.save(test_user)
            print(f"✅ JSON: User saved with ID {saved_user2.id}")
            
        finally:
            os.unlink(temp_path)
        
        # Test JSON file repository with existing file
        print("Testing JSON file repository (existing file)...")
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            test_data = {
                'users': [
                    {
                        'id': 1,
                        'name': 'Alice',
                        'email': 'alice@example.com',
                        'created_at': '2023-01-01T12:00:00',
                    }
                ],
                'next_id': 2,
            }
            json.dump(test_data, f)
            temp_path2 = f.name
        
        try:
            json_repo2 = JsonFileUserRepository(temp_path2)
            print(f"✅ JSON existing: Repository loaded, users count: {len(json_repo2._users)}")
            print(f"✅ JSON existing: Next ID: {json_repo2._next_id}")
            print(f"✅ JSON existing: First user: {json_repo2._users[0].name}")
            
        finally:
            os.unlink(temp_path2)
        
        # Test corrupted file handling
        print("Testing corrupted file handling...")
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write('invalid json content')
            temp_path3 = f.name
        
        try:
            json_repo3 = JsonFileUserRepository(temp_path3)
            print(f"✅ Corrupted: Repository created, users count: {len(json_repo3._users)}")
            
        finally:
            os.unlink(temp_path3)
        
        print("✅ All repository functionality tests passed")
        
    except Exception as e:
        print(f"❌ Repository functionality test failed: {e}")
        traceback.print_exc()
    
    print()


def check_notebook_validation():
    """Check notebook validation."""
    print("📓 Notebook Validation Check")
    print("=" * 40)
    
    notebooks_dir = Path("notebooks")
    if not notebooks_dir.exists():
        print("❌ Notebooks directory does not exist")
        return
    
    notebooks = list(notebooks_dir.glob("*.ipynb"))
    print(f"Found {len(notebooks)} notebooks")
    
    for notebook in notebooks:
        try:
            with open(notebook, 'r') as f:
                data = json.load(f)
            
            # Check structure
            if 'cells' not in data or 'metadata' not in data:
                print(f"❌ {notebook.name}: Missing basic structure")
                continue
            
            # Check for outputs
            has_outputs = any(
                cell.get('cell_type') == 'code' and cell.get('outputs')
                for cell in data.get('cells', [])
            )
            
            if has_outputs:
                print(f"⚠️  {notebook.name}: Has outputs")
            else:
                print(f"✅ {notebook.name}: Clean (no outputs)")
                
        except Exception as e:
            print(f"❌ {notebook.name}: Error - {e}")
    
    print()


def check_nbval_compatibility():
    """Check nbval compatibility."""
    print("🔬 nbval Compatibility Check")  
    print("=" * 40)
    
    try:
        import nbval
        print(f"✅ nbval version: {nbval.__version__}")
        
        # Try to run nbval on a notebook
        notebooks = list(Path("notebooks").glob("*.ipynb"))
        if notebooks:
            test_notebook = notebooks[0]
            print(f"Testing nbval on {test_notebook.name}...")
            
            result = run_command(f"python3 -m pytest --nbval {test_notebook}")
            if result.returncode == 0:
                print("✅ nbval test passed")
            else:
                print(f"❌ nbval test failed: {result.stderr}")
                
    except ImportError:
        print("❌ nbval not installed")
    except Exception as e:
        print(f"❌ nbval test error: {e}")
    
    print()


def main():
    """Main debugging function."""
    print("🔍 CI Environment Debugging Script")
    print("=" * 50)
    print()
    
    check_python_environment()
    check_file_system()
    check_imports()
    check_repository_functionality()
    check_notebook_validation()
    check_nbval_compatibility()
    
    print("=" * 50)
    print("🏁 Debug script completed")


if __name__ == "__main__":
    main()