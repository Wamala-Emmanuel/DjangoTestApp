FROM python:3.10-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN apk add --update --no-cache \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    libjpeg-dev \
    libpq-dev \
    libjpeg8-dev \
    liblcms2-dev \
    libblas-dev \
    libatlas-base-dev \
    python-ldap \
    tk
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM alpine
WORKDIR /app
COPY --from=builder ./app .
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
