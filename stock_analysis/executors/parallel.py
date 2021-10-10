import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import dateutil
import pandas as pd
from stock_analysis.data_retrive import DataRetrive
from stock_analysis.utils.formula_helpers import (
    annualized_rate_of_return,
    exponential_moving_average,
    percentage_diff,
    simple_moving_average,
    turnover,
)
from stock_analysis.utils.helpers import get_appropriate_date_momentum
from stock_analysis.utils.logger import logger

now_strting = datetime.datetime.now().strftime("%d-%m-%Y")
logger = logger()
pd.options.display.float_format = "{:,.2f}".format


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
        company_df = DataRetrive.single_company_specific(
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
        company: str = None,
        cutoff_date: Union[str, datetime.datetime] = "today",
        period: int = 50,
        cutoff: int = 5,
        verbosity: int = 1,
    ) -> Dict:

        logger.info(f"Retriving data for {company}")
        company_df = DataRetrive.single_company_complete(company_name=f"{company}.NS")
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)
        action = "Invalid"
        try:
            ema = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=period,
                verbosity=verbosity,
            )
            turnover_value = turnover(company_df["Volume"], ema) / 10000000
            buy = ema + (ema * (cutoff / 100))
            sell = ema - (ema * (cutoff / 100))
            if (buy < company_df["Close"][-1]) and (turnover_value > 1):
                action = "buy"
            elif (sell > company_df["Close"][-1]) and (turnover_value > 1):
                action = "sell"
            elif (sell < company_df["Close"][-1] < buy) and (turnover_value < 1):
                action = "no action"
            long_name = self.unit_quote_retrive(company)["longName"][0]
            current_price = company_df["Close"][-1]
        except (KeyError, IndexError, ValueError, TypeError, ZeroDivisionError):
            logger.warning(f"{company} has less record than minimum rexquired")
            long_name, ema, current_price, turnover_value, buy, sell, action = (
                f"{company} (Invalid name)",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
            )
            company = f"Problem with {company}"

        return {
            "company name": long_name,
            "nse symbol": company,
            "current price": current_price,
            "ema": ema,
            "ideal buy": buy,
            "ideal sell": sell,
            "turnover in cr.": turnover_value,
            "action": action,
        }

    def unit_ema_indicator(
        self,
        company: str = None,
        ema_canditate: Tuple[int, int] = (50, 200),
        cutoff_date: Union[str, datetime.datetime] = "today",
        verbosity: int = 1,
    ) -> Dict:
        logger.info(f"Retriving data for {company}")
        company_df = DataRetrive.single_company_complete(company_name=f"{company}.NS")
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)
        try:
            EMA_A = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            EMA_B = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[1],
                verbosity=verbosity,
            )
            if EMA_A > EMA_B:
                action = "buy"
            else:
                action = "sell"
        except (KeyError, IndexError, ValueError):
            logger.warning(f"{company} has less record than minimum rexquired")
            EMA_A, EMA_B, action = pd.NA, pd.NA, pd.NA
        return {
            "company": company,
            "ema_date": now_strting
            if cutoff_date == "today"
            else cutoff_date.strftime("%d-%m-%Y"),
            f"ema{str(ema_canditate[0])}": EMA_A,
            f"ema{str(ema_canditate[1])}": EMA_B,
            "action": action,
        }

    def unit_quote_retrive(self, company: str) -> pd.DataFrame:
        logger.info(f"Retriving Detail Quote data for {company}")
        try:
            return DataRetrive.single_company_quote(f"{company}.NS")
        except (KeyError, IndexError, ValueError):
            logger.warning(f"Cannot retrive data for {company}")
            return "Invalid"

    def unit_ema_indicator_n3(
        self,
        company: str,
        ema_canditate: Tuple[int, int] = (5, 13, 26),
        cutoff_date: Union[str, datetime.datetime] = "today",
        verbosity: int = 1,
    ) -> Dict:
        logger.info(f"Retriving data for {company}")
        company_df = DataRetrive.single_company_complete(company_name=f"{company}.NS")
        if company_df["Close"].isnull().sum() != 0:
            logger.warning(f"{company} have some missing value, fixing it")
            company_df.dropna(inplace=True)
        try:
            EMA_A = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            EMA_B = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[1],
                verbosity=verbosity,
            )
            EMA_C = exponential_moving_average(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[2],
                verbosity=verbosity,
            )

            percentage_diff_cb = percentage_diff(EMA_C, EMA_B, return_absolute=True)
            percentage_diff_ca = percentage_diff(EMA_C, EMA_A, return_absolute=True)
            percentage_diff_ba = percentage_diff(EMA_B, EMA_A, return_absolute=True)

            if (
                (percentage_diff_cb < 1)
                and (percentage_diff_ca < 1)
                and (percentage_diff_ba < 1)
            ):
                action = "buy"
            else:
                action = "sell"

        except (KeyError, IndexError, ValueError):
            logger.warning(f"{company} has less record than minimum required")

            EMA_A, EMA_B, EMA_C, action = pd.NA, pd.NA, pd.NA, pd.NA

        return {
            "company": company,
            "ema_date": now_strting
            if cutoff_date == "today"
            else cutoff_date.strftime("%d-%m-%Y"),
            f"ema{str(ema_canditate[0])}": EMA_A,
            f"ema{str(ema_canditate[1])}": EMA_B,
            f"ema{str(ema_canditate[2])}": EMA_C,
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
        try:
            company_df = DataRetrive.single_company_specific(
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
            elif (sell < company_df["Close"][-1] < buy) and (turnover_value < 1):
                action = "no action"
            long_name = self.unit_quote_retrive(company)["longName"][0]
            current_price = company_df["Close"][-1]
        except (KeyError, IndexError, ValueError, TypeError, ZeroDivisionError):
            logger.warning(f"{company} has less record than minimum rexquired")
            long_name, sma, current_price, action, turnover_value, buy, sell = (
                f"{company} (Invalid name)",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
                "Invalid",
            )
            company = f"Problem with {company}"
        return {
            "company name": long_name,
            "nse symbol": company,
            "sma_date": now_strting
            if cutoff_date == "today"
            else cutoff_date.strftime("%d-%m-%Y"),
            "current price": current_price,
            "sma": sma,
            "ideal buy": buy,
            "ideal sell": sell,
            "turnover in cr.": turnover_value,
            "action": action,
        }

    def unit_momentum(self, company: str, start, end, verbosity: int = 1):

        logger.info(f"Retriving data for {company}")
        try:
            company_df = DataRetrive.single_company_specific(
                company_name=f"{company}.NS", start_date=start, end_date=end
            )
            company_df.reset_index(inplace=True)
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
        except (IndexError, KeyError, ValueError):
            if verbosity > 0:
                logger.debug(f"Data is not available for: {company}")
            company_df = pd.DataFrame(
                {"Date": [datetime.datetime(1000, 1, 1)] * 30, "Close": [pd.NA] * 30}
            )
            ar_yearly, ar_monthly, monthly_start_date = pd.NA, pd.NA, pd.NA

        return {
            "company": company,
            "yearly_start_date": company_df.iloc[0].Date.strftime("%d-%m-%Y"),
            "yearly_start_date_close": company_df.iloc[0].Close,
            "yearly_end_date": company_df.iloc[-1].Date.strftime("%d-%m-%Y"),
            "yearly_end_date_close": company_df.iloc[-1].Close,
            "return_yearly": ar_yearly,
            "monthly_start_date": monthly_start_date,
            "monthly_start_date_close": company_df.iloc[-30].Close,
            "monthly_end_date": company_df.iloc[-1].Date.strftime("%d-%m-%Y"),
            "monthly_end_date_close": company_df.iloc[-1].Close,
            "return_monthly": ar_monthly,
        }

    def unit_custom_indicator(
        self, indicators: List[str], company: str
    ) -> Dict[str, Any]:
        result = {}
        result["company symbol"] = company
        if "daily moving average" in indicators:
            dma_result = self.unit_dma_absolute(company=company)
            result["comany name"] = dma_result["company name"]
            result["dma"] = dma_result["sma"]
            result["dma action"] = dma_result["action"]
        if "exponential moving average" in indicators:
            ema_result = self.unit_ema_absolute(company=company)
            result["comany name"] = ema_result["company name"]
            result["ema"] = ema_result["ema"]
            result["ema action"] = ema_result["action"]

        return result
