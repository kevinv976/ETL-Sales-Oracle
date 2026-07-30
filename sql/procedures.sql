-- sql/procedures.sql
-- Stored procedure que recibe una fila de venta y la inserta o actualiza

CREATE OR REPLACE PROCEDURE SP_CARGAR_VENTA (
    p_id_venta        IN NUMBER,
    p_fecha           IN DATE,
    p_producto        IN VARCHAR2,
    p_categoria       IN VARCHAR2,
    p_cantidad        IN NUMBER,
    p_precio_unitario IN NUMBER,
    p_total_usd       IN NUMBER,
    p_total_pab       IN NUMBER,
    p_vendedor        IN VARCHAR2,
    p_region          IN VARCHAR2,
    p_fecha_carga     IN DATE
) AS
    v_existe NUMBER;
BEGIN
    -- Verificar si el registro ya existe (UPSERT manual)
    SELECT COUNT(*) INTO v_existe
    FROM VENTAS_ETL
    WHERE id_venta = p_id_venta;

    IF v_existe = 0 THEN
        -- INSERT si es nuevo
        INSERT INTO VENTAS_ETL (
            id_venta, fecha, producto, categoria,
            cantidad, precio_unitario, total_usd, total_pab,
            vendedor, region, fecha_carga
        ) VALUES (
            p_id_venta, p_fecha, p_producto, p_categoria,
            p_cantidad, p_precio_unitario, p_total_usd, p_total_pab,
            p_vendedor, p_region, p_fecha_carga
        );
    ELSE
        -- UPDATE si ya existe
        UPDATE VENTAS_ETL SET
            fecha           = p_fecha,
            producto        = p_producto,
            categoria       = p_categoria,
            cantidad        = p_cantidad,
            precio_unitario = p_precio_unitario,
            total_usd       = p_total_usd,
            total_pab       = p_total_pab,
            vendedor        = p_vendedor,
            region          = p_region,
            fecha_carga     = p_fecha_carga
        WHERE id_venta = p_id_venta;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        -- Relanza el error para que Python lo capture y lo registre
        RAISE;
END SP_CARGAR_VENTA;
/
