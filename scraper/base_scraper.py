# scrapers/base_scraper.py
import sqlite3
import logging
from playwright.sync_api import sync_playwright

class BaseScraper:
    def __init__(self, site_name, log_file, db_path):
        self.site_name = site_name
        self.log_file = log_file
        self.db_path = db_path
        self.setup_logging()
        self.create_db()

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

    def create_db(self):
        conn = sqlite3.connect(self.db_path)
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

    def update_product_in_db(self, name, price, availability, link):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE link=?", (link,))
        existing_product = cursor.fetchone()

        if existing_product:
            cursor.execute("""
                UPDATE products
                SET availability = ?, price = ?, last_updated = CURRENT_TIMESTAMP
                WHERE link = ?
            """, (availability, price, link))
            logging.info(f"Prodotto aggiornato: {name} - Disponibilità: {availability}")
        else:
            cursor.execute("""
                INSERT INTO products (name, price, availability, link)
                VALUES (?, ?, ?, ?)
            """, (name, price, availability, link))
            logging.info(f"Prodotto aggiunto: {name} - Disponibilità: {availability}")

        conn.commit()
        conn.close()

    def scrape(self):
        raise NotImplementedError("Subclasses must implement this method")