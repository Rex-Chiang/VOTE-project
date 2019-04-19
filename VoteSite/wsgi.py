import os
import sys

path = '/home/rexsite/VoteSite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'VoteSite.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()