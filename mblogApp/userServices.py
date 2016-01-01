from mblogApp.models import UserProfile
from django.utils import timezone

def getSubscribeStatus(loggedUser, profileUser):
	subscriptionType = 'nosubscribe'

	if loggedUser == None:
		return subscriptionType

	if loggedUser == profileUser:
		subscriptionType = "nosubscribe"
	elif profileUser in loggedUser.profile.following.all():
		subscriptionType = "unsubscribe"
	else:
		subscriptionType = "subscribe"

	return subscriptionType