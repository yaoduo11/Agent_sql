import mysql.connector
import streamlit as st
import sqlite3
from Sql import sql
import pandas as pd
connection=mysql.connector.connect(
    host='localhost',
    user='root',
    password='ydy2350149',
    database='meeting_rooms'
)
cursor=connection.cursor()

cursor.execute("Select * from reservations")
data=cursor.fetchall()
title_color = "#04256e"  # 自定义标题颜色
header_color = "#0d3a9b"
st.markdown(
    f"""
    <style>
    .stTitle {{
        color: {title_color};
        margin-top: 10px;       /* 段前间距 */
        margin-bottom: 20x;
    }}
    .indented-str {{
        text-indent: 2em;
        margin-top: 10px;       /* 段前间距 */
        margin-bottom: 40px;
        color: {header_color};  /* 缩进2字符 */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
    h1 {
      font-size: 52px;
      text-align:left;
      text-transform: uppercase;
   }
    h3 {
      font-size: 20px;
      text-align: left;
      text-transform: uppercase;
   }      
</style>
""", unsafe_allow_html=True)
st.markdown(f'<h1 class="stTitle">🤓SQLDatabese&Show</h1>', unsafe_allow_html=True)
st.text("")
df=pd.DataFrame(data,columns=cursor.column_names,)
st.dataframe(df)
#conn = sqlite3.connect(r'G:\Sqlite\meeting.db')
#cursor=conn.cursor()
#cursor.execute("Select * from reservations")
#data=cursor.fetchall()
#column_names = [description[0] for description in cursor.description]
#for column in column_names:
 #   print(column)
#st.title('streamlit MySQL Connection')
#df=pd.DataFrame(data,columns=column_names)
#st.dataframe(df)

