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
        end_date="01/01/2022", top_company_count=3, save=False, verbosity=0
    )

    check_date_columns = [
        "price (01-01-2021)",
        "price (31-12-2021)",
        "price (30-11-2021)",
    ]

    for column in check_date_columns:
        assert column in mom.columns, "Invalid or missing date based column(s)"


def test_momentum_strategy_with_ema():

    mom_ema = ut.relative_momentum_with_ema(
        top_company_count=3, save=False, verbosity=0
    )

    assert len(mom_ema.columns) == 10, "Incorrect columns"

    # Check for null value
    for key, val in mom_ema.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"


def test_momentum_strategy_with_ema_and_date():

    mom_ema = ut.relative_momentum_with_ema(
        end_date="01/01/2022", top_company_count=3, save=False, verbosity=0
    )

    check_date_columns = [
        "price (01-01-2021)",
        "price (31-12-2021)",
        "price (30-11-2021)",
    ]

    for column in check_date_columns:
        assert column in mom_ema.columns, "Invalid or missing date based column(s)"


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
