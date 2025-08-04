"""
Class-PagesDataAnalysis (类-数据分析页面) 的实现

该类封装了 “单设备处理” 和 “多设备处理” 两个页面，并提供了相应的数据分析（通过后端代理实现）和数据可视化（通过前端代理实现）功能。

需要指出的是，类中的页面渲染模块 (render) 有一定的冗杂性，因为在母页面 portal_page.py 的早期实现中，
我还不了解可以直接通过 Streamlit 内置的 “Page” 对象实现页面的渲染和跳转，而无须自定义 “页面渲染” 方法和自编写条件语句。
"""

# Author: Xuanzhi Chen (陈炫志)
# Email: xuanzhichen.42@gmail.com
# License: MIT

# Latest Update: 2025/07/29


import pandas as pd
import zipfile
import io
import time

import streamlit as st

from app.my_backend_agent import DataAnalyserBackendAgent
from app.my_frontend_agent import DataAnalyserFrontendAgent


class PagesDataAnalysis:
    @staticmethod
    def render(page_title):

        if page_title == '单设备处理':
            PagesDataAnalysis._render_the_2th_page()

        if page_title == '多设备处理':
            PagesDataAnalysis._render_the_3rd_page()

    @staticmethod
    def _build_an_index_table(
        df_log: pd.DataFrame, 
        uploaded_file: pd.ExcelFile, 
        pattern_choice: str
    ):
        # Check existence for identification columns: 'imei/IMEI', 'device name/设备ID'
        # 对上传的日志文件，检查 (excel) 这些“标识列”的数值存在性：imei/IMEI', 'device name/设备ID'
        format_checked = DataAnalyserBackendAgent.check_id_existence(df_log, uploaded_file)

        # Initialize an index table for the identification columns of (multiple) devices,
        # which is useful for finding and extracting the corresponding log data in (multiple) devices
        # 初始化一张关于（多）设备 “标识列” 的索引表，便于（在多设备情况下）查找和提取对应的日志数据
        dfda_log = DataAnalyserBackendAgent.index_a_dfda_log(df_log, format_checked)

        # We use the difference between the offline time and the online time to define the usage period of the device,
        # but in actual use, due to reasons such as battery replacement, the device will go offline and the log will be interrupted,
        # which will affect the accuracy of the calculation; we need to define the online and offline times according to specific needs (pattern)
        # 我们采用日志的下线时间减去上线时间，来定义设备的使用周期，
        # 但是由于实际使用中，中途更换电池等原因会导致设备离线和日志中断（缺失），从而影响计算的准确性
        # 因此需要根据需求 (pattern) 定义好上线和下线时间，以排除这些因素的影响
        dfda_log = DataAnalyserBackendAgent.define_uptime_and_downtime(
            dfda_log, 
            df_log, 
            pattern=pattern_choice,
        )

        return dfda_log
    
    @staticmethod
    def _conduct_the_pipeline(data_analyser: DataAnalyserBackendAgent):

        # Simply calculate the life-cycle in months
        # 简单地计算设备的使用生命周期 (下线时间与上线时间之差)
        data_analyser.get_usage_period()

        # data_analyser.get_month_len_include_break() # 该函数已弃用

        # if pattern_choice == 'multiple_files_single_period':
        #
        #     # Calculate the life-cycle with consideration of day-break events
        #     # 考虑在设备的整个生命周期内，是否出现显著的日志间断现象，以计算实际的使用生命周期
        #     data_analyser.get_month_len_exclude_break(
        #         days_break_threshold=2, 
        #         threshold_days_for_excluding=30
        #     )

        #     # Mark the log characteristic as 'Not continued' if maximal broken days over the threshold
        #     # 如果最大间隔天数超过设定阈值，标记该设备的日志属性为 “不连续”
        #     data_analyser.get_continued_status(broken_down_threshold=15)

        # Single device processing: Backend program will default to scan and detect the interruption of a single log, and extract all continuous time ranges
        # Multiple device processing: User may customize the interested time range through the selection of different processing patterns (pattern_choice)
        # Then: The corresponding time range needs to be extracted as the subsequent parameter statistics space (such as: signal frequency)
        # 单设备处理：后端程序会默认扫描和检测单个日志下的中断情况，并提取所有连续的时长范围
        # 多设备处理：用户可以通过选择不同的处理模式 (pattern_choice) 自定义感兴趣的时长范围
        # 需要据此提取出对应时长范围的 “子日志” (sub-log)，并将该范围作为后续的参数统计空间 (如：信号频次)
        data_analyser.get_sub_log_based_on_usage_period()

        # Count the frequency of the five operation status recorded in the log over the life-cycle 
        # 统计日志记录中五种操作状态 (灌溉开启/灌溉关闭/上线/离线/待机) 在设备生命周期内出现的频次
        data_analyser.get_operation_status()

        # Count the frequency of the four categorizes of signal strength (strong/mid/weak/null)
        # recorded in the log over the life-cycle
        # 统计日志记录中四种信号强度 (强信号/中信号/弱信号/无信号) 在设备生命周期内出现的频次 
        data_analyser.get_signal_strength_frequency()

        # Count the frequency of the cases in which a device went through significant signal switches
        # 统计日志记录中 (相邻的两个时间戳下) 设备显著切换信号强度的频次
        data_analyser.get_signal_switch_frequency(window_len=2) 

    @staticmethod
    def _visualize_usage_track(dfda_log_translated: pd.DataFrame, df_log: pd.DataFrame):

        DataAnalyserFrontendAgent.SingleDeviceProcessing.visualize_usage_track(
            dfda_log_translated=dfda_log_translated,
            df_log=df_log,
        )

    @staticmethod
    def _visualize_operation_real_time(df_log: pd.DataFrame, uploaded_file):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        DataAnalyserFrontendAgent.SingleDeviceProcessing.visualize_operation_real_time(
            df_log=df_log,
            uploaded_file=uploaded_file
        )

    @staticmethod
    def _visualize_signal_real_time(df_log: pd.DataFrame, uploaded_file):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        DataAnalyserFrontendAgent.SingleDeviceProcessing.visualize_signal_real_time(
            df_log=df_log,
            uploaded_file=uploaded_file
        )

    @staticmethod
    def _visualize_operation_daily_average(df_log: pd.DataFrame, uploaded_file):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        DataAnalyserFrontendAgent.SingleDeviceProcessing.visualize_operation_daily_average(
            df_log=df_log,
            uploaded_file=uploaded_file
        )

    @staticmethod
    def _visualize_signal_daily_average(df_log: pd.DataFrame, uploaded_file):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        DataAnalyserFrontendAgent.SingleDeviceProcessing.visualize_signal_daily_average(
            df_log=df_log,
            uploaded_file=uploaded_file
        )
    
    @staticmethod
    def _visualize_usage_lifecycle(dfda_log_translated: pd.DataFrame):

        DataAnalyserFrontendAgent.MultipleDevicesProcessing.visualize_usage_lifecycle(
            dfda_log_translated=dfda_log_translated
        )

    @staticmethod
    def _visualize_operation_freq_by_device_id(dfda_log_translated: pd.DataFrame):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

        DataAnalyserFrontendAgent.MultipleDevicesProcessing.visualize_operation_freq_by_device_id(
            dfda_log_translated=dfda_log_translated
        )

    @staticmethod
    def _visualize_operation_freq_by_device_amount(dfda_log_translated: pd.DataFrame):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        DataAnalyserFrontendAgent.MultipleDevicesProcessing.visualize_operation_freq_by_device_amount(
            dfda_log_translated=dfda_log_translated
        )

    @staticmethod
    def _visualize_signal_freq_by_device_id(dfda_log_translated: pd.DataFrame):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        DataAnalyserFrontendAgent.MultipleDevicesProcessing.visualize_signal_freq_by_device_id(
            dfda_log_translated=dfda_log_translated
        )

    @staticmethod
    def _visualize_signal_freq_by_device_amount(dfda_log_translated: pd.DataFrame):

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        DataAnalyserFrontendAgent.MultipleDevicesProcessing.visualize_signal_freq_by_device_amount(
            dfda_log_translated=dfda_log_translated
        )

    @staticmethod
    def _render_the_2th_page(): # Page title: 单设备处理

        # st.title("单设备处理")
        # st.markdown("---")

        uploaded_file = st.file_uploader(
            label="请将您感兴趣的日志（仅限xlsx文件）拖放到此处：", 
            type="xlsx", 
            accept_multiple_files=False
        )

        # Manufacture a file-like object for default status
        if uploaded_file is None:

            default_path = "../data/testing_instances_for_app/智能控制器样例日志（简化测试版）.xlsx"

            with open(default_path, "rb") as f:
                file_bytes = f.read()

            uploaded_file = io.BytesIO(file_bytes)
            uploaded_file.name = "智能控制器样例日志（简化测试版）.xlsx"

            # st.markdown(
            #     ":orange-background[:warning: 如下一份智能控制器的样例日志已被预加载，"
            #     "以向您演示处理效果]；**请上传并覆盖为您感兴趣的日志**"
            # )
            st.markdown("### 样例日志（预加载）")
            st.markdown(f"文件名（类型）：`{uploaded_file.name}`")
            st.dataframe(pd.read_excel(uploaded_file), use_container_width=True)
        
        df_log = pd.read_excel(uploaded_file)

        dfda_log = PagesDataAnalysis._build_an_index_table(
            df_log, 
            uploaded_file, 
            pattern_choice='single_file_multiple_periods'
        )

        # Implement data analysis logic for each device log
        data_analyser = DataAnalyserBackendAgent(dfda_log)

        for index, row in dfda_log.iterrows():

            # We don't need to pass the device_name or imei, as they are same for single device log
            # device_name = row['device_name']
            # imei = row['imei']

            # Instead, we need to pass the index to identity the row
            data_analyser.identify_id_info(
                df_device_log=df_log, 
                use_index=True, 
                index=index,
                device_name=None,
                imei=None
            )

            PagesDataAnalysis._conduct_the_pipeline(data_analyser)

        dfda_log_updated = data_analyser._df_data_analysis
        dfda_log_translated = DataAnalyserBackendAgent.translate_and_mildly_modify_your_df(dfda_log_updated)

        st.markdown("### 基于日志的参数统计表")

        # st.dataframe(dfda_log_updated, use_container_width=True) # temp code for debugging

        # st.dataframe(dfda_log_translated, use_container_width=True)
        
        st.data_editor(
            dfda_log_translated,
            use_container_width=True,
            column_config={
                "device_name": st.column_config.Column(width=150),
            }
        )

        st.markdown("### 基于日志的可视化与分析")

        st.markdown("#### A. 生命周期与使用时长")

        PagesDataAnalysis._visualize_usage_track(dfda_log_translated, df_log)

        st.markdown("#### B. 操作类型与信号强度")

        status_chart_type = st.selectbox(

            '请选择对控制器的重要特征（操作类型，信号强度）的可视化方式',
            ('实时（即展示所有日志记录）', '日均（即展示每日最频繁的操作类型，或每日的平均信号强度）'),
            key='status_chart_type'

        )
            
        if status_chart_type == '实时（即展示所有日志记录）':

            PagesDataAnalysis._visualize_operation_real_time(df_log, uploaded_file)
            
            PagesDataAnalysis._visualize_signal_real_time(df_log, uploaded_file)

        else:

            PagesDataAnalysis._visualize_operation_daily_average(df_log, uploaded_file)

            PagesDataAnalysis._visualize_signal_daily_average(df_log, uploaded_file)

    @staticmethod
    def _render_the_3rd_page(): # Page title: 多设备处理
        """
        渲染页面：多设备处理
        “后端调用” - 数据分析：
        “前端调用” - 数据可视化：
        """

        # The following three vars coordinate and control the launch of data processing each time,
        # avoiding unnecessary re-processing of data and re-rendering of the current page
        if 'pattern_choice' not in st.session_state:
            st.session_state.pattern_choice = None
        if 'current_pattern' not in st.session_state:
            st.session_state.current_pattern = None
        if 'data_processed' not in st.session_state:
            st.session_state.data_processed = False
        if 'current_file' not in st.session_state: 
            st.session_state.current_file = "智能控制器样例日志（简化测试版）.zip"

        # st.markdown("---")
        # st.header("多设备处理")

        uploaded_file = st.file_uploader(
            label="请将您感兴趣的日志（仅限zip压缩文件）拖放到此处：", 
            type="zip", 
            accept_multiple_files=False
        )
        
        # if uploaded_file is not None:

        if uploaded_file is None:

            default_path = "../data/testing_instances_for_app/智能控制器样例日志（简化测试版）.zip"

            with open(default_path, "rb") as f:
                file_bytes = f.read()

            uploaded_file = io.BytesIO(file_bytes)
            uploaded_file.name = "智能控制器样例日志（简化测试版）.zip"

            # st.markdown(
            #     ":orange-background[:warning: 如下一份智能控制器的样例日志已被预加载，"
            #     "以向您演示处理效果]；**请上传并覆盖为您感兴趣的日志**"
            # )
            st.markdown("### 样例日志（预加载）")
            st.markdown(f"文件名（类型）：`{uploaded_file.name}`")
            st.image(
                "image/testing_instance.png", 
                caption="内含 10 个智能控制器日志的样例压缩包，每个日志文件的格式与“单设备处理”模块中的（预加载）样例相同",
                # width=700
            )

        # Reset session state when a new file is uploaded, 
        # or when a new (data processing) pattern is chosen
        if 'cache_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
            st.session_state.cache_file = st.session_state.current_file
            st.session_state.current_file = uploaded_file.name
            st.session_state.data_processed = False
            st.session_state.current_pattern = None
            st.session_state.pattern_choice = None

        # Read the zip package expected to contain multiple log files related to multiple devices
        zip_data = uploaded_file.read()
        zip_buffer = io.BytesIO(zip_data)
        
        # Extract files from the zip package
        with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
            
            file_list = zip_ref.namelist()
            xlsx_files = [f for f in file_list if f.endswith('.xlsx')]
            
            # Process each extracted xlsx file
            if xlsx_files:

                if st.session_state.current_file == "智能控制器样例日志（简化测试版）.zip":
                    st.markdown(
                        "请选择对每个控制器使用时长的计算模式 (A/B/C)：",
                        help="不同的计算模式将得出不同的使用时长范围，而不同的范围会影响后续的参数统计空间（如：信号频次）。\
                            更具体的解释可在 “操作说明” 页面里找到。"
                    )
                else:
                    st.markdown(
                        "文件上传成功！请选择对每个控制器使用时长的计算模式 (A/B/C)：",
                        help="不同的计算模式将得出不同的使用时长范围，而不同的范围会影响后续的参数统计空间（如：信号频次）。\
                            更具体的解释可在 “操作说明” 页面里找到。"
                    )
                
                pattern_options = {
                    "multiple_files_single_period": "A. 总计累积使用时长", 
                    "multiple_files_latest_period": "B. 最后一次连续使用时长", 
                    "multiple_files_max_period": "C. 最长一次连续使用时长"
                }

                # Render pattern choice buttons
                cols = st.columns(3) 
                for i, (key, label) in enumerate(pattern_options.items()):
                    with cols[i]:
                        if st.button(
                            label, 
                            key=f"pattern_{i}", 
                            use_container_width=True,
                            # help="选择不同的处理模式会影响设备上线和下线时间的定义方式"
                        ):
                            st.session_state.pattern_choice = key

                # # Explicitly retrieve the pattern_choice from session state
                # pattern_choice = st.session_state.pattern_choice

                if uploaded_file.name == "智能控制器样例日志（简化测试版）.zip" and not st.session_state.data_processed:
                    pattern_choice = "multiple_files_single_period"
                else:
                    pattern_choice = st.session_state.pattern_choice
                
                # Check if pattern choice has changed and reset data processing flag(s)
                if pattern_choice is not None and pattern_choice != st.session_state.current_pattern:
                    st.session_state.current_pattern = pattern_choice
                    st.session_state.data_processed = False
                
                # Launch data processing for either the first time,
                # or when the pattern choice has changed by users,
                # or when a new file is uploaded
                if pattern_choice is not None and not st.session_state.data_processed:

                    # st.markdown("---")
                    # st.subheader("基于日志的参数统计表")

                    # Add progress indicator
                    # if len(xlsx_files) > 5：
                    progress_info = st.info(" 批量处理多设备日志可能耗时较久，请耐心等候...", icon="ℹ️")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Initialize an empty dataframe to store the index table of 'whole' devices (rows),
                    # as well as results of data analysis for each 'individual' device (columns)
                    # dfda: Device Log Data Analysis
                    dfda_log_whole = pd.DataFrame()
                    
                    status_text.text("初始化：正在为日志数据构建设备索引表...")
                    for i, xlsx_file in enumerate(xlsx_files):

                        # First half of progress: Pre-processing
                        progress_bar.progress((i + 1) / (len(xlsx_files) * 2))  
                        
                        with zip_ref.open(xlsx_file) as uploaded_file:

                            df_log = pd.read_excel(uploaded_file)

                            dfda_log_individual = PagesDataAnalysis._build_an_index_table(
                                df_log, 
                                uploaded_file, 
                                pattern_choice=pattern_choice
                            )

                            # Merge the index tables of each device
                            dfda_log_whole = DataAnalyserBackendAgent.concat_dfda_log(
                                dfda_log_whole, dfda_log_individual
                            )

                    # Rename the index table for readability
                    dfda_log = dfda_log_whole.copy()
                    
                    # After the index table is built and ready, pass it to the Backend Agent,
                    # initializing an instance to implement the data analysis pipeline for each device log
                    data_analyser = DataAnalyserBackendAgent(dfda_log)

                    status_text.text("索引表构建完成！正在调用内置程序处理日志数据...")
                    for i, xlsx_file in enumerate(xlsx_files):

                        # Second half of progress: Data analysis
                        progress_bar.progress(0.5 + (i + 1) / (len(xlsx_files) * 2)) 

                        with zip_ref.open(xlsx_file) as uploaded_file:

                            df_log = pd.read_excel(uploaded_file)
                            device_name = None
                            imei = None
                                
                            if 'device_name' in df_log.columns:
                                device_name = df_log['device_name'].dropna().iloc[0]
                            elif '设备ID' in dfda_log.columns:
                                device_name = df_log['设备ID'].dropna().iloc[0]

                            if 'imei' in dfda_log.columns:
                                imei = df_log['imei'].dropna().iloc[0]
                            elif 'IMEI' in dfda_log.columns:
                                imei = df_log['IMEI'].dropna().iloc[0]

                            # （接下来的）这一步，和之前第一阶段的实习成果最大的区别在于，之前是:
                            # 根据索引表的 “标识列”（imei, device name）去匹配（上传的压缩包中的以 “标识列” 命名的）日志文件
                            # 但是，由于后来考虑到，命名问题常常不可控，这里反过来修改为了根据日志文件的 “标识列” 去匹配索引表

                            # 这也导致了这部分的代码存在形同虚设的部分,
                            # 因为索引表和日志文件都已在缓存内并已排好序，只需在遍历时同时扫描彼此即可，本质上不存在匹配问题

                            # Latest update: 2025-07-17
                            # 如果未来采用数据库直连的方式，索引表和日志文件的匹配问题将不复存在；
                            # 因为 “查找日志文件” 的逻辑将由数据库的 select 语句实现

                            data_analyser.identify_id_info(
                                df_device_log=df_log, 
                                use_index=False, 
                                index=None,
                                device_name=device_name, 
                                imei=imei
                            )

                            PagesDataAnalysis._conduct_the_pipeline(data_analyser)

                    # Complete the progress bar
                    progress_bar.progress(1.0)
                    status_text.text("处理完成！即将向您展示统计分析与可视化结果...")
                    
                    # Clear the progress indicators after a short delay
                    time.sleep(1.75)
                    progress_info.empty()
                    progress_bar.empty()
                    status_text.empty()

                    # Translate and mildly modify the processed statistical analysis table for subsequent visualization
                    dfda_log_updated = data_analyser._df_data_analysis
                    dfda_log_translated = DataAnalyserBackendAgent.translate_and_mildly_modify_your_df(dfda_log_updated)

                    # Store the processed data in session state for visualization
                    st.session_state.dfda_log_translated = dfda_log_translated
                    st.session_state.all_devices = dfda_log_translated
                    st.session_state.device_indices = [f'No.{i}' for i in range(len(dfda_log_translated))]
                    
                    # Mark data as processed
                    st.session_state.data_processed = True
                    st.session_state.current_pattern = pattern_choice
                    st.session_state.cache_file = st.session_state.current_file

                # Reminder: Remember to move visualization logic outside the pattern_choice conditional block,
                # because it costed me a considerable amount of time to debug the code !!!

                # Lesson: Streamlit always reruns the entire code block when a button is clicked

                # Check if we have processed data available
                if st.session_state.dfda_log_translated is not None: 
                    
                    # Check if user has not yet uploaded a new file
                    if st.session_state.cache_file == st.session_state.current_file:

                        st.markdown("---")
                        st.markdown("### 基于日志的参数统计表")

                        # st.dataframe(st.session_state.dfda_log_translated, use_container_width=True)

                        st.data_editor(
                            st.session_state.dfda_log_translated,
                            use_container_width=True,
                            column_config={
                                "device_name": st.column_config.Column(width=150),
                            }
                        )

                        st.markdown("### 基于日志的可视化与分析")

                        st.markdown("#### A. 生命周期与使用时长")
                                                    
                        PagesDataAnalysis._visualize_usage_lifecycle(
                            dfda_log_translated=st.session_state.dfda_log_translated
                        )
                        
                        st.markdown("#### B. 操作类型与信号强度")

                        visualization_type = st.selectbox(

                            '请选择对控制器的重要特征（操作类型，信号强度）的可视化方式',
                            ('按设备台数显示', '按设备序号显示'),
                            key='visualization_type'

                        )

                        if visualization_type == '按设备序号显示':
                            
                            PagesDataAnalysis._visualize_operation_freq_by_device_id(
                                dfda_log_translated=st.session_state.dfda_log_translated
                            )

                            PagesDataAnalysis._visualize_signal_freq_by_device_id(
                                dfda_log_translated=st.session_state.dfda_log_translated
                            )

                        if visualization_type == '按设备台数显示':

                            PagesDataAnalysis._visualize_operation_freq_by_device_amount(
                                dfda_log_translated=st.session_state.dfda_log_translated
                            )

                            PagesDataAnalysis._visualize_signal_freq_by_device_amount(
                                dfda_log_translated=st.session_state.dfda_log_translated
                            )

            else:
                st.warning("压缩包中没有找到以 '.xlsx' 结尾的日志文件；请检查压缩包的内容并重新上传。")