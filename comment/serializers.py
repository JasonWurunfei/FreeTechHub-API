from rest_framework import serializers
from .models import Comment
from user.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    owner_instance = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "time", "owner", "owner_instance", "sub_comments_of","sub_comments"]
        extra_kwargs = {
            'sub_comments': {'read_only': True}
        }
