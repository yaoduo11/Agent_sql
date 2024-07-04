import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
# 设置自定义主题的颜色
primary_color = "#ff5733"
background_color = "#ffffff"
secondary_background_color = "#2e8b57"
text_color = "#0d43bc"
title_color = "#04256e"  # 自定义标题颜色
header_color = "#04256e"
# 应用背景颜色
st.markdown("<h1 style='text-align: center; background-color: #000045; color: #ece5f6'>Introduction</h1>", unsafe_allow_html=True)
#st.markdown("<h4 style='text-align: center; background-color: #000045; color: #ece5f6'></h4>", unsafe_allow_html=True)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background_color};
    }}
    .stTitle {{
        color: {title_color};
    }}
    .stHeader {{
        color: "#2d66e2";
        text-indent: 0.5em;
    }}
     .indented-text {{
        text-indent: 1em;
        margin-top: 30px;       /* 段前间距 */
        margin-bottom: 30px;  /* 缩进2字符 */
    }}
    .indented-str {{
        text-indent: 0em;
        margin-top: 10px;       /* 段前间距 */
        margin-bottom: 10px;
        color:#97a6c4
        /* 缩进2字符 */
    }}
    .text{{
        text-indent: 2em;
        margin-top: 10px;       /* 段前间距 */
        margin-bottom: 10px;
        color:#041F50;
        font-size:18px;
        /* 缩进2字符 */
    }}

    </style>
    """,
    unsafe_allow_html=True
)
st.text("")
st.markdown(f'<h3 class="indented-str">------------------------------------------------------</h3>',unsafe_allow_html=True)
st.markdown(f'<h2 class="stHeader">🧊基于PDF文档的检索增强生成（RAG）系统</h2>', unsafe_allow_html=True)
#st.text("通过上传PDF文件，用户可对其内容进行提问，并能得到合适的答案")
st.markdown(f'<p class="text">欢迎使用我们的文档问答助手，这是一款基于PDF文档的检索增强生成（RAG）系统，用户通过上传pdf文档后并提出与文档相关的问题，系统会帮助您快速从文档中提取和生成相关信息。以下是关键功能：</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">1、PDF文件上传与解析</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">2、智能信息检索</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">3、自然语言处理与回答生成</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">4、对话时上下文保留</p>', unsafe_allow_html=True)
st.markdown(f'<h2 class="stHeader">🧊使用LLM构建SQL数据库交互的问答系统</h2>', unsafe_allow_html=True)
st.markdown(f'<p class="text">欢迎使用智能会议室预约管理助手，这是一个专为会议室预订和管理设计的智能数据库交互系统。利用先进的语言模型（LLM），该系统可以帮助您轻松预订、更新、删除和查询会议室。以下是系统的主要功能和实现内容：</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">1、系统根据用户的输入查询会议室</p>', unsafe_allow_html=True)
st.markdown(f'<p class="text" style="font-weight: bold;">2、用户想要预定会议室、更改和删除所预定的会议室时，系统会执行相应的操作</p>', unsafe_allow_html=True)
# 设置自定义标题颜
st.markdown("""
<style>
    h1 {
      font-size: 52px;
      text-align:left;
      text-transform: uppercase;
   }
    h2 {
      font-size: 24px;
      text-align: left;
      text-transform: uppercase;
   }
    h3 {
      font-size: 18px;
      text-align: center;
      text-transform: uppercase;
   }
    p {
        font-size: 16px;
        text-align: justify;
        line-height: 1.6;
        color: #4b0082; /* 靛蓝色 */
        margin-top: 20px;
        margin-bottom: 20px;
    }
                    
</style>
""", unsafe_allow_html=True)