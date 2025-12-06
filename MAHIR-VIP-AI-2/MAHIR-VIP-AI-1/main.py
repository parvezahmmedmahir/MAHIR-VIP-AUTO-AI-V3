from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from quotex_api import api
from quotex_websocket import ws_client, start_websocket_handler
from config import MARKET_PAIRS
import random
import os

app = Flask(__name__)
CORS(app) 

# Start WebSocket History Collector
start_websocket_handler()
# Initialize API connection
api.connect()

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def status():
    ws_status = "connected" if ws_client.is_connected else "disconnected"
    return jsonify({
        "status": "online", 
        "system": "MAHIR VIP AUTO AI Backend",
        "websocket": ws_status
    })

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
    try:
        data = request.get_json(silent=True) or {}
        risk_level = data.get('risk_level', 'safe')
        result = api.get_signal(risk_level=risk_level)
        
        status_code = 200 if result["success"] else 503
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/history/<asset>', methods=['GET'])
def get_history(asset):
    """
    Returns the collected closed candle history for an asset.
    """
    # Sanitize asset name
    clean_asset = asset.replace(".csv", "").replace("/", "")
    file_path = f"data/{clean_asset}.csv"
    
    if os.path.exists(file_path):
        try:
            # Read CSV and return as JSON
            import pandas as pd
            df = pd.read_csv(file_path)
            # Limit to last 100 for performance/bandwidth
            data = df.tail(100).to_dict(orient='records')
            return jsonify({"success": True, "asset": asset, "data": data})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        return jsonify({"success": False, "error": "No history found"}), 404

if __name__ == '__main__':
    print("Starting MAHIR VIP AUTO AI Server & History Collector...")
    app.run(host='0.0.0.0', port=5000, debug=True)
