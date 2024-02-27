
# Project Name: AI-Powered Personalized Learning & Therapy Avatar (PLTA)
# Description: This project aims to create a digital avatar that leverages neural networks for providing personalized educational and therapeutic support. It combines the capabilities of a tutor, therapist, and friend into a single accessible digital entity, utilizing emotional intelligence and real-time adaptation to user needs.

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from transformers import pipeline, GPT2Tokenizer, TFGPT2Model

# Load environment variables
load_dotenv()
PORT = os.getenv("PORT", 5000)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt2")

app = Flask(__name__)

class PLTAAvatar:
    """A class for the Personalized Learning & Therapy Avatar."""
    
    def __init__(self, model_name=MODEL_NAME):
        """Initializes the avatar with necessary models and configurations."""
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = TFGPT2Model.from_pretrained(model_name)
        self.emotion_pipeline = pipeline('sentiment-analysis')
    
    def analyze_emotion(self, text):
        """Analyzes the emotional content of the text."""
        return self.emotion_pipeline(text)
    
    def generate_response(self, input_text):
        """Generates a personalized response based on user input."""
        inputs = self.tokenizer.encode(input_text, return_tensors='tf')
        reply_ids = self.model.generate(inputs)
        return self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)

@app.route('/interact', methods=['POST'])
def interact_with_avatar():
    """API endpoint for interacting with the PLTA avatar."""
    data = request.json
    user_input = data.get('input')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        response = avatar.generate_response(user_input)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    avatar = PLTAAvatar()
    app.run(debug=False, port=PORT)

# Project Name: AI-Powered Personalized Learning & Therapy Avatar (PLTA)
# Description: This project aims to create a digital avatar that leverages neural networks for providing personalized educational and therapeutic support. It combines the capabilities of a tutor, therapist, and friend into a single accessible digital entity, utilizing emotional intelligence and real-time adaptation to user needs.

from flask import Flask, request, jsonify
from transformers import pipeline, GPT2Tokenizer, TFGPT2Model
import os

app = Flask(__name__)

class PLTAAvatar:
    """A class for the Personalized Learning & Therapy Avatar."""
    
    def __init__(self):
        """Initializes the avatar with necessary models and configurations."""
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = TFGPT2Model.from_pretrained('gpt2')
        self.emotion_pipeline = pipeline('sentiment-analysis')
    
    def analyze_emotion(self, text):
        """Analyzes the emotional content of the text."""
        try:
            analysis_result = self.emotion_pipeline(text)
            return analysis_result
        except Exception as e:
            return f"Error analyzing emotion: {str(e)}"
    
    def generate_response(self, input_text):
        """Generates a personalized response based on user input."""
        try:
            inputs = self.tokenizer.encode(input_text, return_tensors='tf')
            reply_ids = self.model.generate(inputs)
            response = self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"

@app.route('/interact', methods=['POST'])
def interact_with_avatar():
    """API endpoint for interacting with the PLTA avatar."""
    data = request.json
    user_input = data.get('input')
    
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    try:
        response = avatar.generate_response(user_input)
        emotion_analysis = avatar.analyze_emotion(user_input)
        return jsonify({'response': response, 'emotion': emotion_analysis})
    except Exception as e:
        return jsonify({'error': f"Failed to interact with the avatar: {str(e)}"}), 500

if __name__ == '__main__':
    avatar = PLTAAvatar()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port)

# Project Name: AI-Powered Personalized Learning & Therapy Avatar (PLTA)
# Description: This project aims to create a digital avatar that leverages neural networks for providing personalized educational and therapeutic support. It combines the capabilities of a tutor, therapist, and friend into a single accessible digital entity, utilizing emotional intelligence and real-time adaptation to user needs.

import os
from flask import Flask, request, jsonify
from transformers import pipeline, GPT2Tokenizer, TFGPT2Model

app = Flask(__name__)

class PLTAAvatar:
    """A class for the Personalized Learning & Therapy Avatar."""
    
    def __init__(self):
        """Initializes the avatar with necessary models and configurations."""
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = TFGPT2Model.from_pretrained('gpt2')
        self.emotion_pipeline = pipeline('sentiment-analysis')
    
    def analyze_emotion(self, text):
        """Analyzes the emotional content of the text."""
        return self.emotion_pipeline(text)
    
    def generate_response(self, input_text):
        """Generates a personalized response based on user input."""
        inputs = self.tokenizer.encode(input_text, return_tensors='tf')
        reply_ids = self.model.generate(inputs)
        return self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)

def create_app(avatar):
    """Creates and configures the Flask application."""
    
    @app.route('/interact', methods=['POST'])
    def interact_with_avatar():
        """API endpoint for interacting with the PLTA avatar."""
        data = request.json
        user_input = data.get('input')
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        try:
            response = avatar.generate_response(user_input)
            return jsonify({'response': response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app

if __name__ == '__main__':
    avatar = PLTAAvatar()
    app = create_app(avatar)
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
