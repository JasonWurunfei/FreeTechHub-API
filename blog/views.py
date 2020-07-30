from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BlogSerializer, SeriesSerializer
from .models import Blog, Series
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
            'owner' : request.user.id,
        }
        if request.data.get('series') is not None:
            data.update({'series': request.data['series']})

        if request.data.get('csrfmiddlewaretoken') is not None:
            data.update({'csrfmiddlewaretoken': request.data['csrfmiddlewaretoken']})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]


class QueryView(APIView):
    """
    This view should return a list of all the blogs or series which 
    are belong to the requesting user.
    """
    def get(self, request, format=None, **kwargs):
        blogs = Blog.objects.filter(owner=request.user)
        all_series = Series.objects.filter(owner=request.user)
        user_related_content = {}
        user_related_content['blog'] = [BlogSerializer(blog).data for blog in blogs]
        user_related_content['series'] = [SeriesSerializer(series).data for series in all_series]
        return Response(user_related_content)
