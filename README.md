# Overview
This is a simple demo of Amazon Bedrock, with AI21 and Anthropic model with langchain. For more detail please reference the following link: <br />
- <a href="https://aws.amazon.com/bedrock/" target="_blank">https://aws.amazon.com/bedrock/ </a>
- <a href="https://www.ai21.com/ " target="_blank">https://www.ai21.com/ </a>
- <a href="https://www.anthropic.com/index/claude-2" target="_blank">https://www.anthropic.com/index/claude-2 </a>

# Setup
 Setup <a href='https://docs.aws.amazon.com/cloud9/latest/user-guide/setting-up.html' target='_blank'> Cloud9 <a><br />
 Setup <a href='https://docs.python-guide.org/starting/install3/linux/' target='_blank'> Python <a><br />

 Download source code and install package <br />
 > git clone https://github.com/nguyendinhthi0705/bedrock-rag-stock.git <br />
 > cd bedrock-rag-stock <br />
 > pip3 install -r requirements.txt <br />

# Architect 
## App 1: Architecture - RAG with document
![Architecture 01](./images/architecture01.png)


## App 2: Architecture - Text To SQL Query 
![Architecture 02](./images/architecture02.png)


## App 3: Architecture - ReAct and Agents
![Architecture 02](./images/architecture03.jpg)
# Start App:
 >   streamlit run main.py --server.port 8080
    