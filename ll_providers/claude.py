import os
import anthropic
from typing import Dict, Any
from .base import LLMProvider

class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("Claude API key required. Set CLAUDE_API_KEY environment variable.")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate text using Claude API"""
        try:
            response = self.client.messages.create(
                model=kwargs.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=kwargs.get('max_tokens', 1000),
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information"""
        return {
            "provider": "claude",
            "api_key_configured": bool(self.api_key),
            "models": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-opus-20240229"]
        }