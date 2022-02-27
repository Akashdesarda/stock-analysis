import os
import json
from deta import Deta
from tqdm import tqdm

# loading the sector wise company list which can be inserted into deta base
with open("./data/nifty500_secter_list.json") as f:
    sector_company_list = json.load(f)

# loading Nifty index wise company list which can be inserted into deta base
with open("./data/deta_nifty_index_list.json") as f:
    index_company_list = json.load(f)

# loading secrets
DETA_PROJECT_KEY = os.environ.get("DETA_PROJECT_KEY")
DETA_PROJECT_ID = os.environ.get("DETA_PROJECT_ID")

# creating Deta cloud client
deta_client = Deta(project_key=DETA_PROJECT_KEY, project_id=DETA_PROJECT_ID)

# creating Deta base table: nifty-index-company-db
nifty_index_db = deta_client.Base("nifty-index-company-db")
# creating Deta base table: nifty-sector-company-db
nifty_sector_db = deta_client.Base("nifty-sector-company-db")

# inserting nifty data in loop to Deta base as `put_many` has hard limitation of 25
for record in tqdm(index_company_list):
    nifty_index_db.put(record)
for record in tqdm(sector_company_list):
    nifty_sector_db.put(record)
