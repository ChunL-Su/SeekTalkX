from flask import Flask, request, jsonify, render_template
# from openai import OpenAI
from helper import DeepSeeker, OpenAI
import speech_recognition as sr
import pyttsx3
import threading
import os
import tempfile


client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

#初始化flask
app = Flask(__name__)

# 初始化DeepSeek
deepseek = DeepSeeker(client)
# 初始化语音引擎
engine = pyttsx3.init()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask_question():
    # 处理文本问题
    if 'text' in request.form:
        question = request.form['text']
        response = deepseek.ask(question)
        return jsonify({"text": response})
    else:
        return jsonify({"text": "No text entered"})


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': '未提供音频文件'}), 400

    audio_file = request.files['audio']

    # 保存临时文件
    audio_path = "./tmp_files/temp_audio.wav"

    # This is the real temp file.测试时临时不自动删除
    # with tempfile.NamedTemporaryFile(delete=True, dir="./tmp_files/") as audio_file:
    #     pass
    audio_file.save(audio_path)
    return jsonify({'audio_path': audio_path})

    # 语音转文本
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        try:
            question = r.recognize_google(audio_data, language='zh-CN')
        except Exception as e:
            return jsonify({"error": str(e)})

    # 获取DeepSeek回答
    response = deepseek.ask(question)

    # 文本转语音
    def speak():
        engine.say(response)
        engine.runAndWait()

    # 在新线程中播放语音，避免阻塞请求
    threading.Thread(target=speak).start()

    return jsonify({
        "text": response,
        "question": question
    })


if __name__ == '__main__':
    app.run(debug=True)
