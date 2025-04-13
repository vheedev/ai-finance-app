import sqlite3

DB_NAME = "finance_app.db"

# Initialize database

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            account TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Sample insertion

def insert_sample_transactions(user_id):
    transactions = [
        (user_id, "2025-04-01", "Gaji Bulanan", 7000000, "income", "BCA"),
        (user_id, "2025-04-02", "Belanja Tokopedia via GoPay", -1500000, "expense", "GoPay"),
        (user_id, "2025-04-03", "Investasi Mandiri", -3000000, "expense", "Mandiri"),
        (user_id, "2025-04-04", "Modal Dagang Shopee", -2000000, "expense", "ShopeePay"),
        (user_id, "2025-04-05", "Penjualan via Moka POS", 2500000, "income", "Moka POS"),
        (user_id, "2025-04-08", "Penjualan Tokopedia", 1500000, "income", "Tokopedia"),
        (user_id, "2025-04-09", "Beli bahan baku Tokopedia", -500000, "expense", "Tokopedia"),
        (user_id, "2025-04-10", "Bayar Listrik PLN", -500000, "expense", "BCA"),
        (user_id, "2025-04-12", "Makan Siang", -100000, "expense", "GoPay"),
    ]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT INTO transactions (user_id, date, description, amount, type, account)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', transactions)
    conn.commit()
    conn.close()

# Utility to fetch transactions

def get_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT date, description, amount, type, account FROM transactions WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"date": row[0], "description": row[1], "amount": row[2], "type": row[3], "account": row[4]}
        for row in rows
    ]

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized. Run insert_sample_transactions(user_id) manually to insert demo data.")
