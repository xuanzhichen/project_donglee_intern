# 项目简介

该 `README.md` 文档正在建设中...

在该项目的实习期结束后，余下的内容预计在今年秋季利用我的个人时间抽空完善。

# 关于开发

该平台基于 Python-Streamlit 框架开发，后期方向是考虑与智云公司的 IoT 平台进行衔接。
            
该目标被划分为三个处理阶段：（代码的）接口与封装，实时数据分析，以及平台部署。因此，此部分内容主要是面向智云产品部内部开发者的工作交接说明。[源码](https://github.com/xuanzhichen/project_donglee_intern/tree/main/app)位于项目根目录的 `app/` 路径下。

## 接口与封装说明

在后端数据处理方面，以 “单设备处理” 模块为例，路径 `app/demo_data_analysis/` 下的脚本 `demo_data_analysis.py` 展示了简化接口，通过读取智能控制器日志文件，以一行代码演示：

```Python
# 运行demo: 一行代码执行智能控制器日志数据分析
run_demo(df_log=pd.read_excel('智能控制器样例日志（简化测试版）.xlsx')) 
```

具体的数据处理逻辑如下（仍以 “单设备处理” 为例）：

```Python
# 数据分析程序的运行逻辑
def run_demo(df_log):

    # 1. 初始化 “基于日志的参数统计表”（也作为索引bia）
    dfda_log = index_a_dfda_log(df_log)
    dfda_log = define_uptime_and_downtime(dfda_log, df_log)

    # 2. 初始化数据分析对象
    data_analyser = DataAnalyser(dfda_log)

    # 3. 遍历索引表，执行数据分析管道 (pipeline)
    for index, row in dfda_log.iterrows():
        data_analyser.identify_id_info(df_log, index) # 识别设备ID信息
        data_analyser.get_usage_period() # 统计使用时长相关参数
        data_analyser.get_sub_log_based_on_usage_period() # 提取子日志（即连续时长）
        data_analyser.get_operation_status() # 统计操作类型相关参数
        data_analyser.get_signal_strength_frequency() # 统计信号强度相关参数
        data_analyser.get_signal_switch_frequency() # 统计信号切换相关参数

    # 4. 更新 “基于日志的参数统计表”
    dfda_log_updated = data_analyser._df_data_analysis

    # 5. 翻译 “基于日志的参数统计表”
    dfda_log_translated = translate_and_mildly_modify_your_df(dfda_log_updated)

    # 6. 打印 “基于日志的参数统计表”
    print(dfda_log_translated)
```

在前端数据可视化方面，以 “多设备处理” 模块为例，下述路径结构树进一步展示了该项目中源码的封装形式。
其借助了 Streamlit 平台的第三方容器，采用了开源可视化图表库 —— [ECharts](https://echarts.apache.org/zh/index.html) —— 基于 JavaScript 风格的配置项 (Options)，从而尽可能与智云公司 IOT 平台现有的前端开发框架保持一致。

```shell
app/  # 智能控制器-日志数据分析平台根目录
└── echarts_js_pseudo/  # 前端数据可视化伪代码 (Echarts-JavaScript)
    ├── __init__.py
    ├── single_device_processing/  # 单设备处理
    │   ├── ...
    └── multiple_devices_processing/  # 多设备处理
        ├── options_usage_lifecycle.py  # 生命周期与使用时长-可视化
        ├── options_operation_freq_by_device_amount.py  # 操作类型（按设备台数）-可视化
        ├── options_operation_freq_by_device_id.py  # 操作类型（按设备编号）-可视化
        ├── options_signal_freq_by_device_amount.py  # 信号强度（按设备台数）-可视化
        └── options_signal_freq_by_device_id.py  # 信号强度（按设备编号）-可视化
```

## 实时数据分析（后期方向）

该平台目前仅支持离线数据分析（即通过用户手动上传日志文件）；后期考虑对接智云公司的 IoT 平台数据库，直接进行日志调取，以实现实时数据分析。

## 平台部署（后期方向）

该平台目前部署在社区版的免费公有云上，鉴于数据私有性和系统稳定性等问题，后期考虑将其部署在智云公司的阿里云服务器之上。

