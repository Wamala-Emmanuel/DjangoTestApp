from apps.companies.models import Company
from apps.roles.models import Role
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='user_added_by')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='user_approved_by')
    deactivated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='user_deactivated_by')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True, related_name='role')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='company')
    approved_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    deactivated_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username) + " " + str(self.user.first_name) + " " + str(self.user.last_name) + " " + str(self.role.name)
