import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toolbox.data_analyser import DataAnalyser
from utils.build_your_df_features import init_df_data_analysis

# Setup global variables
current_file_path = os.path.abspath(__file__)
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(current_file_path))
PATH_SUPERIOR = os.path.join('data', 'reframing', 'collection_sep_device_log', 'haida')
PATH_OUTPUT = os.path.join('experiments', 'tests_data_visualization', 'tests_data')


# Latest update: 2025-05-12
def display_path():
    print(f"Input path: {PROJECT_ROOT_PATH}/{PATH_SUPERIOR}")
    print(f"Output path: {PROJECT_ROOT_PATH}/{PATH_OUTPUT}")

# Latest update: 2025-05-12
def output_df_data_analysis(df_data_analysis, file_name):
    df_data_analysis.to_csv(
        os.path.join(
            PROJECT_ROOT_PATH, PATH_OUTPUT, file_name
        ),
        index=False
    )

# Design test functions
# Latest update: 2025-05-12
def test_get_downtime_uptime(data_analyser, device_name, df_device_log): 
    data_analyser.get_downtime_uptime(device_name, df_device_log)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_downtime_uptime.csv')
    
    return data_analyser

# Latest update: 2025-05-12
def test_get_month_len_include_break(data_analyser, device_name):
    data_analyser.get_month_len_include_break(device_name)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_month_len.csv')

    return data_analyser
    
# Latest update: 2025-05-12
def test_get_month_len_exclude_break(data_analyser, device_name, df_device_log, days_break_threshold=2):
    data_analyser.get_month_len_exclude_break(device_name, df_device_log, days_break_threshold)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_month_len.csv')

    return data_analyser

# Latest update: 2025-05-13
def test_get_operation_status(data_analyser, device_name, df_device_log):
    data_analyser.get_operation_status(device_name, df_device_log)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_operation_status.csv')

    return data_analyser

# Latest update: 2025-05-13
def test_get_signal_strength_frequency(data_analyser, device_name, df_device_log):
    data_analyser.get_signal_strength_frequency(device_name, df_device_log)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_signal_strength.csv')

    return data_analyser

# Latest update: 2025-05-13
def test_get_signal_switch_frequency(data_analyser, device_name, df_device_log):
    data_analyser.get_signal_switch_frequency(device_name, df_device_log)
    df_data_analysis_update = data_analyser._df_data_analysis
    output_df_data_analysis(df_data_analysis_update, 'test_get_signal_switch_frequency.csv')

    return data_analyser

# Latest update: 2025-05-13
def main():
    # display_path()

    # Set the device name appeared in the first row of equipments_verification.xlsx
    device_name = 'r24zIcmdHvbIjmkUZ1F6'   

    # Read the device log and initialize the dataframe for data analysis
    df_device_log = pd.read_excel(
        os.path.join(
            PROJECT_ROOT_PATH, PATH_SUPERIOR, (device_name + '.xlsx')
        )
    )
    df_data_analysis_init = init_df_data_analysis(haida=True, sanyi=False, small_town=False)

    # Initialize the data analyser instance
    data_analyser = DataAnalyser(df_data_analysis_init)

    # Pass the instance to each of the test functions for Independent module testing
    # data_analyser = test_get_downtime_uptime(data_analyser, device_name, df_device_log)
    # data_analyser = test_get_month_len_include_break(data_analyser, device_name)
    # data_analyser = test_get_month_len_exclude_break(data_analyser, device_name, df_device_log)

    # data_analyser = test_get_operation_status(data_analyser, device_name, df_device_log)

    # data_analyser = test_get_signal_strength_frequency(data_analyser, device_name, df_device_log)

    data_analyser = test_get_signal_switch_frequency(data_analyser, device_name, df_device_log)

    print("\nTesting program runs successfully!")


if __name__ == "__main__":
    main()  