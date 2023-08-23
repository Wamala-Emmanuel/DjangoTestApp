from django.contrib import admin
from django.urls import path
from .views import companies, company, add_company, update_company, active_company, deactive_company

urlpatterns = [
    path('companies/', companies, name="companies"),
    path('company/<int:company_id>/', company, name="company"),
    path('add-company/', add_company, name="add_company"),
    path('update-company/<int:company_id>/', update_company, name="update_company"),
    path('active-company/<int:company_id>/', active_company, name="active_company"),
    path('deactive-company/<int:company_id>/', deactive_company, name="deactive_company"),


]