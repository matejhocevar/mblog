from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from mblogApp.models import UserProfile


class RegistrationForm(ModelForm):
	username = forms.CharField(label="Username", max_length=50)
	email = forms.EmailField(label="Email", max_length=254)
	password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)
	confirmPassword = forms.CharField(label="Confirm password", max_length=100, widget=forms.PasswordInput)

	class Meta:
		model = UserProfile
		exclude = ('',)

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("Username is already taken, please select another.")

	def clean(self):
		try:
			if self.cleaned_data['password'] != self.cleaned_data['confirmPassword']:
				raise forms.ValidationError("The passwords did not match. Please try again.")
			return self.cleaned_data
		except:
			raise forms.ValidationError("Password is required.")

class LoginForm(forms.Form):
	username = forms.CharField(label="Username")
	password = forms.CharField(label="Password", widget=forms.PasswordInput())