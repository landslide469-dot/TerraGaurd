import sqlite3 as sq
import random

DB_NAME = "TerraGaurd.db"

#LINK TO LOGIN OR CRAETE ACCOUNT PAGE


#CREATING NEW USER TABLE
def create_new_user(name,mobile,password):
    
    conn = sq.connect(DB_NAME,timeout=10)
    cur = conn.cursor()
    cur_exe = cur.execute(""" CREATE TABLE IF NOT EXISTS users (
            name TEXT NOT NULL,
            mobile TEXT,
            password TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
    
    if cur_exe:
        
        insert = cur.execute(""" 
                             INSERT INTO users (name,mobile,password) 
                             VALUES(?,?,?)
                             """,(name,mobile,password))
        
    if(insert):
        print("New User ",name," added !")
        
    print("New Database Craeted !")
    conn.commit()
    conn.close()
    
    
    
    #FOR LOGIN
def fetch_user(mobile,password):
    
    conn = sq.connect(DB_NAME)
    cur = conn.cursor()
    query = cur.execute("""
                        SELECT * FROM users WHERE mobile = ? AND password = ?
                        """,(mobile,password))
    
    result = query.fetchone()
    
    print("Welcome , ",result[0])
   
   

# -----------------------------
# CREATE AREA TABLE
# -----------------------------
def create_area_table():
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS areaTable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area_code TEXT UNIQUE,
                name TEXT,
                mobile TEXT,
                risk_rate TEXT,
                disaster TEXT,
                latitude REAL,
                longitude REAL
            )
        """)
        conn.commit()


# -----------------------------
# FETCH AREA BY CODE
# -----------------------------
def fetchAreaTableByCode(code):
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT latitude,longitude FROM areaTable WHERE area_code == ?""",(code,))
        res = cursor.fetchone()
        if res:
            return res
        else:
            return None





# -----------------------------
# GENERATE UNIQUE CODE
# -----------------------------
def generate_unique_code():
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        while True:
            code = str(random.randint(100000, 999999))
            cursor.execute("SELECT 1 FROM areaTable WHERE area_code = ?", (code,))
            if not cursor.fetchone():
                return code

# -----------------------------
# INSERT AREA
# -----------------------------
def insert_user_area(name, mobile, risk_rate, disaster, latitude, longitude):
    # Make sure table exists
    create_area_table()

    # Check if area already exists
    existing_code = fetchAreaTable(latitude, longitude)
    if existing_code:
        print("Area already exists with code:", existing_code)
        return existing_code

    # Otherwise, insert new area
    code = generate_unique_code()
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO areaTable (
                area_code, name, mobile, risk_rate, disaster, latitude, longitude
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (code, name, mobile, risk_rate, disaster, latitude, longitude))
        conn.commit()
        print("NEW AREA WITH CODE:", code, "INSERTED!")
        return code



# ------------------------------------------------
# GET USER AREA TABLE BY LAT LON
# ------------------------------------------------

def fetchAreaTable(lat, lon):
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT area_code 
            FROM areaTable 
            WHERE latitude == ? AND longitude == ?
        """, (lat, lon))
        
        res = cursor.fetchone() #[0]
        if res:
            print(res)
            return res 
        else:
            print("NOO")




