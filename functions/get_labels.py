""" Get labels by blob_id from dynamodb table """

import json
import boto3
import os


def get_labels(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']
    dynamodb = boto3.resource('dynamodb', region_name=region)
    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])
    # print(80*'-')
    # print(event)
    # print(80*'-')
    try:
        print(80*'-')
        blob_id = event['path']['blob_id']
        print(blob_id)
        print(80*'-')
        # get item
        item = master_table.get_item(
            Key={
                'blob_id': blob_id
            }
        )

        print(80*'-')
        # print(item)
        labels = item['Item']['labels']
        print(labels)
        print(80*'-')
        response = {
            "statusCode": 200,
            "body": json.dumps(labels)
        }
    except Exception as e:
        print(e)
        response = {
            "statusCode": 404,
            "body": json.dumps("Image not found, Please use a valid blob_id, Or upload a new image")
        }

    return response
