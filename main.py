from datetime import datetime

import pytz

from src.data_interface import (
    DynamoDB,
    S3ObjectStorage,
)
from src.logger import logging
from settings import Settings


settings = Settings()
logger = logging.getLogger(settings.LOGGER)


def main():
    # Read from S3
    score_data_df = S3ObjectStorage().get(
        bucket=settings.BUCKET,
        path=f"heuristic-scores/{settings.RUN_ID}-mean-score.csv",
    )
    if score_data_df is None:
        return

    # Add time
    date = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    score_data_df["date"] = [date]

    # Save on DynamoDB
    DynamoDB().put(
        data=score_data_df,
        table=settings.DYNAMODB_TABLE,
    )


if __name__ == "__main__":
    main()
