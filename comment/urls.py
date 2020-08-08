from django.urls import path, include
from rest_framework import routers
from .views import CommentViewSet, QueryView

router = routers.DefaultRouter()
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query/', QueryView.as_view())
]
