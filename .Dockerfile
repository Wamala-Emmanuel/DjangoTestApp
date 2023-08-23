FROM python:3.10-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get -y install python3.10-tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM alpine
WORKDIR /app
COPY --from=builder ./app .
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
