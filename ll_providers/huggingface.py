import os
from huggingface_hub import InferenceClient
from typing import Dict, Any
from .base import LLMProvider

class HuggingFaceProvider(LLMProvider):
    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("Hugging Face API key required. Set HUGGINGFACE_API_KEY environment variable.")
        
        self.model_name = model_name or os.getenv('HUGGINGFACE_MODEL', 'microsoft/DialoGPT-medium')
        self.client = InferenceClient(token=self.api_key)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Hugging Face API"""
        try:
            response = self.client.text_generation(
                prompt, 
                model=self.model_name,
                max_new_tokens=kwargs.get('max_tokens', 1000),
                return_full_text=False,
                temperature=kwargs.get('temperature', 0.7)
            )
            return response
        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}")
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            "provider": "huggingface",
            "api_key_configured": bool(self.api_key),
            "current_model": self.model_name,
            "supported_models": [
                "microsoft/DialoGPT-medium",
                "meta-llama/Llama-2-7b-chat-hf",
                "meta-llama/Llama-2-13b-chat-hf",
                "deepseek-ai/deepseek-coder-6.7b-instruct",
                "deepseek-ai/deepseek-llm-7b-chat"
            ]
        }
    
    def set_model(self, model_name: str):
        """Change the model being used"""
        self.model_name = model_name
        
    @classmethod
    def create_deepseek_provider(cls, api_key: str = None):
        """Create a provider configured for Deepseek models"""
        return cls(api_key=api_key, model_name="deepseek-ai/deepseek-llm-7b-chat")
    
    @classmethod
    def create_llama_provider(cls, api_key: str = None, model_size: str = "7b"):
        """Create a provider configured for Llama models"""
        model_map = {
            "7b": "meta-llama/Llama-2-7b-chat-hf",
            "13b": "meta-llama/Llama-2-13b-chat-hf",
            "70b": "meta-llama/Llama-2-70b-chat-hf"
        }
        model_name = model_map.get(model_size, model_map["7b"])
        return cls(api_key=api_key, model_name=model_name)