# Sprint 0 Quick Start Guide

## Day 1-2: Project Foundation Setup

This guide helps you immediately start Sprint 0 of the Reddit Comment Stories project. Follow these steps in order.

## Prerequisites

- Python 3.9 or higher installed
- Git configured
- GitHub account with repository access
- Reddit account for API access

## Step 1: Environment Setup (30 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/redtales-engine.git
cd redtales-engine

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Create project structure
mkdir -p backend/{scrapers,generators,utils}
mkdir -p frontend/components
mkdir -p infrastructure/cdk
mkdir -p output/stories
mkdir -p tests/{unit,integration}

# Create initial files
touch backend/__init__.py
touch backend/scrapers/__init__.py
touch backend/generators/__init__.py
touch backend/utils/__init__.py
touch requirements.txt
touch requirements-dev.txt
touch .env.example
touch Makefile
```

## Step 2: Initial Dependencies (15 minutes)

Create `requirements.txt`:
```txt
# Reddit API
praw==7.7.1

# AI APIs
openai==1.35.0
anthropic==0.28.0

# Web Framework
streamlit==1.35.0

# AWS
boto3==1.34.0

# Utilities
python-dotenv==1.0.0
requests==2.31.0
pydantic==2.7.0

# Data handling
pandas==2.2.0
markdown==3.6
```

Create `requirements-dev.txt`:
```txt
# Testing
pytest==8.2.0
pytest-asyncio==0.23.0
pytest-cov==5.0.0

# Code Quality
black==24.4.0
flake8==7.0.0
mypy==1.10.0
pre-commit==3.7.0

# Development
ipython==8.24.0
jupyter==1.0.0
```

Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Step 3: Reddit API Setup (45 minutes)

1. **Create Reddit App**:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Name: "Reddit Comment Stories Dev"
   - App type: Select "script"
   - Description: "AI story generator from Reddit comments"
   - About URL: (leave blank)
   - Redirect URI: http://localhost:8000
   - Click "Create app"
   - Note your CLIENT_ID (under "personal use script")
   - Note your SECRET key

2. **Create `.env.example`**:
```env
# Reddit API
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
REDDIT_USER_AGENT=RedditCommentStories/1.0 by YourUsername

# AI APIs (choose one)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO

# Storage
OUTPUT_DIR=./output/stories
```

3. **Create `.env`** from the example and fill in your credentials

4. **Test Reddit Connection** - Create `test_reddit_auth.py`:
```python
#!/usr/bin/env python3
import os
import praw
from dotenv import load_dotenv

load_dotenv()

def test_reddit_connection():
    """Test Reddit API authentication"""
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        # Test by fetching a subreddit
        subreddit = reddit.subreddit('AskReddit')
        print(f"Successfully connected to Reddit!")
        print(f"Subreddit: {subreddit.display_name}")
        print(f"Subscribers: {subreddit.subscribers:,}")
        
        # Fetch one post as a test
        for post in subreddit.hot(limit=1):
            print(f"\nSample post: {post.title}")
            print(f"Score: {post.score}")
            print(f"Comments: {post.num_comments}")
            
        return True
        
    except Exception as e:
        print(f"Reddit authentication failed: {e}")
        return False

if __name__ == "__main__":
    test_reddit_connection()
```

Run: `python test_reddit_auth.py`

## Step 4: AI API Setup (30 minutes)

Choose either OpenAI or Claude:

### Option A: OpenAI Setup
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Option B: Claude Setup
1. Get API key from https://console.anthropic.com/
2. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

**Test AI Connection** - Create `test_ai_auth.py`:
```python
#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    """Test OpenAI API connection"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello, Reddit Stories!'"}],
            max_tokens=50
        )
        
        print("OpenAI Response:", response.choices[0].message.content)
        return True
    except Exception as e:
        print(f"OpenAI test failed: {e}")
        return False

def test_anthropic():
    """Test Anthropic Claude API connection"""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Hello, Reddit Stories!'"}]
        )
        
        print("Claude Response:", response.content[0].text)
        return True
    except Exception as e:
        print(f"Claude test failed: {e}")
        return False

if __name__ == "__main__":
    # Test whichever API key is configured
    if os.getenv('OPENAI_API_KEY'):
        test_openai()
    elif os.getenv('ANTHROPIC_API_KEY'):
        test_anthropic()
    else:
        print("No AI API key configured!")
```

Run: `python test_ai_auth.py`

## Step 5: Create Makefile (15 minutes)

Create `Makefile` for common commands:
```makefile
.PHONY: setup test run clean install dev-install

# Setup commands
setup: install
	@echo "Setting up Reddit Comment Stories development environment..."
	python -m pip install --upgrade pip
	pre-commit install

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Test commands
test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=backend --cov-report=html

# Run commands
run:
	streamlit run frontend/app.py

run-cli:
	python -m backend.main

# Quality checks
lint:
	flake8 backend/ tests/
	black --check backend/ tests/

format:
	black backend/ tests/

typecheck:
	mypy backend/

# Clean commands
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

# Development helpers
test-auth:
	python test_reddit_auth.py
	python test_ai_auth.py

create-issue:
	@echo "Opening GitHub to create a new issue..."
	@open https://github.com/yourusername/redtales-engine/issues/new
```

## Step 6: Git Configuration (10 minutes)

Create `.gitignore`:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/
ENV/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/

# Output
output/
*.log
*.mp3
*.wav

# Temporary
tmp/
temp/
```

## Step 7: First Commit (5 minutes)

```bash
git add .
git commit -m "Initial project setup - Sprint 0 foundation"
git push origin main
```

## Step 8: Create GitHub Issues (20 minutes)

1. Go to your GitHub repository
2. Navigate to Issues → New Issue
3. Copy the templates from `GITHUB_ISSUES.md`
4. Create the first 5 issues for Milestone 0
5. Assign yourself to Issue #1

## Validation Checklist

Before moving to actual development:

- [ ] Virtual environment activated
- [ ] All dependencies installed without errors
- [ ] Reddit API test successful
- [ ] AI API test successful
- [ ] Project structure created
- [ ] Git repository initialized and pushed
- [ ] At least 5 GitHub issues created
- [ ] Makefile commands working

## Next Steps

1. **Start Issue #1**: Complete the project structure setup
2. **Daily Standup**: Even if solo, write brief progress notes
3. **Commit Often**: Make small, frequent commits
4. **Test Everything**: Write tests as you code

## Quick Commands Reference

```bash
# Start your day
source venv/bin/activate
git pull origin main

# Test your setup
make test-auth

# Run linting
make lint

# Format code
make format

# Run tests
make test

# Clean up
make clean
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure virtual environment is activated
2. **Reddit 401 Error**: Check CLIENT_ID and SECRET in .env
3. **AI API Error**: Verify API key and check account credits
4. **Permission Denied**: Check file permissions, especially on scripts

### Getting Help

- Check the `TROUBLESHOOTING.md` section in CLAUDE.md
- Review closed GitHub issues for similar problems
- Create a new issue with the `help-wanted` label

---

You're now ready to start Sprint 0! Begin with Issue #1 and work through the setup tasks. Remember to update issue status as you progress.