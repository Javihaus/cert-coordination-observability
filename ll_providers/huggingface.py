import os
import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, Optional, List
from .base import LLMProvider


class HuggingFaceProvider(LLMProvider):
    """
    Comprehensive HuggingFace provider supporting any model with proper permissions.
    Designed for systematic measurement of coordination patterns in multi-agent systems.
    """
    
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initialize HuggingFace provider with flexible model support.
        
        Args:
            api_key: HF API token (defaults to HUGGINGFACE_API_KEY env var)
            model_name: Any HF model ID (e.g., 'meta-llama/Llama-2-7b-chat-hf')
        """
        self.api_key = api_key or os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            raise ValueError("HuggingFace API key required. Set HUGGINGFACE_API_KEY environment variable.")
        
        self.model_name = model_name or os.getenv('HUGGINGFACE_MODEL', 'microsoft/DialoGPT-medium')
        self.base_url = "https://api-inference.huggingface.co/models"
        
        # Rate limiting and retry configuration
        self.max_retries = 3
        self.retry_delay = 2.0
        self.timeout = 60  # Increased for large models
        
        # Track performance metrics for CERT analysis
        self.request_history = []
        
    async def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate text using any HuggingFace model with proper error handling.
        
        Args:
            prompt: Input text prompt
            **kwargs: Generation parameters (max_tokens, temperature, etc.)
            
        Returns:
            Generated text string
            
        Raises:
            Exception: On API errors, timeouts, or invalid responses
        """
        start_time = time.time()
        
        # Prepare request parameters
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": kwargs.get('max_tokens', 500),
                "temperature": kwargs.get('temperature', 0.7),
                "return_full_text": kwargs.get('return_full_text', False),
                "do_sample": kwargs.get('do_sample', True),
                "top_p": kwargs.get('top_p', 0.9),
                "repetition_penalty": kwargs.get('repetition_penalty', 1.1)
            },
            "options": {
                "wait_for_model": True,  # Wait if model is loading
                "use_cache": kwargs.get('use_cache', True)
            }
        }
        
        url = f"{self.base_url}/{self.model_name}"
        
        # Attempt generation with retries
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        
                        response_time = time.time() - start_time
                        
                        # Log request for CERT metrics
                        self._log_request(response.status, response_time, attempt + 1)
                        
                        if response.status == 200:
                            result = await response.json()
                            return self._extract_generated_text(result)
                            
                        elif response.status == 503:
                            # Model loading - wait and retry
                            error_detail = await response.text()
                            print(f"Model loading (attempt {attempt + 1}): {error_detail}")
                            
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(self.retry_delay * (attempt + 1))
                                continue
                            else:
                                raise Exception(f"Model still loading after {self.max_retries} attempts")
                                
                        elif response.status == 429:
                            # Rate limited - exponential backoff
                            error_detail = await response.text()
                            print(f"Rate limited (attempt {attempt + 1}): {error_detail}")
                            
                            if attempt < self.max_retries - 1:
                                await asyncio.sleep(self.retry_delay * (2 ** attempt))
                                continue
                            else:
                                raise Exception(f"Rate limited after {self.max_retries} attempts")
                                
                        elif response.status == 400:
                            # Bad request - likely model-specific issue
                            error_detail = await response.text()
                            raise Exception(f"Bad request for model {self.model_name}: {error_detail}")
                            
                        elif response.status == 404:
                            # Model not found or no access
                            raise Exception(f"Model {self.model_name} not found or access denied. Check model name and permissions.")
                            
                        else:
                            # Other HTTP error
                            error_detail = await response.text()
                            raise Exception(f"HuggingFace API error {response.status}: {error_detail}")
                            
            except asyncio.TimeoutError:
                last_exception = Exception(f"Request timeout ({self.timeout}s) on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                    
            except aiohttp.ClientError as e:
                last_exception = Exception(f"Network error on attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
                    
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay)
                    continue
        
        # All retries failed
        raise last_exception or Exception(f"Failed after {self.max_retries} attempts")
    
    def _extract_generated_text(self, result: Any) -> str:
        """Extract generated text from HuggingFace API response."""
        try:
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict):
                    return result[0].get("generated_text", "")
                else:
                    return str(result[0])
            elif isinstance(result, dict):
                return result.get("generated_text", str(result))
            elif isinstance(result, str):
                return result
            else:
                raise Exception(f"Unexpected response format: {type(result)} - {result}")
        except Exception as e:
            raise Exception(f"Failed to extract text from response: {str(e)}")
    
    def _log_request(self, status_code: int, response_time: float, attempt: int):
        """Log request metrics for CERT analysis."""
        self.request_history.append({
            "timestamp": time.time(),
            "model": self.model_name,
            "status_code": status_code,
            "response_time": response_time,
            "attempt": attempt,
            "success": status_code == 200
        })
        
        # Keep only recent history (last 100 requests)
        if len(self.request_history) > 100:
            self.request_history = self.request_history[-100:]
    
    async def test_model_availability(self) -> Dict[str, Any]:
        """Test if the current model is available and accessible."""
        try:
            test_prompt = "Hello"
            start_time = time.time()
            
            result = await self.generate(test_prompt, max_tokens=10)
            response_time = time.time() - start_time
            
            return {
                "available": True,
                "model": self.model_name,
                "response_time": response_time,
                "test_output": result
            }
            
        except Exception as e:
            return {
                "available": False,
                "model": self.model_name,
                "error": str(e)
            }
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get comprehensive provider information for CERT analysis."""
        recent_requests = self.request_history[-10:] if self.request_history else []
        successful_requests = [r for r in recent_requests if r["success"]]
        
        return {
            "provider": "huggingface",
            "api_key_configured": bool(self.api_key),
            "current_model": self.model_name,
            "base_url": self.base_url,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "recent_requests": len(recent_requests),
            "recent_success_rate": len(successful_requests) / max(1, len(recent_requests)),
            "avg_response_time": sum(r["response_time"] for r in successful_requests) / max(1, len(successful_requests)),
            "supported_features": [
                "Any HuggingFace model with API access",
                "Automatic retry with exponential backoff",
                "Model loading detection and waiting",
                "Rate limit handling",
                "Performance metrics collection"
            ]
        }
    
    def set_model(self, model_name: str):
        """Change the model being used - supports any HF model."""
        self.model_name = model_name
        print(f"Switched to model: {model_name}")
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics for CERT behavioral analysis."""
        if not self.request_history:
            return {"message": "No requests made yet"}
        
        successful = [r for r in self.request_history if r["success"]]
        failed = [r for r in self.request_history if not r["success"]]
        
        return {
            "total_requests": len(self.request_history),
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate": len(successful) / len(self.request_history),
            "avg_response_time": sum(r["response_time"] for r in successful) / max(1, len(successful)),
            "min_response_time": min((r["response_time"] for r in successful), default=0),
            "max_response_time": max((r["response_time"] for r in successful), default=0),
            "error_types": {},  # Could be expanded to categorize errors
            "recent_performance": self.request_history[-10:]
        }
    
    # Convenience factory methods for common models
    @classmethod
    def create_deepseek_provider(cls, api_key: str = None, model_variant: str = "7b-chat"):
        """Create provider for Deepseek models."""
        model_map = {
            "7b-chat": "deepseek-ai/deepseek-llm-7b-chat",
            "6.7b-instruct": "deepseek-ai/deepseek-coder-6.7b-instruct",
            "7b-instruct": "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
        }
        model_name = model_map.get(model_variant, model_map["7b-chat"])
        return cls(api_key=api_key, model_name=model_name)
    
    @classmethod
    def create_llama_provider(cls, api_key: str = None, model_size: str = "7b"):
        """Create provider for Llama models."""
        model_map = {
            "7b": "meta-llama/Llama-2-7b-chat-hf",
            "13b": "meta-llama/Llama-2-13b-chat-hf",
            "70b": "meta-llama/Llama-2-70b-chat-hf",
            "3.1-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "3.1-70b": "meta-llama/Meta-Llama-3.1-70B-Instruct"
        }
        model_name = model_map.get(model_size, model_map["7b"])
        return cls(api_key=api_key, model_name=model_name)
    
    @classmethod
    def create_mistral_provider(cls, api_key: str = None, model_variant: str = "7b-instruct"):
        """Create provider for Mistral models."""
        model_map = {
            "7b-instruct": "mistralai/Mistral-7B-Instruct-v0.2",
            "7b-instruct-v0.3": "mistralai/Mistral-7B-Instruct-v0.3",
            "nemo": "mistralai/Mistral-Nemo-Instruct-2407"
        }
        model_name = model_map.get(model_variant, model_map["7b-instruct"])
        return cls(api_key=api_key, model_name=model_name)
    
    @classmethod
    def create_custom_provider(cls, model_name: str, api_key: str = None):
        """Create provider for any HuggingFace model by exact model ID."""
        return cls(api_key=api_key, model_name=model_name)


