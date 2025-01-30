# scrapers/fantasiastore_scraper.py
from .base_scraper import BaseScraper

class FantasiaStoreScraper(BaseScraper):
    def __init__(self):
        super().__init__("FantasiaStore", "logs/scraper_fantasiastore_log.txt", "database/products.db")

    def scrape(self):
        url = "https://fantasiastore.it/it/13-pokemon?preordine=1"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            try:
                page.wait_for_selector(".h3.product-title", timeout=60000)  # 60 secondi di timeout
            except Exception as e:
                logging.error(f"Errore durante l'attesa del selettore .product-title: {e}")
                browser.close()
                return

            products = page.query_selector_all(".product")
            if not products:
                logging.error("Nessun prodotto trovato.")
                browser.close()
                return

            for product in products:
                try:
                    name = product.query_selector(".h3.product-title").inner_text().strip()
                    price = product.query_selector(".product-price-and-shipping").inner_text().strip()
                    availability = product.query_selector(".product-availability").inner_text().strip()

                    logging.info(f"Prodotto trovato: {name}, Prezzo: {price}, Disponibilità: {availability}")
                    self.update_product_in_db(name, price, availability, "N/A")  # FantasiaStore doesn't provide links
                except Exception as e:
                    logging.error(f"Errore durante lo scraping di un prodotto: {e}")

            browser.close()