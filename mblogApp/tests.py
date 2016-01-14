from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from mblogApp.models import UserProfile
from selenium import webdriver
from mblogApp.exceptions import *


class RegistrationTests(StaticLiveServerTestCase):
	fixtures = ['mblogapp']

	username = "testuser"
	password = "testuser"
	email = "test@tests.com"

	def setUp(self):
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()

	def tearDown(self):
		self.selenium.quit()

	def test_registration_pass_not_match(self):
		self.go('/register/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(self.username)
		username_input = self.selenium.find_element_by_name("email")
		username_input.send_keys(self.email)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(self.password)
		password_input = self.selenium.find_element_by_name("confirmPassword")
		password_input.send_keys('testpassword2')
		self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()
		if self.selenium.find_element_by_xpath('//*[@id="login-container"]/form/ul/li').text != 'The passwords did not match. Please try again.':
			raise PasswordsDontMatchException()

	def test_registration_wrong_email(self):
		self.go('/register/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(self.username)
		username_input = self.selenium.find_element_by_name("email")
		username_input.send_keys('test@tests')
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(self.password)
		password_input = self.selenium.find_element_by_name("confirmPassword")
		password_input.send_keys(self.password)
		self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()
		if self.selenium.find_element_by_xpath('//*[@id="login-container"]/form/ul[1]/li').text != 'Enter a valid email address.':
			raise InvalidEmailException()

	def test_registration_success(self):
		self.go('/register/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(self.username)
		username_input = self.selenium.find_element_by_name("email")
		username_input.send_keys(self.email)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(self.password)
		password_input = self.selenium.find_element_by_name("confirmPassword")
		password_input.send_keys(self.password)
		self.selenium.find_element_by_xpath('//input[@value="Sign in"]').click()
		self.selenium.implicitly_wait(1)
		if "login" not in self.selenium.title:
			raise RegistrationFailedException()


	'''
		Test utilities
	'''
	def go(self, location):
		self.selenium.get('%s%s' % (self.live_server_url, location))


class LoginTests(StaticLiveServerTestCase):
	fixtures = ['mblogapp']

	username = 'matox'
	password = 'matej'

	def setUp(self):
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()

	def tearDown(self):
		self.selenium.quit()

	def test_login_failed_no_username(self):
		self.go('/login/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys('')
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(self.password)
		self.click_login()
		if "home" in self.selenium.title:
			raise LoginFailedException()

	def test_login_failed_no_password(self):
		self.go('/login/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(self.username)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys('')
		self.click_login()
		if "home" in self.selenium.title:
			raise LoginFailedException()

	def test_login_success(self):
		self.go('/login/')
		username_input = self.selenium.find_element_by_name("username")
		username_input.send_keys(self.username)
		password_input = self.selenium.find_element_by_name("password")
		password_input.send_keys(self.password)
		self.click_login()
		if "home" not in self.selenium.title:
			raise LoginFailedException()

	'''
		Test utilities
	'''
	def click_login(self):
		self.selenium.find_element_by_xpath('//*[@id="submit"]').click()
		self.selenium.implicitly_wait(1)

	def go(self, location):
		self.selenium.get('%s%s' % (self.live_server_url, location))

	def logout(self):
		self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[3]/a').click()
		if self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[1]/a').text != 'LOGIN':
			raise LogoutFailedException()


class NavigationTests(StaticLiveServerTestCase):
	fixtures = ['mblogapp']

	def setUp(self):
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()

	def tearDown(self):
		self.selenium.quit()

	def test_home_page(self):
		self.go('')
		assert "home" in self.selenium.title
		welcome = self.selenium.find_element_by_xpath('/html/body/main/aside[1]/section[1]/div/h4')
		if welcome:
			if welcome.text != 'Hello blogger!':
				raise InvalidLoginException()
		else:
			raise	InvalidLoginException()

	# authenticated user required
	# def test_find_user(self):
	# 	LoginTests()
	#
	# 	self.go('profile/matox')
	# 	if "matox" not in self.selenium.title:
	# 		raise ProfileNotFoundException()

	'''
		Test utilities
	'''
	def logout(self):
		self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[3]/a').click()
		if self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[1]/a').text != 'LOGIN':
			raise LogoutFailedException()

	def go(self, location):
		self.selenium.get('%s%s' % (self.live_server_url, location))


class ActionsTests(StaticLiveServerTestCase):
	fixtures = ['mblogapp']

	def setUp(self):
		self.selenium = webdriver.Firefox()
		self.selenium.maximize_window()

	def tearDown(self):
		self.selenium.quit()

	def subscribe(self):
		followers = self.selenium.find_element_by_xpath('/html/body/main/aside[1]/section[1]/div[3]/div[3]/p[1]')
		followers_num = followers.text

		subscribe_btn = self.selenium.find_element_by_xpath('//*[@id="subscribe-btn"]').click()
		self.selenium.implicitly_wait(1)
		if subscribe_btn.text != 'Unsubscribe':
			raise SubscribeFailedException()

		current_followers = followers.text

		subscribers = self.selenium.find_element_by_xpath('/html/body/main/aside[2]/section[2]/ul')
		found = False
		for subscriber in subscribers.find_elements_by_xpath(".//*"):
			if subscriber.text == self.username:
				found = True
				break

		if not found:
			raise SubscribersListException()

		if followers_num == current_followers:
			raise SubscribersNumberException()

	def unsubscribe(self):
		followers = self.selenium.find_element_by_xpath('/html/body/main/aside[1]/section[1]/div[3]/div[3]/p[1]')
		followers_num = followers.text

		subscribe_btn = self.selenium.find_element_by_xpath('//*[@id="subscribe-btn"]').click()
		self.selenium.implicitly_wait(1)
		if subscribe_btn.text != 'Subscribe':
			raise SubscribeFailedException()

		current_followers = followers.text

		subscribers = self.selenium.find_element_by_xpath('/html/body/main/aside[2]/section[2]/ul')
		found = False
		for subscriber in subscribers.find_elements_by_xpath(".//*"):
			if subscriber.text == self.username:
				found = True
				break

		if found:
			raise SubscribersListException()

		if followers_num == current_followers:
			raise SubscribersNumberException()

	'''
		Test utilities
	'''
	def logout(self):
		self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[3]/a').click()
		if self.selenium.find_element_by_xpath('/html/body/header/div/nav/ul/li[1]/a').text != 'LOGIN':
			raise LogoutFailedException()

	def go(self, location):
		self.selenium.get('%s%s' % (self.live_server_url, location))