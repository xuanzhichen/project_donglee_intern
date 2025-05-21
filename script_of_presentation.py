import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Set up the project root path and superior input path
# project_root_path = 'D:\project_code\project_donglee_intern'
project_root_path = 'project_code\project_donglee_intern'
input_superior_path = 'output'

def get_your_df(input_superior_path, file_name):
    file_path = os.path.join(project_root_path, input_superior_path, (str(file_name) + '.xlsx'))
    df_data_analysis = pd.read_excel(file_path)
    return df_data_analysis

def generate_statistical_summary(df):
    # Numeric columns summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_summary = df[numeric_cols].describe()
    
    # Date columns summary
    date_cols = ['下线日期 (或当前日志时间)', '上线日期']
    date_summary = {}
    for col in date_cols:
        if col in df.columns:
            date_summary[col] = {
                'Min': df[col].min(),
                'Max': df[col].max()
            }
    
    return numeric_summary, date_summary

def analyze_distributions(df, title):
    st.subheader(f"{title} - 分布分析")

    # Set font to support Chinese characters
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font for Chinese
    plt.rcParams['axes.unicode_minus'] = False    # Fix minus sign display
    
    # Add column selector for detailed analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    selected_col = st.selectbox("选择要详细分析的列", numeric_cols, key=f"detail_select_{title}")
    
    # Create detailed distribution plot for selected column
    st.subheader(f"{selected_col} 的详细分布分析")
    
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram with KDE
    sns.histplot(data=df, x=selected_col, kde=True, ax=ax1)
    ax1.set_title(f'{selected_col} 的分布直方图')
    
    # Box plot
    sns.boxplot(data=df, y=selected_col, ax=ax2)
    ax2.set_title(f'{selected_col} 的箱线图')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
    
    # Display summary statistics for the selected column
    st.subheader(f"{selected_col} 的统计摘要")
    col_stats = df[selected_col].describe()
    st.dataframe(col_stats)
    
    # Add distribution overview section
    st.subheader("所有数值型变量的分布概览")
    
    # Select numeric columns for distribution analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    # Create distribution plots
    n_cols = 3
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        sns.histplot(data=df, x=col, ax=axes[idx], kde=True)
        axes[idx].set_title(f'{col}的分布')
    
    # Remove empty subplots
    for idx in range(len(numeric_cols), len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def create_visualizations(df, title):
    # Create a container for the visualizations
    with st.container():
        st.subheader(f"{title} - 数据可视化")
        
        # Select numeric columns for visualization
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # Create a dropdown for column selection
        selected_col = st.selectbox("选择要可视化的特征(列)", numeric_cols, key=f"select_{title}")
        
        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)
        
        # Create and display histogram in first column
        with col1:
            fig_hist = px.histogram(
                df, 
                x=selected_col,
                title=f"{selected_col} 分布直方图",
                nbins=30,
                color_discrete_sequence=['#2E86C1'],
                opacity=0.8,
                marginal='box',
                template='plotly_white'
            )
            fig_hist.update_layout(
                title_font_size=20,
                title_font_color='#2C3E50',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                showlegend=False,
                plot_bgcolor='white',
                height=500
            )
            st.plotly_chart(fig_hist, use_container_width=True, key=f"hist_{title}_{selected_col}")
        
        # Create and display box plot in second column
        with col2:
            fig_box = px.box(
                df, 
                y=selected_col,
                title=f"{selected_col} 箱线图",
                color_discrete_sequence=['#2E86C1'],
                template='plotly_white',
                points='all'
            )
            fig_box.update_layout(
                title_font_size=20,
                title_font_color='#2C3E50',
                xaxis_title_font_size=14,
                yaxis_title_font_size=14,
                showlegend=False,
                plot_bgcolor='white',
                height=500
            )
            st.plotly_chart(fig_box, use_container_width=True, key=f"box_{title}_{selected_col}")

# Set up the page
st.set_page_config(page_title="智云灌溉设备-日志数据分析平台", layout="wide")
st.title("智云灌溉设备-日志数据分析平台")
st.markdown(":red[**所有分析结果基于当前输入日志的[截止记录日期]: 05/07/2025**]")

# Create sidebar navigation
st.sidebar.title("导航")
page = st.sidebar.radio("我的数据分析项目", ["统计表概览", "异常值检测", "相关性分析", "聚类分析"])

