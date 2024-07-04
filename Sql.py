#!/usr/bin/env python
# coding: utf-8

# In[6]:


from langchain_community.utilities import SQLDatabase
def sql():
    db_user="root"
    db_password="ydy2350149"
    db_host="localhost"
    db_database="meeting_rooms"
    db=SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}")
    return db

