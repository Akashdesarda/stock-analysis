import os
from http import HTTPStatus
from typing import Union

from beanie import init_beanie
from beanie.odm.operators.update.general import Set
from dotenv import load_dotenv
from fastapi import FastAPI, Path
from motor.motor_asyncio import AsyncIOMotorClient

from stock_analysis.indicator import Indicator
from stock_analysis.momentum_strategy import MomentumStrategy
from stock_analysis.schema.api import *
from stock_analysis.schema.db import AsyncNiftyIndex, AsyncNiftySector

load_dotenv()
client = AsyncIOMotorClient(os.environ["MONGODB_CONNECTION_STRING"])


# FastAPI app init
app = FastAPI(
    title="Stock Analysis",
    description="An helping hand to identify & analyze stocks/company to invest",
    version="2.2",
)
# REST API for heal check
@app.get("/")
def _index():
    """Health check"""
    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
    }


# REST API for running algo strategy
@app.post("/api/momentum/relative-momentum/")
def relative_momentum(input_response: RelativeMomentum):
    """REST API for running relative-momentum algo strategy"""
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.relative_momentum(
        end_date=input_response.end_date,
        top_company_count=input_response.top_company_count,
        save=False,
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/momentum/relative-momentum-ema/")
def relative_momentum_ema(input_response: RelativeMomentumEMA):
    """REST API for running relative-momentum-ema algo strategy"""
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.relative_momentum_with_ema(
        end_date=input_response.end_date,
        top_company_count=input_response.top_company_count,
        ema_canditate=input_response.ema_candidate,
        save=False,
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/momentum/absolute-momentum-dma/")
def absolute_momentum_dma(input_response: AbsoluteMomentumDMA):
    """REST API for running absolute-momentum-dma algo strategy"""
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.absolute_momentum_with_dma(
        end_date=input_response.end_date,
        period=input_response.period,
        cutoff=input_response.cutoff,
        save=False,
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/indicator/volume-n-days/")
def volume_n_days(input_response: VolumeNDaysIndicator):
    """REST API for running volume-n-days algo strategy"""
    ind = Indicator(company_name=input_response.company)
    result = ind.volume_n_days_indicator(duration=input_response.duration, save=False)
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/indicator/ema-indicator-short/")
def ema_indicator_short(input_response: EMAIndicator):
    """REST API for running ema-indicator-short algo strategy"""
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_indicator(
        ema_canditate=input_response.ema_candidate,
        cutoff_date=input_response.cutoff_date,
        save=False,
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/indicator/ema-indicator-detail/")
def ema_indicator_detail(input_response: EMAIndicator):
    """REST API for running ema-indicator-detail algo strategy"""
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_detail_indicator(
        ema_canditate=input_response.ema_candidate,
        cutoff_date=input_response.cutoff_date,
        save=False,
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.post("/api/indicator/ema-crossover-indicator/")
def ema_crossover_indicator(input_response: EMACrossoverIndicator):
    """REST API for running ema-crossover-indicator algo strategy"""
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_crossover_detail_indicator(
        ema_canditate=input_response.ema_candidate, save=False
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


# REST API for performing CRUD ops on MongoDB
@app.get("/api/db/{collection}/{document_id}")
async def _db_get_document(collection: str, document_id: str):
    """REST API for for performing MongoDB CRUD Ops - GET a specific document from desired collection"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[AsyncNiftyIndex, AsyncNiftySector],
    )
    if collection == "nifty-index":
        return await AsyncNiftyIndex.get(document_id)
    if collection == "nifty-sector":
        return await AsyncNiftySector.get(document_id)


@app.post("/api/db/{collection}/query")
async def _db_find_documents(
    collection: str, query: dict, skip: int | None = None, limit: int | None = None
):
    """REST API for for performing MongoDB CRUD Ops - Find document(s) based on desired query"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[AsyncNiftyIndex, AsyncNiftySector],
    )
    if collection == "nifty-index":
        return await AsyncNiftyIndex.find_many(query).skip(skip).limit(limit).to_list()
    if collection == "nifty-sector":
        return await AsyncNiftySector.find_many(query).skip(skip).limit(limit).to_list()


@app.post("/api/db/nifty-index/insert")
async def _insert_document_nifty_index(documents: list[NiftyIndex]):
    """REST API for for performing MongoDB CRUD Ops - Insert/Add document nifty-index collection"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[AsyncNiftyIndex],
    )
    await AsyncNiftyIndex.insert_many(
        [AsyncNiftyIndex(**document.dict()) for document in documents]
    )
    return {"message": "OK"}


@app.post("/api/db/nifty-index/insert")
async def _insert_document_nifty_sector(documents: list[NiftySector]):
    """REST API for for performing MongoDB CRUD Ops - Insert/Add document nifty-index collection"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[NiftySector],
    )
    await AsyncNiftySector.insert_many(
        [AsyncNiftySector(**document.dict()) for document in documents]
    )
    return {"message": "OK"}


@app.delete("/api/db/{collection}/remove")
async def _delete_document(collection: str, query: dict):
    """REST API for for performing MongoDB CRUD Ops - Delete a document based on query"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[AsyncNiftyIndex, AsyncNiftySector],
    )
    if collection == "nifty-index":
        await AsyncNiftyIndex.find(query).delete()
    if collection == "nifty-sector":
        await AsyncNiftySector.find(query).delete()
    return {"message": "OK"}


@app.patch("/api/db/{collection}/update")
async def _update_document(collection: str, find_query: dict, update_query: dict):
    """REST API for for performing MongoDB CRUD Ops - Update desired document"""
    # Initialize beanie with the Product document class
    await init_beanie(
        database=client["stock-repo-db"],
        document_models=[AsyncNiftyIndex, AsyncNiftySector],
    )
    if collection == "nifty-index":
        await AsyncNiftyIndex.find(find_query).update(Set(update_query))
    if collection == "nifty-sector":
        await AsyncNiftySector.find(find_query).update(Set(update_query))
    return {"message": "OK"}
