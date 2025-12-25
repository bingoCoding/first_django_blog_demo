"""
ASGI config for django_blog_program project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

profile = os.environ.get('DJANGO_PROFILE', 'dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog_program.settings.%s' % profile)

application = get_asgi_application()