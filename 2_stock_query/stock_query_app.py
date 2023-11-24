import streamlit as st #all streamlit commands will be available through the "st" alias
import stock_query_lib as glib #reference to local lib script
import stock_query_database_lib as databaselib #reference to local lib script


st.set_page_config(page_title="RAG Chatbot") 
st.title("Stock Query Chatbot") 

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
        
input_text = st.chat_input("What is the ticker symbol for Amazon?") #display a chat input box


if input_text:
    
    with st.chat_message("user"): #display a user chat message
        st.markdown(input_text) #renders the user's latest message
        
    st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
    chat_response = glib.query_stock(input_text=input_text)
    
    with st.chat_message("assistant"): #display a bot chat message
        st.markdown(chat_response) #display bot's latest response
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history

