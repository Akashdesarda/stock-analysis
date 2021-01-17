import os
import glob
import datetime
import pandas as pd
import streamlit as st
from stock_analysis.indicator import Indicator
from stock_analysis.utils.logger import logger
from stock_analysis.unit_strategy import UnitStrategy

def newest_file(path: str)-> str:
    file_list = glob.glob(path)
    return max(file_list, key=os.path.getctime)
# Sidebar and task intros
default_intro = """
# Welcome to Stock Analysis
"""
unit_intro = """
### This is used to perform Unit strategy
"""
ind_intro = """
### This is used to perform Indicator
"""
st.set_page_config('Stock Analysis')
task = st.sidebar.selectbox(
    "Please select the task to start Stock Analysis",
    ("Home", "Unit strategy", "Indicator")
)
st.sidebar.info("Select a task above")
# st.title("Stock Analysis")
if task == 'Home':
    st.markdown(default_intro)
elif task == 'Unit strategy':
    st.markdown(unit_intro)
elif task == 'Indicator':
    st.markdown(ind_intro)

if task == 'Unit strategy':
    #TODO: Add more interaction by adding start/continue button 
    # if st.button('Start'):
    yaml_path = st.text_input(label='Enter Company name yaml file location')
    if yaml_path:
        sa = UnitStrategy(path=yaml_path)
    else:
        st.warning('Yaml file with Company name must be given')
    sub_task = st.selectbox(
        label="Choose sub task to perform",
        options=(' ','Momentum Strategy','Momentum with EMA')
    )
    if sub_task == 'Momentum Strategy':
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
    **Following are the Default Parameters**
    - **Date**: today
    - **Top company count**: 20
    - **Export path**: Same folder
    - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    sa.momentum_strategy()
                st.dataframe(
                    pd.read_csv(newest_file('./momentum_result_*.csv'))
                )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/momentum_result_*.csv")}""")
        
        elif sub_task_mode == 'Manual mode':
            sub_task_para_date = st.date_input(
                label="Input desired")
            sub_task_para_date = sub_task_para_date.strftime('%d/%m/%Y')
            sub_task_para_count = st.number_input(
                label='Input top company count',
                value=20
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1
            )
            if (sub_task_para_date) and (sub_task_para_count) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
    **Following Parameters are given:**
    - **Date**: {sub_task_para_date}
    - **Top company count**: {sub_task_para_count}
    - **Export path**: {sub_task_para_export}
    - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):
                        sa.momentum_strategy(
                            end_date=sub_task_para_date,
                            top_company_count=int(sub_task_para_count),
                            export_path=sub_task_para_export,
                            verbosity=int(sub_task_para_verbosity)
                        )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/momentum_result_*.csv'))
                )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/momentum_result_*.csv")}""")

    elif sub_task == "Momentum with EMA":
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
    **Following are the Default Parameters**
    - **Date**: today
    - **Top company count**: 20
    - **EMA Candidate**: 50,200
    - **Export path**: Same folder
    - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    sa.momentum_with_ema_strategy()
                st.dataframe(
                        pd.read_csv(newest_file('./momentum_ema*.csv'))
                    )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/momentum_ema*.csv")}""")
        elif sub_task_mode == 'Manual mode':
            sub_task_para_date = st.date_input(
                label="Input desired")
            sub_task_para_date = str(sub_task_para_date.strftime('%d/%m/%Y'))
            sub_task_para_emacandidate1 = st.number_input(
                label=("Input desired first EMA candidate"),
                value=5
            )
            sub_task_para_emacandidate2 = st.number_input(
                label=("Input desired second EMA candidate"),
                value=200
            )
            sub_task_para_count = st.number_input(
                label='Input top company count',
                value=20
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1
            )
            if (sub_task_para_date) and (sub_task_para_count) and (sub_task_para_emacandidate1) and (sub_task_para_emacandidate2) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
    **Following Parameters are given:**
    - **Date**: {sub_task_para_date}
    - **EMA Candidate**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Top company count**: {sub_task_para_count}
    - **Export path**: {sub_task_para_export}
    - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):
                        sa.momentum_with_ema_strategy(
                            end_date=sub_task_para_date,
                            top_company_count=sub_task_para_count,
                            ema_canditate=(sub_task_para_emacandidate1,sub_task_para_emacandidate2),
                            export_path=sub_task_para_export,
                            verbosity=sub_task_para_verbosity
                        )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/momentum_ema*.csv'))
                )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/momentum_ema*.csv")}""")

