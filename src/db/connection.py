import mysql.connector
from config.settings import DB_CONFIG
def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as exc:
        raise RuntimeError(f"MySQL connection failed: {exc}. Check service and .env.") from exc
