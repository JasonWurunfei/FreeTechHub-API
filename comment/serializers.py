from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "content", "time", "status", "owner","sub_comments_of","sub_comments"]
        extra_kwargs = {
            'sub_comments': {'read_only': True}
        }
