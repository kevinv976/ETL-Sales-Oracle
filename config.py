# config.py
# Edita estos valores con tus credenciales Oracle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_CONFIG = {
    "user":     "USUARIO_KEVIN",
    "password": "opmleWZr_12",
    "dsn":      "localhost:1521/orcl",
}

API_URL = "https://open.er-api.com/v6/latest/USD"

CSV_PATH  = os.path.join(BASE_DIR, "data", "ventas.csv")
LOG_PATH  = os.path.join(BASE_DIR, "logs", "etl.log")