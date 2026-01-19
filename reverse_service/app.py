"""Reverse Service - Reverses the input text."""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "reverse"})


@app.route('/process', methods=['POST'])
def process():
    """Process text by reversing it."""
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text']

    if not text or text.strip() == '':
        return jsonify({"error": "Input text cannot be empty"}), 400

    result = text[::-1]
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
