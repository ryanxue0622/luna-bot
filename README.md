# Luna Bot: 情感智能AI桌宠

Luna Bot（小Luna）是一个运行在树莓派上的AI桌面拟人机器人，具有语音交互、情绪表情和人格特质。项目使用Python开发，结合了离线语音识别、云端GPT对话和LCD表情显示功能。

## 功能特点

- **唤醒与休眠逻辑**: 支持"Hi, Luna"和"小Luna"唤醒词，自动休眠或关键词休眠
- **语音交互**: 使用Vosk进行离线中文语音识别，通过OpenAI GPT生成回复
- **情绪表情**: 在LCD屏幕上显示对应情绪的表情动画，响应用户情感需求
- **多平台支持**: 运行于树莓派5（主要平台）和macOS（测试模式）
- **易于扩展**: 模块化设计，预留摄像头、舵机和Web控制接口

## 硬件需求

- 树莓派5（16GB）
- USB麦克风
- 2.4英寸ILI9341 LCD屏幕（SPI接口）
- （可选）Logitech C270摄像头
- （可选）舵机

## 软件依赖

- Python 3.11+
- Vosk（离线语音识别）
- OpenAI API（GPT对话）
- edge-tts（语音合成）
- 其他依赖见requirements.txt

## 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/ryanxue0622/luna-bot.git
cd luna-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置OpenAI API密钥
```bash
# 创建.env文件并添加你的API密钥
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. 启动项目
```bash
python main.py  # 正常模式
python main.py --test  # 测试模式（适用于macOS）
```

## 目录结构

```
luna-bot/
├── main.py               # 主程序入口
├── voice_input.py        # 麦克风监听 + Vosk 识别
├── chat_gpt.py           # 调用 GPT 接口
├── voice_output.py       # 播报模块（edge-tts）
├── screen_display.py     # 表情显示 + 动画播放
├── emotion_detect.py     # 情绪关键词分析
├── config.py             # 所有配置项
├── memory.json           # 聊天记录本地存储
├── requirements.txt      # 项目依赖
└── README.md             # 使用说明
```

## 使用说明

1. **唤醒小Luna**:
   - 说出"Hi, Luna"或"小Luna"

2. **与小Luna对话**:
   - 唤醒后直接说话，小Luna会使用GPT回应
   - 表情会根据对话内容显示相应情绪

3. **让小Luna休眠**:
   - 说出"睡觉吧Luna"、"睡吧Luna"、"goodnight Luna"或"晚安Luna"
   - 或者保持8秒静默，小Luna会自动休眠

4. **测试模式**:
   - 使用`--test`参数启动，适用于在macOS上开发调试
   - 测试模式下通过命令行模拟语音输入和LCD显示

## 扩展功能

项目预留了以下扩展接口：

- **摄像头人脸识别**: 支持Logitech C270摄像头
- **舵机控制**: 用于头部动作
- **Web控制界面**: 从手机远程控制
- **本地模型替换**: 支持替换为本地模型（如Qwen）

## 许可证

MIT License
