import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from mblogApp.postServices import *
from mblogApp.userServices import *
from mblogApp.databaseServices import *
from mblogApp.forms import RegistrationForm, LoginForm, PostForm

from django.db.models import Q
from mblogApp.models import UserProfile, Post


def indexController(request):
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
		form = PostForm()
		return render_to_response('mblogApp/index.html', RequestContext(request, {'u': user, 'posts': posts, 'form': form}))


def profileController(request, username):
	loggedUser = None
	if request.user.is_authenticated():
		loggedUser = request.user

	profileUser = get_object_or_404(User, username=username)

	if loggedUser == profileUser:
		return HttpResponseRedirect("/")

	subscriptionType = getSubscribeStatus(loggedUser=loggedUser, profileUser=profileUser)

	posts_list = Post.objects.filter(author=profileUser.profile).order_by("postTime").reverse()

	page = request.GET.get('page')
	posts = paginatePosts(postList=posts_list, numberOfResults=10, page=page)

	if page:
		return render_to_response('mblogApp/post/post.html', RequestContext(request, {'posts': posts}))
	else:
		form = PostForm(initial={'content': '@'+profileUser.username})
		return render_to_response('mblogApp/profile/index.html', RequestContext(request, {'u': profileUser, 'subscriptionType': subscriptionType, 'posts': posts, 'form': form}))


def postController(request):
	if request.user.is_authenticated():
		user = request.user

		if request.is_ajax():
			form = PostForm(request.POST)
			if form.is_valid():
				post = Post()
				post.content = form.cleaned_data['content']
				post.locationTown = form.cleaned_data['town']
				post.locationCountry = form.cleaned_data['country']
				post.postTime = timezone.now()
				post.image = request.FILES.get('file')
				user.profile.posts.add(post)

				post.save()
				user.save()

				newForm = PostForm()
				return render_to_response('mblogApp/post/addNew.html', RequestContext(request, {'u': user, 'form': newForm, 'status': "success"}))
			else:
				return render_to_response('mblogApp/post/addNew.html', RequestContext(request, {'u': user, 'form': form, 'status': "error"}))
		else:
			return HttpResponseRedirect('/login')
	else:
		return HttpResponseRedirect('/login')
	return None


def subscribeController(request, username=None, mode=None):
	if request.user.is_authenticated():
		me = request.user.profile
		user = User.objects.get(username=username)
		userProfile = user.profile

		if mode == "subscribe":
			list = subscribe(user=userProfile, me=me)
		elif mode == "unsubscribe":
			list = unsubscribe(user=userProfile, me=me)
		elif mode == "info":
			st = getSubscribeStatus(loggedUser=me.user, profileUser=user)
			return render_to_response('mblogApp/profile/info.html', RequestContext(request, {'u': user, 'subscriptionType': st}))

		return render_to_response('mblogApp/subscribers.html', RequestContext(request, {'subscribers': list}))
	else:
		return render_to_response('mblogApp/login/index.html', RequestContext(request, {}))


def tagController(request, tagname):
	user = None
	if request.user.is_authenticated():
		user = request.user
	tag = "#%s" % tagname

	posts_list = Post.objects.filter(Q(content__contains=tag)).order_by("postTime").reverse()

	page = request.GET.get('page')
	posts = paginatePosts(postList=posts_list, numberOfResults=10, page=page)

	if page:
		return render_to_response('mblogApp/post/post.html', RequestContext(request, {'posts': posts}))
	else:
		form = PostForm(initial={'content': tag})
		return render_to_response('mblogApp/tag.html', RequestContext(request, {'u': user, 'tag': tagname, 'posts': posts, 'form': form}))


def searchController(request, query=None):
	if query:
		queryset = User.objects.filter(Q(username__contains=query) | Q(profile__displayName__contains=query)).values('username', 'profile__displayName', 'profile__profileImage')
	else:
		queryset = User.objects.values('username', 'profile__displayName', 'profile__profileImage')
	serialized = json.dumps(list(queryset), cls=DjangoJSONEncoder)

	return HttpResponse(serialized, content_type='application/json')


def loginController(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
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
		return HttpResponseRedirect('/')
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