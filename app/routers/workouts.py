from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from app import models, schemas, db
from passlib.context import CryptContext
from typing import Annotated

router = APIRouter(prefix="/workouts", tags=["workouts"])
SessionDep = Annotated[AsyncSession, Depends(db.get_db)]

@router.post("/", response_model=schemas.WorkoutResponse)
def create_workout(workout: schemas.WorkoutCreate, db: SessionDep):
    new_workout = models.Workout(**workout.dict(), owner_id=1) 
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.get("/", response_model=list[schemas.WorkoutResponse])
def get_workouts(db: SessionDep):
    return db.query(models.Workout).all()

@router.delete("/", status_code=204)
def delete_workout(workout_id: int, db: SessionDep):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}
