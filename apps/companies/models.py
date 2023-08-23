from django.db import models
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='company_added_by')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='company_approved_by')
    deactivated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='company_deactivated_by')
    deactivated_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    logo = models.ImageField(upload_to='companies/%Y/%m/%d/', editable=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
