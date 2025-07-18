#!/usr/bin/env python3
"""
Simple test runner to identify failing tests without pytest version requirements.
"""

import sys
import os
import traceback
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

def test_singleton_basic():
    """Test singleton pattern basic functionality."""
    print("Testing singleton pattern...")
    try:
        from patterns.singleton import singleton
        
        @singleton
        class TestService:
            def __init__(self):
                self.value = 42
        
        s1 = TestService()
        s2 = TestService()
        assert s1 is s2
        print("✅ Singleton basic test passed")
        return True
    except Exception as e:
        print(f"❌ Singleton basic test failed: {e}")
        traceback.print_exc()
        return False

def test_repository_sqlite():
    """Test SQLite repository functionality."""
    print("Testing SQLite repository...")
    try:
        from patterns.repository import SqliteUserRepository, User
        
        repo = SqliteUserRepository(':memory:')
        user = User(id=None, name='Test User', email='test@example.com')
        saved_user = repo.save(user)
        
        assert saved_user.id == 1
        assert saved_user.name == 'Test User'
        
        found_user = repo.find_by_id(1)
        assert found_user is not None
        assert found_user.name == 'Test User'
        
        print("✅ SQLite repository test passed")
        return True
    except Exception as e:
        print(f"❌ SQLite repository test failed: {e}")
        traceback.print_exc()
        return False

def test_repository_json_file():
    """Test JSON file repository functionality."""
    print("Testing JSON file repository...")
    try:
        from patterns.repository import JsonFileUserRepository, User
        
        # Test with new file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            repo = JsonFileUserRepository(temp_path)
            assert len(repo._users) == 0
            assert repo._next_id == 1
            
            user = User(id=None, name='Test User', email='test@example.com')
            saved_user = repo.save(user)
            assert saved_user.id == 1
            
            print("✅ JSON file repository new file test passed")
            
            # Test with existing file
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
                repo2 = JsonFileUserRepository(temp_path2)
                assert len(repo2._users) == 1
                assert repo2._next_id == 2
                assert repo2._users[0].name == 'Alice'
                print("✅ JSON file repository existing file test passed")
                
            finally:
                os.unlink(temp_path2)
            
        finally:
            os.unlink(temp_path)
            
        return True
        
    except Exception as e:
        print(f"❌ JSON file repository test failed: {e}")
        traceback.print_exc()
        return False

def test_factory_pattern():
    """Test factory pattern functionality."""
    print("Testing factory pattern...")
    try:
        from patterns.factory import ShapeFactory, NotificationFactory
        
        # Test shape factory
        circle = ShapeFactory.create_shape('circle', radius=5)
        assert circle.radius == 5
        assert abs(circle.area() - 78.53981633974483) < 0.001
        
        # Test notification factory
        email = NotificationFactory.create_notifier('email')
        assert email.smtp_server == 'smtp.gmail.com'
        
        print("✅ Factory pattern test passed")
        return True
    except Exception as e:
        print(f"❌ Factory pattern test failed: {e}")
        traceback.print_exc()
        return False

def test_observer_pattern():
    """Test observer pattern functionality."""
    print("Testing observer pattern...")
    try:
        from patterns.observer import WeatherStation, CurrentConditionsDisplay
        
        station = WeatherStation()
        display = CurrentConditionsDisplay()
        
        station.register_observer(display)
        assert len(station._observers) == 1
        
        station.set_measurements(25.0, 65.0, 1013.0)
        # Should not raise any exceptions
        
        print("✅ Observer pattern test passed")
        return True
    except Exception as e:
        print(f"❌ Observer pattern test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🤖 Running simple test suite...")
    print("=" * 50)
    
    tests = [
        test_singleton_basic,
        test_repository_sqlite,
        test_repository_json_file,
        test_factory_pattern,
        test_observer_pattern,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"❌ {failed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)