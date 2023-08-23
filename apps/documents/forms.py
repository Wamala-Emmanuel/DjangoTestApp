from dataclasses import field
from django import forms
from .models import Document, Category, RejectedDocument, File
from apps.accounts.models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import default
from django.forms.widgets import CheckboxSelectMultiple

class DocumentForm(forms.ModelForm):

    company_approvers = forms.ModelMultipleChoiceField(
        queryset = Profile.objects.all(),
    )

    class Meta:
        model = Document
        fields = [
            'category', 
            'comments',
            'company_approvers'
        ]

    def __init__(self,*args, user=None, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['company_approvers'] = forms.ModelMultipleChoiceField(
                queryset=Profile.objects.filter(active=True, role__name = 'Company Approver', company = user.profile.company),
                required=True,
                help_text="Select Company Approver")

class DocumentFileForm(DocumentForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta(DocumentForm.Meta):
        fields = DocumentForm.Meta.fields + ['file',]

class SignatoryForm(DocumentForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta(DocumentForm.Meta):
        fields = DocumentForm.Meta.fields + ['file',]
        exclude = (
            'category',
            'comments',
        )

class SignatorySignedForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = File
        fields = (
            'file',)

class AssignSignatoryForm(forms.ModelForm):

    aa_signatory = forms.ModelChoiceField(queryset=Profile.objects.filter(active=True, role__name = 'A Signatory'), required=False, help_text="Select A Signatory")
    bb_signatory = forms.ModelChoiceField(queryset=Profile.objects.filter(active=True, role__name = 'B Signatory'), required=False, help_text="Select B Signatory")

    class Meta:
        model = Document
        fields = [
            'aa_signatory', 
            'bb_signatory'
        ]

    def clean(self):
        aa_signatory = self.cleaned_data.get('aa_signatory')
        bb_signatory = self.cleaned_data.get('bb_signatory')
        if not aa_signatory and not bb_signatory:
            raise forms.ValidationError('One of fields is required')
        return self.cleaned_data

class RejectedDocumentForm(forms.ModelForm):
    class Meta:
        model = RejectedDocument
        fields = [
            'reason_for_rejection', 
        ]

class RejectForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'reason_for_rejection', 
        ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'file'
        ]

