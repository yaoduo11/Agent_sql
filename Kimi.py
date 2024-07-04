#!/usr/bin/env python
# coding: utf-8

# In[5]:


import logging
from typing import Any
from langchain_core.language_models import LLM
from langchain_community.llms import OpenAI
from openai import OpenAI
class Kimi(LLM):
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return LLM
        
    # 必须定义 _call 方法
    def _call(self, prompt: str, **kwargs: Any) -> str:
        try:
            client =OpenAI(
                # 请替换为您自己的 API 密钥
            api_key="sk-649wIPk2jJsV2iorRvk9Yud0bZ5puRN8nGDZivMi8wPn54MA",
            base_url="https://api.moonshot.cn/v1",
           )
            
            completion = client.chat.completions.create(
                model="moonshot-v1-8k",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Error in Kimi _call: {e}", exc_info=True)
            raise
            
            
    


# In[ ]:




