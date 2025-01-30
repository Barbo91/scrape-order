import sqlite3
import logging
from playwright.sync_api import sync_playwright

# Configurazione logging
logging.basicConfig(
    filename="logs/scraper_fantasiastore_log.txt",  # File di log
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
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Funzione per aggiungere o aggiornare i prodotti nel database
def update_product_in_db(name, price, availability):
    conn = sqlite3.connect("database/products.db")
    cursor = conn.cursor()

    # Controlla se il prodotto è già nel database
    cursor.execute("SELECT * FROM products WHERE name=?", (name,))
    existing_product = cursor.fetchone()

    if existing_product:
        # Se il prodotto esiste, aggiorna la disponibilità
        cursor.execute("""
            UPDATE products
            SET availability = ?, price = ?, last_updated = CURRENT_TIMESTAMP
            WHERE name = ?
        """, (availability, price, name))
        logging.info(f"Prodotto aggiornato: {name} - Disponibilità: {availability}")
    else:
        # Se il prodotto non esiste, inseriscilo
        cursor.execute("""
            INSERT INTO products (name, price, availability)
            VALUES (?, ?, ?)
        """, (name, price, availability))
        logging.info(f"Prodotto aggiunto: {name} - Disponibilità: {availability}")

    conn.commit()
    conn.close()

# Funzione di scraping
def scrape_fantasiastore():
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
                # Estrazione dei dati
                name = product.query_selector(".h3.product-title").inner_text().strip()
                price = product.query_selector(".product-price-and-shipping").inner_text().strip()
                availability = product.query_selector(".product-availability").inner_text().strip()

                # Logga il prodotto
                logging.info(f"Prodotto trovato: {name}, Prezzo: {price}, Disponibilità: {availability}")

                # Aggiungi o aggiorna il prodotto nel database
                update_product_in_db(name, price, availability)
            except Exception as e:
                logging.error(f"Errore durante lo scraping di un prodotto: {e}")

        browser.close()

if __name__ == "__main__":
    create_db()  # Crea il database se non esiste
    scrape_fantasiastore()  # Esegui lo scraping
