#!/usr/bin/env python3
"""
Test script to verify CERT API functionality
"""
import requests
import json
import time
import sys

def test_health_endpoint(base_url):
    """Test health check endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_consistency_endpoint(base_url):
    """Test behavioral consistency endpoint"""
    try:
        test_data = {
            "agent_id": "test_agent_1",
            "prompt": "What is the capital of France?",
            "responses": [
                "The capital of France is Paris.",
                "Paris is the capital of France.",
                "France's capital city is Paris."
            ]
        }
        
        response = requests.post(f"{base_url}/measure/consistency", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Consistency test passed - Score: {result.get('consistency_score', 'N/A')}")
            return True
        else:
            print(f"✗ Consistency test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Consistency test error: {e}")
        return False

def test_coordination_endpoint(base_url):
    """Test coordination effect endpoint"""
    try:
        test_data = {
            "agent_a_id": "agent_a",
            "agent_b_id": "agent_b",
            "agent_a_baseline": 0.8,
            "agent_b_baseline": 0.9,
            "coordinated_performance": 0.75,
            "interaction_pattern": "sequential"
        }
        
        response = requests.post(f"{base_url}/measure/coordination", json=test_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Coordination test passed - Effect: {result.get('coordination_effect', 'N/A')}")
            return True
        else:
            print(f"✗ Coordination test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Coordination test error: {e}")
        return False

def main():
    """Run API tests"""
    base_url = "http://localhost:8000"
    
    print("CERT API Test Suite")
    print("=" * 30)
    print(f"Testing API at: {base_url}")
    print("Make sure the server is running with: python3 start_server.py")
    print()
    
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/health", timeout=1)
            if response.status_code == 200:
                print("Server is ready!")
                break
        except:
            pass
        time.sleep(1)
        if i == max_retries - 1:
            print("Server not responding. Please check if it's running.")
            sys.exit(1)
    
    # Run tests
    tests = [
        test_health_endpoint,
        test_consistency_endpoint,
        test_coordination_endpoint
    ]
    
    passed = 0
    for test in tests:
        if test(base_url):
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("✓ All API tests passed! CERT framework is working correctly.")
    else:
        print("✗ Some API tests failed. Please check the server logs.")

if __name__ == "__main__":
    main()