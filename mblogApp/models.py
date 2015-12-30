from django.db import models
from django.db.models.aggregates import Count
from random import randint

def randomDefaultImage():
		return '/static/media/profile/default_%d.png' % randint(0, 12)

def randomPostImage():
		return '/static/media/img/post/default_%d.png' % randint(0, 12)

class User(models.Model):
	username = models.CharField(max_length=50)
	displayName = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	registerDate = models.DateTimeField()
	location = models.CharField(max_length=100, blank=True)
	description = models.TextField(max_length=254, blank=True)
	webpage = models.URLField(max_length=200, blank=True)
	profileImage = models.ImageField(upload_to='mblogApp/static/media/profile', default=randomDefaultImage, blank=True)

	following = models.ManyToManyField("self", related_name='followers', symmetrical=False, null=True)

	def __unicode__(self):
		return "%50s - %20s %20s %25s %20s %100s %50s" % (self.displayName, self.username, self.password, self.email, self.registerDate, self.location, self.webpage)

	def random(self):
		return User.objects.all().order_by('?')[:1].get()

class Post(models.Model):
	author = models.ForeignKey('User', related_name='posts')
	postTime = models.DateTimeField()
	locationTown = models.CharField(max_length=100, blank=True)
	locationCountry = models.CharField(max_length=100, blank=True)
	content = models.TextField(max_length=800)
	# image = models.ImageField(upload_to='mblogApp/static/media/img/post', default=randomPostImage, blank=True)
	image = models.ImageField(upload_to='mblogApp/static/media/img/post', blank=True)

	def __unicode__(self):
		return self.content