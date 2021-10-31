# Image Recognition API ⚡🔎 
> A simple API for the recognition of images using AWS Rekognition on the back-end. Using the Serverless framework for describing infrastructure. 

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Awesome](https://awesome.re/badge.svg)](https://github.com/kfrawee/)

---

## Overview:
Users for this API are other developers. The API stores an image, does image recognition on it and returns results to the user with a GET endpoint. 

<p align="center">
<img src="images/readme/diagram.png" title="Architecture diagram" alt="Architecture diagram" width=100%>
</p>

---

## Workflow:
- Send a `POST` request. Response return unique `upload_url`.
- The user uploads a picture to the `upload_url.`
- Once the image has been `PUT` to the `upload_url`, it gets stored in an **S3 bucket**. Once successfully stored, this will trigger the image recognition process.
- Using **AWS Rekognition** for image recognition process. 
- Once the image recognition process finishes, the user can retrieve the results from a `GET` endpoint.

### TODO:
- The API stores an image, does image recognition on it and returns results to the user in two ways, with a **callback** and a GET endpoint.
- Send request with **optionally provided ``callback_url``** in request body. Response return unique upload_url.
- Once the image recognition process finishes, the user receives a callback under the **``callback_url``** they indicated in the first step.

## Usage
This project uses [`serverless`](https://www.serverless.com/) framework ⚡. So, make sure you get that first and give the necessary permissions to `serverless cli`. Follow [this page](https://www.serverless.com/framework/docs/getting-started/) for getting started. <br>

```yml
$ serverless deploy
```
After deployment is successful, you can check the setup details using:
```yml
$ serverless info

Service Information
service: image-rec-api
stage: dev
region: us-east-1
stack: image-rec-api-dev
resources: 32
api keys:
  None
endpoints:
  POST - https://t4wuc5yjab.execute-api.us-east-1.amazonaws.com/dev/blobs/upload
  GET - https://t4wuc5yjab.execute-api.us-east-1.amazonaws.com/dev/blobs/get/{blob_id}
functions:
  upload: image-rec-api-dev-upload
  label_on_upload: image-rec-api-dev-label_on_upload
  get_labels: image-rec-api-dev-get_labels
layers:
  None
```
Now, test the services by uploading an image on S3.<br> 
You can use [Postman](https://www.postman.com/) tool or [REQBIN](reqbin.com) to test the API and send HTTP requests:
- Send a `POST` request to `https://t4wuc5yjab.execute-api.us-east-1.amazonaws.com/dev/blobs/upload`
<br>You will get a response with a `upload_url` and `blob_id` to use it later for getting image labels:

<p align="center">
<img src="images/readme/post.png" title="POST Request" alt="POST Request" width=1000%>
</p>

```json
{
    "upload_url": "https://s3.amazonaws.com/image-rec-api-bucket-dev/20211031155847779721.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQQUG4IQDBWONVQNN%2F20211031%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211031T155847Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFgaCXVzLWVhc3QtMSJHMEUCIQC7mAnPZUPw65jrZKN85T3FgRpemwJZtAdfJbbCnA1u4AIgcKBS3pkzpqU07lPg6XCXEO8xxiMOZ%2F1bWf%2FlwpeI7wAqpgII8f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwMzU3MTYzNTA5ODIiDPfmKXl3ZaEgWHdDpSr6Ad%2Bf8ifnCibQsixEhBlOGKwVDA%2FL7HrJ%2F%2BiWaUVMwmA8k7wgV3l4qD0zvXTj77har6JoiTID43PbnikFK11NDIN2gwm7bSQM30Iqj2Y%2BlATFM17lJQAMKQ0sV8yzuvSnCjwr7gKRtigjgZZjBWqXRWaxg94SgozmrAN27GSUkdGt%2BFZ1z6QKDtbmkMLE2JHOx2Df4GEosjSyIG%2FV3T1GbxiqOqF3%2Be6Y4tTZRrXuLYO3hZeR26empATL9Tx5CAPv8EJGJ6yR6tnKvSEbwsK%2FMiUhfUmfkhI345G961ktJ%2FHTEJeaZbI6eI6M7y2Emf9UEkGAbwf%2Fbar0xJYwt%2Fr6iwY6mgE%2BkK3fFAghCRrej%2BFYuGrvUlb%2Bket5XRDMF0K68S1zDdBP0lgGWiuhEz04hY5ty5IsNZLnJMzV%2FRlseozYDnwMLt3SjyfJGKZdS%2BGOcjvE1hS2xRs94%2BQKuFjqniT%2FEaEYYUFZ%2BM5Gl15kiasyoy%2Bb50paaO6odf8%2Bs1jxTcPELPZCHknVFAu8pPz0ItZp4w8kjXrYCfjLXgRT&X-Amz-Signature=0c525f950302867763c586cca459f4856a2e4e56b1c109b2f6d2728439b8d6a2",
    "blob_id": "20211031155847779721"
}
```
- Use `upload_url` to upload the image to **S3**:
```bash
$ curl "upload_url" --upload-file "path/to/image"
```
```bash
$ curl "https://s3.amazonaws.com/image-rec-api-bucket-dev/20211031155847779721.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQQUG4IQDBWONVQNN%2F20211031%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211031T155847Z&X-Amz-Expires=600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFgaCXVzLWVhc3QtMSJHMEUCIQC7mAnPZUPw65jrZKN85T3FgRpemwJZtAdfJbbCnA1u4AIgcKBS3pkzpqU07lPg6XCXEO8xxiMOZ%2F1bWf%2FlwpeI7wAqpgII8f%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgwwMzU3MTYzNTA5ODIiDPfmKXl3ZaEgWHdDpSr6Ad%2Bf8ifnCibQsixEhBlOGKwVDA%2FL7HrJ%2F%2BiWaUVMwmA8k7wgV3l4qD0zvXTj77har6JoiTID43PbnikFK11NDIN2gwm7bSQM30Iqj2Y%2BlATFM17lJQAMKQ0sV8yzuvSnCjwr7gKRtigjgZZjBWqXRWaxg94SgozmrAN27GSUkdGt%2BFZ1z6QKDtbmkMLE2JHOx2Df4GEosjSyIG%2FV3T1GbxiqOqF3%2Be6Y4tTZRrXuLYO3hZeR26empATL9Tx5CAPv8EJGJ6yR6tnKvSEbwsK%2FMiUhfUmfkhI345G961ktJ%2FHTEJeaZbI6eI6M7y2Emf9UEkGAbwf%2Fbar0xJYwt%2Fr6iwY6mgE%2BkK3fFAghCRrej%2BFYuGrvUlb%2Bket5XRDMF0K68S1zDdBP0lgGWiuhEz04hY5ty5IsNZLnJMzV%2FRlseozYDnwMLt3SjyfJGKZdS%2BGOcjvE1hS2xRs94%2BQKuFjqniT%2FEaEYYUFZ%2BM5Gl15kiasyoy%2Bb50paaO6odf8%2Bs1jxTcPELPZCHknVFAu8pPz0ItZp4w8kjXrYCfjLXgRT&X-Amz-Signature=0c525f950302867763c586cca459f4856a2e4e56b1c109b2f6d2728439b8d6a2" \
> -- upload-file images/test_cases/test1.jpeg

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  113k    0     0  100  113k      0  82121  0:00:01  0:00:01 --:--:-- 82194
```

- Now, you have successfully uploaded the image `test1.jpeg` to **S3**.
<p align="center">
<img src="images/test_cases/test1.jpeg" title="Test Image" alt="Test Image" width=80%>
</p>

- This would trigger a lambda fuction to label the image and store the details in DyanamoDB. 
- You can later query the endpoint using `blob_id` for getting labels associated to the image by sending a `GET` request to `https://t4wuc5yjab.execute-api.us-east-1.amazonaws.com/dev/blobs/get/{blob_id}`:

<p align="center">
<img src="images/readme/get.png" title="GET Request" alt="Get Request" width=80%>
</p>

*Response:*
```json
{
    "blob_id": "20211031155847779721",
    "labels": [
        "car",
        "sports car",
        "coupe",
        "tire",
        "wheel"
    ],
    "created_on": "2021-10-31 16:02:42.160306"
}
```

## Clean
To remove Serverless service and all resources:

```yml
$ serverless remove

Serverless: Stack delete finished...
```

---

