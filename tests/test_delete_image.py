import json
import sys
from unittest.mock import patch

sys.path.append("src/delete_image")

from handler import lambda_handler


@patch("handler.s3")
@patch("handler.table")
def test_delete_image_success(mock_table, mock_s3):

    mock_table.get_item.return_value = {
        "Item": {
            "image_id": "123",
            "s3_key": "images/sample.jpg"
        }
    }

    event = {
        "pathParameters": {
            "id": "123"
        }
    }

    response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "Image deleted successfully"


@patch("handler.table")
def test_delete_image_not_found(mock_table):

    mock_table.get_item.return_value = {}

    event = {
        "pathParameters": {
            "id": "999"
        }
    }

    response = lambda_handler(event, None)

    assert response["statusCode"] == 404