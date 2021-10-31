""" Get labels by blob_id from dynamodb table """

import json
import boto3
import os


def get_labels(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']
    dynamodb = boto3.resource('dynamodb', region_name=region)
    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    blob_id = event['pathParameters']['blob_id']
    print(blob_id)
    try:
        labels = master_table.get_item(
            Key={
                'blob_id': blob_id
            }
        )

        print(labels)
        response = {
            "statusCode": 200,
            "body": json.dumps(labels['Item'])
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 400,
            "body": json.dumps("Not Found, Please use a valid blob_id, Or upload new image.")
        }

    return response
