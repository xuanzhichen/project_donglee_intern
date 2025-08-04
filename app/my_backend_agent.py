"""
Class-DataAnalyserBackendAgent (类-数据分析后端代理) 的实现

关于该类的封装，一方面是为了将数据分析的业务逻辑与前端可视化相分离（通过继承 DataAnalyser 实现），
另一方面则存在一定的 “历史原因”：

在实例化 DataAnalyser 以对日志数据进行分析之前，初始化一张索引表，这一步被特意分离出来并通过该后端代理隐性实现。
这是因为在该项目的实习初期，日志数据并不是按设备划分好的，而是杂糅在一张大型的数据表中。
因此，首先初始化一张关于（不同）设备的索引表，再去查找和提取对应的日志数据，是必要的。

为了具体做到这一点，程序会根据索引表的 “标识列”（imei, device name）去匹配（以 “标识列” 命名的）日志文件；
但是（随着需求的不断变化），由于后来考虑到，命名问题常常不可控，甚至反过来修改为了根据日志文件的 “标识列” 去匹配索引表。
这也导致了该后端代理的代码存在形同虚设的部分，因为索引表和日志文件都已在缓存内并已排好序，只需在遍历时同时扫描彼此即可，本质上不存在匹配问题。

# Latest update: 2025-07-17
# 如果未来采用数据库直连的方式，索引表和日志文件的匹配问题将不复存在；因为 “查找日志文件” 的逻辑将由数据库的 select 语句实现
"""

# Author: Xuanzhi Chen (陈炫志)
# Email: xuanzhichen.42@gmail.com
# License: MIT

# Latest Update: 2025/07/07


import pandas as pd

from utils import DataAnalyser
from utils.build_your_df_features import index_a_dfda_log, translate_and_mildly_modify_your_df


class DataAnalyserBackendAgent(DataAnalyser):
    """
    我的 Streamlit Web Application 后端代理
    """

    @staticmethod
    def check_id_existence(df_log, uploaded_file):
        """
        Check existence for identification columns and their values: 
        (1) 'imei/IMEI', 
        (2) 'device name/设备ID'
        """

        file_name = uploaded_file.name
        columns_to_check = []

        if 'imei' in df_log.columns:
            columns_to_check.append('imei')
        elif 'IMEI' in df_log.columns:
            columns_to_check.append('IMEI')
        elif 'device_name' in df_log.columns:
            columns_to_check.append('device_name')
        elif  '设备ID' in df_log.columns:
            columns_to_check.append('设备ID')
        else:
            error_message = (
                    f"当前日志 '{file_name}' 文件不存在任一标识列：imei/IMEI/device_name/设备ID。"
                    f"缺乏标识列将无法进行数据分析。"
                    f"请检查该日志格式的正确性，或放弃对该日志的分析。"
                )
            raise ValueError(error_message)
        
        for column in columns_to_check:

            # # Check if the column has exactly one unique value (excluding NaN values)
            # unique_count = df_log[column].dropna().nunique()
            # if unique_count != 1:
            #     error_message = (
            #         f"在当前日志 {file_name} 文件的 '{column}' 这一列中"
            #         f"检测到存在非唯一的 id 值。"
            #         f"请检查该日志格式的正确性，或手动删除该列，或放弃对该日志的分析。"
            #     )
            #     raise ValueError(error_message)
            
            # Check if the column has at least one non-NaN value
            if df_log[column].dropna().empty:
                error_message = (
                    f"在当前日志 '{file_name}' 文件的 '{column}' 这一列中"
                    f"检测到所有值均为 NaN（即空值）。"
                    f"请检查该日志格式的正确性，或放弃对该日志的分析。"
                )
                raise ValueError(error_message)
            
        return True

    @staticmethod
    def index_a_dfda_log(df_log, format_checked=True):
        """
        在实例化 DataAnalyser 以对日志数据进行分析 (dfda, dataframe for data analysis) 之前，
        初始化一张索引表，这一步被特意分离出来并在该函数中实现。
        这一操作具有历史原因，即在该项目的实习初期，日志数据并不是按设备划分好的，而是杂糅在一张大型的数据表中。
        因此，首先初始化一张关于（不同）设备的索引表，再去查找和提取对应的日志数据，是必要的。

        Args:
            df_log: TBD...
            format_checked: This para does nothing but for the sake of consistency for the function call.
        """

        # file_name = uploaded_file.name
        # index_success, dfda_log = index_a_dfda_log(df_log)

        # if not index_success:
        #     error_message = (
        #             f"在当前日志 {file_name} 文件中"
        #             f"检测到所有标识列 (imei/IMEI/device name/设备ID) 存在完全空值。"
        #             f"请检查该日志格式的正确性，或手动删除该列，或放弃对该日志的分析。"
        #         )
        #     raise ValueError(error_message)
        # else:
        #     return dfda_log
        
        return index_a_dfda_log(df_log)
    
    @staticmethod
    def define_uptime_and_downtime(dfda_log, df_log, pattern='single_file_multiple_periods'):
        """
        Args:
            pattern: 
            'single_file_multiple_periods', 
            'multiple_files_single_period',
            'multiple_files_latest_period', 
            'multiple_files_max_period'
        """
        # Convert '创建时间' to datetime and sort
        df_log_sorted = df_log.copy()
        df_log_sorted['创建时间'] = pd.to_datetime(df_log_sorted['创建时间'])
        df_log_sorted = df_log_sorted.sort_values('创建时间', ascending=False)
        
        # Get unique dates from '创建时间' column
        unique_dates = df_log_sorted['创建时间'].dt.date.unique()
        unique_dates = sorted(unique_dates, reverse=True)
        
        # Find continuous periods
        continuous_periods = []
        current_period = [unique_dates[0]]
        
        for i in range(1, len(unique_dates)):
            current_date = unique_dates[i]
            previous_date = unique_dates[i-1]
            
            # Check if dates are consecutive (difference of 1 day)
            if (previous_date - current_date).days == 1:
                current_period.append(current_date)
            else:
                # End of current period, start new one
                if len(current_period) > 0:
                    continuous_periods.append(current_period)
                current_period = [current_date]
        
        # Add the last period
        if len(current_period) > 0:
            continuous_periods.append(current_period)
        
        dfda_log_updated = dfda_log.copy()
        
        if pattern == 'single_file_multiple_periods':
            # Create new rows in dfda_log for each continuous period
            for i, period in enumerate(continuous_periods):
                if i == 0:
                    # Update the original row
                    dfda_log_updated.loc[0, 'downtime'] = pd.to_datetime(period[0]).date()
                    dfda_log_updated.loc[0, 'uptime'] = pd.to_datetime(period[-1]).date()
                    
                else:
                    # Add new row for additional periods
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
    
    @staticmethod
    def concat_dfda_log(dfda_log_whole, dfda_log_individual):
        return pd.concat([dfda_log_whole, dfda_log_individual], ignore_index=True)
        
    @staticmethod
    def translate_and_mildly_modify_your_df(df_data_analysis):
        return translate_and_mildly_modify_your_df(df_data_analysis)