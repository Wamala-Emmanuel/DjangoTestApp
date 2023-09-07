FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apk update && apk add tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
