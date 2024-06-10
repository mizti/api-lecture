from fastapi import FastAPI, Depends
from routes import student_routes #, lecture_routes, attendance_routes
#from utils.database import MemoryDatabase, MySQLDatabase
#import os
from dependencies import get_db, get_student_db

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace

resource = Resource(attributes={
    "service.name": "fastapi-service"
})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)


app = FastAPI(debug=True)

app.include_router(
    student_routes.router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_student_db)]
)
FastAPIInstrumentor.instrument_app(app)

@app.get("/hello")
async def hello():
    print("here is hello")
    return "Hello!"

# app.include_router(lecture_routes.router, prefix="/lectures", tags=["lectures"])

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])
