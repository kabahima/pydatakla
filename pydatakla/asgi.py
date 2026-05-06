

import os

from django.core.asgi import get_asgi_application  # pyright: ignore[reportMissingModuleSource]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydatakla.settings")

application = get_asgi_application()
app = application
