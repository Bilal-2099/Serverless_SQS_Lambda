# Serverless SQS Lambda

## Overview

Basic serverless project using **AWS SQS** and **AWS Lambda**.  
An SQS message triggers a Lambda function which processes the data.

## Files
```
├── README.md
├── lambda_code.py
└── employee3.csv
```

- `lambda_code.py` – Lambda function code triggered by SQS  
- `employee3.csv` – Sample input data  

## Services Used
- AWS Lambda  
- Amazon SQS  
- Amazon S3 (if used inside Lambda)  

## How It Works
1. A message is sent to an SQS queue  
2. SQS triggers the Lambda function  
3. Lambda processes the message and performs required logic  

## Requirements
- Python 3.x  
- boto3  
- AWS account with SQS and Lambda configured  

## Notes
- Commands and infrastructure setup are assumed to be handled separately  
- This project demonstrates an event-driven serverless workflow  

