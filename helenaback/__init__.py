from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth import create_superuser
from django.db.models import signals
   
signals.post_syncdb.disconnect(
    create_superuser,
    sender="this",
    dispatch_uid='django.contrib.auth.management.create_superuser')

# Create our own test user automatically.

def create_testuser(app, created_models, verbosity, **kwargs):
    if not settings.DEBUG:
        return
    try:
        auth_models.User.objects.get(username='helena')
    except auth_models.User.DoesNotExist:
        print '*' * 80
        print 'Creating test user -- login: helena, password: helena'
        print '*' * 80
        assert auth_models.User.objects.create_superuser('helena', 'x@x.com', 'helena')
    else:
        print 'Test user already exists.'

signals.post_syncdb.connect(create_testuser,
    sender=auth_models, dispatch_uid='helena.create_testuser')