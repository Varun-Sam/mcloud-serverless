## Overview

This is a serverless image management backend application built using AWS services and deployed locally using LocalStack.

The application supports:

- Upload image
- List images
- Filter images
- Retrieve single image
- Delete image

The project was initially implemented manually using AWS CLI commands to understand the integrations deeply and was later migrated to AWS CDK for Infrastructure as Code (IaC).

---

# Architecture

```text
Client
   ↓
API Gateway
   ↓
Lambda Functions
   ↓
S3 + DynamoDB
```

---

# AWS Services Used

- API Gateway — Expose REST APIs
- Lambda — Serverless business logic
- S3 — Store image files
- DynamoDB — Store image metadata
- IAM — Permissions management
- CloudFormation — CDK deployments
- SSM — CDK bootstrap metadata
- LocalStack — Local AWS simulation
- AWS CDK — Infrastructure as Code

---

# Project Structure

```text
MCloud/
│
├── src/
│   ├── upload_image/
│   │   ├── handler.py
│   │   └── payload.json
│   │
│   ├── list_images/
│   │   └── handler.py
│   │
│   ├── get_image/
│   │   └── handler.py
│   │
│   └── delete_image/
│       └── handler.py
│
├── infrastructure/
│   ├── app.py
│   ├── cdk.json
│   ├── requirements.txt
│   └── infrastructure/
│       └── infrastructure_stack.py
│
├── docker-compose.yml
└── README.md
```

---

# REST API Endpoints

- POST /images — Upload image
- GET /images — List images
- GET /images/{id} — Retrieve image
- DELETE /images/{id} — Delete image

---

# Features

## Upload Image

- Upload image to S3
- Store metadata in DynamoDB
- Generate unique UUID image IDs

---

## List Images

Supports filtering using:

- user_id
- title

---

## Retrieve Image

- Fetch metadata from DynamoDB
- Retrieve image from S3
- Return image as base64 response

---

## Delete Image

- Delete image object from S3
- Delete metadata from DynamoDB

---

# Local Development Setup

## Prerequisites

Install:

- Docker Desktop
- Python 3.11+
- Node.js
- AWS CLI
- AWS CDK

---

# Start LocalStack

```bash
docker compose up -d
```

Verify:

```bash
docker ps
```

---

# Deploy Infrastructure Using CDK

Go to infrastructure folder:

```bash
cd infrastructure
```

Activate virtual environment:

```bash
.venv\Scripts\activate
```

Set dummy AWS credentials:

```bash
set AWS_ACCESS_KEY_ID=test
set AWS_SECRET_ACCESS_KEY=test
set AWS_DEFAULT_REGION=us-east-1
```

Bootstrap CDK:

```bash
cdklocal bootstrap
```

Deploy infrastructure:

```bash
cdklocal deploy
```

---

# API Testing Examples

## Upload Image

```bash
curl -X POST ^
https://YOUR_API_ID.execute-api.localhost.localstack.cloud:4566/prod/images ^
-H "Content-Type: application/json" ^
-d @payload.json
```

---

## List Images

```bash
curl https://YOUR_API_ID.execute-api.localhost.localstack.cloud:4566/prod/images
```

---

## Filter By User

```bash
curl "https://YOUR_API_ID.execute-api.localhost.localstack.cloud:4566/prod/images?user_id=user123"
```

---

## Get Single Image

```bash
curl https://YOUR_API_ID.execute-api.localhost.localstack.cloud:4566/prod/images/IMAGE_ID
```

---

## Delete Image

```bash
curl -X DELETE ^
https://YOUR_API_ID.execute-api.localhost.localstack.cloud:4566/prod/images/IMAGE_ID
```

---

# Unit Testing Plan

## Suggested Tools

- pytest
- unittest.mock
- moto

---

# Unit Tests To Add


