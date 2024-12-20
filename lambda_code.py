import csv
import json
import boto3


def lambda_handler(event, context):
    # Initialize S3 resource
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')

    # Process each SQS message
    for record in event['Records']:
        # Parse SQS message body
        try:
            message = json.loads(record['body'])
            event_params = message['Records'][0]  # S3 event details
            bucket = event_params["s3"]["bucket"]["name"]
            key = event_params["s3"]["object"]["key"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"Error parsing SQS message: {str(e)}")
            continue

        # Validate bucket and key
        if bucket != "Your_Bucket_Name" or not key.startswith("input/"):
            print(f"Skipping invalid bucket or key. Bucket: {bucket}, Key: {key}")
            continue

        print(f"Processing file: {key} from bucket: {bucket}")

        # Read file from S3
        try:
            s3_object = s3_resource.Object(bucket, key)
            data = s3_object.get()['Body'].read().decode('utf-8').splitlines()
        except Exception as e:
            print(f"Error reading S3 object: {str(e)}")
            continue

        # Parse CSV
        try:
            lines = csv.reader(data)
            headers = next(lines)  # Extract headers
            print(f"Headers: {headers}")
            list_data = list(lines)
        except Exception as e:
            print(f"Error processing CSV data: {str(e)}")
            continue

        # Aggregate salary data
        india = []
        us = []
        for i in list_data:
            try:
                country = i[3].strip().lower()
                salary = int(i[2])
                if country == 'india':
                    india.append(salary)
                elif country == 'us':
                    us.append(salary)
            except (IndexError, ValueError) as e:
                print(f"Error processing row {i}: {str(e)}")
                continue

        india_total = sum(india)
        us_total = sum(us)
        print(f"Total India salary spend: {india_total}")
        print(f"Total US salary spend: {us_total}")

        # Prepare output content
        file_content = f"Total India salary spend: {india_total}, Total US salary spend: {us_total}"
        output_key = f"output/agg_{key.split('/')[-1].replace('.csv', '.txt')}"

        # Write results to S3
        try:
            s3_client.put_object(Body=file_content, Bucket=bucket, Key=output_key)
            print(f"Aggregated data written to: {output_key}")
        except Exception as e:
            print(f"Error writing to S3: {str(e)}")
            continue

    return {
        'statusCode': 200,
        'body': "SQS messages processed successfully"
    }