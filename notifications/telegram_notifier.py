# notifications/telegram_notifier.py
import requests

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"Failed to send Telegram message: {response.text}")