from pathlib import Path
import pandas as pd
from src.services.fuel_service import list_fuel_records
from src.services.mileage_service import calculate_mileage,invalid_readings
REPORTS=Path("reports"); REPORTS.mkdir(exist_ok=True)
def vehicle_report():
    df=calculate_mileage(list_fuel_records())
    if df.empty: return pd.DataFrame(columns=["vehicle_code","valid_full_tank_intervals","average_mileage_km_l","fuel_expense"])
    rows=[]
    for code,g in df.groupby("vehicle_code"):
        vals=g["mileage_km_per_litre"].dropna()
        rows.append({"vehicle_code":code,"valid_full_tank_intervals":int(vals.count()),"average_mileage_km_l":round(float(vals.mean()),2) if len(vals) else None,"fuel_expense":round(float(g.total_cost.sum()),2)})
    return pd.DataFrame(rows)
def monthly_report():
    rows=list_fuel_records()
    if not rows: return pd.DataFrame(columns=["month","vehicle_code","fuel_expense","litres_purchased","purchase_count"])
    df=pd.DataFrame(rows); df["month"]=pd.to_datetime(df.fill_date).dt.to_period("M").astype(str)
    return df.groupby(["month","vehicle_code"],as_index=False).agg(fuel_expense=("total_cost","sum"),litres_purchased=("litres","sum"),purchase_count=("record_id","count"))
def export_reports():
    records=list_fuel_records()
    frames={"fuel_records_analysis.csv":calculate_mileage(records),"vehicle_mileage_report.csv":vehicle_report(),"monthly_expense_summary.csv":monthly_report(),"invalid_readings.csv":invalid_readings(records)}
    paths=[]
    for name,frame in frames.items():
        path=REPORTS/name; frame.to_csv(path,index=False); paths.append(path)
    return paths
