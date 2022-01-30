from stock_analysis.indicator import Indicator

company_list = [
    "BAJAJ",
    "ADANIGREEN",
    "HDFCAMC",
    "WHIRLPOOL",
    "ABB",
    "INDIAMART",
    "CENTRALBK",
    "CENTURYPLY",
]

ind = Indicator(company_name=company_list)


def test_ema_indicator():

    ema = ind.ema_indicator(save=False, verbosity=0)
    # Check for columns
    assert len(ema.columns) == 7, "Incorrect no of columns"

    # Check for null value
    for key, val in ema.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"


def test_ema_detail_indicator():

    ema_detail = ind.ema_detail_indicator(save=False, verbosity=0)
    # Check for correct order of columns
    c = [
        "company",
        "ema_date",
        "ema50",
        "ema200",
        "percentage_diff",
        "outcome",
        "action",
        "longName",
        "price",
        "regularMarketVolume",
        "marketCap",
        "bookValue",
        "priceToBook",
        "averageDailyVolume3Month",
        "averageDailyVolume10Day",
        "fiftyTwoWeekLowChange",
        "fiftyTwoWeekLowChangePercent",
        "fiftyTwoWeekRange",
        "fiftyTwoWeekHighChange",
        "fiftyTwoWeekHighChangePercent",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
    ]
    assert c == list(ema_detail.columns), "Either less or misplaced columns"
    # Check for null value
    for key, val in ema_detail.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"


def test_ema_crossover():

    ema_cross = ind.ema_crossover_detail_indicator(save=False, verbosity=0)

    # Check for correct order of columns
    c = [
        "company",
        "ema_date",
        "ema5",
        "ema13",
        "ema26",
        "action",
        "longName",
        "price",
        "regularMarketVolume",
        "marketCap",
        "bookValue",
        "priceToBook",
        "averageDailyVolume3Month",
        "averageDailyVolume10Day",
        "fiftyTwoWeekLowChange",
        "fiftyTwoWeekLowChangePercent",
        "fiftyTwoWeekRange",
        "fiftyTwoWeekHighChange",
        "fiftyTwoWeekHighChangePercent",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
    ]
    assert c == list(ema_cross.columns), "Either less or misplaced columns"
    # Check for null value
    for key, val in ema_cross.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"
