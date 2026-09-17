"""
WSGI config for EcoShare Tashkent project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecoshare.settings")

application = get_wsgi_application()