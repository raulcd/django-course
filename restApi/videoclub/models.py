from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import get_language, ugettext as _

class Video(models.Model):
    name = models.CharField(_('Name'), max_length=150, unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    viewers = models.ManyToManyField(User, through="WatchedBy")
    creator = models.ForeignKey(User, related_name="video_creator")
    
    
    def __unicode__(self):
        return unicode(self.name)
    

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    videos = models.ManyToManyField(Video)
    
    def __unicode__(self):
        return unicode(self.name)
    
    
class WatchedBy(models.Model):
    user = models.ForeignKey(User)
    video = models.ForeignKey(Video)
    date = models.DateTimeField(_('First watch'))
    times = models.IntegerField(_('Times'), default=1)
    
    class Meta:
        unique_together = ("user","video")
    
    def __unicode__(self):
        return unicode(self.video) + " watched by " + unicode(self.user)