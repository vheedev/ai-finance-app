import sqlite3
from datetime import datetime

DB_NAME = "finance_app.db"

def add_transaction(user_id):
    print("\n=== Tambah Transaksi Baru ===")
    while True:
        try:
            date = input("Tanggal (YYYY-MM-DD): ").strip()
            datetime.strptime(date, "%Y-%m-%d")  # Validate format
            description = input("Deskripsi: ").strip()
            amount = float(input("Jumlah (gunakan tanda - untuk pengeluaran): "))
            trans_type = "income" if amount > 0 else "expense"
            account = input("Sumber/Akun (misal: BCA, GoPay, Tokopedia): ").strip()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions (user_id, date, description, amount, type, account)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, date, description, amount, trans_type, account))
            conn.commit()
            conn.close()

            print("✅ Transaksi berhasil disimpan!")
        except Exception as e:
            print(f"⚠️ Gagal menyimpan transaksi: {e}")

        again = input("Tambah transaksi lagi? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    add_transaction(1)  # for manual test
