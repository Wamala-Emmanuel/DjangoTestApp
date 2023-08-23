from django.db import models
from django.db import models
from django.utils import timezone
from django.conf import settings

class AuditLog(models.Model):
    activity_type = models.CharField(
        max_length=255, null=True, blank=True)
    http_method = models.CharField(
        max_length=255, null=True, blank=True)
    description = models.TextField()
    request_body = models.TextField(null=True, blank=True)
    url = models.CharField(
        max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(
        auto_now_add=True, editable=False)
    updated = models.DateTimeField(
        auto_now_add=True, editable=True)

    def __str__(self):
        return str(self.activity_type) + " " + str(self.added_by)