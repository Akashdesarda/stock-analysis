from pathlib import Path

import pandas as pd
import streamlit as st
import yaml
from stock_analysis.utils.streamlit import (
    get_available_index,
    get_available_symbol_wrt_index,
    get_index_table,
    get_sector_table,
    manual_multi_choice,
)


def input_widget():
    """Streamlit widget/componet which is used to take desired input use

    Returns:
        List: symbol of companies based on selected input method
    """
    # NOTE - need to create a empty `company_list` as it will be populated eventually, but before need
    # to restrict showing error msg
    company_list = st.empty()

    # Main Input select category
    input_option = st.selectbox(
        "Select input method",
        (
            "Select Options",
            "Manual select company symbol",
            "Upload",
            "Curated Index",
            "Curated Sector",
            "Combination (Curated Index + Sector)",
        ),
    )

    # Input logic for Manual method
    if input_option == "Manual select company symbol":
        all_company_list = manual_multi_choice()
        company_list = st.multiselect("Select Company", all_company_list)

    # Input logic for File upload method
    if input_option == "Upload":
        uploaded_file = st.file_uploader(
            label="Upload file containing company symbol(s)",
            type=["yml", "yaml", "json", "csv"],
        )
        # logic for yaml file
        if uploaded_file:
            if Path(uploaded_file.name).suffix == ".yaml":
                data = yaml.load(uploaded_file, Loader=yaml.FullLoader)
                # NOTE - it can have more than one Index data, so allowing to select any one
                company_list_select = st.selectbox(
                    "Select Index", options=list(data.keys())
                )
                company_list = data[company_list_select]

                # logic for csv file
            elif Path(uploaded_file.name).suffix == ".csv":
                data = pd.read_csv(uploaded_file)
                # NOTE - it can have more than one Index data, so allowing to select any one
                company_list_select = st.selectbox(
                    "Select Index", options=data.columns.to_list()
                )
                company_list = data.loc[:, company_list_select].dropna().to_list()

    # NOTE -  adding nifty-sector-company-db & nifty-company-company-db into session to avoid multiple api call
    # Input logic for Index method
    if input_option == "Curated Index":
        # adding index table into session if not already present
        with st.spinner("Retriving data from the Database"):
            if "index_table" not in st.session_state:
                st.session_state["index_table"] = get_index_table()
        # multibox select widget for index
        selected_index = st.multiselect(
            "Select Index", get_available_index(st.session_state["index_table"]),
        )
        if selected_index:
            # filtering symbol for selected index(s)
            company_list = get_available_symbol_wrt_index(
                selected_index, st.session_state["index_table"]
            )

    # Input logic for Curated Sector method
    if input_option == "Curated Sector":
        # adding sector table into session if not already present
        with st.spinner("Retriving data from the Database"):
            if "sector_table" not in st.session_state:
                st.session_state["sector_table"] = get_sector_table()
        # multibox select widget for sector
        selected_sector = st.multiselect(
            "Select Sector", st.session_state["sector_table"]["Industry"].unique()
        )
        if selected_sector:
            # filtering symbol for selected sector/industry
            company_list = st.session_state["sector_table"][
                st.session_state["sector_table"]["Industry"].isin(selected_sector)
            ]["key"].to_list()

    # Input logic for combination method
    if input_option == "Combination (Curated Index + Sector)":
        with st.spinner("Retriving data from the Database"):
            # adding index table into session if not already present
            if "index_table" not in st.session_state:
                st.session_state["index_table"] = get_index_table()
            # adding sector table into session if not already present
            if "sector_table" not in st.session_state:
                st.session_state["sector_table"] = get_sector_table()

        # creating two columns for taking combine input
        index_column, sector_column = st.columns(2)

        # ops on index column
        with index_column:
            # multibox select widget for index
            selected_index = st.multiselect(
                "Select Index", get_available_index(st.session_state["index_table"]),
            )
            index_company_list = get_available_symbol_wrt_index(
                selected_index, st.session_state["index_table"]
            )

        # ops on sector column
        with sector_column:
            # multibox select widget for sector
            selected_sector = st.multiselect(
                "Select Sector", st.session_state["sector_table"]["Industry"].unique()
            )
            # if selected_sector:
            # filtering symbol for selected sector/industry
            sector_company_list = st.session_state["sector_table"][
                st.session_state["sector_table"]["Industry"].isin(selected_sector)
            ]["key"].to_list()
        company_list = list(set(index_company_list).intersection(sector_company_list))

    return company_list


def sidebar_widget() -> str:
    """Stremlit sidebar widget/component that is used for sidebar activity

    Returns:
        str: chosen sidebar option
    """
    # Sidebar and task intros
    default_intro = "# Welcome to Stock Analysis"
    momentum_intro = "## This is used to perform Momentum strategy"
    ind_intro = "## This is used to perform Indicator"
    cus_mul_ind_intro = "## This is used to perform Custom multichoice indicator"

    task = st.sidebar.selectbox(
        "Please select the task to start Stock Analysis",
        ("Home", "Momentum strategy", "Indicator", "Multi choice Indicator"),
    )
    st.sidebar.info("Select a task above")
    # st.title("Stock Analysis")
    if task == "Home":
        st.markdown(default_intro)
    elif task == "Momentum strategy":
        st.markdown(momentum_intro)
    elif task == "Indicator":
        st.markdown(ind_intro)
    elif task == "Multi choice Indicator":
        st.markdown(cus_mul_ind_intro)

    return task
