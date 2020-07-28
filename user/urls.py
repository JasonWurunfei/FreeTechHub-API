from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, GetSelfView, FollowershipViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('followership',FollowershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getself/', GetSelfView.as_view())
]
