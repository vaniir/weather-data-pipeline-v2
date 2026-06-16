# Weather Data Pipeline

## Overview

This project simulates a weather data engineering pipeline using Python, PostgreSQL, and dbt.

Weather data is generated or requested, stored as raw JSON in PostgreSQL, transformed through dbt staging and cleaning models, and aggregated into analytics-ready marts.

## Architecture

Synthetic Weather Generator or API requests
    ↓
PostgreSQL (raw_weather_data)
    ↓
dbt Staging Models
    ↓
dbt Clean Models
    ↓
Analytics Marts

## Tech Stack

- Python
- PostgreSQL
- dbt
- psycopg2
- dotenv

## Data Pipeline

### Raw Layer

Weather data is stored in PostgreSQL as JSONB payloads.

### Staging Layer

dbt staging models extract fields from JSON and apply data type conversions.

### Clean Layer

dbt cleaning models:
- standardize text fields
- validate weather measurements
- create data quality flags

### Mart Layer

Analytics-ready tables including:
- daily weather summaries
- weekly weather summaries
- city-level weather statistics

## Data Quality Checks

The pipeline validates:

- location fields
- temperature ranges
- humidity ranges
- wind measurements
- pressure values
- cloud coverage values

Validation results are stored as flags for downstream use.

## How to Run

### 1. Create environment variables

Create a `.env` file in the root directory:

```
DB_HOST=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=

OPENWEATHER_API_KEY= (only required for API ingestion mode)
```

---

### 2. Initialize database

Run the one-time database setup:

```bash
cd src
python setup_db.py
```

This creates the required tables for raw weather ingestion.

---

### 3. Ingest data (choose one option)

#### Option A (Recommended): Synthetic Data

```bash
cd scripts
python generate_synthetic_data.py
```

Generates:
- 14 cities
- hourly data
- 30 days of weather records

#### Option B: OpenWeather API ingestion

```bash
cd src
python ingestion.py
```

Pulls live weather data from OpenWeather API.

---

### 4. Run dbt transformations

```bash
cd weather_dbt
dbt run
```

This executes:
- staging models
- cleaning models
- marts

---

### 5. Run data quality tests

```bash
dbt test
```

Validates:
- null checks
- range validations
- mart-level constraints

---

### 6. Query results

Example queries:

```sql
SELECT * FROM daily_weather_mart;
SELECT * FROM weekly_weather_mart;
SELECT * FROM weather_condition_mart;
SELECT * FROM weather_summary_mart;
```

---

## Pipeline Summary

```
Ingestion (Synthetic or API)
        ↓
PostgreSQL (raw layer)
        ↓
dbt staging (JSON extraction)
        ↓
dbt cleaning (validation + standardization)
        ↓
dbt marts (analytics-ready tables)
        ↓
dbt tests (data quality validation)
```

## Future Improvements

- Additional weather data sources
- Automated orchestration
- Cloud deployment
- Advanced monitoring