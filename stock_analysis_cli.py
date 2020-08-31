import warnings
from stock_analysis.data_retrive import StockAnalysis
from stock_analysis.indicator import Indicator

warnings.filterwarnings('ignore')
print("Please give your input to Start Stock Analysis")

task = int(input("Choice task to Perform \n1.Stock Analysis \n2.Indicator \nChoice: "))
if task == 1:
    yaml_path = input("Enter Company name yaml file location: ")
    sa = StockAnalysis(path=yaml_path)
    
    sub_task = int(input("Choose sub task to perform: \n1.Momentum Strategy \nChoice: "))
    if sub_task == 1:
        sub_task_para = int(input("Choose input parameter nature \n1.Default --> i)Date = today, \
ii)Top company count = 20 iii)Export path = Same folder iv)Verbosity (level of detail logging): Detail\
\n2.Manual \nChoice: "))
        if sub_task_para == 1:
            sa.momentum_strategy()
        if sub_task_para == 2:
            print("In Manual mode whereever you see 'default' then presing enter key will take default value")
            sub_task_para_date = (input("Input desired date (default: today)(eg: 01/06/2020): ") or 'today')
            if (len(sub_task_para_date.strip()) == 10 or sub_task_para_date =='today'):
                sub_task_para_date = str(sub_task_para_date)
            else:
                raise ValueError(f"Given date: {sub_task_para_date} is invalid. Eg input: 01/06/2020")
            sub_task_para_count = int(input("Input top company count (Default:20): ") or 20)
            sub_task_para_export = (input('Enter path to save result (eg: ./some_folder) (default: .  (to save in current working directory): ') or '.')
            sub_task_para_verbosity = int(input('Input Verbosity [level 0: Minimal, 1: Detail (default: 1)]: ') or 1)
            
            sa.momentum_strategy(end_date=sub_task_para_date,
                                 top_company_count=sub_task_para_count,
                                 export_path=sub_task_para_export,
                                 verbosity=sub_task_para_verbosity)
            