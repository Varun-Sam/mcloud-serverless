import json
import sys
from unittest.mock import patch, MagicMock

sys.path.append("src/get_image")

from handler import lambda_handler


@patch("handler.s3")
@patch("handler.table")
def test_get_image_success(mock_table, mock_s3):

    mock_table.get_item.return_value = {
        "Item": {
            "image_id": "123",
            "title": "Sample",
            "user_id": "user123",
            "tags": ["plain"],
            "s3_key": "images/sample.jpg"
        }
    }

    mock_body = MagicMock()
    mock_body.read.return_value = b"hello"

    mock_s3.get_object.return_value = {
        "Body": mock_body
    }

    event = {
        "pathParameters": {
            "id": "123"
        }
    }

    response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["image_id"] == "123"
    assert body["title"] == "Sample"


@patch("handler.table")
def test_get_image_not_found(mock_table):

    mock_table.get_item.return_value = {}

    event = {
        "pathParameters": {
            "id": "999"
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 404