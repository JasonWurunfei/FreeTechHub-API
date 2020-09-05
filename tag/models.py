from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Tag(models.Model):
    limit = models.Q(app_label='blog',      model='blog') | \
            models.Q(app_label='question',  model='question')
    
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to=limit)

    object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey('content_type', 'object_id')

    tag_name = models.CharField(max_length=30)

    def __str__(self):
        return f"<Tag {self.id}: {self.tag_name}>"
