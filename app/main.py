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
from opentelemetry.trace import StatusCode, Status

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
import logging

# Open Telemetry Settings
resource = Resource(attributes={"service.name": "fastapi-service"})
#resource = Resource.create({"service.name": "fastapi-service"})
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# OTLP Log Settings
log_provider = LoggerProvider(resource=resource)
set_logger_provider(log_provider)
log_exporter = OTLPLogExporter(endpoint="localhost:4317", insecure=True)
log_processor = BatchLogRecordProcessor(log_exporter)
log_provider.add_log_record_processor(log_processor)
logging_handler = LoggingHandler(level=logging.INFO)

logging.getLogger().addHandler(logging_handler)
logging.getLogger().setLevel(logging.INFO)

app = FastAPI(debug=True)
app.include_router(
    student_routes.router,
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_student_db)]
)
FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)

@app.get("/hello")
async def hello():
    with tracer.start_as_current_span("hello-span") as span:
        span.set_attribute("custom-attribute", "value")
        span.add_event("start-processing hello")

        logging.info("Processing /hello request")
        print("here is hello")
        span.add_event("end-processing")
        span.set_status(Status(StatusCode.OK))

        return "Hello!"
    
# app.include_router(lecture_routes.router, prefix="/lectures", tags=["lectures"])

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])
