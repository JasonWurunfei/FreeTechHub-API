from django.urls import path, include
from rest_framework import routers
from .views import QuestionViewSet, AnswerViewSet,  QueryViewSet

router = routers.DefaultRouter()
router.register('question', QuestionViewSet)
router.register('answer', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('query-related-content/', QueryViewSet.as_view()),
]