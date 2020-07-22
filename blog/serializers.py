from rest_framework import serializers
# from tag.serializers import TagToTaggedItemSerializer
from .models import Blog
from tag.serializers import TagSerializer

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = [ "id", "title", "content",
            "date", "viewTimes", "owner", 'tags']
