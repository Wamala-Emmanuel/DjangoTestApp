FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get -y install tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM alpine
WORKDIR /app
COPY --from=builder /app .
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
