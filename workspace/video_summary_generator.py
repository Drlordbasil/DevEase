import tensorflow as tf
import cv2
import numpy as np
from transformers import pipeline
from gtts import gTTS
from speech_recognition import Recognizer, AudioFile
import os

class VideoSummaryGenerator:
    def __init__(self, user_preferences):
        self.user_preferences = user_preferences
        self.nlp = pipeline("summarization")
        self.speech_recognizer = Recognizer()

    def extract_audio(self, video_path):
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frames = []
        success, frame = video.read()
        while success:
            frames.append(frame)
            success, frame = video.read()
        video.release()
        audio_path = video_path.split('.')[0] + '.wav'
        os.system(f"ffmpeg -i {video_path} -ab 160k -ac 2 -ar 44100 -vn {audio_path}")
        return audio_path, fps, frames

    def transcribe_audio(self, audio_path):
        with AudioFile(audio_path) as source:
            audio_data = self.speech_recognizer.record(source)
        text = self.speech_recognizer.recognize_google(audio_data)
        return text

    def summarize_text(self, text):
        summary = self.nlp(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def generate_summary(self, video_path):
        audio_path, fps, frames = self.extract_audio(video_path)
        transcript = self.transcribe_audio(audio_path)
        summary = self.summarize_text(transcript)
        return summary

    def text_to_speech(self, text, language='en'):
        tts = gTTS(text=text, lang=language, slow=False)
        audio_path = "summary_audio.mp3"
        tts.save(audio_path)
        return audio_path

class UserPreferences:
    def __init__(self, interests, viewing_habits):
        self.interests = interests
        self.viewing_habits = viewing_habits

def main():
    user_preferences = UserPreferences(interests=["technology", "science"], viewing_habits=["evening", "weekends"])
    video_summary_generator = VideoSummaryGenerator(user_preferences)
    video_path = "input_video.mp4"
    summary = video_summary_generator.generate_summary(video_path)
    print(summary)
    audio_summary_path = video_summary_generator.text_to_speech(summary)
    print(f"Audio summary saved at: {audio_summary_path}")

if __name__ == "__main__":
    main()