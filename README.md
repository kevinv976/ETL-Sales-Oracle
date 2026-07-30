# ETL-Sales Oracle

Pipeline ETL que extrae datos de ventas desde un archivo CSV y una API pública,
los transforma con Pandas y los carga en Oracle mediante stored procedures.

## Estructura

```
etl_sales_oracle/
├── data/
│   └── ventas.csv          # Datos de origen (CSV)
├── etl/
│   ├── extractor.py        # Extracción desde CSV y API
│   ├── transformer.py      # Limpieza y normalización
│   ├── loader.py           # Carga a Oracle
│   └── pipeline.py         # Orquestador principal
├── sql/
│   ├── create_tables.sql   # Tablas destino
│   └── procedures.sql      # Stored procedures de carga
├── logs/                   # Logs generados automáticamente
├── config.py               # Configuración de conexión
├── requirements.txt
└── README.md
```

## Requisitos

```bash
pip install -r requirements.txt
```

## Configuración

Copia `.env.example` como `.env` y coloca ahí tus credenciales Oracle reales:

```bash
cp .env.example .env
```

El archivo `.env` no se sube a GitHub (está en `.gitignore`). `config.py` lee
las credenciales desde ahí usando `python-dotenv`.

## Ejecución

```bash
python etl/pipeline.py
```

## Tecnologías

- Python 3.10+
- oracledb (driver Oracle oficial)
- Pandas (transformación)
- Requests (API pública)
- Oracle SQL + PL/SQL
