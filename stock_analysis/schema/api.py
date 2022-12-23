from typing import Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Field


class RelativeMomentum(BaseModel):
    """Request api model for relative momentum"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    end_date: str = Field(
        ...,
        description="either 'today' for current date or dd/mm/yyyy format",
        example="today",
    )
    top_company_count: int = Field(
        ..., description="after sorting total company to retrive", example=3
    )


class RelativeMomentumEMA(BaseModel):
    """Request api model for relative momentum with EMA"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    end_date: str = Field(
        ...,
        description="either 'today' for current date or dd/mm/yyyy format",
        example="today",
    )
    top_company_count: int = Field(
        ..., description="after sorting total company to retrive", example=3
    )
    ema_candidate: Tuple[int, int] = Field(
        ...,
        description="2 EMA candidate that will be used for calculating EMA",
        example=[5, 20],
    )


class AbsoluteMomentumDMA(BaseModel):
    """Request api model for absolute momentum with DMA"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    period: int
    end_date: str = Field(
        ...,
        description="either 'today' for current date or dd/mm/yyyy format",
        example="today",
    )
    cutoff: int = Field(
        ..., description="Desired cutoff to determine action", example=5
    )


class VolumeNDaysIndicator(BaseModel):
    """Request api model for Volume N days indicator"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    duration: int = Field(
        ..., description="Total days from current date to retrive data", example=90
    )


class EMAIndicator(BaseModel):
    """Request api model for EMA indicator"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    ema_candidate: Tuple[int, int] = Field(
        ...,
        description="2 EMA candidate that will be used for calculating EMA",
        example=[5, 20],
    )
    cutoff_date: str = Field(
        ...,
        description="Desired date till which to calculate ema. Either 'today' for current date or dd/mm/yyyy format",
        example="today",
    )


class EMACrossoverIndicator(BaseModel):
    """Request api model for EMA crossover indicator"""

    company: List[str] = Field(
        ...,
        description="List of company symbol",
        example=["ADANIGREEN", "HDFCAMC", "WHIRLPOOL", "APLAPOLLO", "LALPATHLAB"],
    )
    ema_candidate: Tuple[int, int, int] = Field(
        ..., description="Three Period (or days) to calculate EMA", example=[5, 13, 26]
    )


class DBGet(BaseModel):
    """Request api model for Deta Base `get` ops"""

    db_name: str = Field(
        ..., description="name of the database", example="nifty-index-company-db"
    )
    key: str = Field(..., description="key to perform ops", example="TCS")


class DBFetch(BaseModel):
    """Request api model for Deta Base `fetch` ops"""

    db_name: str = Field(
        ..., description="name of the database", example="nifty-index-company-db"
    )
    query: Optional[Union[Dict, list]] = Field(
        None, description="query to fetch data", example={"Industry": "IT"}
    )


class DBPut(BaseModel):
    """Request api model for Deta Base `put` & `put_many` ops"""

    db_name: str = Field(..., description="name of the database", example="dummy-db")
    data: Union[Dict, List, str, int, bool] = Field(
        ...,
        description="data to write to db",
        example={"key": "TCS", "Nifty50": True, "Nifty500": True},
    )


class DBDelete(BaseModel):
    """Request api model for Deta Base `delete` ops"""

    db_name: str = Field(..., description="name of the database", example="dummy-db")
    key: str = Field(..., description="key to perform ops", example="TCS")
