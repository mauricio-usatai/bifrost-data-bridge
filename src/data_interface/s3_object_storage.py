from typing import Optional

from io import BytesIO, StringIO

import boto3
import pandas as pd
from pandas import DataFrame
from botocore.exceptions import ClientError

from settings import Settings

from ..logger import logging
from .data_interface import DataInterface


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


class S3ObjectStorage(DataInterface):
    def __init__(self):
        if settings.DEPLOY == "local":
            self._s3 = boto3.resource(
                "s3",
                endpoint_url="http://minio:9000",
                aws_access_key_id="miniodev",
                aws_secret_access_key="miniodev",
                verify=False,
            )
        else:
            self._s3 = boto3.resource(
                "s3",
                region_name=settings.AWS_REGION,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )

    def put(self, data: DataFrame, path: str, bucket: str) -> None:
        """
        Put data into S3 storage

        Args:
            data (DataFrame): Data to be saved
            path (str): The path inside the bucket
            bucket (str): bucket name
        """
        obj = self._s3.Object(bucket, path)
        try:
            # Convert to bytes
            body = StringIO()
            data.to_csv(body)
            body.seek(0)
            body = BytesIO(body.read().encode("utf-8"))
            obj.put(Body=body)
        except ClientError as err:
            logger.error(err)

    def get(self, path: str, bucket: str) -> Optional[DataFrame]:
        """
        Get an object from S3 storage

        Args:
            path (str): The path inside the bucket
            bucket (str): bucket name

        Returns:
            Optional[DataFrame]: The retrieved csv file as a DataFrame
        """
        obj = self._s3.Object(bucket, path)
        try:
            response = obj.get()
            byte_stream = response["Body"]
        except (ClientError, KeyError) as err:
            logger.error(err)
            return None

        stream = StringIO(byte_stream.read().decode("utf-8"))
        return pd.read_csv(stream, index_col=[0])
