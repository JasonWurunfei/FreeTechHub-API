from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('like', views.LikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('like-item/', views.LikeView.as_view()),
    path('like-history/', views.LikeHistory.as_view()),
]
