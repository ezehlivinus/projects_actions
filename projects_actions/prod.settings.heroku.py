from .settings import *

import django_heroku

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

django_heroku.settings(locals())