FROM python:3.10-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
