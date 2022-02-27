from typing import Dict, List, Tuple, Union
from pydantic import BaseModel


class RelativeMomentum(BaseModel):
    """Request api model for relative momentum"""

    company: List[str]
    end_date: str
    top_company_count: int


class RelativeMomentumEMA(BaseModel):
    """Request api model for relative momentum with EMA"""

    company: List[str]
    end_date: str
    top_company_count: int
    ema_candidate: Tuple[int, int]


class AbsoluteMomentumDMA(BaseModel):
    """Request api model for absolute momentum with DMA"""

    company: List[str]
    period: int
    end_date: str
    cutoff: int


class VolumeNDaysIndicator(BaseModel):
    """Request api model for Volume N days indicator"""

    company: List[str]
    duration: int


class EMAIndicator(BaseModel):
    """Request api model for EMA indicator"""

    company: List[str]
    ema_candidate: Tuple[int, int]
    cutoff_date: str


class EMACrossoverIndicator(BaseModel):
    """Request api model for EMA crossover indicator"""

    company: List[str]
    ema_candidate: Tuple[int, int, int]


class DBGet(BaseModel):
    """Request api model for Deta Base `get` ops"""

    db_name: str
    key: str


class DBFetch(BaseModel):
    """Request api model for Deta Base `fetch` ops"""

    db_name: str
    query: Union[Dict, list]


class DBPut(BaseModel):
    """Request api model for Deta Base `put` & `put_many` ops"""

    db_name: str
    data: Union[Dict, List, str, int, bool]


class DBDelete(BaseModel):
    """Request api model for Deta Base `delete` ops"""

    db_name: str
    key: str
