from mblogApp.models import UserProfile
from django.utils import timezone

def getSubscribeStatus(loggedUser, profileUser):
	subscriptionType = 'nosubscribe'

	if loggedUser == None:
		return subscriptionType

	loggedUser = loggedUser.profile

	if loggedUser == profileUser:
		subscriptionType = "nosubscribe"
	elif loggedUser in profileUser.profile.followers.all():
		subscriptionType = "unsubscribe"
	else:
		subscriptionType = "subscribe"

	return subscriptionType

def subscribe(user=None, me=None):
	if user == None or me == None:
		return None
	else:
		user.followers.add(me)
		user.save()

		return user.followers.all()

def unsubscribe(user=None, me=None):
	if user == None or me == None:
		return None
	else:
		user.followers.remove(me)
		user.save()

		return user.followers.all()