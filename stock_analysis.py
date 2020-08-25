import os
from sys import path
import yaml
import datetime
import dateutil
import pandas as pd
from logger import logger
from datetime import date
from typing import List, Union, Tuple
from pandas_datareader import data as pdr
now_strting = datetime.datetime.now().strftime('%d-%m-%Y')

import yfinance as yf
yf.pdr_override()

logger = logger()

class StockAnalysis:
    """
    Perform general operation
    
    Eg:
    >>>from stock_analysis import StockAnalysis
    >>>sa = StockAnalysis('./data/company_list.yaml')
    """
    def __init__(self, path: str):
        """
        Parameters
        ----------
        path : str
            Path to csv
        """
                 
        self.path = path
        
        if 'csv' in os.path.split(self.path)[-1]:
            self.data = pd.read_csv(path, dayfirst=True)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        if 'yaml' in os.path.split(self.path)[-1]:
            with open(self.path, 'r') as f:
                self.data = yaml.load(f)    

    def momentum_strategy(self,
                          end_date: str='today', 
                          top_company_count: int=20,
                          export_path: str='.', 
                          verbosity: int=1)->pd.DataFrame:
        """
        The strategy is used to identity stocks which had 'good performance' based on desired 'return' duration
        
        eg
        >>>from stock_analysis import StockAnalysis
        >>>sa = StockAnalysis('./data/company_list.yaml')
        >>>sa.momentum_strategy(end_date='01/06/2020')

        Parameters
        ----------
        end_date : str, optional
            End date of of stock record to retrive. Must be in format: dd/mm/yyyy, by default 'today' for current date
        top_company_count : int, optional
            No of top company to retrieve based on Annualized return, by default 20
        export_path : str, optional
            Path to save csv, by default '.'

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
        momentum_df = pd.DataFrame(columns=['company', 'yealy_start_date','yealy_start_date_close','yealy_end_date','yealy_end_date_close',
                                            'return_yearly', 'monthly_start_date','monthly_start_date_close','monthly_end_date','monthly_end_date_close','return_monthly'])
        for idx,company in  enumerate(self.data['company']):
            logger.info(f"Retriving data {idx + 1} out of {len(self.data['company'])} for {company}")
            try:
                company_df = DataRetrive.single_company(company_name=f"{company}.NS", start_date=start, end_date=end)
                company_df.reset_index(inplace=True)
                ar_yearly = self._annualized_rate_of_return(end_date=company_df.iloc[-1].Close,
                                                            start_date=company_df.iloc[0].Close,
                                                            duration=1)#(company_df.iloc[-30,0] - company_df.iloc[0,0]).days/365)
                ar_monthly = self._annualized_rate_of_return(end_date=company_df.iloc[-1].Close,
                                                            start_date=self._get_appropriate_date(company_df, verbosity=verbosity)[1],#company_df.iloc[-30].Close,
                                                            duration=(company_df.iloc[-1,0] - company_df.iloc[-30,0]).days/30)
                momentum_df = momentum_df.append({'company':company,
                                                'yealy_start_date':company_df.iloc[0].Date, 
                                                'yealy_start_date_close':company_df.iloc[0].Close, 
                                                'yealy_end_date':company_df.iloc[-1].Date,
                                                'yealy_end_date_close':company_df.iloc[-1].Close,
                                                'return_yearly':ar_yearly, 
                                                'monthly_start_date':self._get_appropriate_date(company_df,verbosity=verbosity)[0].strftime('%Y-%m-%d'),
                                                'monthly_start_date_close':company_df.iloc[-30].Close,
                                                'monthly_end_date':company_df.iloc[-1].Date,
                                                'monthly_end_date_close':company_df.iloc[-1].Close,
                                                'return_monthly':ar_monthly},
                                                ignore_index=True)
            except:
                invalid_company.append(company)
        momentum_df.sort_values(by=['return_yearly'], 
                                ascending=False, 
                                inplace=True)
        momentum_df.head(top_company_count).to_csv(f"{export_path}/momentum_result_{end.strftime('%d-%m-%Y')}_top_{top_company_count}.csv", index=False)
        if verbosity > 0 and len(invalid_company) != 0:
            logger.debug(f"Following Company's data is not available: {', '.join(invalid_company)}")
    
    @staticmethod
    def _annualized_rate_of_return(end_date: int, 
                                  start_date: int, 
                                  duration: float)-> float:
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
                              duration: Tuple[int,int]=(0,1), 
                              verbosity: int=1)->Tuple[datetime.datetime,float]:
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
        desired_date = current_date - dateutil.relativedelta.relativedelta(years=duration[0], months=duration[1])
        if desired_date < company_df.iloc[0].Date:
            logger.error(f"Given desired date {desired_date.strftime('%m-%d-%Y')} is older than first recorded date {company_df.iloc[0].Date.strftime('%m-%d-%Y')}")
            raise ValueError
        dd_copy = desired_date
        
        if verbosity > 0:
            logger.debug(f"Your desired date is {desired_date.strftime('%m-%d-%Y')}")
        
        if len(company_df.loc[company_df['Date'] == desired_date]) != 0:
            desired_close = company_df.loc[company_df['Date'] == desired_date]
        else:    
            for i in range(1,100):
                if len(company_df.loc[company_df['Date'] == desired_date]) == 0:
                    desired_date = desired_date - dateutil.relativedelta.relativedelta(days=i)
                    desired_close = company_df.loc[company_df['Date'] == desired_date]
                break
            if verbosity > 0:
                logger.warning(f"Desired date: {dd_copy.strftime('%m-%d-%Y')} not found going for next possible date: {desired_date.strftime('%m-%d-%Y')}")
        return desired_date,desired_close.iloc[-1].Close
    
    
class DataRetrive:
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
    @staticmethod   
    def single_company(company_name: str,
                       start_date: datetime.datetime,
                       end_date: datetime.datetime, 
                       save: bool=False, 
                       export_path: str=None)->pd.DataFrame:
        """
        Retrive single company date from given start date and end

        Parameters
        ----------
        company_name : str
            name of desired company
        start_date : Tuple(year, month, day)
            Start date 
        end_date : Tuple(year, month, day)
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
        data = pdr.get_data_yahoo(company_name, start=start_date, end=end_date)
        
        if save is True:
            data.to_csv(f"{export_path}/{company_name}.csv")
        
        return data
    
        
        
