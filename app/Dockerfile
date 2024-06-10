FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# for debug: use with --progress=plain --no-cache
#RUN pwd
#RUN ls

COPY . /code

ENV PYTHONPATH=/code
ENV OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
