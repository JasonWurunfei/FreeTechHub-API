from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from tag.models import Tag
from like.models import Like
from comment.models import Comment

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

    owner       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='blogs',
                                    on_delete=models.CASCADE)

    series      = models.ForeignKey(Series,
                                    related_name='blogs',
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL)

    root_comment = models.ForeignKey(Comment,
                                     related_name='special_comment',
                                     null=True,
                                     on_delete=models.CASCADE)

    tags        = GenericRelation(Tag, related_query_name='blog')

    background_image = ProcessedImageField(upload_to=settings.BLOG_DIR,
                                  default='blog/default.png',
                                  verbose_name='blog',)

    @property
    def content_type(self):
        return ContentType.objects.get(app_label='blog', model='blog')

    @property
    def content_type_id(self):
        return self.content_type.id

    @property
    def like_num(self):
        return Like.objects.filter(content_type=self.content_type,
                                   object_id=self.id,
                                   like_type=True).count()

    @property
    def dislike_num(self):
        return Like.objects.filter(content_type=self.content_type,
                                   object_id=self.id,
                                   like_type=False).count()

    @property
    def view_num(self):
        return View.objects.filter(content_type=self.content_type,
                                   object_id=self.id).count()

    @property
    def owner_instance(self):
        return self.owner


class View(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    limit = models.Q(app_label='blog',      model='blog') | \
            models.Q(app_label='question',  model='question')

    content_type    = models.ForeignKey(ContentType,
                                        on_delete=models.CASCADE,
                                        limit_choices_to=limit)

    object_id       = models.PositiveIntegerField()
    content_object  = GenericForeignKey('content_type', 'object_id')
