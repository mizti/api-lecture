from fastapi import APIRouter, Depends, HTTPException
from utils.database import DatabaseInterface
from models.lecture import Lecture, UpdateLecture
from typing import List
from dependencies import get_lecture_db

router = APIRouter()
lectures_db = {}

@router.post("", response_model=Lecture)
async def create_lecture(lecture: Lecture, db: DatabaseInterface = Depends(get_lecture_db)) -> Lecture:
    db.save_item(lecture)
    return lecture

@router.get("", response_model=List[Lecture])
async def list_lecture(db: DatabaseInterface = Depends(get_lecture_db)) -> List[Lecture]:
    return db.list_items()

@router.get("/{lecture_id}", response_model=Lecture)
async def get_lecture(lecture_id: int, db: DatabaseInterface = Depends(get_lecture_db)) -> Lecture:
    return db.get_item(lecture_id)

@router.put("/{lecture_id}", response_model=Lecture)
async def update_lecture(lecture_id: int, update_lecture: UpdateLecture, db: DatabaseInterface = Depends(get_lecture_db)):
    updated_lecture = db.update_item(lecture_id, update_lecture)
    if updated_lecture is None:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return updated_lecture

@router.delete("/{lecture_id}", response_model=Lecture)
async def delete_lecture(lecture_id: int, db: DatabaseInterface = Depends(get_lecture_db)) -> Lecture:
    return db.delete_item(lecture_id)
