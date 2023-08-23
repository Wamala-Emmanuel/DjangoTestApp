from multiprocessing import context
from tkinter import NO
from unicodedata import category
from django.shortcuts import render, get_object_or_404
from .models import Document, Category, RejectedDocument, File
from .forms import DocumentForm, CategoryForm, RejectForm, RejectedDocumentForm, AssignSignatoryForm, SignatoryForm, DocumentFileForm, SignatorySignedForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.core.mail import send_mail
from apps.audit_logs.models import AuditLog
from helpers.tasks import send_notification_mail
from helpers.sending_email import sending_email
import smtplib


def delete_category(request, category_id):
    Category.objects.filter(id=category_id).delete()
    messages.success(request, "Document Category Deleted Successfully")
    return HttpResponseRedirect("/document-categories") 

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=category)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.added_by = request.user
            instance.save()
            messages.success(request, "Document Category Updates Successfully")
            return HttpResponseRedirect("/document-categories")

    context = {
        'form': form
    }
    
    return render(request, 'documents/update_document_category.html', context)
    
def document_categories(request):
    categories = Category.objects.all().order_by('-created')
    
    page = request.GET.get('page', 1)

    paginator = Paginator(categories, 10)
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories
    }

    return render(request, 'documents/categories.html', context)

def documents(request):

    # mail = 'otimtonyjeff@gmail.com'
    # message = 'Testing testing testing'
    
    # send_notification_mail.delay(mail, message)

    page = request.GET.get('page', 1)
    categories = Category.objects.all()[:5]

    all_documents  = Document.objects.filter()
    number_of_approved = Document.objects.filter().count()
    number_of_rejected = Document.objects.filter().count()
    number_of_signed = Document.objects.filter().count()
    number_of_at_signatory = Document.objects.filter().count()
    number_of_completed = Document.objects.filter(stage = 'Completed').count()


    if request.user.profile.role.name == 'Bank Originator':
        documents = Document.objects.filter(
            stage = 'Bank Originator', 
            status='Approved', 
            rejected = False,
            forwaded_to_signatories_by__isnull=True
        ).order_by('-created')

    elif request.user.profile.role.name == 'A Signatory':
        documents = Document.objects.filter(Q(stage = 'Signatory') | Q(stage = 'A Signatory'), status='Approved').order_by('-created')

    elif request.user.profile.role.name == 'B Signatory':
        documents = Document.objects.filter(
            Q(stage = 'Signatory') | Q(stage = 'B Signatory'), 
            status='Approved',
            b_signatory = request.user
        ).order_by('-created')

    elif request.user.profile.role.name == 'Company Approver':
        documents = Document.objects.filter(approvers=request.user, stage='Approver', status='Pending').order_by('-created')

    else:
        documents = Document.objects.filter(added_by=request.user, stage='Approver', status='Pending').order_by('-created')

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    
    context = {
        'documents': documents,
        'categories': categories,
        'number_of_approved': number_of_approved,
        'number_of_rejected': number_of_rejected,
        'number_of_signed' : number_of_signed,
        'number_of_at_signatory': number_of_at_signatory,
        'number_of_completed': number_of_at_signatory,
    }

    return render(request, 'documents/documents.html', context)

def upload_signed_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    form = SignatoryForm(request.POST or None, request.FILES or None, instance=document)
    old_file_path = document.file.path
    print (".......................")

    # if request.method == 'POST' and request.FILES:
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         if document.a_signatory == None and request.user.profile.role.name == 'A Signatory' and document.b_signatory:
    #             instance.stage = 'Completed'
    #             instance.a_signatory = request.user
    #             instance.a_signatory_signed_date = datetime.datetime.now()
            
    #         if document.a_signatory and request.user.profile.role.name == 'B Signatory' and document.b_signatory == None:
    #             instance.stage = 'Completed'
    #             instance.a_signatory = request.user
    #             instance.a_signatory_signed_date = datetime.datetime.now()
                
    #         if document.a_signatory == None and request.user.profile.role.name == 'A Signatory' and document.b_signatory == None:
    #             instance.stage = 'B Signatory'
    #             instance.a_signatory = request.user
    #             instance.a_signatory_signed_date = datetime.datetime.now()

    #         if document.a_signatory == None and request.user.profile.role.name == 'B Signatory' and document.b_signatory == None:
    #             instance.stage = 'A Signatory'
    #             instance.b_signatory = request.user
    #             instance.b_signatory_signed_date = datetime.datetime.now()

    #         os.remove(old_file_path)
    #         instance.save()
    #         messages.success(request, "Signed Document Uploaded Successfully")
    #         return HttpResponseRedirect("/document/" + str(document_id) + "/")

    # context = {
    #     'form': form
    # }
    
    # return render(request, 'documents/upload_signed_document.html', context)