# Load the dataframes
df_general_log_stat_haida = get_your_df(
    input_superior_path=input_superior_path, 
    file_name='基于日记250507-海大设备数据分析-250515'
)

df_general_log_stat_scaled_month_haida = get_your_df(
    input_superior_path=input_superior_path, 
    file_name='基于日记250507-海大设备数据分析-月均化缩放-250519'
)

df_general_log_stat_scaled_prob_haida = get_your_df(
    input_superior_path=input_superior_path, 
    file_name='基于日记250507-海大设备数据分析-概率化缩放-250519'
)

if page == "统计表概览":
    # Create tabs for different dataframes
    # tab1, tab2, tab3 = st.tabs(["原始数据", "月均化缩放数据", "概率化缩放数据"])

    # Common content for all tabs
    st.markdown("---")
    st.header("统计表概览")
    
    # Initialize session state if not exists
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "原始统计表 (频次累记)"
    
    # Create a selectbox to control which dataframe is shown
    selected_tab = st.selectbox(
        "选择数据视图",
        ["原始统计表 (频次累记)", "月均化缩放统计表", "概率化缩放统计表"],
        key="tab_selector"
    )
    
    # Set the current dataframe based on selection
    if selected_tab == "原始统计表 (频次累记)":
        current_df = df_general_log_stat_haida
    elif selected_tab == "月均化缩放统计表":
        current_df = df_general_log_stat_scaled_month_haida
    else:  # 概率化缩放统计表
        current_df = df_general_log_stat_scaled_prob_haida
    
    # Display the dataframe
    st.subheader("(暂时仅限海大项目)")
    st.dataframe(current_df)
    
    st.markdown(":orange-badge[⚠️ **观察记录 \& 要点汇报:**]")
    st.markdown("- [右上角]下载数据表，更改后缀名为 xlsx 即可在 Excel 中打开")
    st.markdown("""
    - 主要特征介绍 :violet[@excalidraw.com]
        1. 直接影响到使用时长的计算结果：`使用月数`, `离线次数`, `离线天数`, 以及`实际使用月数`
        2. 一个设备的日志记录是否算具有 `连续性`？
        3. 增添的感兴趣指标：`信号强度切换次数`
    """)
    st.markdown("""
    - 固定与排序日志长度/使用月数、对频次的样本空间的影响？
        1. 原始统计表：频次累记
        2. 月均化缩放
        3. 概率化缩放
    """)
    st.markdown("- 程序参数会可能会影响统计表的计算结果：")
    code = '''# The core code snippet for data processing
# 数据处理的核心代码片段
for index, row in df_data_analysis.iterrows():
    try:
        device_name = row['device_name']
        df_device_log, file_path = get_df_device_log(device_name, input_superior_path)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")

    ### Implement data processing logic for each device log
    ### 施行对于每个灌溉设备日志数据的处理逻辑
    data_analyser.identify_id_info(device_name=device_name, df_device_log=df_device_log)

    # Update log length
    # 记录日志的长度 (便于对频次型指标进行划归)
    data_analyser.get_log_len()

    # Update downtime and uptime
    # 更新下线时间与上线时间
    data_analyser.get_downtime_uptime()

    # Simply calculate the life-cycle in months
    # 简单地计算设备的使用生命周期 (下线时间与上线时间之差)
    data_analyser.get_month_len_include_break()

    # Calculate the life-cycle with consideration of day-break events
    # 考虑在设备的整个生命周期内，是否出现显著的日志间断现象，以计算实际的使用生命周期
    data_analyser.get_month_len_exclude_break(
        days_break_threshold=2, 
        threshold_days_for_excluding=30
    )

    # Mark the log characteristic as 'Not continued' if maximal broken days over the threshold
    # 如果最大间隔天数超过设定阈值，标记该设备的日志属性为 "不连续"
    data_analyser.get_continued_status(broken_down_threshold=15)

    # Count the frequency of the five operation status recorded in the log over the life-cycle 
    # 统计日志记录中五种操作状态 (灌溉开启/灌溉关闭/上线/离线/待机) 在设备生命周期内出现的频次
    data_analyser.get_operation_status()

    # Count the frequency of the four categorizes of signal strength (strong/mid/weak/null)
    # recorded in the log over the life-cycle
    # 统计日志记录中四种信号强度 (强信号/中信号/弱信号/无信号) 在设备生命周期内出现的频次 
    data_analyser.get_signal_strength_frequency()

    # Count the frequency of the cases in which a device went through significant signal switches
    # 统计日志记录中 (相邻的两个时间戳下) 设备显著切换信号强度的频次
    data_analyser.get_signal_switch_frequency(window_len=2) '''
    st.code(code, language="python", line_numbers=True, height=500)
    
    # Display summary statistics
    st.subheader("统计摘要")
    numeric_summary, date_summary = generate_statistical_summary(current_df)
    
    # Display date summary in a dataframe format
    st.write("日期范围统计摘要：")
    date_summary_df = pd.DataFrame({
        '日期字段': date_summary.keys(),
        '最小值': [summary['Min'] for summary in date_summary.values()],
        '最大值': [summary['Max'] for summary in date_summary.values()]
    })
    
    st.dataframe(date_summary_df)
        
    # Display numeric summary
    st.write("数值型数据统计摘要：")
    st.dataframe(numeric_summary)
    st.markdown(":orange-badge[⚠️ **观察记录 \& 要点汇报:**]")
    st.markdown("1. 在新版的日志数据下，设备的平均使用时长依旧不长，约为 3.3 个月")
    st.markdown("2. 设备的平均离线时间为 1 个月；结论 1 在结论 2 的基础上推断出")
    st.markdown("3. 对于数值大小的感受可能仍需要定量分析")
    
    # Create visualizations
    create_visualizations(current_df, "选择面板")
    create_visualizations(current_df, "比对面板 (如果适用)")
    st.markdown(":orange-badge[⚠️ **观察记录 \& 要点汇报:**]")
    st.markdown("注意缩放对设备状态次数 (开启/关闭灌溉)、信号强度次数、信号强度切换次数等 `频次型` 特征的影响")

