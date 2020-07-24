from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BlogSerializer
from .models import Blog
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def create(self, request, *args, **kwargs):
        data = {
            'title': request.data['title'],
            'content': request.data['content'],
            'viewTimes': 0,
            'owner' : request.user.id
        }
        if request.data['csrfmiddlewaretoken'] is not None:
            data.update({'csrfmiddlewaretoken': request.data['csrfmiddlewaretoken']})
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
