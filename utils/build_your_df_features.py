# Latest update: 2025-05-19

import pandas as pd
import os

current_file_path = os.path.abspath(__file__)
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(current_file_path))
PATH_SUPERIOR = os.path.join('data', 'external')


def init_df_data_analysis(haida=True, sanyi=False, small_town=False):
    # Read only the first three columns from the equipments_verification_mycopy_20250421.xlsx
    # Note: equipments_verification_20250421 is not selected to read because of Garbled
    df_equipments_verification = pd.read_excel(
        os.path.join(PROJECT_ROOT_PATH, PATH_SUPERIOR, 
                    'equipments_verification_mycopy_20250421.xlsx'),
        usecols=[0,1,2]
    )

    # Rename columns to English names for better readability
    df_equipments_verification.columns = [ 
        'outbound_item', 
        'device_code',
        'device_name'
    ]

    # Replace specific values in 'outbound_item' column
    df_equipments_verification['outbound_item'] = \
        df_equipments_verification['outbound_item'].replace({
        '海大总部': 'haida',
        '三一总部': 'sanyi', 
        '小城故事': 'small_town'
    })

    # Create a dataframe for data analysis (HaiDa temporarily)
    if haida is True:
        df_data_analysis = \
        df_equipments_verification[df_equipments_verification['outbound_item'] == 'haida'].copy()

        # Initialize datetime columns with date objects
        df_data_analysis['log_len'] = 0
        df_data_analysis['downtime'] = pd.Series(dtype='datetime64[ns]')
        df_data_analysis['uptime'] = pd.Series(dtype='datetime64[ns]')
        df_data_analysis['months_len'] = 0
        df_data_analysis['num_days_breaks'] = 0
        df_data_analysis['max_days_break'] = 0
        df_data_analysis['total_days_breaks'] = 0
        df_data_analysis['months_len_exclude_breaks'] = 0
        df_data_analysis['continued_status'] = 'T'
        df_data_analysis['times_of_standby'] = 0
        df_data_analysis['times_of_irrigation_start'] = 0
        df_data_analysis['times_of_irrigation_close'] = 0
        df_data_analysis['times_of_uptime'] = 0
        df_data_analysis['times_of_downtime'] = 0
        df_data_analysis['times_of_strong_signal'] = 0
        df_data_analysis['times_of_mid_signal'] = 0
        df_data_analysis['times_of_weak_signal'] = 0
        df_data_analysis['times_of_null_signal'] = 0
        df_data_analysis['average_signal'] = 0.0
        df_data_analysis['min_signal'] = 0
        df_data_analysis['max_signal'] = 0
        df_data_analysis['times_signal_switch_strong_mid'] = 0
        df_data_analysis['times_signal_switch_strong_weak'] = 0
        df_data_analysis['times_signal_switch_strong_null'] = 0
        df_data_analysis['times_signal_switch_mid_weak'] = 0
        df_data_analysis['times_signal_switch_mid_null'] = 0
        df_data_analysis['times_signal_switch_weak_null'] = 0

    return df_data_analysis
    
def main():
    # print(PROJECT_ROOT_PATH)
    # print(PATH_SUPERIOR)

    df_data_analysis = init_df_data_analysis(haida=True, sanyi=False, small_town=False)
    
    print(df_data_analysis)
    print(f"Shape: {df_data_analysis.shape}")


if __name__ == "__main__":
    main()  
