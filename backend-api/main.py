from fastapi import FastAPI
from api.api_v1 import api_router
from fastapi.responses import RedirectResponse

app = FastAPI(title="ToDo List API", version="0.0.1")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/version")
def get_version():
    return {"version": app.version}