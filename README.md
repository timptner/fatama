# FaTaMa

This repository contains the source code of the registration platform for the 
conference of the student councils for mechanical engineering.

[Django](https://www.djangoproject.com) is used as the web framework and 
[Bulma](https://bulma.io) for styling.

## Development

1. Clone the repository
2. Create a config file `.env`
3. Generate a new secret key with 
   `django.core.management.utils.get_random_secret_key` and add 
   `SECRET_KEY="<value>"` to the config file
4. Create a new postgres database
   1. Add database details (host, post, name, user, password) to the config file
   2. Migrate database with `python manage.py migrate`
   3. Create an initial superuser with `python manage.py createsuperuser`

## Author

Aiven Timptner
