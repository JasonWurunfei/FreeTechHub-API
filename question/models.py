from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from like.models import Like
from tag.models import Tag
from comment.models import Comment

class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    bounty = models.PositiveIntegerField(default=0)
    viewTimes = models.IntegerField(default=0, blank=True)
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE)
    tags = GenericRelation(Tag, related_query_name='question')
    
    @property
    def owner_instance(self):
        return self.owner

class Answer(models.Model):
    content = models.TextField()
    time = models.DateTimeField(auto_now=True) 
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    root_comment = models.ForeignKey(Comment, related_name='root_comment', null=True, on_delete=models.CASCADE)

    @property
    def content_type(self):
        return ContentType.objects.get(app_label='question', model='answer')
    
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
    def owner_instance(self):
        return self.owner
    