import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from gtts import gTTS
import speech_recognition as sr
from transformers import pipeline

class LearningCompanion:
    def __init__(self):
        self.user_profiles = {}
        self.content_generator = pipeline("text-generation", model="gpt2")
        self.vectorizer = CountVectorizer()
        self.model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=10000, output_dim=64))
        model.add(LSTM(128))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def add_user(self, user_id, user_data):
        self.user_profiles[user_id] = user_data

    def generate_content(self, topic):
        return self.content_generator(topic, max_length=50, num_return_sequences=1)[0]['generated_text']

    def update_learning_path(self, user_id, user_interaction):
        text_data = [user_interaction]
        vectorized_data = self.vectorizer.fit_transform(text_data).toarray()
        prediction = self.model.predict(np.array([vectorized_data[0]]))
        self.user_profiles[user_id]['learning_path'].append(prediction)

    def text_to_speech(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio_data = recognizer.listen(source)
            text = recognizer.recognize_google(audio_data)
            return text

def main():
    companion = LearningCompanion()
    companion.add_user("user1", {"learning_path": []})
    content = companion.generate_content("Basics of Python programming")
    print(content)
    companion.update_learning_path("user1", "Learnt variables and data types in Python")
    print(companion.user_profiles["user1"]["learning_path"])
    companion.text_to_speech("Welcome to your personalized learning companion")
    print(companion.speech_to_text())

if __name__ == "__main__":
    main()