from dagster import asset, Definitions, AssetExecutionContext
import subprocess
import os
import sys # Added this

# Get the path to the current python interpreter
PYTHON_PATH = sys.executable

@asset(group_name="medical_pipeline")
def telegram_raw_data(context: AssetExecutionContext):
    """Task 1: Scraping Telegram"""
    context.log.info("Starting Telegram Scraper...")
    subprocess.run([PYTHON_PATH, "src/scraper.py"], check=True)

@asset(deps=[telegram_raw_data], group_name="medical_pipeline")
def raw_postgres_tables(context: AssetExecutionContext):
    """Task 2: Loading JSON/CSV to Postgres"""
    context.log.info("Loading data into Postgres...")
    subprocess.run([PYTHON_PATH, "src/load_to_db.py"], check=True)

@asset(deps=[telegram_raw_data], group_name="medical_pipeline")
def yolo_enrichment_data(context: AssetExecutionContext):
    """Task 3: Running YOLOv8 on images"""
    context.log.info("Running YOLOv8 Detection...")
    subprocess.run([PYTHON_PATH, "src/yolo_detect.py"], check=True)

@asset(deps=[raw_postgres_tables, yolo_enrichment_data], group_name="medical_pipeline")
def dbt_transformed_models(context: AssetExecutionContext):
    """Task 2: Running dbt Transformations"""
    dbt_dir = os.path.join(os.getcwd(), "medical_warehouse")
    # Using 'dbt' directly usually works if it's in your PATH
    subprocess.run(["dbt", "run", "--profiles-dir", "."], cwd=dbt_dir, check=True)

defs = Definitions(
    assets=[telegram_raw_data, raw_postgres_tables, yolo_enrichment_data, dbt_transformed_models]
)