FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && rm -rf /var/lib/apt/lists/*
RUN apt-get -y install python3.10-tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
