import sqlite3


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collection_products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productid INTEGER NOT NULL,
            collection TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def insert_collection(productid, collection):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO collection_products (productid, collection)
        VALUES (?, ?)
    ''', (productid, collection))

    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
