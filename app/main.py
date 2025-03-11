from fastapi import FastAPI, Depends
from routes import student_routes, lecture_routes
#from utils.database import MemoryDatabase, MySQLDatabase
#import os
from dependencies import get_db, get_student_db, get_lecture_db

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Set up OpenTelemetry
trace.set_tracer_provider(TracerProvider())
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = FastAPI(debug=True)
FastAPIInstrumentor.instrument_app(app)

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
