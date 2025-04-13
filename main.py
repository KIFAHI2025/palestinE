from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "pdf_index.db"

@app.get("/search")
def search(query: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    try:
        c.execute("SELECT name FROM pdfs WHERE content LIKE ?", ('%' + query + '%',))
        results = c.fetchall()
        download_url = "https://mega.nz/folder/yMU1nAiJ#L2_C5FWjqobyUuQV6NQplQ" 
        return [{"name": result[0], "download_link": download_url} for result in results]

    except Exception as e:
        return {"error": str(e)}

    finally:
        conn.close()
