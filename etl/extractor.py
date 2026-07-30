# etl/extractor.py
import pandas as pd
import requests
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import CSV_PATH, API_URL

logger = logging.getLogger(__name__)


def extraer_csv() -> pd.DataFrame:
    """Lee el archivo CSV de ventas y retorna un DataFrame."""
    logger.info(f"Extrayendo datos desde CSV: {CSV_PATH}")
    try:
        df = pd.read_csv(CSV_PATH)
        logger.info(f"  {len(df)} filas leídas del CSV.")
        return df
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {CSV_PATH}")
        raise


def extraer_tipo_cambio() -> dict:
    """
    Llama a la API pública de tasas de cambio y retorna
    un dict con las tasas relevantes (USD → PAB, MXN, COP).
    """
    logger.info(f"Extrayendo tipo de cambio desde API: {API_URL}")
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        tasas = {
            "USD_PAB": data["rates"].get("PAB", 1.0),
            "USD_MXN": data["rates"].get("MXN", 17.0),
            "USD_COP": data["rates"].get("COP", 4000.0),
        }
        logger.info(f"  Tasas obtenidas: {tasas}")
        return tasas

    except requests.RequestException as e:
        logger.warning(f"Error al llamar la API: {e}. Usando tasas por defecto.")
        return {"USD_PAB": 1.0, "USD_MXN": 17.5, "USD_COP": 4100.0}
