from fastapi import APIRouter, Depends
from utils.database import DatabaseInterface
from models.student import Student
from typing import List
from dependencies import get_db

router = APIRouter()

from fastapi import APIRouter, HTTPException
students_db = {}

@router.post("", response_model=Student)
async def create_student(student: Student, db: DatabaseInterface = Depends(get_db)) -> Student:
    db.save_student(student)
    print(db.students)
    return student

@router.get("", response_model=List[Student])
async def list_student(db: DatabaseInterface = Depends(get_db)) -> List[Student]:
    return db.list_students()

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int, db: DatabaseInterface = Depends(get_db)) -> Student:
    return db.get_student(student_id)

@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, student: Student, db: DatabaseInterface = Depends(get_db)) -> Student:    
    return db.update_student(student_id, student)

@router.delete("/{student_id}", response_model=Student)
async def delete_student(student_id: int, db:DatabaseInterface = Depends(get_db)) -> Student:
    return db.delete_student(student_id)