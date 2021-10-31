# Image Recognition API ⚡🔎 
> A simple API for the recognition of images using AWS Rekognition on the back-end. Using the Serverless framework for describing infrastructure. 

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)  [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Awesome](https://awesome.re/badge.svg)](https://github.com/kfrawee/)

--- 

## Overview:
Users for this API are other developers. The API stores an image, does image recognition on it and returns results to the user with a GET endpoint. 

<p align="center">
<img src="./images/readme/diagram.png" title="Architecture diagram" alt="Architecture diagram" width=100%>
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

```sh
$ serverless deploy
```