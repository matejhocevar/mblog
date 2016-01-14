# mblog
> Micro blog created with django framework

Main purpose of this project is to build django reference point and to learn good django code practices

## Prerequisites
	Coming soon...

## Installation
	git clone https://github.com/matoxxx/mblog.git

Navigate to:

	cd mblog

##### Create virtual enviroment
	virtualenv env

##### Activate virtual enviroment
on Windows:

	cd env/Scripts
	activate

on Unix:

	source env/bin/activate

##### Install dependencies:
	pip install -r requirements.txt

##### Migrate database:
	python manage.py migrate

##### Installion fixtures
	python manage.py loaddata mblogapp

## Usage

##### Running application
	python manage.py runsever <ip:port>			# example: python manage.py runserver 127.0.0.1:8000

##### Create fixtures
	python manage.py dumpdata auth.user mblogApp > mblogApp/fixtures/mblogapp.json

#### Testing application
	python manage.py test

## Heroku deploy
	Coming soon...

## Todo
+ user & group permissions
+ proper readme file
+ stress tests

## Author
Matej Hocevar [@matoxxx](https://github.com/matoxxx)
