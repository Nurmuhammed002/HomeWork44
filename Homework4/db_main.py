import sqlite3


def create_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Создание таблицы для продуктов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        productid TEXT NOT NULL,
        category TEXT NOT NULL,
        infoproduct TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


def add_product(productid, category, infoproduct):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO products_details (productid, category, infoproduct)
    VALUES (?, ?, ?)
    ''', (productid, category, infoproduct))

    conn.commit()
    conn.close()


def get_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products_details')
    products = cursor.fetchall()

    conn.close()
    return products
