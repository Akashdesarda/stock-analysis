import datetime

import streamlit as st

from stock_analysis.app.widget import input_widget
from stock_analysis.momentum_strategy import MomentumStrategy


def momentum_strategy_sub_app():
    """It creates streamlit sub-page for momentum strategy"""
    try:
        company_symbol_list = input_widget()
        with st.expander("See the selected Company symbol based on chosen criteria"):
            st.write(company_symbol_list)
    except:
        pass

    if company_symbol_list:
        sa = MomentumStrategy(company_name=company_symbol_list)

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
                - **Verbosity** (level of detail loging): detail
                """
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
                    - **Verbosity**: {sub_task_para_verbosity}
                    """
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
                - **Verbosity** (level of detail loging): detail
                """
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
                    - **Verbosity**: {sub_task_para_verbosity}
                    """
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
                - **Verbosity** (level of detail loging): detail
                """
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
                    - **Cutoff Percentage**: {sub_task_para_cutoff}
                    """
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
