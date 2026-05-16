import json
import uuid
import boto3
import base64
from datetime import datetime

# S3 Client
s3 = boto3.client(
    "s3",
    endpoint_url="http://host.docker.internal:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

# DynamoDB Resource
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

        # Parse request body
        body = json.loads(event["body"])

        image_name = body["image_name"]
        image_content = body["image_content"]

        user_id = body["user_id"]
        title = body["title"]
        tags = body["tags"]

        # Generate unique image ID
        image_id = str(uuid.uuid4())

        # Decode base64 image
        image_bytes = base64.b64decode(image_content)

        # S3 object key
        s3_key = f"images/{image_id}_{image_name}"

        # Upload image to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=image_bytes
        )

        # Store metadata in DynamoDB
        table.put_item(
            Item={
                "image_id": image_id,
                "user_id": user_id,
                "title": title,
                "tags": tags,
                "s3_key": s3_key,
                "created_at": datetime.utcnow().isoformat()
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Image uploaded successfully",
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