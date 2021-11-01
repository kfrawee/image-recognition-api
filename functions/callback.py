# import requests
import json
from boto3.docs.docstring import BatchActionDocstring
import urllib3


def callback(event, context):
    # 1. check ['eventName'] == 'MODIFY'
    try:
        for record in event['Records']:
            if record['eventName'] == 'MODIFY':
                # get callback_url and labels
                callback_url, labels = get_data(record)

                if callback_url:
                    sendLabelsresponsebody = send_labels(callback_url, labels)
                else:
                    sendLabelsresponsebody = "No callback_url provided"

            else:
                pass
        print('------------------------')

        response = {
            "statusCode": 200,
            "body": json.dumps(sendLabelsresponsebody)
        }
        return response

    except Exception as e:
        print(e)
        print('------------------------')

        responsebody = str(e)
        response = {
            "statusCode": 500,
            "body": json.dumps(responsebody)
        }
        return response
    # # TODO check if webhook provided or not

    # if event

    # # check if vallid url if status code is 200 or not
    # url = "https://webhook.site/53919b2d-7d8d-4ad8-ba6a-5929d38ae711"
    # # print(requests.get(url).status_code)

    # # msg = {
    # http = urllib3.PoolManager()
    # data = {'node_id1': "VLTTKeV-ixhcGgq53", 'node_id2': "VLTTKeV-ixhcGgq51", 'type': 1})
    # r = http.request(
    #     "POST", "http://myhost:8000/api/v1/edges",
    #     body=json.dumps(data),
    #     headers={'Content-Type': 'application/json'})
    #     "Labels": [
    #         "car",
    #         "sports car",
    #         "coupe",
    #         "tire",
    #         "wheel"
    #     ]
    # }
    # encoded_msg = json.dumps(msg).encode('utf-8')
    # resp = requests.post(url, data=encoded_msg)

    # response = {
    #     "statusCode": resp.status_code,
    #     "body": encoded_msg
    # }

    # return response


def get_data(record):

    print("GETTING DATA FROM sMODIFY Event")

    # Parse newImage and url
    newImage = record['dynamodb']['NewImage']
    callback_url = newImage['callback_url']['S']
    labels = newImage['labels']['S']

    print(callback_url)
    print(labels)

    print("Done handling MODIFY Event")
    return callback_url, labels


def send_labels(url, labels):
    http = urllib3.PoolManager()
    # check if valid url
    print(http.request("GET", url).status)
    if http.request("GET", url).status != "200":
        body = "Not valid callback url"
    else:
        data = labels
        response = http.request(
            "POST", url,
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        print(response)
        print(response.status)
        body = "Labels sent successfully"

    return {
        "body": json.dumps(body)
    }
