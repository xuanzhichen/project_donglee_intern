# Historical update: 2025-05-19
# Latest update: 2025-06-17

import pandas as pd
import os

current_file_path = os.path.abspath(__file__)
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(current_file_path))
PATH_SUPERIOR = os.path.join('data', 'external')


def translate_and_mildly_modify_your_df(df_data_analysis):
    df_data_analysis_translated_and_modified = df_data_analysis.copy()

    column_mapping = {
        # 'outbound_item': '出库项目',
        # 'device_code': '设备编号',
        # 'device_name': '设备名称',
        # 'log_len': '日志长度',
        'downtime': '下线日期 (或日志导出时间)',
        'uptime': '上线日期',
        'days_len': '使用天数',
        'months_len': '使用月数',
        # 'num_days_breaks': '设备离线次数',
        # 'max_days_break': '最大离线天数',
        # 'total_days_breaks': '总计离线天数',
        # 'months_len_exclude_breaks': '实际使用月数 (不含中途离线)',
        # 'continued_status': '连续性',
        'times_of_standby': '待机次数',
        'times_of_irrigation_start': '开闭灌溉次数',
        # 'times_of_irrigation_close': '关闭灌溉次数',
        'times_of_uptime': '上下线次数',
        # 'times_of_downtime': '设备下线次数',
        'times_of_strong_signal': '强信号次数',
        'times_of_mid_signal': '中等强度次数',
        'times_of_weak_signal': '弱/无强度次数',
        # 'times_of_null_signal': '无信号次数',
        'average_signal': '平均信号强度',
        'min_signal': '最小信号强度',
        'max_signal': '最大信号强度',
        'times_signal_switch_strong_mid': '强/中信号切换次数',
        'times_signal_switch_strong_weak': '强/弱（无）信号切换次数',
        # 'times_signal_switch_strong_null': '强/无信号切换次数',
        'times_signal_switch_mid_weak': '中/弱（无）信号切换次数',
        # 'times_signal_switch_mid_null': '中/无信号切换次数',
        # 'times_signal_switch_weak_null': '弱/无信号切换次数'
    }

    # Add values from dismissed columns to targeted columns, then delete dismissed columns
    df_data_analysis_translated_and_modified['times_of_weak_signal'] += df_data_analysis_translated_and_modified['times_of_null_signal']
    df_data_analysis_translated_and_modified.drop(columns=['times_of_null_signal'], inplace=True)
    
    df_data_analysis_translated_and_modified['times_signal_switch_strong_weak'] += df_data_analysis_translated_and_modified['times_signal_switch_strong_null']
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_strong_null'], inplace=True)
    
    df_data_analysis_translated_and_modified['times_signal_switch_mid_weak'] += df_data_analysis_translated_and_modified['times_signal_switch_mid_null']
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_mid_null'], inplace=True)
    
    # Simply delete these columns
    df_data_analysis_translated_and_modified.drop(columns=['times_of_irrigation_close'], inplace=True)
    df_data_analysis_translated_and_modified.drop(columns=['times_of_downtime'], inplace=True)
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_weak_null'], inplace=True)

    # Rename columns to Chinese
    df_data_analysis_translated_and_modified.rename(columns=column_mapping, inplace=True)
    
    # # Rename 'haida' to '海大总部' in the '出库项目' column
    # df_data_analysis_translated['出库项目'] = \
    #     df_data_analysis_translated['出库项目'].replace('haida', '海大总部')
    
    # # Rename 'T/F' to '是/否' in the '连续性' column
    # df_data_analysis_translated['连续性'] = \
    #     df_data_analysis_translated['连续性'].replace('T', '是').replace('F', '否')

    return df_data_analysis_translated_and_modified

# 该函数已经弃用
def init_df_log_data_analysis(haida=True, sanyi=False, small_town=False):
    """该函数已经弃用"""
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

