from django.urls import path, include
from rest_framework import routers
from question import views

router = routers.DefaultRouter()
router.register('question', views.QuestionViewSet)
router.register('answer', views.AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('query-related-content/', views.QueryViewSet.as_view()),
    path('sorted-answers/', views.SortedAnswersViewSet.as_view())
]