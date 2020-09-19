import os
import yaml
import datetime
import dateutil
import pandas as pd
import yfinance as yf
from typing import List, Union, Tuple
from pandas_datareader import data as pdr
from stock_analysis.indicator import Indicator
from stock_analysis.utils.logger import logger
from stock_analysis.data_retrive import DataRetrive

yf.pdr_override()
logger = logger()
pd.options.display.float_format = '{:,.2f}'.format


class UnitStrategy:
    """
    Perform general operation

    Eg:
    >>>from stock_analysis.unit_strategy import UnitStrategy
    >>>sa = UnitStrategy('./data/company_list.yaml')
    """

    def __init__(self, path: str=None, company_name: List=None):
        """
        Parameters
        ----------
        path : str, optional
            Path to company yaml/json. Either path or company_name can be used, by default None
        company_name : List, optional
            List of company name. If path is used then this is obsolete as 'path' preside over 'company_name', by default None
        """

        
        self.path = path
        self.company_name = company_name

        if path is not None:
            with open(self.path, 'r') as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            self.data = {'company':self.company_name}

    def momentum_strategy(self,
                          end_date: str = 'today',
                          top_company_count: int = 20,
                          save: bool =True,
                          export_path: str = '.',
                          verbosity: int = 1) -> pd.DataFrame:
        """
        The strategy is used to identity stocks which had 'good performance' based on desired 'return' duration

        eg
        >>>from stock_analysis import UnitStrategy
        >>>sa = UnitStrategy('./data/company_list.yaml')
        >>>sa.momentum_strategy(end_date='01/06/2020')

        Parameters
        ----------
        end_date : str, optional
            End date of of stock record to retrive. Must be in format: dd/mm/yyyy, by default 'today' for current date
        top_company_count : int, optional
            No of top company to retrieve based on Annualized return, by default 20
        save : int, optional
            Wether to export to disk, by default True
        export_path : str, optional
            Path to export csv. To be used only if 'save' is True, by default '.'

        Returns
        -------
        pd.DataFrame
            Record based on monthly and yearly calculation
        """

        if end_date == 'today':
            end = datetime.datetime.now()
        else:
            end = datetime.datetime.strptime(end_date, '%d/%m/%Y').date()
        start = end - dateutil.relativedelta.relativedelta(years=1)

        invalid_company = []
        momentum_df = pd.DataFrame(columns=['company', 'yearly_start_date', 'yearly_start_date_close', 'yearly_end_date', 'yearly_end_date_close',
                                            'return_yearly', 'monthly_start_date', 'monthly_start_date_close', 'monthly_end_date', 'monthly_end_date_close', 'return_monthly'])
        for idx, company in enumerate(self.data['company']):
            logger.info(
                f"Retriving data {idx + 1} out of {len(self.data['company'])} for {company}")
            try:
                company_df = DataRetrive.single_company_specific(
                    company_name=f"{company}.NS", start_date=start, end_date=end)
                company_df.reset_index(inplace=True)
                ar_yearly = self._annualized_rate_of_return(end_date=company_df.iloc[-1].Close,
                                                            start_date=company_df.iloc[0].Close,
                                                            duration=1)  # (company_df.iloc[-30,0] - company_df.iloc[0,0]).days/365)
                ar_monthly = self._annualized_rate_of_return(end_date=company_df.iloc[-1].Close,
                                                             start_date=self._get_appropriate_date(company_df, verbosity=verbosity)[1],  # company_df.iloc[-30].Close,
                    duration=(company_df.iloc[-1, 0] - company_df.iloc[-30, 0]).days/30)
                momentum_df = momentum_df.append({'company': company,
                                                  'yearly_start_date': company_df.iloc[0].Date.strftime('%d-%m-%Y'),
                                                  'yearly_start_date_close': company_df.iloc[0].Close,
                                                  'yearly_end_date': company_df.iloc[-1].Date.strftime('%d-%m-%Y'),
                                                  'yearly_end_date_close': company_df.iloc[-1].Close,
                                                  'return_yearly': ar_yearly,
                                                  'monthly_start_date': self._get_appropriate_date(company_df, verbosity=verbosity)[0].strftime('%d-%m-%Y'),
                                                  'monthly_start_date_close': company_df.iloc[-30].Close,
                                                  'monthly_end_date': company_df.iloc[-1].Date.strftime('%d-%m-%Y'),
                                                  'monthly_end_date_close': company_df.iloc[-1].Close,
                                                  'return_monthly': ar_monthly},
                                                ignore_index=True)
            except:
                invalid_company.append(company)
        momentum_df.sort_values(by=['return_yearly'],
                                ascending=False,
                                inplace=True)
        
        if verbosity > 0 and len(invalid_company) != 0:
            logger.debug(
                f"Following Company's data is not available: {', '.join(invalid_company)}")
        if save is True:
            momentum_df.head(top_company_count).to_csv(
            f"{export_path}/momentum_result_{end.strftime('%d-%m-%Y')}_top_{top_company_count}.csv", index=False)
            logger.debug(f"Saved at {export_path}/momentum_result_{end.strftime('%d-%m-%Y')}_top_{top_company_count}.csv")
        if verbosity > 0:
            logger.debug(
                f"Sample output:\n{momentum_df.head(top_company_count)}")
            
        return momentum_df.head(top_company_count)
    
    def momentum_with_ema_strategy(self,
                                    end_date: str = 'today',
                                    top_company_count: int = 20,
                                    ema_canditate:Tuple[int, int]=(50,200),
                                    save: bool=True,
                                    export_path: str = '.',
                                    verbosity: int = 1)->pd.DataFrame:
        
        logger.info("Performing Momentum Strategy task")
        momentum_df = self.momentum_strategy(end_date=end_date,
                                             top_company_count=top_company_count,
                                             save=False,
                                             verbosity=verbosity)
        momentum_df.reset_index(drop=True,inplace=True)
        
        ind = Indicator(company_name=momentum_df.loc[:,'company'])
        logger.info(f"Performing EMA task on top {top_company_count} company till {end_date}")
        if end_date == 'today':
            cutoff_date = end_date
            save_date = datetime.datetime.now().strftime('%d-%m-%Y')
        else:
            save_date = end_date.replace('/', '-')
            cutoff_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            assert isinstance(cutoff_date, datetime.datetime), 'Incorrect date type'
        ema_df = ind.ema_indicator(ema_canditate=ema_canditate,
                                   cutoff_date=cutoff_date,
                                   save=False, 
                                   verbosity=verbosity)
        momentum_ema_df = momentum_df.merge(ema_df, 
                                            on='company',
                                            validate='1:1')
        if save is True:
            momentum_ema_df.reset_index(drop=True, inplace=True)
            momentum_ema_df.to_csv(
            f"{export_path}/momentum_ema{ema_canditate[0]}-{ema_canditate[1]}_{save_date}_top_{top_company_count}.csv", index=False)
            logger.debug(f"Saved at {export_path}/momentum_ema{ema_canditate[0]}-{ema_canditate[1]}_{save_date}_top_{top_company_count}.csv")
            if verbosity > 0:
                logger.debug(
                    f"Sample output:\n{momentum_ema_df.head()}")
        else:
            return momentum_ema_df

    @staticmethod
    def _annualized_rate_of_return(end_date: int,
                                   start_date: int,
                                   duration: float) -> float:
        """
        Calculate annulized rate of return

        Parameters
        ----------
        end_date : int
            Close value Current date or most present date. Consider it as going from bottom to top. 
        start_date : int
            Close value on Start date or first record. Consider it as going from bottom to top.
        duration : float
            Total duration wrt to year

        Returns
        -------
        float
            Annulized return
        """
        return (((end_date / start_date) ** (1/duration)) - 1) * 100

    @staticmethod
    def _get_appropriate_date(company_df: pd.DataFrame,
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
                f"Your desired date for monthly return is {desired_date.strftime('%d-%m-%Y')}")

        if len(company_df.loc[company_df['Date'] == desired_date]) != 0:
            desired_close = company_df.loc[company_df['Date'] == desired_date]
        else:
            for i in range(1, 100):
                if len(company_df.loc[company_df['Date'] == desired_date]) == 0:
                    desired_date = desired_date - \
                        dateutil.relativedelta.relativedelta(days=i)
                    desired_close = company_df.loc[company_df['Date']
                                                   == desired_date]
                break
            if verbosity > 0:
                logger.warning(
                    f"Desired date: {dd_copy.strftime('%d-%m-%Y')} not found going for next possible date: {desired_date.strftime('%d-%m-%Y')}")
        return desired_date, desired_close.iloc[-1].Close
