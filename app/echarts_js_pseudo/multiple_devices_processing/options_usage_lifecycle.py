import pandas as pd


def get_options_usage_lifecycle(
        usage_months: pd.Series,
        month_labels: list,
        month_counts: list
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “多设备处理” 页面中，“生命周期与使用时长” 的可视化与分析。

    Args:
        usage_months (pd.Series): 从处理后的日志分析统计表 (DataFrame) 中提取的 “使用月数” 列
        month_labels (list): 根据 usage_months 中的极值月数，生成对应的标签列表，例如 [0个月, 1个月, 2个月, ..., 12个月]
        month_counts (list): 根据 usage_months 中的 “使用月数”，生成 month_labels 中对应标签下的计数列表
    """

    # Create the bar chart options
    options_usage_lifecycle = {
        # "title": {
        #     "text": "设备使用生命周期分布", 
        #     "left": "center",
        #     "textStyle": {
        #         "fontSize": 16,
        #         "fontWeight": "bold"
        #     }
        # },
        "tooltip": {
            "trigger": "axis", 
            "axisPointer": {"type": "shadow"},
            "formatter": "{b}: {c}台设备"
        },
        "grid": {
            "left": "3%", 
            "right": "4%",  
            "bottom": "15%", 
            "top": "17.5%", 
            "containLabel": True
        },
        "xAxis": {
            "type": "category",
            "name": f"横轴：使用月数分布（平均使用月数为：{usage_months.mean():.1f}个月）",
            'nameLocation': 'center',
            'nameGap': 40,
            'nameTextStyle': {
                'align': 'center',
                'fontSize': 12
            },
            "data": month_labels,
            "axisLabel": {
                "rotate": 0, 
                'margin': 15,
                'showMinLabel': True,
                'showMaxLabel': True,
                'interval': 0,
                'fontSize': 11
            },
        },
        "yAxis": {
            "type": "value",
            "name": "设备台数",
            'nameLocation': 'end',
            'nameGap': 30,
            'nameTextStyle': {
                'align': 'left',
                # 'fontSize': 12
            },
            'axisLabel': {
                'margin': 20,
                # 'fontSize': 11
            },
            "splitLine": {
                "show": True, 
                "lineStyle": {"type": "dashed"}
            }
        },
        "series": [{
            "name": "设备数量",
            "type": "bar",
            "data": month_counts,
            "itemStyle": {
                "color": "#22C55E",
                "borderRadius": [3, 3, 0, 0],
                "borderWidth": 0
            },
            "emphasis": {
                "itemStyle": {
                    "color": "#16A34A",
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0,0,0,0.3)"
                }
            },
            "markLine": {
                # "silent": True,
                "symbol": "none",
                "lineStyle": {
                    "color": "#EF4444",
                    "type": "solid",
                    "width": 2
                },
                # "label": {
                #     "show": True,
                #     "position": "top",
                #     "formatter": f"平均: {usage_months.mean():.1f}个月",
                #     "fontSize": 11,
                #     "color": "#EF4444",
                #     "fontWeight": "bold"
                # },
                "data": [
                    {
                        "xAxis": usage_months.mean(),
                        "name": "平均使用月数"
                    }
                ]
            }
        }]
    }

    return options_usage_lifecycle