# examples/autogen_integration.py
"""
Complete AutoGen integration with CERT observability.
Drop-in replacement for standard AutoGen agents with systematic coordination measurement.
"""

import requests
import json
from autogen import ConversableAgent, GroupChat, GroupChatManager
from typing import Dict, List, Optional
import time

class CERTClient:
    """Simple client for CERT observability API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def measure_consistency(self, agent_id: str, prompt: str, responses: List[str]) -> Dict:
        """Measure behavioral consistency for an agent"""
        try:
            response = requests.post(
                f"{self.base_url}/measure/consistency",
                json={
                    "agent_id": agent_id,
                    "prompt": prompt,
                    "responses": responses
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def measure_coordination(self, agent_a_baseline: float, agent_b_baseline: float, 
                           coordinated_performance: float, interaction_pattern: str) -> Dict:
        """Measure coordination effect between agents"""
        try:
            response = requests.post(
                f"{self.base_url}/measure/coordination",
                json={
                    "agent_a_id": "agent_a",
                    "agent_b_id": "agent_b", 
                    "agent_a_baseline": agent_a_baseline,
                    "agent_b_baseline": agent_b_baseline,
                    "coordinated_performance": coordinated_performance,
                    "interaction_pattern": interaction_pattern
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

class CERTInstrumentedAgent(ConversableAgent):
    """AutoGen agent with CERT observability instrumentation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cert_client = CERTClient()
        self.response_history = []
        self.baseline_performance = 0.85  # Default baseline
        
    def generate_reply(self, messages, sender=None, **kwargs):
        """Generate reply with CERT measurement"""
        # Get original response
        response = super().generate_reply(messages, sender, **kwargs)
        
        # Extract prompt for consistency measurement
        prompt = messages[-1]["content"] if messages else ""
        
        # Store response for consistency analysis
        if isinstance(response, str):
            self.response_history.append(response)
            
            # Measure consistency when we have enough responses
            if len(self.response_history) >= 3:
                consistency = self.cert_client.measure_consistency(
                    agent_id=self.name,
                    prompt=prompt,
                    responses=self.response_history[-3:]
                )
                
                if "consistency_score" in consistency:
                    print(f"🔍 Agent {self.name} consistency: {consistency['consistency_score']:.3f}")
                    
                    if consistency["consistency_score"] < 0.7:
                        print(f"⚠️  LOW CONSISTENCY WARNING for {self.name}")
        
        return response
    
    def set_baseline_performance(self, performance: float):
        """Set baseline performance for coordination measurement"""
        self.baseline_performance = performance

class CERTGroupChatManager(GroupChatManager):
    """GroupChat manager with coordination effect measurement"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cert_client = CERTClient()
        self.conversation_quality_history = []
        
    def run_chat(self, *args, **kwargs):
        """Run chat with coordination measurement"""
        print("🚀 Starting CERT-instrumented group chat...")
        
        # Run original chat
        result = super().run_chat(*args, **kwargs)
        
        # Measure coordination effects
        self._measure_group_coordination()
        
        return result
    
    def _measure_group_coordination(self):
        """Measure coordination effects across group chat"""
        # Simple quality assessment (in practice, you'd use more sophisticated metrics)
        estimated_quality = self._estimate_conversation_quality()
        
        if len(self.groupchat.agents) >= 2:
            # Get agent baselines
            agent_a = self.groupchat.agents[0]
            agent_b = self.groupchat.agents[1]
            
            baseline_a = getattr(agent_a, 'baseline_performance', 0.8)
            baseline_b = getattr(agent_b, 'baseline_performance', 0.8)
            
            # Measure coordination effect
            coordination = self.cert_client.measure_coordination(
                agent_a_baseline=baseline_a,
                agent_b_baseline=baseline_b,
                coordinated_performance=estimated_quality,
                interaction_pattern="group_chat"
            )
            
            if "coordination_effect" in coordination:
                gamma = coordination["coordination_effect"]
                print(f"📊 Group coordination effect: γ = {gamma:.3f}")
                
                if gamma < 0.9:
                    print(f"⚠️  COORDINATION DEGRADATION: {coordination['performance_change_percent']:.1f}%")
                elif gamma > 1.1:
                    print(f"✅ COORDINATION BENEFIT: {coordination['performance_change_percent']:.1f}%")
    
    def _estimate_conversation_quality(self) -> float:
        """Estimate conversation quality (placeholder implementation)"""
        # In practice, you'd use more sophisticated evaluation
        # This is a simplified placeholder
        return 0.75

def create_cert_supply_chain_agents():
    """Create instrumented agents for supply chain coordination example"""
    
    # Create CERT-instrumented agents
    forecaster = CERTInstrumentedAgent(
        name="Forecaster",
        llm_config={"model": "gpt-4"},
        system_message="You are a demand forecasting specialist. Analyze trends and predict future demand."
    )
    forecaster.set_baseline_performance(0.87)
    
    optimizer = CERTInstrumentedAgent(
        name="Optimizer", 
        llm_config={"model": "gpt-4"},
        system_message="You are an inventory optimization expert. Optimize stock levels based on demand forecasts."
    )
    optimizer.set_baseline_performance(0.89)
    
    negotiator = CERTInstrumentedAgent(
        name="Negotiator",
        llm_config={"model": "gpt-4"},
        system_message="You are a procurement negotiator. Secure favorable supplier terms based on inventory needs."
    )
    negotiator.set_baseline_performance(0.78)
    
    return [forecaster, optimizer, negotiator]

# Complete working example
def main():
    """Complete supply chain coordination example with CERT measurement"""
    
    print("🔧 Setting up CERT-instrumented supply chain agents...")
    
    # Create agents
    agents = create_cert_supply_chain_agents()
    
    # Create group chat with CERT measurement
    groupchat = GroupChat(
        agents=agents,
        messages=[],
        max_round=10
    )
    
    manager = CERTGroupChatManager(groupchat=groupchat)
    
    # Run coordination task
    task = """
    We need to coordinate our Q4 supply chain strategy:
    1. Forecaster: Predict Q4 demand for our top product lines
    2. Optimizer: Recommend optimal inventory levels
    3. Negotiator: Suggest supplier negotiation strategy
    
    Work together to create a coordinated plan.
    """
    
    print("📋 Starting coordination task...")
    result = manager.run_chat(
        message=task,
        max_turns=10
    )
    
    print("✅ Coordination task completed with CERT measurement!")
    return result

if __name__ == "__main__":
    main()