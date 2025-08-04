"""
Class-DataAnalyserFrontendAgent (类-数据分析前端代理) 的实现

关于该类的封装 —— 尤其是对配置项 (Options) 的直接调用 —— 其本意是为了方便东篱智云科技有限公司的开发人员进行代码移植；
因为该公司的主要产品，智云 IOT 平台，采用了基于 Vue-JavaScript 的开发框架 (ECharts-可视化)。
"""

# Author: Xuanzhi Chen (陈炫志)
# Email: xuanzhichen.42@gmail.com
# License: MIT

# Latest Update: 2025/07/29


# 导入开源可视化图表库的 —— ECharts —— 基于 JavaScript 风格的配置项 (Options)
# ECharts：https://echarts.apache.org/zh/index.html
from app.echarts_js_pseudo import (

    # “单设备处理” 页面 >> 生命周期与使用时长-可视化
    get_options_usage_track,

    # “单设备处理” 页面 >> 操作类型（实时）-可视化
    get_options_operation_real_time, 

    # “单设备处理” 页面 >> 操作类型（日均）-可视化
    get_options_operation_daily_average,

    # “单设备处理” 页面 >> 信号强度（实时）-可视化
    get_options_signal_real_time,

    # “单设备处理” 页面 >> 信号强度（日均）-可视化
    get_options_signal_daily_average,

    # “多设备处理” 页面 >> 生命周期与使用时长-可视化
    get_options_usage_lifecycle,

    # “多设备处理” 页面 >> 操作类型（按设备编号）- 可视化
    get_options_operation_freq_by_device_id,

    # “多设备处理” 页面 >> 操作类型（按设备台数）- 可视化
    get_options_operation_freq_by_device_amount,

    # “多设备处理” 页面 >> 信号强度（按设备编号）- 可视化
    get_options_signal_freq_by_device_id,

    # “多设备处理” 页面 >> 信号强度（按设备台数）- 可视化
    get_options_signal_freq_by_device_amount,
)

from streamlit_echarts import st_echarts
import pandas as pd


