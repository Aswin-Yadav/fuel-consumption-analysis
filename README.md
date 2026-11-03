# Fuel Consumption Analysis System
Python + MySQL beginner project for vehicle/fuel records, mileage, monthly expenses, CSV reports, and charts.

## Setup (Windows PowerShell)
1. Install Python 3.10+ and MySQL Server.
2. Create a virtual environment: `py -m venv .venv`
3. Activate it: `\.venv\Scripts\Activate.ps1`
4. Install packages: `python -m pip install -r requirements.txt`
5. Run `database/schema.sql` in MySQL Workbench. Optionally run `database/sample_data.sql`.
6. Copy `.env.example` to `.env` and edit credentials.
7. From this folder run: `python -m src.main`

Linux/macOS: `python3 -m venv .venv`, `source .venv/bin/activate`, install requirements, copy `.env.example` to `.env`, run SQL scripts, then `python -m src.main`.

## Menu
1 List vehicles; 2 Add vehicle; 3 Record fuel; 4 View records; 5 Mileage report; 6 Monthly expenses; 7 Export CSV; 8 Charts; 9 Invalid readings; 0 Exit.

Tests: `python -m unittest discover -s tests -v`

## Mileage limitation
Mileage is calculated only between consecutive full-tank records, using the distance between them divided by litres at the later full fill. This assumes the same tank fill level and no omitted fuel purchases. Partial-fill distance/litre is shown only as an estimate, not reliable full-tank mileage. Cost/km is the latest fill cost divided by the distance since the prior record, so it is an approximate interval indicator.