# Task for Indicator
elif task == 'Indicator':
    yaml_path = st.text_input(label='Enter Company name yaml file location')
    if yaml_path:
        ind = Indicator(path=yaml_path)
    else:
        st.warning('Yaml file with Company name must be given')
    sub_task = st.selectbox(
        label="Choose sub task to perform",
        options=(' ',
            'Volume Indicator for [n] days',
            'Exponential moving average (short)',
            'Exponential moving average (detailed)',
            'Exponential moving average crossover'
        )
    )
    if sub_task == 'Volume Indicator for [n] days':
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
    **Following are the Default Parameters**
    - **Duration**: 90 days
    - **Export path**: Same folder
    - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    ind.volume_indicator_n_days()
                st.dataframe(
                    pd.read_csv(newest_file('./VolumeIndicator90Days_detailed_*.csv'))
                )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/VolumeIndicator90Days_detailed_*.csv")}""")
        elif sub_task_mode == 'Manual mode':
            sub_task_para_duration = st.number_input(
                label='Input desired duration',
                min_value=1,
                value=90
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1,
            )
            if (sub_task_para_duration) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
    **Following Parameters are given:**
    - **Duration**: {sub_task_para_duration}
    - **Export path**: {sub_task_para_export}
    - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):
                        ind.volume_indicator_n_days(
                            duration=sub_task_para_duration,
                            export_path=sub_task_para_export,
                            verbosity=sub_task_para_verbosity
                        )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/VolumeIndicator90Days_detailed_*.csv'))
                )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/VolumeIndicator90Days_detailed_*.csv")}""")
                    
    elif sub_task == 'Exponential moving average (short)':
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
    **Following are the Default Parameters**
    - **EMA Candidate**: 50,200 days
    - **Export path**: Same folder
    - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    ind.ema_indicator()
                st.dataframe(
                    pd.read_csv(newest_file('./ema_indicator*.csv'))
                )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/ema_indicator*.csv")}""")
        elif sub_task_mode == 'Manual mode':
            sub_task_para_emacandidate1 = st.number_input(
                label='Input desired first EMA candidate',
                value=5,
                step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label='Input desired second EMA candidate',
                value=200,
                step=1
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1
            )
            if (sub_task_para_emacandidate1) and (sub_task_para_emacandidate2) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
    **Following Parameters are given:**
    - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Export path**: {sub_task_para_export}
    - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):
                        ind.ema_indicator(
                            ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2),
                            export_path=sub_task_para_export,
                            verbosity=sub_task_para_verbosity
                        )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/ema_indicator*.csv'))
                    )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/ema_indicator*.csv")}""")
                    
    elif sub_task == 'Exponential moving average (detailed)':
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
    **Following are the Default Parameters**
    - **EMA Candidate**: 50, 200 days
    - **Export path**: Same folder
    - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    ind.ema_indicator_detail()
                st.dataframe(
                    pd.read_csv(newest_file('./ema_indicator_detail*.csv'))
                )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/ema_indicator_detail*.csv")}""")
        elif sub_task_mode == 'Manual mode':
            sub_task_para_emacandidate1 = st.number_input(
                label='Input desired first EMA candidate',
                value=5,
                step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label='Input desired second EMA candidate',
                value=200,
                step=1
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1
            )
            if (sub_task_para_emacandidate1) and (sub_task_para_emacandidate2) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
    **Following Parameters are given:**
    - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}
    - **Export path**: {sub_task_para_export}
    - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):    
                        ind.ema_indicator_detail(
                        ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2),
                        export_path=sub_task_para_export,
                        verbosity=sub_task_para_verbosity
                )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/ema_indicator_detail*.csv'))
                )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/ema_indicator_detail*.csv")}""")
    
    elif sub_task == 'Exponential moving average crossover':
        st.markdown('**Please continue and provide input parameters**')
        sub_task_mode = st.selectbox(
            f'Select the mode to perform {sub_task}',
            ('Default mode', 'Manual mode')
        )
        if sub_task_mode == 'Default mode':
            st.markdown("""
            **Following are the Default Parameters**
            - **EMA Candidate**: 5, 13, 26 days
            - **Export path**: Same folder
            - **Verbosity** (level of detail loging): detail """)
            if st.button('Continue'):
                with st.spinner("Running the query"):
                    ind.ema_crossover_indicator_detail()
                st.dataframe(
                    pd.read_csv(newest_file('./ema_crossover_indicator_detail*.csv'))
                )
                st.success(
                    f"""Result have been saved to {newest_file(f"{os.path.abspath('.')}/ema_crossover_indicator_detail*.csv")}""")
        elif sub_task_mode == 'Manual mode':
            sub_task_para_emacandidate1 = st.number_input(
                label='Input desired first EMA candidate',
                value=5,
                step=1
            )
            sub_task_para_emacandidate2 = st.number_input(
                label='Input desired second EMA candidate',
                value=13,
                step=1
            )
            sub_task_para_emacandidate3 = st.number_input(
                label='Input desired third EMA candidate',
                value=26,
                step=1
            )
            sub_task_para_export = st.text_input(
                label='Enter path to save result',
                value='.'
            )
            sub_task_para_verbosity = st.number_input(
                label="Input Verbosity (level 0: Minimal, 1: Detail)",
                value=1,
                min_value=0,
                max_value=1
            )
            if (sub_task_para_emacandidate1) and (sub_task_para_emacandidate2) and (sub_task_para_emacandidate3) and (sub_task_para_export) and (sub_task_para_verbosity) is not None:
                st.markdown(f"""
                **Following Parameters are given:**
                - **EMA candidates**: {sub_task_para_emacandidate1}, {sub_task_para_emacandidate2}, {sub_task_para_emacandidate3}
                - **Export path**: {sub_task_para_export}
                - **Verbosity**: {sub_task_para_verbosity}""")
                if st.button('Continue'):
                    with st.spinner("Running the query"):
                        ind.ema_crossover_indicator_detail(
                            ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2, sub_task_para_emacandidate3),
                            export_path=sub_task_para_export,
                            verbosity=sub_task_para_verbosity
                    )
                    st.dataframe(
                    pd.read_csv(newest_file(f'{sub_task_para_export}/ema_crossover_indicator_detail*.csv'))
                )
                    st.success(
                        f"""Result have been saved to {newest_file(f"{os.path.abspath(f'{sub_task_para_export}')}/ema_crossover_indicator_detail*.csv")}""")