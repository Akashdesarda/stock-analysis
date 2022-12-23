from bunnet import Document, Indexed
from pydantic import BaseModel


class NiftyIndex(Document):
    symbol: Indexed(str)
    Nifty50: bool = False
    Nifty100: bool = False
    Nifty200: bool = False
    Nifty500: bool = False
    NiftySmallcap50: bool = False
    NiftySmallcap250: bool = False
    NiftyMidcap50: bool = False
    NiftyMidcap150: bool = False
    NiftyMidcap400: bool = False
    NiftyNext50: bool = False

    class Settings:
        name = "nifty-index"


class NiftySector(Document):
    symbol: Indexed(str)
    company_name: str
    isin_code: str
    industry: Indexed(str)
    series: str

    class Settings:
        name = "nifty-sector"


class ProjectSymbol(BaseModel):
    symbol: str


class ProjectionIndustry(BaseModel):
    industry: str
