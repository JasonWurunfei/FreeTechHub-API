from django.db import models
from django.conf import settings

# Create your models here.
class Blog(models.Model):
    title       = models.CharField(max_length=40)
    content     = models.TextField()
    date        = models.DateTimeField(auto_now=True)
    viewTimes   = models.IntegerField(default=0, blank=True)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs', on_delete=models.CASCADE)