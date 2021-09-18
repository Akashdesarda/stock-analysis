import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import pandas as pd
import yaml
from joblib import Parallel, delayed, parallel_backend

from stock_analysis.executors.parallel import UnitExecutor
from stock_analysis.utils.formula_helpers import outcome_analysis, percentage_diff
from stock_analysis.utils.helpers import new_folder
from stock_analysis.utils.logger import logger

now_strting = datetime.datetime.now().strftime("%d-%m-%Y")
logger = logger()
pd.options.display.float_format = "{:,.2f}".format


@dataclass
class Indicator(UnitExecutor):
    """Perform Indicator operation which are based on specific metrics used to study the performance
    of desired stock/company.

    Args:
        path ([str, optional]): Path to company yaml/json. Either path or company_name can be used.
        company_name ([List, optional]): List of company name. If path is used then this is obsolete
        as 'path' preside over 'company_name'

    Example:
    ```python
    from stock_analysis.indicator import Indicator
    ind = Indicator('./data/company_list.yaml')
    ```
    """

    path: Optional[str] = None
    company_name: Optional[List] = None

    def __post_init__(self):
        if self.path is not None:
            with open(self.path, "r") as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            self.data = {"company": self.company_name}

    def volume_n_days_indicator(
        self,
        duration: int = 90,
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """Mean Volume Indicator based on desired days

        Args:
            duration (int, optional): Total days from current date to retrive data. Defaults to 90.
            save (bool, optional): Save to hard disk. Defaults to True.
            export_path (str, optional): Path to save, to be used only if 'save' is true. Defaults to ".".
            verbosity (int, optional): Level of detail logging,1=< Deatil, 0=Less detail. Defaults to 1.

        Returns:
            All Volume based indicator

        Example:
        ```python
        from stock_analysis.indicator import Indicator
        ind = Indicator('./data/company_list.yaml')
        vol = ind.volume_n_days_indicator(150)
        ```
        """

        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_vol_indicator_n_days)(company, duration)
                for company in self.data["company"]
            )

        vol_ind_df = pd.DataFrame(result)
        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{vol_ind_df.head()}")
        if save is True:
            new_folder(export_path)
            vol_ind_df.to_csv(
                f"{export_path}/VolumeIndicator90Days_detailed_{now_strting}.csv",
                index=False,
            )
            if verbosity > 0:
                logger.debug(
                    f"Save at {export_path}/VolumeIndicator90Days_detailed_{now_strting}.csv"
                )
        else:
            return vol_ind_df

    def ema_indicator(
        self,
        ema_canditate: Tuple[int, int] = (50, 200),
        cutoff_date: Union[str, datetime.datetime] = "today",
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """Exponential moving average based on desired two period (or no of days)

        Args:
            ema_canditate (Tuple[int, int], optional): Two number used two calculate EMA. Defaults to (50, 200).
            cutoff_date (Union[str, datetime.datetime], optional): Desired date till which to calculate ema. Defaults to "today".
            save (bool, optional): Save to hard disk. Defaults to True.
            export_path (str, optional): Path to save, to be used only if 'save' is true. Defaults to ".".
            verbosity (int, optional): Level of detail logging,1=< Detail, 0=Less detail. Defaults to 1.

        Returns:
            EMA and indicators based on it

        Example:
        ```python
        from stock_analysis.indicator import Indicator
        ind = Indicator('./data/company_list.yaml')
        ema = ind.ema_indicator((50,200), '01/06/2020')
        ```
        """

        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_ema_indicator)(
                    company, ema_canditate, cutoff_date, verbosity
                )
                for company in self.data["company"]
            )

        ema_indicator_df = pd.DataFrame(result)
        ema_indicator_df.dropna(inplace=True)
        ema_indicator_df["percentage_diff"] = ema_indicator_df.apply(
            lambda x: percentage_diff(
                x[f"ema{str(ema_canditate[0])}"],
                x[f"ema{str(ema_canditate[1])}"],
                return_absolute=True,
            ),
            axis=1,
        )
        ema_indicator_df["outcome"] = ema_indicator_df.apply(
            lambda x: outcome_analysis(x["percentage_diff"]), axis=1
        )

        ema_indicator_df = ema_indicator_df[
            [
                "company",
                "ema_date",
                f"ema{str(ema_canditate[0])}",
                f"ema{str(ema_canditate[1])}",
                "percentage_diff",
                "outcome",
                "action",
            ]
        ]

        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{ema_indicator_df.head()}")
        if save is True:
            new_folder(export_path)
            ema_indicator_df.to_csv(
                f"{export_path}/ema_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv",
                index=False,
            )
            if verbosity > 0:
                logger.debug(
                    f"Exported at {export_path}/ema_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv"
                )

        else:
            return ema_indicator_df

    def ema_detail_indicator(
        self,
        ema_canditate: Tuple[int, int] = (50, 200),
        cutoff_date: Union[str, datetime.datetime] = "today",
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """Exponential moving average based on desired two period (or no of days) with additional info
        which include:
        > regularMarketVolume, marketCap, bookValue, priceToBook, averageDailyVolume3Month,
        averageDailyVolume10Day, fiftyTwoWeekLowChange, fiftyTwoWeekLowChangePercent, fiftyTwoWeekRange,
        fiftyTwoWeekHighChange, fiftyTwoWeekHighChangePercent, fiftyTwoWeekLow, fiftyTwoWeekHigh

        Args:
            ema_canditate (Tuple[int, int], optional): Two number used two calculate EMA. Defaults to (50, 200).
            cutoff_date (Union[str, datetime.datetime], optional): Desired date till which to calculate ema. Defaults to "today".
            save (bool, optional): Save to hard disk. Defaults to True.
            export_path (str, optional): Path to save, to be used only if 'save' is true. Defaults to ".".
            verbosity (int, optional): Level of detail logging,1=< Detail, 0=Less detail. Defaults to 1.

        Returns:
            EMA and detailed metrics for indicators

        Example:
        ```python
        from stock_analysis.indicator import Indicator
        ind = Indicator('./data/company_list.yaml')
        ema = ind.ema_detail_indicator((50,200), '01/06/2020')
        ```
        """

        logger.info("Performing EMA Indicator Task")
        ema_short = self.ema_indicator(
            ema_canditate=ema_canditate,
            cutoff_date=cutoff_date,
            save=False,
            verbosity=verbosity,
        )

        logger.info("Extarcting detail company quote data")
        batch_company_quote = pd.DataFrame()
        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            company_quote = Parallel()(
                delayed(self.unit_quote_retrive)(company)
                for company in ema_short["company"]
            )
        for single_company_quote in company_quote:
            if isinstance(single_company_quote, pd.DataFrame):
                batch_company_quote = batch_company_quote.append(single_company_quote)

        batch_company_quote = batch_company_quote.reset_index().rename(
            columns={"index": "company"}
        )
        batch_company_quote = batch_company_quote[
            [
                "company",
                "longName",
                "price",
                "regularMarketVolume",
                "marketCap",
                "bookValue",
                "priceToBook",
                "averageDailyVolume3Month",
                "averageDailyVolume10Day",
                "fiftyTwoWeekLowChange",
                "fiftyTwoWeekLowChangePercent",
                "fiftyTwoWeekRange",
                "fiftyTwoWeekHighChange",
                "fiftyTwoWeekHighChangePercent",
                "fiftyTwoWeekLow",
                "fiftyTwoWeekHigh",
            ]
        ]

        batch_company_quote["company"] = batch_company_quote["company"].str.replace(
            ".NS", ""
        )

        ema_quote = ema_short.merge(batch_company_quote, on="company", validate="1:1")

        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{ema_quote.head()}")
        if save is not False:
            ema_quote.to_csv(
                f"{export_path}/ema_detail_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv",
                index=False,
            )
            if verbosity > 0:
                logger.debug(
                    f"Exported at {export_path}/ema_detail_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv"
                )

        else:
            return ema_quote

    def ema_crossover_detail_indicator(
        self,
        ema_canditate: Tuple[int, int, int] = (5, 13, 26),
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """Exponential moving average for crossover triple period technique

        Args:
            ema_canditate (Tuple[int, int, int], optional): Three Period (or days) to calculate EMA. Defaults to (5, 13, 26).
            save (bool, optional): Save to hard disk. Defaults to True.
            export_path (str, optional): Path to save, to be used only if 'save' is true. Defaults to ".".
            verbosity (int, optional): Level of detail logging,1=< Deatil, 0=Less detail. Defaults to 1.

        Returns:
            Results is based on crossover ema and detailed metrics

        Example:
        ```python
        from stock_analysis.indicator import Indicator
        ind = Indicator('./data/company_list.yaml')
        ema = ind.ema_crossover_detail_indicator((5,10,020), '01/06/2020')
        ```
        """

        logger.info("Performing EMA Indicator Task")
        ema_short = self._ema_indicator_n3(
            ema_canditate=ema_canditate, verbosity=verbosity
        )

        logger.info("Extarcting detail company quote data")
        batch_company_quote = pd.DataFrame()
        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            company_quote = Parallel()(
                delayed(self.unit_quote_retrive)(company)
                for company in ema_short["company"]
            )
        for single_company_quote in company_quote:
            if isinstance(single_company_quote, pd.DataFrame):
                batch_company_quote = batch_company_quote.append(single_company_quote)

        batch_company_quote = batch_company_quote.reset_index().rename(
            columns={"index": "company"}
        )
        batch_company_quote = batch_company_quote[
            [
                "company",
                "longName",
                "price",
                "regularMarketVolume",
                "marketCap",
                "bookValue",
                "priceToBook",
                "averageDailyVolume3Month",
                "averageDailyVolume10Day",
                "fiftyTwoWeekLowChange",
                "fiftyTwoWeekLowChangePercent",
                "fiftyTwoWeekRange",
                "fiftyTwoWeekHighChange",
                "fiftyTwoWeekHighChangePercent",
                "fiftyTwoWeekLow",
                "fiftyTwoWeekHigh",
            ]
        ]

        batch_company_quote["company"] = batch_company_quote["company"].str.replace(
            ".NS", ""
        )

        ema_quote = ema_short.merge(batch_company_quote, on="company", validate="1:1")

        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{ema_quote.head()}")
        if save is not False:
            ema_quote.to_csv(
                f"{export_path}/ema_crossover_detail_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}-{str(ema_canditate[2])}_{len(self.data['company'])}company_{now_strting}.csv",
                index=False,
            )
            if verbosity > 0:
                logger.debug(
                    f"Exported at {export_path}/ema_crossover_detail_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}-{str(ema_canditate[2])}_{len(self.data['company'])}company_{now_strting}.csv"
                )

        else:
            return ema_quote

    def _ema_indicator_n3(
        self,
        ema_canditate: Tuple[int, int, int] = (5, 13, 26),
        cutoff_date: Union[str, datetime.datetime] = "today",
        verbosity: int = 1,
    ) -> pd.DataFrame:

        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_ema_indicator_n3)(
                    company, ema_canditate, cutoff_date, verbosity
                )
                for company in self.data["company"]
            )
        ema_indicator_df = pd.DataFrame(result)
        ema_indicator_df.dropna(inplace=True)

        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{ema_indicator_df.head()}")
        return ema_indicator_df
