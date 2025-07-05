# GitHub Issues Templates for Reddit Comment Stories

Copy and paste these templates to create issues in your GitHub repository. Each issue is tagged with appropriate labels and milestone assignments.

## Milestone 0: Project Setup Issues

### Issue #1: Setup Python project structure and virtual environment
**Labels:** `setup`, `infrastructure`, `milestone-0`
```markdown
## Description
Create the foundational Python project structure with proper virtual environment setup and dependency management.

## Acceptance Criteria
- [ ] Python 3.9+ virtual environment created
- [ ] Project directory structure matches proposed layout
- [ ] requirements.txt with initial dependencies
- [ ] .gitignore for Python projects
- [ ] Basic README.md with setup instructions
- [ ] Makefile or setup script for easy environment setup

## Technical Details
- Use venv or poetry for dependency management
- Include development dependencies (pytest, black, flake8)
- Setup pre-commit hooks for code quality
```

### Issue #2: Configure Reddit API authentication
**Labels:** `setup`, `integration`, `milestone-0`
```markdown
## Description
Set up Reddit API authentication using PRAW and validate connection.

## Acceptance Criteria
- [ ] Reddit app created on reddit.com/prefs/apps
- [ ] .env.example file with required Reddit variables
- [ ] Authentication test script that fetches user info
- [ ] Error handling for invalid credentials
- [ ] Documentation for obtaining Reddit API credentials

## Technical Details
- Use PRAW (Python Reddit API Wrapper)
- Implement credential validation on startup
- Add connection retry logic
```

### Issue #3: Setup OpenAI/Claude API integration
**Labels:** `setup`, `integration`, `milestone-0`
```markdown
## Description
Configure AI model API integration with support for both OpenAI and Claude.

## Acceptance Criteria
- [ ] Environment variables for API keys
- [ ] Model selection configuration
- [ ] Basic prompt test that returns response
- [ ] Error handling for API failures
- [ ] Cost tracking/logging setup

## Technical Details
- Support both OpenAI and Anthropic SDKs
- Implement interface for swappable models
- Add request/response logging
```

---

## Milestone 1: Proof of Concept Issues

### Issue #6: Implement Reddit post fetching with PRAW
**Labels:** `feature`, `backend`, `milestone-1`
```markdown
## Description
Create Reddit scraper module that fetches top posts from specified subreddits.

## Acceptance Criteria
- [ ] Fetch top N posts from subreddit
- [ ] Support multiple time ranges (day, week, month)
- [ ] Extract post metadata (title, score, created_utc)
- [ ] Handle NSFW filtering
- [ ] Implement rate limiting (60 req/min)

## Technical Details
```python
class RedditScraper:
    def get_top_posts(self, subreddit: str, limit: int = 10, time_filter: str = 'day')
    def get_post_details(self, post_id: str)
```
```

### Issue #7: Create comment extraction and filtering logic
**Labels:** `feature`, `backend`, `milestone-1`
```markdown
## Description
Extract and filter top comments from Reddit posts with quality checks.

## Acceptance Criteria
- [ ] Extract top 5 comments by score
- [ ] Filter out deleted/removed comments
- [ ] Exclude bot comments (AutoModerator, etc.)
- [ ] Minimum score threshold (10 upvotes)
- [ ] Preserve comment metadata
- [ ] Handle nested comments appropriately

## Technical Details
```python
def get_top_comments(post_id: str, limit: int = 5) -> List[Comment]
def is_valid_comment(comment: Comment) -> bool
def clean_comment_text(text: str) -> str
```
```

### Issue #8: Design AI prompt template for story generation
**Labels:** `feature`, `ai`, `milestone-1`
```markdown
## Description
Create effective prompt engineering for coherent story generation from Reddit comments.

## Acceptance Criteria
- [ ] Prompt template that produces 300-500 word stories
- [ ] Clear instructions for narrative flow
- [ ] Context preservation from all comments
- [ ] Multiple prompt variations for testing
- [ ] Consistent output format

## Example Prompt Structure
```
You are a creative writer. Transform this Reddit post and its top comments into an engaging short story.

Post Title: {title}
Comments:
1. {comment_1}
2. {comment_2}
...

Create a cohesive narrative that naturally incorporates all perspectives.
```
```

---

## Milestone 2: MVP Release Issues

