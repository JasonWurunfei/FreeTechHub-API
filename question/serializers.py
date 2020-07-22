from rest_framework.serializers import ModelSerializer
from .models import Question,Answer
from tag.serializers import TagSerializer

class QuestionSerializer(ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Question
        fields = [
            "id", "title", "content", "date",
            "bounty", "viewTimes", "status", "owner",
            "tags"
        ]

class AnswerSerializer(ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
