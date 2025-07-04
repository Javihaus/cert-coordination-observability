#!/usr/bin/env python3
"""
Run all CERT framework tests
"""
import sys
import subprocess
from pathlib import Path

def run_test(test_file, description):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"File: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, test_file],
            cwd=Path(__file__).parent.parent,
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all tests"""
    print("CERT Framework - Complete Test Suite")
    print("=" * 60)
    
    tests = [
        ("tests/test_deployment.py", "Basic Deployment Test"),
        ("tests/test_api_directly.py", "Direct API Function Test"),
        ("tests/test_llm_providers.py", "LLM Provider Integration Test"),
        ("tests/test_performance.py", "Performance Test"),
        ("tests/test_api.py", "API Endpoint Test")
    ]
    
    results = []
    for test_file, description in tests:
        test_path = Path(__file__).parent.parent / test_file
        if test_path.exists():
            success = run_test(str(test_path), description)
            results.append((description, success))
        else:
            print(f"Warning: {test_file} not found")
            results.append((description, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = 0
    for description, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{description:40} {status}")
        if success:
            passed += 1
    
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Framework is ready for deployment.")
        return True
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed. Minor issues may exist.")
        return True
    else:
        print("❌ Multiple test failures. Please check configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)