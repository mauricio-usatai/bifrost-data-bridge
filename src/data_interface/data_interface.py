from typing import Optional
from abc import ABC, abstractmethod

from pandas import DataFrame


class DataInterface(ABC):
    """
    A commom data interface
    """

    @abstractmethod
    def put(self, data: DataFrame, **kwargs) -> None:
        """
        Puts data into the destination interface

        Args:
            data (DataFrame): The data to be stored
            kwargs: Data destination related attributes
        """
        raise NotImplementedError

    def get(self, **kwargs) -> Optional[DataFrame]:
        """
        Get data from a data source and return it as a DataFrame

        Args:
            kwargs: Data sourcew related attributes
        """
        raise NotImplementedError
