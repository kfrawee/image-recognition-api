""" Send labels to callback url """
import json
import urllib3


def get_data(record):
    """ Parse data from the newImage """

    # Get callback_url
    newImage = record['dynamodb']['NewImage']
    callback_url = newImage['callback_url']['S']

    # Get labels
    labels_dict = newImage['labels']['L']
    labels = []
    for l in labels_dict:
        labels.append(l['S'])

    return callback_url, labels


def send_labels(url, labels):
    """ Send labels to the callback url """
    http = urllib3.PoolManager()
    # check if valid url by sending a get request

    if http.request("GET", url).status != 200:
        body = "Invalid callback url"

    else:
        # send labels
        response = http.request(
            "POST", url,
            body=json.dumps(labels),
            headers={'Content-Type': 'application/json'})

        body = "Labels have been sent successfully"

    return {
        "body": json.dumps(body)
    }


def callback(event, context):
    # check ['eventName'] == 'MODIFY'
    try:
        for record in event['Records']:
            if record['eventName'] == 'MODIFY':
                # get callback_url and labels
                callback_url, labels = get_data(record)

                # check if callback is available
                if callback_url:
                    sendLabelsresponsebody = send_labels(callback_url, labels)
                else:
                    sendLabelsresponsebody = "No callback_url provided"

            else:
                pass

        response = {
            "statusCode": 200,
            "body": json.dumps(sendLabelsresponsebody)
        }

    except Exception as e:
        responsebody = str(e)
        response = {
            "statusCode": 500,
            "body": json.dumps(responsebody)
        }

    return response
