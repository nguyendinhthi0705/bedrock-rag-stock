import streamlit as st
import sys
sys.path.append("./1_stock_qna")
sys.path.append("./2_stock_query")
sys.path.append("./3_stock_tools")
sys.path.append("./4_stock_analysis")
from stock_qna_app import stock_qna 
from stock_query_app import stock_query
from stock_tools_app import stock_tools
from stock_analysis_app import stock_analysis
from PIL import Image



st.sidebar.success("Select a a tool below.")

image = Image.open('Artificial-Intelligence-Stocks.jpg')
st.image(image, caption='')


page_names_to_funcs = {
    "Stock Analysis": stock_analysis,
    "Stock Tools": stock_tools,
    "Stock Q&A": stock_qna, 
    "Stock Query": stock_query,
}

demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()