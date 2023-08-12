import sys, os

DOMAIN = "domeen.ee" # Teie domeeni nimi (ilma www.-ta)

APPNAME = "djangoveeb" # Django applikatsiooni nimi

PREFIX = "/www/apache/domains/www.%s" % (DOMAIN,)

# Add a custom Python path.

sys.path.insert(0, os.path.join(PREFIX, APPNAME))

sys.path.insert(0, os.path.join(PREFIX, ".virtualenvs/website/lib/python2.7/site-packages/"))

# Switch to the directory of your project. (Optional.)

os.chdir(os.path.join(PREFIX, APPNAME))

# Set the DJANGO_SETTINGS_MODULE environment variable.

os.environ['DJANGO_SETTINGS_MODULE' ] = "%s.settings" % (APPNAME,)

import django

django.setup()

from flup.server.fcgi import WSGIServer

from django.core.handlers.wsgi import WSGIHandler

WSGIServer(WSGIHandler()).run()