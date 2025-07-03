# cert/integrations/autogen_wrapper.py
import cert_client
from autogen import ConversableAgent

class CERTInstrumentedAgent(ConversableAgent):
    """AutoGen agent with CERT observability instrumentation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cert_client = cert_client.CERTClient()
        self.response_history = []
        
    def generate_reply(self, messages, sender=None, **kwargs):
        # Get baseline response
        response = super().generate_reply(messages, sender, **kwargs)
        
        # Collect for consistency measurement
        prompt = messages[-1]["content"] if messages else ""
        self.response_history.append(response)
        
        # Measure consistency when we have multiple responses
        if len(self.response_history) >= 3:
            consistency = self.cert_client.measure_consistency(
                agent_id=self.name,
                prompt=prompt,
                responses=self.response_history[-3:]
            )
            print(f"Agent {self.name} consistency: {consistency['consistency_score']:.3f}")
            
        return response