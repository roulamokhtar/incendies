#######
import dj_database_url
from .settings import *
DEBUG = True
DATABASES['default'].update(dj_database_url.config())
SECRET_KEY = '2n-j0(*@!!!1)87l!*7l#jme&g_w(c)b6zteg9(w7mf2^#m&ju'
ALLOWED_HOSTS = ['incendies.herokuapp.com']