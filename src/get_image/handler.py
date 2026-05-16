import json
import boto3
import base64


s3 = boto3.client(
    "s3",
    endpoint_url="http://host.docker.internal:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("images_metadata")

BUCKET_NAME = "images-bucket"


def lambda_handler(event, context):

    try:

        image_id = event["pathParameters"]["id"]

        # Get metadata
        response = table.get_item(
            Key={
                "image_id": image_id
            }
        )

        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "message": "Image not found"
                })
            }

        s3_key = item["s3_key"]

        # Fetch image from S3
        s3_response = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )

        image_bytes = s3_response["Body"].read()

        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "image_id": image_id,
                "title": item["title"],
                "user_id": item["user_id"],
                "tags": item["tags"],
                "image_content": image_base64
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }