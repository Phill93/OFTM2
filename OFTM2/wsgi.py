'''WSGI for OFTM2'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OFTM2.settings.base')

application = get_wsgi_application()
