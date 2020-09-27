import datetime
import pandas as pd
from typing import List, Union
from stock_analysis.utils.helpers import get_appropriate_date_ema


def annualized_rate_of_return(end_date: int,
                              start_date: int,
                              duration: float) -> float:
    """
    Calculate annulized rate of return

    Parameters
    ----------
    end_date : int
        Close value Current date or most present date.
        Consider it as going from bottom to top.
    start_date : int
        Close value on Start date or first record.
        Consider it as going from bottom to top.
    duration : float
        Total duration wrt to year

    Returns
    -------
    float
        Annulized return
    """
    return (((end_date / start_date) ** (1/duration)) - 1) * 100


def exponential_moving_avarage(data_df: Union[pd.Series, List],
                               period: int,
                               cutoff_date: Union[str,
                                                  datetime.datetime] = 'today',
                               smoothing_factor: int = 2,
                               verbosity: int = 1) -> float:
    """Calculate exponential moving avarage based on given period

    Parameters
    ----------
    data : Union[pd.Series,List]
        Data to calculate ema
    period : int
        Period for which ema has to be calculated
    smoothing_factor : int, optional
        Smoothing factor which will be used to calculate
        Multiplying factor, by default 2

    Returns
    -------
    float
        ema value
    """
    ema_list = []
    # Calculating multiplying factor
    mf = smoothing_factor/(1 + period)

    # Calculating first SMA
    sma0 = (sum(data_df['Close'][:period])) / period

    # Calculating first EMA
    ema0 = (data_df['Close'][period] * mf) + (sma0 * (1 - mf))

    # Calculating latest EMA
    ema_pre = ema0

    for idx in range(1, len(data_df)-50):
        ema = (data_df['Close'][idx + 50] * mf) + (ema_pre * (1 - mf))
        ema_pre = ema
        ema_list.append(ema)
        # if cutoff_date is not None:
        if idx == (len(data_df) - 50):
            break
    data_df['ema'] = [pd.NA] * (len(data_df) - len(ema_list)) + ema_list
    if cutoff_date == 'today':
        date = data_df.index[-1]
    else:
        date = get_appropriate_date_ema(
            company_df=data_df,
            desired_date=cutoff_date,
            verbosity=verbosity
        )

    return float(data_df[data_df.index == date]['ema'])


def percentage_diff_analysis(value_a: float,
                             value_b: float):
    """
    Used to calculate Percentage difference of Value of B wrt to A
    """
    return abs((value_b - value_a)/((value_a + value_b) / 2) * 100)


def outcome_analysis(ratio: float):
    """
    Used to determine closeness based on any given ratio analysis 
    like percentage difference 
    """
    if 5 < ratio < 5:
        outcome = 'close by'
    else:
        outcome = 'far away'
    return outcome
