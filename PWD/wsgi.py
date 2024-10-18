"""
WSGI config for PWD project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PWD.settings')

application = get_wsgi_application()



from django.contrib.auth import get_user_model

User = get_user_model()

# Hardcoded credentials
username = 'admin'
email = 'admin@example.com'
password = '0711169847a'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")