def edit_document(request, document_id):  
    document = get_object_or_404(Document, id=document_id)
    form = DocumentFileForm(request.POST or None, request.FILES or None, instance=document)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.stage = 'Approver'
            instance.save()
            
            messages.success(request, "Form Updated Successfully")
            return HttpResponseRedirect("/document/" + str(document_id) + "/")

    context = {
        'form': form
    }
    
    return render(request, 'documents/edit_document.html', context)

def upload_document(request):
    if request.method == 'POST':
        form = DocumentFileForm(request.POST or None, request.FILES or None, user=request.user)
        if form.is_valid():
            approvers = []
            company_approvers = form.cleaned_data['company_approvers']
            for company_approver in company_approvers: 
                approvers.append(company_approver.user)

            files = request.FILES.getlist('file')

            instance = form.save(commit=False)
            instance.added_by = request.user
            instance.save()
            instance.approvers.set(approvers)

            form.save_m2m()

            if files:
                for f in files:
                    File.objects.create(document=instance,file=f)
            messages.success(request, "Document Uploaded Successfully")

            return HttpResponseRedirect("/documents/")

    else:
        form = DocumentFileForm(user=request.user)

    context = {
        'form': form
    }
    
    return render(request, 'documents/upload_document.html', context)

def pending_company_approval(request):
    print ("........................") 

def company_approved(request):

    page = request.GET.get('page', 1)
    documents = Document.objects.filter(status='Approved').order_by('-created')

    if request.user.profile.role.name == 'Bank Originator':
        documents = documents.filter(added_by =  request.user)

    elif request.user.profile.role.name == 'Company Approver':
        documents = documents.filter(approved_by=request.user)

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/company_approved.html', context)

def approve_document(request, document_id):
    document = Document.objects.filter(id=document_id)
    apporvers_list = [request.user]

    if request.user in document.first().approvers.all():
        if not request.user in document.first().approved_by.all():
            approved = document.first().approved_by.add(request.user)
            if list(document.first().approvers.all()) == list(document.first().approved_by.all()):
                document.update(date_approved=datetime.datetime.now(), stage = 'Bank Originator', status='Approved', rejected=False)
                messages.error(request, "Document approved successfully")
                return HttpResponseRedirect("/document/" + str(document_id) + "/")
            else:
                messages.error(request, "Document approved successfully")
                return HttpResponseRedirect("/document/" + str(document_id) + "/")
        else:
            messages.error(request, "Already approved successfully")
            return HttpResponseRedirect("/document/" + str(document_id) + "/")
    else:
        messages.error(request, "Not permitted to approve document")
        return HttpResponseRedirect("/document/" + str(document_id) + "/")

def forward_to_signatories(request, document_id):
    Document.objects.filter(id=document_id).update(forwaded_to_signatories_by=request.user, date_forwaded_to_signatories=datetime.datetime.now(), stage='Signatories')
    messages.success(request, "Document Forwaded Successsfully")

    return HttpResponseRedirect("/document/" + str(document_id) + "/")

def completed_documents(request):
    page = request.GET.get('page', 1)
    
    documents = Document.objects.filter(signed=True, completed=True).order_by('-created')

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/completed_documents.html', context)

def signatory_signed_documents(request):
    page = request.GET.get('page', 1)
    
    documents = Document.objects.filter(signed=True, completed=False).order_by('-created')

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/signed_documents.html', context)

def complete_document(request, document_id):
    Document.objects.filter(id=document_id).update(
        completed = True, 
        date_completed = datetime.datetime.now()
    )
    messages.success(request, "Document Completed Successsfully")
    return HttpResponseRedirect("/signatory-signed-documents/")

