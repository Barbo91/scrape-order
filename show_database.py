import sqlite3

# Funzione per visualizzare i prodotti nel database
def show_products_in_db():
    conn = sqlite3.connect("database/products.db")
    cursor = conn.cursor()
    
    # Seleziona tutti i prodotti dal database
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    if products:
        for product in products:
            id, name, price, availability, link, last_updated = product
            print(f"ID: {id}")
            print(f"Nome: {name}")
            print(f"Prezzo: {price}")
            print(f"Disponibilità: {availability}")
            print(f"Link: {link}")
            print(f"Ultimo aggiornamento: {last_updated}")
            print("-" * 40)
    else:
        print("Nessun prodotto trovato nel database.")

    conn.close()

if __name__ == "__main__":
    show_products_in_db()  # Visualizza i prodotti nel database
