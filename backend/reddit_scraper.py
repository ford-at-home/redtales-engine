"""
Reddit scraper module for fetching posts and comments

Uses PRAW to interact with Reddit API.
"""

import praw
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging
from backend.config import config

logger = logging.getLogger(__name__)

# Known bot accounts to filter out
BOT_ACCOUNTS = {
    'AutoModerator',
    'RemindMeBot',
    'WikiTextBot',
    'TotesMessenger',
    'GoodBot_BadBot',
    'B0tRank',
    'RepostSleuthBot',
}

@dataclass
class RedditPost:
    """Reddit post data"""
    id: str
    title: str
    author: str
    score: int
    created_utc: datetime
    subreddit: str
    url: str
    num_comments: int
    
@dataclass 
class RedditComment:
    """Reddit comment data"""
    id: str
    body: str
    author: str
    score: int
    created_utc: datetime
    is_top_level: bool


class RedditScraper:
    """Handles Reddit API interactions"""
    
    def __init__(self):
        """Initialize Reddit client"""
        self.reddit = praw.Reddit(
            client_id=config.reddit_client_id,
            client_secret=config.reddit_client_secret,
            user_agent=config.reddit_user_agent
        )
        self.reddit.read_only = True  # We only need read access
        logger.info(f"Reddit client initialized with user agent: {config.reddit_user_agent}")
        
    def test_connection(self) -> bool:
        """Test Reddit API connection"""
        try:
            # Try to access the front page
            for submission in self.reddit.front.hot(limit=1):
                logger.info(f"Successfully connected to Reddit API. Test post: {submission.title[:50]}...")
                return True
        except Exception as e:
            logger.error(f"Failed to connect to Reddit API: {e}")
            return False
            
    def get_top_posts(self, subreddit_name: str, limit: int = 10, 
                     time_filter: str = "day") -> List[RedditPost]:
        """
        Fetch top posts from a subreddit
        
        Args:
            subreddit_name: Name of the subreddit
            limit: Number of posts to fetch
            time_filter: Time period (hour, day, week, month, year, all)
            
        Returns:
            List of RedditPost objects
        """
        posts = []
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            for submission in subreddit.top(time_filter=time_filter, limit=limit):
                # Skip deleted or removed posts
                if submission.author is None or submission.selftext == "[removed]":
                    continue
                    
                post = RedditPost(
                    id=submission.id,
                    title=submission.title,
                    author=str(submission.author) if submission.author else "[deleted]",
                    score=submission.score,
                    created_utc=datetime.fromtimestamp(submission.created_utc),
                    subreddit=subreddit_name,
                    url=submission.url,
                    num_comments=submission.num_comments
                )
                posts.append(post)
                logger.debug(f"Fetched post: {post.title[:50]}... (score: {post.score})")
                
            logger.info(f"Fetched {len(posts)} posts from r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"Error fetching posts from r/{subreddit_name}: {e}")
            raise
            
    def get_top_comments(self, post_id: str, limit: int = 5) -> List[RedditComment]:
        """
        Fetch top comments from a post
        
        Args:
            post_id: Reddit post ID
            limit: Number of comments to fetch
            
        Returns:
            List of RedditComment objects
        """
        comments = []
        try:
            submission = self.reddit.submission(id=post_id)
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=0)  # Remove "more comments" placeholders
            
            valid_comments = []
            for comment in submission.comments.list():
                # Filter out invalid comments
                if self._is_valid_comment(comment):
                    valid_comments.append(comment)
                    
            # Sort by score and take top N
            valid_comments.sort(key=lambda c: c.score, reverse=True)
            
            for comment in valid_comments[:limit]:
                reddit_comment = RedditComment(
                    id=comment.id,
                    body=self._clean_comment_body(comment.body),
                    author=str(comment.author),
                    score=comment.score,
                    created_utc=datetime.fromtimestamp(comment.created_utc),
                    is_top_level=comment.parent_id.startswith("t3_")
                )
                comments.append(reddit_comment)
                logger.debug(f"Fetched comment by {reddit_comment.author} (score: {reddit_comment.score})")
                
            logger.info(f"Fetched {len(comments)} valid comments from post {post_id}")
            return comments
            
        except Exception as e:
            logger.error(f"Error fetching comments from post {post_id}: {e}")
            raise
            
    def _is_valid_comment(self, comment) -> bool:
        """Check if a comment is valid for inclusion"""
        # Check if comment is deleted
        if comment.author is None:
            return False
            
        # Check if comment body is removed
        if comment.body in ["[removed]", "[deleted]", None]:
            return False
            
        # Check if author is a known bot
        if str(comment.author) in BOT_ACCOUNTS:
            return False
            
        # Check minimum score
        if comment.score < config.min_comment_score:
            return False
            
        # Check minimum length (avoid very short comments)
        if len(comment.body.strip()) < 20:
            return False
            
        return True
        
    def _clean_comment_body(self, body: str) -> str:
        """Clean comment text for story generation"""
        # Remove common Reddit formatting
        cleaned = body.strip()
        
        # Remove edit notes
        if "EDIT:" in cleaned or "Edit:" in cleaned:
            cleaned = cleaned.split("EDIT:")[0].split("Edit:")[0].strip()
            
        # Remove excessive newlines
        cleaned = "\n".join(line.strip() for line in cleaned.split("\n") if line.strip())
        
        # Limit length for very long comments
        if len(cleaned) > 1000:
            cleaned = cleaned[:1000] + "..."
            
        return cleaned


def test_connection():
    """Test Reddit API connection (used by Makefile)"""
    scraper = RedditScraper()
    if scraper.test_connection():
        print("✅ Reddit API connection successful!")
        
        # Try fetching a post
        posts = scraper.get_top_posts("AskReddit", limit=1)
        if posts:
            print(f"✅ Successfully fetched post: {posts[0].title[:50]}...")
            
            # Try fetching comments
            comments = scraper.get_top_comments(posts[0].id, limit=3)
            print(f"✅ Successfully fetched {len(comments)} comments")
            
        return True
    else:
        print("❌ Reddit API connection failed!")
        return False


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    test_connection()