import dateutil
import datetime
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple, Union
from stock_analysis.data_retrive import DataRetrive
from stock_analysis.utils.logger import logger
from stock_analysis.utils.formula_helpers import (
    exponential_moving_avarage,
    abs_percentage_diff,
    simple_moving_average,
    turnover,
)

now_strting = datetime.datetime.now().strftime("%d-%m-%Y")
logger = logger()
pd.options.display.float_format = "{:,.2f}".format

@dataclass
class UnitExecutor:

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
            EMA_A = exponential_moving_avarage(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            EMA_B = exponential_moving_avarage(
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
            EMA_A = exponential_moving_avarage(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[0],
                verbosity=verbosity,
            )
            EMA_B = exponential_moving_avarage(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[1],
                verbosity=verbosity,
            )
            EMA_C = exponential_moving_avarage(
                data_df=company_df,
                cutoff_date=cutoff_date,
                period=ema_canditate[2],
                verbosity=verbosity,
            )

            percentage_diff_cb = abs_percentage_diff(EMA_C, EMA_B)
            percentage_diff_ca = abs_percentage_diff(EMA_C, EMA_A)
            percentage_diff_ba = abs_percentage_diff(EMA_B, EMA_A)

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

        try:
            sma = simple_moving_average(company_df["Close"][-(period - 1) :], period)
            buy = sma + (sma * (cutoff / 100))
            sell = sma - (sma * (cutoff / 100))
            if buy < company_df["Close"][-1]:
                action = "buy"
            elif sell > company_df["Close"][-1]:
                action = "sell"
            elif sell < company_df["Close"][-1] < buy:
                action = "no action"
            long_name = self.unit_quote_retrive(company)["longName"][0]
            current_price = company_df["Close"][-1]
            turnover_value = turnover(company_df["Volume"][-period:], sma) / 10000000
        except (KeyError, IndexError, ValueError, TypeError):
            logger.warning(f"{company} has less record than minimum rexquired")
            long_name, sma, current_price, action, turnover_value = (
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