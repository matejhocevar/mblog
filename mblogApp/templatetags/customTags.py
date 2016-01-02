from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='getPostImage')
def getPostImage(post):
	url = ''
	print settings.MEDIA_URL
	try:
		print "Path: " + post.image.path
		print "URL: " + post.image.url
		url = '/static/%s' % (str(post.image).split('static/')[1])
	except:
		return url

	print "Url: " + url
	return url