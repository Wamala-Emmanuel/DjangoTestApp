from unicodedata import name
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
