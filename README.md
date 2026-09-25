# AWS Serverless URL Shortener with Analytics

A serverless URL shortening application built using **Amazon API Gateway, AWS Lambda, Amazon DynamoDB, and IAM**.

The application allows users to convert long URLs into short URLs, redirect users from the short URL to the original destination, and track the number of clicks for each shortened URL.

---

## 📌 Project Overview

Long URLs can be difficult to share, remember, and manage. This project provides a simple URL-shortening service using AWS serverless technologies.

The application provides three main capabilities:

1. **Create a shortened URL**
2. **Redirect users using the shortened URL**
3. **View shortened URLs and their click analytics**

The backend is completely serverless, meaning there are no servers or virtual machines to manage.

### High-Level Architecture

```text
                    ┌─────────────────┐
                    │      User       │
                    │    Browser      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    Frontend     │
                    │    index.html   │
                    └────────┬────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │       API Gateway          │
              │      URLShortenerAPI       │
              └─────────────┬──────────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        POST /links     GET /{code}   GET /admin/links
             │              │              │
             ▼              ▼              ▼
        ┌─────────┐    ┌───────────┐   ┌─────────┐
        │ Create  │    │ Redirect  │   │  Admin  │
        │ Lambda  │    │  Lambda   │   │ Lambda  │
        └────┬────┘    └─────┬─────┘   └────┬────┘
             │               │              │
             ▼               ▼              │
        ┌─────────────┐  ┌──────────────┐   │
        │ URLShortener│  │ URLClick     │   │
        │ Table       │  │ Analytics    │   │
        └─────────────┘  │ Table        │   │
                         └──────────────┘   │
                                            │
                                            ▼
                                     URLShortenerTable
```

---

# 🚀 Features

### 1. URL Shortening

Users can enter a long URL and generate a unique short code.

Example:

```text
Original URL:
https://www.example.com/very/long/path

Short URL:
https://4htulcdu61.execute-api.ap-south-2.amazonaws.com/abc123
```

---

### 2. URL Redirection

When a user opens the generated short URL:

```text
Short URL
    ↓
API Gateway
    ↓
Redirect Lambda
    ↓
DynamoDB
    ↓
Original URL
    ↓
HTTP 302 Redirect
```

The user is automatically redirected to the original URL.

---

### 3. Click Analytics

Every time a shortened URL is accessed, the application records information about the click.

The analytics data is stored in:

```text
URLClickAnalyticsTable
```

The application can use this information to determine how many times a shortened URL has been accessed.

---

### 4. Admin Link Listing

The application provides an administrative API endpoint that returns the shortened URLs stored in the system.

It provides information such as:

* Short code
* Original URL
* Creation time
* Click count

---

### 5. Serverless Architecture

The backend uses AWS managed services:

* Amazon API Gateway
* AWS Lambda
* Amazon DynamoDB
* AWS IAM

No EC2 instances or traditional backend servers are required.

---

# 🏗️ AWS Services Used

## Amazon API Gateway

API Gateway provides the HTTP API endpoints used by the frontend.

API Gateway endpoint:

```text
https://4htulcdu61.execute-api.ap-south-2.amazonaws.com
```

The API is deployed in:

```text
AWS Region: ap-south-2
Region: Asia Pacific (Hyderabad)
```

### Routes

| Method | Route          | Purpose                             |
| ------ | -------------- | ----------------------------------- |
| POST   | `/links`       | Create a shortened URL              |
| GET    | `/{code}`      | Redirect to original URL            |
| GET    | `/admin/links` | Retrieve stored links and analytics |

CORS is enabled so that the frontend can communicate with the API.

---

# ⚡ AWS Lambda Functions

The project contains three Lambda functions.

## 1. URLShortenerCreateLambda

Responsible for creating shortened URLs.

### Workflow

```text
Frontend
   ↓
POST /links
   ↓
API Gateway
   ↓
URLShortenerCreateLambda
   ↓
Generate short code
   ↓
Save URL in DynamoDB
   ↓
Return short code
```

The Lambda stores the URL in:

```text
URLShortenerTable
```

---

## 2. URLShortenerRedirectLambda

Responsible for handling short URLs.

### Workflow

```text
User opens short URL
        ↓
GET /{code}
        ↓
API Gateway
        ↓
Redirect Lambda
        ↓
Find code in DynamoDB
        ↓
Record click
        ↓
HTTP 302 Redirect
        ↓
Original URL
```

This Lambda interacts with both:

```text
URLShortenerTable
URLClickAnalyticsTable
```

---

## 3. URLShortenerAdminLambda

Responsible for retrieving stored shortened URLs.

### Workflow

```text
Frontend
   ↓
GET /admin/links
   ↓
API Gateway
   ↓
URLShortenerAdminLambda
   ↓
URLShortenerTable
   ↓
Return links and click information
```

---

# 🗄️ DynamoDB Database

The application uses two DynamoDB tables.

## URLShortenerTable

