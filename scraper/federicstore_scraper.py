# scrapers/federicstore_scraper.py
from .base_scraper import BaseScraper

class FedericStoreScraper(BaseScraper):
    def __init__(self):
        super().__init__("FedericStore", "logs/scraper_federicstore_log.txt", "database/products.db")

    def scrape(self):
        url = "https://federicstore.it/categoria/prevendita/"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            products = page.query_selector_all(".product")
            for product in products:
                try:
                    name = product.query_selector(".woocommerce-loop-product__title")
                    price = product.query_selector(".woocommerce-Price-amount")
                    link = product.query_selector("a")

                    if name and "live" not in name.inner_text().lower():
                        name_text = name.inner_text().strip()
                        price_text = price.inner_text().strip() if price else "N/A"
                        link_href = link.get_attribute("href") if link else "N/A"

                        availability_button = product.query_selector(".button.product_type_simple")
                        if availability_button:
                            button_text = availability_button.inner_text().strip().lower()
                            if "preordina" in button_text:
                                availability_text = "Disponibile"
                            elif "esaurito" in button_text:
                                availability_text = "Esaurito"
                            else:
                                availability_text = "Sconosciuto"
                        else:
                            availability_text = "Sconosciuto"

                        logging.info(f"Prodotto trovato: {name_text}, Prezzo: {price_text}, Disponibilità: {availability_text}, Link: {link_href}")
                        self.update_product_in_db(name_text, price_text, availability_text, link_href)
                except Exception as e:
                    logging.error(f"Errore durante il scraping di un prodotto: {e}")

            browser.close()