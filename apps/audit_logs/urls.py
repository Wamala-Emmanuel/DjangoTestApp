from django.contrib import admin
from django.urls import path
from .views import audit_logs

urlpatterns = [
    path('audit_logs/', audit_logs, name="audit_logs"),
]