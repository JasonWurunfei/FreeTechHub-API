from django.urls import path, include
from rest_framework import routers
from .views import TagViewSet, QueryByTagView, SaveTagsView

router = routers.DefaultRouter()
router.register('tag', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query/', QueryByTagView.as_view()),
    path('saveTags/', SaveTagsView.as_view()),
]
