import json
import random
import requests
import os

from flask import Flask, request

# Create a Flask instance
app = Flask(__name__)

# Constants
GROUPME_BOT_POST_URL = "https://api.groupme.com/v3/bots/post"
CONCH_RESPONSES = [
    "Maybe someday.", "Nothing.", "Neither.", "I don't think so.",
    "Yes.", "No.", "Try asking again."
]
BOT_NAME = os.getenv("GROUPME_BOT_NAME")
BOT_ID = os.getenv("GROUPME_BOT_ID")

# Use the "/" route to handle POST requests from GroupMe
@app.route("/", methods = ["GET", "POST"])
def process_request():
    """Processes a GroupMe message and returns a reply if applicable."""
    if request.method  == 'POST':

        data = request.get_json()

        # Don't respond this bot's message
        if data["name"] == BOT_NAME:
            return "Bot message received", 200

        msg = data["text"]
        base_msg_id = data["id"]
        # Only start if the message begins with "/magicconch"
        if msg.startswith("/magicconch"):
            conch_response = generate_random_response()

            return send_groupme_bot_message_reply(
                BOT_ID, conch_response, base_msg_id)
        return "This should not execute.", 200
    else:
        return "All hail the Magic Conch!", 200

def generate_random_response():
    """Returns a random string response from the Magic Conch."""
    return random.choice(CONCH_RESPONSES)

def send_groupme_bot_message(bot_id, message, attachments = []):
    """Constructs and sends a POST request to the GroupMe bots API.

    Args:
        bot_id (str): GroupMe bot ID.
        message (str): Message string.
        attachments (List[obj], optional): List of message attachments. Defaults
            to an empty list.
    """

    # Construct message payload
    data = {
        "bot_id"            : bot_id,
        "text"              : message,
        "attachments"       : attachments,
    }

    # Send POST request
    with requests.post(GROUPME_BOT_POST_URL, json = data) as response:
        return str(response.headers), 200

def send_groupme_bot_message_reply(bot_id, message, base_msg_id):
    """Constructs and sends reply message to the GroupMe bots API.

    Args:
        bot_id (str): GroupMe bot ID.
        message (str): Message string.
        base_msg_id (str): ID of the original request message.
    """
    attachments = [
        {
            "type"          : "reply",
            "base_reply_id" : str(base_msg_id),
        }
    ]
    return send_groupme_bot_message(bot_id, message, attachments)

if __name__ == "__main__":
    app.run(debug = True)