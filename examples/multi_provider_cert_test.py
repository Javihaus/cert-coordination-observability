#!/usr/bin/env python3
"""
Example: Multi-Provider CERT Analysis
Demonstrates how to use Claude, Deepseek, and Llama for coordination observability
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def run_multi_provider_consistency_test():
    """Run consistency analysis across multiple LLM providers"""
    print("Multi-Provider Consistency Analysis")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    from cert.core.behavioral_analysis import BehavioralAnalyzer
    from ll_providers.claude import ClaudeProvider
    from ll_providers.huggingface import HuggingFaceProvider
    
    analyzer = BehavioralAnalyzer()
    
    # Test prompts
    prompts = [
        "Explain the concept of machine learning in simple terms.",
        "What are the benefits of renewable energy?",
        "How does blockchain technology work?"
    ]
    
    # Initialize providers
    providers = {}
    
    # Claude
    try:
        claude = ClaudeProvider()
        if claude.get_provider_info()['api_key_configured']:
            providers['claude'] = claude
    except Exception as e:
        print(f"Claude initialization failed: {e}")
    
    # Deepseek
    try:
        deepseek = HuggingFaceProvider.create_deepseek_provider()
        if deepseek.get_provider_info()['api_key_configured']:
            providers['deepseek'] = deepseek
    except Exception as e:
        print(f"Deepseek initialization failed: {e}")
    
    # Llama
    try:
        llama = HuggingFaceProvider.create_llama_provider(model_size="7b")
        if llama.get_provider_info()['api_key_configured']:
            providers['llama'] = llama
    except Exception as e:
        print(f"Llama initialization failed: {e}")
    
    if not providers:
        print("No providers available. Please configure API keys in .env file.")
        return
    
    print(f"Available providers: {list(providers.keys())}")
    
    # Run tests for each prompt
    for i, prompt in enumerate(prompts):
        print(f"\n--- Test {i+1}: {prompt[:50]}... ---")
        
        responses = []
        response_sources = []
        
        # Collect responses from all providers
        for provider_name, provider in providers.items():
            try:
                response = await provider.generate(prompt, max_tokens=200)
                responses.append(response)
                response_sources.append(provider_name)
                print(f"✓ {provider_name}: {response[:80]}...")
            except Exception as e:
                print(f"✗ {provider_name}: Error - {e}")
        
        # Analyze consistency if we have multiple responses
        if len(responses) >= 2:
            result = analyzer.measure_consistency(
                agent_id=f"multi_provider_test_{i+1}",
                prompt=prompt,
                responses=responses
            )
            
            print(f"\nConsistency Analysis:")
            print(f"  Consistency Score: {result.get('consistency_score', 'N/A'):.3f}")
            print(f"  Mean Semantic Distance: {result.get('mean_semantic_distance', 'N/A'):.3f}")
            print(f"  Standard Deviation: {result.get('std_semantic_distance', 'N/A'):.3f}")
            print(f"  Providers: {', '.join(response_sources)}")
            
            # Interpretation
            score = result.get('consistency_score', 0)
            if score > 0.8:
                print("  → High consistency across providers")
            elif score > 0.6:
                print("  → Moderate consistency across providers")
            else:
                print("  → Low consistency across providers")
        else:
            print("Not enough responses for consistency analysis")

async def run_coordination_effect_simulation():
    """Simulate coordination effects between different LLM providers"""
    print("\n\nCoordination Effect Simulation")
    print("=" * 50)
    
    from cert.core.coordination_effects import CoordinationAnalyzer
    
    coord_analyzer = CoordinationAnalyzer()
    
    # Simulate different coordination scenarios
    scenarios = [
        {
            "name": "Claude + Deepseek Collaboration",
            "agent_a_baseline": 0.85,  # Claude baseline
            "agent_b_baseline": 0.80,  # Deepseek baseline
            "coordinated_performance": 0.75,  # Actual coordinated result
            "interaction_pattern": "sequential"
        },
        {
            "name": "Llama + Claude Collaboration", 
            "agent_a_baseline": 0.75,  # Llama baseline
            "agent_b_baseline": 0.85,  # Claude baseline
            "coordinated_performance": 0.82,  # Actual coordinated result
            "interaction_pattern": "parallel"
        },
        {
            "name": "All Three Providers",
            "agent_a_baseline": 0.80,  # Average of all three
            "agent_b_baseline": 0.80,  # Average of all three
            "coordinated_performance": 0.85,  # Coordinated result
            "interaction_pattern": "ensemble"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n--- {scenario['name']} ---")
        
        result = coord_analyzer.calculate_coordination_effect(
            agent_a_baseline=scenario['agent_a_baseline'],
            agent_b_baseline=scenario['agent_b_baseline'],
            coordinated_performance=scenario['coordinated_performance'],
            interaction_pattern=scenario['interaction_pattern']
        )
        
        print(f"Expected Performance: {result.get('expected_performance', 'N/A'):.3f}")
        print(f"Observed Performance: {result.get('observed_performance', 'N/A'):.3f}")
        print(f"Coordination Effect (γ): {result.get('coordination_effect', 'N/A'):.3f}")
        print(f"Impact Classification: {result.get('impact_classification', 'N/A')}")
        print(f"Performance Change: {result.get('performance_change_percent', 'N/A'):.1f}%")
        
        # Interpretation
        gamma = result.get('coordination_effect', 0)
        if gamma > 1.2:
            print("  → Coordination provides significant benefits")
        elif gamma > 1.0:
            print("  → Coordination provides moderate benefits")
        elif gamma > 0.8:
            print("  → Coordination causes some degradation")
        else:
            print("  → Coordination causes significant degradation")

async def main():
    """Run the complete multi-provider CERT analysis"""
    print("CERT Framework - Multi-Provider Analysis Example")
    print("=" * 60)
    
    await run_multi_provider_consistency_test()
    await run_coordination_effect_simulation()
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("This example demonstrates how CERT framework can measure:")
    print("1. Behavioral consistency across different LLM providers")
    print("2. Coordination effects in multi-agent scenarios")
    print("3. Real-world applicability for AI system observability")

if __name__ == "__main__":
    asyncio.run(main())