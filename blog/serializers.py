from rest_framework import serializers
from .models import Blog, Series
from tag.serializers import TagSerializer
from comment.serializers import CommentSerializer
from user.serializers import UserSerializer

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    owner_instance = UserSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = [ "id", "title", "content",
                   "date", "view_num", "owner",
                   "series", "tags", "like_num",
                   "dislike_num", "content_type_id",
                   "root_comment", "owner_instance", "background_image"]
        
        extra_kwargs = {
            'like_num':        {'read_only': True},
            'dislike_num':     {'read_only': True},
            'view_num':        {'read_only': True},
            'content_type_id': {'read_only': True}
        }


class SeriesSerializer(serializers.ModelSerializer):
    blogs = BlogSerializer(many=True, required=False)

    class Meta:
        model = Series
        fields = [ 
            "id", "name", "description",
            "date", "viewTimes", "owner", 
            "sub_series_of", "sub_series", "blogs"
        ]
        extra_kwargs = {
            'sub_series': {'read_only': True}
        }
