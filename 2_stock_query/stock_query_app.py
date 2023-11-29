import streamlit as st #all streamlit commands will be available through the "st" alias
import stock_query_lib as glib #reference to local lib script
import stock_query_database_lib as databaselib #reference to local lib script

def print_result(st, chat_response):
    st.markdown(chat_response['intermediate_steps'][1])
    if not chat_response['result']:
        st.markdown('Result: No result')
    else:
        st.markdown('Result:' + chat_response['result']) 

def stock_query():
    st.title("Stock Query Agent") 
    st.write("try: what is the stock ticker for Amazon?")

    if 'database' not in st.session_state: #see if the database index hasn't been created yet
        with st.spinner("Initial Database"): #show a spinner while the code in this with block runs
            databaselib.initial_database() 
            st.session_state.database = True #marked as database created
        
    if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
        st.session_state.chat_history = [] #initialize the chat history
        
    input_text = st.chat_input("What is the ticker symbol for Amazon?") #display a chat input box

    if input_text:
    
        with st.chat_message("user"): #display a user chat message
            st.markdown(input_text) #renders the user's latest message
        
        st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
        chat_response = glib.query_stock(input_text)
    
        with st.chat_message("assistant"): #display a bot chat message
            print_result(st, chat_response)
    
        st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history

