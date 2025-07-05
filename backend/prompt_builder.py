"""
Prompt builder module for formatting Reddit data for AI story generation

Handles the construction of prompts that guide AI models to create
cohesive stories from Reddit posts and comments.
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from backend.reddit_scraper import RedditPost, RedditComment
from backend.config import config

logger = logging.getLogger(__name__)

# Story style templates
STORY_STYLES = {
    "engaging": {
        "description": "A balanced, engaging narrative",
        "prompt_addon": "Write in an engaging, accessible style that draws the reader in."
    },
    "comedy": {
        "description": "Humorous and light-hearted",
        "prompt_addon": "Write with humor and wit, finding the funny side of the situation."
    },
    "drama": {
        "description": "Emotional and character-driven",
        "prompt_addon": "Create a dramatic narrative focusing on emotions and character development."
    },
    "documentary": {
        "description": "Factual and journalistic",
        "prompt_addon": "Present the story in a documentary style, as if narrating real events."
    },
    "wholesome": {
        "description": "Uplifting and positive",
        "prompt_addon": "Focus on the heartwarming and positive aspects, creating an uplifting narrative."
    },
    "thriller": {
        "description": "Suspenseful and tense",
        "prompt_addon": "Build suspense and tension throughout the narrative."
    }
}


@dataclass
class StoryPrompt:
    """Structured story prompt data"""
    system_message: str
    user_prompt: str
    post_data: Dict
    style: str
    word_count: tuple


class PromptBuilder:
    """Builds prompts for AI story generation"""
    
    def __init__(self):
        self.styles = STORY_STYLES
        
    def build_story_prompt(
        self, 
        post: RedditPost, 
        comments: List[RedditComment],
        style: str = "engaging",
        min_words: Optional[int] = None,
        max_words: Optional[int] = None
    ) -> StoryPrompt:
        """
        Build a complete prompt for story generation
        
        Args:
            post: Reddit post object
            comments: List of top comments
            style: Story style (engaging, comedy, drama, etc.)
            min_words: Minimum word count (uses config default if None)
            max_words: Maximum word count (uses config default if None)
            
        Returns:
            StoryPrompt object with formatted prompts
        """
        # Use defaults from config if not specified
        min_words = min_words or config.story_min_words
        max_words = max_words or config.story_max_words
        
        # Validate style
        if style not in self.styles:
            logger.warning(f"Unknown style '{style}', defaulting to 'engaging'")
            style = "engaging"
            
        # Build system message
        system_message = self._build_system_message(style)
        
        # Build user prompt
        user_prompt = self._build_user_prompt(post, comments, style, min_words, max_words)
        
        # Create post data dictionary for reference
        post_data = {
            "title": post.title,
            "subreddit": post.subreddit,
            "score": post.score,
            "num_comments": post.num_comments,
            "comment_count": len(comments)
        }
        
        return StoryPrompt(
            system_message=system_message,
            user_prompt=user_prompt,
            post_data=post_data,
            style=style,
            word_count=(min_words, max_words)
        )
        
    def _build_system_message(self, style: str) -> str:
        """Build the system message for the AI"""
        return (
            "You are a creative storyteller who transforms Reddit posts and comments "
            "into engaging narrative stories. You excel at weaving multiple perspectives "
            "into cohesive tales while maintaining the essence of the original content. "
            f"{self.styles[style]['prompt_addon']}"
        )
        
    def _build_user_prompt(
        self, 
        post: RedditPost, 
        comments: List[RedditComment],
        style: str,
        min_words: int,
        max_words: int
    ) -> str:
        """Build the user prompt with post and comment data"""
        
        # Start with the main instruction
        prompt = f"""Transform this Reddit post and its top comments into a {style} story.

**Reddit Post from r/{post.subreddit}:**
"{post.title}"

**Top Comments from the community:**
"""
        
        # Add comments with numbers
        for i, comment in enumerate(comments, 1):
            # Truncate very long comments for the prompt
            comment_text = comment.body
            if len(comment_text) > 500:
                comment_text = comment_text[:500] + "..."
                
            prompt += f"\n{i}. {comment_text}\n"
            
        # Add generation instructions
        prompt += f"""

**Instructions:**
- Create a cohesive narrative that naturally incorporates perspectives from all comments
- The story should flow smoothly, not just list the comments
- Maintain the spirit and tone of the original content
- Write in third person unless first person serves the narrative better
- Length: {min_words}-{max_words} words
- Style: {self.styles[style]['description']}

Begin the story:"""
        
        return prompt
        
    def build_simple_prompt(self, post_title: str, comment_texts: List[str]) -> str:
        """
        Build a simple prompt (for testing or basic use)
        
        Args:
            post_title: The Reddit post title
            comment_texts: List of comment text strings
            
        Returns:
            Simple prompt string
        """
        prompt = f"Create a story based on this Reddit post: '{post_title}'\n\n"
        prompt += "Using these comments as inspiration:\n"
        
        for i, comment in enumerate(comment_texts, 1):
            prompt += f"{i}. {comment}\n"
            
        prompt += "\nWrite a creative story that weaves these elements together."
        
        return prompt
        
    def get_available_styles(self) -> Dict[str, str]:
        """Get available story styles and their descriptions"""
        return {
            style: info["description"] 
            for style, info in self.styles.items()
        }
        
    def estimate_prompt_tokens(self, prompt: StoryPrompt) -> int:
        """
        Estimate the number of tokens in a prompt
        
        Rough estimation: 1 token ≈ 4 characters
        """
        total_chars = len(prompt.system_message) + len(prompt.user_prompt)
        estimated_tokens = total_chars // 4
        
        logger.debug(f"Estimated prompt tokens: {estimated_tokens}")
        return estimated_tokens


def test_prompt_builder():
    """Test the prompt builder with sample data"""
    from datetime import datetime
    
    # Create sample data
    post = RedditPost(
        id="test123",
        title="What's the most embarrassing thing that happened to you at work?",
        author="test_user",
        score=1500,
        created_utc=datetime.now(),
        subreddit="AskReddit",
        url="https://reddit.com/r/AskReddit/comments/test123",
        num_comments=250
    )
    
    comments = [
        RedditComment(
            id="c1",
            body="I once accidentally sent a love letter meant for my wife to the entire company email list. The CEO replied with 'That's sweet, but I'm taken.'",
            author="embarrassed_employee",
            score=500,
            created_utc=datetime.now(),
            is_top_level=True
        ),
        RedditComment(
            id="c2",
            body="During a video call, I forgot I was screen sharing and started browsing job listings. My boss asked if I found anything interesting.",
            author="caught_redhanded",
            score=350,
            created_utc=datetime.now(),
            is_top_level=True
        ),
        RedditComment(
            id="c3",
            body="I fell asleep during a meeting and woke up to everyone staring at me. Apparently, I was snoring loudly and mumbling about pizza.",
            author="sleepy_worker",
            score=275,
            created_utc=datetime.now(),
            is_top_level=True
        )
    ]
    
    # Test the builder
    builder = PromptBuilder()
    
    # Test different styles
    for style in ["engaging", "comedy", "drama"]:
        print(f"\n{'='*50}")
        print(f"Testing {style.upper()} style")
        print('='*50)
        
        prompt = builder.build_story_prompt(post, comments, style=style)
        
        print(f"\nSystem Message:\n{prompt.system_message}")
        print(f"\nUser Prompt Preview (first 500 chars):\n{prompt.user_prompt[:500]}...")
        print(f"\nEstimated tokens: {builder.estimate_prompt_tokens(prompt)}")
        
    print("\n✅ Prompt builder test complete!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_prompt_builder()