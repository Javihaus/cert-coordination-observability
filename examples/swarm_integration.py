# examples/swarm_integration.py
"""
Complete Swarm integration with CERT observability.
Drop-in instrumentation for Swarm agents with systematic coordination measurement.
"""

import requests
import json
from swarm import Swarm, Agent
from typing import Dict, List, Optional, Callable
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

class CERTInstrumentedSwarm(Swarm):
    """Swarm client with CERT observability instrumentation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cert_client = CERTClient()
        self.agent_response_history = {}
        self.agent_baselines = {}
        self.handoff_measurements = []
        
    def run(self, agent, messages, *args, **kwargs):
        """Run with CERT measurement"""
        print(f"🔍 CERT measuring execution for agent: {agent.name}")
        
        # Store initial agent for handoff measurement
        initial_agent = agent
        
        # Run original execution
        result = super().run(agent, messages, *args, **kwargs)
        
        # Measure response consistency
        if hasattr(result, 'messages') and result.messages:
            self._measure_agent_consistency(agent, messages, result.messages)
            
        # Measure handoff coordination if agent changed
        if hasattr(result, 'agent') and result.agent != initial_agent:
            self._measure_handoff_coordination(initial_agent, result.agent)
        
        return result
    
    def _measure_agent_consistency(self, agent, input_messages, output_messages):
        """Measure consistency of agent responses"""
        agent_name = agent.name
        
        # Extract latest response
        if output_messages:
            latest_response = output_messages[-1].get('content', '')
            input_prompt = input_messages[-1].get('content', '') if input_messages else ''
            
            # Store response history
            if agent_name not in self.agent_response_history:
                self.agent_response_history[agent_name] = []
                
            self.agent_response_history[agent_name].append(latest_response)
            
            # Measure consistency when we have enough responses
            if len(self.agent_response_history[agent_name]) >= 3:
                consistency = self.cert_client.measure_consistency(
                    agent_id=agent_name,
                    prompt=input_prompt,
                    responses=self.agent_response_history[agent_name][-3:]
                )
                
                if "consistency_score" in consistency:
                    print(f"📊 Agent {agent_name} consistency: {consistency['consistency_score']:.3f}")
                    
                    if consistency["consistency_score"] < 0.7:
                        print(f"⚠️  LOW CONSISTENCY WARNING for {agent_name}")
    
    def _measure_handoff_coordination(self, from_agent, to_agent):
        """Measure coordination effect during agent handoff"""
        from_baseline = self.agent_baselines.get(from_agent.name, 0.8)
        to_baseline = self.agent_baselines.get(to_agent.name, 0.8)
        
        # Simple quality estimation (in practice, use more sophisticated metrics)
        estimated_quality = self._estimate_handoff_quality()
        
        coordination = self.cert_client.measure_coordination(
            agent_a_baseline=from_baseline,
            agent_b_baseline=to_baseline,
            coordinated_performance=estimated_quality,
            interaction_pattern=f"{from_agent.name}_to_{to_agent.name}_handoff"
        )
        
        if "coordination_effect" in coordination:
            gamma = coordination["coordination_effect"]
            print(f"🔄 Handoff coordination effect: γ = {gamma:.3f}")
            
            if gamma < 0.9:
                print(f"⚠️  HANDOFF DEGRADATION: {coordination['performance_change_percent']:.1f}%")
            elif gamma > 1.1:
                print(f"✅ HANDOFF BENEFIT: {coordination['performance_change_percent']:.1f}%")
                
            self.handoff_measurements.append(coordination)
    
    def _estimate_handoff_quality(self) -> float:
        """Estimate handoff quality (placeholder implementation)"""
        # In practice, you'd use more sophisticated evaluation
        return 0.75
    
    def set_agent_baseline(self, agent_name: str, baseline: float):
        """Set baseline performance for an agent"""
        self.agent_baselines[agent_name] = baseline
        print(f"📈 Set baseline for {agent_name}: {baseline:.3f}")

def create_cert_supply_chain_agents():
    """Create instrumented Swarm agents for supply chain coordination"""
    
    def analyze_demand_trends():
        """Forecasting agent function"""
        return """
        Based on current market data:
        - Q4 demand expected to increase 15% 
        - Holiday season driving consumer electronics
        - Supply chain constraints may limit availability
        
        Transferring to inventory optimizer...
        """
    
    def optimize_inventory_levels():
        """Inventory optimization agent function"""
        return """
        Inventory recommendations based on demand forecast:
        - Increase electronics inventory by 20%
        - Maintain safety stock of 2 weeks
        - Focus on high-velocity items
        
        Transferring to negotiation specialist...
        """
    
    def negotiate_supplier_terms():
        """Negotiation agent function"""
        return """
        Supplier negotiation strategy:
        - Leverage increased volume for 12% discount
        - Secure flexible delivery terms
        - Establish backup suppliers for critical items
        
        Coordination complete.
        """
    
    # Create agents with handoff functions
    forecaster = Agent(
        name="Forecaster",
        instructions="You are a demand forecasting specialist. Analyze market trends and predict future demand.",
        functions=[analyze_demand_trends]
    )
    
    optimizer = Agent(
        name="Optimizer",
        instructions="You are an inventory optimization expert. Create optimal stock strategies based on demand forecasts.",
        functions=[optimize_inventory_levels] 
    )
    
    negotiator = Agent(
        name="Negotiator",
        instructions="You are a procurement negotiator. Develop supplier strategies based on inventory requirements.",
        functions=[negotiate_supplier_terms]
    )
    
    return forecaster, optimizer, negotiator

def create_cert_handoff_function(target_agent: Agent):
    """Create a handoff function that includes CERT measurement"""
    def handoff_with_measurement():
        print(f"🔄 CERT-measured handoff to {target_agent.name}")
        return target_agent
    
    return handoff_with_measurement

# Complete working example with seamless integration
def main():
    """Complete supply chain coordination example with CERT measurement"""
    
    print("🔧 Setting up CERT-instrumented Swarm agents...")
    
    # Create CERT-instrumented Swarm client
    cert_swarm = CERTInstrumentedSwarm()
    
    # Create agents
    forecaster, optimizer, negotiator = create_cert_supply_chain_agents()
    
    # Set agent baselines for coordination measurement
    cert_swarm.set_agent_baseline("Forecaster", 0.87)
    cert_swarm.set_agent_baseline("Optimizer", 0.89)
    cert_swarm.set_agent_baseline("Negotiator", 0.78)
    
    # Create handoff chain with measurement
    forecaster.functions.append(create_cert_handoff_function(optimizer))
    optimizer.functions.append(create_cert_handoff_function(negotiator))
    
    # Run coordination task
    task = """
    Coordinate our Q4 supply chain strategy:
    1. Analyze demand trends for top product lines
    2. Optimize inventory levels based on forecast
    3. Develop supplier negotiation strategy
    
    Execute the complete coordination workflow.
    """
    
    print("📋 Starting CERT-measured coordination task...")
    
    messages = [{"role": "user", "content": task}]
    
    # Execute with CERT measurement
    result = cert_swarm.run(
        agent=forecaster,
        messages=messages
    )
    
    print("\n✅ Coordination task completed with CERT measurement!")
    print(f"📊 Total handoff measurements: {len(cert_swarm.handoff_measurements)}")
    
    # Display measurement summary
    if cert_swarm.handoff_measurements:
        print("\n📈 Coordination Summary:")
        for measurement in cert_swarm.handoff_measurements:
            pattern = measurement.get('interaction_pattern', 'unknown')
            gamma = measurement.get('coordination_effect', 0)
            change = measurement.get('performance_change_percent', 0)
            print(f"   {pattern}: γ={gamma:.3f} ({change:+.1f}%)")
    
    return result

if __name__ == "__main__":
    main()