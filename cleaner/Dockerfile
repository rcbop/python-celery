FROM python:3.8

WORKDIR /app

RUN pip install schedule

COPY cleaner/cleaner.py /app

ENTRYPOINT [ "python" ]
CMD ["cleaner.py"]
