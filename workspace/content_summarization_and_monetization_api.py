import flask
import os
import requests
from transformers import pipeline
from functools import lru_cache

app = flask.Flask(__name__)

class BaseEngine:
    def __init__(self):
        pass

class ContentSummarizer(BaseEngine):
    def __init__(self):
        super().__init__()
        self.summarizer = pipeline("summarization")

    @lru_cache(maxsize=100)
    def summarize(self, content, min_length=50, max_length=200):
        try:
            summary = self.summarizer(content, min_length=min_length, max_length=max_length, do_sample=False)[0]['summary_text']
            return summary
        except Exception as e:
            return f"Error in summarization: {str(e)}"

class MonetizationEngine(BaseEngine):
    def __init__(self, ad_database_url):
        super().__init__()
        self.ad_database_url = ad_database_url

    def fetch_advertisement(self, category="general"):
        try:
            ads = requests.get(f"{self.ad_database_url}/ads?category={category}").json()
            if ads:
                # Future improvement: Implement a more sophisticated selection algorithm
                return ads[0]  # Assuming the API returns a list of ads
            return "No ads available"
        except requests.exceptions.RequestException as e:
            return f"Error fetching ads: {str(e)}"

@app.route('/summarize', methods=['POST'])
def api_summarize():
    data = flask.request.json
    content = data.get('content')
    if not content:
        return flask.jsonify({"error": "No content provided"}), 400

    summarizer = ContentSummarizer()
    summary = summarizer.summarize(content)
    return flask.jsonify({"summary": summary})

@app.route('/monetize', methods=['GET'])
def api_monetize():
    category = flask.request.args.get('category', 'general')
    ad_database_url = os.getenv("AD_DATABASE_URL", "http://example.com")
    monetization_engine = MonetizationEngine(ad_database_url)
    ad = monetization_engine.fetch_advertisement(category)
    return flask.jsonify({"ad": ad})

if __name__ == '__main__':
    app.run(debug=False)