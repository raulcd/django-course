from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^categories/', 'videoclub.views.categoriesTemplate'),
    (r'^videos/', 'videoclub.views.videosRest'),
)
