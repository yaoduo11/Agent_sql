#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, tempfile
import pinecone
from pathlib import Path

from langchain.chains import ConversationChain
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings
from langchain.vectorstores import Chroma
#from langchain import OpenAI
#from langchain.llms.openai import OpenAIChat
#from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
#from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain import hub
#from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import HumanMessage
from langchain_core.chat_history import AIMessage
import streamlit as st

st.set_page_config(page_title="RAG")
st.title("Retrieval Augmented Generation Engine")
loader_pdf = PyPDFLoader(r"G:\llm program\2324_guidebook.pdf") 
docs = loader_pdf.load()

#text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=0)
all_splits = text_splitter.split_documents(docs)
#vectorstore = Chroma.from_documents(documents=all_splits,embedding=QianfanEmbeddingsEndpoint())
vectorstore = Chroma.from_documents(documents=all_splits,embedding=FakeEmbeddings(size=1536))
retriever = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 20})  
    
import sys
sys.path.append(r'F:\PyCharm 2024.1\pythonProject')
os.environ["API_KEY"] = "sk-hF6MmoJLUt0xQ9PUBjQ0GJrYf3K2i3GRiXGyUNtBGsEYFKnI"
from Kimi import Kimi
llm = Kimi()
### Answer question ###
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. Use three sentences maximum and keep the "
    "answer concise.answer Don't use the word 'not' "
    "\n\n"
    "{context}"
)
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
rag_chain = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | qa_prompt
    | llm
    | StrOutputParser()
)

retrieve_docs = (lambda x: x["input"]) | retriever

chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
    answer=rag_chain
)


### Statefully manage chat history ###
store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
#msgs = StreamlitChatMessageHistory(key="special_app_key")
memory = ConversationBufferMemory()

import time
msgs = StreamlitChatMessageHistory(key="special_app_key")
def invoke_with_retry(chain_with_history, query, delay=3):
    try:
        return chain_with_history.invoke(
            {"input": query},
            config={"configurable": {"session_id": "abc"}}
        )['answer']
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(3)  # 在捕获异常后等待指定的秒数
        return "Failed to get a response."
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,  
    input_messages_key="input",
    history_messages_key="history",
    output_messages_key="answer",
)

if 'messages' not in st.session_state:
        st.session_state['messages'] = [] 
 
    #
for message in st.session_state.messages:
     if isinstance(message,HumanMessage):
          with st.chat_message("user"):
               st.markdown(message.content)
     elif isinstance(message,AIMessage):
          with st.chat_message("assistant"):
               st.markdown(message.content)            
if query := st.chat_input():
        st.session_state['messages'].append(HumanMessage(content=query))
        st.balloons()
        st.chat_message("human").write(query)
        with st.spinner('Please Wait for it...'):
             time.sleep(3)
        config = {"configurable": {"session_id": "any"}}
        answer = invoke_with_retry(chain_with_history, query,config)
        st.session_state['messages'].append(AIMessage(content=answer)) 
        st.chat_message("ai").write(answer)

# In[ ]:




