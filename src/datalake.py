import os
import json
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def get_partition_path(base_path: str, date_str: str) -> str:
    # Path: data/raw/telegram_messages/YYYY-MM-DD/
    path = os.path.join(base_path, "raw", "telegram_messages", date_str)
    ensure_dir(path)
    return path

def write_to_json(path: str, data: List[Dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def write_manifest(base_path: str, date_str: str, stats: Dict):
    manifest_path = os.path.join(get_partition_path(base_path, date_str), "_manifest.json")
    payload = {
        "date": date_str,
        "run_at": datetime.now(timezone.utc).isoformat(),
        "channel_stats": stats,
        "total_messages": sum(stats.values())
    }
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)