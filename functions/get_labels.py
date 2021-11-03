""" Get labels by blob_id from dynamodb table """

import json
import boto3
import os


def get_labels(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    dynamodb = boto3.resource('dynamodb', region_name=region)
    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    try:
        # get item
        blob_id = event['path']['blob_id']
        item = master_table.get_item(
            Key={
                'blob_id': blob_id
            }
        )

        # get labels
        labels = item['Item']['labels']

        response = {
            "statusCode": 200,
            "body": labels
        }

    except Exception as e:
        response = {
            "statusCode": 404,
            "body": json.dumps("Image not found. Please use a valid blob_id, or maybe you have uploaded an invalid image format")
        }

    return response
