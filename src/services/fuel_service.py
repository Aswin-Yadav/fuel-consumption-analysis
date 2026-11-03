from datetime import date
from decimal import Decimal, InvalidOperation
from src.db.connection import get_connection

def checked_number(value, label, zero_ok=False):
    try: n=Decimal(str(value))
    except (InvalidOperation,ValueError): raise ValueError(f"{label} must be numeric.")
    if not n.is_finite() or n < 0 or (n == 0 and not zero_ok):
        raise ValueError(f"{label} must be {'zero or more' if zero_ok else 'greater than zero'}.")
    return n

def record_fuel(vehicle_id, day, odometer, litres, cost, full, notes=""):
    try: day=date.fromisoformat(day.strip())
    except ValueError: raise ValueError("Date must use YYYY-MM-DD.")
    odo=checked_number(odometer,"Odometer",True)
    litres=checked_number(litres,"Litres")
    cost=checked_number(cost,"Cost",True)
    conn=get_connection()
    try:
        cur=conn.cursor(dictionary=True)
        cur.execute("SELECT vehicle_id FROM vehicles WHERE vehicle_id=%s",(vehicle_id,))
        if not cur.fetchone(): raise ValueError("Vehicle ID does not exist.")
        cur.execute("SELECT fill_date,odometer_km FROM fuel_records WHERE vehicle_id=%s ORDER BY fill_date DESC,odometer_km DESC,record_id DESC LIMIT 1",(vehicle_id,))
        prev=cur.fetchone()
        if prev and day < prev["fill_date"]: raise ValueError("Enter records chronologically; date is earlier than the last record.")
        if prev and odo < Decimal(str(prev["odometer_km"])): raise ValueError("Odometer cannot be lower than the previous reading.")
        cur.execute("INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (vehicle_id,day,odo,litres,cost,bool(full),notes.strip() or None))
        conn.commit()
    finally: conn.close()

def list_fuel_records():
    conn=get_connection()
    try:
        cur=conn.cursor(dictionary=True)
        cur.execute("SELECT fr.*,v.vehicle_code,v.vehicle_type,v.fuel_type FROM fuel_records fr JOIN vehicles v ON v.vehicle_id=fr.vehicle_id ORDER BY v.vehicle_code,fr.fill_date,fr.odometer_km,fr.record_id")
        return cur.fetchall()
    finally: conn.close()
