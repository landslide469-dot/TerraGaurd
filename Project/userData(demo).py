import sqlite3

DB_NAME = "TerraGuard.db"

def create_new_user_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Newuser (
            name TEXT,
            mobile TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


def insert_new_user(name, mobile, password):
    create_new_user_table()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Newuser (name, mobile, password)
        VALUES (?, ?, ?)
    """, (name, mobile, password))

    conn.commit()
    conn.close()