def rejected_documents(request):

    page = request.GET.get('page', 1)
    documents = Document.objects.filter(status='Rejected').order_by('-created')

    if request.user.profile.role.name == 'Bank Originator':
        documents = documents.filter(added_by =  request.user)

    elif request.user.profile.role.name == 'Company Approver':
        documents = documents.filter(rejected_by=request.user)

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    
    context = {
        'documents': documents,
    }


    # page = request.GET.get('page', 1)

    # if request.user.profile.role == 'Company Approver':
    #     documents = Document.objects.filter(added_by =  request.user, status='Rejected').order_by('-created')

    # elif request.user.profile.role == 'Company Approver':
    #     documents = Document.objects.filter(rejected_by =  request.user, status='Rejected').order_by('-created')

    # paginator = Paginator(documents, 5)

    # try:
    #     documents = paginator.page(page)
    # except PageNotAnInteger:
    #     documents = paginator.page(1)
    # except EmptyPage:
    #     documents = paginator.page(paginator.num_pages)

    # context = {
    #     'documents': documents
    # }

    return render(request, 'documents/rejected_documents.html', context)

def documents_at_signatory(request):
    page = request.GET.get('page', 1)
    documents = Document.objects.filter(forwaded_to_signatories_by=request.user, status='Approved').order_by('-created')

    if request.user.profile.role.name == 'Bank Originator':
        documents = documents.filter(
            Q(stage__icontains='Signatory') | 
            Q(stage__icontains='A Signatory') |
            Q(stage__icontains='B Signatory'))

    elif request.user.profile.role.name == 'Company Approver':
        documents = documents.filter()

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/documents_at_signatory.html', context)

def a_signatory_signed_documents(request):

    page = request.GET.get('page', 1)
    documents = Document.objects.filter(a_signatory = request.user, a_signatory_signed = True).order_by('-created')

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/a_signatory_signed_documents.html', context)

def b_signatory_signed_documents(request):

    page = request.GET.get('page', 1)
    documents = Document.objects.filter(b_signatory = request.user, b_signatory_signed = True).order_by('-created')

    paginator = Paginator(documents, 5)

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)

    context = {
        'documents': documents
    }

    return render(request, 'documents/a_signatory_signed_documents.html', context)

