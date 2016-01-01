from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from mblogApp.postServices import *
from mblogApp.userServices import *
from mblogApp.databaseServices import *
from mblogApp.forms import RegistrationForm, LoginForm

from django.db.models import Q
from mblogApp.models import UserProfile, Post


def index(request):
	user = None
	if request.user.is_authenticated():
		user = request.user
		posts_list = Post.objects.filter(Q(author__in=user.profile.following.all()) | Q(author=user.profile)).order_by("postTime").reverse()
	else:
		posts_list = Post.objects.all().order_by("postTime").reverse()

	page = request.GET.get('page')
	posts = paginatePosts(postList=posts_list, numberOfResults=10, page=page)

	if page:
		return render_to_response('mblogApp/post/post.html', RequestContext(request, {'posts': posts}))
	else:
		return render_to_response('mblogApp/index.html', RequestContext(request, {'u': user, 'posts': posts}))


def profileController(request, username):
	loggedUser = None
	if request.user.is_authenticated():
		loggedUser = request.user
	user = get_object_or_404(User, username=username)

	subscriptionType = getSubscribeStatus(loggedUser, user.profile)

	posts_list = Post.objects.filter(author=user.profile).order_by("postTime").reverse()

	page = request.GET.get('page')
	posts = paginatePosts(postList=posts_list, numberOfResults=10, page=page)

	if page:
		return render_to_response('mblogApp/post/post.html', RequestContext(request, {'posts': posts}))
	else:
		return render_to_response('mblogApp//index.html', RequestContext(request, {'u': user, 'subscriptionType': subscriptionType, 'posts': posts}))


def tagController(request, tagname):
	tag = "#%s" % tagname
	user = get_object_or_404(UserProfile, username='matox2')
	posts_list = Post.objects.filter(Q(content__contains=tag)).order_by("postTime").reverse()

	page = request.GET.get('page')
	posts = paginatePosts(postList=posts_list, numberOfResults=10, page=page)

	if page:
		return render_to_response('mblogApp/post/post.html', RequestContext(request, {'posts': posts}))
	else:
		return render_to_response('mblogApp/tag.html', RequestContext(request, {'u': user, 'tag': tagname, 'posts': posts}))


def loginController(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			profile = authenticate(username=username, password=password)
			if profile is not None:
				login(request, profile)
				return HttpResponseRedirect('/')
			else:
				return render(request, 'mblogApp/login/login.html', RequestContext(request, {'form': form}))
		else:
			return render(request, 'mblogApp/login/login.html', RequestContext(request, {'form': form}))
	else:
		form = LoginForm()
	return render(request, 'mblogApp/login/login.html', RequestContext(request, {'form': form}))


def registerController(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profile')
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			user = User.objects.create_user(username=username, email=email, password=password)
			user.save()

			data = {'username': user.username, 'password': user.password}
			form = LoginForm(initial=data)

			return render_to_response('mblogApp/login/login.html', RequestContext(request, {'form': form}))
		else:
			return render_to_response('mblogApp/login/register.html', RequestContext(request, {'form': form}))

	else:
		form = RegistrationForm()
		return render_to_response('mblogApp/login/register.html', RequestContext(request, {'form': form}))


def noJSController(request):
	return render(request, 'mblogApp/nojavascript.html')


def infinityPostController(request):
	return render(request, 'mblogApp/post/post.html')


def fillController(request, model=None, number=None, author=None, time=None):
	number = int(number)

	if model == 'users':
		users = fillUsers(number=number)
		if users:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': users}))
		else:
			return HttpResponseRedirect('/')
	elif model == 'subscriptions':
		subscriptions = fillSubscriptions(number=number)
		if subscriptions:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': subscriptions}))
		else:
			return HttpResponseRedirect('/')
	elif model == 'posts':
		posts = fillPosts(number=number, authorId=author, time=time)
		if posts:
			return render_to_response('mblogApp/fill.html', RequestContext(request, {'model': model, 'number': number, 'list': posts}))
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')