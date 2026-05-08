import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydatakla.settings")

application = get_wsgi_application()

# Vercel expects 'app'
app = application
