FROM python:3.11.1

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt ./

RUN pip install --no-cache -r requirements.txt

COPY wait-for-rabbitmq.sh /app/wait-for-rabbitmq.sh

RUN chmod +x /app/wait-for-rabbitmq.sh

COPY . .

CMD ["/app/wait-for-rabbitmq.sh", "python", "main.py"]