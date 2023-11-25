import streamlit as st 
import stock_analysis_lib as glib 
import stock_analysis_database_lib as databaselib 
from langchain.callbacks import StreamlitCallbackHandler
import time
import pandas as pd
from PIL import Image


st.set_page_config(page_title="Stock Analysis Agent", page_icon=":robot:", layout="centered") 
image = Image.open('Artificial-Intelligence-Stocks.jpg')
st.image(image, caption='')
st.header("Stock Analysis Agent")
st.write("Try to input with company name like Amazon, Tesla..etc")


if 'database' not in st.session_state: 
    with st.spinner("Initial Database"): 
        databaselib.initial_database() 
        
if 'chat_history' not in st.session_state: 
    st.session_state.chat_history = [] 

agent = glib.initializeAgent()
input_text = st.chat_input("Type company name here!") 
ph = st.empty()
if input_text:
    ph.empty()
    st_callback = StreamlitCallbackHandler(st.container())
    response = agent({
            "input": input_text,
            "chat_history": st.session_state.chat_history,
        },
        callbacks=[st_callback])
    st.subheader("Stock Chart:")
    df = pd.DataFrame(response['intermediate_steps'][1][1],columns=['Close','Volume'])
    df['Volume'] = df['Volume']/10000000
    df.rename(columns={'Close':'Price(USD)','Volume':'Volume(10 millions)'},inplace=True)
    st.line_chart(df)
    st.subheader("Daily sticker:")
    st.dataframe(response['intermediate_steps'][1][1])
    st.subheader("Conclusion:")
    st.write(response['output'])


    

