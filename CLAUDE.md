# Claude Code Configuration - redtales-engine (Reddit Comment Stories)

## Project Overview
Reddit Comment Stories is an AI-powered storytelling application that transforms Reddit posts and their top comments into engaging narrative stories. It scrapes popular Reddit threads (primarily AskReddit), extracts the top 5 comments, and uses AI to weave them into cohesive, entertaining tales.

## Project Status ✅
**Core functionality is now implemented and working!**
- Reddit scraping with PRAW ✅
- Comment filtering and quality control ✅
- AI story generation with AWS Bedrock Claude ✅
- CLI tool with multiple commands ✅
- Markdown and JSON output formats ✅

## Build Commands
```bash
# Setup
uv venv                          # Create virtual environment
source .venv/bin/activate        # Activate environment
uv pip install -r requirements.txt # Install dependencies

# Testing
make test-reddit                 # Test Reddit connection
make test-ai                     # Test AI connection
python test_setup.py             # Run full setup test

# Running
python -m backend test           # Test all connections
python -m backend generate       # Generate a single story
python -m backend batch -n 5     # Generate 5 stories
python -m backend styles         # List available styles

# Development
make lint                        # Run linting
make format                      # Format code with black
make clean                       # Clean cache files
```

## Key Features
- **Reddit Integration**: Uses PRAW to fetch posts and comments
- **AI Story Generation**: Leverages GPT-4 or Claude for narrative creation
- **Comment Curation**: Selects top 5 non-deleted, non-bot comments
- **Multiple Output Formats**: Markdown, JSON, or HTML export
- **Optional Audio**: Text-to-speech via Amazon Polly
- **Flexible Frontend**: Streamlit MVP or Next.js for production

## Architecture Overview
```
Reddit API → Comment Extraction → AI Prompt → Story Generation → Output
     ↓              ↓                  ↓              ↓            ↓
   PRAW      Top 5 Comments    GPT-4/Claude    Narrative    MD/Audio
```

## Tech Stack
- **Backend**: Python with PRAW, OpenAI/Anthropic APIs
- **Frontend**: Streamlit (MVP) or Next.js (production)
- **AI Models**: OpenAI GPT-4 or Anthropic Claude via Bedrock
- **Cloud**: AWS (S3, Lambda, Secrets Manager, Polly)
- **Infrastructure**: AWS CDK for deployment

## Project Structure (Proposed)
```
redtales-engine/
├── backend/
│   ├── reddit_scraper.py    # PRAW integration
│   ├── story_generator.py   # AI story creation
│   ├── prompt_builder.py    # Format comments for AI
│   └── audio_generator.py   # Amazon Polly integration
├── frontend/
│   ├── app.py              # Streamlit interface
│   └── components/         # UI components
├── infrastructure/
│   └── cdk/               # AWS CDK stack
└── output/
    └── stories/           # Generated stories
```

## API Configuration
Create `.env` file:
```
REDDIT_CLIENT_ID=your_reddit_app_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=RedditCommentStories/1.0
OPENAI_API_KEY=your_openai_key
# OR
AWS_PROFILE=your_aws_profile
ANTHROPIC_API_KEY=your_claude_key
```

## Common Operations

### CLI Usage (Recommended)
```bash
# Generate a single story
python -m backend generate

# Generate with specific style and subreddit
python -m backend generate --subreddit tifu --style comedy

# Batch generate multiple stories
python -m backend batch --posts 10 --style drama

# Generate from specific time period
python -m backend generate --time week --style wholesome
```

### Python API Usage
```python
from backend.reddit_scraper import RedditScraper
from backend.story_generator import StoryGenerator

# Initialize components
scraper = RedditScraper()
generator = StoryGenerator()

# Fetch Reddit data
posts = scraper.get_top_posts('AskReddit', limit=10)
post = posts[0]
comments = scraper.get_top_comments(post.id, limit=5)

# Generate story
story = generator.generate_from_post(
    post=post,
    comments=comments,
    style='comedy'
)

# Save story
md_path, json_path = generator.save_story(story)
```

### Available Story Styles
- `engaging` - Balanced, accessible narrative (default)
- `comedy` - Humorous and light-hearted
- `drama` - Emotional and character-driven
- `documentary` - Factual and journalistic
- `wholesome` - Uplifting and positive
- `thriller` - Suspenseful and tense

## Development Guidelines
- **Clean Comments**: Strip formatting, links, and excessive emojis
- **Story Coherence**: Ensure AI prompts guide narrative flow
- **Rate Limiting**: Respect Reddit API limits (60 requests/minute)
- **Error Handling**: Gracefully handle deleted comments/posts
- **Caching**: Store scraped data to avoid redundant API calls

## AI Prompt Engineering
Example prompt structure:
```
You are a creative writer. Turn the following Reddit post and comments into a 
cohesive, engaging short story (300-500 words). Incorporate all perspectives 
naturally into the narrative flow.

Post: {post_title}
Comment 1: {comment_1}
Comment 2: {comment_2}
...

Create a story that weaves these experiences together.
```

## Deployment (AWS)
- **Lambda Functions**: For scraping and story generation
- **S3**: Store generated stories and audio files
- **API Gateway**: REST endpoints for frontend
- **EventBridge**: Schedule daily story generation
- **Secrets Manager**: Store API credentials
- **CloudFront**: CDN for web interface

## Output Examples
- **Markdown**: Clean formatted text with story metadata
- **JSON**: Structured data with story, sources, timestamps
- **Audio**: MP3 files via Amazon Polly
- **Web**: Interactive story viewer with Reddit links

## Performance Considerations
- **API Limits**: Reddit (60/min), OpenAI (varies by tier)
- **Story Length**: 300-500 words optimal for engagement
- **Processing Time**: ~5-10 seconds per story
- **Caching**: Store popular subreddit data for 1 hour

## Future Enhancements
- [ ] Multi-subreddit story compilation
- [ ] User-submitted post/comment sets
- [ ] Story illustrations with DALL-E/Midjourney
- [ ] Daily email digest of best stories
- [ ] Voting system for story quality
- [ ] Multiple narrative styles (comedy, drama, documentary)
- [ ] Translation to multiple languages
- [ ] Podcast-style audio production

## Troubleshooting

### Common Issues
1. **"Reddit authentication failed"**: Check CLIENT_ID and SECRET
2. **"No comments found"**: Post might be locked or deleted
3. **"AI generation failed"**: Verify API keys and quotas
4. **"Story lacks coherence"**: Refine prompt engineering

### Data Quality Tips
- Filter comments by score (minimum 10 upvotes)
- Exclude AutoModerator and known bots
- Handle [deleted] and [removed] gracefully
- Preserve comment threading context when relevant