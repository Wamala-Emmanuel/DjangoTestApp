from django.contrib import admin
from .models import Category, Document, RejectedDocument, File

# Register your models here.
admin.site.register(Document)
admin.site.register(Category)
admin.site.register(RejectedDocument)
admin.site.register(File)


