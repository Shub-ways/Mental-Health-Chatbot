# from flask import Flask, request, jsonify
# from transformers import pipeline
# from textblob import TextBlob
# import pandas as pd
# import torch
# import os
# import json
# import traceback

# # Ensure PyTorch is available
# print(torch.__version__)

# # Initialize Flask app
# app = Flask(__name__)

# # Load the JSON dataset (ensure the path is correct)
# dataset_path = 'mental_health_data.json'
# try:
#     with open(dataset_path, 'r') as f:
#         dataset = json.load(f)
#     print("Dataset loaded successfully")
# except FileNotFoundError as e:
#     print(f"Error loading dataset: {e}")
#     raise

# # Initialize the text generation pipeline
# text_generator = pipeline("text-generation", model="gpt2")

# # Initialize the sentiment analysis pipeline
# sentiment_analyzer = pipeline("sentiment-analysis")

# def generate_response(message):
#     try:
#         # Log the incoming message
#         print(f"Received message: {message}")
        
#         # Sentiment Analysis
#         analysis = TextBlob(message)
#         sentiment_response = ""
#         if analysis.sentiment.polarity < 0:
#             sentiment_response = "I'm here for you. Want to talk about what's bothering you?"
#         elif analysis.sentiment.polarity > 0:
#             sentiment_response = "That's great to hear! Tell me more."
#         else:
#             sentiment_response = "Let's chat. What's on your mind?"

#         # Use the dataset to find relevant responses
#         dataset_response = None
#         message_words = set(message.lower().split())
#         for intent in dataset['intents']:
#             for pattern in intent['patterns']:
#                 pattern_words = set(pattern.lower().split())
#                 if pattern_words & message_words:
#                     dataset_response = intent['responses'][0]  # Simple match for the first response
#                     print(f"Match found: {dataset_response}")  # Log the matched response
#                     break  # Stop at the first match
#             if dataset_response:
#                 break  # Break outer loop if a response is found

#         # Combine responses for a comprehensive reply
#         combined_response = ""
#         if dataset_response:
#             combined_response += f"{dataset_response}"
#         else:
#             combined_response += f"{sentiment_response}"

#         print(f"Combined response: {combined_response}")  # Log the final response
#         return combined_response

#     except Exception as e:
#         print(f"Error in generate_response: {e}")
#         traceback.print_exc()
#         return "Sorry, something went wrong."



# @app.route('/process', methods=['POST'])
# def process():
#     try:
#         data = request.json
#         user_message = data.get('message')
        
#         if not user_message:
#             return jsonify({'botResponse': "Please provide a message."}), 400
        
#         response = generate_response(user_message)
#         return jsonify({'botResponse': response})
#     except Exception as e:
#         print(f"Error in /process route: {e}")
#         traceback.print_exc()
#         return jsonify({'botResponse': "Sorry, something went wrong."}), 500

# if __name__ == '__main__':
#     app.run(port=5000)



from flask import Flask, request, jsonify
from transformers import pipeline
from textblob import TextBlob
import json
import traceback
import os

# Ensure PyTorch is available
import torch
print(torch.__version__)

# Initialize Flask app
app = Flask(__name__)

# Load the JSON dataset (ensure the path is correct)
dataset_path = 'mental_health_data.json'
try:
    with open(dataset_path, 'r') as f:
        dataset = json.load(f)
    print("Dataset loaded successfully")
except FileNotFoundError as e:
    print(f"Error loading dataset: {e}")
    raise

# Initialize the text generation pipeline (optional if not used)
# text_generator = pipeline("text-generation", model="gpt2")

# Initialize the sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

def generate_response(message):
    try:
        # Log the incoming message
        print(f"Received message: {message}")
        
        # Sentiment Analysis
        analysis = TextBlob(message)
        sentiment_response = ""
        if analysis.sentiment.polarity < 0:
            sentiment_response = "I'm here for you. Want to talk about what's bothering you?"
        elif analysis.sentiment.polarity > 0:
            sentiment_response = "That's great to hear! Tell me more."
        else:
            sentiment_response = "Let's chat. What's on your mind?"

        # Use the dataset to find relevant responses
        dataset_response = None
        message_words = set(message.lower().split())
        
        for intent in dataset['intents']:
            for pattern in intent['patterns']:
                pattern_words = set(pattern.lower().split())
                if pattern_words & message_words:
                    dataset_response = intent['responses'][0]  # Simple match for the first response
                    print(f"Match found: {dataset_response}")  # Log the matched response
                    break  # Stop at the first match
            if dataset_response:
                break  # Break outer loop if a response is found

        # Combine responses for a comprehensive reply
        combined_response = ""
        if dataset_response:
            combined_response += f"{dataset_response}"
        else:
            combined_response += f"{sentiment_response}"

        print(f"Combined response: {combined_response}")  # Log the final response
        return combined_response

    except Exception as e:
        print(f"Error in generate_response: {e}")
        traceback.print_exc()
        return "Sorry, something went wrong."

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log the received data
        
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({'botResponse': "Please provide a message."}), 400
        
        response = generate_response(user_message)
        return jsonify({'botResponse': response})
    
    except Exception as e:
        print(f"Error in /process route: {e}")
        traceback.print_exc()
        return jsonify({'botResponse': "Sorry, something went wrong."}), 500

if __name__ == '__main__':
    app.run(port=5000)