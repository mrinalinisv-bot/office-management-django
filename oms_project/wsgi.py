import os
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oms_project.settings')

application = get_wsgi_application()

# Automatically apply database migrations on server boot
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    logging.getLogger(__name__).warning("Startup migration notice: %s", e)
