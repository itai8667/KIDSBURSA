import streamlit as st
import yfinance as yf
import pandas as pd
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="בורסה לילדים",
    layout="wide",
    initial_sidebar_state="collapsed"
)

refresh_count = st_autorefresh(interval=120000, limit=None, key="auto_refresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700;900&display=swap');

/* הסתרת הסיידבר לגמרי — כולל הכפתור לפתיחתו */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
button[kind="header"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

/* עיצוב כללי */
.stApp {
    direction: rtl !important;
    font-family: 'Heebo', sans-serif !important;
}
.block-container {
    direction: rtl !important;
    max-width: 1100px;
    padding-top: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

h1, h2, h3, h4, h5, h6 {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

.stMarkdown p, .stMarkdown li {
    direction: rtl !important;
    text-align: right !important;
    font-family: 'Heebo', sans-serif !important;
}

[data-testid="stSlider"] { direction: ltr !important; }
[data-testid="stRadio"] { direction: rtl !important; text-align: right !important; }

/* טאבים */
.stTabs [data-baseweb="tab-list"] { direction: rtl !important; gap: 6px; }
.stTabs [data-baseweb="tab"] {
    font-size: 17px !important;
    font-weight: 700 !important;
    font-family: 'Heebo', sans-serif !important;
}

/* כפתור הגרלה */
div.stButton > button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: 700;
    width:
