from app.db import engine, Base
from app import models

from fastapi import FastAPI
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    