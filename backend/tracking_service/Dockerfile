FROM python:3.11.1

WORKDIR /app

COPY . /app

COPY wait-for-it.sh /wait-for-it.sh

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]