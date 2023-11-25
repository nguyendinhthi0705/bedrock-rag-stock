import streamlit as st 
import stock_analysis_lib as glib 
import stock_analysis_database_lib as databaselib 
from langchain.callbacks import StreamlitCallbackHandler
import time
import pandas as pd

st.set_page_config(page_title="Stock Analysis App", page_icon=":robot:", layout="wide") 

if 'database' not in st.session_state: 
    with st.spinner("Initial Database"): 
        databaselib.initial_database() 
        
if 'chat_history' not in st.session_state: 
    st.session_state.chat_history = [] 

agent = glib.initializeAgent()
input_text = st.chat_input("Type company name here!") 

if input_text:
    message_placeholder = st.empty()
    st_callback = StreamlitCallbackHandler(st.container())
    response = agent({
            "input": input_text,
            "chat_history": st.session_state.chat_history,
        },
        callbacks=[st_callback])
    st.header("Below are the summary:")
    st.subheader("Price Chart:")
    st.line_chart(pd.DataFrame(response['intermediate_steps'][1][1],columns=['High','Low','Close']))
    st.subheader("Volume Chart:")
    st.line_chart(pd.DataFrame(response['intermediate_steps'][1][1],columns=['Volume']))
    st.subheader("Final Suggestion:")
    st.write(response['output'])


    

