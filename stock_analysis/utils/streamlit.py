"""Packs all the utilities need while creating streamlit web app"""
import pandas as pd
import streamlit as st
from bunnet import init_bunnet
from pymongo import MongoClient

from stock_analysis.schema.db import *
from stock_analysis.utils.helpers import unique_list

# creating async client
client = MongoClient(st.secrets["MONGODB_CONNECTION_STRING"])

# Initialize beanie
# NOTE - db name is stock-repo-db & document_models will eventually become collection
init_bunnet(database=client["stock-repo-db"], document_models=[NiftyIndex, NiftySector])


@st.cache(show_spinner=False)
def manual_multi_choice() -> list[str]:
    """fetch all the available symbol from index db

    Returns:
        list[str]: all available symbol
    """
    nifty_index_data = NiftyIndex.find_all().project(ProjectSymbol).to_list()
    company_symbol_list = [i.symbol for i in nifty_index_data]
    return company_symbol_list


@st.cache(show_spinner=False)
def get_available_index() -> list[str]:
    """extract available indexes

    Args:
        index_table (Optional[list], optional): response data having complete Index table.
        Defaults to None.

    Returns:
        set: Index table
    """
    properties = NiftyIndex.schema()["properties"]
    # removing not needed keys
    del properties["_id"], properties["symbol"]
    return list(properties.keys())


@st.cache(show_spinner=False)
def get_available_symbol_wrt_index(
    indexes: list[str],
) -> list:
    """extract all symbols based on provided Index(s)

    Args:
        indexes (list[str]): desired indexses

    Returns:
        list: symbol(s) based on desired indexes
    """
    symbol_query_result = NiftyIndex.find_many(
        {index: True for index in indexes}
    ).project(ProjectSymbol)
    symbol_list = [i.symbol for i in symbol_query_result]
    return unique_list(symbol_list)


@st.cache(show_spinner=False)
def get_available_sector() -> set:
    """get the available sector/industry from db server api

    Returns:
        list: available sector(s)
    """
    return NiftySector.distinct(NiftySector.industry)


@st.cache(show_spinner=False)
def get_sector_table() -> pd.DataFrame:
    """get the sector table from db server api

    Returns:
        list: sector data table
    """

    return pd.DataFrame(i.dict(exclude={"id"}) for i in NiftySector.find_all())
