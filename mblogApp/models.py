from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth.models import User
from random import randint

def randomDefaultImage():
		return '/static/media/profile/default_%d.png' % randint(0, 21)

def randomPostImage():
		return '/static/media/img/post/default_%d.png' % randint(0, 12)


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	displayName = models.CharField(max_length=100, blank=True)
	location = models.CharField(max_length=100, blank=True)
	description = models.TextField(max_length=254, blank=True)
	webpage = models.URLField(max_length=200, blank=True)
	profileImage = models.ImageField(upload_to='profile', default=randomDefaultImage, blank=True)

	following = models.ManyToManyField("self", related_name='followers', symmetrical=False, blank=True)

	def __unicode__(self):
		return "%255s" % (self.user.username)

	def random(self):
		return User.objects.all().order_by('?')[:1].get()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


class Post(models.Model):
	author = models.ForeignKey('UserProfile', related_name='posts')
	postTime = models.DateTimeField()
	locationTown = models.CharField(max_length=100, blank=True)
	locationCountry = models.CharField(max_length=100, blank=True)
	content = models.TextField(max_length=800)
	# image = models.ImageField(upload_to='mblogApp/static/media/img/post', default=randomPostImage, blank=True)
	image = models.ImageField(upload_to='mblogApp/static/media/img/post', blank=True)

	def __unicode__(self):
		return self.content