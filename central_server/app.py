"""Central Server - Routes requests to appropriate text processing services."""
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Service registry - easily extensible for new services
SERVICES = {
    'uppercase': {
        'url': 'http://uppercase_service:5000/process',
        'description': 'Convert text to UPPERCASE'
    },
    'lowercase': {
        'url': 'http://lowercase_service:5000/process',
        'description': 'Convert text to lowercase'
    },
    'reverse': {
        'url': 'http://reverse_service:5000/process',
        'description': 'Reverse text'
    },
    'wordcount': {
        'url': 'http://wordcount_service:5000/process',
        'description': 'Count number of words'
    }
}


def log_request(operation, text, result, status):
    """Log request details."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'operation': operation,
        'text_length': len(text) if text else 0,
        'status': status,
        'result_preview': str(result)[:50] if result else None
    }
    logger.info(f"Request: {log_entry}")


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "central_server"})


@app.route('/services', methods=['GET'])
def list_services():
    """List all available services."""
    services_list = {key: val['description'] for key, val in SERVICES.items()}
    return jsonify({"services": services_list})


@app.route('/process', methods=['POST'])
def process():
    """Route processing requests to appropriate service."""
    data = request.get_json()

    # Validate request
    if not data:
        log_request(None, None, "No data provided", "error")
        return jsonify({"error": "No data provided"}), 400

    operation = data.get('operation')
    text = data.get('text')

    # Validate operation
    if not operation:
        log_request(None, text, "No operation specified", "error")
        return jsonify({"error": "No operation specified"}), 400

    if operation not in SERVICES:
        log_request(operation, text, "Invalid operation", "error")
        return jsonify({
            "error": f"Invalid operation: {operation}",
            "available_operations": list(SERVICES.keys())
        }), 400

    # Validate text
    if not text or text.strip() == '':
        log_request(operation, text, "Empty input", "error")
        return jsonify({"error": "Input text cannot be empty"}), 400

    # Forward request to appropriate service
    service_url = SERVICES[operation]['url']
    try:
        response = requests.post(
            service_url,
            json={"text": text},
            timeout=10
        )
        response_data = response.json()

        if response.status_code == 200:
            log_request(operation, text, response_data.get('result'), "success")
            return jsonify(response_data)
        else:
            log_request(operation, text, response_data.get('error'), "error")
            return jsonify(response_data), response.status_code

    except requests.exceptions.ConnectionError:
        error_msg = f"Service '{operation}' is unavailable"
        log_request(operation, text, error_msg, "error")
        return jsonify({"error": error_msg}), 503

    except requests.exceptions.Timeout:
        error_msg = f"Service '{operation}' timed out"
        log_request(operation, text, error_msg, "error")
        return jsonify({"error": error_msg}), 504

    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        log_request(operation, text, error_msg, "error")
        return jsonify({"error": error_msg}), 500


if __name__ == '__main__':
    # Create logs directory
    import os
    os.makedirs('/app/logs', exist_ok=True)

    app.run(host='0.0.0.0', port=5000)
