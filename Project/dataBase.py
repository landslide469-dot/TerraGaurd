import sqlite3
import random

DB_NAME = "TerraGuard.db"


        
    
#insertNewArea = cursor.execute("""
                   
                  # INSERT INTO userCode (area_code,name,mobile,risk_rate,disaster,latitude,longitude) VALUES(?,?,?,?,?,?,?)
                   
                  # """,(area_code,name,mobile,risk_rate,disaster,latitude,longitude))
    
    
    #if insertNewArea:
     #   print("AREA ADDED !")
    
    
    
  #  if cursor.execute:
     #   print("Data Base Created !!")
    
   # conn.commit()
   # conn.close()

# Generate a unique 6‑digit area code
def generate_unique_code():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    while True:
        code = str(random.randint(100000, 999999))
        cursor.execute("SELECT 1 FROM userCode WHERE area_code = ?", (code,))
        if not cursor.fetchone():
            conn.close()
            return code
           




# Insert a user record
def insert_user_area(name, mobile, risk_rate, disaster, latitude, longitude):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    area_code = generate_unique_code()
    cursor.execute("""
        INSERT INTO userCode (
            area_code, name, mobile, risk_rate, disaster, latitude, longitude
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (area_code, name, mobile, risk_rate, disaster, latitude, longitude))
    conn.commit()
    conn.close()
    
    
    

def get_user_area(lat, lon):
    lat
    lon
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    res = cursor.execute("""
        SELECT area_code 
        FROM userCode 
        WHERE latitude = ? AND longitude = ?
    """, (lat, lon))
    
    if res == "":
        generate_unique_code()

    result = cursor.fetchone()
    conn.close()

    if result:  # check if a row was found
        return result[0]  # area_code is at index 0
    else:
        
         name = 'abcs'
         mobile = "808209975"
         risk_rate = "91.5%"
         disaster = "Flood"
         latitude = lat
         longitude = lon
        
         insert_user_area(name, mobile, risk_rate, disaster, latitude, longitude)
    
    
    
    
    
def get_user_area_by_code(code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    result_code = cursor.execute("""
                   SELECT latitude, longitude FROM userCode WHERE area_code = ?""",(code,))
    
    searchCodeResult = result_code.fetchall()
    
    return searchCodeResult[0]   
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
def get_user_area(code):
    
    with sq.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        res = cursor.execute("""
            SELECT * FROM areaTable WHERE area_code = ?""",(code))

    lat = res[0]
    long = res[1]
    return lat,long
    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        