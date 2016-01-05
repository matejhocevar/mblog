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


class PostForm(forms.Form):
	town = forms.CharField(label="Town", widget=forms.HiddenInput(), required=False)
	country = forms.CharField(label="Country", widget=forms.HiddenInput(), required=False)
	image = forms.ImageField(help_text="Upload image: ", widget=forms.HiddenInput(), required=False)
	content = forms.CharField(widget=forms.widgets.Textarea(attrs={'id': 'post-new'}))

	def clean_town(self):
		town = self.cleaned_data["town"]
		try:
			if town == "''":
				return None
			else:
				return town
		except:
			return None

	def clean_country(self):
		country = self.cleaned_data["country"]
		try:
			if country == "''":
				return None
			else:
				return country
		except:
			return None


class ProfileEditForm(forms.Form):
	displayName = forms.CharField(label="Name")
	location = forms.CharField(label="Location")
	description = forms.CharField(widget=forms.widgets.Textarea(attrs={}))
	webpage = forms.URLField(label="Web page")
	profileImage = forms.ImageField()