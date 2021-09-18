import datetime

import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()


class DataRetrive:
    """
    Import Stock data using Yahoo Finance Api
    """

    # def __init__(self, path: str):
    #     """
    #     Update or create new csv using Yahoo Finance Api

    #     Parameters
    #     ----------
    #     path : str
    #         path of older csv to be updated or to save new csv
    #     """
    #     self.path = path
    @classmethod
    def single_company_specific(
        cls,
        company_name: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        save: bool = False,
        export_path: str = None,
    ) -> pd.DataFrame:
        """
        Retrive single company date from given start date and end

        Parameters
        ----------
        company_name : str
            name of desired company
        start_date : Tuple[year, month, day]
            Start date
        end_date : Tuple[year, month, day]
            End date

        Returns
        -------
        pd.DataFrame
            Data from Yahoo finance

        Raises
        ------
        ValueError
            [description]
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

        Parameters
        ----------
        company_name : str
            Name of company
        save : bool, optional
            save to disk, by default False
        export_path : str, optional
            path where to save (to be used only if save is True), by default None

        Returns
        -------
        pd.DataFrame
            Data from Yahoo finance
        """

        data = pdr.get_data_yahoo(company_name, progress=False)

        if save is True:
            data.to_csv(f"{export_path}/{company_name}.csv")

        return data

    @classmethod
    def single_company_quote(cls, company_name: str) -> pd.DataFrame:
        return pdr.get_quote_yahoo(company_name)
