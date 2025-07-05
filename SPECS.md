# Technical Specification: Reddit Comment Stories

## Project Status: Core Implementation Complete ✅

### Implemented Features
- ✅ Reddit scraping with PRAW
- ✅ Comment quality filtering
- ✅ AI story generation (AWS Bedrock Claude)
- ✅ Multiple narrative styles
- ✅ CLI tool with full functionality
- ✅ Markdown and JSON output formats

### Pending Features
- ⏳ Streamlit web interface
- ⏳ Audio generation (Amazon Polly)
- ⏳ AWS Lambda deployment
- ⏳ REST API endpoints

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Interface                             │
│                    python -m backend [command]                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────┐
│                      Story Generator                              │
│                 Coordinates all components                        │
└─────────────────────────────────────────────────────────────────┘
         │                       │                       │
┌────────────────┐    ┌────────────────┐    ┌────────────────────┐
│ Reddit Scraper │    │ Prompt Builder │    │    AI Client       │
│     (PRAW)     │    │  (6 styles)    │    │ (AWS Bedrock)      │
└────────────────┘    └────────────────┘    └────────────────────┘
```

---

## Core Components (Implemented)

### 1. **Reddit Scraper** (`backend/reddit_scraper.py`)
- **Tool**: PRAW (Python Reddit API Wrapper)
- **Features**: 
  - OAuth-less authentication (read-only mode)
  - Fetch top posts by time period (hour/day/week/month/year/all)
  - Extract top N comments with quality filtering
  - Bot detection and removal
  - Comment score threshold filtering
  - Text cleaning and formatting

**Key Classes:**
- `RedditScraper`: Main scraping interface
- `RedditPost`: Post data model
- `RedditComment`: Comment data model

### 2. **Prompt Builder** (`backend/prompt_builder.py`)
- **Narrative Styles**: 6 different styles implemented
  - `engaging`: Balanced, accessible narrative
  - `comedy`: Humorous and light-hearted
  - `drama`: Emotional and character-driven
  - `documentary`: Factual and journalistic
  - `wholesome`: Uplifting and positive
  - `thriller`: Suspenseful and tense
- **Features**:
  - Dynamic prompt construction
  - Word count constraints
  - Token estimation
  - Style-specific instructions

### 3. **AI Client** (`backend/ai_client.py`)
- **Multi-Provider Support**:
  - OpenAI GPT-4 (ready but not tested)
  - Anthropic Claude (ready but not tested)
  - AWS Bedrock Claude 3 Sonnet (active)
- **Features**:
  - Automatic provider detection
  - Unified interface for all providers
  - Error handling and retries
  - Connection testing

### 4. **Story Generator** (`backend/story_generator.py`)
- **Core Functionality**:
  - End-to-end story generation pipeline
  - Batch processing capabilities
  - Multiple output formats
  - Metadata tracking
- **Output Formats**:
  - Markdown with frontmatter
  - JSON with full metadata
  - Console display

### 5. **CLI Tool** (`backend/cli.py`)
- **Commands**:
  - `generate`: Single story generation
  - `batch`: Multiple story generation
  - `test`: API connection testing
  - `styles`: List available styles
- **Features**:
  - Comprehensive argument parsing
  - Progress indicators
  - Error handling
  - Verbose logging option

---

## Configuration Management

### Environment Variables (`.env`)
```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
AWS_PROFILE=personal
AWS_DEFAULT_REGION=us-east-1
```

### Config Module (`backend/config.py`)
- Centralized configuration management
- Environment variable validation
- Default values for all settings
- Provider auto-detection

---

## Data Flow

1. **User Input** → CLI command with options
2. **Reddit Scraping** → Fetch posts → Filter → Extract comments
3. **Prompt Building** → Format data → Apply style template
4. **AI Generation** → Send to Bedrock → Receive story
5. **Output** → Format → Save to disk → Display

---

## Quality Controls

### Comment Filtering
- Minimum score threshold (default: 10)
- Bot account detection
- Deleted/removed comment handling
- Minimum length requirement
- Text cleaning (remove edits, excessive formatting)

### Story Generation
- Word count constraints (300-500 words default)
- Style consistency enforcement
- Narrative coherence prompting
- Error handling for API failures

---

## File Structure
```
backend/
├── __init__.py          # Package initialization
├── __main__.py          # Module entry point
├── ai_client.py         # AI provider abstraction
├── cli.py               # Command-line interface
├── config.py            # Configuration management
├── prompt_builder.py    # Prompt engineering
├── reddit_scraper.py    # Reddit API integration
└── story_generator.py   # Core story generation logic
```

---

## Performance Metrics
- Reddit API: ~60 requests/minute limit
- Story generation: 15-20 seconds average
- Batch processing: 5-10 stories/minute
- Token usage: ~1000-2000 per story

---

## Security Considerations
- API keys stored in environment variables
- No user authentication required
- Read-only Reddit access
- AWS credentials via profile
- No sensitive data storage

---

## Future Enhancements

### Phase 1: Web Interface
- Streamlit frontend
- Real-time generation
- Story browsing/search
- Export functionality

### Phase 2: Cloud Deployment
- AWS Lambda functions
- API Gateway endpoints
- S3 storage
- CloudFront CDN

### Phase 3: Advanced Features
- Audio narration (Polly)
- Story illustrations (DALL-E)
- User accounts
- Story voting/rating
- Multi-language support

---

## Testing Strategy
- Unit tests for each module
- Integration tests for pipeline
- Mock external APIs
- Performance benchmarks
- Error scenario coverage