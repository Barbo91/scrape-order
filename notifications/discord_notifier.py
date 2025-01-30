# notifications/discord_notifier.py
import requests

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, message):
        payload = {
            "content": message
        }
        response = requests.post(self.webhook_url, json=payload)
        if response.status_code != 204:
            logging.error(f"Failed to send Discord message: {response.text}")