def index_a_dfda_log(df_log):
    """
    在实例化 DataAnalyser 以对日志数据进行分析 (dfda, dataframe for data analysis) 之前，
    初始化一张索引表，这一步被特意分离出来并在该函数中实现。
    这一操作具有历史原因，即在该项目的实习初期，日志数据并不是按设备划分好的，而是杂糅在一张大型的数据表中。
    因此，首先初始化一张关于（不同）设备的索引表，再去查找和提取对应的日志数据，是必要的。 

    与最初的设想不同，最终的交付项目沿用了统一的、固定的特征构建。
    """
    # index_success = False
    device_name = None
    imei = None
    
    # Have ensured that either device_name (设备ID) or imei is unique
    if ('device_name' in df_log.columns) and (len(df_log['device_name'].dropna()) > 0):
        device_name = df_log['device_name'].dropna().iloc[0]
        # index_success = True

    elif ('设备ID' in df_log.columns) and (len(df_log['设备ID'].dropna()) > 0):
        device_name = df_log['设备ID'].dropna().iloc[0]
        # index_success = True

    if ('imei' in df_log.columns) and (len(df_log['imei'].dropna())> 0):
        imei = int(df_log['imei'].dropna().iloc[0])
        # index_success = True

    elif ('IMEI' in df_log.columns) and (len(df_log['IMEI'].dropna()) > 0):
        imei = int(df_log['IMEI'].dropna().iloc[0])
        # index_success = True

    # if not index_success:
    #     return index_success, None
    
    df_log_data_analysis = pd.DataFrame(
        {
            'device_name': [device_name],
            'imei': [imei]
        }
    )

    # Create a dataframe for data analysis
    # df_log_data_analysis['log_len'] = 0

    df_log_data_analysis['uptime'] = pd.Series(dtype='datetime64[ns]')
    df_log_data_analysis['downtime'] = pd.Series(dtype='datetime64[ns]')

    df_log_data_analysis['days_len'] = 0
    df_log_data_analysis['months_len'] = 0

    # df_log_data_analysis['num_days_breaks'] = 0
    # df_log_data_analysis['max_days_break'] = 0
    # df_log_data_analysis['total_days_breaks'] = 0
    # df_log_data_analysis['months_len_exclude_breaks'] = 0
    # df_log_data_analysis['continued_status'] = 'T'

    df_log_data_analysis['times_of_standby'] = 0
    df_log_data_analysis['times_of_irrigation_start'] = 0
    df_log_data_analysis['times_of_irrigation_close'] = 0
    df_log_data_analysis['times_of_uptime'] = 0
    df_log_data_analysis['times_of_downtime'] = 0

    df_log_data_analysis['times_of_strong_signal'] = 0
    df_log_data_analysis['times_of_mid_signal'] = 0
    df_log_data_analysis['times_of_weak_signal'] = 0
    df_log_data_analysis['times_of_null_signal'] = 0
    df_log_data_analysis['average_signal'] = 0.0
    df_log_data_analysis['min_signal'] = 0
    df_log_data_analysis['max_signal'] = 0

    df_log_data_analysis['times_signal_switch_strong_mid'] = 0
    df_log_data_analysis['times_signal_switch_strong_weak'] = 0
    df_log_data_analysis['times_signal_switch_strong_null'] = 0
    df_log_data_analysis['times_signal_switch_mid_weak'] = 0
    df_log_data_analysis['times_signal_switch_mid_null'] = 0
    df_log_data_analysis['times_signal_switch_weak_null'] = 0

    # return index_success, df_log_data_analysis
    return df_log_data_analysis
    
def main():
    print(PROJECT_ROOT_PATH)
    print(PATH_SUPERIOR)

    # df_data_analysis = init_df_data_analysis(haida=True, sanyi=False, small_town=False)
    # print(df_data_analysis)
    # print(f"Shape: {df_data_analysis.shape}")

    df_log = pd.read_excel(
        os.path.join(PROJECT_ROOT_PATH, PATH_SUPERIOR, 
                    'j4wE36eNXBk1M63f7TUh.xlsx'),
    )
    
    df_log_data_analysis = index_a_dfda_log(df_log)
    print(df_log_data_analysis)
    print(f"Shape: {df_log_data_analysis.shape}")


if __name__ == "__main__":
    main()  
