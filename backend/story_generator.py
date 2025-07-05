"""
Story generator module for creating AI-powered narratives

Coordinates between Reddit data, prompt building, and AI generation
to create cohesive stories from Reddit posts and comments.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

from backend.reddit_scraper import RedditScraper, RedditPost, RedditComment
from backend.prompt_builder import PromptBuilder, StoryPrompt
from backend.ai_client import AIClient
from backend.config import config

logger = logging.getLogger(__name__)


@dataclass
class GeneratedStory:
    """Complete generated story with metadata"""
    id: str
    title: str
    content: str
    style: str
    word_count: int
    source_post: Dict
    source_comments: List[Dict]
    generation_time: float
    created_at: datetime
    ai_provider: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        return data
        
    def to_markdown(self) -> str:
        """Format story as markdown"""
        md = f"# {self.title}\n\n"
        md += f"*Generated from r/{self.source_post['subreddit']} • "
        md += f"{self.style.title()} style • {self.word_count} words*\n\n"
        md += "---\n\n"
        md += self.content
        md += "\n\n---\n\n"
        md += f"**Source:** [{self.source_post['title']}]({self.source_post['url']})\n\n"
        md += f"**Generated:** {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        md += f"**AI Provider:** {self.ai_provider}\n"
        return md


class StoryGenerator:
    """Main story generation coordinator"""
    
    def __init__(self, ai_client: Optional[AIClient] = None):
        """
        Initialize story generator
        
        Args:
            ai_client: Optional AI client instance (creates default if None)
        """
        self.reddit_scraper = RedditScraper()
        self.prompt_builder = PromptBuilder()
        self.ai_client = ai_client or AIClient()
        
    def generate_from_post(
        self,
        post: RedditPost,
        comments: List[RedditComment],
        style: str = "engaging",
        min_words: Optional[int] = None,
        max_words: Optional[int] = None
    ) -> GeneratedStory:
        """
        Generate a story from a Reddit post and comments
        
        Args:
            post: Reddit post object
            comments: List of comment objects
            style: Story style
            min_words: Minimum word count
            max_words: Maximum word count
            
        Returns:
            GeneratedStory object
        """
        logger.info(f"Generating {style} story from post: {post.title[:50]}...")
        
        start_time = datetime.now()
        
        # Build the prompt
        prompt = self.prompt_builder.build_story_prompt(
            post=post,
            comments=comments,
            style=style,
            min_words=min_words,
            max_words=max_words
        )
        
        # Generate the story
        try:
            # Combine system and user prompts for the AI
            if hasattr(self.ai_client.provider, 'client') and hasattr(self.ai_client.provider.client, 'chat'):
                # OpenAI-style with separate system message
                story_content = self.ai_client.generate_story(
                    prompt.user_prompt,
                    max_tokens=1500  # Enough for ~500 word story
                )
            else:
                # Anthropic/Bedrock style - combine prompts
                full_prompt = f"{prompt.system_message}\n\n{prompt.user_prompt}"
                story_content = self.ai_client.generate_story(
                    full_prompt,
                    max_tokens=1500
                )
                
        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            raise
            
        # Calculate generation time
        generation_time = (datetime.now() - start_time).total_seconds()
        
        # Count words in the generated story
        word_count = len(story_content.split())
        
        # Create story ID
        story_id = f"{post.id}_{style}_{int(datetime.now().timestamp())}"
        
        # Prepare source data
        source_post = {
            "id": post.id,
            "title": post.title,
            "author": post.author,
            "score": post.score,
            "subreddit": post.subreddit,
            "url": post.url,
            "num_comments": post.num_comments
        }
        
        source_comments = [
            {
                "id": comment.id,
                "author": comment.author,
                "score": comment.score,
                "preview": comment.body[:100] + "..." if len(comment.body) > 100 else comment.body
            }
            for comment in comments
        ]
        
        # Create the story object
        story = GeneratedStory(
            id=story_id,
            title=self._generate_story_title(post.title, style),
            content=story_content,
            style=style,
            word_count=word_count,
            source_post=source_post,
            source_comments=source_comments,
            generation_time=generation_time,
            created_at=datetime.now(),
            ai_provider=self.ai_client.provider_name
        )
        
        logger.info(f"Story generated successfully: {word_count} words in {generation_time:.2f}s")
        
        return story
        
    def generate_from_subreddit(
        self,
        subreddit: str,
        post_limit: int = 5,
        time_filter: str = "day",
        style: str = "engaging"
    ) -> List[GeneratedStory]:
        """
        Generate multiple stories from top posts in a subreddit
        
        Args:
            subreddit: Subreddit name
            post_limit: Number of posts to process
            time_filter: Time period for top posts
            style: Story style
            
        Returns:
            List of GeneratedStory objects
        """
        logger.info(f"Generating stories from r/{subreddit} (top {post_limit} from {time_filter})")
        
        stories = []
        
        # Fetch top posts
        posts = self.reddit_scraper.get_top_posts(
            subreddit_name=subreddit,
            limit=post_limit,
            time_filter=time_filter
        )
        
        for i, post in enumerate(posts, 1):
            logger.info(f"Processing post {i}/{len(posts)}: {post.title[:50]}...")
            
            try:
                # Skip posts with too few comments
                if post.num_comments < 5:
                    logger.warning(f"Skipping post with only {post.num_comments} comments")
                    continue
                    
                # Fetch comments
                comments = self.reddit_scraper.get_top_comments(
                    post_id=post.id,
                    limit=config.default_comment_limit
                )
                
                if len(comments) < 3:
                    logger.warning(f"Skipping post with only {len(comments)} valid comments")
                    continue
                    
                # Generate story
                story = self.generate_from_post(post, comments, style=style)
                stories.append(story)
                
            except Exception as e:
                logger.error(f"Failed to generate story for post {post.id}: {e}")
                continue
                
        logger.info(f"Generated {len(stories)} stories from r/{subreddit}")
        return stories
        
    def _generate_story_title(self, post_title: str, style: str) -> str:
        """Generate a creative title for the story"""
        # For now, use a simple format
        # Could enhance this with AI generation later
        style_prefix = {
            "comedy": "The Hilarious Tale of",
            "drama": "The Dramatic Story of",
            "documentary": "The True Account of",
            "wholesome": "The Heartwarming Story of",
            "thriller": "The Suspenseful Tale of",
            "engaging": "The Story of"
        }
        
        prefix = style_prefix.get(style, "The Story of")
        
        # Clean up the post title
        if post_title.endswith("?"):
            title_base = post_title[:-1]
            return f"{prefix} {title_base}"
        else:
            return f"{prefix}: {post_title}"
            
    def save_story(self, story: GeneratedStory, output_dir: str = "output/stories") -> Tuple[str, str]:
        """
        Save story to disk
        
        Args:
            story: GeneratedStory object
            output_dir: Directory to save files
            
        Returns:
            Tuple of (markdown_path, json_path)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create filename from story ID
        base_filename = f"{story.created_at.strftime('%Y%m%d_%H%M%S')}_{story.id}"
        
        # Save as markdown
        md_path = os.path.join(output_dir, f"{base_filename}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(story.to_markdown())
            
        # Save as JSON
        json_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(story.to_dict(), f, indent=2, ensure_ascii=False)
            
        logger.info(f"Story saved: {md_path}")
        
        return md_path, json_path


def test_story_generator():
    """Test the story generator with a real Reddit post"""
    generator = StoryGenerator()
    
    # Test with a single post from AskReddit
    posts = generator.reddit_scraper.get_top_posts("AskReddit", limit=1)
    
    if not posts:
        print("No posts found!")
        return
        
    post = posts[0]
    print(f"📖 Using post: {post.title}")
    
    # Get comments
    comments = generator.reddit_scraper.get_top_comments(post.id, limit=5)
    print(f"💬 Found {len(comments)} comments")
    
    # Generate story
    print("🤖 Generating story...")
    story = generator.generate_from_post(post, comments, style="engaging")
    
    print(f"\n✅ Story generated!")
    print(f"Title: {story.title}")
    print(f"Words: {story.word_count}")
    print(f"Time: {story.generation_time:.2f}s")
    print(f"\nPreview:\n{'-'*50}")
    print(story.content[:500] + "..." if len(story.content) > 500 else story.content)
    print('-'*50)
    
    # Save the story
    md_path, json_path = generator.save_story(story)
    print(f"\n📁 Story saved to:\n  - {md_path}\n  - {json_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_story_generator()