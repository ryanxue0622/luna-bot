import json
import os
from openai import OpenAI
from voice_input import transcribe_audio
from voice_output import speak_text

# 初始化 OpenAI 客户端（用你的 API 密钥）
client = OpenAI(api_key="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")

# 载入历史对话作为“记忆”
if os.path.exists("memory.json"):
    with open("memory.json", "r") as f:
        messages = json.load(f)
else:
    messages = [
        {
            "role": "system",
            "content": "你是小Luna，一个可爱温柔、情商极高的陪伴型AI助手。你擅长提供情绪支持、鼓励和温暖的话语。你的语气总是轻柔、善解人意，并愿意倾听和安慰用户。"
        }
    ]

print("小Luna准备好了，按 Ctrl+C 退出。")

try:
    while True:
        user_input = transcribe_audio()  # 录音转文字
        if not user_input:
            continue

        if user_input.lower() in ["退出", "exit", "quit"]:
            print("再见！Luna会想你的。")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # 使用新版本接口
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})

            print("Luna:", reply)
            speak_text(reply)

            # 保存记忆
            with open("memory.json", "w") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print("Luna 遇到了一点小问题：", str(e))

except KeyboardInterrupt:
    print("\n用户手动退出。记忆已保存。")