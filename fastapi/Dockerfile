FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./fastapi /app
COPY ./report.py /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
