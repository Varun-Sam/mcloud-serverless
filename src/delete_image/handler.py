import json
import boto3


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

        # Fetch metadata first
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

        # Delete image from S3
        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )

        # Delete metadata from DynamoDB
        table.delete_item(
            Key={
                "image_id": image_id
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Image deleted successfully",
                "image_id": image_id
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }