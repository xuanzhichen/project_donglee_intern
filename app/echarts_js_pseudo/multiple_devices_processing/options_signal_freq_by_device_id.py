def get_options_signal_freq_by_device_id(
        signal_cols: list,
        device_indices: list,
        signal_series: list
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “多设备处理” 页面中，“信号强度分布（按设备编号）” 的可视化与分析。

    Args:
        signal_cols (list): 信号强度种类的名称列表，例如 ['强信号次数', '中等强度次数', '弱/无强度次数']
        device_indices (list): 设备序号列表（即日志参数统计表的 “行”，但从 1 开始编号），例如 [1, 2, 3, ..., 10]
        signal_series (list[dict]): 信号强度序列列表，每个元素是一个字典，包含构成 “堆叠柱状图 (Stacked Bar)” 的键值对参数
    """

    signal_options_signal_freq_by_device_id = {
        "title": {
            "text": "多设备信号强度分布", 
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis", 
            "axisPointer": {"type": "shadow"}
        },
        "legend": {
            "data": signal_cols, 
            "top": "7.25%"
        },
        "grid": {
            "left": "3%", 
            "right": "4%",  
            "bottom": "15%", 
            "top": "17.5%", 
            "containLabel": True
        },
        "dataZoom": [
            {
                "type": "slider", 
                "show": True, 
                "xAxisIndex": [0], 
                "start": 0, 
                "end": 100, 
                "height": 20
            },
            {
                "type": "inside", 
                "xAxisIndex": [0], 
                "start": 0, 
                "end": 100
            }
        ],
        "xAxis": {
            "type": "category",
            "name": "设备序号(No.)",
            'nameLocation': 'center',
            'nameGap': 60,
            'nameTextStyle': {
                'align': 'center'
            },
            "data": device_indices,
            "axisLabel": {
                "rotate": 45, 
                'margin': 20,
                'showMinLabel': True,
                'showMaxLabel': True,
                'interval': 'auto'
            },
        },
        "yAxis": {
            "type": "value",
            "name": "信号强度频次",
            'nameLocation': 'end',
            'nameGap': 30,
            'nameTextStyle': {
                'align': 'left'
            },
            'axisLabel': {
                'margin': 20
            },
            "splitLine": {
                "show": True, 
                "lineStyle": {"type": "dashed"}
            }
        },
        "series": signal_series
    }

    return signal_options_signal_freq_by_device_id