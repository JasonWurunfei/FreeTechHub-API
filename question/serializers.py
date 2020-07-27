from rest_framework import serializers
from .models import Question,Answer
from tag.serializers import TagSerializer
        
class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ["content", "time", "status", "owner", "question"]

class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = ["id", "title", "content", "date", "viewTimes",
        "owner", "status", "bounty", "tags", "answers"]
