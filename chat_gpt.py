import json
import os
import time
import re
from datetime import datetime
from openai import OpenAI
from config import openai_api_key, gpt_model, personality_prompt

class ChatGPT:
    """OpenAI GPT API 交互类"""
    
    def __init__(self, memory_file="memory.json", long_memory_file="memory_long.json"):
        """初始化 ChatGPT
        
        Args:
            memory_file: 记忆文件路径
            long_memory_file: 长期记忆文件路径
        """
        self.memory_file = memory_file
        self.long_memory_file = long_memory_file
        self.client = OpenAI(api_key=openai_api_key)
        self.messages = self._load_memory()
        self.long_memory = self._load_long_memory()
        
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
                    "content": personality_prompt
                }
            ]
            
    def _load_long_memory(self):
        """加载长期记忆
        
        Returns:
            长期记忆数据
        """
        if os.path.exists(self.long_memory_file):
            with open(self.long_memory_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {
                "conversations": [],
                "preferences": {
                    "likes": [],
                    "dislikes": [],
                    "interests": []
                }
            }
            
    def _save_memory(self):
        """保存对话历史到文件"""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
            
    def _save_long_memory(self):
        """保存长期记忆到文件"""
        with open(self.long_memory_file, "w", encoding="utf-8") as f:
            json.dump(self.long_memory, f, ensure_ascii=False, indent=2)
            
    def _extract_preferences(self, text):
        """从文本中提取用户偏好
        
        Args:
            text: 用户输入文本
            
        Returns:
            提取的偏好字典
        """
        preferences = {
            "likes": [],
            "dislikes": [],
            "interests": []
        }
        
        like_patterns = [
            r"我喜欢([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我爱([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我超爱([\u4e00-\u9fa5a-zA-Z0-9]+)"
        ]
        
        dislike_patterns = [
            r"我不喜欢([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我讨厌([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我不爱([\u4e00-\u9fa5a-zA-Z0-9]+)"
        ]
        
        interest_patterns = [
            r"我想([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我要学([\u4e00-\u9fa5a-zA-Z0-9]+)",
            r"我对([\u4e00-\u9fa5a-zA-Z0-9]+)感兴趣"
        ]
        
        for pattern in like_patterns:
            matches = re.findall(pattern, text)
            preferences["likes"].extend(matches)
            
        for pattern in dislike_patterns:
            matches = re.findall(pattern, text)
            preferences["dislikes"].extend(matches)
            
        for pattern in interest_patterns:
            matches = re.findall(pattern, text)
            preferences["interests"].extend(matches)
            
        return preferences
        
    def _update_long_memory(self, user_input, reply, emotion):
        """更新长期记忆
        
        Args:
            user_input: 用户输入
            reply: GPT回复
            emotion: 检测到的情绪
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conversation = {
            "user_input": user_input,
            "reply": reply,
            "emotion": emotion,
            "timestamp": timestamp
        }
        
        self.long_memory["conversations"].append(conversation)
        
        preferences = self._extract_preferences(user_input)
        
        for category, items in preferences.items():
            for item in items:
                if item not in self.long_memory["preferences"][category]:
                    self.long_memory["preferences"][category].append(item)
        
        self._save_long_memory()
        
    def _inject_memory_context(self):
        """注入记忆上下文到提示词中
        
        Returns:
            包含记忆上下文的提示词
        """
        if not self.long_memory["preferences"]["likes"] and not self.long_memory["preferences"]["interests"]:
            return personality_prompt
            
        memory_context = personality_prompt + "\n\n用户偏好信息："
        
        if self.long_memory["preferences"]["likes"]:
            memory_context += f"\n- 用户喜欢: {', '.join(self.long_memory['preferences']['likes'])}"
            
        if self.long_memory["preferences"]["interests"]:
            memory_context += f"\n- 用户感兴趣: {', '.join(self.long_memory['preferences']['interests'])}"
            
        return memory_context
        
    def chat(self, user_input, emotion="neutral"):
        """与 GPT 交流
        
        Args:
            user_input: 用户输入文本
            emotion: 检测到的情绪
            
        Returns:
            GPT 回复文本
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.messages[0]["role"] == "system":
            self.messages[0]["content"] = self._inject_memory_context()
        
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
            
            self._update_long_memory(user_input, reply, emotion)
            
            return reply
            
        except Exception as e:
            print(f"GPT 调用出错: {str(e)}")
            return f"抱歉，我遇到了一点小问题: {str(e)}"
