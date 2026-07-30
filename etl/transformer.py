# etl/transformer.py
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def transformar(df: pd.DataFrame, tasas: dict) -> pd.DataFrame:
    """
    Aplica todas las transformaciones al DataFrame:
    - Elimina filas inválidas
    - Normaliza tipos de datos
    - Agrega columnas calculadas con tipo de cambio
    """
    logger.info("Iniciando transformaciones...")
    filas_inicial = len(df)

    # 1. Eliminar filas con producto vacío
    df = df.dropna(subset=["producto"])
    logger.info(f"  Filas sin producto eliminadas: {filas_inicial - len(df)}")

    # 2. Eliminar filas con cantidad <= 0 (datos inválidos)
    invalidas = df[df["cantidad"] <= 0]
    if not invalidas.empty:
        logger.info(f"  Filas con cantidad inválida eliminadas: {len(invalidas)}")
        logger.info(f"    Detalle: {invalidas[['id_venta','producto','cantidad']].to_dict('records')}")
    df = df[df["cantidad"] > 0]

    # 3. Normalizar texto
    df["producto"]   = df["producto"].str.strip().str.title()
    df["categoria"]  = df["categoria"].str.strip().str.upper()
    df["vendedor"]   = df["vendedor"].str.strip()
    df["region"]     = df["region"].str.strip().str.upper()

    # 4. Convertir fecha
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
    df = df.dropna(subset=["fecha"])

    # 5. Calcular total en USD
    df["total_usd"] = (df["cantidad"] * df["precio_unitario"]).round(2)

    # 6. Agregar equivalencias con tipo de cambio de la API
    df["total_pab"] = (df["total_usd"] * tasas["USD_PAB"]).round(2)
    df["total_mxn"] = (df["total_usd"] * tasas["USD_MXN"]).round(2)
    df["total_cop"] = (df["total_usd"] * tasas["USD_COP"]).round(2)

    # 7. Columna de fecha de carga
    df["fecha_carga"] = datetime.now()

    logger.info(f"  Transformación completa. Filas listas para cargar: {len(df)}")
    return df.reset_index(drop=True)
