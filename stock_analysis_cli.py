import warnings
from stock_analysis.unit_strategy import MomentumStrategy
from stock_analysis.indicator import Indicator
from stock_analysis.utils.logger import logger

logger = logger()
warnings.filterwarnings('ignore')
logger.info("Please give your input to Start Stock Analysis")

task = int(
    input("Choice task to Perform \n1.Unit Strategy \n2.Indicator \nChoice: "))
# Tasks for Unit Strategy
if task == 1:
    yaml_path = input("Enter Company name yaml file location: ")
    sa = MomentumStrategy(path=yaml_path)

    sub_task = int(
        input("Choose sub task to perform: \n1.Momentum Strategy\n2.Momentum with EMA \nChoice: "))
    
# Sub-task for Momentum Strategy    
    if sub_task == 1:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)Date = today, \
ii)Top company count = 20 iii)Export path = Same folder iv)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            sa.momentum_strategy()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_date = (
                input("Input desired date (default: today)(eg: 01/06/2020): ") or 'today')
            if (len(sub_task_para_date.strip()) == 10 or sub_task_para_date == 'today'):
                sub_task_para_date = str(sub_task_para_date)
            else:
                raise ValueError(
                    f"Given date: {sub_task_para_date} is invalid. Eg input: 01/06/2020")
            sub_task_para_count = int(
                input("Input top company count (Default:20): ") or 20)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)

            sa.momentum_strategy(end_date=sub_task_para_date,
                                 top_company_count=sub_task_para_count,
                                 export_path=sub_task_para_export,
                                 verbosity=sub_task_para_verbosity)

# Sub-task for Momentum with EMA Strategy
    elif sub_task == 2:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)Date = today, \
ii)Top company count = 20 iii)EMA candidate = 50,200 iv)Export path = Same folder iv)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            sa.momentum_with_ema_strategy()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_date = (
                input("Input desired date (default: today)(eg: 01/06/2020): ") or 'today')
            if (len(sub_task_para_date.strip()) == 10 or sub_task_para_date == 'today'):
                sub_task_para_date = str(sub_task_para_date)
            else:
                raise ValueError(
                    f"Given date: {sub_task_para_date} is invalid. Eg input: 01/06/2020")
            sub_task_para_count = int(
                input("Input top company count (Default:20): ") or 20)
            sub_task_para_emacandidate1 = int(
                input("Input desired first EMA candidate (default: 50): ") or 50)
            sub_task_para_emacandidate2 = int(
                input("Input desired second EMA candidate (default: 200): ") or 200)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)

            sa.momentum_with_ema_strategy(end_date=sub_task_para_date,
                                          top_company_count=sub_task_para_count,
                                          ema_canditate=(sub_task_para_emacandidate1,sub_task_para_emacandidate2),
                                          export_path=sub_task_para_export,
                                          verbosity=sub_task_para_verbosity)

# Task for Indicator
elif task == 2:
    yaml_path = input("Enter Company name yaml file location: ")
    ind = Indicator(path=yaml_path)

    sub_task = int(input(
        "Choose sub task to perform: \n1.Volume Indicator for [n] days\n2.Exponential moving average (short)\n3.Exponential moving average (detailed)\n4.Exponential moving average crossover \nChoice: "))
    if sub_task == 1:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)Duration = 90 days, \
ii)Export path = Same folder iii)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            ind.volume_n_days_indicator()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_duration = int(
                input("Input desired duration (default: 90): ") or 90)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)
            ind.volume_n_days_indicator(duration=sub_task_para_duration,
                                        export_path=sub_task_para_export,
                                        verbosity=sub_task_para_verbosity)

    elif sub_task == 2:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)EMA Candidate = (50,200) days, \
ii)Export path = Same folder iii)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            ind.ema_indicator()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_emacandidate1 = int(
                input("Input desired first EMA candidate (default: 50): ") or 50)
            sub_task_para_emacandidate2 = int(
                input("Input desired second EMA candidate (default: 200): ") or 200)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)
            ind.ema_indicator(ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2),
                              export_path=sub_task_para_export,
                              verbosity=sub_task_para_verbosity)
    
    elif sub_task == 3:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)EMA Candidate = (50,200) days, \
ii)Export path = Same folder iii)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            ind.ema_detail_indicator()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_emacandidate1 = int(
                input("Input desired first EMA candidate (default: 50): ") or 50)
            sub_task_para_emacandidate2 = int(
                input("Input desired second EMA candidate (default: 200): ") or 200)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)
            ind.ema_detail_indicator(
                ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2),
                export_path=sub_task_para_export,
                verbosity=sub_task_para_verbosity
                )

    elif sub_task == 4:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)EMA Candidate = (5, 13, 26) days, \
ii)Export path = Same folder iii)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            ind.ema_crossover_detail_indicator()
        elif sub_task_para == 2:
            logger.info(
                "In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_emacandidate1 = int(
                input("Input desired first EMA candidate (default: 5): ") or 5)
            sub_task_para_emacandidate2 = int(
                input("Input desired second EMA candidate (default: 13): ") or 13)
            sub_task_para_emacandidate3 = int(
                input("Input desired third EMA candidate (default: 26): ") or 26)
            sub_task_para_export = (input(
                'Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(
                input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)
            ind.ema_crossover_detail_indicator(
                ema_canditate=(sub_task_para_emacandidate1, sub_task_para_emacandidate2, sub_task_para_emacandidate3),
                export_path=sub_task_para_export,
                verbosity=sub_task_para_verbosity
                )