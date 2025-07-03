import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import logging

class BehavioralAnalyzer:
    """
    Implements behavioral consistency measurement from CERT mathematical framework.
    
    C(A_i, p) = 1 - σ({d(r_j, r_k)}) / μ({d(r_j, r_k)})
    where d(·,·) measures semantic distance using embedding similarity.
    """
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.logger = logging.getLogger(__name__)
        
    def measure_consistency(self, agent_id: str, prompt: str, responses: List[str]) -> Dict:
        """
        Measure behavioral consistency for an agent across multiple responses.
        
        Returns:
            Dictionary with consistency score and supporting metrics
        """
        if len(responses) < 2:
            return {"error": "Need at least 2 responses for consistency measurement"}
            
        try:
            # Generate embeddings for all responses
            embeddings = self.model.encode(responses)
            
            # Calculate pairwise semantic distances
            distances = []
            for i in range(len(embeddings)):
                for j in range(i + 1, len(embeddings)):
                    distance = cosine(embeddings[i], embeddings[j])
                    distances.append(distance)
            
            # Calculate consistency using coefficient of variation
            mean_distance = np.mean(distances)
            std_distance = np.std(distances)
            
            if mean_distance == 0:
                consistency_score = 1.0  # Perfect consistency
            else:
                consistency_score = 1 - (std_distance / mean_distance)
                consistency_score = max(0, consistency_score)  # Bound at 0
            
            return {
                "agent_id": agent_id,
                "prompt": prompt,
                "consistency_score": float(consistency_score),
                "mean_semantic_distance": float(mean_distance),
                "std_semantic_distance": float(std_distance),
                "num_responses": len(responses),
                "timestamp": np.datetime64('now').astype(str)
            }
            
        except Exception as e:
            self.logger.error(f"Consistency measurement failed: {e}")
            return {"error": str(e)}