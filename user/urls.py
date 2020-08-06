from django.urls import path, include
from rest_framework import routers
from user  import views
from .views import UserViewSet, GetSelfView, FollowershipViewSet
from .views import FollowingshowView, ChangePasswordView, FriendRequestViewSet
from .views import GetRequestView, FriendshipViewSet, GetFriendView

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('followership',FollowershipViewSet)
router.register('friendrequest',FriendRequestViewSet)
router.register('friendship',FriendshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getself/', GetSelfView.as_view()),
    path('getfollowing/', views.FollowingshowView.as_view()),
    path('getfollower/', views.FollowershowView.as_view()),
    path('changepassword/', views.ChangePasswordView.as_view()),
    path('getrequest/', views.GetRequestView.as_view()),
    path('getfriendlists/', views.GetFriendView.as_view()),
]
