# Cloud Resume Challenge - Backend

This repository contains the backend infrastructure for the [Cloud Resume Challenge](https://cloudresumechallenge.dev/). It features a serverless application built with AWS SAM that creates an API to track the number of visitors to a resume website.

## Architecture

The application uses the following AWS services:

*   **AWS Lambda**: A Python function (`dynamo_api.py`) that contains the core logic for processing API requests and interacting with DynamoDB.
*   **Amazon API Gateway**: Provides an HTTP endpoint that triggers the Lambda function. It is configured to accept `GET`, `POST`, and `OPTIONS` requests on the `/counter` path.
*   **Amazon DynamoDB**: A NoSQL database (`visitor_counter_v1`) used to store and retrieve the visitor count. A single item with a primary key `id: "counter"` holds the count.
*   **AWS SAM (Serverless Application Model)**: Used as the framework for defining the application's resources as Infrastructure as Code (`template.yml`).

When a request hits the API Gateway endpoint, it invokes the Lambda function. The function then reads from or writes to the DynamoDB table to manage the visitor count and returns the updated count in the response.

## API Endpoints

The API is exposed through a single endpoint defined in the SAM template.

*   `ANY /counter`

### Functionality
*   **`GET /counter`**: Retrieves the current visitor count from the DynamoDB table.
*   **`POST /counter`**:
    *   If the request body is `{"visited": false}`, it increments the visitor count by one.
    *   If the request body is `{"visited": true}`, it returns the current count without incrementing.
    *   This endpoint is designed to be called by the frontend to update the count for a new visitor session.
*   **`OPTIONS /counter`**: Handles CORS preflight requests, allowing cross-origin access from the resume website.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment. The workflow is defined in `.github/workflows/python-app.yml` and performs the following steps on every push to the `main` branch:

1.  **Checkout Repository**: Checks out the source code.
2.  **Set up Python**: Configures the Python environment.
3.  **Install Dependencies**: Installs `boto3` and `pytest`.
4.  **Run Pytest Tests**: Executes the unit tests located in `test_dynamo_pytest.py` to validate the Lambda function's logic.
5.  **Configure AWS Credentials**: Sets up AWS access using secrets stored in GitHub.
6.  **Install AWS SAM CLI**: Installs the SAM command-line tool.
7.  **Package Application**: Packages the SAM application, uploading the code to an S3 bucket.
8.  **Deploy Application**: Deploys the packaged application to AWS CloudFormation, creating or updating the necessary resources.

The following secrets must be configured in the repository's GitHub settings for the workflow to succeed:
*   `AWS_ACCESS_KEY_ID`
*   `AWS_SECRET_ACCESS_KEY`
*   `S3_BUCKET` (for SAM deployment artifacts)

## Testing

Unit tests for the Lambda function are implemented using `pytest` and `unittest.mock`. The test file `test_dynamo_pytest.py` covers the following scenarios:

*   Correct handling of `OPTIONS` preflight requests.
*   Retrieving the visitor count via a `GET` request.
*   Incrementing the count for a new visitor via a `POST` request.
*   Handling `POST` requests from returning visitors without incrementing the count.
*   Automatic initialization of the counter in DynamoDB if it doesn't exist.
*   Graceful error handling for malformed JSON in `POST` requests.

## Deployment

The application is deployed using the AWS Serverless Application Model (SAM) CLI.

### Prerequisites
*   AWS CLI
*   AWS SAM CLI
*   An AWS account with appropriate permissions
*   An S3 bucket for deployment artifacts

### Manual Deployment Steps

1.  **Package the application:**
    This command packages the local code and dependencies and uploads them to your S3 bucket.

    ```bash
    sam package \
      --template-file template.yml \
      --output-template-file packaged.yaml \
      --s3-bucket YOUR_S3_BUCKET_NAME
    ```

2.  **Deploy the application:**
    This command deploys the packaged CloudFormation template to your AWS account.

    ```bash
    sam deploy \
      --template-file packaged.yaml \
      --stack-name cloud-resume \
      --capabilities CAPABILITY_IAM \
      --region us-east-1
    ```

After deployment, the API Gateway endpoint URL will be available in the `Outputs` section of the CloudFormation stack.