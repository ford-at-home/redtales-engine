# AWS Services Analysis: Reddit Comment Stories

## Recommended AWS Services

| AWS Service        | Purpose                                                          | Reason for Use                                                                 |
|--------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Lambda             | Serverless backend to handle API requests and story generation  | Cost-effective, scalable execution of backend logic                            |
| API Gateway        | Create RESTful API endpoints                                    | Easily connect frontend to backend services                                    |
| S3                 | Host static frontend (e.g., Streamlit bundle or static site)    | Scalable, simple hosting for frontend assets                                  |
| CloudFront         | CDN for frontend assets                                         | Improves performance and availability                                          |
| Secrets Manager    | Store Reddit and AI API keys securely                          | Ensures secure management of sensitive data                                    |
| Amazon Polly       | Optional audio generation for stories                          | Converts text stories to lifelike speech                                       |
| DynamoDB (Optional)| Cache or store popular/generated stories                       | NoSQL store that scales easily, low-latency                                    |

## Why These?

- All services support a fully serverless, low-cost stack.
- Scalable and easy to integrate.
- Secure API key handling and flexible compute with Lambda.

## AWS Tutorials

- [Deploying a Serverless Application with AWS Lambda and API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)
- [Hosting a Static Website on Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Using Secrets Manager with Lambda](https://docs.aws.amazon.com/secretsmanager/latest/userguide/integrating_cloudformation.html)
- [Using Amazon Polly](https://docs.aws.amazon.com/polly/latest/dg/what-is.html)
