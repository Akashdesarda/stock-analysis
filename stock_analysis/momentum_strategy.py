"""This packs all the api functionality w.r.t. Momentum strategy
"""
import datetime
from dataclasses import dataclass
from typing import List, Optional, Tuple

import dateutil
import pandas as pd
import yaml
import yfinance as yf
from joblib import Parallel, delayed, parallel_backend

from stock_analysis.executors.parallel import UnitExecutor
from stock_analysis.indicator import Indicator
from stock_analysis.utils.helpers import new_folder
from stock_analysis.utils.logger import set_logger

yf.pdr_override()
logger = set_logger()
pd.options.display.float_format = "{:,.2f}".format
now_strting = datetime.datetime.now().strftime("%d-%m-%Y")


@dataclass
class MomentumStrategy(UnitExecutor):
    """Traders measure momentum in many different ways to identify opportunity pockets.
    The core idea across all these strategies remains the same i.e to identify momentum and ride the
    wave. The strategy are combinations of several metrics to determine momentum.

    Usage:
    ```python
    from stock_analysis.momentum_strategy import MomentumStrategy
    ma = MomentumStrategy('./data/company_list.yaml')
    ```

    Args:
        path ([str, optional]): Path to company yaml/json. Either path or company_name can be used.
        Default to None.
        company_name ([List, optional]): List of company name. If path is used then this is obsolete
        as 'path' preside over 'company_name'. Default to None.
    """

    path: Optional[str] = None
    company_name: Optional[List] = None

    def __post_init__(self):
        if self.path is not None:
            with open(self.path, "r", encoding="utf-8") as input_file:
                self.data = yaml.load(input_file, Loader=yaml.FullLoader)
        else:
            self.data = {"company": self.company_name}

    def relative_momentum(
        self,
        end_date: str = "today",
        top_company_count: int = 20,
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """The strategy is used to identity stocks which had 'good performance'
        based on desired 'return' duration


        Args:
            end_date (str, optional): End date of of stock record to retrive. Must be in
            format: dd/mm/yyyy. Defaults to 'today'.
            top_company_count (int, optional): No of top company to retrieve based on Annualized
            return. Defaults to 20.
            save (bool, optional): Wether to export to disk. Defaults to True.
            export_path (str, optional): Path to export csv.To be used only if 'save' is True.
            Defaults to '.'.
            verbosity (int, optional): Level of detail logging, 1=< Deatil, 0=Less detail.
            Defaults to 1.

        Returns:
            Record based on monthly and yearly calculation

        Example:

        ```python
        from stock_analysis import MomentumStrategy
        sa = MomentumStrategy('./data/company_list.yaml')
        ms = sa.relative_momentum(end_date='01/06/2020')
        ```
        """
        if end_date == "today":
            end = datetime.datetime.now()
        else:
            end = datetime.datetime.strptime(end_date, "%d/%m/%Y").date()
        start = end - dateutil.relativedelta.relativedelta(years=1)

        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_momentum)(company, start, end, verbosity)
                for company in self.data["company"]
            )
        momentum_df = pd.DataFrame(result)

        # NOTE -"price (01-01-1000)" & "price (<NA>)" gets added as extra column if any given company's
        # data is not available. So need to remove this extra column.
        if "price (01-01-1000)" in momentum_df.columns:
            momentum_df.drop("price (01-01-1000)", axis="columns", inplace=True)
        if "price (<NA>)" in momentum_df.columns:
            momentum_df.drop("price (<NA>)", axis="columns", inplace=True)
        # need to drop a row who is have at three or more values as `NA`
        momentum_df.dropna(axis="index", thresh=3, inplace=True)
        # also need to drop a column who is having more than 2 values as `NA`
        momentum_df.dropna(axis="columns", thresh=2, inplace=True)

        # need sorting based on "return_yearly" to display the result
        momentum_df.sort_values(by=["return_yearly"], ascending=False, inplace=True)

        momentum_df.reset_index(inplace=True, drop=True)

        if verbosity > 0:
            logger.debug(f"Sample output:\n{momentum_df.head(top_company_count)}")
        if save is True:
            new_folder(export_path)
            momentum_df.head(top_company_count).to_csv(
                f"{export_path}/momentum_result_{end.strftime('%d-%m-%Y')}_top_{top_company_count}.csv",
                index=False,
                float_format="%.2f",
            )
            if verbosity > 0:
                logger.debug(
                    f"Saved at {export_path}/momentum_result_{end.strftime('%d-%m-%Y')}_top_{top_company_count}.csv"
                )
        else:
            return momentum_df.head(top_company_count)

    def relative_momentum_with_ema(
        self,
        end_date: str = "today",
        top_company_count: int = 20,
        ema_canditate: Tuple[int, int] = (50, 200),
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """The strategy is used to identity stocks with 'good performance'
        based on desired 'return' duration and 'exponential moving avg'.

        Args:
            end_date (str, optional): End date of of stock record to retrive. Must be in
            format: dd/mm/yyyy. Defaults to 'today'.
            top_company_count (int, optional): No of top company to retrieve based on Annualized
            return. Defaults to 20.
            ema_canditate (Tuple[int, int], optional): Period (or days) to calculate EMA.
            Defaults to (50, 200).
            save (bool, optional): Wether to export to disk. Defaults to True.
            export_path (str, optional): Path to export csv.To be used only if 'save' is True.
            Defaults to '.'.
            verbosity (int, optional): Level of detail logging,1=< Deatil, 0=Less detail. Defaults to 1.

        Returns:
            Record based on monthly and yearly calculation and EMA calculation

         Example:

        ```python
        from stock_analysis import MomentumStrategy
        sa = MomentumStrategy('./data/company_list.yaml')
        mes = sa.relative_momentum_with_ema('01/06/2020', 30)
        ```
        """

        logger.info("Performing Momentum Strategy task")
        momentum_df = self.relative_momentum(
            end_date=end_date,
            top_company_count=top_company_count,
            save=False,
            verbosity=verbosity,
        )
        momentum_df.reset_index(drop=True, inplace=True)

        ind = Indicator(company_name=momentum_df["symbol"])
        logger.info(
            f"Performing EMA task on top {top_company_count} company till {end_date}"
        )
        if end_date == "today":
            cutoff_date = end_date
            save_date = datetime.datetime.now().strftime("%d-%m-%Y")
        else:
            save_date = end_date.replace("/", "-")
            cutoff_date = datetime.datetime.strptime(end_date, "%d/%m/%Y")
            assert isinstance(cutoff_date, datetime.datetime), "Incorrect date type"
        ema_df = ind.ema_indicator(
            ema_canditate=ema_canditate,
            cutoff_date=cutoff_date,
            save=False,
            verbosity=verbosity,
        )
        # droping company, price (date) column as `momentum_df` already has it
        ema_df.drop(columns=ema_df.columns[[1, 2]], inplace=True)
        momentum_ema_df = momentum_df.merge(ema_df, on="symbol", validate="1:1")
        if save is True:
            new_folder(export_path)
            momentum_ema_df.reset_index(drop=True, inplace=True)
            momentum_ema_df.to_csv(
                f"{export_path}/momentum_ema{ema_canditate[0]}-{ema_canditate[1]}_{save_date}_top_{top_company_count}.csv",
                index=False,
                float_format="%.2f",
            )
            logger.debug(
                f"Saved at {export_path}/momentum_ema{ema_canditate[0]}-{ema_canditate[1]}_{save_date}_top_{top_company_count}.csv"
            )
            if verbosity > 0:
                logger.debug(f"Sample output:\n{momentum_ema_df.head()}")
        else:
            return momentum_ema_df

    def absolute_momentum_with_dma(
        self,
        end_date: str = "today",
        period: int = 200,
        cutoff: int = 5,
        save: bool = False,
        export_path: str = ".",
    ) -> Optional[pd.DataFrame]:
        """Action determination based on Daily moving average and Turnover

        Args:
            end_date (str, optional): Latest date to retrive data. Defaults to "today".
            period (int, optional): Desired period (in days) for batch SMA calculation. Defaults to 200.
            cutoff (int, optional): Desired cutoff to determine action. Defaults to 5.
            save (bool, optional): Save to hard disk. Defaults to False.
            export_path (str, optional): Path to save, to be used only if 'save' is true. Defaults to ".".

        Returns:
            Results with action (buy, sell, or no action) including DMA and turnover

         Example:

        ```
        from stock_analysis import MomentumStrategy
        sa = MomentumStrategy('./data/company_list.yaml')
        mes = sa.absolute_momentum_with_dma('01/06/2020', 30)
        ```
        """
        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_dma_absolute)(company, end_date, period, cutoff)
                for company in self.data["company"]
            )
        dma_compile = pd.DataFrame(result)
        # NOTE -"price (<NA>)" gets added as extra column if any given company's data is not available.
        # So need to remove this extra column.
        if "price (<NA>)" in dma_compile.columns:
            dma_compile.drop("price (<NA>)", axis="columns", inplace=True)
        # further droping row will at least 4 NA values
        dma_compile.dropna(thresh=4, inplace=True)

        if save is True:
            new_folder(export_path)
            if end_date == "today":
                end_date = now_strting
            else:
                end_date = end_date.replace("/", "-")
            dma_compile.to_csv(
                f"{export_path}/dma_action_cutoff_{str(cutoff)}_{end_date}.csv",
                index=False,
                float_format="%.2f",
            )
        else:
            return dma_compile
