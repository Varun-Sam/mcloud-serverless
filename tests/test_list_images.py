import json
import sys
from unittest.mock import patch

sys.path.append("src/list_images")

from handler import lambda_handler


@patch("handler.table")
def test_list_images_success(mock_table):

    mock_table.scan.return_value = {
        "Items": [
            {
                "image_id": "1234",
                "title": "Space",
                "user_id": "user1234"
            }
        ]
    }

    event = {
        "queryStringParameters": None
    }

    response = lambda_handler(event, None)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert len(body) == 1
    assert body[0]["title"] == "Space"