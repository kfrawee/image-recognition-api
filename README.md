# Image Recognition API ⚡🔎 
> A simple API for the recognition of images using AWS Rekognition on the back-end. Using the Serverless framework for describing infrastructure. 

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Awesome](https://awesome.re/badge.svg)](https://github.com/kfrawee/)

---

## Overview:
A simple API for the recognition of images using AWS Rekognition on the back-end. Users for this API are other developers. The API stores an image, does image recognition on it and returns results to the user in two ways, with a `callback` and a `GET` endpoint.

<br>
<p align="center">
<img src="images/readme/diagram.png" title="Architecture diagram" alt="Architecture diagram" width=100%><br>
<b>Architecture diagram</b>
</p>

---

## Workflow:
- Send `POST` request with *optionally* provided `callback_url` in request body. Response return unique `upload_url`.
- The user uploads a picture to the `upload_url`.
Once the image has been `PUT` to the `upload_url`, it gets stored in an **S3 bucket**. Once successfully stored, this will trigger AWS Rekognition for the image recognition process.
- Once the image recognition process finishes, the user receives a callback under the `callback_url` they indicated in the first step.
- User can also retrieve the results from a `GET` endpoint.

## Usage

- Clone the repository:
  ``` sh
  $ git clone https://github.com/kfrawee/image-recognition-api.git
  ```

- Navigate to the directory:

  ```sh
  $ cd .\image-recognition-api\
  ```
> This project uses [`serverless`](https://www.serverless.com/) framework ⚡. So, make sure you get that first and give the necessary permissions to `serverless cli`. Follow [this page](https://www.serverless.com/framework/docs/getting-started/) for getting started. <br>

- Deploy the stack:
  ```yml
  $ serverless deploy
  ```
- After deployment is successful, you can check the setup details using:
  ```yml
  $ serverless info

  Service Information
  service: image-rec-api
  stage: dev
  region: us-east-1
  stack: image-rec-api-dev
  resources: 36
  api keys:
    None
  endpoints:
    POST - https://jok587gh7j.execute-api.us-east-1.amazonaws.com/dev/images/upload
    GET - https://jok587gh7j.execute-api.us-east-1.amazonaws.com/dev/images/labels/{blob_id}
  functions:
    upload: image-rec-api-dev-upload
    label_on_upload: image-rec-api-dev-label_on_upload
    callback: image-rec-api-dev-callback
    get_labels: image-rec-api-dev-get_labels
  layers:
    None
  ```

<!-- https://reqbin.com/req/c-1n4ljxb9/curl-get-request-example -->
- Now, test the API by uploading an image on S3.<br> 
  >*Using `curl` to send requests or you can use [Postman](https://www.postman.com/) tool or [REQBIN](reqbin.com) to send HTTP requests:*
  
  - Send a `POST` request to the POST endpoint:
    - *Provide your `callback` url in request body. You can use [webhook.site](https://webhook.site/) to get free webhook url.*<br><br>
    
    ```sh
    curl -X POST https://jok587gh7j.execute-api.us-east-1.amazonaws.com/dev/images/upload
    -H 'Content-Type: application/json'
    -d '{"callback_url":"https://webhook.site/53919b2d-7d8d-4ad8-ba6a-5929d38ae711"}'
    ```
    <br>

    You will get a response with a `blob_id`, `upload_url` and `callback_url` *(if provided)*: 
    ```json
    {
        "blob_id": "20211102064424400413",
        "upload_url": "https://s3.amazonaws.com/image-rec-api-bucket-dev/20211102064424400413.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQQUG4IQDLZFZLBWE%2F20211102%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211102T064424Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEH8aCXVzLWVhc3QtMSJHMEUCIEMUsf%2Bt4IBOsM39Mztt%2F3glVe%2FaWMF5Y9swkVF6wRiBAiEAiR4M88dVX1PEAf18LWfJcGb0AtgHS5Q9F64GEMVi3TQqnQIIKBAAGgwwMzU3MTYzNTA5ODIiDALq9j%2Fa765eP6eFfCr6AYIoEvGRrwl7kRnBUDn%2Bxll4xsEiDw2ACQBQz7XOu%2BaCOZhUeDUGwiwR%2FJcg62WAPlArUNMGpwaP9fMk2dphnDog5N1e%2BYRIGONWD1Iw%2BKhcrWtjBXWxg2oB42rWaLOKGpUllwgFS4SJTApSVR6plgX9ryxKJI2dNcie5G9bbwRFA3DOS8Y%2BgC3LUhU2YMju148oBc9qyKcAbh5MXKzWHLE%2FgUR2age76jgJiAqqbkNKj6PPYk9L80kgzc3mOLu0W7f7HWAZVHSQd7CRBIF3bhGE0%2Fe%2F0YE9B411AybmflXE5SnQtK3RtqvVTLQnXFP0OSca1IayjHm4uVswq7yDjAY6mgFhZJyYpKRVYU%2FpxRQ1ickfPlwOAqajJcDEe3ya84JTqoVdBadWmvr2d5KuTFZTg8lG8z%2B35cE7Oe9IBBU32y%2BDaXXiXbrgh9H7B5Q57dBx9%2Fusps7C7YV%2Bm6F4QNp64Gj06oEs0Y4L6wP50hlXWyvtoZRnS1F2d%2BevPg%2BGW%2BHytq%2BmQIpoAsx5PTxiPYe%2BS4NbzpGZc%2Fu45v%2FI&X-Amz-Signature=8b576edcd162789178d6421d5d5b9e36c8f0c0b242b57b079a86ea941f5b07ca",
        "callback_url": "https://webhook.site/53919b2d-7d8d-4ad8-ba6a-5929d38ae711"
    }
    ```
  - Use `upload_url` to upload the image to **S3**:
    ```bash
    $ curl "upload_url" \
    --upload-file "path/to/image"
    ```
    ```bash
    $ curl "https://s3.amazonaws.com/image-rec-api-bucket-dev/20211102064424400413.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQQUG4IQDLZFZLBWE%2F20211102%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211102T064424Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEH8aCXVzLWVhc3QtMSJHMEUCIEMUsf%2Bt4IBOsM39Mztt%2F3glVe%2FaWMF5Y9swkVF6wRiBAiEAiR4M88dVX1PEAf18LWfJcGb0AtgHS5Q9F64GEMVi3TQqnQIIKBAAGgwwMzU3MTYzNTA5ODIiDALq9j%2Fa765eP6eFfCr6AYIoEvGRrwl7kRnBUDn%2Bxll4xsEiDw2ACQBQz7XOu%2BaCOZhUeDUGwiwR%2FJcg62WAPlArUNMGpwaP9fMk2dphnDog5N1e%2BYRIGONWD1Iw%2BKhcrWtjBXWxg2oB42rWaLOKGpUllwgFS4SJTApSVR6plgX9ryxKJI2dNcie5G9bbwRFA3DOS8Y%2BgC3LUhU2YMju148oBc9qyKcAbh5MXKzWHLE%2FgUR2age76jgJiAqqbkNKj6PPYk9L80kgzc3mOLu0W7f7HWAZVHSQd7CRBIF3bhGE0%2Fe%2F0YE9B411AybmflXE5SnQtK3RtqvVTLQnXFP0OSca1IayjHm4uVswq7yDjAY6mgFhZJyYpKRVYU%2FpxRQ1ickfPlwOAqajJcDEe3ya84JTqoVdBadWmvr2d5KuTFZTg8lG8z%2B35cE7Oe9IBBU32y%2BDaXXiXbrgh9H7B5Q57dBx9%2Fusps7C7YV%2Bm6F4QNp64Gj06oEs0Y4L6wP50hlXWyvtoZRnS1F2d%2BevPg%2BGW%2BHytq%2BmQIpoAsx5PTxiPYe%2BS4NbzpGZc%2Fu45v%2FI&X-Amz-Signature=8b576edcd162789178d6421d5d5b9e36c8f0c0b242b57b079a86ea941f5b07ca" \
    > --upload-file test_cases/test1.jpeg
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                   Dload  Upload   Total   Spent    Left  Speed
    100  113k    0     0  100  113k      0  67758  0:00:01  0:00:01 --:--:-- 67779
    ```

  - Now, the image have been uploaded successfully to **S3**.
    <p align="center">
    <img src="images/test_cases/test1.jpeg" title="Test Image" alt="Test Image" width=80%><br>
    <b>Test image: test1.jpeg</b>
    </p>

  - Once uploaded; the image will get labeled and the results will be stored for later queries. Also, the labels will be sent to your `callback_url` *(if provided)*:

  <p align="center">
  <img src="images/readme/webhook_labels.png" title="callback results" alt="callback results" width=90%><br>
  <b>Labeling results from callback url</b>
  </p>     
    
    - You can also query the endpoint using `blob_id` to get the labels associated to the image; send a request the `GET` endpoint:
    
      ```bash
      curl https://jok587gh7j.execute-api.us-east-1.amazonaws.com/dev/images/labels/20211102064424400413
      -H "Accept: application/json" 
      ```
      - Response:
        
        ```json
        {
        "statusCode": 200,
        "body": ["car", "sports car", "coupe", "tire", "wheel"]
        }
        ```

---
## Clean
To remove Serverless service and all resources:

```yml
$ serverless remove

Serverless: Stack delete finished...
```
