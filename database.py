import sqlite3

#koneksi ke database
def create_connection(db_file="inventory.db"):
    """ creating database connection to SQLite files """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

#get data semua akun
def get_all_accounts():
    """ Mengambil semua akun dari tabel accounts """
    conn = create_connection()
    if conn is not None:
        try:
            conn.row_factory = sqlite3.Row #memungkinkan mengakses kolom berdasarkan nama
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts ORDER BY name")
            accounts = cursor.fetchall()
            return accounts
        except sqlite3.Error as e:
            print(f"Error fetching accounts: {e}")
            return []
        finally:
            conn.close()
    return []

#add_account, get_pets, dll. di sini