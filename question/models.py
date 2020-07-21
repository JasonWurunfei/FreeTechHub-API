from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    bounty = models.PositiveIntegerField(default=0)
    viewTimes = models.IntegerField(default=0, blank=True)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    tags = GenericRelation(Tag)
    