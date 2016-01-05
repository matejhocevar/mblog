from mblogApp.models import UserProfile
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


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
		logger.error("User %s unsuccessfully subscribed to user %s. One of users does not exists" %(me, user))
		return None
	else:
		user.followers.add(me)
		user.save()

		logger.info("User %s successfully subscribed to user %s." %(me.user.username, user.user.username))
		return user.followers.all()


def unsubscribe(user=None, me=None):
	if user == None or me == None:
		logger.error("User %s unsuccessfully subscribed to user %s. One of users does not exists." %(me.user.username, user.user.username))
		return None
	else:
		user.followers.remove(me)
		user.save()

		logger.info("User %s successfully unsubscribed to user %s." %(me, user))
		return user.followers.all()