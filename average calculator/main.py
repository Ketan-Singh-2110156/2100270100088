from flask import Flask, jsonify
import requests
import time
import threading
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
EXTERNAL_API_URL = "https://api.example.com/numbers"
TOKEN_TYPE = os.getenv("TOKEN_TYPE", "Bearer")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WINDOW_SIZE = 10
NUMBER_TYPES = {'p': 'prime', 'f': 'fibonacci', 'e': 'even', 'r': 'random'}

window = []
window_lock = threading.Lock()

logging.basicConfig(level=logging.INFO)

def fetch_numbers(number_type):
    try:
        start_time = time.time()
        headers = {"Authorization": f"{TOKEN_TYPE} {ACCESS_TOKEN}"}
        response = requests.get(f"{EXTERNAL_API_URL}/{number_type}", headers=headers, timeout=0.5)
        elapsed_time = time.time() - start_time
        
        logging.info(f"Response status code: {response.status_code}")
        if response.status_code == 200 and elapsed_time < 0.5:
            logging.info(f"Response data: {response.json()}")
            return response.json()
        else:
            logging.error(f"Failed to fetch numbers: {response.text}")
    except requests.RequestException as e:
        logging.error(f"RequestException: {e}")
    return []

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    if number_id not in NUMBER_TYPES:
        return jsonify({"error": "Invalid number ID"}), 400

    number_type = NUMBER_TYPES[number_id]
    fetched_numbers = fetch_numbers(number_type)

    with window_lock:
        window_prev_state = list(window)
        for num in fetched_numbers:
            if num not in window:
                if len(window) >= WINDOW_SIZE:
                    window.pop(0)
                window.append(num)

        window_curr_state = list(window)
        avg = sum(window_curr_state) / len(window_curr_state) if window_curr_state else 0.0

    response = {
        "numbers": fetched_numbers,
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "avg": round(avg, 2)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
