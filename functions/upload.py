""" return a genereted presigned url and blob_id """
import json
import os
import datetime
import re
import boto3


def generate_presigned_url(bucket: str, region: str = 'us-east-1'):
    """ Generate presigned url for upload, and blob_id for later usage """

    # generate blob_id from timestamp
    blob_id = re.sub('[- :.]', '', str(datetime.datetime.now()))

    # presigned url
    s3_client = boto3.client('s3',
                             region_name=region,
                             config=boto3.session.Config(s3={'addressing_style': 'path'},
                                                         signature_version='s3v4'))

    upload_url = s3_client.generate_presigned_url(ClientMethod='put_object',
                                                  Params={'Bucket': bucket,
                                                          'Key': f'{blob_id}.jpg'},  # TODO use the format from filename from request body not hardcoded
                                                  ExpiresIn=3600,  # 60 minuets 60*60 for testing
                                                  HttpMethod='PUT')

    return upload_url, blob_id


def add_date_to_master_table(dynamodb, blob_id, callback_url):

    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    # create item
    item = {
        'blob_id': str(blob_id),
        'created_on': str(datetime.datetime.now()),
        # 'labels': "",
        'callback_url': callback_url,
    }

    # add date to table
    master_table.put_item(Item=item)

    # response
    response = {
        "statusCode": 201,
        "body": {
            'blob_id': str(blob_id),
            'created_on': str(datetime.datetime.now()),
            'callback_url': callback_url,
        }
    }
    # print(response)

    return response


def upload(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    print(80*'-')
    print(event)
    print(80*'-')
    # generate url and blob_id
    upload_url, blob_id = generate_presigned_url(bucket, region)

    # check if the request have a body with a callback url or not
    # get callback_url
    try:
        callback_url = json.loads(event["body"])["callback_url"]
        print(80*'-')
        print(callback_url)
        print(80*'-')

    except Exception as e:
        print(e)
        callback_url = ""

    # add data to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name=region)
    add_date_to_master_table(dynamodb,
                             blob_id,
                             callback_url)

    responseBody = {"blob_id": blob_id,
                    "upload_url": upload_url,
                    "callback_url": callback_url}

    return {"statusCode": 200,
            "body": json.dumps(responseBody)}
