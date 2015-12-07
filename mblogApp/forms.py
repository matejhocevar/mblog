from django import forms
from django.utils import timezone

class RegisterForm(forms.Form):
	username = forms.CharField(label="Username", max_length=50)
	email = forms.EmailField(label="Email", max_length=254)
	password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
	confirmPassword = forms.CharField(label="Confirm password", max_length=100, widget=forms.PasswordInput)
