# Reddit Comment Stories

**Reddit Comment Stories** is an AI-powered storytelling app that scrapes top Reddit posts (especially from AskReddit), grabs the top 5 comments, and turns them into short narrative stories. The result is a creative remix of community insight, wit, and lived experiences into engaging, readable tales.

## Features

- Pulls the top posts from AskReddit (or other subreddits)
- Extracts the top 5 comments from each post
- Uses an AI model (like Claude or GPT) to stitch together a narrative that showcases the perspectives in story format
- Outputs can be saved as Markdown or shared via link
- Optional: Voice synthesis for storytelling audio playback

## Example

> **Prompt**: "What was the weirdest thing you saw at a wedding?"
>
> **Story Output**:
> _It started with a goat in a tuxedo..._

## Use Cases

- Fun entertainment and exploration of Reddit wisdom
- Great for newsletters, creative writing prompts, or podcast content
- A new way to discover Reddit

## Stack

- Python backend
- Reddit API (PRAW or Pushshift)
- OpenAI or Anthropic API for story generation
- Optional: Streamlit, Flask, or Next.js frontend

## License

MIT
