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

    url = s3_client.generate_presigned_url(ClientMethod='put_object',
                                           Params={'Bucket': bucket,
                                                   'Key': f'{blob_id}.jpg'},  # TODO use the format from filename from request body not hardcoded
                                           ExpiresIn=600,  # 10 minuets 10*60
                                           HttpMethod='PUT')

    return url, blob_id


def upload(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    # generate url and blob_id
    url, blob_id = generate_presigned_url(bucket, region)

    # response body
    body = {"upload_url": url,
            "blob_id": blob_id}

    return {"statusCode": 200,
            "body": json.dumps(body)}
