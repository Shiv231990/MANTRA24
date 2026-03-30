import os
from django.core.wsgi import get_wsgi_application

# Ensure this matches your settings path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

application = get_wsgi_application()
