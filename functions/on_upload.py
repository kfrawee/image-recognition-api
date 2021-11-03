"""  responsible to store the blob_id (image_id) and labels on each successful PUT operation on S3 bucket. """
import json
import boto3
import os


def label_on_upload(event, context):
    """ send images to aws rekognition and store results to dynamodb """
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    # get the uploaded files
    files_uploaded = event['Records']
    for file in files_uploaded:
        blob_id = file['s3']['object']['key']

        # rekognition
        rekognition_client = boto3.client(
            'rekognition', region_name=region)
        # Trying getting labels
        try:
            response = rekognition_client.detect_labels(Image={'S3Object':
                                                               {'Bucket': bucket,
                                                                'Name': blob_id}},
                                                        MaxLabels=5)

            image_labels = []
            for label in response['Labels']:
                image_labels.append(label['Name'].lower())

            # update labels to dynamodb
            dynamodb = boto3.resource('dynamodb', region_name=region)

            update_data_to_master_table_response = update_data_to_master_table(dynamodb=dynamodb,
                                                                               blob_id=blob_id,
                                                                               labels=image_labels)

            on_upload_ResponseBody = {
                "updateImageDataToMasterTableResponse": update_data_to_master_table_response,
            }

            response = {
                "statusCode": 200,
                "body": json.dumps(on_upload_ResponseBody)
            }

        except Exception as e:

            # delete invalid (failed) record from dynamodb
            delete_data_from_master_table(dynamodb=dynamodb,
                                          blob_id=blob_id)

            response = {
                "body": json.dumps(str(e))
            }

        # delete the object after labeling
        delete_s3_object(bucket, region, blob_id)

        return response


def update_data_to_master_table(dynamodb, blob_id, labels):

    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    master_table.update_item(Key={'blob_id': blob_id},
                             AttributeUpdates={
                                 'labels':
                                 {'Value': labels,
                                  'Action': 'PUT'}
    })

    # response
    response = {
        "statusCode": 201,
        "body": json.dumps({'blob_id': blob_id,
                            'labels': labels})
    }
    print(response)

    return response


def delete_data_from_master_table(dynamodb, blob_id):

    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    master_table.delete_item(
        Key={
            'blob_id': blob_id
        }
    )

    # response
    response = {
        "statusCode": 200,
        "body": json.dumps({'blob_id': blob_id})
    }

    return response


def delete_s3_object(bucket, region, key):
    """ delete object from s3 """
    s3_client = boto3.client('s3', region_name=region)
    s3_client.delete_object(Bucket=bucket, Key=key)
