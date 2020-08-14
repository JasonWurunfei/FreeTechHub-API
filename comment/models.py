from django.db import models
from django.conf import settings

class Comment(models.Model):
    content = models.TextField(default='', blank=True)
    time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commentors', on_delete=models.CASCADE)
    sub_comments_of = models.ForeignKey('self', on_delete=models.CASCADE,
                                      related_name="sub_comments",
                                      null=True)
    @property
    def sub_comment_models(self):
        return Comment.objects.filter(sub_comments_of=self.id)
