import pandas as pd
import numpy as np
COLS=["record_id","vehicle_id","vehicle_code","fill_date","odometer_km","litres","total_cost","full_tank_flag","distance_km","mileage_km_per_litre","partial_fill_estimate_km_per_litre","cost_per_km","calculation_note"]
def calculate_mileage(records):
    # Reliable mileage needs consecutive full-tank fills, same fill level, and no omitted purchases.
    if not records: return pd.DataFrame(columns=COLS)
    df=pd.DataFrame(records).copy()
    df["fill_date"]=pd.to_datetime(df["fill_date"])
    for c in ["odometer_km","litres","total_cost"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    df["full_tank_flag"]=df["full_tank_flag"].astype(bool)
    df=df.sort_values(["vehicle_id","fill_date","odometer_km","record_id"]).reset_index(drop=True)
    for c in ["distance_km","mileage_km_per_litre","partial_fill_estimate_km_per_litre","cost_per_km"]: df[c]=np.nan
    df["calculation_note"]="Not enough data for reliable mileage"
    for _,g in df.groupby("vehicle_id",sort=False):
        prev=None; prev_full=None
        for i in g.index:
            row=df.loc[i]
            if prev is not None:
                last=df.loc[prev]; distance=float(row.odometer_km-last.odometer_km)
                if distance < 0: df.loc[i,"calculation_note"]="INVALID: odometer decreased"
                elif distance == 0: df.loc[i,"calculation_note"]="No distance between readings"
                else:
                    df.loc[i,"distance_km"]=distance
                    df.loc[i,"cost_per_km"]=float(row.total_cost)/distance
                    if row.full_tank_flag and prev_full is not None:
                        full_distance=float(row.odometer_km-df.loc[prev_full,"odometer_km"])
                        if full_distance>0 and row.litres>0:
                            df.loc[i,"mileage_km_per_litre"]=full_distance/float(row.litres)
                            df.loc[i,"calculation_note"]="Full-tank interval; assumes no omitted fills"
                    elif not row.full_tank_flag:
                        df.loc[i,"partial_fill_estimate_km_per_litre"]=distance/float(row.litres)
                        df.loc[i,"calculation_note"]="Approximate only: partial fill"
            if row.full_tank_flag: prev_full=i
            prev=i
    return df[COLS]
def invalid_readings(records):
    cols=["record_id","vehicle_code","fill_date","odometer_km","issue"]
    if not records: return pd.DataFrame(columns=cols)
    df=pd.DataFrame(records).copy(); df["fill_date"]=pd.to_datetime(df["fill_date"])
    df=df.sort_values(["vehicle_id","fill_date","record_id"]); issues=[]
    for _,g in df.groupby("vehicle_id"):
        prev=None
        for _,r in g.iterrows():
            if prev is not None and r.odometer_km < prev.odometer_km:
                issues.append({"record_id":r.record_id,"vehicle_code":r.vehicle_code,"fill_date":r.fill_date,"odometer_km":r.odometer_km,"issue":"Odometer reading decreased"})
            prev=r
    return pd.DataFrame(issues,columns=cols)
