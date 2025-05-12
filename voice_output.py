import os
import time
import platform
import asyncio
from edge_tts import Communicate
from config import voice_model, TEST_MODE

async def edge_speak(text, voice=voice_model, rate="+0%"):
    """使用 edge-tts 播放语音
    
    Args:
        text: 要播放的文本
        voice: 语音模型
        rate: 语速调整
    """
    communicate = Communicate(text=text, voice=voice, rate=rate)
    await communicate.save("luna_output.mp3")
    os.system("mpg123 luna_output.mp3")

def speak_text(text):
    """跨平台文本转语音
    
    Args:
        text: 要播放的文本
    """
    if TEST_MODE:
        print(f"【测试模式】小Luna说: {text}")
        return
        
    print(f"小Luna说: {text}")
    system = platform.system()

    if system == "Linux":
        asyncio.run(edge_speak(text))
    elif system == "Darwin":  # macOS
        os.system(f'say "{text}"')  # Mac 用 say 播放
    else:
        print("暂不支持的系统，只显示文本。")
        
def say_awake():
    """播放唤醒回应"""
    speak_text("我在呢~")
    
def say_sleep():
    """播放休眠提示"""
    speak_text("我先休息一下，有需要再叫我哦~")
