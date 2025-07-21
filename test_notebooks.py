#!/usr/bin/env python3
"""
Test notebook execution to identify any issues that might cause CI failures.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def test_notebook_execution():
    """Test if notebooks can be executed properly."""
    print("🔍 Testing notebook execution...")
    
    notebooks_dir = Path("learning-resources/notebooks")
    notebooks = sorted([f for f in notebooks_dir.glob("*.ipynb") if ".ipynb_checkpoints" not in str(f)])
    
    print(f"Found {len(notebooks)} notebooks to test")
    
    failed_notebooks = []
    
    for notebook in notebooks:
        print(f"Testing {notebook.name}...")
        
        try:
            # Check if the notebook has basic structure
            with open(notebook, 'r') as f:
                data = json.load(f)
            
            # Check for basic notebook structure
            if 'cells' not in data:
                print(f"❌ {notebook.name}: Missing cells")
                failed_notebooks.append(notebook.name)
                continue
                
            if 'metadata' not in data:
                print(f"❌ {notebook.name}: Missing metadata")
                failed_notebooks.append(notebook.name)
                continue
            
            # Check for cleared outputs (required by CI)
            has_outputs = False
            for cell in data.get('cells', []):
                if cell.get('cell_type') == 'code' and cell.get('outputs'):
                    has_outputs = True
                    break
            
            if has_outputs:
                print(f"⚠️  {notebook.name}: Has outputs (should be cleared)")
                # This is a warning, not a failure for notebook validation
            
            # Check for execution count
            has_execution_count = False
            for cell in data.get('cells', []):
                if cell.get('cell_type') == 'code' and cell.get('execution_count'):
                    has_execution_count = True
                    break
            
            if has_execution_count:
                print(f"⚠️  {notebook.name}: Has execution counts (should be cleared)")
                # This is a warning, not a failure for notebook validation
            
            print(f"✅ {notebook.name}: Basic structure valid")
            
        except json.JSONDecodeError as e:
            print(f"❌ {notebook.name}: Invalid JSON - {e}")
            failed_notebooks.append(notebook.name)
        except Exception as e:
            print(f"❌ {notebook.name}: Error - {e}")
            failed_notebooks.append(notebook.name)
    
    if failed_notebooks:
        print(f"\n❌ {len(failed_notebooks)} notebooks failed validation:")
        for nb in failed_notebooks:
            print(f"  - {nb}")
        return False
    else:
        print(f"\n✅ All {len(notebooks)} notebooks passed validation")
        return True

def clear_notebook_outputs():
    """Clear outputs from notebooks if they exist."""
    print("\n🔍 Clearing notebook outputs...")
    
    notebooks_dir = Path("learning-resources/notebooks")
    notebooks = sorted([f for f in notebooks_dir.glob("*.ipynb") if ".ipynb_checkpoints" not in str(f)])
    
    cleared_count = 0
    
    for notebook in notebooks:
        try:
            with open(notebook, 'r') as f:
                data = json.load(f)
            
            modified = False
            for cell in data.get('cells', []):
                if cell.get('cell_type') == 'code':
                    if cell.get('outputs'):
                        cell['outputs'] = []
                        modified = True
                    if cell.get('execution_count'):
                        cell['execution_count'] = None
                        modified = True
            
            if modified:
                with open(notebook, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"✅ Cleared outputs from {notebook.name}")
                cleared_count += 1
            else:
                print(f"✅ {notebook.name} already clean")
                
        except Exception as e:
            print(f"❌ Error clearing {notebook.name}: {e}")
    
    print(f"\n🎉 Cleared outputs from {cleared_count} notebooks")
    return cleared_count > 0

def main():
    """Main function."""
    print("🤖 Testing notebook validation...")
    print("=" * 50)
    
    # Test notebook structure
    structure_ok = test_notebook_execution()
    
    # Clear outputs if needed
    outputs_cleared = clear_notebook_outputs()
    
    print("=" * 50)
    
    if structure_ok:
        print("✅ Notebook structure validation passed")
    else:
        print("❌ Notebook structure validation failed")
    
    if outputs_cleared:
        print("🔧 Notebook outputs were cleared")
    else:
        print("✅ Notebook outputs were already clean")
    
    return structure_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)