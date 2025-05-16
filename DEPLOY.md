# Deployment Guide: Reddit Comment Stories (AWS)

This guide explains how to deploy the Reddit Comment Stories app to AWS using serverless architecture and static hosting.

---

## Architecture

- **Frontend**: Static site hosted on S3 + CloudFront
- **Backend**: AWS Lambda (Python) with API Gateway
- **Secrets**: AWS Secrets Manager (Reddit API keys, AI API keys)
- **AI Model**: OpenAI API or Bedrock (Anthropic)

---

## Step-by-Step Deployment

### 1. **Infrastructure as Code**
Use AWS CDK (Python or TypeScript)
- Lambda function to:
  - Scrape Reddit via PRAW
  - Call AI model
  - Return story
- API Gateway for HTTP access
- S3 bucket + CloudFront for hosting frontend

### 2. **Build & Deploy**
- Create `.env` with Reddit + AI credentials
- Use `Makefile` or GitHub Actions to:
  - Install deps
  - Package and deploy Lambda
  - Sync frontend to S3
  - Invalidate CloudFront

```bash
make deploy  # example target
```

---

## Optional Enhancements

* Add logging to CloudWatch for debugging
* Use Step Functions if chaining multiple API calls
* Use DynamoDB to cache story results for repeat requests
