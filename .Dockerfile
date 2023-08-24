FROM python:3.10-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update
RUN apt-get -y install tk
RUN python -m pip install --upgrade pip setuptools wheel
RUN python -m pip install cx_Oracle --upgrade
RUN pip install Django==4.2 \
    django-environ \
    django-crispy-forms \
    celery \
    django_celery_results \
    Pillow \
    unittest-xml-reporting \
    python-ldap \
    git+https://github.com/azure-samples/ms-identity-python-utilities@main
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM alpine
WORKDIR /app
COPY --from=builder ./app .
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
