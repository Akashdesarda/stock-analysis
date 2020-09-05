import yfinance as yf
import os
import yaml
import datetime
import dateutil
import pandas as pd
from stock_analysis.utils.logger import logger
from stock_analysis.data_retrive import DataRetrive
from typing import List, Union, Tuple
now_strting = datetime.datetime.now().strftime('%d-%m-%Y')

yf.pdr_override()
logger = logger()
pd.options.display.float_format = '{:,.2f}'.format
   
    
class Indicator:
    """Perform all variety of Indicator operation 
    """    

    def __init__(self, path: str = None, company_name: List = None):
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
            if 'yaml' in os.path.split(self.path)[-1]:
                with open(self.path, 'r') as f:
                    self.data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            self.data = {'company':self.company_name}

    def volume_indicator_n_days(self, duration: int = 90,
                                save:bool=True,
                                export_path: str = '.',
                                verbosity: int = 1):

        end = datetime.datetime.now()
        start = end - dateutil.relativedelta.relativedelta(days=duration)
        vol_ind_df = pd.DataFrame(columns=[
                                  'company', 'current date', 'start date', 'current volume', 'mean volume', 'action'])
        for idx, company in enumerate(self.data['company']):
            logger.info(
                f"Retriving data {idx + 1} out of {len(self.data['company'])} for {company}")
            company_df = DataRetrive.single_company_specific(
                company_name=f"{company}.NS", start_date=start, end_date=end)
            buy_stock = company_df.iloc[-1].Volume > company_df['Volume'].mean()
            vol_ind_df = vol_ind_df.append({'company': company,
                                            'current date': company_df.index[-1].strftime('%d-%m-%Y'),
                                            'start date': company_df.index[0].strftime('%d-%m-%Y'),
                                            'current volume': company_df.iloc[-1].Volume,
                                            'mean volume': company_df['Volume'].mean(),
                                            'close price': company_df.iloc[-1].Close,
                                            'action': buy_stock},
                                           ignore_index=True)

        if verbosity > 0:
            logger.debug(
                f"Here are sample 5 company\n{vol_ind_df.head()}\n remaining can be viewed at exported path")
        # vol_ind_df_true['company'].to_csv(f'{export_path}/VolumeIndicator90Days_{now_strting}.csv', index=False)
        if save is True:
            vol_ind_df.to_csv(
                f"{export_path}/VolumeIndicator90Days_detailed_{now_strting}.csv", index=False)
            if verbosity > 0:
                logger.debug(
                    f"Save at {export_path}/VolumeIndicator90Days_detailed_{now_strting}.csv")

    def ema_indicator(self, ema_canditate: Tuple[int, int] = (50, 200),
                      cutoff_date: Union[str,datetime.datetime]='today',
                      save: bool=True,
                      export_path: str = '.',
                      verbosity: int = 1):

        invalid = []
        ema_indicator_df = pd.DataFrame(columns=[
                                        'company', f'ema{str(ema_canditate[0])}', f'ema{str(ema_canditate[1])}', 'action'])
        for idx, company in enumerate(self.data['company']):
            logger.info(
                f"Retriving data {idx + 1} out of {len(self.data['company'])} for {company}")
            company_df = DataRetrive.single_company_complete(
                company_name=f"{company}.NS")
            if company_df['Close'].isnull().sum() != 0:
                logger.warning(f"{company} have some missing value, fixing it")
                company_df.dropna(inplace=True)
            try:
                ema_A = self._exponential_moving_avarage(
                    data_df=company_df,
                    cutoff_date=cutoff_date,
                    period=50)
                ema_B = self._exponential_moving_avarage(
                    data_df=company_df,
                    cutoff_date=cutoff_date,
                    period=200)
                if ema_A > ema_B:
                    action = 'buy'
                else:
                    action = 'sell'
                ema_indicator_df = ema_indicator_df.append({'company': company,
                                                            f'ema{str(ema_canditate[0])}': ema_A,
                                                            f'ema{str(ema_canditate[1])}': ema_B,
                                                            'action': action},
                                                           ignore_index=True)
            except Exception as e:
                print(company, e)
                invalid.append(company)
                logger.warning(
                    f"{', '.join(invalid)} has less record than minimum rexquired")

        if verbosity > 0:
            logger.debug(
                f"Here are sample 5 company\n{ema_indicator_df.head()}\n remaining can be viewed at exported path")
        if save is True:
            ema_indicator_df.to_csv(
            f"{export_path}/ema_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv", index=False)    
            if verbosity > 0:
                logger.debug(
                    f"Exported at {export_path}/ema_indicator{str(ema_canditate[0])}-{str(ema_canditate[1])}_{len(self.data['company'])}company_{now_strting}.csv")

        return ema_indicator_df

    def _exponential_moving_avarage(self, 
                                    data_df: Union[pd.Series, List],
                                    period: int,
                                    cutoff_date: Union[str,datetime.datetime]='today',
                                    smoothing_factor: int = 2) -> float:
        """Calculate exponential moving avarage based on given period

        Parameters
        ----------
        data : Union[pd.Series,List]
            Data to calculate ema
        period : int
            Period for which ema has to be calculated
        smoothing_factor : int, optional
            Smoothing factor which will be used to calculate Multiplying factor, by default 2

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
        data_df['ema'] =[pd.NA] * (len(data_df) - len(ema_list)) + ema_list
        if cutoff_date == 'today':
            date = data_df.index[-1]
        else:
            date = self._get_appropriate_date(
                company_df=data_df,
                desired_date=cutoff_date
            )
        
        return float(data_df[data_df.index == date]['ema'])
    
    def _get_appropriate_date(self, 
                              company_df: pd.DataFrame,
                              desired_date  : datetime.datetime,
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
        raise ValueError
        
        
        if verbosity > 0:
            logger.debug(
                f"Your desired date is {desired_date.strftime('%d-%m-%Y')}")
    
        for day_idx in range(1,100):
            if desired_date not in company_df.index:
                date = desired_date - dateutil.relativedelta.relativedelta(days=day_idx)
            else:
                date = desired_date
            if date in company_df.index:
                break
        if verbosity > 0 and desired_date != date:
                logger.warning(
                    f"Desired date: {desired_date.strftime('%d-%m-%Y')} not found going for next possible date: {date.strftime('%d-%m-%Y')}")
        
        return date
