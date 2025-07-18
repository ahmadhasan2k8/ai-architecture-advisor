#!/usr/bin/env python3
"""Test Docker image imports."""

import sys
sys.path.append('/home/jupyter/work/src')

try:
    from patterns import Singleton, ComputerBuilder
    print('✅ Docker image working correctly')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)