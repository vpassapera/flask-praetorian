FROM python:3.6.8-stretch

ARG port
ARG service

RUN mkdir /logs

COPY ./setup.py /app/
COPY ./.project_metadata.json /app/
COPY ./README.rst /app/
COPY ./flask_praetorian/ /app/flask_praetorian
COPY ./example/runner.py /app/

WORKDIR /app
RUN pip install .[dev]

# Note that example.py is expected to be put in place by docker-compose

CMD ["python", "example.py", "--port=5000", "--logfile=/logs/example.log"]
