from pathlib import Path

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1c0j8auewfm#pazumw0(u(@r#8t!qdo*^6n_qmx+o1n_d=no&g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

BASE_DIR = Path(__file__).resolve().parent.parent
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': Path.joinpath(BASE_DIR, 'db.sqlite3'),
    }
}

REAL_IDM = {
    'LDAP_SERVER': "",          # required, server address e.g. '192.168.1.1'
    'SEARCH_BASE': "",          # required, where the groups and users are located e.g. 'dc=win,dc=local'
    'BIND_USER': "",            # optional, bind user e.g. bind@win.local
    'BIND_PASSWD': "",          # optional
    'LDAP_USER_ATTRIBUTE': ""   # optional, mapping for User.username and AD attribute name used to search the user from AD. Defaults to 'sAMAccountName'
}
