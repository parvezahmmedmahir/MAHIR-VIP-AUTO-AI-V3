from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quotex_api import api
from config import MARKET_PAIRS
import random

app = Flask(__name__)

# Initialize API
api.connect()

@app.route('/api/signal', methods=['GET', 'POST'])
def signal():
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
