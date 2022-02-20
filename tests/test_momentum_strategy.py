from stock_analysis.momentum_strategy import MomentumStrategy
import datetime

now_strting = datetime.datetime.now().strftime("%d-%m-%Y")
company_list = [
    "ADANIGREEN",
    "HDFCAMC",
    "WHIRLPOOL",
    "BAJAJ",
    "ABCXYZ",
    "ABB",
    "INDIAMART",
    "CENTRALBK",
    "CENTURYPLY",
]

ut = MomentumStrategy(company_name=company_list)


def test_relative_momentum():

    mom = ut.relative_momentum(top_company_count=3, save=False, verbosity=0)

    # Check for columns
    assert len(mom.columns) == 7, "Incorrect columns"

    # Check for null value
    for key, val in mom.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"


def test_relative_momentum_date():

    mom = ut.relative_momentum(
        end_date="01/01/2020", top_company_count=3, save=False, verbosity=0
    )

    yearly_start_date = list(mom["yearly_start_date"])
    yearly_end_date = list(mom["yearly_end_date"])
    monthly_start_date = list(mom["monthly_start_date"])
    monthly_end_date = list(mom["monthly_end_date"])

    check_yearly_start_date = ["01-01-2019", "01-01-2019", "01-01-2019"]
    check_yearly_end_date = ["31-12-2019", "31-12-2019", "31-12-2019"]
    check_monthly_start_date = ["29-11-2019", "29-11-2019", "29-11-2019"]
    check_monthly_end_date = ["31-12-2019", "31-12-2019", "31-12-2019"]

    assert check_yearly_start_date == yearly_start_date, "Invalid yearly start date"
    assert check_yearly_end_date == yearly_end_date, "Invalid yearly end date"
    assert check_monthly_start_date == monthly_start_date, "Invalid monthly start date"
    assert check_monthly_end_date == monthly_end_date, "Invalid monthly end date"


def test_momentum_strategy_with_ema():

    mom_ema = ut.relative_momentum_with_ema(
        top_company_count=3, save=False, verbosity=0
    )

    assert len(mom_ema.columns) == 17, "Incorrect columns"

    # Check for null value
    for key, val in mom_ema.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"


def test_momentum_strategy_with_date():

    mom_ema = ut.relative_momentum_with_ema(
        end_date="01/01/2020", top_company_count=3, save=False, verbosity=0
    )

    yearly_start_date = list(mom_ema["yearly_start_date"])
    yearly_end_date = list(mom_ema["yearly_end_date"])
    monthly_start_date = list(mom_ema["monthly_start_date"])
    monthly_end_date = list(mom_ema["monthly_end_date"])

    check_yearly_start_date = ["01-01-2019", "01-01-2019", "01-01-2019"]
    check_yearly_end_date = ["31-12-2019", "31-12-2019", "31-12-2019"]
    check_monthly_start_date = ["29-11-2019", "29-11-2019", "29-11-2019"]
    check_monthly_end_date = ["31-12-2019", "31-12-2019", "31-12-2019"]

    assert check_yearly_start_date == yearly_start_date, "Invalid yearly start date"
    assert check_yearly_end_date == yearly_end_date, "Invalid yearly end date"
    assert check_monthly_start_date == monthly_start_date, "Invalid monthly start date"
    assert check_monthly_end_date == monthly_end_date, "Invalid monthly end date"


def test_dma():
    dma_with_per = ut.absolute_momentum_with_dma()
    # Check for correct order of columns

    c = [
        "symbol",
        "company",
        f"price ({now_strting})",
        "sma",
        "ideal buy",
        "ideal sell",
        "turnover in cr.",
        "action",
    ]
    assert c == list(dma_with_per.columns), "Either less or misplaced columns"
    # Check for null value
    for key, val in dma_with_per.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"
