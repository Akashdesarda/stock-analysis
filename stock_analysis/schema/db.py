import beanie
import bunnet
from pydantic import BaseModel


class NiftyIndex(bunnet.Document):
    symbol: bunnet.Indexed(str)
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


class NiftySector(bunnet.Document):
    symbol: bunnet.Indexed(str)
    company_name: str
    isin_code: str
    industry: bunnet.Indexed(str)
    series: str

    class Settings:
        name = "nifty-sector"


class AsyncNiftyIndex(beanie.Document):
    symbol: beanie.Indexed(str)
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


class AsyncNiftySector(beanie.Document):
    symbol: beanie.Indexed(str)
    company_name: str
    isin_code: str
    industry: beanie.Indexed(str)
    series: str

    class Settings:
        name = "nifty-sector"


class ProjectSymbol(BaseModel):
    symbol: str


class ProjectionIndustry(BaseModel):
    industry: str
