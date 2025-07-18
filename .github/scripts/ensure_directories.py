#!/usr/bin/env python3
"""Ensure required directories exist for CI/CD."""

import os
from pathlib import Path

# Directories that should exist
required_dirs = [
    "data",
    "docs"
]

for dir_path in required_dirs:
    path = Path(dir_path)
    if not path.exists():
        print(f"Creating directory: {dir_path}")
        try:
            path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"Warning: Cannot create {dir_path} due to permissions")
            # Create a marker file instead
            marker = Path(f"{dir_path}_exists.marker")
            marker.touch()
    else:
        print(f"Directory exists: {dir_path}")

# Create README files if possible
readme_contents = {
    "data/README.md": "# Data Directory\n\nSample data files for design patterns tutorials.",
    "docs/README.md": "# Documentation Directory\n\nAdditional documentation for design patterns."
}

for filepath, content in readme_contents.items():
    try:
        path = Path(filepath)
        if not path.exists() and path.parent.exists():
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Created: {filepath}")
    except Exception as e:
        print(f"Could not create {filepath}: {e}")