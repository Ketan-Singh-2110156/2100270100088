from flask import Flask, jsonify
from dotenv import load_dotenv
import requests
import os
import time
import threading

load_dotenv()

app = Flask(__name__)

EXTERNAL_API_URL = "https://20.244.56.144/test/numbers"
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
WINDOW_SIZE = 10
NUMBER_TYPES = {'p': 'primes', 'f': 'fibo', 'e': 'e', 'r': 'rand'}


window = []
window_lock = threading.Lock()

def fetch_numbers(number_type):
    try:
        start_time = time.time()
        headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
        response = requests.get(f"{EXTERNAL_API_URL}/{number_type}", headers=headers, timeout=0.5)
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200 and elapsed_time < 0.5:
            return response.json()
    except requests.RequestException:
        pass
    return []


