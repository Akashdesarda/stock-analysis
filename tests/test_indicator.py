from stock_analysis.indicator import Indicator

company_list = ['ADANIGREEN','HDFCAMC','WHIRLPOOL']

ind = Indicator(company_name=company_list)

def test_ema_indicator():
    
    ema = ind.ema_indicator(
        save=False,
        verbosity=0
    )
    # Check for columns
    assert len(ema.columns) == 6, 'Incorrect column'
    
    # Check for null value
    for key,val in ema.isna().sum().to_dict().items():
        assert val == 0, f'Found Null value in {key}'

def ema_indicator_detail():
    
    ema_detail = ind.ema_indicator_detail(
        save=False,
        verbosity=0
    )
    # Check for correct order of columns
    c = ['company', 'ema50', 'ema200', 'ratio', 'outcome', 'action', 'longName', 'price', 'regularMarketVolume', 'marketCap', 'bookValue', 'priceToBook', 'averageDailyVolume3Month', 'averageDailyVolume10Day', 'fiftyTwoWeekLowChange', 'fiftyTwoWeekLowChangePercent', 'fiftyTwoWeekRange', 'fiftyTwoWeekHighChange', 'fiftyTwoWeekHighChangePercent', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh']
    assert c == list(ema_detail.columns), 'Either less or misplaced columns'
    # Check for null value
    for key,val in ema_detail.isna().sum().to_dict().items():
        assert val == 0, f'Found Null value in {key}'
