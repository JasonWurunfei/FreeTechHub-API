from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

# Create your models here.
class Series(models.Model):
    name        = models.CharField(max_length=40)
    description = models.TextField()
    date        = models.DateTimeField(auto_now=True)
    viewTimes   = models.IntegerField(default=0, blank=True)

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='series',
                                    on_delete=models.CASCADE)

    sub_series_of = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      related_name="sub_series",
                                      blank=True,
                                      null=True,)



class Blog(models.Model):
    title       = models.CharField(max_length=40)
    content     = models.TextField()
    date        = models.DateTimeField(auto_now=True)
    viewTimes   = models.IntegerField(default=0, blank=True)

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='blogs',
                                    on_delete=models.CASCADE)

    series      = models.ForeignKey(Series,
                                    related_name='blogs',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

    tags        = GenericRelation(Tag, related_query_name='blog')
