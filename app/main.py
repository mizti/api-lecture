from fastapi import FastAPI, Depends
from routes import student_routes, lecture_routes
#from utils.database import MemoryDatabase, MySQLDatabase
#import os
from dependencies import get_db, get_student_db, get_lecture_db

app = FastAPI(debug=True)

app.include_router(
    student_routes.router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_student_db)]
)

@app.get("/hello")
async def hello():
    print("here is hello")
    return "Hello!"

app.include_router(
    lecture_routes.router,
    prefix="/lectures",
    tags=["lectures"],
    dependencies=[Depends(get_lecture_db)]
)

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])
