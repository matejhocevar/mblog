from mblogApp.models import User
from django.utils import timezone

def getSubscribeStatus(loggedUser, profileUser):
	subscriptionType = 'nosubscribe'

	if loggedUser == profileUser:
		subscriptionType = "nosubscribe"
	elif profileUser in loggedUser.following.all():
		subscriptionType = "unsubscribe"
	else:
		subscriptionType = "subscribe"

	return subscriptionType

def registerUser(username, email, password):
	user = None

	user = User(username=username, email=email, password=password, registerDate=timezone.now())

	if user != None:
		user.save()

	return user