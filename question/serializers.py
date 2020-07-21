from rest_framework.serializers import ModelSerializer
from .models import Question

class QuestionSerializer(ModelSerializer):

    class Meta:
        model = Question
        fields = [
            "id", "title", "content",
            "date", "viewTimes", "owner",
            "rewarded_money","note","status",
            "question_type",'tags'
        ]
        