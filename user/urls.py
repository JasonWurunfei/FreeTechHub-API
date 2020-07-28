from django.urls import path, include
from rest_framework import routers
from user  import views
from .views import UserViewSet, GetSelfView, FollowershipViewSet,FollowingshowView

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('followership',FollowershipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getself/', GetSelfView.as_view()),
    path('getfollowing/', views.FollowingshowView.as_view()),
    path('getfollower/', views.FollowershowView.as_view())
]
