from dataclasses import field
from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 
            'address', 
            'email', 
            'phone', 
            'logo'
        ]
