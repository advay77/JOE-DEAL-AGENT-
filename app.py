from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import os
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)
CORS(app)

# Voice recognition function
recognizer = sr.Recognizer()
def recognize_speech_from_audio(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return f"Speech recognition error: {e}"

# Text-to-speech function
engine = pyttsx3.init()
def text_to_speech(text, filename="response.wav"):
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded."}), 400
        audio_file = request.files['audio']
        audio_path = "temp_input.wav"
        audio_file.save(audio_path)
        recognized_text = recognize_speech_from_audio(audio_path)
        # Here you can add logic to generate a response (e.g., with an LLM or rules)
        response_text = f"You said: {recognized_text}"
        tts_path = text_to_speech(response_text)
        return send_file(tts_path, mimetype="audio/wav")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
