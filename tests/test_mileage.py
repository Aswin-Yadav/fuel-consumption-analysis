import unittest
from datetime import date
from src.services.mileage_service import calculate_mileage
class MileageTests(unittest.TestCase):
    def setUp(self):
        self.records=[
        {"record_id":1,"vehicle_id":1,"vehicle_code":"CAR-1","fill_date":date(2026,1,1),"odometer_km":1000,"litres":20,"total_cost":2000,"full_tank_flag":True},
        {"record_id":2,"vehicle_id":1,"vehicle_code":"CAR-1","fill_date":date(2026,1,10),"odometer_km":1300,"litres":25,"total_cost":2500,"full_tank_flag":True},
        {"record_id":3,"vehicle_id":1,"vehicle_code":"CAR-1","fill_date":date(2026,1,15),"odometer_km":1360,"litres":5,"total_cost":500,"full_tank_flag":False}]
    def test_full_tank_mileage(self):
        row=calculate_mileage(self.records).query("record_id == 2").iloc[0]
        self.assertAlmostEqual(row["mileage_km_per_litre"],12.0)
    def test_partial_is_estimate(self):
        row=calculate_mileage(self.records).query("record_id == 3").iloc[0]
        self.assertAlmostEqual(row["partial_fill_estimate_km_per_litre"],12.0)
        self.assertTrue(pd_is_nan(row["mileage_km_per_litre"]))
    def test_empty(self): self.assertTrue(calculate_mileage([]).empty)
def pd_is_nan(x): return x != x
if __name__=="__main__": unittest.main()
