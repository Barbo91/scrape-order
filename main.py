import schedule
import time
from scraper.federicstore_scraper import scrape_federicstore, create_db

# Crea il database all'avvio
create_db()

# Funzione di scheduling per eseguire lo scraping ogni X secondi
def job():
    scrape_federicstore()

# Esegui lo scraping ogni SCRAPING_INTERVAL secondi
schedule.every(30).seconds.do(job)  # Puoi cambiare 30 con SCRAPING_INTERVAL se vuoi usare il parametro di config.py

while True:
    schedule.run_pending()
    time.sleep(1)
