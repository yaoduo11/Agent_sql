import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain import SQLDatabase
from Sql import sql
from Kimi import Kimi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import MessagesPlaceholder
#from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
#from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
#from operator import itemgetter
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory,
)
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
import os
import re
#langsmith运行环境
#langsmith运行环境
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
#os.environ["OPENAI_API_KEY"]="sk-649wIPk2jJsV2iorRvk9Yud0bZ5puRN8nGDZivMi8wP"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"]="default"
import re
#import chromadb
#from chromadb.config import Settings
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
#from langchain_community.embeddings import FakeEmbeddings
from langchain_community.embeddings import BaichuanTextEmbeddings
from PIL import Image
st.image("logo.png")
#st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="logo.png")
title_color = "#04256e"  # 自定义标题颜色
header_color = "#0d3a9b"
st.markdown(
    f"""
    <style>
    .stTitle {{
        color: {title_color};
    }}
    .stHeader {{
        color: {header_color};
        text-indent: 0.5em;
    }}
     .indented-text {{
        text-indent: 3em;
        margin-top: 30px;       /* 段前间距 */
        margin-bottom: 30px;  /* 缩进2字符 */
    }}
    .indented-str {{
        text-indent: 2em;
        margin-top: 10px;       /* 段前间距 */
        margin-bottom: 10px;
        color: {header_color};  /* 缩进2字符 */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
    h1 {
      font-size: 36px;
      text-align:left;
      text-transform: uppercase;
   }
    h2 {
      font-size: 30px;
      text-align: left;
      text-transform: uppercase;
   }
    h3 {
      font-size: 20px;
      text-align: left;
      text-transform: uppercase;
   }        
</style>
""", unsafe_allow_html=True)
st.markdown(f'<h1 class="stTitle">Conference room reservation Q&A assistant</h1>', unsafe_allow_html=True)
st.text("")

#st.title("📖")

msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("Hello, I am your conference room management assistant! I can help you book, inquire, update and delete meeting room reservations.Please tell me what is your problem?")

view_messages = st.expander("View the message contents in session state")
#db=sql()
db=SQLDatabase.from_uri(r"sqlite:///G:\Sqlite\meeting_rooms.db")
print(db.table_info)
llm=Kimi()
#print(db.table_info)
examples = [
    {"input": "List all rooms.", "query": "SELECT * FROM rooms;"},
    {
        "input": "Are there any meeting rooms available on June 25,2024, from 10:00 AM to 11:00 AM?",
        "query": "SELECT r.room_number FROM rooms r WHERE r.is_available = 1 AND NOT EXISTS ( SELECT 1 FROM reservations WHERE reservations.room_number = r.room_number AND reservations.start_time <= '2024-06-25 11:00:00' AND reservations.end_time >= '2024-06-25 10:00:00' );",
    },
    {
        "input": "Could you assist with booking A1012 from 9 to 10 am on the 28th?",
        "query": "INSERT INTO reservations (room_number, user_name, start_time, end_time) VALUES ('A1012', 'Human', '2024-06-28 09:00:00', '2024-06-28 10:00:00');",
    },
    {
        "input": "Help me book a C101 meeting room for me.",
        "query": "INSERT INTO reservations (room_number, user_name, start_time, end_time) VALUES ('C101', 'me', datetime('now'), datetime('now', '+1 hour'));",
    },
    {
        "input": "Help me delete the conference room I just booked A1022.",
        "query": "DELETE FROM reservations WHERE room_number = 'A1022';",
    },
    {
        "input": "Help me delete the conference room I just booked",
        "query": "DELETE FROM reservations WHERE id = {id};",
    },
    {
        "input": "Is conference room A1012 available?",
        "query": "SELECT `is_available` FROM `rooms` WHERE `room_number` = 'A1012';",
    },
    {
        "input": "Is conference room A1012 available from 9 Am to 10 Am on the 18th?",
        "query": "SELECT `is_available` FROM rooms WHERE room_number = 'A1012' AND `is_available` = 1 AND ((`created_at` <= '2024-06-18 09:00:00' AND `updated_at` >= '2024-06-18 09:00:00') OR (`created_at` <= '2024-06-18 10:00:00' AND `updated_at` >= '2024-06-18 10:00:00'));",
    },
    {
        "input": "What type of C101 meeting room is this?.",
        "query": "SELECT `room_type` FROM `rooms` WHERE `room_number` = 'C101';",
    },
    {
        "input": "Help me find a conference room that can accommodate 30 people?",
        "query": "SELECT `room_number`, `is_available` FROM `rooms` WHERE `capacity` >= 30 AND `is_available` = 1 LIMIT 1;",
    },
    {
        "input": "How many people can conference room A1022 accommodate?",
        "query": "SELECT capacity FROM rooms WHERE room_number = 'A1022';",
    },
    {
        "input": "Help me find a meeting room in the library.",
        "query":"SELECT `room_number`, `capacity`, `room_type` FROM `rooms` WHERE `location` LIKE '%library%' AND `is_available` = 1 LIMIT 5;"
    },
    {
        "input": " Please Help me delete the conference room with id=97.",
        "query": " DELETE FROM reservations WHERE reserved_id = 97;",
    },
    {
        "input": "Help me change the conference room I just booked to C101?",
        "query":"UPDATE reservations SET room_number = 'C101' WHERE id = {id};"
    },
    {
        "input": "Help me change the conference room with id=97 to H202",
        "query": "UPDATE reservations SET room_number = 'H202'WHERE reserved_id = 97;",
    },
]
system=("Please answer the corresponding question by writing SQLite  code, using the following database table information:{info} \n"
        "The question is: {input}\n"
        "Ensure the SQL query is correct and does not include any table aliases (like 'r.' or 'res.').\n"
        "Ensure the SQL code is correct, and includes no additional text.\n"
        "Users can only reserve one meeting room at the same time"
        "Get the reservation ID value from the AI answer of the historical conversation and replace {id},Generate correct executable sql code"
        "user_name default value='Human'"
        "Don't use DROP statement"
        "```sql\n...\n```"
       )
