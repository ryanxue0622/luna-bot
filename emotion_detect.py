"""
情绪检测模块
基于关键词匹配识别情绪状态
"""
from typing import Dict, List, Tuple

EMOTION_KEYWORDS = {
    "happy": ["谢谢你", "开心", "你好棒", "感谢", "棒", "好", "喜欢", "爱", "哈哈"],
    "angry": ["烦", "不开心", "讨厌", "生气", "难过", "失望", "烦躁", "郁闷"],
    "thinking": ["为什么", "请解释", "解释一下", "怎么", "如何", "是什么", "什么意思"],
    "sleeping": ["晚安", "休息", "睡觉", "睡吧", "累了", "困了", "goodnight"],
}

def detect_emotion(text: str) -> str:
    """从文本中检测情绪
    
    Args:
        text: 输入文本
        
    Returns:
        情绪类型: "happy", "angry", "thinking", "sleeping" 或默认为 "neutral"
    """
    text = text.lower()
    
    emotion_scores = {}
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        emotion_scores[emotion] = score
    
    max_score = 0
    detected_emotion = "neutral"
    for emotion, score in emotion_scores.items():
        if score > max_score:
            max_score = score
            detected_emotion = emotion
    
    return detected_emotion

def get_emotion_animation(emotion: str) -> List[str]:
    """获取对应情绪的动画文件列表
    
    Args:
        emotion: 情绪类型
        
    Returns:
        动画文件名列表
    """
    animations = {
        "happy": ["smile_1.bmp", "smile_2.bmp", "smile_3.bmp"],
        "angry": ["angry_1.bmp", "angry_2.bmp", "angry_3.bmp"],
        "thinking": ["think_1.bmp", "think_2.bmp", "think_3.bmp"],
        "sleeping": ["sleep_1.bmp", "sleep_2.bmp", "sleep_3.bmp"],
        "neutral": ["neutral_1.bmp", "neutral_2.bmp", "neutral_3.bmp"]
    }
    
    return animations.get(emotion, animations["neutral"])