class DataAnalyserFrontendAgent():
    """
    我的 Streamlit Web Application 数据分析前端代理；所有的方法实现遵循以下三步过程流：

    第一步：处理基于日志的参数统计表，得到相应的变量
    第二步：将第一步得到的变量作为参数传递，获取 ECharts 基于 JavaScript 风格的配置项 (Options)
    第三步：将第二步得到的配置项作为参数传递，使用 Streamlit 的第三方容器 (ECharts) 以可视化图表
    """

    # “单设备处理” 页面
    class SingleDeviceProcessing():
        """
        该类用于 “单设备处理” 页面中的数据可视化与分析。
        """

        # Helper function to format dates as YY-MM-DD
        def format_dates(dates):

            formatted_dates = []

            for date in dates:
                # Get the last two digits of the year
                year_short = str(date.year)[-2:]
                formatted_dates.append(f"{year_short}-{date.strftime('%m-%d')}")

            return formatted_dates
        
        # Helper function to map status to a number
        def map_status(status):
            if status not in ['设备上线', '设备下线', '设备状态', '开启灌溉', '关闭灌溉']:
                return 0  # '*无类型记录'
            elif status in ['设备上线', '设备下线']:
                return 1  # '上线/下线'
            elif status in ['开启灌溉', '关闭灌溉']:
                return 2  # '开启灌溉'
            else:  
                return 3 # '设备状态'

        # 生命周期与使用时长-可视化
        @staticmethod
        def visualize_usage_track(dfda_log_translated, df_log):

            def _get_required_parameters(dfda_log_translated, df_log):

                required_parameters = {}

                # Get the date range from the dataframe
                df_log['创建时间'] = pd.to_datetime(df_log['创建时间']) # Ensure '创建时间' is in datetime format
                df_log_dates = df_log['创建时间'].dt.date
                min_date = df_log_dates.min()
                max_date = df_log_dates.max()
                
                # Create date range from min to max date
                date_range = pd.date_range(start=min_date, end=max_date, freq='D')
                
                # Initialize status array (0 = offline, 1 = online)
                status_data = []
                
                # Check each date in the range
                for date in date_range:
                    date_only = date.date()
                    is_online = False
                    
                    # Check if this date falls within any online period
                    for _, row in dfda_log_translated.iterrows():
                        try:
                            online_start = pd.to_datetime(row['上线日期']).date()
                            online_end = pd.to_datetime(row['下线日期 (或日志导出时间)']).date()
                            
                            # Check if current date is within the online period
                            if (online_start <= date_only) and (date_only <= online_end):
                                is_online = True
                                break
                        except:

                            # Handle any date parsing errors
                            continue
                    
                    status_data.append(1 if is_online else 0)
                
                # Format dates for x-axis (e.g., 2025-01-01 -> 25-01)
                x_axis_dates = DataAnalyserFrontendAgent.SingleDeviceProcessing.format_dates(date_range)

                # x_axis_dates (list): 根据日志起始范围内连续的日期列表，格式已简化，例如 ['25-01', '25-02', ..., '25-12']
                required_parameters['x_axis_dates'] = x_axis_dates
                
                # status_data (list): 设备上下线状态的数据列表，1 表示设备在线（即日志连续），0 表示设备离线（即日志中断）
                required_parameters['status_data'] = status_data

                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated, df_log)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_usage_track = get_options_usage_track(
                x_axis_dates=required_parameters['x_axis_dates'],
                status_data=required_parameters['status_data']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_usage_track, height="400px")

        # 操作类型（实时）-可视化
        @staticmethod
        def visualize_operation_real_time(df_log: pd.DataFrame, uploaded_file):
            
            def _get_required_parameters(df_log):

                required_parameters = {}

                # Define the 4 categories
                status_categories = ['0', '1', '2', '3']

                # Format dates for real-time status chart
                x_axis_data = DataAnalyserFrontendAgent.SingleDeviceProcessing.format_dates(
                    df_log.sort_values('创建时间')['创建时间']
                )

                status_raw = df_log.sort_values('创建时间')['操作类型'].tolist()    
                y_axis_data = [DataAnalyserFrontendAgent.SingleDeviceProcessing.map_status(s) for s in status_raw]

                # x_axis_data (list): 即日志本身的记录范围（未必连续），格式已简化，例如 ['25-01', '25-02', ..., '25-12']
                required_parameters['x_axis_data'] = x_axis_data

                # y_axis_data (list): 映射日志的每个时间戳 (x_axis_data) 所对应的操作类型（编码）
                required_parameters['y_axis_data'] = y_axis_data

                # status_categories (list): 对不同操作类型的编码，例如 [0, 1, 2, 3]
                required_parameters['status_categories'] = status_categories

                return required_parameters
            
            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(df_log)
            
            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_operation_real_time = get_options_operation_real_time(
                uploaded_file=uploaded_file,
                x_axis_data=required_parameters['x_axis_data'],
                y_axis_data=required_parameters['y_axis_data'],
                status_categories=required_parameters['status_categories']
            )
            
            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_operation_real_time, height="500px")

        # 操作类型（日均）-可视化
        @staticmethod
        def visualize_operation_daily_average(df_log: pd.DataFrame, uploaded_file):
            
            def _get_required_parameters(df_log):

                required_parameters = {}

                # Define the 4 categories
                status_categories = ['0', '1', '2', '3']

                daily_status = df_log.copy()
                daily_status['date'] = daily_status['创建时间'].dt.date

                daily_status_mode = daily_status.groupby('date')['操作类型'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
                daily_status_mode = daily_status_mode.sort_index()

                daily_status_mode_idx = daily_status_mode.map(DataAnalyserFrontendAgent.SingleDeviceProcessing.map_status).tolist()
                daily_status_dates = DataAnalyserFrontendAgent.SingleDeviceProcessing.format_dates(pd.to_datetime(daily_status_mode.index))

                # daily_status_dates (list): 将实时日志按日聚合（降频）后的列表，格式已简化，例如 ['25-01-01', '25-01-02', ..., '25-12-31']
                required_parameters['daily_status_dates'] = daily_status_dates
                
                # daily_status_mode_idx (list): 映射日志的每个日期 (daily_status_dates) 所对应的操作类型（编码），
                # 准确来说，是该日期下，操作类型出现次数最多的操作类型（编码）
                required_parameters['daily_status_mode_idx'] = daily_status_mode_idx
                
                # status_categories (list): 对不同操作类型的编码，例如 [0, 1, 2, 3]
                required_parameters['status_categories'] = status_categories

                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(df_log)  
            
            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_operation_daily_average = get_options_operation_daily_average(
                uploaded_file=uploaded_file,
                daily_status_dates=required_parameters['daily_status_dates'],
                daily_status_mode_idx=required_parameters['daily_status_mode_idx'],
                status_categories=required_parameters['status_categories']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_operation_daily_average, height="500px")
        
        # 信号强度（实时）-可视化   
        @staticmethod
        def visualize_signal_real_time(df_log: pd.DataFrame, uploaded_file):
            
            def _get_required_parameters(df_log):

                required_parameters = {}

                signal_data = [0 if pd.isna(val) else val for val in df_log.sort_values('创建时间')['信号']]
                x_axis_data_signal = DataAnalyserFrontendAgent.SingleDeviceProcessing.format_dates(
                    df_log.sort_values('创建时间')['创建时间']
                )

                # signal_data (list): 映射日志的每个时间戳 (x_axis_data_signal) 所对应的信号强度值
                required_parameters['signal_data'] = signal_data

                # x_axis_data_signal (list): 即日志本身的记录范围（未必连续），格式已简化，例如 ['25-01', '25-02', ..., '25-12']
                required_parameters['x_axis_data_signal'] = x_axis_data_signal

                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(df_log)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)   
            options_signal_real_time = get_options_signal_real_time(
                uploaded_file=uploaded_file,
                signal_data=required_parameters['signal_data'],
                x_axis_data_signal=required_parameters['x_axis_data_signal']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_signal_real_time, height="500px")

        # 信号强度（日均）-可视化
        @staticmethod
        def visualize_signal_daily_average(df_log: pd.DataFrame, uploaded_file):
            
            def _get_required_parameters(df_log):

                required_parameters = {}

                daily_signal = df_log.copy()
                daily_signal['date'] = daily_signal['创建时间'].dt.date

                daily_signal_mean = daily_signal.groupby('date')['信号'].mean().round(2)
                daily_signal_mean = daily_signal_mean.sort_index()

                daily_signal_dates = DataAnalyserFrontendAgent.SingleDeviceProcessing.format_dates(
                    pd.to_datetime(daily_signal_mean.index)
                )
                daily_signal_values = [0 if pd.isna(val) else val for val in daily_signal_mean]

                # daily_signal_dates (list): 将实时日志按日聚合（降频）后的列表，格式已简化，例如 ['25-01-01', '25-01-02', ..., '25-12-31']
                required_parameters['daily_signal_dates'] = daily_signal_dates

                # daily_signal_values (list): 映射日志的每个日期 (daily_signal_dates) 所对应的信号（日平均）强度值
                # 注意：如果该日期下没有信号强度值，则该值为 0
                required_parameters['daily_signal_values'] = daily_signal_values

                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(df_log)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_signal_daily_average = get_options_signal_daily_average(
                uploaded_file=uploaded_file,
                daily_signal_dates=required_parameters['daily_signal_dates'],
                daily_signal_values=required_parameters['daily_signal_values']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_signal_daily_average, height="500px")

    # “多设备处理” 页面
    class MultipleDevicesProcessing():
        """
        该类用于 “多设备处理” 页面中的数据可视化与分析。
        """

        # Helper function to set ranges based on device indices
        def set_ranges_based_on_device_indices(dfda_log_translated):
             
            device_indices = [f'No.{i}' for i in range(len(dfda_log_translated))]

            return device_indices


        # Helper function to generate dynamic frequency ranges
        def generate_dynamic_freq_ranges(data_series, num_bins=5):
            """
            Generate dynamic frequency thresholds based on data distribution
            
            Args:
                data_series: pandas Series containing the frequency data
                num_bins: number of bins to create (default: 5)
            
            Returns:
                list of tuples: (min_val, max_val, label)
            """

            if len(data_series) == 0:
                return [(0, 1, '1')]
            
            # Get data statistics
            min_val = data_series.min()
            max_val = data_series.max()
            
            # If all values are the same, create a simple threshold
            if min_val == max_val:
                rounded_val = round(min_val)
                return [(0, rounded_val, f'{rounded_val}')]
            
            # Use percentiles to create more meaningful thresholds
            percentiles = [20, 40, 60, 80] if num_bins == 5 else [25, 50, 75]
            thresholds = [data_series.quantile(p/100) for p in percentiles]
            
            # Round up the thresholds for better readability
            rounded_thresholds = []
            for threshold in thresholds:

                # Round up to nearest 5, 10, 25, 50, or 100 depending on magnitude
                if threshold <= 10:
                    rounded = round(threshold)
                elif threshold <= 50:
                    rounded = round(threshold / 5) * 5
                elif threshold <= 200:
                    rounded = round(threshold / 10) * 10
                elif threshold <= 1000:
                    rounded = round(threshold / 25) * 25
                else:
                    rounded = round(threshold / 100) * 100
                rounded_thresholds.append(rounded)
            
            # Ensure we have unique thresholds and add 0 as starting point
            rounded_thresholds = sorted(list(set([0] + rounded_thresholds)))
            
            # Create proper bins with non-overlapping ranges
            freq_ranges = []
            for i in range(len(rounded_thresholds) - 1):

                start = rounded_thresholds[i]
                end = rounded_thresholds[i + 1]
                
                if i == len(rounded_thresholds) - 2:  # Last bin
                    label = f'>{start}'
                else:
                    label = f'{start}-{end}'
                
                freq_ranges.append((start, end, label))
            
            return freq_ranges

        # 生命周期与使用时长-可视化
        @staticmethod
        def visualize_usage_lifecycle(dfda_log_translated: pd.DataFrame):

            def _get_required_parameters(dfda_log_translated):

                required_parameters = {}
                
                usage_months = dfda_log_translated['使用月数']
                            
                min_month = 0
                max_month = int(usage_months.max())               
                month_ranges = []
                month_counts = []
                month_labels = []
                
                for i in range(min_month, max_month + 1):
                    start = i
                    end = i + 1
                    label = f'{start}个月'
                    
                    count = len(usage_months[(usage_months >= start) & (usage_months < end)])
                    
                    month_ranges.append((start, end, label))
                    month_counts.append(count)
                    month_labels.append(label)

                # usage_months (pd.Series): 从处理后的日志分析统计表 (DataFrame) 中提取的 “使用月数” 列
                required_parameters['usage_months'] = usage_months

                # month_labels (list): 根据 usage_months 中的极值月数，生成对应的标签列表，
                # 例如 [0个月, 1个月, 2个月, ..., 12个月]
                required_parameters['month_counts'] = month_counts
                
                # month_counts (list): 根据 usage_months 中的 “使用月数”，生成 month_labels 中对应标签下的计数列表
                required_parameters['month_labels'] = month_labels
                
                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_usage_lifecycle = get_options_usage_lifecycle(
                usage_months=required_parameters['usage_months'],
                month_labels=required_parameters['month_labels'],
                month_counts=required_parameters['month_counts']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_usage_lifecycle, height="400px")

        # 操作类型分布（按设备编号）- 可视化
        @staticmethod
        def visualize_operation_freq_by_device_id(dfda_log_translated: pd.DataFrame):
            
            def _get_required_parameters(dfda_log_translated):

                required_parameters = {}

                all_devices = dfda_log_translated # 重赋值以提升代码可读性
                device_indices = DataAnalyserFrontendAgent.MultipleDevicesProcessing.set_ranges_based_on_device_indices(dfda_log_translated)

                operation_type_cols = ['待机次数', '开闭灌溉次数', '上下线次数']
                operation_series = []

                for i, col in enumerate(operation_type_cols):
                    operation_series.append({
                        "name": col,
                        "type": "bar",
                        "stack": "operation", 
                        "data": all_devices[col].tolist(),
                        "itemStyle": {"color": ["#5470C6", "#91CC75", "#FAC858"][i]}
                    })

                # operation_type_cols (list): 操作类型种类的名称列表，例如 ['待机次数', '开闭灌溉次数', '上下线次数']
                required_parameters['operation_type_cols'] = operation_type_cols

                # device_indices (list): 设备序号列表（即日志参数统计表的 “行”，但从 1 开始编号），
                # 例如 [1, 2, 3, ..., 10]
                required_parameters['device_indices'] = device_indices

                # operation_series (list[dict]): 操作类型序列列表，每个元素是一个字典，
                # 包含构成 “堆叠柱状图 (Stacked Bar)” 的键值对参数
                required_parameters['operation_series'] = operation_series
                
                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_operation_freq_by_device_id = get_options_operation_freq_by_device_id(
                operation_type_cols=required_parameters['operation_type_cols'],
                device_indices=required_parameters['device_indices'],
                operation_series=required_parameters['operation_series']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_operation_freq_by_device_id, height="500px")

        # 操作类型分布（按设备台数）- 可视化
        @staticmethod
        def visualize_operation_freq_by_device_amount(dfda_log_translated: pd.DataFrame):

            def _get_required_parameters(dfda_log_translated):

                required_parameters = {}

                all_devices = dfda_log_translated # 重赋值以提升代码可读性

                operation_freq_data = []
                operation_categories = ['待机次数', '开闭灌溉次数', '上下线次数']
                
                # Generate dynamic ranges based on the first category (can be adjusted)
                dynamic_ranges = DataAnalyserFrontendAgent.MultipleDevicesProcessing.generate_dynamic_freq_ranges(
                    data_series=all_devices[operation_categories[0]],
                    num_bins=5
                )
                
                for col in operation_categories:
                    category_data = []
                    for start, end, label in dynamic_ranges:
                        if '>' in label:  
                            count = len(all_devices[all_devices[col] >= start])
                        else:
                            count = len(all_devices[(all_devices[col] >= start) & (all_devices[col] < end)])
                        category_data.append(count)
                    
                    operation_freq_data.append({
                        "name": col,
                        "type": "bar",
                        "data": category_data,
                        "itemStyle": {"color": ["#5470C6", "#91CC75", "#FAC858"][operation_categories.index(col)]}
                    })
                
                # Extract labels for y-axis
                range_labels = [label for _, _, label in dynamic_ranges]

                # operation_categories (list): 操作类型种类的名称列表，例如 ['待机次数', '开闭灌溉次数', '上下线次数']
                required_parameters['operation_categories'] = operation_categories

                # range_labels (list): 操作类型频次范围的标签列表（可以不均匀），即通过动态切割生成，例如 ['0-10', '10-100', '100-1000']
                required_parameters['range_labels'] = range_labels

                # operation_freq_data (list[dict]): 操作类型频次数据列表，每个元素是一个字典，包含构成 “群组柱状图 (Grouped Bar)” 的键值对参数
                required_parameters['operation_freq_data'] = operation_freq_data

                return required_parameters
            
            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated)
            
            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_operation_freq_by_device_amount = get_options_operation_freq_by_device_amount(
                operation_categories=required_parameters['operation_categories'],
                range_labels=required_parameters['range_labels'],
                operation_freq_data=required_parameters['operation_freq_data']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_operation_freq_by_device_amount, height="500px")

        # 信号强度分布（按设备编号）- 可视化
        @staticmethod
        def visualize_signal_freq_by_device_id(dfda_log_translated: pd.DataFrame):
            
            def _get_required_parameters(dfda_log_translated):

                required_parameters = {}

                all_devices = dfda_log_translated # 重赋值以提升代码可读性
                device_indices = DataAnalyserFrontendAgent.MultipleDevicesProcessing.set_ranges_based_on_device_indices(dfda_log_translated)

                signal_cols = ['强信号次数', '中等强度次数', '弱/无强度次数']
                signal_series = []

                for i, col in enumerate(signal_cols):
                    signal_series.append({
                        "name": col,
                        "type": "bar",
                        "stack": "signal",
                        "data": all_devices[col].tolist(),
                        "itemStyle": {"color": ["#FF6B6B", "#4ECDC4", "#45B7D1"][i]}
                    })

                # signal_cols (list): 信号强度种类的名称列表，例如 ['强信号次数', '中等强度次数', '弱/无强度次数']
                required_parameters['signal_cols'] = signal_cols

                # device_indices (list): 设备序号列表（即日志参数统计表的 “行”，但从 1 开始编号），例如 [1, 2, 3, ..., 10]
                required_parameters['device_indices'] = device_indices

                # signal_series (list[dict]): 信号强度序列列表，每个元素是一个字典，包含构成 “堆叠柱状图 (Stacked Bar)” 的键值对参数
                required_parameters['signal_series'] = signal_series

                return required_parameters
            
            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated)
            
            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_signal_freq_by_device_id = get_options_signal_freq_by_device_id(
                signal_cols=required_parameters['signal_cols'],
                device_indices=required_parameters['device_indices'],
                signal_series=required_parameters['signal_series']
            )
            
            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_signal_freq_by_device_id, height="500px")

        # 信号强度分布（按设备台数）- 可视化
        @staticmethod
        def visualize_signal_freq_by_device_amount(dfda_log_translated: pd.DataFrame):

            def _get_required_parameters(dfda_log_translated):

                required_parameters = {}

                all_devices = dfda_log_translated # 重赋值以提升代码可读性

                signal_freq_data = []
                signal_categories = ['强信号次数', '中等强度次数', '弱/无强度次数']
                
                # Generate dynamic ranges based on the first signal category
                signal_dynamic_ranges = DataAnalyserFrontendAgent.MultipleDevicesProcessing.generate_dynamic_freq_ranges(
                    data_series=all_devices[signal_categories[0]],
                    num_bins=5
                )
                
                for col in signal_categories:
                    category_data = []
                    for start, end, label in signal_dynamic_ranges:
                        if '>' in label:  
                            count = len(all_devices[all_devices[col] >= start])
                        else:
                            count = len(all_devices[(all_devices[col] >= start) & (all_devices[col] < end)])
                        category_data.append(count)
                    
                    signal_freq_data.append({
                        "name": col,
                        "type": "bar",
                        "data": category_data,
                        "itemStyle": {"color": ["#FF6B6B", "#4ECDC4", "#45B7D1"][signal_categories.index(col)]}
                    })
                
                # Extract labels for y-axis
                signal_range_labels = [label for _, _, label in signal_dynamic_ranges]

                # signal_categories (list): 信号强度种类的名称列表，例如 ['强信号次数', '中等强度次数', '弱/无强度次数']
                required_parameters['signal_categories'] = signal_categories

                # range_labels (list): 信号强度频次范围的标签列表（可以不均匀），即通过动态切割生成，例如 ['0-10', '10-100', '100-1000']
                required_parameters['signal_range_labels'] = signal_range_labels

                # signal_freq_data (list[dict]): 信号强度频次数据列表，每个元素是一个字典，包含构成 “群组柱状图 (Grouped Bar)” 的键值对参数
                required_parameters['signal_freq_data'] = signal_freq_data

                return required_parameters

            # 第一步：根据日志统计表，获取必要的参数
            required_parameters = _get_required_parameters(dfda_log_translated)

            # 第二步：获取 ECharts 基于 JavaScript 风格的配置项 (Options)
            options_signal_freq_by_device_amount = get_options_signal_freq_by_device_amount(
                signal_categories=required_parameters['signal_categories'],
                signal_range_labels=required_parameters['signal_range_labels'],
                signal_freq_data=required_parameters['signal_freq_data']
            )

            # 第三步：使用 Streamlit 的第三方容器 (ECharts) 以可视化图表    
            st_echarts(options=options_signal_freq_by_device_amount, height="500px")
