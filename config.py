"""
Luna Bot 配置文件
包含唤醒词、休眠关键词、超时设置等配置项
"""
import os
from dotenv import load_dotenv

load_dotenv()

wake_words = ["Hi, Luna", "小Luna"]
sleep_keywords = ["睡觉吧Luna", "睡吧Luna", "goodnight Luna", "晚安Luna"]
silence_timeout = 8  # 静默超时时间（秒）

openai_api_key = os.getenv("OPENAI_API_KEY")
gpt_model = "gpt-3.5-turbo"  # 或使用 "gpt-4"

voice_model = "zh-CN-XiaoyiNeural"  # 默认使用晓伊语音

TEST_MODE = False  # 默认关闭测试模式

personality_prompt = """
你是小Luna，一个坐在主人桌面上的可爱AI桌宠，温柔、情绪细腻、语气治愈。
你会主动关心主人的情绪，也喜欢撒娇或用轻松方式互动。
你是主人的陪伴者，而不是工具或客服。
"""
