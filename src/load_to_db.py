import os
import json
import pandas as pd
from sqlalchemy import create_engine, text  # Import 'text'
from dotenv import load_dotenv

load_dotenv()

# Database connection - using port 5435 as we set earlier
DB_URL = "postgresql://admin:password@localhost:5435/medical_warehouse"
engine = create_engine(DB_URL)

def load_raw_json_to_db(data_path):
    all_data = []
    
    # Walk through the data lake
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".json") and not file.startswith("_"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    all_data.extend(json.load(f))
    
    if not all_data:
        print("No JSON data found in the specified path.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # FIX: Use engine.begin() and text() for SQLAlchemy 2.0
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    
    # Load to PostgreSQL
    df.to_sql('telegram_messages', engine, schema='raw', if_exists='replace', index=False)
    print(f"Successfully loaded {len(df)} records to raw.telegram_messages")

if __name__ == "__main__":
    load_raw_json_to_db("data/raw/telegram_messages")