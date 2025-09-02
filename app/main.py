from app.db import engine, Base
from app import models
from app.routers import users, workouts
from fastapi import FastAPI
import uvicorn

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(workouts.router)

@app.get("/")
def root():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
    