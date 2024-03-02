FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -U pip && pip install -r requirements.txt

CMD ["python", "src/main.py"]
