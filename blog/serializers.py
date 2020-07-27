from rest_framework import serializers
# from tag.serializers import TagToTaggedItemSerializer
from .models import Blog, Series
from tag.serializers import TagSerializer

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = [ "id", "title", "content",
            "date", "viewTimes", "owner",
            "series", "tags"]


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
