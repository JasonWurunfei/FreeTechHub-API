from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, QueryByTagView

router = routers.DefaultRouter()
router.register('tag', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query/', QueryByTagView.as_view()),
]
