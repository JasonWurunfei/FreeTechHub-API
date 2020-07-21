from rest_framework.serializers import ModelSerializer
from .models import Question

class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = [
            "id", "title", "content",
            "date",  "owner", "viewTimes",
            "bounty","status"
        ]
        