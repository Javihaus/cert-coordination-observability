#!/usr/bin/env python3
"""
Performance Test for CERT Framework with Real API Keys
"""
import os
import sys
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
load_dotenv()

async def test_claude_performance():
    """Test Claude API performance"""
    print("=== Testing Claude Performance ===")
    
    try:
        from ll_providers.claude import ClaudeProvider
        
        start_time = time.time()
        claude = ClaudeProvider()
        
        # Test prompt
        prompt = "Explain artificial intelligence in 2 sentences."
        
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        api_start = time.time()
        response = await claude.generate(prompt, max_tokens=100)
        api_end = time.time()
        
        print(f"Response: {response}")
        print(f"API Response Time: {api_end - api_start:.2f}s")
        print(f"Total Time: {time.time() - start_time:.2f}s")
        
        return True, response
        
    except Exception as e:
        print(f"Claude test failed: {e}")
        return False, str(e)

async def test_huggingface_performance():
    """Test Hugging Face API performance"""
    print("\n=== Testing Hugging Face Performance ===")
    
    try:
        from ll_providers.huggingface import HuggingFaceProvider
        
        start_time = time.time()
        hf = HuggingFaceProvider()
        
        # Test prompt
        prompt = "Hello, how are you today?"
        
        print(f"Model: {hf.model_name}")
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        api_start = time.time()
        response = await hf.generate(prompt, max_tokens=50)
        api_end = time.time()
        
        print(f"Response: {response}")
        print(f"API Response Time: {api_end - api_start:.2f}s")
        print(f"Total Time: {time.time() - start_time:.2f}s")
        
        return True, response
        
    except Exception as e:
        print(f"Hugging Face test failed: {e}")
        return False, str(e)

async def test_deepseek_performance():
    """Test Deepseek model performance"""
    print("\n=== Testing Deepseek Performance ===")
    
    try:
        from ll_providers.huggingface import HuggingFaceProvider
        
        start_time = time.time()
        deepseek = HuggingFaceProvider.create_deepseek_provider()
        
        # Test prompt
        prompt = "Write a simple Python function to calculate factorial:"
        
        print(f"Model: {deepseek.model_name}")
        print(f"Prompt: {prompt}")
        print("Generating response...")
        
        api_start = time.time()
        response = await deepseek.generate(prompt, max_tokens=100)
        api_end = time.time()
        
        print(f"Response: {response}")
        print(f"API Response Time: {api_end - api_start:.2f}s")
        print(f"Total Time: {time.time() - start_time:.2f}s")
        
        return True, response
        
    except Exception as e:
        print(f"Deepseek test failed: {e}")
        return False, str(e)

async def test_cert_consistency():
    """Test CERT behavioral consistency analysis"""
    print("\n=== Testing CERT Consistency Analysis ===")
    
    try:
        from cert.core.behavioral_analysis import BehavioralAnalyzer
        
        analyzer = BehavioralAnalyzer()
        
        # Test with varied responses
        responses = [
            "Machine learning is a subset of AI that learns from data.",
            "ML is part of artificial intelligence focused on learning patterns.",
            "Machine learning uses algorithms to find patterns in data automatically."
        ]
        
        start_time = time.time()
        result = analyzer.measure_consistency(
            agent_id="test_agent",
            prompt="What is machine learning?",
            responses=responses
        )
        end_time = time.time()
        
        print(f"Analysis completed in {end_time - start_time:.2f}s")
        print(f"Consistency Score: {result.get('consistency_score', 'N/A'):.3f}")
        print(f"Mean Semantic Distance: {result.get('mean_semantic_distance', 'N/A'):.3f}")
        print(f"Standard Deviation: {result.get('std_semantic_distance', 'N/A'):.3f}")
        
        return True, result
        
    except Exception as e:
        print(f"CERT consistency test failed: {e}")
        return False, str(e)

async def test_cert_coordination():
    """Test CERT coordination effect analysis"""
    print("\n=== Testing CERT Coordination Analysis ===")
    
    try:
        from cert.core.coordination_effects import CoordinationAnalyzer
        
        analyzer = CoordinationAnalyzer()
        
        start_time = time.time()
        result = analyzer.calculate_coordination_effect(
            agent_a_baseline=0.85,  # Claude performance
            agent_b_baseline=0.80,  # Deepseek performance
            coordinated_performance=0.88,  # Combined performance
            interaction_pattern="sequential"
        )
        end_time = time.time()
        
        print(f"Analysis completed in {end_time - start_time:.3f}s")
        print(f"Coordination Effect (γ): {result.get('coordination_effect', 'N/A'):.3f}")
        print(f"Impact Classification: {result.get('impact_classification', 'N/A')}")
        print(f"Performance Change: {result.get('performance_change_percent', 'N/A'):.1f}%")
        
        return True, result
        
    except Exception as e:
        print(f"CERT coordination test failed: {e}")
        return False, str(e)

async def run_full_performance_test():
    """Run comprehensive performance test"""
    print("CERT Framework Performance Test")
    print("=" * 50)
    
    total_start = time.time()
    
    # Test all components
    tests = [
        ("Claude API", test_claude_performance),
        ("Hugging Face API", test_huggingface_performance),
        ("Deepseek Model", test_deepseek_performance),
        ("CERT Consistency", test_cert_consistency),
        ("CERT Coordination", test_cert_coordination)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success, result = await test_func()
            results.append((test_name, success, result))
        except Exception as e:
            print(f"Test {test_name} crashed: {e}")
            results.append((test_name, False, str(e)))
    
    total_end = time.time()
    
    # Summary
    print("\n" + "="*50)
    print("PERFORMANCE TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, result in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name:20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    print(f"Total execution time: {total_end - total_start:.2f}s")
    
    if passed >= 3:
        print("🎉 Framework is performing well!")
    else:
        print("⚠️  Some performance issues detected")

if __name__ == "__main__":
    asyncio.run(run_full_performance_test())