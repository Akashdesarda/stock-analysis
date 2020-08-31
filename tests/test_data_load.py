import os
import yaml
from stock_analysis.utils.logger import logger

data_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','data'))
logger = logger()

def test_yaml():
    logger.info("Loading")
    with open(f'{data_path}/sample_company.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        
    assert isinstance(data,dict), 'Incorrect data'
    
def test_company_name():
    logger.info("Loading")
    with open(f'{data_path}/sample_company.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    assert isinstance(data['company'], list)