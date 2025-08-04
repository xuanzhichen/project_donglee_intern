"""
一行代码执行智能控制器日志数据分析
"""


import pandas as pd
from data_analyser import DataAnalyser


def index_a_dfda_log(df_log):
    device_name = None
    imei = None
    
    if ('device_name' in df_log.columns) and (len(df_log['device_name'].dropna()) > 0):
        device_name = df_log['device_name'].dropna().iloc[0]

    elif ('设备ID' in df_log.columns) and (len(df_log['设备ID'].dropna()) > 0):
        device_name = df_log['设备ID'].dropna().iloc[0]

    if ('imei' in df_log.columns) and (len(df_log['imei'].dropna())> 0):
        imei = int(df_log['imei'].dropna().iloc[0])

    elif ('IMEI' in df_log.columns) and (len(df_log['IMEI'].dropna()) > 0):
        imei = int(df_log['IMEI'].dropna().iloc[0])

    df_log_data_analysis = pd.DataFrame(
        {
            'device_name': [device_name],
            'imei': [imei]
        }
    )

    df_log_data_analysis['uptime'] = pd.Series(dtype='datetime64[ns]')
    df_log_data_analysis['downtime'] = pd.Series(dtype='datetime64[ns]')

    df_log_data_analysis['days_len'] = 0
    df_log_data_analysis['months_len'] = 0

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

    return df_log_data_analysis

def define_uptime_and_downtime(dfda_log, df_log, pattern='single_file_multiple_periods'):
    """
    'single_file_multiple_periods', 
    'multiple_files_single_period',
    'multiple_files_latest_period', 
    'multiple_files_max_period'
    """

    df_log_sorted = df_log.copy()
    df_log_sorted['创建时间'] = pd.to_datetime(df_log_sorted['创建时间'])
    df_log_sorted = df_log_sorted.sort_values('创建时间', ascending=False)
    
    unique_dates = df_log_sorted['创建时间'].dt.date.unique()
    unique_dates = sorted(unique_dates, reverse=True)
    
    continuous_periods = []
    current_period = [unique_dates[0]]
    
    for i in range(1, len(unique_dates)):
        current_date = unique_dates[i]
        previous_date = unique_dates[i-1]
        
        if (previous_date - current_date).days == 1:
            current_period.append(current_date)
        else:
            if len(current_period) > 0:
                continuous_periods.append(current_period)
            current_period = [current_date]
    
    if len(current_period) > 0:
        continuous_periods.append(current_period)
    
    dfda_log_updated = dfda_log.copy()
    
    if pattern == 'single_file_multiple_periods':
        for i, period in enumerate(continuous_periods):
            if i == 0:
                dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(period[0]).date()
                dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(period[-1]).date()
                
            else:
                new_row = dfda_log_updated.iloc[0].copy()
                new_row['downtime'] = pd.to_datetime(period[0]).date()
                new_row['uptime'] = pd.to_datetime(period[-1]).date()
                dfda_log_updated = pd.concat(
                    [dfda_log_updated, pd.DataFrame([new_row])], ignore_index=True
                )
    
    elif pattern == 'multiple_files_single_period':
        latest_period = continuous_periods[0]
        last_period = continuous_periods[-1]
        dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(latest_period[0]).date()
        dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(last_period[-1]).date()

        dfda_log_updated.insert(6, '实际使用天数', 0)
        dfda_log_updated.insert(7, '实际使用月数', 0)

    elif pattern == 'multiple_files_latest_period':
        latest_period = continuous_periods[0]
        dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(latest_period[0]).date()
        dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(latest_period[-1]).date()

    elif pattern == 'multiple_files_max_period':
        if len(continuous_periods) > 1:
            max_period = max(continuous_periods, key=len)
            dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(max_period[0]).date()
            dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(max_period[-1]).date()
        else:
            dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(continuous_periods[0][0]).date()
            dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(continuous_periods[0][-1]).date()

    return dfda_log_updated

def translate_and_mildly_modify_your_df(df_data_analysis):
    df_data_analysis_translated_and_modified = df_data_analysis.copy()

    column_mapping = {
        'downtime': '下线日期 (或日志导出时间)',
        'uptime': '上线日期',
        'days_len': '使用天数',
        'months_len': '使用月数',
        'times_of_standby': '待机次数',
        'times_of_irrigation_start': '开闭灌溉次数',
        'times_of_uptime': '上下线次数',
        'times_of_strong_signal': '强信号次数',
        'times_of_mid_signal': '中等强度次数',
        'times_of_weak_signal': '弱/无强度次数',
        'average_signal': '平均信号强度',
        'min_signal': '最小信号强度',
        'max_signal': '最大信号强度',
        'times_signal_switch_strong_mid': '强/中信号切换次数',
        'times_signal_switch_strong_weak': '强/弱（无）信号切换次数',
        'times_signal_switch_mid_weak': '中/弱（无）信号切换次数',
    }

    df_data_analysis_translated_and_modified['times_of_weak_signal'] += df_data_analysis_translated_and_modified['times_of_null_signal']
    df_data_analysis_translated_and_modified.drop(columns=['times_of_null_signal'], inplace=True)
    
    df_data_analysis_translated_and_modified['times_signal_switch_strong_weak'] += df_data_analysis_translated_and_modified['times_signal_switch_strong_null']
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_strong_null'], inplace=True)
    
    df_data_analysis_translated_and_modified['times_signal_switch_mid_weak'] += df_data_analysis_translated_and_modified['times_signal_switch_mid_null']
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_mid_null'], inplace=True)
    
    df_data_analysis_translated_and_modified.drop(columns=['times_of_irrigation_close'], inplace=True)
    df_data_analysis_translated_and_modified.drop(columns=['times_of_downtime'], inplace=True)
    df_data_analysis_translated_and_modified.drop(columns=['times_signal_switch_weak_null'], inplace=True)

    df_data_analysis_translated_and_modified.rename(columns=column_mapping, inplace=True)

    return df_data_analysis_translated_and_modified

def run_demo(df_log):

    # 1. 初始化 “基于日志的参数统计表”（也作为索索引）
    dfda_log = index_a_dfda_log(df_log)
    dfda_log = define_uptime_and_downtime(dfda_log, df_log)

    # 2. 初始化数据分析对象
    data_analyser = DataAnalyser(dfda_log)

    # 3. 遍历索引表，执行数据分析管道 (pipeline)
    for index, row in dfda_log.iterrows():
        data_analyser.identify_id_info(
            df_device_log=df_log, 
            use_index=True, 
            index=index,
            device_name=None,
            imei=None
        )
        data_analyser.get_usage_period()
        data_analyser.get_sub_log_based_on_usage_period()
        data_analyser.get_operation_status()
        data_analyser.get_signal_strength_frequency()
        data_analyser.get_signal_switch_frequency()

    # 4. 更新 “基于日志的参数统计表”
    dfda_log_updated = data_analyser._df_data_analysis

    # 5. 翻译 “基于日志的参数统计表”
    dfda_log_translated = translate_and_mildly_modify_your_df(dfda_log_updated)

    # 6. 打印 “基于日志的参数统计表”
    print(dfda_log_translated)


if __name__ == '__main__':

    # 运行demo: 一行代码执行智能控制器日志数据分析
    run_demo(df_log=pd.read_excel('智能控制器样例日志（简化测试版）.xlsx'))




