import sqlite3
import logging
from playwright.sync_api import sync_playwright

# Configurazione logging
logging.basicConfig(
    filename="logs/scraper_federicstore_log.txt",  # File di log
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Connessione al database SQLite
def create_db():
    conn = sqlite3.connect("database/products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            availability TEXT,
            link TEXT UNIQUE,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Funzione per aggiungere o aggiornare i prodotti nel database
def update_product_in_db(name, price, availability, link):
    conn = sqlite3.connect("database/products.db")
    cursor = conn.cursor()

    # Controlla se il prodotto è già nel database
    cursor.execute("SELECT * FROM products WHERE link=?", (link,))
    existing_product = cursor.fetchone()

    if existing_product:
        # Se il prodotto esiste, aggiorna la disponibilità
        cursor.execute("""
            UPDATE products
            SET availability = ?, price = ?, last_updated = CURRENT_TIMESTAMP
            WHERE link = ?
        """, (availability, price, link))
        logging.info(f"Prodotto aggiornato: {name} - Disponibilità: {availability}")
    else:
        # Se il prodotto non esiste, inseriscilo
        cursor.execute("""
            INSERT INTO products (name, price, availability, link)
            VALUES (?, ?, ?, ?)
        """, (name, price, availability, link))
        logging.info(f"Prodotto aggiunto: {name} - Disponibilità: {availability}")

    conn.commit()
    conn.close()

# Funzione di scraping
def scrape_federicstore():
    url = "https://federicstore.it/categoria/prevendita/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Selettori CSS basati sulla struttura della pagina
        products = page.query_selector_all(".product")

        for product in products:
            try:
                name = product.query_selector(".woocommerce-loop-product__title")
                price = product.query_selector(".woocommerce-Price-amount")
                link = product.query_selector("a")

                # Escludi i prodotti con la parola "live"
                if name and "live" not in name.inner_text().lower():
                    name_text = name.inner_text().strip()
                    price_text = price.inner_text().strip() if price else "N/A"
                    link_href = link.get_attribute("href") if link else "N/A"

                    # Verifica il bottone di disponibilità
                    availability_button = product.query_selector(".button.product_type_simple")

                    if availability_button:
                        button_text = availability_button.inner_text().strip().lower()
                        logging.debug(f"Button Text: {button_text}")  # Debugging statement

                        if "preordina" in button_text:
                            availability_text = "Disponibile"
                        elif "esaurito" in button_text:
                            availability_text = "Esaurito"
                        else:
                            availability_text = "Sconosciuto"
                    else:
                        availability_text = "Sconosciuto"

                    # Logga il prodotto
                    logging.info(f"Prodotto trovato: {name_text}, Prezzo: {price_text}, Disponibilità: {availability_text}, Link: {link_href}")

                    # Aggiungi o aggiorna il prodotto nel database
                    update_product_in_db(name_text, price_text, availability_text, link_href)
            except Exception as e:
                logging.error(f"Errore durante il scraping di un prodotto: {e}")

        browser.close()

