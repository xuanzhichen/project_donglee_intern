"""
Class-DataAnalyser (类-数据分析) 的实现 (快照版: demo_data_analysis.py)

该类编写了关于 —— 智云公司的智能控制器产品的 —— 日志数据分析的业务逻辑，是构成整个项目后端的中心。
然而，其实现不涉及繁杂的数理统计，而是侧重于对产品业务的理解，并根据其业务需求调整相应的计算逻辑。

其原型是该项目的 experiment 文件夹下，jupyter notebook 中一系列代码的集合。
后来为了开发智云公司的 web 端应用，进行了优化和封装。
"""

# Author: Xuanzhi Chen (陈炫志)
# Email: xuanzhichen.42@gmail.com
# License: MIT

# Latest Update: 2025/07/03


import pandas as pd


class DataAnalyser():
    """
    DataAnalyser is designed to take your initialized dataframe in,
    running certain expected processing framework to get insights into the massive and dirty log data,
    and return a statistic sheet as either the quantitative testimony or the source for data visualization.

    DataAnalyser 被设计为接受一个初始化的 dataframe 作为输入 (该 dataframe 包含了我的实习雇主期望了解的特征),
    运行某种预期的处理框架以获取对大量脏乱日志数据的觉察,
    并返回一个统计表 (df_data_analysis) 作为我的实习雇主所需要的定量证据，或作为可用于可视化的数据来源。
    """

    # Latest update: 2025-05-13
    def __init__(self, df_data_analysis):

        self._df_data_analysis = df_data_analysis

    # Latest update: 2025-06-20
    def identify_id_info(
            self, 
            df_device_log,
            use_index: False,
            index: None,
            device_name: None,
            imei: None
    ):
        """
        特别提醒关于 use_index: 历史原因；当处理单设备日志时，所有的 "标识列" 数值都是一样的
        """
        self._device_name = device_name
        self._df_device_log = df_device_log

        self._use_index = use_index
        self._index = index
        self._imei = imei

        # Create a mask once and reuse it to speed up the process
        if self._device_name is not None:
            self._mask = self._df_data_analysis['device_name'] == self._device_name
        else: # imei for identify
            self._mask = self._df_data_analysis['imei'] == self._imei

        # Filter the dataframe to only include rows where operation is '设备状态'
        # A non-null value of signal_strength is only recorded when the operation is '设备状态'
        self._df_device_log_standby = self._df_device_log[self._df_device_log['操作类型'] == '设备状态']
        # self._df_device_log_standby = self._df_device_log[self._df_device_log['operation'] == '设备状态']
        
        return self
    
    # Latest update: 2025-06-20
    def get_usage_period(self):
        if self._use_index:
            # Get the first (and should be only) value using index
            downtime = self._df_data_analysis.loc[self._index, 'downtime']
            uptime = self._df_data_analysis.loc[self._index, 'uptime']

        else:
            downtime = self._df_data_analysis.loc[self._mask, 'downtime'].iloc[0]
            uptime = self._df_data_analysis.loc[self._mask, 'uptime'].iloc[0]
            
        # Calculate the time difference between downtime and uptime in days and in months
        if downtime == uptime:
            days_len = 1
        else:
            days_len = abs((downtime - uptime).days)
            
        months_len = days_len // 30

        # Update days_len and months_len for the specified device
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'days_len'] = days_len
            self._df_data_analysis.loc[self._index, 'months_len'] = months_len

        else:
            self._df_data_analysis.loc[self._mask, 'days_len'] = days_len
            self._df_data_analysis.loc[self._mask, 'months_len'] = months_len

        return self
    
    # Latest update: 2025-06-25
    def get_sub_log_based_on_usage_period(self):
        """
        Implement this function immediately after running 'get_usage_period'.

        事实上先获取子日志再根据其起始范围获取使用天数和使用月数是可以的，因为这两个特征仅仅涉及字面上的加减运算，
        不涉及日志范围内的计数和统计。同时，由于历史原因，“使用天数” 和 “使用月数” 作为统计表最靠前的两个特征，
        其在类里面的实现方式被我过早地确定了，我也就遵守这个顺序了。
        """
        # Get downtime and uptime timestamps from df_data_analysis
        if self._use_index:
            downtime = self._df_data_analysis.loc[self._index, 'downtime']
            uptime = self._df_data_analysis.loc[self._index, 'uptime']
        else:
            downtime = self._df_data_analysis.loc[self._mask, 'downtime'].iloc[0]
            uptime = self._df_data_analysis.loc[self._mask, 'uptime'].iloc[0]
            # downtime = self._df_data_analysis.loc[self._mask, 'downtime']
            # uptime = self._df_data_analysis.loc[self._mask, 'uptime']
        
        # Normalize timestamps to date-only and filter the device log based on the time range
        self._df_device_log = self._df_device_log[
            (pd.to_datetime(self._df_device_log['创建时间']).dt.date <= pd.to_datetime(downtime).date()) &
            (pd.to_datetime(self._df_device_log['创建时间']).dt.date >= pd.to_datetime(uptime).date())
        ]

        # Update the df_device_log_standby
        self._df_device_log_standby = self._df_device_log[self._df_device_log['操作类型'] == '设备状态']
        # self._df_device_log_standby = self._df_device_log[self._df_device_log['operation'] == '设备状态']

        return self
    
    # Latest update: 2025-05-19
    def get_log_len(self):
        log_len = len(self._df_device_log)
        self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'log_len'
        ] = log_len

        return self

    # Latest update: 2025-05-12
    def get_downtime_uptime(self):  
        # Define downtime (or current time if normal functionality) and uptime
        downtime = pd.to_datetime(self._df_device_log['create_time'].iloc[0])
        uptime = pd.to_datetime(self._df_device_log['create_time'].iloc[-1])

        # Update downtime and uptime for the specified device
        self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'downtime'
        ] = pd.to_datetime(downtime.date())

        self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'uptime'
        ] = pd.to_datetime(uptime.date())

        return self

    # Latest update: 2025-05-12
    def get_month_len_include_break(self):  
        """该函数已弃用"""
        # Get the first (and should be only) value
        downtime = self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'downtime'
        ].iloc[0]
        uptime = self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'uptime'
        ].iloc[0]
        
        # Calculate the time difference between downtime and uptime in months
        days_len = abs((downtime - uptime).days)
        months_len = days_len // 30

        # Update months_len for the specified device
        self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'months_len'
        ] = months_len

        return self

    # Latest update: 2025-07-03
    def get_month_len_exclude_break(self, days_break_threshold=2, threshold_days_for_excluding=30):
        if self._use_index:
            # Initialize months_len_exclude_breaks assuming no breaks
            months_len_include_breaks = self._df_data_analysis.loc[
                self._index, 'months_len'
            ]
            self._df_data_analysis.loc[
                self._index, 'months_len_exclude_breaks'
            ] = months_len_include_breaks

        else:
            months_len_include_breaks = self._df_data_analysis.loc[
                self._mask, 'months_len'
            ].iloc[0]
            self._df_data_analysis.loc[
                self._mask, 'months_len_exclude_breaks'
            ] = months_len_include_breaks

        # Sort the dataframe by create_time to ensure chronological order
        df_sorted = self._df_device_log.copy()
        df_sorted['create_time'] = pd.to_datetime(df_sorted['create_time'])
        df_sorted = df_sorted.sort_values('create_time')

        # Calculate the time difference between consecutive records
        df_sorted['time_diff'] = df_sorted['create_time'].diff()

        # Find gaps larger than the days_break_threshold
        large_gaps = df_sorted[df_sorted['time_diff'] > pd.Timedelta(days=days_break_threshold)]
        
        if not large_gaps.empty:

            # Find the maximum gap in days and update max_days_break
            max_gap_days = large_gaps['time_diff'].max().days

            # Calculate the total days of breaks
            total_days_breaks = large_gaps['time_diff'].sum().days

            if self._use_index:
                # Count the number of large gaps and update num_days_break
                self._df_data_analysis.loc[self._index, 'num_days_breaks'] = len(large_gaps)
                self._df_data_analysis.loc[self._index, 'max_days_break'] = max_gap_days
                self._df_data_analysis.loc[self._index, 'total_days_breaks'] = total_days_breaks
            else:
                self._df_data_analysis.loc[self._mask, 'num_days_breaks'] = len(large_gaps)
                self._df_data_analysis.loc[self._mask, 'max_days_break'] = max_gap_days
                self._df_data_analysis.loc[self._mask, 'total_days_breaks'] = total_days_breaks
            
            # # Check if there are gaps over 3 days outside the holiday period (2024-12-31 to 2025-01-07)
            # holiday_start = pd.Timestamp('2024-12-31')
            # holiday_end = pd.Timestamp('2025-01-07')
            
            # for idx, row in large_gaps.iterrows():
            #     gap_start = row['create_time'] - row['time_diff']
            #     gap_end = row['create_time']
                
            #     # Check if the gap is completely outside the holiday period
            #     # and update continued_status
            #     if (gap_end < holiday_start) or (gap_start > holiday_end):
            #         df_ev_haida_data_analysis.loc[
            #             df_ev_haida_data_analysis['device_name'] == device_name, 'continued_status'
            #         ] = 'no'
            #         break
            #     # Check if the gap extends beyond the holiday period
            #     # and update continued_status
            #     elif (gap_start < holiday_start and gap_end > holiday_start) or \
            #             (gap_start < holiday_end and gap_end > holiday_end):
            #         df_ev_haida_data_analysis.loc[
            #             df_ev_haida_data_analysis['device_name'] == device_name, 'continued_status'
            #         ] = 'no'
            #         break

            # Update months_len_exclude_breaks
            if total_days_breaks > threshold_days_for_excluding:
                month_breaks = total_days_breaks // 30
                months_len_exclude_breaks = months_len_include_breaks - month_breaks

                if self._use_index:
                    self._df_data_analysis.loc[
                        self._index, 'months_len_exclude_breaks'
                    ] = months_len_exclude_breaks
                else:
                    self._df_data_analysis.loc[
                        self._mask, 'months_len_exclude_breaks'
                    ] = months_len_exclude_breaks

        return self
    
    # Latest update: 2025-05-13
    def get_continued_status(self, broken_down_threshold=30):
        max_days_break = self._df_data_analysis.loc[
            self._df_data_analysis['device_name'] == self._device_name, 'max_days_break'
        ].iloc[0]

        if max_days_break >= broken_down_threshold:
            self._df_data_analysis.loc[
                self._df_data_analysis['device_name'] == self._device_name, 'continued_status'
        ] = 'F'

        return self
    
    # Latest update: 2025-06-25
    def get_operation_status(self):
        # times_of_standby = len(self._df_device_log[self._df_device_log['operation'] == '设备状态'])
        # times_of_irrigation_start = len(self._df_device_log[self._df_device_log['operation'] == '开启灌溉'])
        # times_of_irrigation_close = len(self._df_device_log[self._df_device_log['operation'] == '关闭灌溉'])
        # times_of_uptime = len(self._df_device_log[self._df_device_log['operation'] == '设备上线'])
        # times_of_downtime = len(self._df_device_log[self._df_device_log['operation'] == '设备下线'])

        times_of_standby = len(self._df_device_log[self._df_device_log['操作类型'] == '设备状态'])
        times_of_irrigation_start = len(self._df_device_log[self._df_device_log['操作类型'] == '开启灌溉'])
        times_of_irrigation_close = len(self._df_device_log[self._df_device_log['操作类型'] == '关闭灌溉'])
        times_of_uptime = len(self._df_device_log[self._df_device_log['操作类型'] == '设备上线'])
        times_of_downtime = len(self._df_device_log[self._df_device_log['操作类型'] == '设备下线'])

        # Update times_of_standby (设备状态)
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_standby'] = times_of_standby
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_standby'] = times_of_standby
 
        # Update times_of_irrigation_start (开启灌溉)
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_irrigation_start'] = times_of_irrigation_start
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_irrigation_start'] = times_of_irrigation_start

        # Update times_of_irrigation_close (关闭灌溉)
        # Notes: This record will finally be deleted for CH translation simplicity, however
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_irrigation_close'] = times_of_irrigation_close
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_irrigation_close'] = times_of_irrigation_close

        # Update times_of_uptime (设备上线)
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_uptime'] = times_of_uptime
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_uptime'] = times_of_uptime

        # Update times_of_downtime (设备下线)
        # Notes: This record will finally be deleted for CH translation simplicity, however
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_downtime'] = times_of_downtime
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_downtime'] = times_of_downtime

        return self
    
    # Latest update: 2025-06-26
    def get_signal_strength_frequency(self):
        # Instead of looping through rows, vectorized operations for signal statistics
        signal_strength = self._df_device_log_standby['信号']
        # signal_strength = self._df_device_log_standby['signal_strength']

        # Count strong signals (>= 21.5)
        strong_signals = (signal_strength >= 21.5).sum()
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_strong_signal'] = strong_signals
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_strong_signal'] = strong_signals
        
        # Count medium signals (>= 11.5 and < 21.5)
        mid_signals = ((signal_strength >= 11.5) & (signal_strength < 21.5)).sum()
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_mid_signal'] = mid_signals
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_mid_signal'] = mid_signals
        
        # Count weak signals (>= 1.5 and < 11.5)
        weak_signals = ((signal_strength >= 1.5) & (signal_strength < 11.5)).sum()
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_weak_signal'] = weak_signals
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_weak_signal'] = weak_signals
        
        # Count null signals (< 1.5)
        null_signals = (signal_strength < 1.5).sum()
        if self._use_index:
            self._df_data_analysis.loc[self._index, 'times_of_null_signal'] = null_signals
        else:
            self._df_data_analysis.loc[self._mask, 'times_of_null_signal'] = null_signals

        # Calculate some basic statistics (if there are numeric values)
        if self._use_index:
            if signal_strength.empty:
                pass
            else:
                self._df_data_analysis.loc[self._index, 'average_signal'] = round(signal_strength.mean(), 2)
                self._df_data_analysis.loc[self._index, 'min_signal'] = signal_strength.min()
                self._df_data_analysis.loc[self._index, 'max_signal'] = signal_strength.max()
        else:
            if signal_strength.empty:
                pass
            else:
                self._df_data_analysis.loc[self._mask, 'average_signal'] = round(signal_strength.mean(), 2)
                self._df_data_analysis.loc[self._mask, 'min_signal'] = signal_strength.min()
                self._df_data_analysis.loc[self._mask, 'max_signal'] = signal_strength.max()

        return self

    # Latest update: 2025-06-26
    def get_signal_switch_frequency(self, window_len=2):
        # Function to determine which interval a signal value falls into
        def get_signal_strength_category(signal_value):
            if 0< signal_value < 1.5:
                return "null"
            elif 1.5 <= signal_value < 11.5:
                return "weak"
            elif 11.5 <= signal_value < 21.5:
                return "mid"
            else: # 21.5 <= signal_value < float('inf')
                return "strong"
            
        # Define the order: strong > mid > weak > null
        strength_order = {"strong": 3, "mid": 2, "weak": 1, "null": 0}

        # Get signal strength values as a list for easier iteration
        signal_values = self._df_device_log_standby['信号'].tolist()
        # signal_values = self._df_device_log_standby['signal_strength'].tolist()
        
        # Iterate through adjacent signal values
        for i in range(len(signal_values) - 1):
            current_signal = signal_values[i]
            next_signal = signal_values[i + (window_len - 1)]
            # next_signal = signal_values[i + 1]
            
            # Determine which intervals the signals fall into
            current_interval = get_signal_strength_category(current_signal)
            next_interval = get_signal_strength_category(next_signal)
            
            # Skip if both signals fall into the same interval
            if current_interval == next_interval:
                continue
            # Sort different intervals (strong > mid > weak > null) to ensure consistent column
            else:
                intervals = sorted([current_interval, next_interval], 
                                key=lambda x: strength_order[x], 
                                reverse=True)
                column_name = f'times_signal_switch_{intervals[0]}_{intervals[1]}'
                
                # Update the counter for the specific switch type
                if self._use_index:
                    self._df_data_analysis.loc[self._index, column_name] += 1
                else:
                    self._df_data_analysis.loc[self._mask, column_name] += 1
             
        return self
