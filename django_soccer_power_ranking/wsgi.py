"""
WSGI config for djangoproject_spi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_soccer_power_ranking.settings")


from django_soccer_power_ranking.settings import DEBUG
if DEBUG:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
else:
    # Static media handling in HEROKU
    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise

    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)