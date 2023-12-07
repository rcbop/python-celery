FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY report.py /app
COPY disney.html.j2 /app/

ENTRYPOINT [ "python" ]
CMD ["-m", "celery", "-A", "report", "worker", "--loglevel=info"]
