from stock_analysis.custom_multi_indicator import CustomMultiIndicator

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

cus_mul_ind = CustomMultiIndicator(company_name=company_list)


def test_single_indicator():

    mul_ind_dma = cus_mul_ind.multi_choice_indicator(
        indicators=["daily moving average"], save=False
    )

    # Check for columns
    assert len(mul_ind_dma.columns) == 4, "Incorrect no of columns in dma"

    mul_ind_ema = cus_mul_ind.multi_choice_indicator(
        indicators=["exponential moving average"], save=False
    )

    # Check for columns
    assert len(mul_ind_ema.columns) == 4, "Incorrect no of columns in ema"


def test_multi_indicator():
    indicators = ["daily moving average", "exponential moving average"]
    mul_ind = cus_mul_ind.multi_choice_indicator(indicators=indicators, save=False)

    # Check for columns
    assert len(mul_ind.columns) == 2 + (len(indicators) * 2), "Incorrect no of columns"

    # Check for null value
    for key, val in mul_ind.isna().sum().to_dict().items():
        assert val == 0, f"Found Null value in {key}"