# Usage examples and testing utilities
async def test_multiple_models(api_key: str, models: List[str]) -> Dict[str, Any]:
    """Test availability of multiple models."""
    results = {}
    
    for model in models:
        provider = HuggingFaceProvider(api_key=api_key, model_name=model)
        results[model] = await provider.test_model_availability()
        
        # Small delay between tests
        await asyncio.sleep(1)
    
    return results


def get_popular_models() -> Dict[str, List[str]]:
    """Get list of popular models by category."""
    return {
        "deepseek": [
            "deepseek-ai/deepseek-llm-7b-chat",
            "deepseek-ai/deepseek-coder-6.7b-instruct",
            "deepseek-ai/deepseek-coder-7b-instruct-v1.5"
        ],
        "llama": [
            "meta-llama/Llama-2-7b-chat-hf",
            "meta-llama/Llama-2-13b-chat-hf",
            "meta-llama/Meta-Llama-3.1-8B-Instruct"
        ],
        "mistral": [
            "mistralai/Mistral-7B-Instruct-v0.2",
            "mistralai/Mistral-7B-Instruct-v0.3",
            "mistralai/Mistral-Nemo-Instruct-2407"
        ],
        "microsoft": [
            "microsoft/DialoGPT-medium",
            "microsoft/phi-2"
        ],
        "google": [
            "google/flan-t5-large",
            "google/gemma-7b-it"
        ]
    }
