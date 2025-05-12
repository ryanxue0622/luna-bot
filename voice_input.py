import sounddevice as sd
import vosk
import queue
import json

# 初始化模型（需要提前下载 vosk 模型）
model = model = vosk.Model("vosk-model-small-cn-0.22")  # 中文模型

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def transcribe_audio():
    print("请开始说话（Ctrl+C 停止）...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")