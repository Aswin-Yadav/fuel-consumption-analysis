import pandas as pd
from src.services.vehicle_service import list_vehicles,add_vehicle
from src.services.fuel_service import record_fuel,list_fuel_records
from src.services.mileage_service import calculate_mileage,invalid_readings
from src.analysis.reports import vehicle_report,monthly_report,export_reports
from src.visualization.charts import generate_charts
def table(df): print("No data available." if df is None or df.empty else df.to_string(index=False))
def show_vehicles():
    vs=list_vehicles()
    if not vs: print("No vehicles; add one first.")
    for v in vs: print(f"ID {v['vehicle_id']} | {v['vehicle_code']} | {v['vehicle_type']} | {v['fuel_type']}")
def menu():
    print("\n=== FUEL CONSUMPTION ANALYSIS ===\n1 List vehicles\n2 Add vehicle\n3 Record fuel purchase\n4 View records\n5 Mileage report\n6 Monthly expenses\n7 Export CSV reports\n8 Generate charts\n9 Invalid readings\n0 Exit")
def main():
    while True:
        menu(); choice=input("Choose: ").strip()
        try:
            if choice=="1": show_vehicles()
            elif choice=="2": add_vehicle(input("Vehicle code: "),input("Vehicle type: "),input("Fuel type: ")); print("Vehicle added.")
            elif choice=="3":
                show_vehicles(); vid=int(input("Vehicle ID: ")); day=input("Date YYYY-MM-DD: "); odo=input("Odometer km: "); litres=input("Litres: "); cost=input("Total cost: ")
                full=input("Full tank? y/n: ").lower().strip()=="y"; notes=input("Notes optional: ")
                record_fuel(vid,day,odo,litres,cost,full,notes); print("Record saved.")
            elif choice=="4": table(pd.DataFrame(list_fuel_records()))
            elif choice=="5":
                df=calculate_mileage(list_fuel_records())
                table(df[["vehicle_code","fill_date","odometer_km","litres","full_tank_flag","distance_km","mileage_km_per_litre","partial_fill_estimate_km_per_litre","cost_per_km","calculation_note"]])
                print("Full-tank results assume consistent fill level and no omitted purchases. Partial fills are estimates.")
            elif choice=="6": table(monthly_report())
            elif choice=="7":
                for p in export_reports(): print("Saved:",p)
            elif choice=="8":
                for p in generate_charts(): print("Saved:",p)
            elif choice=="9": table(invalid_readings(list_fuel_records()))
            elif choice=="0": print("Goodbye!"); break
            else: print("Choose a number from 0 to 9.")
        except (ValueError,RuntimeError) as exc: print("Error:",exc)
        except Exception as exc: print("Unexpected error:",exc)
if __name__=="__main__": main()
