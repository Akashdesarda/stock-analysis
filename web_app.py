import streamlit as st
from stock_analysis.app.widget import sidebar_widget
from stock_analysis.app.momentum_strategy_page import momentum_strategy_sub_app
from stock_analysis.app.indicator_page import indicator_sub_app
from stock_analysis.app.custom_multi_indicator_page import (
    custom_multi_indicator_sub_app,
)

# adding sidebar widget
task = sidebar_widget()

if task == "Momentum strategy":
    # this will run all widgets w.r.t momentum strategy
    momentum_strategy_sub_app()
elif task == "Indicator":
    # this will run all widgets w.r.t Indicator
    indicator_sub_app()
elif task == "Multi choice Indicator":
    # this will run all widgets w.r.t Multi choice indicator
    custom_multi_indicator_sub_app()
