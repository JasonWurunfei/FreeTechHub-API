from django.shortcuts import render
from rest_framework import viewsets
from django.conf import settings
from .serializers import QuestionSerializer,AnswerSerializer
from .models import Question, Answer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from comment.models import Comment
from .pagination import Pagination
from blog.models import View
import datetime
import os

# Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthenticatedOrReadOnly,
    ]
    pagination_class = Pagination

    """
    Overide retrieve to support count view number.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            View.objects.get(user=request.user,
                             content_type=instance.content_type,
                             object_id=instance.id)
        except View.DoesNotExist:
            View.objects.create(user=request.user,
                                content_type=instance.content_type,
                                object_id=instance.id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthenticatedOrReadOnly,
    ]

    def create(self, request, *args, **kwargs):
        data = {
            'content':request.data['content'],
            'status': False,
            'owner' : request.user.id,
            'content': request.data['content'],
        }
        if request.data.get('question') is not None:
            data.update({'question': request.data['question']})

        if request.data.get('csrfmiddlewaretoken') is not None:
            data.update({'csrfmiddlewaretoken': request.data['csrfmiddlewaretoken']})

        root_comment = Comment.objects.create(content='', owner=request.user, sub_comments_of=None)
        data.update({'root_comment': root_comment.id})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class QueryViewSet(APIView):
    def get(self, request, format=None, **kwargs):
        request_user = self.request.query_params.get('request_user', None)
        questions = Question.objects.filter(owner=request_user)
        return Response(QuestionSerializer(questions, many=True).data)

class SortedAnswersViewSet(APIView):
    @staticmethod
    def getScore(answer):
        return answer['score']

    def get(self, request, format=None, **kwargs):
        question_id = self.request.query_params.get('question_id', None)
        answers = Answer.objects.filter(question=question_id)
        list = []
        for answer in answers:
            list.append(AnswerSerializer(answer, context={"request": request}).data)
        list.sort(reverse=True, key=SortedAnswersViewSet.getScore)
        return Response(list)
