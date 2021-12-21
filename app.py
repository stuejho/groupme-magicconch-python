import json
import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

# Create a Flask instance
app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def process_request():
    if request.method  == 'POST':
        return "Message sent", 200
    else:
        return "All hail the Magic Conch!", 200

if __name__ == "__main__":
    app.run(debug = True)