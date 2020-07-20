from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, GetSelfView

router = routers.DefaultRouter()
router.register('user', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('getself/', GetSelfView.as_view())
]