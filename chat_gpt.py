import json
import os
import time
from datetime import datetime
from openai import OpenAI
from config import openai_api_key, gpt_model

class ChatGPT:
    """OpenAI GPT API 交互类"""
    
    def __init__(self, memory_file="memory.json"):
        """初始化 ChatGPT
        
        Args:
            memory_file: 记忆文件路径
        """
        self.memory_file = memory_file
        self.client = OpenAI(api_key=openai_api_key)
        self.messages = self._load_memory()
        
    def _load_memory(self):
        """加载历史对话作为记忆
        
        Returns:
            对话历史消息列表
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return [
                {
                    "role": "system",
                    "content": "你是小Luna，一个可爱温柔、情商极高的陪伴型AI助手。你擅长提供情绪支持、鼓励和温暖的话语。你的语气总是轻柔、善解人意，并愿意倾听和安慰用户。"
                }
            ]
            
    def _save_memory(self):
        """保存对话历史到文件"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
            
    def chat(self, user_input):
        """与 GPT 交流
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            GPT 回复文本
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": timestamp
        })
        
        try:
            response = self.client.chat.completions.create(
                model=gpt_model,
                messages=self.messages,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content
            
            self.messages.append({
                "role": "assistant", 
                "content": reply,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self._save_memory()
            
            return reply
            
        except Exception as e:
            print(f"GPT 调用出错: {str(e)}")
            return f"抱歉，我遇到了一点小问题: {str(e)}"
