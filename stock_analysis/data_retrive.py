from dataclasses import dataclass
import datetime

import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr
from stock_analysis.utils.logger import logger

yf.pdr_override()

@dataclass
class DataRetrive:
    """
    Import Stock data using Yahoo Finance Api
    """

    @classmethod
    def single_company_specific(
        cls,
        company_name: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        save: bool = False,
        export_path: str = None,
    ) -> pd.DataFrame:
        """Retrive single company date from given start date and end

        Args:
            company_name (str): name of desired company
            start_date (datetime.datetime): Start date
            end_date (datetime.datetime): End date
            save (bool, optional): save to disk. Defaults to False.
            export_path (str, optional): disk path where to save. Defaults to None.

        Returns:
            pd.DataFrame: Data from Yahoo finance
        """
        data = pdr.get_data_yahoo(
            company_name, start=start_date, end=end_date, progress=False
        )

        if save is True:
            data.to_csv(f"{export_path}/{company_name}.csv")

        return data

    @classmethod
    def single_company_complete(
        cls, company_name: str, save: bool = False, export_path: str = None
    ) -> pd.DataFrame:
        """Retrive complete data right from its IPO till today

        Args:
            company_name (str): Symbol of company
            save (bool, optional): save to disk. Defaults to False.
            export_path (str, optional): path where to save (to be used only if save is True). Defaults to None.

        Returns:
            pd.DataFrame: Data from Yahoo finance
        """
        data = pdr.get_data_yahoo(company_name, progress=False)

        if save is True:
            data.to_csv(f"{export_path}/{company_name}.csv")

        return data

    @classmethod
    def single_company_quote(cls, company_name: str) -> pd.DataFrame:
        return pdr.get_quote_yahoo(company_name)
