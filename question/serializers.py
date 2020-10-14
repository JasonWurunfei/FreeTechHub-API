from rest_framework import serializers
from .models import Question,Answer
from tag.serializers import TagSerializer
from user.serializers import UserSerializer
        
class AnswerSerializer(serializers.ModelSerializer):
    owner_instance = UserSerializer(read_only=True)
    like_num = serializers.IntegerField(read_only=True)
    dislike_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "content", "time", "status",
                  "owner", "owner_instance", "question", "content_type_id",
                  "like_num","dislike_num", "score","root_comment"]

        extra_kwargs = {
            'like_num':         {'read_only': True},
            'dislike_num':      {'read_only': True},
            'score':            {'read_only': True},
            'owner_instance':   {'owner_instance': True},
        }

class QuestionSerializer(serializers.ModelSerializer):
    owner_instance = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, required=False)
    bounty = serializers.IntegerField(required=False)
    
    class Meta:
        model = Question
        fields = [
            "id", "title", "content",
            "date", "viewTimes", "owner",
            "owner_instance", "status", "bounty",
            "tags", "answers", "content_type_id",
            "view_num", "background_image"]
        extra_kwargs = {
            'owner_instance':   {'read_only': True},
            "background_image": {"allow_empty_file": True},
        }