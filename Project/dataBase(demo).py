import sqlite3
import random

DB_NAME = "TerraGuard.db"

# -------------------------------------------------
# CREATE TABLE
# -------------------------------------------------
def create_area_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS userCode (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_code TEXT UNIQUE,
            name TEXT,
            mobile TEXT,
            risk_rate TEXT,
            disaster TEXT,
            latitude REAL,
            longitude REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# -------------------------------------------------
# GENERATE UNIQUE CODE
# -------------------------------------------------
def generate_unique_code():
    create_area_table()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    while True:
        code = str(random.randint(100000, 999999))
        cursor.execute("SELECT 1 FROM userCode WHERE area_code = ?", (code,))
        if not cursor.fetchone():
            conn.close()
            return code


# -------------------------------------------------
# INSERT NEW PLACE
# -------------------------------------------------
def insert_user_area(name, mobile, risk_rate, disaster, latitude, longitude):
    create_area_table()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    area_code = generate_unique_code()

    cursor.execute("""
        INSERT INTO userCode
        (area_code, name, mobile, risk_rate, disaster, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (area_code, name, mobile, risk_rate, disaster, latitude, longitude))

    conn.commit()
    conn.close()

    return area_code


# -------------------------------------------------
# GET AREA BY COORDINATES
# -------------------------------------------------
def get_area_by_coordinates(lat, lon):
    create_area_table()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT area_code FROM userCode
        WHERE latitude = ? AND longitude = ?
    """, (lat, lon))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


# -------------------------------------------------
# GET COORDINATES BY AREA CODE
# -------------------------------------------------
def get_user_area_by_code(code):
    create_area_table()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT latitude, longitude
        FROM userCode
        WHERE area_code = ?
    """, (code,))

    result = cursor.fetchone()
    conn.close()

    return result if result else None