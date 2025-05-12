"""
LCD 表情显示模块
支持在 ILI9341 LCD 屏幕上显示不同情绪的表情动画
"""
import os
import time
import threading
from typing import List
import platform
from config import TEST_MODE

ASCII_EMOTIONS = {
    "happy": """
    ◉‿◉
    """,
    "angry": """
    ಠ_ಠ
    """,
    "thinking": """
    ◔_◔
    """,
    "sleeping": """
    ⊙﹏⊙
    """,
    "neutral": """
    ◐‿◐
    """
}

class LCDDisplay:
    """LCD 显示控制类"""
    def __init__(self):
        self.current_emotion = "neutral"
        self.animation_thread = None
        self.running = False
        
    def initialize(self):
        """初始化 LCD 屏幕"""
        if TEST_MODE:
            print("【测试模式】初始化虚拟 LCD 屏幕")
            return True
            
        try:
            if platform.system() == "Linux":
                print("初始化 LCD 屏幕 (ILI9341)")
                return True
            else:
                print("非 Linux 系统，无法初始化实际 LCD 屏幕")
                return False
        except Exception as e:
            print(f"LCD 初始化失败: {e}")
            return False
    
    def display_emotion(self, emotion):
        """显示情绪表情
        
        Args:
            emotion: 情绪类型
        """
        self.current_emotion = emotion
        
        if TEST_MODE:
            print(f"【测试模式】显示表情: {emotion}")
            print(ASCII_EMOTIONS.get(emotion, ASCII_EMOTIONS["neutral"]))
            return
            
        if platform.system() != "Linux":
            print(f"非 Linux 系统，无法显示实际表情，模拟显示: {emotion}")
            return
            
        print(f"显示表情: {emotion}")
    
    def play_animation(self, animation_files: List[str], loop=True):
        """播放动画序列
        
        Args:
            animation_files: 动画文件列表
            loop: 是否循环播放
        """
        if TEST_MODE:
            print(f"【测试模式】播放动画: {animation_files}")
            return
            
        if platform.system() != "Linux":
            print(f"非 Linux 系统，无法播放实际动画，模拟播放: {animation_files}")
            return
            
        print(f"播放动画: {animation_files}")
        
    def start_animation_thread(self, emotion):
        """在后台线程中播放情绪动画
        
        Args:
            emotion: 情绪类型
        """
        from emotion_detect import get_emotion_animation
        
        self.stop_animation()
        
        animation_files = get_emotion_animation(emotion)
        
        self.running = True
        self.animation_thread = threading.Thread(
            target=self._animation_loop,
            args=(animation_files,)
        )
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
    def _animation_loop(self, animation_files):
        """动画循环
        
        Args:
            animation_files: 动画文件列表
        """
        while self.running:
            for file in animation_files:
                if not self.running:
                    break
                self.display_frame(file)
                time.sleep(0.3)  # 帧率控制
                
    def display_frame(self, frame_file):
        """显示单帧
        
        Args:
            frame_file: 帧文件名
        """
        if TEST_MODE:
            print(f"【测试模式】显示帧: {frame_file}")
            return
            
        if platform.system() != "Linux":
            print(f"非 Linux 系统，无法显示实际帧，模拟显示: {frame_file}")
            return
            
        print(f"显示帧: {frame_file}")
        
    def stop_animation(self):
        """停止当前动画"""
        if self.animation_thread and self.animation_thread.is_alive():
            self.running = False
            self.animation_thread.join(1)
