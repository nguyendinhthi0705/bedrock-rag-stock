import os
from langchain.memory import ConversationBufferWindowMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationalRetrievalChain

from langchain.embeddings import BedrockEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
import json
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.tools import DuckDuckGoSearchRun
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain
from datetime import datetime, timedelta
from pandas_datareader import data as pdr
from datetime import date

def get_llm():
        
    model_parameter = {"temperature": 0.0, "top_p": .5, "max_tokens_to_sample": 2000}
    
    llm = Bedrock(
        credentials_profile_name=os.environ.get("BWB_PROFILE_NAME"), #sets the profile name to use for AWS credentials (if not the default)
        region_name=os.environ.get("BWB_REGION_NAME"), #sets the region name (if not the default)
        endpoint_url=os.environ.get("BWB_ENDPOINT_URL"), #sets the endpoint URL (if necessary)
        model_id="anthropic.claude-v2", #set the foundation model
        model_kwargs=model_parameter) #configure the properties for Claude
    
    return llm



from langchain.prompts.prompt import PromptTemplate

_DEFAULT_TEMPLATE = """Human: Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
<format>
Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Result of SQLResult only"
</format>
Assistant: Understood, I will use the above format and only provide the answer.

Only use the following tables:
<tables>
CREATE TABLE stock_ticker (
	symbol text PRIMARY KEY,
	name text NOT NULL,
	currency text,
	stockExchange text, 
    exchangeShortName text
)
</tables>

If someone asks for ticker symbol, they really mean the stock_ticker table.
<examples>
Question: 
        What is the ticker symbol for Amazon?
        Params: 
        Company name (name): Amazon
        
SQLQuery:SELECT symbol FROM stock_ticker WHERE name LIKE '%Amazon%'

</examples>

Question: {input}

"""

PROMPT = PromptTemplate(
    input_variables=["input", "dialect"], template=_DEFAULT_TEMPLATE
)

def get_db_chain(prompt):
    db = SQLDatabase.from_uri("sqlite:///stock_ticker_database.db")
    llm = get_llm()
    db_chain = SQLDatabaseChain.from_llm(
        llm, 
        db, 
        verbose=True, 
        return_intermediate_steps=True, 
        prompt=prompt, 
    )
    return db_chain
    
def query_stock(input_text):
    db_chain = get_db_chain(PROMPT)
    response = db_chain(input_text)
    
    return response['result']

