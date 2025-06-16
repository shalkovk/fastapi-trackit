FROM python:3.11.1

WORKDIR /app


COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["python", "main.py"]