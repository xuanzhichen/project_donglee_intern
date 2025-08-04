def get_options_signal_daily_average(
    uploaded_file,
    daily_signal_dates,
    daily_signal_values
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “单设备处理” 页面中，“信号强度（日均）” 的可视化与分析。

    Args:
        uploaded_file (st.uploaded_file): 上传的日志文件对象，此处用于获取文件名，以展示图表的标题
        daily_signal_dates (list): 将实时日志按日聚合（降频）后的列表，格式已简化，例如 ['25-01-01', '25-01-02', ..., '25-12-31']
        daily_signal_values (list): 映射日志的每个日期 (daily_signal_dates) 所对应的信号（日平均）强度值；注意：如果该日期下没有信号强度值，则该值为 0
    """

    options_signal_daily_average = {
        'title': {
            'text': f'"{uploaded_file.name.rsplit(".", 1)[0]}" 信号强度的趋势变化（日均）',
            'left': 'center'
        },
        'tooltip': {
            'trigger': 'axis',
            'formatter': '{b}: {a} = {c}'
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '15%',
            'top': '17.5%',
            'containLabel': True
        },
        'dataZoom': [
            {
                'type': 'slider',
                'show': True,
                'xAxisIndex': [0],
                'start': 0,
                'end': 100,
                'height': 20,
                'borderColor': 'transparent',
                'backgroundColor': '#e2e2e2',
                'fillerColor': 'rgba(255, 165, 0, 0.2)',
                'handleStyle': {
                    'color': '#ffa500',
                    'borderColor': '#ffa500'
                },
                'selectedDataBackground': {
                    'lineStyle': {
                        'color': '#ffa500'
                    },
                    'areaStyle': {
                        'color': '#ffa500'
                    }
                }
            },
            {
                'type': 'inside',
                'xAxisIndex': [0],
                'start': 0,
                'end': 100
            }
        ],
        'visualMap': {
            'show': False,
            'type': 'continuous',
            'min': 0,
            'max': 31.0,
            'inRange': {
                'color': ['#808080', '#ffd700', '#ffa500', '#ff4500']
            },
            'calculable': True
        },
        'xAxis': {
            'type': 'category',
            'data': daily_signal_dates,
            'axisLabel': {
                'rotate': 45,
                'margin': 20,
                'showMinLabel': True,
                'showMaxLabel': True,
                'interval': 'auto'
            }
        },
        'yAxis': {
            'type': 'value',
            'name': '信号强度说明 (31-21.5：强信号；21.5-11.5：中信号；11.5-1.5：弱信号；1.5-0：无信号)',
            'nameLocation': 'end',
            'nameGap': 30,
            'nameTextStyle': {
                'align': 'left'
            },
            'min': 0,
            'max': 31.0,
            'axisLabel': {
                'margin': 20
            },
            'splitLine': {
                'show': True,
                'lineStyle': {
                    'type': 'dashed'
                }
            }
        },
        'series': [
            {
                'name': '日均信号强度',
                'type': 'line',
                'data': daily_signal_values,
                'connectNulls': True,
                'itemStyle': {
                    'color': '#ffa500'
                },
                'markLine': {
                    'silent': True,
                    'symbol': 'none',
                    'lineStyle': {
                        'color': '#666',
                        'type': 'dashed'
                    },
                    'data': [
                        {'yAxis': 21.5, 'name': '强信号阈值'},
                        {'yAxis': 11.5, 'name': '中信号阈值'},
                        {'yAxis': 1.5, 'name': '弱信号阈值'}
                    ]
                }
            }
        ]
    }

    return options_signal_daily_average