def document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    uploaded_documents = File.objects.filter(document=document)
    rejection_history = RejectedDocument.objects.filter(document=document).order_by('-created')
    form = RejectedDocumentForm(request.POST or None, request.FILES or None, instance=document, prefix='reject')
    assign_signatory_form = AssignSignatoryForm(request.POST or None, request.FILES or None, instance=document)
    signatory_form = SignatorySignedForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and 'reject' in request.POST:
        if form.is_valid():

            instance = form.save(commit=False)
            instance.rejected_by = request.user 

            if request.user.profile.role.name == 'Company Approver':
                stage = 'Originator'
            elif request.user.profile.role.name == 'Bank Originator':
                stage = 'Originator'
            elif request.user.profile.role.name == 'A Signatory':
                stage = 'Bank Originator'
            elif request.user.profile.role.name == 'B Signatory':
                stage = 'Bank Originator'  

            instance.document = document
            reason_for_rejection = form.cleaned_data['reason_for_rejection']
            Document.objects.filter(id=document_id).update(
                stage = stage, 
                status = 'Rejected', 
                rejected = True, 
                rejected_by = request.user, 
                reason_for_rejection = reason_for_rejection, 
                date_rejected = datetime.datetime.now()
            )
            messages.success(request, "Document Rejected Successsfully")
            return HttpResponseRedirect("/document/" + str(document_id) + "/")

    if request.method == 'POST' and 'signatory_form' in request.POST:
        if signatory_form.is_valid():
            if request.user.profile.role.name == 'A Signatory':
                if document.b_signatory and document.b_signatory_signed and document.a_signatory and not document.a_signatory_signed: 
                    Document.objects.filter(id=document_id).update(
                        stage = 'Bank Originator', 
                        a_signatory_signed = True, 
                        a_signatory_signed_date = datetime.datetime.now()
                    )
                elif document.b_signatory and not document.b_signatory_signed and document.a_signatory and not document.a_signatory_signed: 
                    Document.objects.filter(id=document_id).update(
                        stage = 'B Signatory', 
                        a_signatory_signed = True, 
                        a_signatory_signed_date = datetime.datetime.now()
                    )
                elif not document.b_signatory and not document.b_signatory_signed and document.a_signatory and not document.a_signatory_signed:
                    Document.objects.filter(id=document_id).update(
                        stage = 'Bank Originator', 
                        a_signatory_signed = True, 
                        a_signatory_signed_date = datetime.datetime.now()
                    )
            elif request.user.profile.role.name == 'B Signatory':
                if document.a_signatory and document.a_signatory_signed and document.b_signatory and not document.b_signatory_signed: 
                    Document.objects.filter(id=document_id).update(
                        stage = 'Bank Originator', 
                        b_signatory_signed = True, 
                        b_signatory_signed_date = datetime.datetime.now()
                    )
                elif document.b_signatory and not document.b_signatory_signed and document.a_signatory and not document.a_signatory_signed: 
                    Document.objects.filter(id=document_id).update(
                        stage = 'A Signatory', 
                        b_signatory_signed = True, 
                        b_signatory_signed_date = datetime.datetime.now()
                    )
                elif not document.a_signatory and not document.a_signatory_signed and document.b_signatory and not document.b_signatory_signed:
                    Document.objects.filter(id=document_id).update(
                        stage = 'Bank Originator', 
                        b_signatory_signed = True, 
                        b_signatory_signed_date = datetime.datetime.now()
                    )

            deleted_file = File.objects.filter(document=document).delete()

            files = request.FILES.getlist('file')

            if files:
                for f in files:
                    File.objects.create(
                        document=document,
                        file=f,
                        uploaded_by=request.user
                    )

            messages.success(request, "Document Uploaded Successfully")
            return HttpResponseRedirect("/documents/")

    if request.method == 'POST' and 'assign_signatory_form' in request.POST:
        if assign_signatory_form.is_valid():
            aa_signatory = assign_signatory_form.cleaned_data['aa_signatory']
            bb_signatory = assign_signatory_form.cleaned_data['bb_signatory']

            if aa_signatory:
                a_signatory = aa_signatory.user
            else: 
                a_signatory = ''

            if bb_signatory:
                b_signatory = bb_signatory.user
            else:
                b_signatory = ''

            Document.objects.filter(id=document_id).update(
                a_signatory = a_signatory, 
                b_signatory = b_signatory, 
                forwaded_to_signatories_by = request.user, 
                date_forwaded_to_signatories = datetime.datetime.now(),
                stage = 'Signatory',
            )
            messages.success(request, "Document Assigned to signatory successfully")
            return HttpResponseRedirect("/document/" + str(document_id) + "/")
        else:
            messages.error(request, "Failed to assign signatory. One of the signatories is required")
            return HttpResponseRedirect("/document/" + str(document_id) + "/")

    context = {
        'document': document,
        'form': form,
        'signatory_form': signatory_form,
        'assign_signatory_form': assign_signatory_form,
        'rejection_history': rejection_history,
        'uploaded_documents': uploaded_documents
    }

    return render(request, 'documents/document.html', context)
   
def add_document_category(request):
    form = CategoryForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and request.FILES:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.added_by = request.user
            instance.save()

            # name = form.cleaned_data['name']
            # file = form.cleaned_data['file']

            # description = str(request.user.profile.first_name) + " " + str(request.user.profile.last_name) + " added document category"
            # http_method = request.method
            # activity_type = "add_document_category"
            # url = request.get_full_path()
            # request_body = {
            #     'name': name, 
            #     'file': file
            # }

            # activity_log = AuditLog(
            #     activity_type = activity_type,
            #     http_method = http_method,
            #     description = description,
            #     url = url,
            #     added_by = request.user,
            #     request_body = request_body
            # )
            # activity_log.save()

            messages.success(request, "Document Category Added Successsfully")
            return HttpResponseRedirect("/document-categories/")

    context = {
        'form': form
    }
    
    return render(request, 'documents/add_document_category.html', context)

