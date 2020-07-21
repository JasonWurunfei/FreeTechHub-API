from rest_framework import serializers
# from tag.serializers import TagToTaggedItemSerializer
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    # tags = TagToTaggedItemSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = [
            "id", "title", "content",
            "date", "viewTimes", "owner"
        ]
