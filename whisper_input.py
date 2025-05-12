"""
Whisper 语音识别模块
使用 OpenAI Whisper 模型进行本地语音识别
支持中英文混合语音识别
"""
import os
import time
import queue
import tempfile
import argparse
import numpy as np
import sounddevice as sd
from config import wake_words, TEST_MODE, openai_api_key

try:
    import whisper
except ImportError:
    print("请先安装 whisper: pip install openai-whisper")
    print("如果安装失败，可能需要先安装 ffmpeg")

model = None

def load_model(model_name="base"):
    """加载 Whisper 模型
    
    Args:
        model_name: 模型名称，可选 "tiny", "base", "small", "medium", "large"
    
    Returns:
        加载的模型
    """
    global model
    if model is None:
        print(f"正在加载 Whisper {model_name} 模型...")
        model = whisper.load_model(model_name)
        print("模型加载完成")
    return model

def is_wake_word(text):
    """检查文本是否包含唤醒词
    
    Args:
        text: 输入文本
        
    Returns:
        是否包含唤醒词
    """
    for word in wake_words:
        if word.lower() in text.lower():
            return True
    return False

def listen_for_wake_word(model_name="base"):
    """监听唤醒词
    
    Args:
        model_name: Whisper 模型名称
        
    Returns:
        是否检测到唤醒词
    """
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
        
        model = load_model(model_name)
        
        fs = 16000  # 采样率
        duration = 3  # 每次录音时长（秒）
        
        while True:
            print(".", end="", flush=True)
            recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
            sd.wait()
            
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                import scipy.io.wavfile as wav
                wav.write(temp_filename, fs, recording)
            
            result = model.transcribe(temp_filename, language="zh")
            text = result["text"].strip()
            
            os.unlink(temp_filename)
            
            if text:
                print(f"\n识别到: {text}")
                if is_wake_word(text):
                    return True
                    
    except Exception as e:
        print(f"\n语音监听出错: {e}")
        print("切换到测试模式...")
        TEST_MODE = True
        return listen_for_wake_word()

def transcribe_audio(timeout=None, model_name="base"):
    """录音并转换为文字
    
    Args:
        timeout: 最大录音时间（秒），None 表示无限制
        model_name: Whisper 模型名称
        
    Returns:
        str: 识别出的文本
    """
    global TEST_MODE
    
    if TEST_MODE:
        print("【测试模式】请输入模拟语音内容: ")
        return input("> ")
    
    try:
        print("请开始说话...")
        
        model = load_model(model_name)
        
        fs = 16000  # 采样率
        max_duration = 10  # 最大录音时长（秒）
        
        start_time = time.time()
        recording = sd.rec(int(max_duration * fs), samplerate=fs, channels=1)
        
        print("正在录音...", end="", flush=True)
        silence_threshold = 0.01
        silence_duration = 0
        last_audio_time = time.time()
        
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            if timeout and elapsed > timeout:
                sd.stop()
                print("\n录音超时")
                return ""
                
            if elapsed >= max_duration:
                break
                
            current_position = int(elapsed * fs)
            if current_position < len(recording):
                current_volume = np.abs(recording[current_position-100:current_position]).mean() if current_position > 100 else 0
                
                if current_volume > silence_threshold:
                    silence_duration = 0
                    last_audio_time = current_time
                    print(".", end="", flush=True)
                else:
                    silence_duration = current_time - last_audio_time
                    
                if silence_duration > 1.5 and elapsed > 1:  # 确保至少录了1秒
                    break
                    
            time.sleep(0.1)
            
        sd.stop()
        print("\n录音结束，正在识别...")
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_filename = temp_file.name
            import scipy.io.wavfile as wav
            wav.write(temp_filename, fs, recording)
        
        result = model.transcribe(temp_filename, language="zh")
        text = result["text"].strip()
        
        os.unlink(temp_filename)
        
        print(f"识别结果: {text}")
        return text
        
    except Exception as e:
        print(f"语音识别出错: {e}")
        print("切换到测试模式...")
        TEST_MODE = True
        return transcribe_audio(timeout)

def main():
    """测试入口"""
    parser = argparse.ArgumentParser(description="Whisper 语音识别测试")
    parser.add_argument("--test", action="store_true", help="启用测试模式")
    parser.add_argument("--model", default="base", help="Whisper 模型名称 (tiny, base, small, medium, large)")
    args = parser.parse_args()
    
    if args.test:
        global TEST_MODE
        TEST_MODE = True
        print("已启动测试模式，将模拟语音输入")
    
    try:
        while True:
            print("\n===== Whisper 语音识别测试 =====")
            text = transcribe_audio(model_name=args.model)
            print(f"识别结果: {text}")
            
            if text.lower() in ["退出", "exit", "quit"]:
                break
                
    except KeyboardInterrupt:
        print("\n用户手动退出。")

if __name__ == "__main__":
    main()
