from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from like.models import Like
from tag.models import Tag
from comment.models import Comment
from blog.models import View

class Question(models.Model):
    title       = models.CharField(max_length=50)
    content     = models.TextField()
    date        = models.DateTimeField(auto_now=True)
    bounty      = models.PositiveIntegerField(default=0)
    viewTimes   = models.IntegerField(default=0, blank=True)
    status      = models.BooleanField(default=False)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    tags        = GenericRelation(Tag, related_query_name='question')
    background_image = ProcessedImageField(upload_to=settings.QUESTION_DIR,
                                  processors=[ResizeToFill(100,100)],
                                  default='question/default.png',
                                  verbose_name='question',)
    
    @property
    def owner_instance(self):
        return self.owner

    @property
    def content_type(self):
        return ContentType.objects.get(app_label='question', model='question')

    @property
    def content_type_id(self):
        return self.content_type.id
    
    @property
    def view_num(self):
        return View.objects.filter(content_type=self.content_type,
                                   object_id=self.id).count()

class Answer(models.Model):
    content         = models.TextField()
    time            = models.DateTimeField(auto_now=True)
    status          = models.BooleanField(default=False)
    
    owner           = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name='answers',
                                        on_delete=models.CASCADE)

    question        = models.ForeignKey(Question, related_name='answers',
                                        on_delete=models.CASCADE)

    root_comment    = models.ForeignKey(Comment, related_name='root_comment',
                                        null=True, on_delete=models.CASCADE)


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
    def owner_instance(self):
        return self.owner
    