from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BlogSerializer, SeriesSerializer
from .models import Blog, Series, View
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from comment.models import Comment


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

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

        root_comment = Comment.objects.create(content='', owner=request.user, sub_comments_of=None)
        data.update({'root_comment': root_comment.id})
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


class UpdateSelectedView(APIView):
    """
    This view will update the foreign key of sub series
    or related blogs of one series
    """
    def post(self, request, *args, **kwargs):

        series = Series.objects.get(id=request.data['series'])
        selected_blogs = request.data['selected_items']['blog']
        selected_series = request.data['selected_items']['series']

        # if it recursively selected itself, remove it.
        if series.id in selected_series:
            selected_series.remove(series.id)

        # If related_blogs and related_series is not empty, it means
        # that this view is called when editing an existing series

        # remove not selected blogs but used to be in that series
        related_blogs = Blog.objects.filter(series=series)
        for blog in related_blogs:
            if blog.id not in selected_blogs:
                blog.series = None          # point the foreign key to null to remove
                blog.save()

        # remove not selected series but used to be in that series
        related_series = Series.objects.filter(sub_series_of=series)
        for sub_series in related_series:
            if sub_series.id not in selected_series:
                sub_series.sub_series_of = None # point the foreign key to null to remove
                sub_series.save()

        # add selected blogs
        for blog_id in selected_blogs:
            blog = Blog.objects.get(id=blog_id)
            blog.series = series
            blog.save()

        # add selected series
        for series_id in selected_series:
            sub_series = Series.objects.get(id=series_id)
            sub_series.sub_series_of = series
            sub_series.save()

        return Response(SeriesSerializer(series).data)
