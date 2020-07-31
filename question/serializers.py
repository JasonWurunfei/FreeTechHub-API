from rest_framework import serializers
from .models import Question,Answer
from tag.serializers import TagSerializer
        
class AnswerSerializer(serializers.ModelSerializer):
    like_num = serializers.IntegerField(read_only=True)
    dislike_num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "content", "time", "status",
                  "owner", "question", "like_num",
                  "dislike_num"]

class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    answers = AnswerSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = ["id", "title", "content", "date", "viewTimes",
        "owner", "status", "bounty", "tags", "answers"]
