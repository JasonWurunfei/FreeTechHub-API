from django.urls import path, include
from rest_framework import routers
from .views import BlogViewSet, SeriesViewSet, QueryView

router = routers.DefaultRouter()
router.register('blog', BlogViewSet)
router.register('series', SeriesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query-related-content/', QueryView.as_view()),
]
