from src.db.connection import get_connection
FUEL_TYPES = {"Petrol","Diesel","CNG","Electric","Other"}
def list_vehicles():
    conn=get_connection()
    try:
        cur=conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM vehicles ORDER BY vehicle_code")
        return cur.fetchall()
    finally: conn.close()
def add_vehicle(code, kind, fuel):
    code,kind,fuel=code.strip().upper(),kind.strip(),fuel.strip().title()
    if not code or not kind: raise ValueError("Vehicle code and type are required.")
    if fuel not in FUEL_TYPES: raise ValueError("Fuel type must be Petrol, Diesel, CNG, Electric, or Other.")
    conn=get_connection()
    try:
        cur=conn.cursor()
        cur.execute("INSERT INTO vehicles(vehicle_code,vehicle_type,fuel_type) VALUES(%s,%s,%s)",(code,kind,fuel))
        conn.commit()
    finally: conn.close()
