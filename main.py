from fastapi import FastAPI
from src.routes import contacts

app = FastAPI()

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Contact Manager API"}