### Issue #12: Create Streamlit web interface layout
**Labels:** `feature`, `frontend`, `milestone-2`
```markdown
## Description
Build the basic Streamlit web interface with intuitive layout and navigation.

## Acceptance Criteria
- [ ] Header with app title and description
- [ ] Subreddit selection dropdown (prepopulated options)
- [ ] Number of posts selector (1-10)
- [ ] Generate button with loading state
- [ ] Story display area with formatting
- [ ] Responsive layout for mobile

## UI Components
- st.selectbox for subreddit selection
- st.slider for number of posts
- st.button with spinner for generation
- st.markdown for story display
- st.expander for source attribution
```

### Issue #14: Add batch processing capability
**Labels:** `feature`, `performance`, `milestone-2`
```markdown
## Description
Enable processing multiple Reddit posts into stories in a single session.

## Acceptance Criteria
- [ ] Process up to 10 posts concurrently
- [ ] Progress bar showing completion
- [ ] Individual story generation status
- [ ] Error handling per story
- [ ] Batch results summary

## Technical Requirements
- Use asyncio or threading for parallel processing
- Implement progress callback system
- Add circuit breaker for API failures
```

---

## Milestone 3: Enhanced Features Issues

### Issue #19: Implement multiple narrative style templates
**Labels:** `feature`, `ai`, `milestone-3`
```markdown
## Description
Add support for different narrative styles to create variety in generated stories.

## Acceptance Criteria
- [ ] At least 3 narrative styles: Comedy, Drama, Documentary
- [ ] Style selector in UI
- [ ] Style-specific prompt templates
- [ ] Consistent quality across styles
- [ ] User can preview style descriptions

## Style Examples
- **Comedy**: Light-hearted, humorous take with punchlines
- **Drama**: Emotional, character-driven narrative
- **Documentary**: Factual, journalistic presentation
```

### Issue #21: Integrate Amazon Polly for audio generation
**Labels:** `feature`, `audio`, `milestone-3`
```markdown
## Description
Add text-to-speech capability using Amazon Polly for audio story versions.

## Acceptance Criteria
- [ ] AWS Polly integration with boto3
- [ ] Multiple voice options (at least 3)
- [ ] MP3 file generation
- [ ] Audio file storage in S3
- [ ] Estimated cost per story shown

## Technical Details
```python
class AudioGenerator:
    def generate_audio(story_text: str, voice: str = 'Matthew') -> str
    def upload_to_s3(audio_file: bytes, story_id: str) -> str
```
```

---

## Milestone 4: Production Readiness Issues

### Issue #27: Create AWS CDK infrastructure code
**Labels:** `infrastructure`, `deployment`, `milestone-4`
```markdown
## Description
Define complete AWS infrastructure using CDK for production deployment.

## Acceptance Criteria
- [ ] Lambda functions for story generation
- [ ] S3 buckets for storage
- [ ] API Gateway for REST endpoints
- [ ] CloudFront distribution
- [ ] RDS/DynamoDB for metadata
- [ ] All resources tagged appropriately

## CDK Stack Components
- Story processing Lambda
- S3 bucket with lifecycle rules
- API Gateway with rate limiting
- CloudWatch log groups
- IAM roles with least privilege
```

### Issue #35: Implement scheduled story generation
**Labels:** `feature`, `automation`, `milestone-4`
```markdown
## Description
Create automated daily story generation from trending Reddit posts.

## Acceptance Criteria
- [ ] EventBridge rule for daily execution
- [ ] Lambda function for scheduled processing
- [ ] Configurable subreddit list
- [ ] Email notification on completion
- [ ] Story quality threshold before publishing
- [ ] Failure alerting

## Schedule Options
- Daily at 9 AM EST
- Process top 10 posts from each configured subreddit
- Store results with "daily-digest" tag
```

---

## Label Definitions

### Type Labels
- `feature`: New functionality
- `bug`: Something isn't working
- `enhancement`: Improvement to existing feature
- `documentation`: Documentation updates
- `infrastructure`: DevOps, deployment, tooling

### Component Labels
- `frontend`: UI/UX related
- `backend`: Server-side logic
- `integration`: External API integrations
- `ai`: AI/ML model related
- `audio`: Audio generation features

### Priority Labels
- `critical`: Must have for milestone
- `high`: Should have for milestone
- `medium`: Nice to have
- `low`: Future consideration

### Milestone Labels
- `milestone-0`: Project Setup
- `milestone-1`: Proof of Concept
- `milestone-2`: MVP Release
- `milestone-3`: Enhanced Features
- `milestone-4`: Production Readiness