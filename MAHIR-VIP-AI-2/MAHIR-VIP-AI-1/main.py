from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from quotex_api import api
from config import MARKET_PAIRS
import random
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Initialize API connection for serverless
api.connect()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def status():
    return jsonify({"status": "online", "system": "MAHIR VIP AUTO AI Backend"})

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return jsonify({"error": "File not found"}), 404

@app.route('/api/assets', methods=['GET'])
def get_assets():
    return jsonify({"assets": MARKET_PAIRS})

@app.route('/api/signal', methods=['POST', 'GET'])
def generate_signal():
    """
    Generates a signal for a random asset, retrying until a valid CALL/PUT is found.
    """
    try:
        # Get Risk Level from Request
        data = request.get_json(silent=True) or {}
        risk_level = data.get('risk_level', 'safe')

        # Try up to 10 different assets to find a valid signal
        max_attempts = 10
        for attempt in range(max_attempts):
            asset = random.choice(MARKET_PAIRS)
            analysis = api.analyze_market(asset, risk_level=risk_level)
            
            # If we got a valid signal (not WAIT), return it
            if analysis["signal"] in ["CALL", "PUT"]:
                response = {
                    "success": True,
                    "data": {
                        "pair": analysis["asset"],
                        "direction": analysis["signal"],
                        "expiry": "1 MINUTE",
                        "confidence": f"{analysis['confidence']}%",
                        "strategy": analysis["strategy"],
                        "timestamp": analysis["timestamp"]
                    }
                }
                return jsonify(response)
        
        # If no valid signal found after all attempts, return error
        return jsonify({
            "success": False, 
            "error": "No strong signals available at this moment. Please try again."
        }), 503
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



if __name__ == '__main__':
    print("Starting MAHIR VIP AUTO AI Server...")
    print("Initializing API connection...")
    app.run(host='0.0.0.0', port=5000, debug=True)
