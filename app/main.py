from fastapi import FastAPI
from . endpoints import dogs

app = FastAPI()
app.include_router(dogs.router, prefix="/idogsapi", tags=["breeds"])

@app.get("/")
def read_root():
    return {"message": "Welcome to IDogs API. Your favourite API for dogs content.", "documentation": "No documentation yet"}
