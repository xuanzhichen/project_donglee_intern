"""
Intelligent Controller - Log Data Analysis Platform
Donglee Intelligence-Cloud Co., Ltd. Internship Project Delivery

智能控制器-日志数据分析平台
智云科技有限公司实习项目交付
"""

# Author: Xuanzhi Chen (陈炫志)
# Email: xuanzhichen.42@gmail.com
# License: MIT

# Latest Update: 2025/07/29


import os
import sys
import streamlit as st

# To fix the issue regarding failing to recognize the import path 
# I don't setup variable-environment for my IDE when run this project in a local computer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# st.set_page_config(
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# st.title("智云设备日志-数据分析与自查平台")

# st.sidebar.title("菜单")
# page = st.sidebar.radio(
#     "请选择对应的功能", 
#     [
#         "操作说明", 
#         "单设备处理", 
#         "多设备处理",
#         "相关性分析"
#     ]
# )

# if page == "操作说明":
#     st.markdown("---")
#     st.header("操作说明")
#     st.markdown("该页面正在建设中...", help="该部分内容会在正式部署后完善")

# elif page == "单设备处理":
#     page_title = '单设备处理'
#     PagesDataAnalysis.render(page_title)

# elif page == "多设备处理":
#     page_title = '多设备处理'
#     PagesDataAnalysis.render(page_title)

# elif page == '相关性分析':
#     st.markdown("---")
#     st.header("相关性分析")
#     st.markdown("该页面正在建设中...", help="该部分内容会在正式部署后完善")


# Get the absolute path to the image file
image_path = os.path.join(os.path.dirname(__file__), "image", "donglee_zhiyun_logo_2_2.png")

# Check if the image file exists before trying to use it
if os.path.exists(image_path):
    st.logo(
        image=image_path,
        size="large",
        icon_image=image_path
    )
else:
    # Fallback: use a simple title instead of logo
    st.title("智能控制器-日志数据分析平台")

pages = [
    st.Page(
        "page_intern_intro.py",
        title="简介 (Intro to my Intern Project)",
        icon=":material/home:"
    ),
    st.Page(
        "page_instruction.py",
        title="操作说明",
        icon=":material/article:"
    ),
    st.Page(
        "page_single_device_processing.py",
        title="单设备处理",
        icon=":material/insert_chart:"
    ),
    st.Page(
        "page_multiple_devices_processing.py",
        title="多设备处理",
        icon=":material/insert_chart:"
    ),
    st.Page(
        "page_correlation_analysis.py",
        title="相关性分析",
        icon=":material/widgets:"
    ),
]

page = st.navigation(pages)
page.run()

# Inject custom CSS to fix the width of the sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 345px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar.container(height=245):

    if page.title == "简介 (Intro to my Intern Project)":
        st.page_link("page_intern_intro.py", label="简介 (Intro to my Intern Project)", icon=":material/help_outline:")
        st.write("该页面正在建设中...")

    if page.title == "操作说明":
        st.page_link("page_instruction.py", label="操作说明", icon=":material/help_outline:")
        # st.write("欢迎使用智能控制器-日志数据分析平台!")
        st.markdown("""
            该模块向您介绍平台所涵盖的数据分析功能与开发背景。
            作为示例，平台将在其余模块自动为您预加载一份智能控制器的样例日志，以便向您直接演示相应的处理效果；
            当上传并覆盖为您感兴趣的日志后，后台程序会自动为您重新运行。
        """)

    if page.title == "单设备处理":
        st.page_link("page_single_device_processing.py", label="单设备处理", icon=":material/help_outline:")
        st.write(
            "该模块协助您细致排查某一控制器在其使用周期内（由于更换电池，或设备故障引起的）连续与中断变化，"
            "并依据时间轴可视化其不同操作类型的切换，以及其信号强度的波动情况。"
        )
        
    if page.title == "多设备处理":
        st.page_link("page_multiple_devices_processing.py", label="多设备处理", icon=":material/help_outline:")
        st.write(
            "该模块协助您批量统计多台控制器的使用时长及对应参数，"
            "并可视化它们的操作类型和信号强度的频次分布。"  
        )
        st.write("对于您在多设备处理中识别出的个别设备，您亦可返回 “单设备处理” 模块，进行细致的排查。")

    if page.title == "相关性分析":
        st.page_link("page_correlation_analysis.py", label="相关性分析", icon=":material/help_outline:")
        st.write(
            "该模块允许您上传在 “多设备处理” 模块中得到的 “基于日志的参数统计表”，"
            "并采用基础的机器学习向您挖掘不同参数（特征）之间的相关性。"
        )
        st.write("示例：控制器的信号强度与使用时长之间的相关性分析")

st.sidebar.caption(
    """
    **智能控制器-日志数据分析平台**  
    产品部 实习项目  
    2025.04.22 - 2025.08.04  
    [广东·东篱智云科技有限公司](http://www.donglee.net/)  


    Copyright © 2025 *Xuanzhi Chen* (Donglee Intelligence-Cloud Co., Ltd.) All rights reserved.
    """
)

    