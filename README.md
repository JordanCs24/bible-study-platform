Bible Study Platform

A cloud-hosted Bible study web application built on AWS. Search scripture
by verse reference, keyword, or ask deep questions and receive warm,
thoughtful responses powered by AI.

Live Demo

Coming soon — deployment to custom domain in Phase 4.

Features

Phase 1 (Complete)


Search by direct verse reference (John 3:16, John 3:16-20, John 3)
Browse all 66 books of the Bible by Old and New Testament
Translation toggle between KJV and WEB
Intelligent input normalization handling capitalization, missing spaces,
and edge cases like 1Chronicles3:12
Graceful error handling for misspelled or nonexistent references
Fully automated CI/CD pipeline deploying to AWS on every push


Phase 2 (Complete)


AI-powered verse finder — type a single keyword and receive the most
well known verses related to that topic
Warm conversational responses for deep spiritual questions powered by
AWS Bedrock and Claude Haiku 4.5
Custom AI personality prompt — caring, spiritually deep, never preachy
Automatic failover to Amazon Nova Lite if the primary model is unavailable
SNS email alerting so the developer is notified the moment AI goes down
Graceful 503 error response to users if both AI models fail
Input length protection limiting queries to 500 characters to prevent abuse
Lambda timeout tuned to 30 seconds to handle AI response times
Markdown rendering in the frontend for clean formatted AI responses


Phase 3 (Planned)


Data analytics dashboard treating the Bible as a 31,000 verse dataset
Word frequency charts across books and testaments
Thematic heat maps showing where themes like love and faith concentrate
Reading plan builder by topic, pace, or book


Phase 4 (Planned)


User accounts with saved history and bookmarks via AWS Cognito
Full Bible reader mode with chapter by chapter navigation
Shareable verse cards
Custom domain and production polish


Tech Stack

Frontend


HTML, CSS, JavaScript
Marked.js for rendering AI markdown responses
Hosted on AWS S3 with CloudFront CDN


Backend


AWS Lambda (Python 3.13) — serverless function handling all query routing
AWS API Gateway — HTTP API exposing Lambda as a public endpoint
AWS Bedrock — AI layer for conversational and keyword queries

Primary model: Claude Haiku 4.5 (Anthropic) via cross-region inference profile
Fallback model: Amazon Nova Lite via cross-region inference profile





Alerting


AWS SNS — email notifications when the AI layer becomes unavailable


Data


AWS S3 data lake storing all 66 KJV Bible books as structured JSON
AWS Athena for SQL queries across Bible data (Phase 3)
KJV and WEB translations (both fully public domain)


Infrastructure


AWS IAM with least privilege security principles
GitHub Actions for automated CI/CD deployment
CloudWatch for monitoring and logging
AWS Budgets for cost monitoring and alerting


Architecture

User Browser
→ CloudFront CDN
→ S3 Static Frontend (HTML, CSS, JS)
→ API Gateway HTTP API
→ Lambda Function (Python)
  → Type 1: Direct verse reference → S3 data lake lookup (no AI cost)
  → Type 2: Single keyword → AWS Bedrock (Claude Haiku 4.5)
  → Type 3: Conversational question → AWS Bedrock (Claude Haiku 4.5)
      → On failure: Amazon Nova Lite fallback
      → On total failure: SNS alert + 503 response to user
→ Response rendered in browser

Query Types

The Lambda dispatcher automatically detects and routes three types of queries.

Type 1: Direct verse reference
Examples: John 3:16, John 3:16-20, 1 Chronicles 3:5, John 3
Routes directly to S3 for an instant lookup with no AI cost.

Type 2: Single keyword
Examples: love, faith, forgiveness
Routes to AWS Bedrock which returns the most well known verses
containing that word. Limited to 300 output tokens.

Type 3: Conversational question
Examples: Are we going to be married in heaven, Why does God allow suffering
Routes to AWS Bedrock with a custom system prompt that responds with
warmth, care, and spiritual depth without being preachy.
Limited to 600 output tokens.

AI Resilience Architecture

The AI layer is built with a two-model failover system.

Bedrock call → Claude Haiku 4.5
    ↓ (on failure)
SNS alert sent to developer emails
    ↓
Retry with Amazon Nova Lite
    ↓ (on failure)
Return 503 to user with friendly error message

This means a single model outage never results in a broken experience
for the user without the developer being notified.

Input Normalization

The backend normalizes all input before processing so users never have
to worry about formatting. All of these inputs produce the same result.

john3:16
JOHN 3:16
JOHN 3 : 16
1chronicles3:5
1Chronicals3:12

Project Structure

bible-study-platform/
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── app.js
│   └── data/
│       └── Bible-kjv/        # All 66 KJV books as JSON
├── backend/
│   └── lambda/
│       └── verse_search/
│           ├── handler.py    # Lambda function
│           └── test_handler.py  # Unit tests
├── infrastructure/
│   └── README.md
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions CI/CD
└── README.md

Setup and Development

Prerequisites


AWS account with Free Tier
Python 3.13+
AWS CLI configured with IAM credentials
Node.js (for AWS SAM CLI, optional)


Local Development

Clone the repository.

bash
git clone https://github.com/YOUR-USERNAME/bible-study-platform.git

cd bible-study-platform

Create and activate a virtual environment.

bash
python -m venv .venv
source .venv/bin/activate

Install dependencies.

bash
pip install boto3

Run unit tests.

bash
cd backend/lambda/verse_search
python -m unittest test_handler.py -v

Deployment

Every push to the main branch that includes changes to
backend/lambda/verse_search/ automatically deploys to AWS Lambda
via GitHub Actions.

Required GitHub Secrets:

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

Data Sources

KJV Bible data sourced from
aruljohn/Bible-kjv,
public domain.

WEB translation coming in Phase 2.

Security


Root AWS account is never used for application access
Dedicated IAM user with scoped permissions for development
Lambda execution role follows least privilege with scoped IAM policies:

S3 read access scoped to the bible-platform-jordan bucket
Bedrock InvokeModel for AI queries
SNS Publish scoped to the specific alerts topic ARN
CloudWatch logging



No API keys or credentials committed to version control
GitHub Secrets used for all sensitive values
Input length validation prevents oversized requests from reaching Bedrock


Cost Architecture

This project is designed to minimize AWS spend at every layer.


Type 1 queries hit S3 only — no AI cost
Type 2 queries capped at 300 output tokens
Type 3 queries capped at 600 output tokens
Input queries limited to 500 characters
Claude Haiku 4.5 chosen as primary model for its low cost per token
AWS Budgets alert configured at $5/month threshold
Free Tier covers Lambda, API Gateway, S3, and CloudWatch entirely


Roadmap


 Phase 1: Foundation, static frontend, verse search, S3 data lake,
Lambda dispatcher, API Gateway, CI/CD
 Phase 2: AI layer with AWS Bedrock, Claude Haiku 4.5, Nova Lite
fallback, SNS alerting, cost controls, markdown rendering
 Phase 3: Data analytics pipeline with Athena, visualizations
 Phase 4: User accounts, custom domain, production polish


Author

Jordan Sowell
Rising Junior, Computer Science with AI Minor
Aspiring Cloud Engineer

Built as a portfolio project for cloud engineering internship applications,
demonstrating hands-on AWS architecture, serverless backend development,
AI integration, fault tolerance design, and cloud cost management.
ShareProject contentAWS Cloud and AI LearningCreated by youAdd PDFs, documents, or other text to reference in this project.