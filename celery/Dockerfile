FROM python:3.8

WORKDIR /app

COPY ./celery/requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY report.py /app
COPY disney.html.j2 /app/

CMD ["celery", "-A", "report", "worker", "--loglevel=info"]
