from prefect import flow, task, get_run_logger
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INGESTION_DIR = PROJECT_ROOT / "src"
DBT_DIR = PROJECT_ROOT / "weather_dbt"

print(f"Project root: {PROJECT_ROOT}")
print(f"Ingestion directory: {INGESTION_DIR}")
print(f"DBT directory: {DBT_DIR}")
print(f"Python executable: {sys.executable}")

@task(retries=3, retry_delay_seconds=300)
def run_ingestion_script():
    logger = get_run_logger()

    try:
        logger.info("Starting ingestion")

        subprocess.run(
            [sys.executable, "ingestion.py"],
            cwd=INGESTION_DIR,
            check=True
        )

        logger.info("Ingestion successful")

    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise


@task(retries=2, retry_delay_seconds=120)
def run_dbt_models():
    logger = get_run_logger()

    try:
        logger.info("Dbt Starting")

        subprocess.run(
            ["dbt", "run"],
            cwd=DBT_DIR,
            check=True
        )

        logger.info("Dbt successful")
    
    except Exception as e:
        logger.error(f"Dbt failed: {e}")
        raise

@task(retries=1, retry_delay_seconds=60)
def run_dbt_tests():
    logger = get_run_logger()

    try:
        logger.info("Testing")

        subprocess.run(
            ["dbt", "test"],
            cwd=DBT_DIR,
            check=True
        )

        logger.info("All test passed")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

@flow
def weather_pipeline():
    logger = get_run_logger()

    logger.info("Starting weather pipeline")

    run_ingestion_script()
    run_dbt_models()
    run_dbt_tests()

    logger.info("Weather pipeline completed")

if __name__ == "__main__":
    weather_pipeline()