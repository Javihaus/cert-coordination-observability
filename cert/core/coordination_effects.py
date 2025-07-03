import numpy as np
from typing import Dict, List, Optional
import logging

class CoordinationAnalyzer:
    """
    Implements coordination effect measurement: γ = Observed / Expected
    
    γ > 1: Coordination provides performance benefits
    γ < 1: Coordination introduces performance degradation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_coordination_effect(
        self,
        agent_a_baseline: float,
        agent_b_baseline: float,
        coordinated_performance: float,
        interaction_pattern: str
    ) -> Dict:
        """
        Calculate coordination effect γ for agent interaction.
        
        Returns:
            Coordination effect analysis with actionable insights
        """
        try:
            # Expected performance from independent operation
            expected_performance = agent_a_baseline * agent_b_baseline
            
            if expected_performance == 0:
                return {"error": "Cannot calculate coordination effect with zero baseline"}
            
            # Coordination effect ratio
            gamma = coordinated_performance / expected_performance
            
            # Classify coordination impact
            if gamma > 1.2:
                impact = "highly_beneficial"
            elif gamma > 1.0:
                impact = "beneficial"
            elif gamma > 0.8:
                impact = "degraded"
            else:
                impact = "severely_degraded"
            
            return {
                "agent_a_baseline": float(agent_a_baseline),
                "agent_b_baseline": float(agent_b_baseline),
                "expected_performance": float(expected_performance),
                "observed_performance": float(coordinated_performance),
                "coordination_effect": float(gamma),
                "impact_classification": impact,
                "interaction_pattern": interaction_pattern,
                "performance_change_percent": float((gamma - 1) * 100),
                "timestamp": np.datetime64('now').astype(str)
            }
            
        except Exception as e:
            self.logger.error(f"Coordination effect calculation failed: {e}")
            return {"error": str(e)}