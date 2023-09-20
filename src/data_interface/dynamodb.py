import boto3
from pandas import DataFrame

from botocore.config import Config
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
)

from settings import Settings
from .data_interface import DataInterface
from ..logger import logging


settings = Settings()
config = Config(
    connect_timeout=settings.DYNAMO_CONNECT_TIMEOUT,
    read_timeout=settings.DYNAMO_READ_TIMEOUT,
    retries={"max_attempts": settings.DYNAMO_MAX_RETRIES},
)
logger = logging.getLogger(settings.LOGGER)


class DynamoDB(DataInterface):
    def __init__(self):
        if settings.DEPLOY == "local":
            self.client = boto3.client(
                "dynamodb",
                config=config,
                endpoint_url="http://dynamodb:8000",
                region_name=settings.AWS_REGION,
                aws_access_key_id="dummy-key-id",
                aws_secret_access_key="dummy-key",
            )
        else:
            self.client = boto3.client(
                "dynamodb",
                config=config,
                region_name=settings.AWS_REGION,
            )

    def put(self, data: DataFrame, table: str) -> None:
        """
        Put data into a DynamoDB table

        Args:
            data (DataFrame): The data to be saved
            table (str): Table name
        """
        for index in range(len(data)):
            # Build DynamoDB insert statement
            item = {
                key: {"S": str(value)}
                for key, value in data.iloc[index].to_dict().items()
            }
            try:
                self.client.put_item(
                    TableName=table,
                    Item=item,
                )
            except (ClientError, EndpointConnectionError) as err:
                logger.error(err)
                raise