class Indicator:
    
    def __init__(self, path: List):
        
        self.path = path

        if 'yaml' in os.path.split(self.path)[-1]:
            with open(self.path, 'r') as f:
                self.data = yaml.load(f)
        
    def volume_indicator_n_days(self, duration: int=90, 
                                export_path: str='.',
                                verbosity: int=1):
        
        end = datetime.datetime.now()
        start = end - dateutil.relativedelta.relativedelta(days=duration)
        vol_ind_df = pd.DataFrame(columns=['company','current date' ,'start date','current volume','mean volume','action'])
        for idx,company in  enumerate(self.data['company']):
            logger.info(f"Retriving data {idx + 1} out of {len(self.data['company'])} for {company}")
            company_df = DataRetrive.single_company(company_name=f"{company}.NS", start_date=start, end_date=end)
            buy_stock = company_df.iloc[-1].Volume > company_df['Volume'].mean()
            vol_ind_df = vol_ind_df.append({'company':company,
                                            'current date':company_df.index[-1].strftime('%m-%d-%Y'),
                                            'start date':company_df.index[0].strftime('%d-%m-%Y'),
                                            'current volume':company_df.iloc[-1].Volume,
                                            'mean volume':company_df['Volume'].mean(),
                                            'close price':company_df.iloc[-1].Close,
                                            'action':buy_stock},
                                        ignore_index=True)
        
        if verbosity > 0:
            logger.info(f"Here are sample 5 company\n{vol_ind_df.head()}\n remaining can be viewed at exported path")
        # vol_ind_df_true['company'].to_csv(f'{export_path}/VolumeIndicator90Days_{now_strting}.csv', index=False)
        vol_ind_df.to_csv(f"{export_path}/VolumeIndicator90Days_detailed_{now_strting}.csv", index=False)
    