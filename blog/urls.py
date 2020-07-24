from django.urls import path, include
from rest_framework import routers
from .views import BlogViewSet, SeriesViewSet

router = routers.DefaultRouter()
router.register('blog', BlogViewSet)
router.register('series', SeriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
