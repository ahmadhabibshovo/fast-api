from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/courses",
    tags=["courses"]
)

@router.post("/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.create_course(db=db, course=course)
    return db_course

@router.get("/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    courses = crud.get_courses(db, skip=skip, limit=limit)
    return courses

@router.get("/{id}", response_model=schemas.Course)
def read_course(id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course(db, course_id=id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.patch("/{id}", response_model=schemas.Course)
def update_course(id: int, course: schemas.CourseUpdate, db: Session = Depends(get_db)):
    db_course = crud.update_course(db, course_id=id, course=course)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course

@router.delete("/{id}", response_model=schemas.Course)
def delete_course(id: int, db: Session = Depends(get_db)):
    db_course = crud.delete_course(db, course_id=id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course
