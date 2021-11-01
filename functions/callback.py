# import requests
import json
import urllib3


def get_data(record):

    # Parse newImage and url
    newImage = record['dynamodb']['NewImage']
    # print(80*'-')
    # print(newImage)
    # print(80*'-')

    callback_url = newImage['callback_url']['S']
    print(callback_url)

    labels_dict = newImage['labels']['L']
    labels = []
    for l in labels_dict:
        labels.append(l['S'])

    print(labels)

    return callback_url, labels


def send_labels(url, labels):
    http = urllib3.PoolManager()
    # check if valid url
    # print(80*'-')
    # print(http.request("GET", url).status,
    #       type(http.request("GET", url).status))
    # print(80*'-')
    if http.request("GET", url).status != 200:
        body = "Not valid callback url"
    else:
        data = labels
        response = http.request(
            "POST", url,
            body=json.dumps(data),
            headers={'Content-Type': 'application/json'})
        print(80*'-')
        print(response.status)
        print(80*'-')
        body = "Labels have been sent successfully"

    return {
        "body": json.dumps(body)
    }


def callback(event, context):
    # 1. check ['eventName'] == 'MODIFY'
    # print(80*'-')
    # print(event)
    # print(80*'-')
    try:
        for record in event['Records']:
            if record['eventName'] == 'MODIFY':
                # get callback_url and labels
                callback_url, labels = get_data(record)
                # print(80*'-')
                # print(callback_url, labels)
                # print(80*'-')

                if callback_url:
                    sendLabelsresponsebody = send_labels(callback_url, labels)
                else:
                    sendLabelsresponsebody = "No callback_url provided"

            else:
                pass
        # print('------------------------')

        response = {
            "statusCode": 200,
            "body": json.dumps(sendLabelsresponsebody)
        }
        return response

    except Exception as e:
        print(e)
        responsebody = str(e)
        response = {
            "statusCode": 500,
            "body": json.dumps(responsebody)
        }
        return response
