# file: database.py

import sqlite3

def create_connection(db_file="inventory.db"):
    """ Membuat koneksi database ke file SQLite """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_all_accounts():
    """ Mengambil semua akun dari tabel akun """
    conn = create_connection()
    if conn is not None:
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM akun ORDER BY nama_akun")
            accounts = cursor.fetchall()
            return accounts
        except sqlite3.Error as e:
            print(f"Error fetching accounts: {e}")
            return []
        finally:
            conn.close()
    return []

def add_account(name):
    """ Menambahkan akun baru ke tabel akun """
    conn = create_connection()
    if conn is not None:
        sql = ''' INSERT INTO akun(nama_akun)
                VALUES(?) '''
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (name,))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding account: {e}")
            return None
        finally:
            conn.close()
    return None

#fetching data pet berdasarkan account_id
def get_pets_by_account_id(account_id):
    """ Mengambil semua pet dari satu akun berdasarkan account_id """
    conn = create_connection()
    pets = []
    if conn is not None:
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, nama_pet, age_pet, weight_pet FROM pets WHERE akun_id = ?", (account_id,))
            pets = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching pets: {e}")
        finally:
            conn.close()
    return pets

# fungsi add, update, delete pet
def add_pet(name, age, weight, account_id):
    """ Menambahkan pet baru ke akun tertentu """
    conn = create_connection()
    sql = ''' INSERT INTO pets(nama_pet, age_pet, weight_pet, akun_id)
            VALUES(?,?,?,?) '''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, age, weight, account_id))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding pet: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_pet(pet_id, name, age, weight):
    """ Memperbarui data pet yang sudah ada """
    conn = create_connection()
    sql = ''' UPDATE pets
            SET nama_pet = ? ,
                age_pet = ? ,
                weight_pet = ?
            WHERE id = ?'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (name, age, weight, pet_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating pet: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_pet(pet_id):
    """ Menghapus pet dari database berdasarkan id """
    conn = create_connection()
    sql = 'DELETE FROM pets WHERE id = ?'
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (pet_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting pet: {e}")
        return False
    finally:
        if conn:
            conn.close()

def delete_account(account_id):
    """ Menghapus akun dan semua pet yang terkait dengannya """
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            # Langkah 1: Hapus semua pet yang memiliki akun_id ini
            cursor.execute("DELETE FROM pets WHERE akun_id = ?", (account_id,))
            # Langkah 2: Hapus akun itu sendiri
            cursor.execute("DELETE FROM akun WHERE id = ?", (account_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting account: {e}")
            return False
        finally:
            conn.close()
    return False

#fungsi transfer pet
def transfer_pet(pet_id, new_account_id):
    """ Memindahkan pet ke akun lain dengan mengubah akun_id-nya """
    conn = create_connection()
    sql = ''' UPDATE pets SET akun_id = ? WHERE id = ?'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (new_account_id, pet_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error transferring pet: {e}")
        return False
    finally:
        if conn:
            conn.close()