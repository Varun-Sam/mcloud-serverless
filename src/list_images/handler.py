import json
import boto3


dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://host.docker.internal:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

table = dynamodb.Table("images_metadata")


def lambda_handler(event, context):

    try:

        query_params = event.get("queryStringParameters") or {}

        user_id_filter = query_params.get("user_id")
        title_filter = query_params.get("title")

        response = table.scan()

        items = response.get("Items", [])

        # Apply filters
        filtered_items = []

        for item in items:

            if user_id_filter and item.get("user_id") != user_id_filter:
                continue

            if title_filter and title_filter.lower() not in item.get("title", "").lower():
                continue

            filtered_items.append(item)

        return {
            "statusCode": 200,
            "body": json.dumps(filtered_items)
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }