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

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def signal():
    try:
        result = api.get_signal()
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 503
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
