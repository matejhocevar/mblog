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
		model = User
		exclude = ('date_joined',)

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
				self.add_error('password', forms.ValidationError("The passwords did not match. Please try again."))
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
	displayName = forms.CharField(label="Name", required=False)
	location = forms.CharField(label="Location", required=False)
	description = forms.CharField(label="Description", required=False, widget=forms.widgets.Textarea(attrs={'cols': 'auto', 'rows': 'auto'}))
	webpage = forms.URLField(label="Web page", required=False)
	profileImage = forms.ImageField(required=False)

from django.http import HttpResponseBadRequest

def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap