#!/usr/bin/env python3
"""
Test script for LLM providers (Claude, Deepseek, Llama) with CERT framework
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_environment():
    """Load environment variables"""
    load_dotenv()
    
    # Check if API keys are configured
    claude_key = os.getenv('CLAUDE_API_KEY')
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if not claude_key or claude_key == 'your_claude_key_here':
        print("⚠️  CLAUDE_API_KEY not configured")
    else:
        print("✓ Claude API key configured")
    
    if not hf_key or hf_key == 'your_hf_key_here':
        print("⚠️  HUGGINGFACE_API_KEY not configured")
    else:
        print("✓ Hugging Face API key configured")

async def test_claude_provider():
    """Test Claude provider"""
    print("\n=== Testing Claude Provider ===")
    try:
        from ll_providers.claude import ClaudeProvider
        
        claude = ClaudeProvider()
        info = claude.get_provider_info()
        print(f"Provider: {info['provider']}")
        print(f"API Key Configured: {info['api_key_configured']}")
        print(f"Available Models: {info['models']}")
        
        if info['api_key_configured']:
            prompt = "Explain quantum computing in one sentence."
            response = await claude.generate(prompt)
            print(f"Test Response: {response[:100]}...")
            return True
        else:
            print("Skipping generation test - API key not configured")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_huggingface_provider():
    """Test Hugging Face provider with default model"""
    print("\n=== Testing Hugging Face Provider (Default) ===")
    try:
        from ll_providers.huggingface import HuggingFaceProvider
        
        hf = HuggingFaceProvider()
        info = hf.get_provider_info()
        print(f"Provider: {info['provider']}")
        print(f"API Key Configured: {info['api_key_configured']}")
        print(f"Current Model: {info['current_model']}")
        print(f"Supported Models: {len(info['supported_models'])} models")
        
        if info['api_key_configured']:
            prompt = "Hello, how are you?"
            response = await hf.generate(prompt)
            print(f"Test Response: {response[:100]}...")
            return True
        else:
            print("Skipping generation test - API key not configured")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_deepseek_provider():
    """Test Deepseek provider"""
    print("\n=== Testing Deepseek Provider ===")
    try:
        from ll_providers.huggingface import HuggingFaceProvider
        
        deepseek = HuggingFaceProvider.create_deepseek_provider()
        info = deepseek.get_provider_info()
        print(f"Provider: {info['provider']}")
        print(f"API Key Configured: {info['api_key_configured']}")
        print(f"Current Model: {info['current_model']}")
        
        if info['api_key_configured']:
            prompt = "Write a simple Python function to add two numbers."
            response = await deepseek.generate(prompt, max_tokens=150)
            print(f"Test Response: {response[:100]}...")
            return True
        else:
            print("Skipping generation test - API key not configured")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_llama_provider():
    """Test Llama provider"""
    print("\n=== Testing Llama Provider ===")
    try:
        from ll_providers.huggingface import HuggingFaceProvider
        
        llama = HuggingFaceProvider.create_llama_provider(model_size="7b")
        info = llama.get_provider_info()
        print(f"Provider: {info['provider']}")
        print(f"API Key Configured: {info['api_key_configured']}")
        print(f"Current Model: {info['current_model']}")
        
        if info['api_key_configured']:
            prompt = "What is artificial intelligence?"
            response = await llama.generate(prompt, max_tokens=100)
            print(f"Test Response: {response[:100]}...")
            return True
        else:
            print("Skipping generation test - API key not configured")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

async def test_cert_integration():
    """Test CERT framework integration with multiple providers"""
    print("\n=== Testing CERT Framework Integration ===")
    try:
        from cert.core.behavioral_analysis import BehavioralAnalyzer
        from ll_providers.claude import ClaudeProvider
        from ll_providers.huggingface import HuggingFaceProvider
        
        analyzer = BehavioralAnalyzer()
        prompt = "Explain machine learning briefly."
        
        # Collect responses from different providers
        responses = []
        
        # Try Claude
        try:
            claude = ClaudeProvider()
            if claude.get_provider_info()['api_key_configured']:
                response = await claude.generate(prompt)
                responses.append(response)
                print("✓ Claude response collected")
        except Exception as e:
            print(f"Claude error: {e}")
        
        # Try Hugging Face default
        try:
            hf = HuggingFaceProvider()
            if hf.get_provider_info()['api_key_configured']:
                response = await hf.generate(prompt)
                responses.append(response)
                print("✓ Hugging Face response collected")
        except Exception as e:
            print(f"Hugging Face error: {e}")
        
        # Try Deepseek
        try:
            deepseek = HuggingFaceProvider.create_deepseek_provider()
            if deepseek.get_provider_info()['api_key_configured']:
                response = await deepseek.generate(prompt)
                responses.append(response)
                print("✓ Deepseek response collected")
        except Exception as e:
            print(f"Deepseek error: {e}")
        
        if len(responses) >= 2:
            # Analyze consistency
            result = analyzer.measure_consistency("multi_provider_test", prompt, responses)
            print(f"Consistency Analysis:")
            print(f"  - Consistency Score: {result.get('consistency_score', 'N/A')}")
            print(f"  - Number of Responses: {result.get('num_responses', 'N/A')}")
            print(f"  - Mean Distance: {result.get('mean_semantic_distance', 'N/A')}")
            return True
        else:
            print("Not enough responses for consistency analysis")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("CERT Framework - LLM Provider Tests")
    print("=" * 50)
    
    setup_environment()
    
    tests = [
        test_claude_provider,
        test_huggingface_provider,
        test_deepseek_provider,
        test_llama_provider,
        test_cert_integration
    ]
    
    passed = 0
    for test in tests:
        try:
            if await test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} failed: {e}")
    
    print(f"\n{passed}/{len(tests)} tests passed")
    
    if passed >= 3:  # At least basic functionality working
        print("✓ LLM providers are ready for use!")
    else:
        print("⚠️  Some issues detected. Check API keys and configuration.")

if __name__ == "__main__":
    asyncio.run(main())