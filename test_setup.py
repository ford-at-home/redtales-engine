#!/usr/bin/env python3
"""
Test script to verify Reddit Comment Stories setup

This script tests:
1. Environment configuration
2. Reddit API connection
3. AI API connection
"""

import sys
import logging
from backend.config import config
from backend.reddit_scraper import RedditScraper
from backend.ai_client import AIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_configuration():
    """Test configuration loading"""
    print("\n=== Testing Configuration ===")
    print(f"Environment: {config.app_env}")
    print(f"AI Provider: {config.ai_provider}")
    print(f"AWS Profile: {config.aws_profile}")
    print(f"Default Subreddit: {config.default_subreddit}")
    
    if config.validate():
        print("✅ Configuration is valid")
        return True
    else:
        print("❌ Configuration validation failed")
        return False


def test_reddit_connection():
    """Test Reddit API connection"""
    print("\n=== Testing Reddit API ===")
    
    if not config.reddit_client_id or config.reddit_client_id == "your_reddit_client_id_here":
        print("❌ Reddit credentials not configured. Please update .env file with:")
        print("   REDDIT_CLIENT_ID=<your_client_id>")
        print("   REDDIT_CLIENT_SECRET=<your_client_secret>")
        print("\n   Get credentials at: https://www.reddit.com/prefs/apps")
        return False
        
    try:
        scraper = RedditScraper()
        if scraper.test_connection():
            print("✅ Reddit API connection successful")
            
            # Try fetching a post
            posts = scraper.get_top_posts("AskReddit", limit=1)
            if posts:
                print(f"✅ Fetched post: {posts[0].title[:60]}...")
                
                # Try fetching comments
                comments = scraper.get_top_comments(posts[0].id, limit=3)
                print(f"✅ Fetched {len(comments)} comments")
                
                return True
        else:
            print("❌ Reddit API connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Reddit API error: {e}")
        return False


def test_ai_connection():
    """Test AI API connection"""
    print("\n=== Testing AI API ===")
    
    try:
        client = AIClient()
        print(f"Using provider: {client.provider_name}")
        
        if client.test_connection():
            print("✅ AI API connection successful")
            
            # Try a simple generation
            test_prompt = "Write a one-sentence story about a robot learning to laugh."
            result = client.generate_story(test_prompt, max_tokens=50)
            print(f"✅ Test generation: {result}")
            
            return True
        else:
            print("❌ AI API connection failed")
            return False
            
    except Exception as e:
        print(f"❌ AI API error: {e}")
        return False


def test_full_pipeline():
    """Test the full story generation pipeline"""
    print("\n=== Testing Full Pipeline ===")
    
    try:
        # Skip if Reddit not configured
        if not config.reddit_client_id or config.reddit_client_id == "your_reddit_client_id_here":
            print("⚠️  Skipping full pipeline test - Reddit credentials not configured")
            return True
            
        scraper = RedditScraper()
        client = AIClient()
        
        # Fetch a post
        posts = scraper.get_top_posts("AskReddit", limit=1)
        if not posts:
            print("❌ No posts found")
            return False
            
        post = posts[0]
        print(f"📖 Post: {post.title}")
        
        # Fetch comments
        comments = scraper.get_top_comments(post.id, limit=5)
        print(f"💬 Found {len(comments)} comments")
        
        # Build a simple prompt
        prompt = f"""Transform this Reddit post and its top comments into a short story:

Post: {post.title}

Comments:
"""
        for i, comment in enumerate(comments, 1):
            prompt += f"\n{i}. {comment.body[:200]}..."
            
        prompt += "\n\nWrite a creative 2-3 paragraph story that weaves these perspectives together."
        
        # Generate story
        print("🤖 Generating story...")
        story = client.generate_story(prompt, max_tokens=500)
        
        print("\n📚 Generated Story Preview:")
        print("-" * 50)
        print(story[:300] + "..." if len(story) > 300 else story)
        print("-" * 50)
        
        print("\n✅ Full pipeline test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Reddit Comment Stories - Setup Test")
    print("=" * 50)
    
    results = {
        "Configuration": test_configuration(),
        "Reddit API": test_reddit_connection(),
        "AI API": test_ai_connection(),
    }
    
    # Only test full pipeline if both APIs work
    if results["Reddit API"] and results["AI API"]:
        results["Full Pipeline"] = test_full_pipeline()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test}: {status}")
        
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to start generating stories.")
        print("\nNext steps:")
        print("  1. Run the CLI: python -m backend.cli")
        print("  2. Start the web app: streamlit run frontend/app.py")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration above.")
        
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())