from fastapi import FastAPI, Depends
from routes import student_routes #, lecture_routes, attendance_routes
#from utils.database import MemoryDatabase, MySQLDatabase
#import os
from dependencies import get_db

app = FastAPI(debug=True)

app.include_router(
    student_routes.router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_db)]
)

@app.get("/hello")
async def hello():
    print("here is hello")
    return "Hello!"

# app.include_router(lecture_routes.router, prefix="/lectures", tags=["lectures"])

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])
