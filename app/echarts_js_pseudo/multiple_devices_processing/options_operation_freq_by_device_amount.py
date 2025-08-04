def get_options_operation_freq_by_device_amount(
        operation_categories: list,
        range_labels: list,
        operation_freq_data: list
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “多设备处理” 页面中，“操作类型分布（按设备台数）” 的可视化与分析。

    Args:
        operation_categories (list): 操作类型种类的名称列表，例如 ['待机次数', '开闭灌溉次数', '上下线次数']
        range_labels (list): 操作类型频次范围的标签列表（可以不均匀），即通过动态切割生成，例如 ['0-10', '10-100', '100-1000']
        operation_freq_data (list[dict]): 操作类型频次数据列表，每个元素是一个字典，包含构成 “群组柱状图 (Grouped Bar)” 的键值对参数
    """

    options_operation_freq_by_device_amount = {
        "title": {
            "text": "多设备操作类型频次分布", 
            "left": "center"
        },
        "tooltip": {
            "trigger": "axis", 
            "axisPointer": {"type": "shadow"}
        },
        "legend": {
            "data": operation_categories, 
            "top": "7.25%",
            "right": "3.5%",
            "orient": "vertical"
        },
        "grid": {
            "left": "3%", 
            "right": "4%",  
            "bottom": "15%", 
            "top": "17.5%", 
            "containLabel": True
        },
        "xAxis": {
            "type": "value",
            "name": "横轴：设备台数",
            'nameLocation': 'center',
            'nameGap': 50,
            'nameTextStyle': {
                'align': 'center'
            },
            'axisLabel': {
                'margin': 20,
                'showMinLabel': True,
                'showMaxLabel': True,
                'interval': 'auto'
            },
            "splitLine": {
                "show": True, 
                "lineStyle": {"type": "dashed"}
            }
        },
        "yAxis": {
            "type": "category",
            "name": "纵轴：操作类型频次（范围）",
            'nameLocation': 'end',
            'nameGap': 30,
            'nameTextStyle': {
                'align': 'left'
            },
            "data": range_labels,
            "axisLabel": {
                'margin': 20
            }
        },
        "series": operation_freq_data
    }

    return options_operation_freq_by_device_amount