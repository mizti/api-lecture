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
from opentelemetry import trace, metrics
from opentelemetry.trace import StatusCode, Status

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry._logs import set_logger_provider
import logging

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

def init_metrics(meter):
    # Recommendations counter
    app_hello_counter = meter.create_counter(
        'app_hello_counter', unit='helo', description="Counts the total number of given greetings"
    )
    rec_svc_metrics = {
        "app_hello_counter": app_hello_counter,
    }
    return rec_svc_metrics

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

# OTLP Metrics Settings
metric_reader1 = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="localhost:4317", insecure=True), export_interval_millis=5000)

metric_reader2 = PeriodicExportingMetricReader(ConsoleMetricExporter(), export_interval_millis=5000)
metrics_provider = MeterProvider(resource=resource, metric_readers=[metric_reader1, metric_reader2])
metrics.set_meter_provider(metrics_provider)
meter = metrics_provider.get_meter(__name__)
rec_svc_metrics = init_metrics(meter)

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
        rec_svc_metrics["app_hello_counter"].add(1, {'greeting.type': 'hello'})
        print("here is hello")
        span.add_event("end-processing")
        span.set_status(Status(StatusCode.OK))

        return "Hello!"
    
# app.include_router(lecture_routes.router, prefix="/lectures", tags=["lectures"])

# app.include_router(attendance_routes.router, prefix="/lectures/{lectureId}/students", tags=["attendances"])

