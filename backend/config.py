"""
Configuration management for Reddit Comment Stories

Handles environment variables and application settings.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()

@dataclass
class Config:
    """Application configuration"""
    
    # Reddit API
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str
    reddit_rate_limit: int = 60
    
    # AI API
    ai_provider: str = "openai"  # openai, anthropic, or bedrock
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    aws_profile: Optional[str] = None
    aws_region: str = "us-east-1"
    ai_rate_limit: int = 10
    
    # Application settings
    app_env: str = "development"
    log_level: str = "INFO"
    cache_ttl: int = 3600
    
    # Story generation
    default_subreddit: str = "AskReddit"
    default_post_limit: int = 10
    default_comment_limit: int = 5
    min_comment_score: int = 10
    story_min_words: int = 300
    story_max_words: int = 500
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        # Determine AI provider based on available credentials
        ai_provider = "openai"  # default
        if os.getenv("ANTHROPIC_API_KEY"):
            ai_provider = "anthropic"
        elif os.getenv("AWS_PROFILE") == "personal":
            ai_provider = "bedrock"
        elif os.getenv("OPENAI_API_KEY"):
            ai_provider = "openai"
            
        return cls(
            # Reddit API (required)
            reddit_client_id=os.getenv("REDDIT_CLIENT_ID", ""),
            reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET", ""),
            reddit_user_agent=os.getenv("REDDIT_USER_AGENT", "RedditCommentStories/1.0"),
            reddit_rate_limit=int(os.getenv("REDDIT_RATE_LIMIT", "60")),
            
            # AI API
            ai_provider=ai_provider,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            aws_profile=os.getenv("AWS_PROFILE"),
            aws_region=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            ai_rate_limit=int(os.getenv("AI_RATE_LIMIT", "10")),
            
            # Application
            app_env=os.getenv("APP_ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            
            # Story generation
            default_subreddit=os.getenv("DEFAULT_SUBREDDIT", "AskReddit"),
            default_post_limit=int(os.getenv("DEFAULT_POST_LIMIT", "10")),
            default_comment_limit=int(os.getenv("DEFAULT_COMMENT_LIMIT", "5")),
            min_comment_score=int(os.getenv("MIN_COMMENT_SCORE", "10")),
            story_min_words=int(os.getenv("STORY_MIN_WORDS", "300")),
            story_max_words=int(os.getenv("STORY_MAX_WORDS", "500")),
        )
    
    def validate(self) -> bool:
        """Validate configuration"""
        errors = []
        
        # Check Reddit credentials
        if not self.reddit_client_id:
            errors.append("REDDIT_CLIENT_ID is required")
        if not self.reddit_client_secret:
            errors.append("REDDIT_CLIENT_SECRET is required")
            
        # Check AI credentials based on provider
        if self.ai_provider == "openai" and not self.openai_api_key:
            errors.append("OPENAI_API_KEY is required for OpenAI provider")
        elif self.ai_provider == "anthropic" and not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required for Anthropic provider")
        elif self.ai_provider == "bedrock" and not self.aws_profile:
            errors.append("AWS_PROFILE is required for Bedrock provider")
            
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
            
        return True
    
    def get_aws_session(self):
        """Get AWS session with the configured profile"""
        if self.aws_profile:
            return boto3.Session(profile_name=self.aws_profile)
        return boto3.Session()


# Global config instance
config = Config.from_env()