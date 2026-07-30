# etl/loader.py
import oracledb
import pandas as pd
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DB_CONFIG

logger = logging.getLogger(__name__)


def obtener_conexion():
    """Crea y retorna una conexión a Oracle."""
    conn = oracledb.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dsn=DB_CONFIG["dsn"]
    )
    return conn


def cargar_datos(df: pd.DataFrame) -> dict:
    """
    Carga el DataFrame transformado a Oracle.
    Usa el stored procedure SP_CARGAR_VENTA para cada fila,
    garantizando la lógica de negocio en la base de datos.
    Retorna un resumen del resultado.
    """
    exitosas = 0
    errores = 0
    conn = None

    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        logger.info(f"Conexión Oracle establecida. Cargando {len(df)} filas...")

        for _, fila in df.iterrows():
            try:
                # Llamada al stored procedure (definido en sql/procedures.sql)
                cursor.callproc("SP_CARGAR_VENTA", [
                    int(fila["id_venta"]),
                    fila["fecha"].to_pydatetime(),
                    str(fila["producto"]),
                    str(fila["categoria"]),
                    int(fila["cantidad"]),
                    float(fila["precio_unitario"]),
                    float(fila["total_usd"]),
                    float(fila["total_pab"]),
                    str(fila["vendedor"]),
                    str(fila["region"]),
                    fila["fecha_carga"].to_pydatetime(),
                ])
                exitosas += 1

            except oracledb.DatabaseError as e:
                errores += 1
                logger.error(f"  Error en fila id_venta={fila['id_venta']}: {e}")

        conn.commit()
        logger.info(f"Carga finalizada. Exitosas: {exitosas} | Errores: {errores}")

    except oracledb.DatabaseError as e:
        logger.critical(f"No se pudo conectar a Oracle: {e}")
        raise
    finally:
        if conn:
            conn.close()

    return {"exitosas": exitosas, "errores": errores}


def registrar_log(resumen: dict, duracion_seg: float):
    """Guarda un registro del resultado del ETL en la tabla ETL_LOG de Oracle."""
    conn = None
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ETL_LOG
                (fecha_ejecucion, filas_cargadas, filas_error, duracion_seg, estado)
            VALUES
                (SYSDATE, :1, :2, :3, :4)
        """, [
            resumen["exitosas"],
            resumen["errores"],
            round(duracion_seg, 2),
            "OK" if resumen["errores"] == 0 else "PARCIAL"
        ])
        conn.commit()
        logger.info("Registro guardado en ETL_LOG.")
    except Exception as e:
        logger.warning(f"No se pudo guardar en ETL_LOG: {e}")
    finally:
        if conn:
            conn.close()
