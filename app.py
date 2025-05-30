from flask import Flask, request, jsonify
from flask_cors import CORS # To handle CORS issues from frontend
import requests
import json
import socket

# Import your existing functions from Sympteller_code.py
# Assuming Sympteller_code.py is in the same directory
from Sympteller_code import is_connected, query_gemini, query_ollama_mistral, detect_disease

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.get_json()
    symptoms = data.get('symptoms')

    if not symptoms:
        return jsonify({'error': 'No symptoms provided'}), 400

    try:
        diagnosis = detect_disease(symptoms)
        return jsonify({'diagnosis': diagnosis})
    except Exception as e:
        return jsonify({'error': f'An error occurred during diagnosis: {str(e)}'}), 500

if __name__ == '__main__':
    # You might want to remove API keys from here and use environment variables for production
    # These lines are just to make sure the imported functions can access them.
    # For a robust solution, pass them explicitly or set as environment variables.
    # For this example, assuming Sympteller_code.py already has them defined globally.
    app.run(debug=True, port=5000) # Run on port 5000