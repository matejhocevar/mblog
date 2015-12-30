from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import ValidationError
from mblogApp.userUtils import *
from mblogApp.forms import *
from mblogApp.fillDB import *


def index(request):
	user = get_object_or_404(User, username='qwertzr')
	posts = Post.objects.filter(author=user).order_by("postTime").reverse()
	return render_to_response('mblogApp/index.html', RequestContext(request, {'u': user, 'posts': posts}))


def profileController(request, username):
	loggedUser = get_object_or_404(User, username='qwertzr')
	user = get_object_or_404(User, username=username)
	subscriptionType = getSubscribeStatus(loggedUser, user)
	posts = Post.objects.filter(author=user).order_by("postTime").reverse()
	return render_to_response('mblogApp/profile/index.html', RequestContext(request, {'u': user, 'st': subscriptionType, 'posts': posts}))


def tagController(request, tagname):
	return render(request, 'mblogApp/tag/index.html')


def loginController(request):
	return render(request, 'mblogApp/login/login.html')


def registerController(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = RegisterForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			try:
				user = None
				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password']
				passwordConfirm = form.cleaned_data['confirmPassword']

				if password == passwordConfirm:
					user = registerUser(username, email, password)
				else:
					raise ValidationError('Passwords must match.')

			except ValidationError as ve:
				pass
			return render_to_response('mblogApp/login/registerSuccessful.html', RequestContext(request, {'u': user}))

	else:
		form = RegisterForm()

		return render_to_response('mblogApp/login/register.html', RequestContext(request, {'form': form}))


def noJSController(request):
	return render(request, 'mblogApp/nojavascript.html')


def infinityPostController(request):
	return render(request, 'mblogApp/post/post.html')


def fillController(request, model=None, number=None):
	number = int(number)

	if model == 'users':
		users = fillUsers(number)
		if users:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': users}))
		else:
			return render_to_response(status=404)
	elif model == 'subscriptions':
		subscriptions = fillSubscriptions(number)
		if subscriptions:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': subscriptions}))
		else:
			return render_to_response(status=404)
	elif model == 'posts':
		posts = fillPosts(number)
		if posts:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': posts}))
		else:
			return render_to_response(status=404)
	else:
		return render_to_response(status=404)