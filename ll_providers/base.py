# cert/llm_providers/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    def get_provider_info(self) -> Dict[str, Any]:
        pass