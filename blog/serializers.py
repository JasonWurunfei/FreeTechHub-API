from rest_framework import serializers
from .models import Blog, Series
from tag.serializers import TagSerializer

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    like_num = serializers.IntegerField(read_only=True)
    dislike_num = serializers.IntegerField(read_only=True)
    content_type_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Blog
        fields = [ "id", "title", "content",
            "date", "viewTimes", "owner",
            "series", "tags", "like_num",
            "dislike_num", "content_type_id"]


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
