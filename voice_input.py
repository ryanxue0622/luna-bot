import queue
import json
import numpy as np
import time
from config import wake_words, TEST_MODE

if not TEST_MODE:
    try:
        import sounddevice as sd
        import vosk
        # 初始化模型（需要提前下载 vosk 模型）
        model = vosk.Model("vosk-model-small-cn-0.22")  # 中文模型
        q = queue.Queue()
    except Exception as e:
        print(f"警告: 语音识别初始化失败: {e}")
        print("将在测试模式下运行")
        TEST_MODE = True

def callback(indata, frames, time, status):
    """回调函数：将音频数据放入队列"""
    if status:
        print(status)
    q.put(bytes(indata))

def is_wake_word(text):
    """检查文本是否包含唤醒词"""
    for word in wake_words:
        if word.lower() in text.lower():
            return True
    return False

def listen_for_wake_word():
    """监听唤醒词"""
    global TEST_MODE
    
    if TEST_MODE:
        print("【测试模式】监听唤醒词中...")
        user_input = input("模拟语音输入 (输入唤醒词唤醒): ")
        if is_wake_word(user_input):
            print("【测试模式】检测到唤醒词！")
            return True
        return False
    
    try:
        print("监听唤醒词中（'Hi, Luna' 或 '小Luna'）...")
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', 
                            channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, 16000)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"识别到: {text}")
                        if is_wake_word(text):
                            return True
    except Exception as e:
        print(f"语音监听出错: {e}")
        print("切换到测试模式...")
        TEST_MODE = True
        return listen_for_wake_word()
            
def transcribe_audio(timeout=None):
    """录音并转换为文字
    
    Args:
        timeout: 最大录音时间（秒），None 表示无限制
        
    Returns:
        str: 识别出的文本
    """
    global TEST_MODE
    
    if TEST_MODE:
        print("【测试模式】请输入模拟语音内容: ")
        return input("> ")
    
    try:    
        print("请开始说话...")
        start_time = time.time()
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                            channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, 16000)
            while True:
                if timeout and (time.time() - start_time) > timeout:
                    return ""
                    
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    return result.get("text", "")
    except Exception as e:
        print(f"语音识别出错: {e}")
        print("切换到测试模式...")
        TEST_MODE = True
        return transcribe_audio(timeout)
