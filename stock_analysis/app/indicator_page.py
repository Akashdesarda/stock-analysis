import datetime

import streamlit as st
from stock_analysis.app.widget import input_widget

from stock_analysis.indicator import Indicator


def indicator_sub_app():
    """It creates a streamlit sub page for Indicator
    """
    try:
        company_symbol_list = input_widget()
        with st.expander("See the selected Company symbol based on chosen criteria"):
            st.write(company_symbol_list)
    except:
        pass

    if company_symbol_list:
        ind = Indicator(company_name=company_symbol_list)

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
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode"),
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
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode"),
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
                **Following are the Default Parameters**
                - **EMA Candidate**: 50,200 days
                - **Verbosity** (level of detail loging): detail
                """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_indicator50-200_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
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
                    - **Verbosity**: {sub_task_para_verbosity}
                    """
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
                        file_name=f"ema_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

    elif sub_task == "Exponential moving average (detailed)":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode"),
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
                **Following are the Default Parameters**
                - **EMA Candidate**: 50, 200 days
                - **Verbosity** (level of detail loging): detail
                """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_detail_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_detail_indicator50-200_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
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
                    - **Verbosity**: {sub_task_para_verbosity}
                    """
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
                        file_name=f"ema_detail_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )

    elif sub_task == "Exponential moving average crossover":
        st.markdown("**Please continue and provide input parameters**")
        sub_task_mode = st.selectbox(
            f"Select the mode to perform {sub_task}", ("Default mode", "Manual mode"),
        )
        if sub_task_mode == "Default mode":
            st.markdown(
                """
                **Following are the Default Parameters**
                - **EMA Candidate**: 5, 13, 26 days
                - **Verbosity** (level of detail loging): detail
                """
            )
            if st.button("Continue"):
                with st.spinner("Running the query"):
                    result = ind.ema_crossover_detail_indicator(save=False)
                st.dataframe(result)
                st.download_button(
                    "Download result",
                    data=result.to_csv(index=False).encode("utf-8"),
                    mime="text/csv",
                    file_name=f"ema_crossover_detail_indicator5-13-26_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
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
                    - **Verbosity**: {sub_task_para_verbosity}
                    """
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
                        file_name=f"ema_crossover_detail_indicator{sub_task_para_emacandidate1}-{sub_task_para_emacandidate2}-{sub_task_para_emacandidate3}_{datetime.datetime.now().strftime('%d-%m-%Y')}.csv",
                    )
