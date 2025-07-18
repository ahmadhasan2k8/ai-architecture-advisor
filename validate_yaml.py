#!/usr/bin/env python3
"""Validate YAML files in the project."""

import yaml
import sys

def validate_yaml(filepath):
    """Validate a YAML file."""
    try:
        with open(filepath, 'r') as file:
            yaml.safe_load(file)
        print(f"✅ {filepath} is valid YAML")
        return True
    except yaml.YAMLError as e:
        print(f"❌ {filepath} has YAML errors:")
        print(f"   {e}")
        return False

if __name__ == "__main__":
    files_to_check = [
        ".github/workflows/ci.yml",
        "docker-compose.yml"
    ]
    
    all_valid = True
    for file in files_to_check:
        if not validate_yaml(file):
            all_valid = False
    
    sys.exit(0 if all_valid else 1)