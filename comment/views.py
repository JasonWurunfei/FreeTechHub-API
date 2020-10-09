from django.shortcuts import render
from rest_framework import viewsets
from .serializers import  CommentSerializer
from .models import Comment
from user.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from websocket.middleware import live_sockects
from asgiref.sync import async_to_sync
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def create(self, request, *args, **kwargs):
        data = {
            'content': request.data['content'],
            'owner' : request.user.id,
        }
        sub_comments_of = request.data.get('sub_comments_of')

        if sub_comments_of is not None:
            data.update({'sub_comments_of': sub_comments_of})
        
        if request.data.get('csrfmiddlewaretoken') is not None:
            data.update({'csrfmiddlewaretoken': request.data['csrfmiddlewaretoken']})

        serializer = self.get_serializer(data=data)
        if sub_comments_of != None:
            try:
                parentComment = Comment.objects.get(id=data['sub_comments_of'])
            except Comment.DoesNotExist:
                parentComment = None
            
            if parentComment != None:
                receiver = parentComment.owner
                socket = live_sockects.get_socket(receiver.pk)
            
            if socket != None:
                async_to_sync(socket.send_json)({"type": "reply"})
            

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class QueryView(APIView):
    @staticmethod
    def get_serialized_sub_comments(comment, request):
        serialized_sub_trees = []
        if len(comment.sub_comment_models) == 0:
            return {
                "comment": CommentSerializer(comment, context={"request": request}).data,
                "serialized_sub_trees": serialized_sub_trees
            }
        

        for sub_comment in comment.sub_comment_models:
            sub_tree_list = QueryView.get_serialized_sub_comments(sub_comment, request)
            serialized_sub_trees.append(sub_tree_list)
        
        comment_dict = {
            "comment": CommentSerializer(comment, context={"request": request}).data,
            "serialized_sub_trees": serialized_sub_trees
        }
        
        return comment_dict

    def get(self, request, format=None, **kwargs):
        root_comment_id = self.request.query_params.get('id', None)
        root_comment = Comment.objects.get(id=root_comment_id)
        comment_dict = QueryView.get_serialized_sub_comments(root_comment, request)
        return Response(comment_dict)
    