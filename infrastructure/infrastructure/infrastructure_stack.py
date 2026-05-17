
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)

from constructs import Construct


class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # =========================================================
        # S3 Bucket
        # =========================================================

        bucket = s3.Bucket(
            self,
            "ImagesBucket",
            bucket_name="images-bucket"
        )

        # =========================================================
        # DynamoDB Table
        # =========================================================

        table = dynamodb.Table(
            self,
            "ImagesMetadataTable",
            table_name="images_metadata",
            partition_key=dynamodb.Attribute(
                name="image_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        # =========================================================
        # Lambda Functions
        # =========================================================

        upload_lambda = _lambda.Function(
            self,
            "UploadImageLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../src/upload_image")
        )

        list_lambda = _lambda.Function(
            self,
            "ListImagesLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../src/list_images")
        )

        get_lambda = _lambda.Function(
            self,
            "GetImageLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../src/get_image")
        )

        delete_lambda = _lambda.Function(
            self,
            "DeleteImageLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("../src/delete_image")
        )

        # =========================================================
        # Permissions
        # =========================================================

        bucket.grant_read_write(upload_lambda)
        bucket.grant_read_write(get_lambda)
        bucket.grant_read_write(delete_lambda)

        table.grant_read_write_data(upload_lambda)
        table.grant_read_data(list_lambda)
        table.grant_read_data(get_lambda)
        table.grant_read_write_data(delete_lambda)

        # =========================================================
        # API Gateway
        # =========================================================

        api = apigateway.RestApi(
            self,
            "ImagesApi",
            rest_api_name="images-api"
        )

        images = api.root.add_resource("images")

        image_id = images.add_resource("{id}")

        # =========================================================
        # API Methods
        # =========================================================

        images.add_method(
            "POST",
            apigateway.LambdaIntegration(upload_lambda)
        )

        images.add_method(
            "GET",
            apigateway.LambdaIntegration(list_lambda)
        )

        image_id.add_method(
            "GET",
            apigateway.LambdaIntegration(get_lambda)
        )

        image_id.add_method(
            "DELETE",
            apigateway.LambdaIntegration(delete_lambda)
        )