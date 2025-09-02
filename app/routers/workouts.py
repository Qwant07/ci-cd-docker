from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from app import models, schemas, db, auth
from passlib.context import CryptContext
from sqlalchemy.orm import Session

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post("/", response_model=schemas.WorkoutResponse)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    new_workout = models.Workout(**workout.dict(), owner_id=current_user.id) 
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.get("/", response_model=list[schemas.WorkoutResponse])
def get_workouts(db: Session = Depends(db.get_db)):
    return db.query(models.Workout).all()

@router.delete("/", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(db.get_db), current_user: models.User = Depends(auth.get_current_user)):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()
    return {"message": "Workout deleted successfully"}
