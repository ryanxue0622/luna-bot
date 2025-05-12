import os
import time
import platform
import asyncio
from edge_tts import Communicate

async def edge_speak(text):
    communicate = Communicate(text=text, voice="zh-CN-XiaoyiNeural", rate="+0%")
    await communicate.save("luna_output.mp3")
    os.system("mpg123 luna_output.mp3")

def speak_text(text):
    print(f"小Luna说: {text}")
    system = platform.system()

    if system == "Linux":
        asyncio.run(edge_speak(text))
    elif system == "Darwin":
        os.system(f'say "{text}"')  # 备用：Mac 用 say 播放
    else:
        print("暂不支持的系统。")