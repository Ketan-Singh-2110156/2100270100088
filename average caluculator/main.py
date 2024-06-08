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
