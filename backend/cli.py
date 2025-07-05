"""
CLI tool for Reddit Comment Stories

Provides command-line interface for generating stories from Reddit posts.
"""

import argparse
import logging
import sys
import json
from datetime import datetime
from typing import Optional

from backend.reddit_scraper import RedditScraper
from backend.story_generator import StoryGenerator
from backend.prompt_builder import PromptBuilder
from backend.config import config

# Configure logging
def setup_logging(verbose: bool = False):
    """Configure logging based on verbosity"""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' if verbose else '%(levelname)s: %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def cmd_generate(args):
    """Generate a single story from a subreddit"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Generating story from r/{args.subreddit}")
    
    # Initialize components
    scraper = RedditScraper()
    generator = StoryGenerator()
    
    # Fetch posts
    logger.info(f"📊 Fetching top posts from the last {args.time}...")
    posts = scraper.get_top_posts(
        subreddit_name=args.subreddit,
        limit=args.posts,
        time_filter=args.time
    )
    
    if not posts:
        logger.error("No posts found!")
        return 1
        
    # Find a suitable post
    story_generated = False
    for i, post in enumerate(posts):
        logger.info(f"📖 Trying post {i+1}/{len(posts)}: {post.title[:60]}...")
        
        # Skip if too few comments
        if post.num_comments < 5:
            logger.warning(f"  ⚠️  Skipping (only {post.num_comments} comments)")
            continue
            
        # Fetch comments
        comments = scraper.get_top_comments(post.id, limit=5)
        
        if len(comments) < 3:
            logger.warning(f"  ⚠️  Skipping (only {len(comments)} valid comments)")
            continue
            
        # Generate story
        logger.info(f"🤖 Generating {args.style} story...")
        try:
            story = generator.generate_from_post(
                post=post,
                comments=comments,
                style=args.style
            )
            
            # Display story
            print(f"\n{'='*60}")
            print(f"✨ {story.title}")
            print(f"{'='*60}\n")
            print(story.content)
            print(f"\n{'='*60}")
            print(f"📊 Story Stats:")
            print(f"  • Words: {story.word_count}")
            print(f"  • Style: {story.style}")
            print(f"  • Generation time: {story.generation_time:.2f}s")
            print(f"  • Source: r/{story.source_post['subreddit']}")
            print(f"{'='*60}")
            
            # Save if requested
            if args.output:
                if args.output.endswith('.md'):
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(story.to_markdown())
                elif args.output.endswith('.json'):
                    with open(args.output, 'w', encoding='utf-8') as f:
                        json.dump(story.to_dict(), f, indent=2)
                else:
                    # Save both formats
                    md_path, json_path = generator.save_story(story, args.output)
                    logger.info(f"📁 Story saved to:\n  - {md_path}\n  - {json_path}")
            else:
                # Save to default location
                md_path, json_path = generator.save_story(story)
                logger.info(f"📁 Story saved to:\n  - {md_path}\n  - {json_path}")
                
            story_generated = True
            break
            
        except Exception as e:
            logger.error(f"  ❌ Generation failed: {e}")
            continue
            
    if not story_generated:
        logger.error("Failed to generate any stories from the available posts")
        return 1
        
    return 0


def cmd_batch(args):
    """Generate multiple stories in batch mode"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"🚀 Batch generation from r/{args.subreddit}")
    logger.info(f"📊 Processing {args.posts} posts with {args.style} style")
    
    # Initialize generator
    generator = StoryGenerator()
    
    # Generate stories
    stories = generator.generate_from_subreddit(
        subreddit=args.subreddit,
        post_limit=args.posts,
        time_filter=args.time,
        style=args.style
    )
    
    if not stories:
        logger.error("No stories generated!")
        return 1
        
    # Save stories
    output_dir = args.output_dir or "output/stories"
    logger.info(f"📁 Saving {len(stories)} stories to {output_dir}")
    
    for story in stories:
        generator.save_story(story, output_dir)
        
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Batch Generation Complete")
    print(f"{'='*60}")
    print(f"  • Stories generated: {len(stories)}")
    print(f"  • Average words: {sum(s.word_count for s in stories) // len(stories)}")
    print(f"  • Total generation time: {sum(s.generation_time for s in stories):.2f}s")
    print(f"  • Output directory: {output_dir}")
    print(f"{'='*60}")
    
    return 0


