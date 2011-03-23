from django.contrib import admin
from videoclub.models import *

admin.site.register(Video)
admin.site.register(Category)
admin.site.register(WatchedBy)