#!/usr/bin/env python3
"""
Test script to verify CERT framework deployment
"""
import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_python_version():
    """Test Python version compatibility"""
    print("Testing Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("ERROR: Python 3.8+ required")
        return False
    print("✓ Python version OK")
    return True

def test_imports():
    """Test critical imports"""
    print("\nTesting imports...")
    try:
        import fastapi
        print("✓ FastAPI imported")
        
        import uvicorn
        print("✓ Uvicorn imported")
        
        import numpy as np
        print("✓ NumPy imported")
        
        from cert.core.behavioral_analysis import BehavioralAnalyzer
        print("✓ BehavioralAnalyzer imported")
        
        from cert.core.coordination_effects import CoordinationAnalyzer
        print("✓ CoordinationAnalyzer imported")
        
        return True
    except ImportError as e:
        print(f"ERROR: Import failed - {e}")
        return False

def test_basic_functionality():
    """Test basic CERT functionality"""
    print("\nTesting basic functionality...")
    try:
        from cert.core.behavioral_analysis import BehavioralAnalyzer
        from cert.core.coordination_effects import CoordinationAnalyzer
        
        # Test behavioral analyzer
        analyzer = BehavioralAnalyzer()
        responses = ["Hello world", "Hi there", "Hey there"]
        result = analyzer.measure_consistency("test_agent", "greeting", responses)
        
        if "error" in result:
            print(f"ERROR: BehavioralAnalyzer failed - {result['error']}")
            return False
        print("✓ BehavioralAnalyzer working")
        
        # Test coordination analyzer
        coord_analyzer = CoordinationAnalyzer()
        result = coord_analyzer.calculate_coordination_effect(0.8, 0.9, 0.75, "sequential")
        
        if "error" in result:
            print(f"ERROR: CoordinationAnalyzer failed - {result['error']}")
            return False
        print("✓ CoordinationAnalyzer working")
        
        return True
    except Exception as e:
        print(f"ERROR: Functionality test failed - {e}")
        return False

def main():
    """Run all tests"""
    print("CERT Framework Deployment Test")
    print("=" * 40)
    
    tests = [
        test_python_version,
        test_imports,
        test_basic_functionality
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        else:
            break
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✓ All tests passed! Ready for deployment.")
        return True
    else:
        print("✗ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)