def cmd_test(args):
    """Test Reddit and AI connections"""
    logger = logging.getLogger(__name__)
    
    print("🧪 Testing Reddit Comment Stories Setup")
    print("=" * 60)
    
    # Test Reddit
    print("\n📡 Testing Reddit API...")
    scraper = RedditScraper()
    if scraper.test_connection():
        print("✅ Reddit API: Connected")
        
        # Try fetching a post
        posts = scraper.get_top_posts("AskReddit", limit=1)
        if posts:
            print(f"✅ Sample post: {posts[0].title[:50]}...")
    else:
        print("❌ Reddit API: Failed")
        return 1
        
    # Test AI
    print("\n🤖 Testing AI API...")
    from backend.ai_client import AIClient
    ai_client = AIClient()
    
    if ai_client.test_connection():
        print(f"✅ AI API: Connected ({ai_client.provider_name})")
        
        # Test generation
        if not args.dry_run:
            test_result = ai_client.generate_story(
                "Write a one-sentence story about a robot.",
                max_tokens=50
            )
            print(f"✅ Test generation: {test_result[:50]}...")
    else:
        print("❌ AI API: Failed")
        return 1
        
    print("\n✅ All systems operational!")
    return 0


def cmd_styles(args):
    """List available story styles"""
    builder = PromptBuilder()
    styles = builder.get_available_styles()
    
    print("📝 Available Story Styles")
    print("=" * 60)
    
    for style, description in styles.items():
        print(f"  • {style:<12} - {description}")
        
    print("=" * 60)
    print(f"Use --style with any of these options (default: engaging)")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Reddit Comment Stories - Transform Reddit posts into engaging narratives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate                    # Generate a story from r/AskReddit
  %(prog)s generate -s funny -r tifu   # Generate a funny story from r/tifu  
  %(prog)s batch -n 5                  # Generate 5 stories in batch
  %(prog)s test                        # Test API connections
  %(prog)s styles                      # List available story styles
        """
    )
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', 
                                           help='Generate a single story')
    generate_parser.add_argument('-r', '--subreddit', default='AskReddit',
                               help='Subreddit to fetch posts from (default: AskReddit)')
    generate_parser.add_argument('-s', '--style', default='engaging',
                               help='Story style (default: engaging)')
    generate_parser.add_argument('-t', '--time', default='day',
                               choices=['hour', 'day', 'week', 'month', 'year', 'all'],
                               help='Time period for top posts (default: day)')
    generate_parser.add_argument('-p', '--posts', type=int, default=10,
                               help='Number of posts to check (default: 10)')
    generate_parser.add_argument('-o', '--output',
                               help='Output file (.md or .json) or directory')
    generate_parser.set_defaults(func=cmd_generate)
    
    # Batch command
    batch_parser = subparsers.add_parser('batch',
                                       help='Generate multiple stories')
    batch_parser.add_argument('-r', '--subreddit', default='AskReddit',
                            help='Subreddit to fetch posts from')
    batch_parser.add_argument('-n', '--posts', type=int, default=5,
                            help='Number of stories to generate (default: 5)')
    batch_parser.add_argument('-s', '--style', default='engaging',
                            help='Story style')
    batch_parser.add_argument('-t', '--time', default='day',
                            choices=['hour', 'day', 'week', 'month', 'year', 'all'],
                            help='Time period for top posts')
    batch_parser.add_argument('-o', '--output-dir',
                            help='Output directory (default: output/stories)')
    batch_parser.set_defaults(func=cmd_batch)
    
    # Test command
    test_parser = subparsers.add_parser('test',
                                      help='Test API connections')
    test_parser.add_argument('--dry-run', action='store_true',
                           help='Skip actual API calls')
    test_parser.set_defaults(func=cmd_test)
    
    # Styles command
    styles_parser = subparsers.add_parser('styles',
                                        help='List available story styles')
    styles_parser.set_defaults(func=cmd_styles)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Execute command
    if args.command is None:
        parser.print_help()
        return 0
        
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())