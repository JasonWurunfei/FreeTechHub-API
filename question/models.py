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
    tags = GenericRelation(Tag, related_query_name='question')
    

class Answer(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
