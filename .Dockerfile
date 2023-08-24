FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update
RUN apt-get -y install tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
