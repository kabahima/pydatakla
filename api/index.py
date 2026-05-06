import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pydatakla.settings')

try:
    from django.core.wsgi import get_wsgi_application  # noqa: E402
    app = get_wsgi_application()
except Exception as e:
    logger.error(f"Failed to initialize Django WSGI application: {e}", exc_info=True)
    
    # Fallback WSGI app for debugging
    def app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [b'Django initialization failed. Check logs for details.']
