# Technical Specification: Reddit Comment Stories

## Objective

Automate the creation of short stories using the top 5 comments from selected Reddit posts (e.g., AskReddit).

---

## Core Components

### 1. **Reddit Scraper**
- **Tool**: PRAW (Python Reddit API Wrapper)
- **Function**: 
  - Authenticate to Reddit
  - Fetch latest/top posts from a given subreddit (default: AskReddit)
  - For each post, get the post title and top 5 comments (non-deleted, non-bot)

### 2. **Prompt Generator**
- Format the post and comments into a single prompt:

You are a creative writer. Turn the following Reddit post and comments into a short story...

Prompt: <Post title>
Comment 1: ...
Comment 2: ...
...

### 3. **AI Story Generator**
- **Option A**: OpenAI (gpt-4)
- **Option B**: Anthropic Claude via Bedrock
- Return a short story that incorporates all 5 comments in narrative form

### 4. **Frontend (Optional)**
- Streamlit (for MVP) or Next.js for full UI
- Inputs: subreddit, story length
- Output: Generated story + button to export/share

---

## Alternatives

- **API**: Pushshift (faster access but may be outdated); fallback if PRAW fails
- **Output Format**: Could include HTML, JSON, or text export
- **Audio Story**: Use Amazon Polly for speech synthesis if needed

## Challenges

- Detect and filter out deleted or low-quality comments
- Comment formatting (newlines, links, emojis) cleanup
- Keeping stories coherent with wildly different comment tones

## Future Ideas

- Generate illustrations using DALL·E or Midjourney
- Allow users to submit their own post/comment set
- "Story of the Day" feed