elif page == "异常值检测":
    st.markdown("---")
    st.header("异常值检测")
    
    # Add dataframe selection
    st.subheader("选择数据视图")
    selected_tab = st.selectbox(
        "选择要分析的数据表",
        ["原始统计表 (频次累记)", "月均化缩放统计表", "概率化缩放统计表"],
        key="outlier_tab_selector"
    )
    
    # Set the current dataframe based on selection
    if selected_tab == "原始统计表 (频次累记)":
        current_df = df_general_log_stat_haida
    elif selected_tab == "月均化缩放统计表":
        current_df = df_general_log_stat_scaled_month_haida
    else:  # 概率化缩放统计表
        current_df = df_general_log_stat_scaled_prob_haida
    
    # Get key variables for analysis (excluding first 6 columns and '连续性')
    key_vars = current_df.columns.tolist()
    key_vars = key_vars[6:]
    if '连续性' in key_vars:
        key_vars.remove('连续性')
    
    # Function to detect outliers using IQR method with non-negative lower bound
    def detect_outliers(df, columns):
        outlier_indices = {}
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = max(0, Q1 - 1.5 * IQR)  # Ensure lower bound is not negative
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_indices[col] = outliers.index.tolist()
        return outlier_indices
    
    # Detect outliers
    outlier_indices = detect_outliers(current_df, key_vars)
    
    # Create overview of columns with outliers
    st.subheader("异常值检测概览")
    
    # Create a summary dataframe
    overview_data = []
    for col in key_vars:
        if col in outlier_indices and len(outlier_indices[col]) > 0:
            overview_data.append({
                '特征': col,
                '异常值数量': len(outlier_indices[col]),
                '异常值比例': f"{(len(outlier_indices[col]) / len(current_df) * 100):.1f}%"
            })
    
    if overview_data:
        overview_df = pd.DataFrame(overview_data)
        overview_df = overview_df.sort_values('异常值数量', ascending=False)
        st.dataframe(overview_df, use_container_width=True)
        st.markdown("---")
    else:
        st.info("当前数据集中未检测到异常值")
        st.markdown("---")
    
    # Create two columns for side-by-side display
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Add outlier detection section
        st.subheader("异常值检测细节")
        
        # Create a selectbox for users to choose which variable to analyze
        selected_var = st.selectbox("选择要分析的特征", key_vars)
        
        # Display outlier information for selected variable
        if selected_var in outlier_indices:
            # Get only the relevant columns for display (设备名称 and selected variable)
            display_cols = ['设备名称', selected_var]
            outliers = current_df.iloc[outlier_indices[selected_var]][display_cols]
            
            # Calculate IQR statistics
            Q1 = current_df[selected_var].quantile(0.25)
            Q3 = current_df[selected_var].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = max(0, Q1 - 1.5 * IQR)  # Ensure lower bound is not negative
            upper_bound = Q3 + 1.5 * IQR
            
            # Display statistics
            st.write(f"**{selected_var} 的异常值统计:**")
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("异常值数量", len(outlier_indices[selected_var]))
            with stat_col2:
                st.metric("下界", f"{lower_bound:.2f}")
            with stat_col3:
                st.metric("上界", f"{upper_bound:.2f}")
            
            # Display outlier data with fixed height
            st.write("**异常值数据:**")
            st.dataframe(outliers, height=210)
    
    with col_right:
        if selected_var in outlier_indices:
            # Create visualization for the selected variable
            fig = go.Figure()
            
            # Add box plot
            fig.add_trace(go.Box(
                y=current_df[selected_var],
                name=selected_var,
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            ))
            
            # Add horizontal lines for bounds
            fig.add_hline(y=lower_bound, line_dash="dash", line_color="red", annotation_text="下界")
            fig.add_hline(y=upper_bound, line_dash="dash", line_color="red", annotation_text="上界")
            
            # Update layout
            fig.update_layout(
                title=f"{selected_var} 的箱线图与异常值",
                yaxis_title=selected_var,
                showlegend=False,
                height=600  # Increased height for better visibility
            )
            
            st.plotly_chart(fig, use_container_width=True)

    st.markdown(":orange-badge[⚠️ **观察记录 \& 要点汇报:**]")
    st.markdown("理论上讲，异常值的丰富程度能够给相关性分析提供线索；例如，我们可能期望异常值丰富的特征 (例如最小信号强度、 中/弱信号切换次数等) 与设备的使用时长存在潜在的相关性")

