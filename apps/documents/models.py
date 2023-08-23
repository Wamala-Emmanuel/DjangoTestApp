from unicodedata import category
from django.db import models
from django.conf import settings
from helpers.validators import validate_file_size

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='category_added_by')
    file = models.FileField(upload_to='document_categories/%Y/%m/%d/', editable=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class Document(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    comments = models.TextField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='document_added_by')
    a_signatory = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='a_signatory')
    b_signatory = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='b_signatory')
    a_signatory_signed_date = models.DateTimeField(blank=True, null=True)
    b_signatory_signed_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='document_approved_by', blank=True)
    forwaded_to_signatories_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='forwaded_to_signatories_by')
    date_forwaded_to_signatories = models.DateTimeField(blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    stage = models.CharField(max_length=255, default='Approver')
    approvers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='document_approvers')
    status = models.CharField(max_length=255, default='Pending')
    rejected = models.BooleanField(default=False)
    a_signatory_signed = models.BooleanField(default=False)
    b_signatory_signed = models.BooleanField(default=False)
    signed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    rejected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='document_rejected_by')
    reason_for_rejection = models.TextField(blank=True, null=True)
    date_rejected = models.DateTimeField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.category) + " - " + str(self.added_by)

class File(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='file_uploaded_by')
    document = models.ForeignKey(Document,on_delete=models.CASCADE, related_name='document_file')
    file = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name="Files", validators=[validate_file_size], help_text="Allowed size is 50MB")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class RejectedDocument(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, blank=True, null=True)
    reason_for_rejection = models.TextField()
    rejected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='rejected_document_by')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)