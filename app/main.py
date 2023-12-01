from fastapi import FastAPI
from routes import student_routes #, lecture_routes, attendance_routes

app = FastAPI()

app.include_router(student_routes.router, prefix="/students", tags=["students"])

@app.get("/hello")
async def hello():
    return "Hello!"

# app.include_router(lecture_routes.router, prefix="/lectures", tags=["lectures"])

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])
