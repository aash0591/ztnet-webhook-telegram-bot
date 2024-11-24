import os
import requests
import logging
from flask import Flask, request
from waitress import serve

app = Flask(__name__)

# Load the Telegram Bot token and Chat ID from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_IDS = os.getenv('TELEGRAM_CHAT_IDS').split(',')

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')  # Omit logger name
logging.getLogger("urllib3").setLevel(logging.WARNING)  # Suppress urllib3 debug logs
logger = logging.getLogger(__name__)

# Define your webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received webhook data:", data)

    # Try to build the message dynamically with checks
    message = f"Webhook Event Notification:\n\nEvent Type: {data.get('hookType', 'N/A')}\n"
    message += f"User Email: {data.get('userEmail', 'N/A')}\n"
    message += f"Network ID: {data.get('networkId', 'N/A')}\n"
    message += f"User ID: {data.get('userId', 'N/A')}\n"
    message += f"Organization ID: {data.get('organizationId', 'N/A')}\n"

    # Include additional fields dynamically
    additional_fields = [key for key in data.keys() if key not in ['hookType', 'userEmail', 'networkId', 'userId', 'organizationId']]
    if additional_fields:
        message += "\nAdditional Data:\n"
        for field in additional_fields:
            message += f"{field}: {data.get(field, 'N/A')}\n"

    # Send the message to Telegram chat(s)
    for chat_id in TELEGRAM_CHAT_IDS:
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(telegram_url, data=payload)
        print("Telegram response:", response.json())

        # Log the raw request body
        raw_data = request.data.decode('utf-8')  # Get raw body data as a string
        logger.debug("Raw Request Body: %s", raw_data)

        # Log Telegram user information if the response is successful
        response_data = response.json()
        if response_data.get('ok') and 'result' in response_data:
            chat_info = response_data['result'].get('chat', {})
            chat_id = chat_info.get("id")
            first_name = chat_info.get("first_name")
            last_name = chat_info.get("last_name")
            username = chat_info.get("username")
            chat_type = chat_info.get("type")

            # Log formatted Telegram user info
            logger.debug(
                "Telegram User Info: ID: %s, Name: %s  %s, Username: %s, Type: %s",
                chat_id,
                first_name,
                last_name if last_name else "",
                username,
                chat_type,
            )

        # Log separator for clarity
        logger.debug("=" * 50)

    return 'OK', 200


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)  # Use Waitress as the WSGI server
