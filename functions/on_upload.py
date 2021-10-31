"""  responsible to store the blob_id (image_id) and labels on each successful PUT operation on S3 bucket. """
import json
import datetime
import boto3
import os


def label_on_upload(event, context):
    """ send images to aws rekognition and store results to dynamodb """
    bucket = os.environ['BUCKET_NAME']
    region = os.environ['REGION_NAME']

    # get file_name
    files_uploaded = event['Records']
    for file in files_uploaded:
        file_name = file['s3']['object']['key']
        blob_id = file_name.split('.')[0]  # remove .jpg
        print(file_name, blob_id)

        # rekognition
        rekognition_client = boto3.client(
            'rekognition', region_name=region)
        try:
            response = rekognition_client.detect_labels(Image={'S3Object':
                                                               {'Bucket': bucket,
                                                                'Name': file_name}},
                                                        MaxLabels=5)
            # print(response)

            image_labels = []
            # print(f'Detected Labeles for {file_name}\n')
            for label in response['Labels']:
                image_labels.append(label['Name'].lower())
                # print(f"Label: {label['Name']}")

            # add results to dynamodb
            dynamodb = boto3.resource('dynamodb', region_name=region)
            add_image_date_to_master_table_response = add_image_date_to_master_table(dynamodb=dynamodb,
                                                                                     blob_id=blob_id,
                                                                                     labels=image_labels)
            # print(json.dumps(add_image_date_to_master_table_response))

            on_upload_ResponseBody = {
                "addImageDataToMasterTableResponse": add_image_date_to_master_table_response,
            }

            response = {
                "statusCode": 200,
                "body": json.dumps(on_upload_ResponseBody)
            }

            # delete image after labeling
        except Exception as e:
            response = {
                "statusCode": 500,
                "body": json.dumps(str(e))
            }

        print(response)

        delete_s3_object(bucket, region, file_name)
        return response


def add_image_date_to_master_table(dynamodb, blob_id, labels):

    master_table = dynamodb.Table(os.environ['MASTER_TABLE'])

    # data
    item = {
        'blob_id': str(blob_id),
        'labels': labels,
        'created_on': str(datetime.datetime.now())}

    # add image date to table
    master_table.put_item(Item=item)

    # response
    response = {
        "statusCode": 201,
        "body": json.dumps(item)
    }
    print(response)

    return response


# TODO: Delete the object from s3
def delete_s3_object(bucket, region, file_name):
    s3_client = boto3.client('s3', region_name=region)
    s3_client.delete_object(Bucket=bucket, Key=file_name)