example_prompt = ChatPromptTemplate.from_template("{input}\nSQL code: {query}")
embeddings =BaichuanTextEmbeddings(baichuan_api_key="sk-f10e1b6e67585b28f774c8cb06a992dd")
#embeddings=FakeEmbeddings(size=1536)
vectorstore= Chroma()
vectorstore.delete_collection()
example_selector=SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    vectorstore,
    k=3,
    input_keys=["input"],
    

)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=example_selector,
     input_variables=["input"], #"dialect", "top_k"
)
prompt = ChatPromptTemplate.from_messages([
    ('system',system),
    few_shot_prompt,
    MessagesPlaceholder(variable_name='history'),
    ('human','{input}')                          
        ])

def get_schema(_) -> str:
    return db.get_table_info()
def run(query):
    try:
        return db.run_no_throw(query)
    except Exception as e:
        return f"Error: {str(e)}"

def get_sql(x):
    # 定义正则表达式来匹配不同形式的 SQL 语句
    pattern = r"(?:SQL query:\s*(.*?)(?:(?=\s*```)|$))|(?:```sql\s*(.*?)\s*```)|(?:^(.*?)\s*```$)"
    match = re.search(pattern, x, re.DOTALL)
    
    if match:
        # 如果匹配到以 "SQL query:" 开头的情况
        if match.group(1):
            sql_query = match.group(1).strip()
        # 如果匹配到以 ```sql 开头和 ``` 结尾的情况
        elif match.group(2):
            sql_query = match.group(2).strip()
        # 如果匹配到包含 SQL 语句并以 ``` 结尾的情况
        elif match.group(3):
            sql_query = match.group(3).strip()
        else:
            sql_query = ""
        return sql_query

    return x.strip()
import ast
def get_id():
    result = db.run("SELECT last_insert_rowid();")
    # 将字符串解析为列表
    result_list = ast.literal_eval(result)
    # 提取 id 值
    return str(result_list[0][0])
#生成正确的sql语句
chain_sql=(#{"info":get_schema,"question":RunnablePassthrough()}
           #|RunnableLambda(get_session_history)
           #RunnablePassthrough.assign(id=get_id)
           RunnablePassthrough.assign(id=lambda x: get_id())
           |prompt
           |llm
           |StrOutputParser()
           |RunnableLambda(get_sql)
           )

execute=("Please provide a natural language answer to the {input} by combining the following database information, questions and execution results of the sql code:\n"
"Generate concise responses based on SQL {query} results."
"Ensure that the result:{response} include key information and Don't appear sql code content."
"After executing an INSERT statement, result content include reserved_id={id} and save it for subsequent queries."

)


execute_prompt=ChatPromptTemplate.from_messages([
    ('system',execute),
    MessagesPlaceholder(variable_name='history'),
    ('human','{input}')                          
        ])
execute_sql=(#{"info":get_schema,"question":RunnablePassthrough()}
             RunnablePassthrough.assign(query=chain_sql)
             |RunnablePassthrough.assign(response=lambda x:run(x["query"]))
             |RunnablePassthrough.assign(id=lambda x: get_id())
             |execute_prompt
             |llm
             |StrOutputParser())

runnable_with_history=RunnableWithMessageHistory(
    execute_sql,
    lambda session_id: msgs,
    #get_session_history,
    input_messages_key="input",
    history_messages_key="history",
    #output_messages_key="answer"
)
import time
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    with st.spinner('Please Wait for it...'):
             time.sleep(3)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "c"}}
    
    response = runnable_with_history.invoke({"input": prompt,"info":db.table_info}, config)
    if "Error:" in response:
        st.chat_message("ai").write("Sorry, the content was incorrectly recognized, please re-enter. For example: booking C102, etc. short sentences")
    else:
        st.chat_message("ai").write(response)
with view_messages:
    """
    Message History initialized with:
    ```python
    msgs = StreamlitChatMessageHistory(key="langchain_messages")
    ```

    Contents of `st.session_state.langchain_messages`:
    """
    view_messages.json(st.session_state.langchain_messages)
#uploaded_file = st.file_uploader("Choose a file")
#if uploaded_file is not None:
 #   file_c=uploaded_file.getvalue()#用二进制读数据库
  #  file_p="file"
#else:
   # st.stop()
