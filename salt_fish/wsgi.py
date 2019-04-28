"""
WSGI config for salt_fish project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
BASE_DIR = "/home/cqh/python_project_dir/salt_fish/"
sys.path.append(BASE_DIR)
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salt_fish.settings")

application = get_wsgi_application()
