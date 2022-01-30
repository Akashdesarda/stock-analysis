import datetime
from dataclasses import dataclass
from typing import List, Optional

import pandas as pd
import yaml
from joblib import Parallel, delayed, parallel_backend

from stock_analysis.executors.parallel import UnitExecutor
from stock_analysis.utils.helpers import new_folder
from stock_analysis.utils.logger import logger

now_strting = datetime.datetime.now().strftime("%d-%m-%Y")
logger = logger()
pd.options.display.float_format = "{:,.2f}".format


@dataclass
class CustomMultiIndicator(UnitExecutor):
    """Perform Multi-Indicator operation which are based on specific metrics used to study the performance
    of desired stock/company. User has the ability to choose any indicator from availabe list.

    Args:
        path ([str, optional]): Path to company yaml/json. Either path or company_name can be used.
        company_name ([List, optional]): List of company name. If path is used then this is obsolete
        as 'path' preside over 'company_name'

    Example:
    ```python
    from stock_analysis.indicator import CustomMultiIndicator
    cus_mul_ind = CustomMultiIndicator('./data/company_list.yaml')
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

    def multi_choice_indicator(
        self,
        indicators: List[str],
        save: bool = True,
        export_path: str = ".",
        verbosity: int = 1,
    ) -> Optional[pd.DataFrame]:
        """Apply indicator based on user selected indicator

        Args:
            indicators (List[str]): list of all the indicators that must be applied
            save (bool, optional): save to result as csv. Defaults to True.
            export_path (str, optional): path to save on disk. Must be used only in `save` is True.
            Defaults to ".".
            verbosity (int, optional): level of detailed to be logged. Defaults to 1.

        Example:
        ```python
        from stock_analysis.custom_multi_indicator import CustomMultiIndicator
        indicators = ["daily moving average", "exponential moving average"]
        mul_ind = cus_mul_ind.multi_choice_indicator(indicators=indicators, save=False)
        ```
        Returns:
            Optional[pd.DataFrame]: compiled results of all selected indicators
        """
        with parallel_backend(n_jobs=-1, backend="multiprocessing"):
            result = Parallel()(
                delayed(self.unit_custom_indicator)(indicators, company)
                for company in self.data["company"]
            )

        multi_choice_df = pd.DataFrame(result)
        if verbosity > 0:
            logger.debug(f"Here are sample 5 company\n{multi_choice_df.head()}")
        if save is True:
            new_folder(export_path)
            multi_choice_df.to_csv(
                f"{export_path}/multi_choice_indicator_{now_strting}.csv",
                index=False,
            )
            if verbosity > 0:
                logger.debug(
                    f"Save at {export_path}/multi_choice_indicator_{now_strting}.csv"
                )
        else:
            return multi_choice_df
