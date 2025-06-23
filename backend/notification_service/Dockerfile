FROM python:3.11.1

WORKDIR /app


COPY requirements.txt .

COPY wait-for-rabbitmq.sh /wait-for-rabbitmq.sh

RUN apt-get update && apt-get install -y netcat

RUN pip install --no-cache -r requirements.txt

COPY . .

RUN chmod +x /wait-for-rabbitmq.sh

COPY wait-for-rabbitmq.sh /wait-for-rabbitmq.sh

ENTRYPOINT ["/wait-for-rabbitmq.sh"]

CMD ["python", "main.py"]