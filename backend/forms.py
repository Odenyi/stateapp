from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

import re

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    terms_and_conditions = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'id': 'terms'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ( 'email', 'phone_number', 'password1', 'password2')
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Remove any non-digit characters from the phone number
        cleaned_phone_number = re.sub(r'\D', '', phone_number)

        if len(cleaned_phone_number) < 10 or len(cleaned_phone_number) > 13:
            raise forms.ValidationError("Phone number must have between 10 and 13 digits")

        if not cleaned_phone_number.startswith(('+254', '254', '0')):
            raise forms.ValidationError("Phone number must start with +254, 254, or 0")

        return phone_number
