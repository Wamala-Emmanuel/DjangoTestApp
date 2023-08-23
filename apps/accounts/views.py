import profile
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
# from .models import User
from apps.documents.models import Document
from django.contrib.auth.models import User

from email import message
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileForm
from .models import Profile
import csv
from django.contrib import messages
# from helpers.ldap_authentication import ldap_authentication
from helpers.audit_log import audit_log
# from apps.activity_logs.models import ActivityLog
import logging
import datetime
import os
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

logname = 'test-' + str(datetime.date.today()) +'.log'
# logfile = os.path.join(os.pardir, logname)

logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

# logger.info('Start reading database')

def users(request):
    users = User.objects.all().order_by('-date_joined')
    number_of_users = users.count()

    page = request.GET.get('page', 1)

    query = request.GET.get("q")

    if query:
        users = users.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(email__icontains=query) 
        )

    paginator = Paginator(users, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'account/users.html', {
        'users': users,
        'number_of_users': number_of_users
    })

def user(request, user_id):

    user = get_object_or_404(User, id=user_id)
    documents = Document.objects.all()
    return render(request, 'account/user.html', {
        'user': user,
        'documents': documents
    })

def activate_user(request, user_id):
    user = User.objects.filter(id=user_id)
    profile = Profile.objects.filter(user = user.first())
    user.update(is_active=True)
    profile.update(
        approved_by = request.user, 
        approved_date = datetime.datetime.now(), 
        active=True
    )

    messages.success(request, "User Activated Successfully")
    return HttpResponseRedirect("/users/")

def deactivate_user(request, user_id):
    user = User.objects.filter(id=user_id)
    profile = Profile.objects.filter(user = user.first())
    user.update(is_active=False)
    profile.update(deactivated_by = request.user, deactivated_date=datetime.datetime.now(), active=False,)

    messages.success(request, "User Deactivated Successfully")
    return HttpResponseRedirect("/users/")

@login_required
def edit(request, user_id):
    user = User.objects.filter(id=user_id)
    profile = Profile.objects.filter(user = user.first())


    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = user.first())
        profile_form = ProfileForm(request.POST, instance = profile.first())

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()

            cd = form.cleaned_data
            profile_cd = profile_form.cleaned_data

            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            role = profile_cd['role']
            address = profile_cd['address']
            company = profile_cd['company']

            request_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'role': role
            }

            messages.success(request, 'User edited successfully')
            return HttpResponseRedirect("/users")   
    else:
        form = UserEditForm(instance = user.first())
        profile_form = ProfileForm(instance = profile.first())

    return render(request,'account/edit.html',{
        'profile_form': profile_form,
        'form': form
    })

def export_users(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'SAP Number', 'Branch', 'Role', 'Active', 'Approved', 'Approved By', 'Date Approved', 'Deactivated By', 'Date Deactivated', 'Date Created'])
    
    users = Profile.objects.all().values_list('fname', 'lname', 'username', 'branch', 'role', 'active', 'approved', 'approvedby', 'dateapproved', 'deactivatedby', 'datedeactivated', 'timecreated')
    
    for user in users:
        writer.writerow(user)
        
    return response

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']

            user = User.objects.filter(username=username)

            if user:
                user = user.first()
                if user.is_active:
                    # authentication = ldap_authentication(cd['username'], cd['password'])
                    # if(authentication['status']):
                    #     user.backend = 'django.contrib.auth.backends.ModelBackend'
                    #     login(request, user)
                    #     return HttpResponseRedirect("/upload_credit_score/")
                    # else:
                    #     messages.success(request, authentication['error'])
                    #     return HttpResponseRedirect("/login")
                    login(request, user)
                    if user.profile.role.name == 'SuperUser':
                        return HttpResponseRedirect("/users/")
                    else:
                        return HttpResponseRedirect("/documents/")

                else:
                    messages.error(request, 'User is not active')
                    return HttpResponseRedirect("/")
            else:
                messages.error(request, 'User not found')
                return HttpResponseRedirect("/")
                
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def add_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            username = cd['username']
            first_name = cd['first_name']
            last_name = cd['last_name']
            email = cd['email']
            role = cd['role']
            address = cd['address']
            company = cd['company']

            try:
                register = User.objects.create(
                    username = username, 
                    first_name = first_name, 
                    last_name = last_name, 
                    email = email,
                    is_active = False,
                    )

                Profile(user=register, role=role, added_by=request.user, company=company, address=address,).save()

                request_data = {
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'role': role
                }

                messages.success(request, "User registered successfully")
                return HttpResponseRedirect("/users")

            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect("/add_user")

    else:
        form = UserRegistrationForm()
        
    return render(request,'account/add_user.html',{
        'form': form,
        'sidebar': 'users',
    })


