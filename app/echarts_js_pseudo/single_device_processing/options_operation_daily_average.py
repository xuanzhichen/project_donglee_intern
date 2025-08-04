def get_options_operation_daily_average(
    uploaded_file,
    daily_status_dates: list,
    daily_status_mode_idx: list,
    status_categories: list
):
    """
    返回一个 ECharts 的 (JavaScript) 配置项，用于绘制 “单设备处理” 页面中，“操作类型（日均）” 的可视化与分析。

    Args:
        uploaded_file (st.uploaded_file): 上传的日志文件对象，此处用于获取文件名，以展示图表的标题
        daily_status_dates (list): 将实时日志按日聚合（降频）后的列表，格式已简化，例如 ['25-01-01', '25-01-02', ..., '25-12-31']
        daily_status_mode_idx (list): 映射日志的每个日期 (daily_status_dates) 所对应的操作类型（编码），准确来说，是该日期下，操作类型出现次数最多的操作类型（编码）
        status_categories (list): 对不同操作类型的编码，例如 [0, 1, 2, 3]
    """
    options_operation_daily_average = {
        'title': {
            'text': f'"{uploaded_file.name.rsplit(".", 1)[0]}" 操作类型的趋势变化（日均）',
            'left': 'center',
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
                'fillerColor': 'rgba(84, 112, 198, 0.2)',
                'handleStyle': {
                    'color': '#5470C6',
                    'borderColor': '#5470C6'
                },
                'selectedDataBackground': {
                    'lineStyle': {
                        'color': '#5470C6'
                    },
                    'areaStyle': {
                        'color': '#5470C6'
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
        'xAxis': {
            'type': 'category',
            'data': daily_status_dates,
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
            'name': '操作类型说明 (3：设备状态；2：开启/关闭灌溉；1：设备上线/下线；0：无日志记录)',
            'nameLocation': 'end',
            'nameGap': 30,
            'nameTextStyle': {
                'align': 'left'
            },
            'min': 0,
            'max': 3,
            'interval': 1,
            'data': status_categories,
            'splitLine': {
                'show': True,
                'lineStyle': {
                    'type': 'dashed'
                }
            },
            'axisLabel': {
                'formatter': '{value}'
            }
        },
        'series': [{
            'name': '日均操作类型',
            'type': 'line',
            'step': 'start',
            'data': daily_status_mode_idx,
            'itemStyle': {
                'color': '#5470C6'
            }
        }]
    }

    return options_operation_daily_average