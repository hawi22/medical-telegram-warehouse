import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Database connection
DB_URL = "postgresql://admin:password@localhost:5435/medical_warehouse"
engine = create_engine(DB_URL)

def load_raw_json_to_db(data_path):
    all_data = []
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".json") and not file.startswith("_"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    all_data.extend(json.load(f))
    
    if not all_data:
        return

    df = pd.DataFrame(all_data)
    
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        # FIX: Manually drop the table with CASCADE to remove dependent dbt views
        conn.execute(text("DROP TABLE IF EXISTS raw.telegram_messages CASCADE;"))
    
    df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
    print(f"Successfully loaded {len(df)} records to raw.telegram_messages")

def load_yolo_to_db():
    csv_path = "data/yolo_detections.csv"
    if not os.path.exists(csv_path):
        print("YOLO CSV not found.")
        return

    df = pd.read_csv(csv_path)
    
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        # CASCADE here too just in case
        conn.execute(text("DROP TABLE IF EXISTS raw.yolo_detections CASCADE;"))
    
    df.to_sql('yolo_detections', engine, schema='raw', if_exists='replace', index=False)
    print(f"Successfully loaded YOLO results to raw.yolo_detections")

if __name__ == "__main__":
    load_raw_json_to_db("data/raw/telegram_messages")
    load_yolo_to_db()