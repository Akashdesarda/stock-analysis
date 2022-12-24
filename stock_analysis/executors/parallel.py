"""This packs all the individual function with the scope of running for just unit input data.
"""
import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import dateutil
import pandas as pd

# from stock_analysis.data_retrieve import DataRetrieve
from stock_analysis.utils.formula_helpers import (
    annualized_rate_of_return,
    exponential_moving_average,
    percentage_diff,
    simple_moving_average,
    turnover,
)
from stock_analysis.utils.helpers import get_appropriate_date_momentum
from stock_analysis.utils.logger import set_logger
import yfinance as yf
from pandas_datareader import data as pdr

yf.pdr_override()

now_string = datetime.datetime.now().strftime("%d-%m-%Y")
logger = set_logger()
pd.options.display.float_format = "{:,.2f}".format


class DataRetrieve:
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


@dataclass
class UnitExecutor:
    """UnitExecutor class packs all the different strategies, indicators, etc. which
    can be used to execute on unit (single) data. This can be inhereted into other
    class and consumed into multiprocessing iterator used for batch of data.
    """

    # TODO: Add all parallel executor function here
    def unit_vol_indicator_n_days(self, company: str = None, duration: int = 90):
        end = datetime.datetime.now()
        start = end - dateutil.relativedelta.relativedelta(days=duration)
        logger.info(f"Retriving data for {company}")
        company_df = DataRetrieve.single_company_specific(
            company_name=f"{company}.NS", start_date=start, end_date=end
        )

        buy_stock = company_df.iloc[-1].Volume > company_df["Volume"].mean()
        print(f"Problem with {company}, moving on")
        return {
            "company": company,
            "current date": company_df.index[-1].strftime("%d-%m-%Y"),
            "start date": company_df.index[0].strftime("%d-%m-%Y"),
            "current volume": company_df.iloc[-1].Volume,
            "mean volume": company_df["Volume"].mean(),
            "close price": company_df.iloc[-1].Close,
            "action": buy_stock,
        }

    def unit_ema_absolute(
        self,
        company: str,
        cutoff_date: Union[str, datetime.datetime] = "today",
        period: int = 50,
        cutoff: int = 5,
        verbosity: int = 1,
    ) -> Dict:

        logger.info(f"Retrieving data for {company}")
        company_df = DataRetrieve.single_company_complete(
            company_name=f"{company}.NS"
        )  # NS = Nifty
        # need to drop rows which have Null values
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)
        action = "Invalid"  # deafult value, if not used then error occurs of `UnboundLocalError`
        try:
            closing_date = company_df.index[-1].strftime("%d-%m-%Y")
            closing_price = company_df["Close"][-1]
            ema = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=period,
                verbosity=verbosity,
            )
            # NOTE - turnover needs to be relative to 1 cr so dividing it by 1 cr
            turnover_value = turnover(company_df["Volume"], ema) / 10000000
            buy = ema + (ema * (cutoff / 100))
            sell = ema - (ema * (cutoff / 100))
            if (buy < company_df["Close"][-1]) and (turnover_value > 1):
                action = "buy"
            elif (sell > company_df["Close"][-1]) and (turnover_value > 1):
                action = "sell"
            elif (sell < company_df["Close"][-1] < buy) and (turnover_value > 1):
                action = "no action"
            long_name = self.unit_quote_retrive(company)["longName"][0]

        except (KeyError, IndexError, ValueError, TypeError, ZeroDivisionError):
            logger.warning(
                f"{company}'s record are less than minimum required or delisted or incorrect"
            )
            (
                company,
                long_name,
                ema,
                closing_date,
                closing_price,
                turnover_value,
                buy,
                sell,
                action,
            ) = (
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
            )

        return {
            "symbol": company,
            "company": long_name,
            f"price ({closing_date})": closing_price,
            "ema": ema,
            "ideal buy": buy,
            "ideal sell": sell,
            "turnover in cr.": turnover_value,
            "action": action,
        }

    def unit_ema_indicator(
        self,
        company: str,
        ema_canditate: Tuple[int, int] = (50, 200),
        cutoff_date: Union[str, datetime.datetime] = "today",
        verbosity: int = 1,
    ) -> Dict:
        logger.info(f"Retriving data for {company}")
        company_df = DataRetrieve.single_company_complete(
            company_name=f"{company}.NS"
        )  # NS = Nifty
        if cutoff_date == "today":
            ema_date = now_string
        else:
            ema_date = cutoff_date.strftime("%d-%m-%Y")

        # need to drop rows which have Null values
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)

        try:
            closing_date = company_df.index[-1].strftime("%d-%m-%Y")
            closing_price = company_df["Close"][-1]
            long_name = self.unit_quote_retrive(company)["longName"][0]
            ema_candidate_a = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            ema_candidate_b = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[1],
                verbosity=verbosity,
            )
            # DEPRECATED - removed as part of output remodel
            # if ema_candidate_a > ema_candidate_b:
            #     action = "buy"
            # else:
            #     action = "sell"
        except (KeyError, IndexError, ValueError, TypeError):
            logger.warning(f"{company} has less record than minimum rexquired")
            ema_candidate_a, ema_candidate_b, long_name, closing_date, closing_price = (
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
            )
        return {
            "symbol": company,
            "company": long_name,
            f"price ({closing_date})": closing_price,
            f"ema{str(ema_canditate[0])} ({ema_date})": ema_candidate_a,
            f"ema{str(ema_canditate[1])} ({ema_date})": ema_candidate_b,
        }

    def unit_quote_retrive(self, company: str) -> pd.DataFrame:
        logger.info(f"Retriving Detail Quote data for {company}")
        try:
            return DataRetrieve.single_company_quote(f"{company}.NS")
        except (KeyError, IndexError, ValueError):
            logger.warning(f"Cannot retrive data for {company}")
            return "Invalid"

    def unit_ema_indicator_n3(
        self,
        company: str,
        ema_canditate: Tuple[int, int, int] = (5, 13, 26),
        cutoff_date: Union[str, datetime.datetime] = "today",
        verbosity: int = 1,
    ) -> Dict:
        logger.info(f"Retriving data for {company}")
        company_df = DataRetrieve.single_company_complete(company_name=f"{company}.NS")
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)
        try:
            ema_candidate_a = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            ema_candidate_b = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[1],
                verbosity=verbosity,
            )
            ema_candidate_c = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[2],
                verbosity=verbosity,
            )

            percentage_diff_cb = percentage_diff(
                ema_candidate_c, ema_candidate_b, return_absolute=True
            )
            percentage_diff_ca = percentage_diff(
                ema_candidate_c, ema_candidate_a, return_absolute=True
            )
            percentage_diff_ba = percentage_diff(
                ema_candidate_b, ema_candidate_a, return_absolute=True
            )

            if (
                (percentage_diff_cb < 1)
                and (percentage_diff_ca < 1)
                and (percentage_diff_ba < 1)
            ):
                action = "buy"
            else:
                action = "sell"

        except (KeyError, IndexError, ValueError, TypeError):
            logger.warning(f"{company} has less record than minimum required")

            ema_candidate_a, ema_candidate_b, ema_candidate_c, action = (
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
            )

        return {
            "symbol": company,
            "ema_date": now_string
            if cutoff_date == "today"
            else cutoff_date.strftime("%d-%m-%Y"),
            f"ema{str(ema_canditate[0])}": ema_candidate_a,
            f"ema{str(ema_canditate[1])}": ema_candidate_b,
            f"ema{str(ema_canditate[2])}": ema_candidate_c,
            # 'percentage_diffCB': percentage_diff_cb,
            # 'percentage_diffCA': percentage_diff_ca,
            # 'percentage_diffBA': percentage_diff_ba,
            "action": action,
        }

    def unit_dma_absolute(
        self,
        company: str = None,
        end_date: Union[str, datetime.datetime] = "today",
        period: int = 200,
        cutoff: int = 5,
    ) -> Dict:
        logger.info(f"Retriving data for {company}")
        if end_date == "today":
            cutoff_date = datetime.datetime.today()
        else:
            cutoff_date = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
        start_date = cutoff_date - dateutil.relativedelta.relativedelta(months=18)
        if cutoff_date == "today":
            sma_date = now_string
        else:
            sma_date = cutoff_date.strftime("%d-%m-%Y")
        try:
            company_df = DataRetrieve.single_company_specific(
                company_name=f"{company}.NS",
                start_date=start_date,
                end_date=cutoff_date,
            )
            if company_df["Close"].isnull().sum() != 0:
                logger.warning(f"{company} have some missing value, fixing it")
                company_df.dropna(inplace=True)
        except (KeyError, ValueError, IndexError):
            company_df = pd.DataFrame(
                {
                    "Open": pd.NA,
                    "High": pd.NA,
                    "Low": pd.NA,
                    "Close": pd.NA,
                    "Adj Close": pd.NA,
                    "Volume": pd.NA,
                },
                index=["Date"],
            )
        action = "Invalid"
        try:
            sma = simple_moving_average(company_df["Close"][-(period - 1) :], period)
            turnover_value = turnover(company_df["Volume"][-period:], sma) / 10000000
            buy = sma + (sma * (cutoff / 100))
            sell = sma - (sma * (cutoff / 100))
            if (buy < company_df["Close"][-1]) and (turnover_value > 1):
                action = "buy"
            elif (sell > company_df["Close"][-1]) and (turnover_value > 1):
                action = "sell"
            elif (sell < company_df["Close"][-1] < buy) and (turnover_value > 1):
                action = "no action"
            long_name = self.unit_quote_retrive(company)["longName"][0]
            closing_price = company_df["Close"][-1]
        except (KeyError, IndexError, ValueError, TypeError, ZeroDivisionError):
            logger.warning(f"{company} has less record than minimum rexquired")
            long_name, sma, closing_price, action, turnover_value, buy, sell = (
                f"{company} (Invalid name)",
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
            )
            company = f"Problem with {company}"
        return {
            "symbol": company,
            "company": long_name,
            f"price ({sma_date})": closing_price,
            "sma": sma,
            "ideal buy": buy,
            "ideal sell": sell,
            "turnover in cr.": turnover_value,
            "action": action,
        }

    def unit_momentum(self, company: str, start, end, verbosity: int = 1):

        logger.info(f"Retriving data for {company}")
        try:
            company_df = DataRetrieve.single_company_specific(
                company_name=f"{company}.NS", start_date=start, end_date=end
            )
            company_df.reset_index(inplace=True)
            long_name = self.unit_quote_retrive(company)["longName"][0]
            ar_yearly = annualized_rate_of_return(
                end_date=company_df.iloc[-1].Close,
                start_date=company_df.iloc[0].Close,
                duration=1,
            )  # (company_df.iloc[-30,0] - company_df.iloc[0,0]).days/365)
            ar_monthly = annualized_rate_of_return(
                end_date=company_df.iloc[-1].Close,
                start_date=get_appropriate_date_momentum(
                    company_df, company, verbosity=verbosity
                )[1],
                duration=(company_df.iloc[-1, 0] - company_df.iloc[-30, 0]).days / 30,
            )
            monthly_start_date = get_appropriate_date_momentum(
                company_df, company, verbosity=0
            )[0].strftime("%d-%m-%Y")
        except (IndexError, KeyError, ValueError, TypeError):
            if verbosity > 0:
                logger.debug(f"Data is not available for: {company}")
            company_df = pd.DataFrame(
                {"Date": [datetime.datetime(1000, 1, 1)] * 30, "Close": [pd.NA] * 30}
            )
            long_name, ar_yearly, ar_monthly, monthly_start_date = (
                pd.NA,
                pd.NA,
                pd.NA,
                pd.NA,
            )

        return {
            "symbol": company,
            "company": long_name,
            f"price ({company_df.iloc[0].Date.strftime('%d-%m-%Y')})": company_df.iloc[
                0
            ].Close,
            f"price ({company_df.iloc[-1].Date.strftime('%d-%m-%Y')})": company_df.iloc[
                -1
            ].Close,
            "return_yearly": ar_yearly,
            f"price ({monthly_start_date})": company_df.iloc[-30].Close,
            "return_monthly": ar_monthly,
        }

    def unit_custom_indicator(
        self, indicators: List[str], company: str
    ) -> Dict[str, Any]:
        result = {}
        result["symbol"] = company
        if "daily moving average" in indicators:
            dma_result = self.unit_dma_absolute(company=company)
            # name of `price` key will keep on chaning so need to unpack it
            _, dma_company, dma_price, dma_sma, _, _, _, dma_action = dma_result.keys()
            result["comany"] = dma_result[dma_company]
            result[dma_price] = dma_result[dma_price]
            result["dma"] = dma_result[dma_sma]
            result["dma action"] = dma_result[dma_action]
        if "exponential moving average" in indicators:
            ema_result = self.unit_ema_absolute(company=company)
            # name of `price` key will keep on chaning so need to unpack it
            _, ema_company, ema_price, ema, _, _, _, ema_action = ema_result.keys()
            result["comany"] = ema_result[ema_company]
            result[ema_price] = ema_result[ema_price]
            result["ema"] = ema_result[ema]
            result["ema action"] = ema_result[ema_action]

        return result
