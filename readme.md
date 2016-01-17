# mblog
> Micro blog created with django framework

Main purpose of this project is to build django reference point and to learn good django code practices

## Prerequisites
	virtualenv
	pip
	django

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

## Testing

##### Functional tests
	python manage.py test

##### Stress tests:
Download gevent - http://www.lfd.uci.edu/~gohlke/pythonlibs/#gevent

	pip install gevent-1.0.2-cp27-none-win_amd64.whl
	pip install locustio

	locust -f stress.py --host=http://localhost

Visit [locust dashboard](http://127.0.0.1:8089/)

## Todo
+ user & group permissions

### Author
Matej Hocevar [@matoxxx](https://github.com/matoxxx)
