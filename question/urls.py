from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet

router = routers.DefaultRouter()
router.register('question', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
