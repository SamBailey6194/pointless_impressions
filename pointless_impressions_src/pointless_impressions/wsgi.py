"""
WSGI config for pointless_impressions project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'pointless_impressions_src.pointless_impressions.settings.dev'
    )

application = get_wsgi_application()
