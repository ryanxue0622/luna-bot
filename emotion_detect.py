"""
情绪检测模块
基于关键词匹配识别情绪状态
支持六种情绪类别：开心、伤心、生气、思考、困倦、害怕
"""
from typing import Dict, List, Tuple

EMOTION_KEYWORDS = {
    "happy": ["开心", "谢谢你", "真棒", "喜欢", "感谢", "棒", "好", "爱", "哈哈", "开心", "高兴", "快乐", "满意"],
    "sad": ["难过", "孤单", "伤心", "委屈", "失望", "悲伤", "哭", "想哭", "伤感", "遗憾", "心痛"],
    "angry": ["讨厌", "生气", "烦", "滚", "不开心", "烦躁", "郁闷", "恼火", "愤怒", "不爽", "厌烦"],
    "thinking": ["为什么", "这是什么", "怎么做", "请解释", "解释一下", "怎么", "如何", "是什么", "什么意思", "思考", "想知道"],
    "sleep": ["累了", "睡觉", "晚安", "想休息", "休息", "睡吧", "困了", "goodnight", "疲惫", "困倦"],
    "scared": ["害怕", "担心", "不敢", "我怕", "恐惧", "惊吓", "紧张", "忧虑", "惊慌", "恐慌", "怕"],
}

def detect_emotion(text: str) -> str:
    """从文本中检测情绪
    
    Args:
        text: 输入文本
        
    Returns:
        情绪类型: "happy", "sad", "angry", "thinking", "sleep", "scared" 或默认为 "neutral"
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
        "sad": ["sad_1.bmp", "sad_2.bmp", "sad_3.bmp"],
        "angry": ["angry_1.bmp", "angry_2.bmp", "angry_3.bmp"],
        "thinking": ["think_1.bmp", "think_2.bmp", "think_3.bmp"],
        "sleep": ["sleep_1.bmp", "sleep_2.bmp", "sleep_3.bmp"],
        "scared": ["scared_1.bmp", "scared_2.bmp", "scared_3.bmp"],
        "neutral": ["neutral_1.bmp", "neutral_2.bmp", "neutral_3.bmp"]
    }
    
    return animations.get(emotion, animations["neutral"])
