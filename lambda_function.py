import csv
import json
import boto3
from io import StringIO

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = 'tabletocsv'
BUCKET_NAME = 'table.ro.csv'

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    items = response['Items']

    if not items:
        return {
            'statusCode': 200,
            'body': 'No data found in DynamoDB table'
        }

    # Create CSV in memory
    csv_buffer = StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=items[0].keys())
    writer.writeheader()
    writer.writerows(items)

    # Upload CSV to S3
    s3.put_object(Bucket=BUCKET_NAME, Key='dynamodb_data.csv', Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'CSV file created and uploaded to S3 successfully'
    }
