from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Like
from .serializers import LikeSerializer
from rest_framework import viewsets
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeView(APIView):
    """
    This view will handle users' like or dislike request
    update rule:
        a. if this user liked this content before
            1) ask for like again   => unlike the content
            2) ask for dislike      => unlike the content, and dislike the content

        b. if this user disliked this content before
            1) ask for dislike again => undislike the content
            2) ask for like          => undislike the content, and like the content
    """

    def post(self, request, format=None, **kwargs):

        data = request.data
        item_type = ContentType.objects.get(id=data['content_type'])

        
        likes = Like.objects.filter(user=request.user,
                                    content_type=item_type,
                                    object_id=data['object_id'])
        
        data = {
            "user"          : request.user.id,
            "content_type"  : item_type.id,
            "like_type"     : data['like_type'],
            "object_id"     : data['object_id']
        }

        # try to find if this user done this item before
        done = False if len(likes.filter(like_type=data['like_type'])) == 0 else True
        
        # delete old records if they exist.
        if likes: # i.e. if likes is not empty
            for like in likes:
                like.delete()
        
        if not done:    # if not done yet, create new record
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:           # done it before, undo it
            return Response("Undo success!", status=status.HTTP_200_OK)


class LikeHistoryView(APIView):
    """
    This view will show whether this user liked or disliked
    the content or neither.
    """
    def get(self, request, format=None, **kwargs):
        content_type = request.query_params.get('content_type', None)
        object_id = request.query_params.get('object_id', None)

        item_type = ContentType.objects.get(id=content_type)
        try:
            like = Like.objects.get(user=request.user,
                                    content_type=item_type,
                                    object_id=object_id)
            
            history = "liked" if like.like_type == True else "disliked"
            return Response(history, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response("none", status=status.HTTP_200_OK)

