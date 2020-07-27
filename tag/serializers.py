from rest_framework import serializers
from .models import Tag
from django.contrib.contenttypes.models import ContentType

class TagSerializer(serializers.ModelSerializer):

    def validate_content_type(self, value):
        """
        Limit the content type to only blog and question
        """

        if value != ContentType.objects.get(app_label='blog', model='blog') and \
           value != ContentType.objects.get(app_label='question', model='question'):
           raise serializers.ValidationError("Tagged object can only be blog or question.")

        return value

    def validate_object_id(self, value):
        """
        Check if the tagged object is exist
        """
        tagged_item_type = ContentType.objects.get(
            id=self.initial_data['content_type']).model_class()
        try:
            obj = tagged_item_type.objects.get(id=value)
        except Blog.DoesNotExist:
            raise serializers.ValidationError("Tagged blog does not exsit.")
        except Question.DoesNotExist:
            raise serializers.ValidationError("Tagged blog does not exsit.")

        return value

    class Meta:
        model = Tag
        fields = "__all__"

