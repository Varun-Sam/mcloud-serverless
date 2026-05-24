import json
import sys
from unittest.mock import patch

sys.path.append("src/upload_image")

from handler import lambda_handler


@patch("handler.table")
@patch("handler.s3")
def test_upload_image_success(mock_s3, mock_table):

    event = {
        "body": json.dumps({
            "image_name": "sample.jpg",
            "image_content": "aGVsbG8=",
            "user_id": "user123",
            "title": "Sample",
            "tags": ["plain"]
        })
    }

    response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "Image uploaded successfully"
    assert "image_id" in body