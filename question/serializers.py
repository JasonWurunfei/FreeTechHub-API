from rest_framework import serializers
from .models import Question,Answer
from tag.serializers import TagSerializer
        
class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Question
        fields = '__all__'
