import transformers
from transformers import pipeline
import torch
from flask import Flask, request, jsonify

class ContentSummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization")

    def summarize_text(self, text, min_length=50, max_length=200):
        summary = self.summarizer(text, min_length=min_length, max_length=max_length, do_sample=False)
        return summary[0]['summary_text']

class APIManager:
    def __init__(self):
        self.app = Flask(__name__)
        self.content_summarizer = ContentSummarizer()

    def start_api(self):
        @self.app.route('/summarize', methods=['POST'])
        def summarize():
            data = request.get_json()
            text = data['text']
            min_length = data.get('min_length', 50)
            max_length = data.get('max_length', 200)
            summary = self.content_summarizer.summarize_text(text, min_length, max_length)
            return jsonify({'summary': summary})

        self.app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    api_manager = APIManager()
    api_manager.start_api()