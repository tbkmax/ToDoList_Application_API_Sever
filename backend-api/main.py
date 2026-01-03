from fastapi import FastAPI
from api.api_v1 import api_router

app = FastAPI(title="ToDo List API", version="1.0.0")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}