from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from src.services.fuel_service import list_fuel_records
from src.services.mileage_service import calculate_mileage
from src.analysis.reports import monthly_report
OUT=Path("output"); OUT.mkdir(exist_ok=True)
def generate_charts():
    records=list_fuel_records()
    if not records: print("No records found."); return []
    made=[]; data=calculate_mileage(records); valid=data.dropna(subset=["mileage_km_per_litre"])
    if not valid.empty:
        avg=valid.groupby("vehicle_code",as_index=False)["mileage_km_per_litre"].mean()
        plt.figure(figsize=(8,5)); plt.bar(avg.vehicle_code,avg.mileage_km_per_litre)
        plt.title("Average Full-Tank Mileage by Vehicle"); plt.xlabel("Vehicle"); plt.ylabel("km per litre"); plt.tight_layout()
        p=OUT/"vehicle_mileage.png"; plt.savefig(p,dpi=150); plt.close(); made.append(p)
    else: print("No valid full-tank intervals for mileage chart.")
    monthly=monthly_report()
    if not monthly.empty:
        exp=monthly.groupby("month",as_index=False).fuel_expense.sum()
        plt.figure(figsize=(8,5)); plt.plot(exp.month,exp.fuel_expense,marker="o")
        plt.title("Monthly Fuel Expense Trend"); plt.xlabel("Month"); plt.ylabel("Fuel expense"); plt.xticks(rotation=30,ha="right"); plt.tight_layout()
        p=OUT/"monthly_fuel_expense.png"; plt.savefig(p,dpi=150); plt.close(); made.append(p)
    return made
