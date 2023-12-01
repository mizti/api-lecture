from fastapi import APIRouter, HTTPException
from models.student import Student
import json

router = APIRouter()
students_db = {}

@router.post("", response_model=Student)
async def create_student(student: Student):
    student_id = len(students_db) + 1
    student.id = student_id
    students_db[student_id] = student
    return student

@router.get("")
async def create_student():
    res = students_db
    return res

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    return students_db[student_id]

@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: int, student: Student):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    updated_student = students_db[student_id]
    updated_student.name = student.name
    updated_student.registration_number = student.registration_number
    updated_student.email = student.email
    # 他の属性が更新される場合はここに追加
    students_db[student_id] = updated_student
    return updated_student

@router.delete("/{student_id}", response_model=Student)
async def delete_student(student_id: int):
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    deleted_student = students_db.pop(student_id)
    return deleted_student

