from datetime import datetime
import imp
import json
from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from .models import Company
from apps.documents.models import Document, Category
from .forms import CompanyForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from apps.audit_logs.models import AuditLog
import json
from apps.accounts.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def deactive_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    Company.objects.filter(id=company_id).update(
        is_approved=False, 
        is_deactivated = True ,
        deactivated_by=request.user, 
        deactivated_date=datetime.now())
    
    description = str(request.user.first_name) + " " + str(request.user.last_name) + " deactivated company " + str(company) 
    http_method = request.method
    activity_type = "deactivate_company"
    url = request.get_full_path()
    request_body = {
        'company_id': company_id
    }

    activity_log = AuditLog(
        activity_type = activity_type,
        http_method = http_method,
        description = description,
        url = url,
        added_by = request.user,
        request_body = request_body
    )
    activity_log.save()

    messages.success(request, 'Company Deactivated Successfully')
    return HttpResponseRedirect("/companies/")

def active_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    Company.objects.filter(id=company_id).update(
        is_approved=True, 
        approved_by=request.user, 
        approved_date=datetime.now(),
        is_deactivated = False)

    description = str(request.user.first_name) + " " + str(request.user.last_name) + " activated company " + str(company) 
    http_method = request.method
    activity_type = "activate_company"
    url = request.get_full_path()
    request_body = {
        'company_id': company_id
    }

    activity_log = AuditLog(
        activity_type = activity_type,
        http_method = http_method,
        description = description,
        url = url,
        added_by = request.user,
        request_body = request_body
    )
    activity_log.save()

    messages.success(request, 'Company Activated Successfully')
    return HttpResponseRedirect("/companies/")

def companies(request):
    companies = Company.objects.all().order_by('-created')
    number_of_companies = companies.count()
    page = request.GET.get('page', 1)

    query = request.GET.get("q")

    if query:
        companies = companies.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) 
        )

    paginator = Paginator(companies, 10)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)

    return render(request, 'companies/companies.html', {
        'companies': companies,
        'number_of_companies': number_of_companies
    })

def company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    documents = Document.objects.filter()
    categories = Category.objects.all()
    users = Profile.objects.filter(company=company)

    return render(request, 'companies/company.html', {
        'company': company,
        'users': users,
        'documents': documents,
        'categories': categories
    })

def add_company(request):
    form = CompanyForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.added_by = request.user
            instance.save()

            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            logo = form.cleaned_data['logo']

            description = str(request.user.first_name) + " " + str(request.user.last_name) + " added new company "
            http_method = request.method
            activity_type = "add_company"
            url = request.get_full_path()
            request_body = {
                'name': name, 
                'address': address, 
                'email': email, 
                'phone': phone, 
                'logo': logo
            }

            activity_log = AuditLog(
                activity_type = activity_type,
                http_method = http_method,
                description = description,
                url = url,
                added_by = request.user,
                request_body = request_body
            )
            activity_log.save()

            messages.success(request, "Company added Successsfully")
            return HttpResponseRedirect("/companies/")

    context = {
        'form': form
    }

    return render(request, 'companies/add_company.html', context)

def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    company_name = company.name
    form = CompanyForm(request.POST or None, request.FILES or None, instance=company)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            logo = form.cleaned_data['logo']

            description = str(request.user.first_name) + " " + str(request.user.last_name) + " updated " + str(company_name)
            http_method = request.method
            activity_type = "add_company"
            url = request.get_full_path()
            request_body = {
                'name': name, 
                'address': address, 
                'email': email, 
                'phone': phone, 
                'logo': logo
            }

            activity_log = AuditLog(
                activity_type = activity_type,
                http_method = http_method,
                description = description,
                url = url,
                added_by = request.user,
                request_body = request_body
            )
            activity_log.save()

            messages.success(request, company.name + " updated successfully")
            return HttpResponseRedirect("/companies/")

    context = {
        'form': form
    }

    return render(request, 'companies/update_company.html', context)