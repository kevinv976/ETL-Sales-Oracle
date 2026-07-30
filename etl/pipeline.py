# etl/pipeline.py
import logging
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import LOG_PATH
from etl.extractor import extraer_csv, extraer_tipo_cambio
from etl.transformer import transformar
from etl.loader import cargar_datos, registrar_log

# ── Configuración de logging ──────────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
        logging.StreamHandler(),          # también muestra en consola
    ]
)
logger = logging.getLogger("pipeline")


def ejecutar_pipeline():
    logger.info("=" * 55)
    logger.info("  ETL-Sales Oracle — inicio del pipeline")
    logger.info("=" * 55)
    inicio = time.time()

    try:
        # ── EXTRACT ──────────────────────────────────────────────
        df_ventas = extraer_csv()
        tasas     = extraer_tipo_cambio()

        # ── TRANSFORM ────────────────────────────────────────────
        df_limpio = transformar(df_ventas, tasas)

        # ── LOAD ─────────────────────────────────────────────────
        resumen = cargar_datos(df_limpio)

        duracion = time.time() - inicio
        registrar_log(resumen, duracion)

        logger.info("=" * 55)
        logger.info(f"  Pipeline finalizado en {duracion:.1f}s")
        logger.info(f"  Filas cargadas : {resumen['exitosas']}")
        logger.info(f"  Filas con error: {resumen['errores']}")
        logger.info("=" * 55)

    except Exception as e:
        logger.critical(f"Pipeline abortado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    ejecutar_pipeline()
