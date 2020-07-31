from django.shortcuts import render
from .models import Like
from .serializers import LikeSerializer
from rest_framework import viewsets

# Create your views here.
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
