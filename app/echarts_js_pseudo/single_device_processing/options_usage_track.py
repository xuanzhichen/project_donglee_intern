def get_options_usage_track(
    x_axis_dates: list,
    status_data: list
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “单设备处理” 页面中，“生命周期与使用时长” 的可视化与分析。

    Args:
        x_axis_dates (list): 根据日志起始范围内连续的日期列表，格式已简化，例如 ['25-01', '25-02', ..., '25-12']
        status_data (list): 设备上下线状态的数据列表，1 表示设备在线（即日志连续），0 表示设备离线（即日志中断）
    """
    
    options_usage_track = {
        # "title": {
        #     "text": f'智云设备 "{uploaded_file.name.rsplit(".", 1)[0]}" 在线状态时间线',
        #     "left": "center",
        #     # "textStyle": {
        #     #     "fontSize": 16,
        #     #     "fontWeight": "bold"
        #     # }
        # },
        "tooltip": {
            "trigger": "axis",
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
                "height": 20,
                "borderColor": "transparent",
                "backgroundColor": "#e2e2e2",
                "fillerColor": "rgba(34, 197, 94, 0.2)",
                "handleStyle": {
                    "color": "#22C55E",
                    "borderColor": "#22C55E"
                },
                "selectedDataBackground": {
                    "lineStyle": {
                        "color": "#22C55E"
                    },
                    "areaStyle": {
                        "color": "#22C55E"
                    }
                }
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
            # "name": "日期",
            "nameLocation": "center",
            "nameGap": 40,
            "nameTextStyle": {
                "align": "center",
                # "fontSize": 12
            },
            "data": x_axis_dates,
            "axisLabel": {
                "rotate": 45,
                "margin": 20,
                "showMinLabel": True,
                "showMaxLabel": True,
                "interval": "auto",
                # "fontSize": 11
            }
        },
        "yAxis": {
            "type": "value",
            "name": "控制器状态说明 (1：日志连续；0：日志中断)",
            "nameLocation": "end",
            "nameGap": 30,
            "nameTextStyle": {
                "align": "left",
                # "fontSize": 12
            },
            "min": 0,
            "max": 1,
            "interval": 1,
            "axisLabel": {
                "margin": 20,
                "fontSize": 11,
            },
            "splitLine": {
                "show": True,
                "lineStyle": {
                    "type": "dashed",
                    # "opacity": 0.3
                }
            }
        },
        "series": [{
            "name": "设备状态",
            "type": "line",
            "step": "start",
            "data": status_data,
            "itemStyle": {
                "color": "#22C55E"
            },
            "lineStyle": {
                "width": 3
            },
            "symbol": "circle",
            "symbolSize": 6,
            "emphasis": {
                "itemStyle": {
                    "color": "#16A34A",
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0,0,0,0.3)"
                }
            }
        }]
    }

    return options_usage_track