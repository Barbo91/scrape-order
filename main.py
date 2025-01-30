# main.py
import schedule
import time
from scraper.federicstore_scraper import FedericStoreScraper
from scraper.fantasiastore_scraper import FantasiaStoreScraper
from notifications.telegram_notifier import TelegramNotifier
from notifications.discord_notifier import DiscordNotifier
import config

# Initialize notifiers
telegram_notifier = TelegramNotifier(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID)
discord_notifier = DiscordNotifier(config.DISCORD_WEBHOOK_URL)

# Initialize scrapers
federicstore_scraper = FedericStoreScraper()
fantasiastore_scraper = FantasiaStoreScraper()

def job():
    try:
        federicstore_scraper.scrape()
        fantasiastore_scraper.scrape()
        telegram_notifier.send_message("Scraping completed successfully.")
        discord_notifier.send_message("Scraping completed successfully.")
    except Exception as e:
        telegram_notifier.send_message(f"Scraping failed: {e}")
        discord_notifier.send_message(f"Scraping failed: {e}")

# Schedule the job to run every 30 seconds
schedule.every(30).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)