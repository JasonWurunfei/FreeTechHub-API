from rest_framework import serializers
from .models import Tag
from blog.models import Blog
from blog.serializers import BlogSerializer

class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Blog):
            data = {
                'contenttype': 'blog',
                'id': value.id,
                'title': value.title,
                'content': value.content,
                'date': value.date,
                'viewTimes': value.viewTimes,
                'owner_id': value.owner.id
            }
            return data
        raise Exception('Unexpected type of tagged object')

class TagSerializer(serializers.ModelSerializer):
    tagged_object = TaggedObjectRelatedField(read_only=True)
    class Meta:
        model = Tag
        fields = ["id", "tagged_object", "tag_name"]
