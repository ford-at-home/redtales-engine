"""
AI Client module for story generation

Supports multiple AI providers: OpenAI, Anthropic, and AWS Bedrock.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod

from backend.config import config

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text completion from prompt"""
        pass
        
    @abstractmethod
    def test_connection(self) -> bool:
        """Test API connection"""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-4-turbo-preview"  # Latest model with better instruction following
            logger.info(f"OpenAI client initialized with model: {self.model}")
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
            
    def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate story using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative storyteller who writes engaging narratives."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.8,  # More creative output
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
            
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            logger.info("OpenAI API connection successful")
            return True
        except Exception as e:
            logger.error(f"OpenAI API connection failed: {e}")
            return False


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""
    
    def __init__(self, api_key: str):
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
            self.model = "claude-3-opus-20240229"  # Latest Claude model
            logger.info(f"Anthropic client initialized with model: {self.model}")
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
            
    def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate story using Claude"""
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.8
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
            
    def test_connection(self) -> bool:
        """Test Anthropic API connection"""
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            logger.info("Anthropic API connection successful")
            return True
        except Exception as e:
            logger.error(f"Anthropic API connection failed: {e}")
            return False


class BedrockProvider(AIProvider):
    """AWS Bedrock provider for Claude"""
    
    def __init__(self, session):
        try:
            self.client = session.client('bedrock-runtime', region_name=config.aws_region)
            # Use Claude 3 Sonnet which is more commonly available for on-demand
            self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            logger.info(f"Bedrock client initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
            
    def generate_completion(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate story using Bedrock Claude"""
        try:
            # Bedrock uses a specific format for Claude
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.8,
                "top_p": 0.9
            })
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text'].strip()
            
        except Exception as e:
            logger.error(f"Bedrock API error: {e}")
            raise
            
    def test_connection(self) -> bool:
        """Test Bedrock API connection"""
        try:
            # List available models to test connection
            bedrock = config.get_aws_session().client('bedrock', region_name=config.aws_region)
            response = bedrock.list_foundation_models()
            
            # Check if Claude is available
            claude_available = any(
                'claude' in model.get('modelId', '').lower() 
                for model in response.get('modelSummaries', [])
            )
            
            if claude_available:
                logger.info("Bedrock API connection successful - Claude models available")
                return True
            else:
                logger.warning("Bedrock API connected but Claude models not found")
                return False
                
        except Exception as e:
            logger.error(f"Bedrock API connection failed: {e}")
            return False


class AIClient:
    """Main AI client that manages different providers"""
    
    def __init__(self, provider: Optional[str] = None):
        """
        Initialize AI client with specified provider
        
        Args:
            provider: Provider name (openai, anthropic, bedrock) or None to auto-detect
        """
        self.provider_name = provider or config.ai_provider
        self.provider = self._initialize_provider()
        
    def _initialize_provider(self) -> AIProvider:
        """Initialize the appropriate AI provider"""
        if self.provider_name == "openai":
            if not config.openai_api_key:
                raise ValueError("OpenAI API key not found in environment")
            return OpenAIProvider(config.openai_api_key)
            
        elif self.provider_name == "anthropic":
            if not config.anthropic_api_key:
                raise ValueError("Anthropic API key not found in environment")
            return AnthropicProvider(config.anthropic_api_key)
            
        elif self.provider_name == "bedrock":
            if not config.aws_profile:
                raise ValueError("AWS profile not configured")
            session = config.get_aws_session()
            return BedrockProvider(session)
            
        else:
            raise ValueError(f"Unknown AI provider: {self.provider_name}")
            
    def generate_story(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Generate a story from the given prompt
        
        Args:
            prompt: The story generation prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated story text
        """
        logger.info(f"Generating story with {self.provider_name} provider")
        return self.provider.generate_completion(prompt, max_tokens)
        
    def test_connection(self) -> bool:
        """Test the AI provider connection"""
        return self.provider.test_connection()


def test_connection():
    """Test AI API connection (used by Makefile)"""
    try:
        client = AIClient()
        print(f"Testing {client.provider_name} provider...")
        
        if client.test_connection():
            print(f"✅ {client.provider_name} API connection successful!")
            
            # Try generating a short test completion
            test_prompt = "Write a one-sentence story about a cat."
            result = client.generate_story(test_prompt, max_tokens=50)
            print(f"✅ Test generation successful: {result[:50]}...")
            
            return True
        else:
            print(f"❌ {client.provider_name} API connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing AI connection: {e}")
        return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_connection()