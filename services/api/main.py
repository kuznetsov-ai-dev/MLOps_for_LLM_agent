# /services/api/main.py
# путь: /services/api/main.py
from fastapi import FastAPI

app = FastAPI(title="rossmann-api")


@app.get("/health")
def health():
    return {"status": "ok"}
