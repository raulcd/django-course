from django.conf.urls.defaults import *
from piston.resource import Resource
from users.views import *
from piston.authentication import HttpBasicAuthentication

user_resource = Resource(handler=UserHandler)

urlpatterns = patterns('',
   # Response content type: json
   url(r'^(?P<user_id>[^/]+)$', user_resource, {'emitter_format': 'json'}),
   url(r'^$', user_resource, {'emitter_format': 'json'}),
)