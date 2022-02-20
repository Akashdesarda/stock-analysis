from fastapi import FastAPI

from stock_analysis.momentum_strategy import MomentumStrategy
from stock_analysis.indicator import Indicator
from stock_analysis.api.request_models import *

app = FastAPI()


@app.post("/api/momentum/relative-momentum/")
def relative_momentum(input_response: RelativeMomentum):
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.relative_momentum(
        end_date=input_response.end_date,
        top_company_count=input_response.top_company_count,
        save=False,
    )
    result = result.set_index("symbol").T
    return result


@app.post("/api/momentum/relative-momentum-ema/")
def relative_momentum_ema(input_response: RelativeMomentumEMA):
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.relative_momentum_with_ema(
        end_date=input_response.end_date,
        top_company_count=input_response.top_company_count,
        ema_canditate=input_response.ema_candidate,
        save=False,
    )
    result = result.set_index("symbol").T
    return result


@app.post("/api/momentum/absolute-momentum-dma/")
def absolute_momentum_dma(input_response: AbsoluteMomentumDMA):
    ms = MomentumStrategy(company_name=input_response.company)
    result = ms.absolute_momentum_with_dma(
        end_date=input_response.end_date,
        period=input_response.period,
        cutoff=input_response.cutoff,
        save=False,
    )
    result = result.set_index("symbol").T
    return result


@app.post("/api/indicator/volume-n-days/")
def volume_n_days(input_response: VolumeNDaysIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.volume_n_days_indicator(duration=input_response.duration, save=False)
    result = result.set_index("symbol").T
    return result


@app.post("/api/indicator/ema-indicator-short/")
def ema_indicator_short(input_response: EMAIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_indicator(
        ema_canditate=input_response.ema_candidate,
        cutoff_date=input_response.cutoff_date,
        save=False,
    )
    result = result.set_index("symbol").T
    return result


@app.post("/api/indicator/ema-indicator-detail/")
def ema_indicator_detail(input_response: EMAIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_detail_indicator(
        ema_canditate=input_response.ema_candidate,
        cutoff_date=input_response.cutoff_date,
        save=False,
    )
    result = result.set_index("symbol").T
    return result


@app.post("/api/indicator/ema-crossover-indicator/")
def ema_crossover_indicator(input_response: EMACrossoverIndicator):
    ind = Indicator(company_name=input_response.company)
    result = ind.ema_crossover_detail_indicator(
        ema_canditate=input_response.ema_candidate, save=False
    )
    result = result.set_index("symbol").T
    return result
