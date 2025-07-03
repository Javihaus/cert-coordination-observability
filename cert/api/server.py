from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
import logging

from cert.core.behavioral_analysis import BehavioralAnalyzer
from cert.core.coordination_effects import CoordinationAnalyzer

app = FastAPI(title="CERT Coordination Observability", version="0.1.0")

# Initialize analyzers
behavioral_analyzer = BehavioralAnalyzer()
coordination_analyzer = CoordinationAnalyzer()

# Pydantic models for API requests
class ConsistencyRequest(BaseModel):
    agent_id: str
    prompt: str
    responses: List[str]

class CoordinationRequest(BaseModel):
    agent_a_id: str
    agent_b_id: str
    agent_a_baseline: float
    agent_b_baseline: float
    coordinated_performance: float
    interaction_pattern: str

@app.post("/measure/consistency")
async def measure_behavioral_consistency(request: ConsistencyRequest):
    """Measure behavioral consistency for an agent"""
    result = behavioral_analyzer.measure_consistency(
        agent_id=request.agent_id,
        prompt=request.prompt,
        responses=request.responses
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.post("/measure/coordination")
async def measure_coordination_effect(request: CoordinationRequest):
    """Measure coordination effect between two agents"""
    result = coordination_analyzer.calculate_coordination_effect(
        agent_a_baseline=request.agent_a_baseline,
        agent_b_baseline=request.agent_b_baseline,
        coordinated_performance=request.coordinated_performance,
        interaction_pattern=request.interaction_pattern
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@app.get("/health")
async def health_check():
    """API health check"""
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)