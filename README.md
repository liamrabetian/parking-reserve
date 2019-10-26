# Parking Reserve

## About Project
This is a simple, yet optimized parking reservation system written in Django. Currently only the backend system.

## Installation

### Requirements

* [Django] - Python Web Developement framework 2.2+
* Python 3.5+

##### Virtual environment

Use Python's own build-in ``venv`` to create a virtual environment and install dependencies inside the (venv).
```sh
$ python3 -m venv venv
```
Activate the virtual environment.
```sh
$ source venv/bin/activate
```
To deactivate the virtual environment.
```sh
$ deactivate
```
Install the dependencies in the ``requirements.txt`` file.

```sh
(venv)$ pip3 install -r requirements.txt
```

##### Django Setup

Setup the Django project, migrate changes and create a superuser to the Database.

```sh
(venv)$ django-admin startproject <project-name> && cd <project-name>
(venv)$ python3 manage.py makemigrations
(venv)$ python3 manage.py migrate
(venv)$ python3 manage.py createsuperuser
```

Run the project

```sh
(venv)$ python3 manage.py runserver
```

## Contributing
### For requests other than user register or login requests:
First send a request to the auth-token api, then use the bearer token in every api request.

Any changes are welcome, including front-end system additions.

   [Django]: <https://www.djangoproject.com>