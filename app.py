import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import yaml

from stock_analysis.indicator import Indicator
from stock_analysis.momentum_strategy import MomentumStrategy
from stock_analysis.custom_multi_indicator import CustomMultiIndicator

# Sidebar and task intros
default_intro = "# Welcome to Stock Analysis"
momentum_intro = "## This is used to perform Momentum strategy"
ind_intro = "## This is used to perform Indicator"
cus_mul_ind_intro = "This is used to perform Custom multichoice indicator"

st.set_page_config("Stock Analysis")
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

# Task for Momentum strategy
if task == "Momentum strategy":
    # TODO: Add more interaction by adding start/continue button
    # if st.button('Start'):
    company_name = st.text_input(
        "Directly give names of all Company",
        help="- Multiple company must be separated by ','. \n- Name must be listed symbol. \n- Eg. ADANIGREEN, HDFCAMC, WHIRLPOOL",
    )
    if company_name:
        company_list = list(map(lambda x: x.strip(), company_name.split(",")))
    st.write("OR")
    uploaded_file = st.file_uploader(
        label="Upload file containing company name(s)",
        type=["yml", "yaml", "json", "csv"],
    )

    if uploaded_file:
        if Path(uploaded_file.name).suffix == ".yaml":
            data = yaml.load(uploaded_file, Loader=yaml.FullLoader)
            company_list_select = st.selectbox(
                "select Stock index", options=list(data.keys())
            )
            company_list = data[company_list_select]
        elif Path(uploaded_file.name).suffix == ".csv":
            data = pd.read_csv(uploaded_file)
            company_list_select = st.selectbox(
                "select Stock index", options=data.columns.to_list()
            )
            company_list = data.loc[:, company_list_select].dropna().to_list()

    if company_name or uploaded_file:
        sa = MomentumStrategy(company_name=company_list)

    sub_task = st.selectbox(
        label="Choose sub task to perform",
        options=(
            "Select Options",
            "Relative momentum strategy",
            "Relative momentum strategy with EMA",
            "Absolute momentum strategy with DMA",
        ),
    )
    if sub_task == "Relative momentum strategy":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **Date**: today
    - **Top company count**: 20
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = sa.relative_momentum(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"momentum_result_{datetime.datetime.now().strftime('%d-%m-%Y')}_top_20.csv",
                )

        elif sub_task_mode == "Manual mode":
            sub_task_para_date = st.date_input(label="Input desire date")
            sub_task_para_date = sub_task_para_date.strftime("%d/%m/%Y")
            sub_task_para_count = st.number_input(
                label="Input top company count", value=20
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (
                (sub_task_para_date)
                and (sub_task_para_count)
                and (sub_task_para_verbosity) is not None
            ):
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **Date**: {sub_task_para_date}
    - **Top company count**: {sub_task_para_count}
    - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = sa.relative_momentum(
                            end_date=sub_task_para_date,
                            top_company_count=int(sub_task_para_count),
                            save=False,
                            verbosity=int(sub_task_para_verbosity),
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"momentum_result_{sub_task_para_date.replace('/','-')}_top_{sub_task_para_count}.csv",
                    )

    elif sub_task == "Relative momentum strategy with EMA":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **Date**: today
    - **Top company count**: 20
    - **EMA Candidate**: 50,200
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = sa.relative_momentum_with_ema(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"momentum_ema50-200_{datetime.datetime.now().strftime('%d-%m-%Y')}_top_20.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_date = st.date_input(label="Input desired")
            sub_task_para_date = str(sub_task_para_date.strftime("%d/%m/%Y"))
            sub_task_para_emacandidate1 = st.number_input(
                label=("Input desired first EMA candidate"), value=5
            )
            sub_task_para_emacandidate2 = st.number_input(
                label=("Input desired second EMA candidate"), value=200
            )
            sub_task_para_count = st.number_input(
                label="Input top company count", value=20
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (
                (sub_task_para_date)
                and (sub_task_para_count)
                and (sub_task_para_emacandidate1)
                and (sub_task_para_emacandidate2)
                and (sub_task_para_verbosity) is not None
            ):
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **Date**: {sub_task_para_date}
    - **EMA Candidate**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Top company count**: {sub_task_para_count}
    - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = sa.relative_momentum_with_ema(
                            end_date=sub_task_para_date,
                            top_company_count=sub_task_para_count,
                            ema_canditate=(
                                sub_task_para_emacandidate1,
                                sub_task_para_emacandidate2,
                            ),
                            save=False,
                            verbosity=sub_task_para_verbosity,
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"momentum_ema{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}_{sub_task_para_date.replace('/','-')}_top_{sub_task_para_count}.csv",
                    )

    elif sub_task == "Absolute momentum strategy with DMA":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **End date**: today
    - **Cutoff Percentage**: 5%
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = sa.absolute_momentum_with_dma(save=False)
                st.dataframe(result.astype("str"))
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"dma_action_cutoff_5_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_end_date = st.date_input(label="Input desire date")
            sub_task_para_end_date = sub_task_para_end_date.strftime("%d/%m/%Y")
            sub_task_para_cutoff = st.number_input(
                label="Input Cuttoff percentage", value=5
            )
            if (sub_task_para_end_date) and (sub_task_para_cutoff) is not None:
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **End date**: {sub_task_para_end_date}
    - **Cutoff Percentage**: {sub_task_para_cutoff}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = sa.absolute_momentum_with_dma(
                            end_date=sub_task_para_end_date,
                            cutoff=int(sub_task_para_cutoff),
                            save=False,
                        )
                    st.dataframe(result.astype("str"))
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"dma_action_cutoff_{sub_task_para_cutoff}_{sub_task_para_end_date.replace('/','-')}.csv",
                    )

# Task for Indicator
elif task == "Indicator":
    company_name = st.text_input(
        "Directly give names of all Company",
        help="- Multiple company must be separated by ','. \n- Name must be listed symbol. \n- Eg. ADANIGREEN, HDFCAMC, WHIRLPOOL",
    )
    if company_name:
        company_list = list(map(lambda x: x.strip(), company_name.split(",")))
    st.write("OR")
    uploaded_file = st.file_uploader(
        label="Upload file containing company name(s)",
        type=["yml", "yaml", "json", "csv"],
    )

    if uploaded_file:
        if Path(uploaded_file.name).suffix == ".yaml":
            data = yaml.load(uploaded_file, Loader=yaml.FullLoader)
            company_list_select = st.selectbox(
                "select Stock index", options=list(data.keys())
            )
            company_list = data[company_list_select]
        elif Path(uploaded_file.name).suffix == ".csv":
            data = pd.read_csv(uploaded_file)
            company_list_select = st.selectbox(
                "select Stock index", options=data.columns.to_list()
            )
            company_list = data.loc[:, company_list_select].dropna().to_list()

    if company_name or uploaded_file:
        ind = Indicator(company_name=company_list)

    sub_task = st.selectbox(
        label="Choose sub task to perform",
        options=(
            "Select Options",
            "Volume Indicator for [n] days",
            "Exponential moving average (short)",
            "Exponential moving average (detailed)",
            "Exponential moving average crossover",
        ),
    )
    if sub_task == "Volume Indicator for [n] days":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **Duration**: 90 days
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.volume_n_days_indicator(save=True)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"VolumeIndicator90Days_detailed_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_duration = st.number_input(
                label="Input desired duration", min_value=1, value=90
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (sub_task_para_duration) and (sub_task_para_verbosity) is not None:
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **Duration**: {sub_task_para_duration}
    - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = ind.volume_n_days_indicator(
                            duration=sub_task_para_duration,
                            save=False,
                            verbosity=sub_task_para_verbosity,
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"VolumeIndicator90Days_detailed_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

    elif sub_task == "Exponential moving average (short)":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **EMA Candidate**: 50,200 days
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_indicator50-200_{len(company_list)}_company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_emacandidate1 = st.number_input(
                label="Input desired first EMA candidate", value=5, step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label="Input desired second EMA candidate", value=200, step=1
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (
                (sub_task_para_emacandidate1)
                and (sub_task_para_emacandidate2)
                and (sub_task_para_verbosity) is not None
            ):
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = ind.ema_indicator(
                            ema_canditate=(
                                sub_task_para_emacandidate1,
                                sub_task_para_emacandidate2,
                            ),
                            save=False,
                            verbosity=sub_task_para_verbosity,
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"ema_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}_{len(company_list)}_company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

    elif sub_task == "Exponential moving average (detailed)":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
    **Following are the Default Parameters**
    - **EMA Candidate**: 50, 200 days
    - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_detail_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_detail_indicator50-200_{len(company_list)}_company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_emacandidate1 = st.number_input(
                label="Input desired first EMA candidate", value=5, step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label="Input desired second EMA candidate", value=200, step=1
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (
                (sub_task_para_emacandidate1)
                and (sub_task_para_emacandidate2)
                and (sub_task_para_verbosity) is not None
            ):
                st.markdown(
                    f"""
    **Following Parameters are given:**
    - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = ind.ema_detail_indicator(
                            ema_canditate=(
                                sub_task_para_emacandidate1,
                                sub_task_para_emacandidate2,
                            ),
                            save=False,
                            verbosity=sub_task_para_verbosity,
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"ema_detail_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}_{len(company_list)}_company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

    elif sub_task == "Exponential moving average crossover":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode")
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
            **Following are the Default Parameters**
            - **EMA Candidate**: 5, 13, 26 days
            - **Verbosity** (level of detail loging): detail """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_crossover_detail_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_crossover_detail_indicator5-13-26_{len(company_list)}company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                )
        elif sub_task_mode == "Manual mode":
            sub_task_para_emacandidate1 = st.number_input(
                label="Input desired first EMA candidate", value=5, step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label="Input desired second EMA candidate", value=13, step=1
            )
            sub_task_para_emacandidate3 = st.number_input(
                label="Input desired third EMA candidate", value=26, step=1
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (
                (sub_task_para_emacandidate1)
                and (sub_task_para_emacandidate2)
                and (sub_task_para_emacandidate3)
                and (sub_task_para_verbosity) is not None
            ):
                st.markdown(
                    f"""
                **Following Parameters are given:**
                - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}, {sub_task_para_emacandidate3}
                - **Verbosity**: {sub_task_para_verbosity}"""
                )
                if st.button("Continue"):
                    with st.spinner("Running the query"):
                        result = ind.ema_crossover_detail_indicator(
                            ema_canditate=(
                                sub_task_para_emacandidate1,
                                sub_task_para_emacandidate2,
                                sub_task_para_emacandidate3,
                            ),
                            save=False,
                            verbosity=sub_task_para_verbosity,
                        )
                    st.dataframe(result)
                    st.download_button(
                        "Download result",
                        data=result.to_csv(index=False).encode("utf-8"),
                        mime="text/csv",
                        file_name=f"ema_crossover_detail_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}-{sub_task_para_emacandidate3}_{len(company_list)}company_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

# Task for Multi choice indicator
elif task == "Multi choice Indicator":
    company_name = st.text_input(
        "Directly give names of all Company",
        help="- Multiple company must be separated by ','. \n- Name must be listed symbol. \n- Eg. ADANIGREEN, HDFCAMC, WHIRLPOOL",
    )
    if company_name:
        company_list = list(map(lambda x: x.strip(), company_name.split(",")))
    st.write("OR")
    uploaded_file = st.file_uploader(
        label="Upload file containing company name(s)",
        type=["yml", "yaml", "json", "csv"],
    )

    if uploaded_file:
        if Path(uploaded_file.name).suffix == ".yaml":
            data = yaml.load(uploaded_file, Loader=yaml.FullLoader)
            company_list_select = st.selectbox(
                "select Stock index", options=list(data.keys())
            )
            company_list = data[company_list_select]
        elif Path(uploaded_file.name).suffix == ".csv":
            data = pd.read_csv(uploaded_file)
            company_list_select = st.selectbox(
                "select Stock index", options=data.columns.to_list()
            )
            company_list = data.loc[:, company_list_select].dropna().to_list()

    if company_name or uploaded_file:
        multi_choice_ind = CustomMultiIndicator(company_name=company_list)

        # Multi select window
        options = st.multiselect(
            label="Please select desired indicator(s), You can select more than one",
            options=["daily moving average", "exponential moving average"],
        )
        # running query
        if st.button("Continue"):
            with st.spinner("Running the query"):
                result = multi_choice_ind.multi_choice_indicator(
                    indicators=options, save=False
                )
            st.dataframe(result.astype("str"))
            st.download_button(
                "Download result",
                data=result.to_csv(index=False).encode("utf-8"),
                mime="text/csv",
                file_name=f"multi_choice_indicator_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
            )
