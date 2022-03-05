import datetime

import streamlit as st
from stock_analysis.app.widget import input_widget

from stock_analysis.momentum_strategy import MomentumStrategy


def custom_multi_indicator_sub_app():
    """It create streamlit sub page for multi choice indicator
    """
    try:
        company_symbol_list = input_widget()
        with st.expander("See the selected Company symbol based on chosen criteria"):
            st.write(company_symbol_list)
    except:
        pass

    if company_symbol_list:
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
