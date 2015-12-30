from faker import Factory as FakerFactory
from mblogApp.models import User, Post

def fillUsers(number=50):
	try:
		# faker = FakerFactory.create('sl-SI')
		faker = FakerFactory.create()
		users = []
		for _ in range(0, number):
			user = User()
			firstName = faker.first_name()
			lastName = faker.last_name()
			user.displayName = "%s %s" % (firstName, lastName)
			user.username = user.displayName.replace(" ", "").lower()
			user.password = faker.password(digits=True, upper_case=True, lower_case=True)
			user.email = "%s@%s" % (user.username, faker.domain_name())
			user.registerDate = faker.date_time_this_decade(before_now=True, after_now=False)
			user.location = "%s, %s" % (faker.city(), faker.country())
			user.description = faker.text(max_nb_chars=200)
			user.webpage = faker.url()

			users.append(user)
			user.save()
	except Exception as e:
		print e.message
		return None

	return users


def fillSubscriptions(number):
	subscriptions = []
	user = User()

	try:
		for _ in range(0, number):
			u1 = user.random()
			u2 = user.random()

			subscriptions.append("%s -> %s" % (u1.displayName, u2.displayName))
			u1.following.add(u2)
			u1.save()

	except Exception as e:
		print e.message
		return None

	return subscriptions

def fillPosts(number):
	posts = []
	user = User()
	faker = FakerFactory.create()

	try:
		for _ in range(0, number):
			p = Post()
			p.postTime = faker.date_time_this_decade(before_now=True, after_now=False)
			p.locationTown = faker.city()
			p.locationCountry = faker.country()
			p.content = faker.sentence(nb_words=50, variable_nb_words=True)

			u = user.random()
			u.posts.add(p)

			posts.append("%s posted at %s in %s, %s" % (u.displayName, p.postTime, p.locationTown, p.locationCountry))
			u.save()
			p.save()

	except Exception as e:
		print e.message
		return None

	return posts