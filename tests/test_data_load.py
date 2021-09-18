from pathlib import Path

import pandas as pd
import yaml
from stock_analysis.utils.logger import logger

data_path = (Path().cwd() / "data").as_posix()
logger = logger()


def test_yaml():
    logger.info("Loading")
    with open(f"{data_path}/sample_company.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    assert isinstance(data, dict), "Incorrect data"


def test_csv():
    data = pd.read_csv(f"{data_path}/sample_company.csv")

    assert isinstance(data, pd.DataFrame), "Incorrect data"


def test_company_name():
    logger.info("Loading")
    with open(f"{data_path}/sample_company.yaml", "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    assert isinstance(data["company"], list)
