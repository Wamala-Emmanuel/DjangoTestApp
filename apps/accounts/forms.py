from django import forms
from django.contrib.auth.models import User
from .models import Profile

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Div, Layout
from apps.roles.models import Role
from apps.companies.models import Company
from .models import Profile
from django.forms import ModelForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.Form):
    username = forms.CharField(required=True, max_length = 7)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all())
    company = forms.ModelChoiceField(queryset=Company.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if User.objects.filter(email=email).exists():
            msg = 'A user with email already exists.'
            self.add_error('email', msg)           
    
        if User.objects.filter(username=username).exists():
            msg = 'A user with username already exists.'
            self.add_error('username', msg)    

        return self.cleaned_data

# class UserRegistrationForm(forms.ModelForm):    
#     class Meta:
#         model = User
#         fields = ('username',)
    
#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('Passwords don\'t match.')
#         return cd['password2']


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'phone', 'role', 'company')



