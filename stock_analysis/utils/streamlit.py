"""Packs all the utilities need while creating streamlit web app"""
from itertools import chain
from typing import List, Optional

import pandas as pd
import streamlit as st
from stock_analysis.api import http_request
from stock_analysis.utils.helpers import unique_list


@st.cache(show_spinner=False)
def manual_multi_choice() -> List[str]:
    """fetch all the available symbol from index db

    Returns:
        List[str]: all available symbol
    """
    # extract all company symbol using rest api
    # EG - response_data = [{...,"key":"xyz"},{...,"key":"xyz"},...,{...,"key":"xyz"}]
    response_data = http_request(
        "db/fetch", "get", {"db_name": "nifty-index-company-db", "query": None}
    )
    company_symbol_list = [
        response_data[idx]["key"] for idx, _ in enumerate(response_data)
    ]
    return company_symbol_list


@st.cache(show_spinner=False)
def get_available_index(index_table: Optional[List] = None) -> set:
    """extract available indexes 

    Args:
        index_table (Optional[List], optional): response data having complete Index table.
        Defaults to None.

    Returns:
        set: Index table
    """
    if index_table is None:
        response_data = http_request(
            "db/fetch", "get", {"db_name": "nifty-index-company-db", "query": None}
        )
        indexes = set(chain.from_iterable(response_data))

        # removing 'key' as it is not an index
        indexes.remove("key")
        return indexes
    else:
        indexes = set(chain.from_iterable(index_table))

        # removing 'key' as it is not an index
        indexes.remove("key")
        return indexes


@st.cache(show_spinner=False)
def get_available_symbol_wrt_index(
    indexes: List[str], index_table: Optional[List] = None
) -> List:
    """extract symbol based on provided Index

    Args:
        indexes (List[str]): desired indexses
        index_table (Optional[List], optional): response data having complete Index table.
        Defaults to None.

    Returns:
        List: symbol(s) based on desired indexes
    """
    if index_table is None:
        response_data = http_request(
            "db/fetch",
            "get",
            {
                "db_name": "nifty-index-company-db",
                "query": {index: True for index in indexes},
            },
        )
        return [unit_response["key"] for unit_response in response_data]
    else:
        symbol_list = []
        for unit_response in index_table:
            for index in indexes:
                if index in unit_response:
                    symbol_list.append(unit_response["key"])
        return unique_list(symbol_list)


@st.cache(show_spinner=False)
def get_available_sector() -> set:
    """get the available sector/industry from db server api

    Returns:
        List: available sector(s)
    """
    response_data = http_request(
        "db/fetch", "get", {"db_name": "nifty-sector-company-db", "query": None}
    )
    return set([unit_response["Industry"] for unit_response in response_data])


@st.cache(show_spinner=False)
def get_sector_table() -> pd.DataFrame:
    """get the sector table from db server api

    Returns:
        List: sector data table
    """
    response_data = http_request(
        "db/fetch", "get", {"db_name": "nifty-sector-company-db", "query": None}
    )
    return pd.DataFrame(response_data)


@st.cache(show_spinner=False)
def get_index_table() -> List:
    """fet the index table from db server api

    Returns:
        List: index data table
    """
    return http_request(
        "db/fetch", "get", {"db_name": "nifty-index-company-db", "query": None}
    )
