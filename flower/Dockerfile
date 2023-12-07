FROM python:3.8

WORKDIR /app

COPY ./flower/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir flower

COPY report.py /app

ENTRYPOINT [ "python" ]
CMD ["-m", "celery", "--broker=pyamqp://guest:guest@rabbitmq//", "--app=report", "flower"]
