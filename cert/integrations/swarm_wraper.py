# cert/integrations/swarm_wrapper.py
import cert_client
from swarm import Agent

def instrument_swarm_handoff(agent_a, agent_b, context="handoff"):
    """Instrument Swarm agent handoffs with CERT measurement"""
    
    cert_client_instance = cert_client.CERTClient()
    
    def measured_handoff(context_variables):
        # Execute handoff
        result_a = agent_a.run(context_variables)
        result_b = agent_b.run(result_a.context_variables)
        
        # Measure coordination effect
        coordination_effect = cert_client_instance.measure_coordination(
            agent_a_baseline=0.85,  # From prior measurement
            agent_b_baseline=0.82,  # From prior measurement
            coordinated_performance=evaluate_combined_result(result_b),
            interaction_pattern=context
        )
        
        if coordination_effect['coordination_effect'] < 0.9:
            print(f"WARNING: Coordination degradation detected: γ={coordination_effect['coordination_effect']:.3f}")
            
        return result_b
    
    return measured_handoff