This table stores the mapping between the generated short code and the original URL.

Conceptually:

| Attribute    | Description               |
| ------------ | ------------------------- |
| `code`       | Unique shortened URL code |
| `target_url` | Original long URL         |
| `created_at` | URL creation timestamp    |

Example:

```json
{
  "code": "abc123",
  "target_url": "https://example.com",
  "created_at": "2026-09-25T07:30:00"
}
```

---

## URLClickAnalyticsTable

This table stores click information for shortened URLs.

It is used by the redirect process to record URL access events.

Conceptually:

```text
Short Code
    ↓
Click Event
    ↓
Analytics Record
```

This allows the application to track URL usage.

---

# 🔐 IAM

AWS IAM controls permissions for the Lambda functions.

The Lambda execution roles provide the required permissions to interact with DynamoDB.

The application follows the AWS serverless security model where Lambda functions use IAM execution roles instead of storing AWS credentials inside the application code.

---

# 🔄 Application Workflow

## Creating a Short URL

The complete process is:

```text
1. User enters a long URL
             ↓
2. Frontend sends POST /links
             ↓
3. API Gateway receives request
             ↓
4. Create Lambda is invoked
             ↓
5. Lambda generates a unique code
             ↓
6. URL is stored in DynamoDB
             ↓
7. Lambda returns the code
             ↓
8. Frontend displays the short URL
```

---

## Redirecting a Short URL

```text
1. User opens the short URL
             ↓
2. API Gateway receives GET /{code}
             ↓
3. Redirect Lambda is invoked
             ↓
4. Lambda searches URLShortenerTable
             ↓
5. Original URL is retrieved
             ↓
6. Click information is recorded
             ↓
7. Lambda returns HTTP 302
             ↓
8. Browser opens original URL
```

---

## Viewing Analytics

```text
Frontend
   ↓
GET /admin/links
   ↓
API Gateway
   ↓
Admin Lambda
   ↓
DynamoDB
   ↓
Link information
   ↓
Frontend
```

---

# 🖥️ Frontend

The frontend is implemented using:

* HTML
* CSS
* JavaScript
* Fetch API

The main frontend file is:

```text
frontend/index.html
```

The frontend communicates directly with API Gateway.

The API base URL is configured as:

```javascript
const API_BASE_URL =
  "https://4htulcdu61.execute-api.ap-south-2.amazonaws.com";
```

---

# 📡 API Documentation

## Create Short URL

### Request

```http
POST /links
```

### Request Body

```json
{
  "target_url": "https://example.com"
}
```

### Example

```bash
curl -X POST \
  https://4htulcdu61.execute-api.ap-south-2.amazonaws.com/links \
  -H "Content-Type: application/json" \
  -d '{"target_url":"https://example.com"}'
```

### Response

```json
{
  "code": "abc123"
}
```

The frontend can construct the short URL using:

```text
https://4htulcdu61.execute-api.ap-south-2.amazonaws.com/abc123
```

---

# 🔗 Redirect API

### Request

```http
GET /{code}
```

Example:

```http
GET /abc123
```

### Expected Behavior

The API looks up `abc123`, records the click, and redirects the browser to the original URL.

The redirect response is:

```text
HTTP 302
```

---

# 📊 Admin API

### Request

```http
GET /admin/links
```

### Example Response

```json
{
  "count": 1,
  "links": [
    {
      "code": "abc123",
      "target_url": "https://example.com",
      "created_at": "2026-09-25T07:30:00",
      "click_count": 1
    }
  ]
}
```

---

# 🧪 Testing

The following functionality has been tested:

| Test                 | Expected Result                     | Status |
| -------------------- | ----------------------------------- | ------ |
| Generate short URL   | Unique short code is returned       | ✅ PASS |
| Store URL            | URL is stored in DynamoDB           | ✅ PASS |
| Open short URL       | User is redirected                  | ✅ PASS |
| Record click         | Analytics information is recorded   | ✅ PASS |
| View analytics       | Link information is displayed       | ✅ PASS |
| List all links       | Admin API returns stored links      | ✅ PASS |
| Frontend API request | Request succeeds without CORS error | ✅ PASS |

---

# 🛠️ Project Structure

```text
AWS-URL-Shortener/
│
├── frontend/
│   └── index.html
│
├── documentation/
│   ├── project-report.docx
│   ├── api-documentation.md
│   └── testing-report.md
│
├── architecture/
│   └── architecture-diagram.png
│
├── screenshots/
│   ├── dynamodb-url-table.png
│   ├── dynamodb-analytics-table.png
│   ├── create-lambda.png
│   ├── redirect-lambda.png
│   ├── admin-lambda.png
│   ├── api-gateway.png
│   ├── api-routes.png
│   ├── frontend.png
│   ├── generated-url.png
│   ├── redirect.png
│   └── analytics.png
│
├── presentation/
│   └── AWS-URL-Shortener.pptx
│
└── README.md
```

---

