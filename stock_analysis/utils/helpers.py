import os
import datetime
import dateutil
import pandas as pd
from typing import Tuple
from stock_analysis.utils.logger import logger


logger = logger()

def get_appropriate_date_ema(company_df: pd.DataFrame,
                         desired_date: datetime.datetime,
                         verbosity: int = 1) -> Tuple[datetime.datetime, float]:
    """
    Return appropriate date which is present in data record.

    Parameters
    ----------
    company_df : pd.DataFrame
        Company dataframe
    duration : datetime.datetime
        Desired date cut-off to calculate ema
    verbosity : int, optional
        Level of detail logging, by default 1

    Returns
    -------
    Tuple[datetime.datetime,float]
        Date,Close value on date retrived

    Raises
    ------
    ValueError
        If desired old is older than first record
    """
    if desired_date < company_df.index[0]:
        logger.error(
            f"Given desired date {desired_date.strftime('%d-%m-%Y')} is older than first recorded date {company_df.index[0].strftime('%d-%m-%Y')}")

    if verbosity > 0:
        logger.debug(
            f"Your desired EMA cut-off date is {desired_date.strftime('%d-%m-%Y')}")

    for day_idx in range(1, 100):
        if desired_date not in company_df.index:
            date = desired_date - \
                dateutil.relativedelta.relativedelta(days=day_idx)
        else:
            date = desired_date
        if date in company_df.index:
            break
    if verbosity > 0 and desired_date != date:
        logger.warning(
            f"Desired date: {desired_date.strftime('%d-%m-%Y')} not found going for next possible date: {date.strftime('%d-%m-%Y')}")

    return date

def get_appropriate_date_momentum(company_df: pd.DataFrame,
                         company,
                         duration: Tuple[int, int] = (0, 1),
                         verbosity: int = 1) -> Tuple[datetime.datetime, float]:
    """
    Return appropriate date which is present in data record.

    Parameters
    ----------
    company_df : pd.DataFrame
        Company dataframe
    duration : Tuple[year,month], optional
        Desired duration to go back to retrive record, by default (0,1)
    verbosity : int, optional
        Level of detail logging,1=< Deatil, 0=Less detail , by default 1

    Returns
    -------
    Tuple[datetime.datetime,float]
        Date,Close value on date retrived

    Raises
    ------
    ValueError
        If desired old is older than first record
    """

    current_date = company_df.iloc[-1].Date
    desired_date = current_date - \
        dateutil.relativedelta.relativedelta(
            years=duration[0], months=duration[1])
    if desired_date < company_df.iloc[0].Date:
        logger.error(
            f"Given desired date {desired_date.strftime('%d-%m-%Y')} is older than first recorded date {company_df.iloc[0].Date.strftime('%d-%m-%Y')}")
        raise ValueError
    dd_copy = desired_date

    if verbosity > 0:
        logger.debug(
            f"Your desired date for monthly return  for {company} is {desired_date.strftime('%d-%m-%Y')}")

    if len(company_df.loc[company_df['Date'] == desired_date]) != 0:
        desired_close = company_df.loc[company_df['Date'] == desired_date]
    else:
        for i in range(1, 100):
            if len(company_df.loc[company_df['Date'] == desired_date]) == 0:
                desired_date = desired_date - \
                    dateutil.relativedelta.relativedelta(days=i)
                desired_close = company_df.loc[company_df['Date'] == desired_date]
            break
        if verbosity > 0:
            logger.warning(
                f"Desired date: {dd_copy.strftime('%d-%m-%Y')} not found going for next possible date: {desired_date.strftime('%d-%m-%Y')}")
    return desired_date, desired_close.iloc[-1].Close

def new_folder(path: str):
    """Create a folder if not present

    Parameters
    ----------
    path : str
        path to create a new folder
    """
    if not os.path.exists(path):
        logger.warning(f"Given {path} mot present, so creating ")
        os.mkdir(path)