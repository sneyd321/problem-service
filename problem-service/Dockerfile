FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD  [ "celery", "-A", "server.c", "worker" ]

CMD ["python", "./app.py"]

