from rest_framework import serializers
from .models import Like
from blog.models import Blog
from question.models import Answer
from skilltree.models import SkillTree, ModifyRequest
from django.contrib.contenttypes.models import ContentType


class LikeSerializer(serializers.ModelSerializer):

    def validate_object_id(self, value):
        """
        Check if the liked object is exist
        """
        liked_item_type = ContentType.objects.get(
            id=self.initial_data['content_type']).model_class()
        try:
            obj = liked_item_type.objects.get(id=value)
        except Blog.DoesNotExist:
            raise serializers.ValidationError("liked blog does not exsit.")
        except Answer.DoesNotExist:
            raise serializers.ValidationError("agreed answer does not exsit.")
        except SkillTree.DoesNotExist:
            raise serializers.ValidationError("voted skilltree does not exsit.")
        except SkillTree.DoesNotExist:
            raise serializers.ValidationError("voted modify request does not exsit.")

        return value

    class Meta:
        model = Like
        fields = "__all__"
        extra_kwargs = {
            'like_type': { "initial": True }
        }
