from django.contrib import admin
from django.urls import path
from .views import completed_documents, b_signatory_signed_documents, documents, complete_document, signatory_signed_documents, documents_at_signatory, a_signatory_signed_documents, pending_company_approval, rejected_documents, company_approved, update_category, delete_category, upload_signed_document, forward_to_signatories, upload_document, edit_document, document_categories, add_document_category, document, approve_document

urlpatterns = [
    
    path('documents/', documents, name="documents"),
    path('document/<int:document_id>/', document, name="document"),
    path('upload-document/', upload_document, name="upload_document"),
    path('add-document_category/', add_document_category, name="add_document_category"),
    path('document-categories/', document_categories, name="document_categories"),
    path('delete-category<int:category_id>/', delete_category, name="delete_category"),
    path('update-category<int:category_id>/', update_category, name="update_category"),
    path('approve-document/<int:document_id>/', approve_document, name="approve_document"),
    path('edit-document/<int:document_id>/', edit_document, name="edit_document"),
    path('upload-signed-document/<int:document_id>/', upload_signed_document, name="upload_signed_document"),
    path('forward-to-signatories/<int:document_id>/', forward_to_signatories, name="forward_to_signatories"),
    path('pending-company-approval/', pending_company_approval, name="pending_company_approval"),
    path('company-approved/', company_approved, name="company_approved"),
    path('rejected_documents/', rejected_documents, name="rejected_documents"),
    path('documents-at-signatory/', documents_at_signatory, name="documents_at_signatory"),
    path('a-signatory-signed-documents/', a_signatory_signed_documents, name="a_signatory_signed_documents"),
    path('signatory-signed-documents/', signatory_signed_documents, name="signatory_signed_documents"),
    path('complete-document/<int:document_id>/', complete_document, name="complete_document"),
    path('completed-documents/', completed_documents, name="completed_documents"),
    path('b-signatory-signed-documents/', b_signatory_signed_documents, name="b_signatory_signed_documents"),

]