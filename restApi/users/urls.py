from django.conf.urls.defaults import *
from piston.resource import Resource
from users.views import UserView, UserViewRoot

urlpatterns = patterns('',
   url(r'^(?P<user_id>[^/]+)$',
        UserView.as_view(),
        name='user'),
   url(r'^$',
        UserViewRoot.as_view(),
        name='user_root'),
)