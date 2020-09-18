from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Like(models.Model):
    date            = models.DateTimeField(auto_now_add=True)
    like_type       = models.BooleanField(default=True)         # 1 -> like, 0 -> dislike
    user            = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE)

    limit = models.Q(app_label='blog',      model='blog') | \
            models.Q(app_label='question',  model='answer') | \
            models.Q(app_label='skilltree', model='skilltree') | \
            models.Q(app_label='skilltree', model='modifyrequest')

    content_type    = models.ForeignKey(ContentType,
                                        on_delete=models.CASCADE,
                                        limit_choices_to=limit)

    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
