from faker import Factory as FakerFactory
from django.contrib.auth.models import User
from mblogApp.models import UserProfile, Post
from random import gauss
from math import fabs, floor
from django.utils import timezone


def fillUsers(number=50):
	try:
		# faker = FakerFactory.create('sl-SI')
		faker = FakerFactory.create()
		users = []
		for _ in range(0, number):
			user = User()
			firstName = faker.first_name()
			lastName = faker.last_name()
			name = "%s %s" % (firstName, lastName)
			user.first_name = firstName
			user.last_name = lastName
			user.username = name.replace(" ", "").lower()
			user.password = faker.password(digits=True, upper_case=True, lower_case=True)
			user.email = "%s@%s" % (user.username, faker.domain_name())
			user.save()

			profile = UserProfile()
			profile.user = user
			profile.displayName = name
			profile.location = "%s, %s" % (faker.city(), faker.country())
			profile.description = faker.text(max_nb_chars=200)
			profile.webpage = faker.url()

			users.append(profile.user)
			profile.save()
	except Exception as e:
		print e.message
		return None

	return users


def fillSubscriptions(number):
	subscriptions = []
	user = UserProfile()

	try:
		for _ in range(0, number):
			u1 = user.random()
			u2 = user.random()

			subscriptions.append("%s -> %s" % (u1.profile.displayName, u2.profile.displayName))
			u1.profile.following.add(u2.profile)
			u1.save()

	except Exception as e:
		print e.message
		return None

	return subscriptions

def fillPosts(number, authorId=None, time=None):
	posts = []
	user = UserProfile()
	faker = FakerFactory.create()

	try:
		for i in range(0, number):
			if i % 100 == 0:
				print "Adding %s. element" % i

			p = Post()

			if time == "now":
				p.postTime = timezone.now()
			else:
				p.postTime = faker.date_time_this_year(before_now=True, after_now=False)

			p.locationTown = faker.city()
			p.locationCountry = faker.country()
			p.content = generatePost(faker, hashtags=True, mentions=True)

			if authorId:
				u = User.objects.get(id=authorId)
			else:
				u = user.random()

			u.profile.posts.add(p)

			posts.append("%s posted at %s in %s, %s" % (u.profile.displayName, p.postTime, p.locationTown, p.locationCountry))
			u.save()
			p.save()

	except Exception as e:
		print e.message
		return None

	return posts

def generatePost(f, hashtags=False, mentions=False):
	content = f.sentence(nb_words=50, variable_nb_words=True)

	if mentions:
		n = int(floor(fabs(gauss(1, 1))))
		for _ in range(0, n):
			u = UserProfile()
			randomUser = u.random()
			content = "@%s %s" % (randomUser.username, content)

	if hashtags:
		n = int(floor(fabs(gauss(1, 1))))
		if n > 0:
			content = "%s %s" % (" ".join(content.split()[:-n]), " ".join(map((lambda x: '#' + x), content.split()[-n:])))

	return content