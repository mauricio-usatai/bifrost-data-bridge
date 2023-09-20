import os
from uuid import uuid4
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()


class Settings(BaseSettings):
    """App config"""

    DEPLOY: str = os.environ.get("DEPLOY", "local")
    RUN_ID: str = os.environ.get("RUN_ID", str(uuid4()))

    # AWS config
    AWS_REGION: str = os.environ.get("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "dummy-key-id")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "dummy-key")

    BUCKET: str = os.environ.get("BUCKET", "dev-midas-news-scoring")
    DYNAMODB_TABLE: str = os.environ.get("DYNAMODB_TABLE", "dev-midas-news-scoring")

    # DynamoDB config
    DYNAMO_HOST: str = os.environ.get("DYNAMO_HOST", "dynamodb")
    DYNAMO_PORT: int = int(os.environ.get("DYNAMO_PORT", "8000"))

    # DynamoDB Connection params
    DYNAMO_CONNECT_TIMEOUT: int = 5
    DYNAMO_READ_TIMEOUT: int = 5
    DYNAMO_MAX_RETRIES: int = 1

    LOGGER: str = "LOGGER"
