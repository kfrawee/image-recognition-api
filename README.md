```sh
aws dynamodb create-table --cli-input-json file://setup/create-master-blobs-labels-table.json --region us-east-1
aws s3 mb s3://image-rec-api-v100 --region=us-east-1
```