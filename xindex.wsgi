import os, sys
sys.path.append('/home/osvaldo/PycharmProjects/xindex/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'growthfactor.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
