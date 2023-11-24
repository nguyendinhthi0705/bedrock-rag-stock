import streamlit as st #all streamlit commands will be available through the "st" alias
import stock_analysis_lib as glib #reference to local lib script
import stock_analysis_database_lib as databaselib #reference to local lib script
from langchain.callbacks import StreamlitCallbackHandler
import time

st.set_page_config(page_title="RAG Chatbot") 
st.title("Stock Analysis Chatbot") 

if 'database' not in st.session_state: #see if the database index hasn't been created yet
    with st.spinner("Initial Database"): #show a spinner while the code in this with block runs
        databaselib.initial_database() 
        st.session_state.database = True #marked as database created
        
if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history

#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"]) #display the chat content
        
input_text = st.chat_input("Type company name here!") #display a chat input box


if input_text:
    message_placeholder = st.empty()
    full_response = ""
    st_callback = StreamlitCallbackHandler(st.container())
    result = glib.interact_with_agent_st(input_text,st.session_state.chat_history ,st_callback)
    for chunk in result:
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")

    message_placeholder.markdown(full_response)
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})

