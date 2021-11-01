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
                                                  ExpiresIn=600,  # 10 minuets 10*60
                                                  HttpMethod='PUT')

    return upload_url, blob_id


def add_date_to_master_table(dynamodb, blob_id, callback_url):

    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    # create item
    item = {
        'blob_id': str(blob_id),
        'created_on': str(datetime.datetime.now()),
        'callback_url': callback_url,
    }

    # add date to table
    master_table.put_item(Item=item)

    # response
    response = {
        "statusCode": 201,
        "body": json.dumps(item)
    }
    # print(response)

    return response


def upload(event, context):
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    # generate url and blob_id
    upload_url, blob_id = generate_presigned_url(bucket, region)

    # check if the request have a body with a callback url or not
    # get callback_url
    try:
        callback_url = event["body"]["callback_url"]
    except Exception as e:
        callback_url = ""

    # add data to dynamodb
    dynamodb = boto3.resource('dynamodb', region_name=region)
    add_date_to_master_table_response = add_date_to_master_table(dynamodb,
                                                                 blob_id,
                                                                 callback_url)

    on_upload_ResponseBody = {
        "addDataToMasterTableResponse": add_date_to_master_table_response,
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(on_upload_ResponseBody)
    }

    return {"statusCode": 200,
            "body": json.dumps(response)}
