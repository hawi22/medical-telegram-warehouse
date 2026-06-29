from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db

app = FastAPI(title="Medical Telegram Analytical API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Telegram Analytics API"}

# Endpoint 1 — Top Products (Terms)
@app.get("/api/reports/top-products")
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    # This query finds frequently mentioned words in medical channel messages
    # Excluding common stop words for better results
    query = text("""
        WITH words AS (
            SELECT regexp_split_to_table(lower(message_text), '\s+') as word
            FROM public_marts.fct_messages
            WHERE length(message_text) > 5
        )
        SELECT word, count(*) 
        FROM words 
        WHERE length(word) > 4 
          AND word NOT IN ('price', 'order', 'medicine', 'phone', 'contact')
        GROUP BY 1 
        ORDER BY 2 DESC 
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"product_term": r[0], "mentions": r[1]} for r in result]

# Endpoint 2 — Channel Activity
@app.get("/api/channels/{channel_name}/activity")
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT total_posts, avg_views, first_post_date, last_post_date 
        FROM public_marts.dim_channels 
        WHERE channel_name ILIKE :name
    """)
    r = db.execute(query, {"name": f"%{channel_name}%"}).fetchone()
    if not r:
        return {"error": "Channel not found"}
    return {
        "channel": channel_name,
        "total_posts": r[0],
        "average_views": round(r[1], 2),
        "active_since": r[2],
        "latest_post": r[3]
    }

# Endpoint 3 — Message Search
@app.get("/api/search/messages")
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    sql = text("""
        SELECT channel_name, message_text, view_count 
        FROM public_marts.fct_messages 
        WHERE message_text ILIKE :q 
        LIMIT :limit
    """)
    result = db.execute(sql, {"q": f"%{query}%", "limit": limit}).fetchall()
    return [{"channel": r[0], "text": r[1], "views": r[2]} for r in result]

# Endpoint 4 — Visual Content Stats (from YOLO)
@app.get("/api/reports/visual-content")
def get_visual_stats(db: Session = Depends(get_db)):
    query = text("""
        SELECT image_category, COUNT(*), ROUND(AVG(view_count), 2) 
        FROM public_marts.fct_image_detections 
        GROUP BY 1
    """)
    result = db.execute(query).fetchall()
    return [{"category": r[0], "count": r[1], "avg_views": r[2]} for r in result]