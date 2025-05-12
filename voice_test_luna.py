import asyncio
import os
from edge_tts import Communicate

# 中文女声列表
voices = {
    "晓伊": "zh-CN-XiaoyiNeural"
}

# 语气风格
styles = [
    ("cheerful", "开心的语气"),
    ("friendly", "友善自然"),
    ("affectionate", "柔情似水"),
    ("sad", "伤感情绪"),
    ("embarrassed", "害羞软萌"),
    ("angry", "情绪丰富"),
    ("chat", "日常闲聊")
]

# 要朗读的文本
test_text = "早安呀，今天的你也很棒呢～记得吃早餐哦。"

# 主程序
async def test_all():
    for name, voice_id in voices.items():
        for style_key, style_desc in styles:
            print(f"\n正在播放：{name} - {style_desc}")
            try:
                ssml_text = f"""
<speak version='1.0' xml:lang='zh-CN'>
  <voice name='{voice_id}'>
    <express-as style='{style_key}'>
      {test_text}
    </express-as>
  </voice>
</speak>
"""

                communicate = Communicate(
                    text=ssml_text,
                    voice=voice_id
                )

                filename = f"test_{name}_{style_key}.mp3"
                await communicate.save(filename)

                os.system(f"mpg123 {filename}")  # macOS 改成 afplay
            except Exception as e:
                print(f"跳过 {name} - {style_desc}，因为出错: {e}")

# 执行
if __name__ == "__main__":
    asyncio.run(test_all())