# ⚙️ Deployment

## Prerequisites

Before deploying the project, you need:

* AWS account
* AWS Console access
* DynamoDB
* AWS Lambda
* API Gateway
* IAM permissions
* A web browser

---

## AWS Resources

Create the following resources:

### DynamoDB

```text
URLShortenerTable
URLClickAnalyticsTable
```

### Lambda

```text
URLShortenerCreateLambda
URLShortenerRedirectLambda
URLShortenerAdminLambda
```

### API Gateway

```text
URLShortenerAPI
```

Routes:

```text
POST /links
GET /{code}
GET /admin/links
```

---

# 🌐 Running the Frontend

The frontend can be opened locally using:

```text
frontend/index.html
```

Open the file in a web browser.

The frontend communicates with the deployed API Gateway backend.

For a production-style deployment, the frontend can be hosted using Amazon S3 and optionally served through Amazon CloudFront.

---

# 🔒 Security Considerations

The current implementation is designed primarily as a learning/demo project.

Important considerations for production deployment include:

### Admin API Authentication

The current:

```text
GET /admin/links
```

endpoint should be protected before production use.

Possible solution:

```text
Amazon Cognito
       ↓
API Gateway
       ↓
Admin Lambda
```

### Additional Production Security

Future production deployment could also include:

* API authentication
* Rate limiting
* AWS WAF
* CloudFront
* HTTPS/custom domain
* CloudWatch monitoring
* More restrictive IAM policies
* Input validation
* URL abuse protection

---

# ⚠️ Current Limitations

The current project has several limitations that are acceptable for a demonstration/academic implementation.

1. The admin API is not currently protected by authentication.
2. The frontend is currently configured to communicate with the deployed API Gateway endpoint.
3. The generated URL uses the API Gateway domain rather than a custom short domain.
4. Analytics are currently focused on click tracking rather than detailed geographic/device analytics.
5. Production-grade rate limiting and abuse prevention are not implemented.

---

# 🚀 Future Enhancements

The project can be extended with:

### Custom Domain

Instead of:

```text
https://4htulcdu61.execute-api.ap-south-2.amazonaws.com/abc123
```

a custom domain could be used:

```text
https://short.example.com/abc123
```

### QR Code Generation

Generate a QR code for every shortened URL.

### URL Expiration

Allow users to specify an expiration time.

### Custom Short Codes

Allow users to request custom aliases.

Example:

```text
short.example.com/github
```

### Authentication

Add user authentication and protected administrator functionality.

### Advanced Analytics

Track:

* Total clicks
* Click timestamps
* Referrer
* Device type
* Browser
* Geographic information

### Monitoring

Integrate Amazon CloudWatch for:

* Lambda logs
* Errors
* API request monitoring
* Performance metrics

---

# 💰 Cost Considerations

This project uses AWS serverless services that generally follow usage-based pricing.

For a small academic/demo workload, usage can be very low.

The main services involved are:

```text
API Gateway
Lambda
DynamoDB
```

AWS pricing should be checked for the specific account, region, and current usage before production deployment.

---

# 📚 Technologies Used

| Technology      | Purpose                          |
| --------------- | -------------------------------- |
| HTML            | Frontend structure               |
| CSS             | Frontend styling                 |
| JavaScript      | Frontend logic/API communication |
| AWS API Gateway | HTTP API                         |
| AWS Lambda      | Serverless backend               |
| Amazon DynamoDB | Data storage                     |
| AWS IAM         | Access control                   |
| AWS Console     | Infrastructure management        |

---

# 🎯 Project Objectives

The project demonstrates the following concepts:

* Serverless application development
* REST/HTTP API design
* AWS Lambda functions
* DynamoDB data storage
* API Gateway routing
* IAM permissions
* CORS configuration
* URL redirection
* Click analytics
* Cloud-based application architecture

---

# ✅ Final Result

The completed application provides an end-to-end URL-shortening system:

```text
                 USER
                  │
                  ▼
             FRONTEND
                  │
                  ▼
           API GATEWAY
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
      CREATE   REDIRECT    ADMIN
      LAMBDA    LAMBDA    LAMBDA
        │         │         │
        │         │         │
        ▼         ▼         ▼
       ┌───────────────────────┐
       │       DYNAMODB        │
       │                       │
       │ URLShortenerTable     │
       │ URLClickAnalyticsTable│
       └───────────────────────┘
```

The project successfully demonstrates how AWS managed services can be combined to build a **serverless URL shortener with analytics without maintaining traditional servers**.

---

# 👥 Team

**Project:** AWS Serverless URL Shortener with Analytics

**Team Members:**

* Add Team Member 1
* Add Team Member 2
* Add Team Member 3
* Add Team Member 4

**AWS Region:**

```text
ap-south-2 (Hyderabad)
```

---

## 📄 License

This project is intended for educational and demonstration purposes.

If this project is based on an existing open-source implementation, retain the original project's license and attribution requirements when distributing the code.
