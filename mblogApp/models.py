from django.db import models

class User(models.Model):
	username = models.CharField(max_length=50)
	displayName = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	email = models.EmailField(max_length=254)
	registerDate = models.DateTimeField()
	location = models.CharField(max_length=100, blank=True)
	description = models.TextField(max_length=254, blank=True)
	webpage = models.URLField(max_length=200, blank=True)
	profileImage = models.ImageField(upload_to='mblogApp/static/media/img/profile', blank=True)

	following = models.ManyToManyField("self", related_name='followers', symmetrical=False, null=True)

	def __unicode__(self):
		return self.displayName

class Post(models.Model):
	author = models.ForeignKey('User', related_name='posts')
	postTime = models.DateTimeField()
	locationTown = models.CharField(max_length=100, blank=True)
	locationCountry = models.CharField(max_length=100, blank=True)
	content = models.TextField(max_length=800)
	image = models.ImageField(upload_to='mblogApp/static/media/img/post', blank=True)

	def __unicode__(self):
		return self.content