elif page == "相关性分析":
    st.markdown("---")
    st.header("相关性分析")
    
    # Add dataframe selection
    st.subheader("选择数据视图")
    selected_tab = st.selectbox(
        "选择要分析的数据表",
        ["原始统计表 (频次累记)", "月均化缩放统计表", "概率化缩放统计表"],
        key="corr_tab_selector"
    )
    
    # Set the current dataframe based on selection
    if selected_tab == "原始统计表 (频次累记)":
        current_df = df_general_log_stat_haida
    elif selected_tab == "月均化缩放统计表":
        current_df = df_general_log_stat_scaled_month_haida
    else:  # 概率化缩放统计表
        current_df = df_general_log_stat_scaled_prob_haida
    
    st.subheader("相关性分析-1：线性相关系数")
    
    # Select target variable for correlation analysis
    target_vars = ['使用月数 (包含中途离线)', '实际使用月数 (不含中途离线)']
    selected_target = st.selectbox(
        "选择目标变量",
        target_vars,
        key="corr_target_selector"
    )
    
    # Get numeric columns for correlation analysis
    numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove target variables from feature list
    feature_cols = [col for col in numeric_cols if col not in target_vars]
    
    # Calculate correlation matrix
    corr_matrix = current_df[feature_cols + [selected_target]].corr()[selected_target].sort_values(ascending=False)
    corr_matrix = corr_matrix.drop(selected_target)  # Remove self-correlation
    
    # Create correlation overview
    st.write("**相关性概览 (按相关系数排序):**")
    overview_data = []
    for feature, corr in corr_matrix.items():
        overview_data.append({
            '特征': feature,
            '相关系数': f"{corr:.3f}",
            '相关性强度': '强' if abs(corr) > 0.7 else '中等' if abs(corr) > 0.3 else '弱'
        })
    
    overview_df = pd.DataFrame(overview_data)
    st.dataframe(overview_df, height=210)
    
    # Add correlation explanation
    st.markdown("""
    **相关性强度说明:**
    - 强相关: |r| > 0.7
    - 中等相关: 0.3 < |r| ≤ 0.7
    - 弱相关: |r| ≤ 0.3
    """)
    
    st.markdown("---")
    
    # Create scatter plot for selected feature
    selected_feature = st.selectbox(
        "选择要分析的特征",
        feature_cols,
        key="corr_feature_selector"
    )
    
    # Create scatter plot
    fig = go.Figure()

    # Calculate correlation coefficient
    corr_value = current_df[selected_feature].corr(current_df[selected_target])

    # Add scatter plot with enhanced styling
    fig.add_trace(go.Scatter(
        x=current_df[selected_feature],
        y=current_df[selected_target],
        mode='markers',
        marker=dict(
            size=8,  # Reduced size to prevent overlap
            color='#2E86C1',
            opacity=0.6,  # Increased transparency
            line=dict(
                color='#1A5276',
                width=1
            )
        ),
        name='数据点',
        hovertemplate=(
            f"<b>设备信息</b><br>"
            f"{selected_feature}: %{{x:.2f}}<br>"
            f"{selected_target}: %{{y:.2f}}<br>"
            "<extra></extra>"
        )
    ))
    
    # Add trend line with enhanced styling
    z = np.polyfit(current_df[selected_feature], current_df[selected_target], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=current_df[selected_feature],
        y=p(current_df[selected_feature]),
        mode='lines',
        line=dict(
            color='#E74C3C',
            width=2,
            dash='solid'
        ),
        name='趋势线',
        hovertemplate=(
            f"<b>趋势线</b><br>"
            f"{selected_feature}: %{{x:.2f}}<br>"
            f"预测{selected_target}: %{{y:.2f}}<br>"
            "<extra></extra>"
        )
    ))
    
    # Add confidence interval
    y_pred = p(current_df[selected_feature])
    mse = np.mean((current_df[selected_target] - y_pred) ** 2)
    std = np.sqrt(mse)
    
    # Sort x values for proper confidence interval plotting
    x_sorted = np.sort(current_df[selected_feature])
    y_pred_sorted = p(x_sorted)
    
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_sorted, x_sorted[::-1]]),
        y=np.concatenate([y_pred_sorted + 1.96*std, y_pred_sorted[::-1] - 1.96*std]),
        fill='toself',
        fillcolor='rgba(231, 76, 60, 0.1)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='95% 置信区间',
        hoverinfo='skip'
    ))
    
    # Update layout with enhanced styling
    fig.update_layout(
        title=dict(
            text=f"{selected_feature} 与 {selected_target} 的相关性分析",
            font=dict(size=20, color='#2C3E50'),
            x=0.02,
            y=0.95
        ),
        xaxis=dict(
            title=dict(
                text=selected_feature,
                font=dict(size=14, color='#2C3E50')
            ),
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)'
        ),
        yaxis=dict(
            title=dict(
                text=selected_target,
                font=dict(size=14, color='#2C3E50')
            ),
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)'
        ),
        showlegend=False,
        plot_bgcolor='white',
        height=450,
        margin=dict(l=50, r=20, t=60, b=40),
        hovermode='closest'
    )
    
    # Add correlation coefficient as annotation
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.5,  # Center horizontally
        y=0.98,
        text=f"相关系数: {corr_value:.3f}",
        showarrow=False,
        font=dict(size=12, color='#2C3E50'),
        bgcolor='rgba(255, 255, 255, 0.8)',
        bordercolor='rgba(0, 0, 0, 0.1)',
        borderwidth=1,
        borderpad=4,
        xanchor='center'  # Center the text relative to x position
    )
    
    st.plotly_chart(fig, use_container_width=True)

    # Add a separator
    st.markdown("---")
    
    # Add new section for machine learning correlation analysis
    st.subheader("相关性分析-2：机器学习 (象征性)")
    
    # Select target variable for ML analysis
    ml_target_vars = ['使用月数 (包含中途离线)', '实际使用月数 (不含中途离线)']
    selected_ml_target = st.selectbox(
        "选择目标变量",
        ml_target_vars,
        key="ml_corr_target_selector"
    )
    
    # Add simple ML parameters control panel
    st.write("**模型参数设置:**")
    col1, col2 = st.columns(2)
    
    with col1:
        n_estimators = st.slider(
            "决策树数量",
            min_value=50,
            max_value=200,
            value=100,
            step=50,
            help="随机森林中决策树的数量"
        )
    
    with col2:
        max_depth = st.slider(
            "最大树深度",
            min_value=3,
            max_value=10,
            value=5,
            step=1,
            help="决策树的最大深度"
        )
    
    # Get numeric columns for ML analysis
    ml_numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove target variables from feature list
    ml_feature_cols = [col for col in ml_numeric_cols if col not in ml_target_vars]
    
    # Create feature importance visualization
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    
    # Prepare data
    X = current_df[ml_feature_cols]
    y = current_df[selected_ml_target]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model with selected parameters
    rf_model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    rf_model.fit(X_scaled, y)
    
    # Get model performance metrics
    from sklearn.metrics import r2_score, mean_squared_error
    y_pred = rf_model.predict(X_scaled)
    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))
    
    # Display model performance
    st.write("**模型性能:**")
    perf_col1, perf_col2 = st.columns(2)
    with perf_col1:
        st.metric("R² 分数", f"{r2:.3f}")
    with perf_col2:
        st.metric("RMSE", f"{rmse:.3f}")
    
    st.markdown("---")
    
    # Get feature importance
    feature_importance = pd.DataFrame({
        '特征': ml_feature_cols,
        '重要性': rf_model.feature_importances_
    }).sort_values('重要性', ascending=False)

    # Display feature importance table
    st.write("**特征重要性排序:**")
    st.dataframe(feature_importance, height=210)
    
    # Create feature importance plot
    fig_ml = go.Figure()
    
    # Sort feature importance in descending order
    feature_importance_sorted = feature_importance.sort_values('重要性', ascending=True)  # ascending=True for horizontal bar chart
    
    fig_ml.add_trace(go.Bar(
        x=feature_importance_sorted['重要性'],
        y=feature_importance_sorted['特征'],
        orientation='h',
        marker=dict(
            color='#2E86C1',
            opacity=0.7
        )
    ))
    
    fig_ml.update_layout(
        title=dict(
            text=f"特征重要性分析 (基于随机森林)",
            font=dict(size=20, color='#2C3E50'),
            x=0.02,
            y=0.95
        ),
        xaxis=dict(
            title=dict(
                text="特征重要性",
                font=dict(size=14, color='#2C3E50')
            ),
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(0, 0, 0, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(0, 0, 0, 0.2)',
            categoryorder='total ascending'  # This ensures the bars are sorted
        ),
        showlegend=False,
        plot_bgcolor='white',
        height=450,
        margin=dict(l=50, r=20, t=60, b=40),
        hovermode='closest'
    )
    
    # Display feature importance plot
    st.plotly_chart(fig_ml, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    **说明:**
    - 特征重要性基于随机森林回归模型
    - 重要性分数表示每个特征对预测目标变量的贡献程度
    - 分数越高表示该特征对目标变量的影响越大
    """)

elif page == "聚类分析":
    st.markdown("---")
    st.header("聚类分析")
    
    # Add dataframe selection
    st.subheader("选择数据视图")
    selected_tab = st.selectbox(
        "选择要分析的数据表",
        ["原始统计表 (频次累记)", "月均化缩放统计表", "概率化缩放统计表"],
        key="cluster_tab_selector"
    )
    
    # Set the current dataframe based on selection
    if selected_tab == "原始统计表 (频次累记)":
        current_df = df_general_log_stat_haida
    elif selected_tab == "月均化缩放统计表":
        current_df = df_general_log_stat_scaled_month_haida
    else:  # 概率化缩放统计表
        current_df = df_general_log_stat_scaled_prob_haida
    
    # Select grouping variable
    group_vars = ['使用月数 (包含中途离线)', '实际使用月数 (不含中途离线)']
    selected_group_var = st.selectbox(
        "选择分组变量",
        group_vars,
        key="group_var_selector"
    )
    
    # Get numeric columns for aggregation
    numeric_cols = current_df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [col for col in numeric_cols if col not in group_vars]
    
    # Group by selected variable and calculate means
    grouped_df = current_df.groupby(selected_group_var)[feature_cols].mean().reset_index()
    
    # Display grouped data
    st.write("**按使用月数分组的特征均值:**")
    st.dataframe(grouped_df, height=210)
    
    # Create line chart for selected features
    st.write("**特征均值随使用月数的变化:**")
    
    # Select features to display
    selected_features = st.multiselect(
        "选择要显示的特征",
        feature_cols,
        default=feature_cols[:3],  # Default to first 3 features
        key="feature_selector"
    )
    
    if selected_features:
        # Create line chart
        fig = px.line(
            grouped_df,
            x=selected_group_var,
            y=selected_features,
            markers=True,
            title='特征均值随使用月数的变化'
        )
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='特征均值随使用月数的变化',
                font=dict(size=20, color='#2C3E50'),
                x=0.02,
                y=0.95
            ),
            xaxis=dict(
                title=selected_group_var,
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            yaxis=dict(
                title='特征均值',
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            plot_bgcolor='white',
            height=450,
            margin=dict(l=50, r=20, t=60, b=40)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation
    st.markdown("""
    **说明:**
    - 数据按使用月数分组
    - 每个使用月数下的特征值取平均值
    - 可以通过选择不同的特征来观察它们随使用月数的变化趋势
    """)

    
