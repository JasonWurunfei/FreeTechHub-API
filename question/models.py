from django.db import models
from django.conf import  settings

class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    time = models.DateTimeField(auto_now=True)
    rewarded_money = models.PositiveIntegerField(default=0)
    viewTimes = models.IntegerField(default=0, blank=True)
    note = models.CharField(max_length=50, null=True, blank=True)
    status = models.BooleanField(default=False)
    question_type = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    