from fastapi import FastAPI

from stock_analysis.api.request_models import *
from stock_analysis.indicator import Indicator
from stock_analysis.momentum_strategy import MomentumStrategy
from stock_analysis.utils.helpers import create_chunks, deta_base_client

app = FastAPI()  # FastAPI app init

# REST API for running algo strategy
@app.get("/api/momentum/relative-momentum/")
def relative_momentum(input_response: RelativeMomentum):
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


@app.get("/api/momentum/relative-momentum-ema/")
def relative_momentum_ema(input_response: RelativeMomentumEMA):
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


@app.get("/api/momentum/absolute-momentum-dma/")
def absolute_momentum_dma(input_response: AbsoluteMomentumDMA):
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


@app.get("/api/indicator/volume-n-days/")
def volume_n_days(input_response: VolumeNDaysIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.volume_n_days_indicator(duration=input_response.duration, save=False)
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


@app.get("/api/indicator/ema-indicator-short/")
def ema_indicator_short(input_response: EMAIndicator):
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


@app.get("/api/indicator/ema-indicator-detail/")
def ema_indicator_detail(input_response: EMAIndicator):
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


@app.get("/api/indicator/ema-crossover-indicator/")
def ema_crossover_indicator(input_response: EMACrossoverIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_crossover_detail_indicator(
        ema_canditate=input_response.ema_candidate, save=False
    )
    # NOTE - by default result is return as dataframe's index as keys so changing it to symbol
    result = result.set_index(
        "symbol"
    ).T  # need to perform `transpose` to match expected output
    return result


# REST API for performing CRUD ops on Deta Base db
# NOTE - `get` can be used to read/fetch/pull based on just `key`
@app.get("/api/db/get/")
def db_get(input_response: DBGet):
    db_client = deta_base_client(input_response.db_name)
    return db_client.get(input_response.key)


# NOTE - `fetch` can be used to retrive data based on Deta base compatible query
@app.get("/api/db/fetch/")
def db_fetch(input_response: DBFetch):
    db_client = deta_base_client(input_response.db_name)
    return db_client.fetch(input_response.query).items


# NOTE - `put` can be used for insert as well as update
@app.put("/api/db/put/")
def db_put(input_response: DBPut):
    db_client = deta_base_client(input_response.db_name)
    # since data is list then we can use `put_many` to speedup the ops
    if isinstance(input_response.data, list):
        if len(input_response.data) <= 25:
            db_client.put_many(input_response.data)
        else:
            # NOTE - Deta has hard limit of 25 for `put_many`. So need to create chunks of 25 element of
            # data so that we can still use `put_many`
            chunked_data = create_chunks(input_response.data, 25)
            for unit_chunk in chunked_data:
                db_client.put_many(unit_chunk)
    else:
        db_client.put(input_response.data)


# NOTE - the `delete` ops take place at `key` level so only key is required
@app.delete("/api/db/delete/")
def db_delete(input_response: DBDelete):
    db_client = deta_base_client(input_response.db_name)
    return db_client.delete(input_response.key)