import datetime
from typing import List, Union

import pandas as pd

from stock_analysis.utils.helpers import get_appropriate_date_ema


def annualized_rate_of_return(end_date: int, start_date: int, duration: float) -> float:
    """Calculate annulized rate of return

    Args:
        end_date (int): Close value Current date or most present date. Consider
                        it as going from bottom to top.
        start_date (int): Close value on Start date or first record. Consider
                        it as going from bottom to top.
        duration (float): Total duration wrt to year

    Returns:
        float: Annulized return
    """

    return (((end_date / start_date) ** (1 / duration)) - 1) * 100


def simple_moving_average(data: Union[pd.Series, List], period: int) -> float:
    """Calculate SMA, which is nothing but calculating mean

    Args:
        data (Union[pd.Series, List]): data on which SMA have to be calculate
        period (int): Total period used to calculate SMA

    Returns:
        float: SMA calculated over given period
    """
    return (sum(data[:period])) / period


def exponential_moving_average(
    data_df: pd.DataFrame,
    period: int,
    cutoff_date: Union[str, datetime.datetime] = "today",
    smoothing_factor: int = 2,
    verbosity: int = 1,
) -> float:
    """Calculate exponential moving avarage based on given period

    Args:
        data_df (pd.Dataframe): Data to calculate ema
        period (int): Period for which ema has to be calculated
        cutoff_date (Union[str, datetime.datetime], optional): . Defaults to "today".
        smoothing_factor (int, optional): Smoothing factor which will be used to calculate 'Multiplying factor'. Defaults to 2.
        verbosity (int, optional): . Defaults to 1.

    Returns:
        float: ema value
    """

    ema_list = []
    # Calculating multiplying factor
    mf = smoothing_factor / (1 + period)

    # Calculating first SMA
    sma0 = simple_moving_average(data_df["Close"], period)

    # Calculating first EMA
    ema0 = (data_df["Close"][period] * mf) + (sma0 * (1 - mf))

    # Calculating latest EMA
    ema_pre = ema0

    for idx in range(1, len(data_df) - 50):
        ema = (data_df["Close"][idx + 50] * mf) + (ema_pre * (1 - mf))
        ema_pre = ema
        ema_list.append(ema)
        # if cutoff_date is not None:
        if idx == (len(data_df) - 50):
            break
    data_df["ema"] = [pd.NA] * (len(data_df) - len(ema_list)) + ema_list
    if cutoff_date == "today":
        date = data_df.index[-1]
    else:
        date = get_appropriate_date_ema(
            company_df=data_df, desired_date=cutoff_date, verbosity=verbosity
        )

    return float(data_df[data_df.index == date]["ema"])


def percentage_diff(
    value_a: float, value_b: float, return_absolute: bool = False
) -> float:
    """Used to calculate Percentage difference of Value of B wrt to A. It can be either absolute or not.

    Args:
        value_a (float): Value a
        value_b (float): Value b
        return_absolute (bool): Return absolute percentage difference

    Returns:
        float: percentage difference
    """
    if return_absolute is True:
        return abs((value_b - value_a) / ((value_a + value_b) / 2) * 100)
    elif return_absolute is False:
        return (value_b - value_a) / ((value_a + value_b) / 2) * 100


def outcome_analysis(ratio: float, cutoff: int = 5) -> str:
    """Used to determine closeness based on any given ratio analysis
    like percentage difference

    Args:
        ratio (float): metrics to determine outcome
        cutoff (int, optional): number to determine outcome. Defaults to 5.

    Returns:
        str: Outcome of analysis
    """ """
    Used to determine closeness based on any given ratio analysis
    like percentage difference
    """
    if cutoff < ratio < cutoff:
        outcome = "close by"
    else:
        outcome = "far away"
    return outcome


def turnover(volume: Union[pd.Series, List], price: float) -> float:
    """Calculate given Stock's batch turnover over specified time

    Args:
        volume (Union[pd.Series, List]): batch volume data
        price (float): price of respective stock

    Returns:
        float
    """
    return (sum(volume) / len(volume)) * price
