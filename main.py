"""
Luna Bot 主程序
实现唤醒/休眠逻辑、语音交互和情绪表情反馈
"""
import os
import time
import argparse
import platform
from config import sleep_keywords, silence_timeout, TEST_MODE
from whisper_input import listen_for_wake_word, transcribe_audio, is_wake_word
from voice_output import speak_text, say_awake, say_sleep
from chat_gpt import ChatGPT
from emotion_detect import detect_emotion
from screen_display import LCDDisplay

def is_sleep_keyword(text):
    """检查是否包含休眠关键词
    
    Args:
        text: 输入文本
        
    Returns:
        是否包含休眠关键词
    """
    text = text.lower()
    for keyword in sleep_keywords:
        if keyword.lower() in text:
            return True
    return False

def main():
    """主程序入口"""
    parser = argparse.ArgumentParser(description="Luna Bot - AI桌宠")
    parser.add_argument("--test", action="store_true", help="启用测试模式")
    args = parser.parse_args()
    
    if args.test:
        global TEST_MODE
        import config
        config.TEST_MODE = True
        print("已启动测试模式，将模拟硬件操作")
    
    print("正在初始化小Luna...")
    gpt = ChatGPT()
    lcd = LCDDisplay()
    lcd.initialize()
    lcd.display_emotion("neutral")
    
    print("小Luna已准备就绪！按 Ctrl+C 退出。")
    
    try:
        while True:
            print("\n===== 监听唤醒模式 =====")
            if listen_for_wake_word():
                say_awake()
                lcd.display_emotion("happy")
                
                active = True
                last_activity_time = time.time()
                
                while active:
                    user_input = transcribe_audio()
                    
                    if not user_input:
                        if time.time() - last_activity_time > silence_timeout:
                            print(f"静默超过 {silence_timeout} 秒，自动休眠")
                            say_sleep()
                            lcd.display_emotion("sleeping")
                            active = False
                        continue
                    
                    last_activity_time = time.time()
                    
                    if is_sleep_keyword(user_input):
                        print("检测到休眠关键词")
                        say_sleep()
                        lcd.display_emotion("sleeping")
                        active = False
                        continue
                    
                    reply = gpt.chat(user_input)
                    
                    user_emotion = detect_emotion(user_input)
                    bot_emotion = detect_emotion(reply)
                    
                    if user_emotion != "neutral":
                        lcd.display_emotion(user_emotion)
                    else:
                        lcd.display_emotion(bot_emotion)
                    
                    speak_text(reply)
                    
                    last_activity_time = time.time()
                
    except KeyboardInterrupt:
        print("\n用户手动退出。")
    finally:
        lcd.stop_animation()
        print("小Luna已关闭。")

if __name__ == "__main__":
    main()
