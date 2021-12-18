FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD  [ "celery", "-A", "server.c", "worker", "--autoscale=10,4", "--pool=solo" ]

CMD ["python", "./app.py"]

