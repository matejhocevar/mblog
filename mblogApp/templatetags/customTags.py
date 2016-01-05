from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='getPostImage')
def getPostImage(post):
	url = ''
	try:
		url = '/static/%s' % (str(post.image).split('static/')[1])
	except:
		return url

	return url