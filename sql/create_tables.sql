-- sql/create_tables.sql
-- Ejecutar en SQL Developer como usuario HR (o el usuario que uses)

-- Tabla principal de ventas
CREATE TABLE VENTAS_ETL (
    id_venta        NUMBER          PRIMARY KEY,
    fecha           DATE            NOT NULL,
    producto        VARCHAR2(100)   NOT NULL,
    categoria       VARCHAR2(50),
    cantidad        NUMBER(10)      NOT NULL,
    precio_unitario NUMBER(10, 2)   NOT NULL,
    total_usd       NUMBER(12, 2),
    total_pab       NUMBER(12, 2),
    vendedor        VARCHAR2(100),
    region          VARCHAR2(50),
    fecha_carga     DATE            DEFAULT SYSDATE
);

-- Tabla de log del ETL
CREATE TABLE ETL_LOG (
    id_log          NUMBER          GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fecha_ejecucion DATE            DEFAULT SYSDATE,
    filas_cargadas  NUMBER,
    filas_error     NUMBER,
    duracion_seg    NUMBER(8, 2),
    estado          VARCHAR2(20)    CHECK (estado IN ('OK', 'PARCIAL', 'ERROR'))
);

-- Vista resumen de ventas por región y categoría
CREATE OR REPLACE VIEW V_VENTAS_RESUMEN AS
SELECT
    region,
    categoria,
    COUNT(*)            AS total_transacciones,
    SUM(cantidad)       AS unidades_vendidas,
    SUM(total_usd)      AS ingresos_usd,
    ROUND(AVG(total_usd), 2) AS promedio_venta_usd
FROM VENTAS_ETL
GROUP BY region, categoria
ORDER BY ingresos_usd DESC;
