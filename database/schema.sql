CREATE DATABASE IF NOT EXISTS fuel_analysis;
USE fuel_analysis;
CREATE TABLE IF NOT EXISTS vehicles (
 vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
 vehicle_code VARCHAR(30) NOT NULL UNIQUE,
 vehicle_type VARCHAR(40) NOT NULL,
 fuel_type ENUM('Petrol','Diesel','CNG','Electric','Other') NOT NULL
);
CREATE TABLE IF NOT EXISTS fuel_records (
 record_id INT AUTO_INCREMENT PRIMARY KEY,
 vehicle_id INT NOT NULL,
 fill_date DATE NOT NULL,
 odometer_km DECIMAL(10,1) NOT NULL,
 litres DECIMAL(10,3) NOT NULL,
 total_cost DECIMAL(10,2) NOT NULL,
 full_tank_flag BOOLEAN NOT NULL DEFAULT FALSE,
 notes VARCHAR(255),
 FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
 CHECK (odometer_km >= 0),
 CHECK (litres > 0),
 CHECK (total_cost >= 0),
 INDEX idx_vehicle_date (vehicle_id, fill_date, odometer_km)
);
