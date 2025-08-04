import streamlit as st
from app.pages_for_data_analysis import PagesDataAnalysis


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

PagesDataAnalysis.render(page_title='单设备处理')