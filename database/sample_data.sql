USE fuel_analysis;
INSERT INTO vehicles(vehicle_code,vehicle_type,fuel_type) VALUES
('CAR-001','Hatchback','Petrol'),('BIKE-001','Motorcycle','Petrol')
ON DUPLICATE KEY UPDATE vehicle_type=VALUES(vehicle_type);
INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes)
SELECT vehicle_id,'2026-01-03',12000,35,3675,TRUE,'Sample full tank' FROM vehicles WHERE vehicle_code='CAR-001';
INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes)
SELECT vehicle_id,'2026-01-12',12420,30,3150,TRUE,'Sample full tank' FROM vehicles WHERE vehicle_code='CAR-001';
INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes)
SELECT vehicle_id,'2026-02-02',12810,28,2940,FALSE,'Sample partial fill' FROM vehicles WHERE vehicle_code='CAR-001';
INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes)
SELECT vehicle_id,'2026-01-04',4000,8,840,TRUE,'Sample full tank' FROM vehicles WHERE vehicle_code='BIKE-001';
INSERT INTO fuel_records(vehicle_id,fill_date,odometer_km,litres,total_cost,full_tank_flag,notes)
SELECT vehicle_id,'2026-01-15',4350,7.5,787.5,TRUE,'Sample full tank' FROM vehicles WHERE vehicle_code='BIKE-001';
