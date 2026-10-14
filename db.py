"""MySQL helper. Credentials are read from the .env file (never hard-coded)."""
import os, mysql.connector
from dotenv import load_dotenv
load_dotenv()
CFG = dict(host=os.getenv("DB_HOST", "localhost"), user=os.getenv("DB_USER", "root"),
           password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME", "eco_pricing"))
if not CFG["password"]:
    raise RuntimeError("DB_PASSWORD missing. Copy .env.example to .env and fill in your MySQL password.")

def run(sql, params=None, many=False, fetch=False):
    con = mysql.connector.connect(**CFG); cur = con.cursor(dictionary=True)
    try:
        (cur.executemany if many else cur.execute)(sql, params or ())
        rows = cur.fetchall() if fetch else None
        con.commit(); return rows
    finally:
        cur.close(); con.close()