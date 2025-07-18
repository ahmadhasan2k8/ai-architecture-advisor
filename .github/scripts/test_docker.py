#!/usr/bin/env python3
"""Test Docker image imports."""

import sys
sys.path.append('/home/jupyter/work/src')

try:
    from patterns.singleton import singleton
    from patterns.factory import ShapeFactory
    from patterns.repository import User, SqliteUserRepository
    from patterns.observer import WeatherStation
    print('✅ Docker image working correctly - all pattern imports successful')
    sys.exit(0)
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)