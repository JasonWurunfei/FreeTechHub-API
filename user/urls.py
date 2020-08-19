from django.urls import path, include
from rest_framework import routers
from user  import views


router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('followership', views.FollowershipViewSet)
router.register('friendrequest', views.FriendRequestViewSet)
router.register('friendship', views.FriendshipViewSet)
router.register('message', views.MessageViewSet)
router.register('chat', views.ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getself/', views.GetSelfView.as_view()),
    path('getfollowerships/<int:user_id>/', views.FollowershipListView.as_view()),
    path('unfollow/', views.UnfollowView.as_view()),
    path('followship_check/<int:follower_id>/<int:following_id>/',
          views.FollowershipCheckView.as_view()),
    path('changepassword/', views.ChangePasswordView.as_view()),
    path('getrequests/<int:user_id>/', views.GetFriendRequestsView.as_view()),
    path('get_received_requests/<int:user_id>/', views.GetReceivedFriendRequestsView.as_view()),
    path('getfriends/<int:user_id>/', views.GetFriendsView.as_view()),
    path('getchat/', views.GetChatView.as_view()),
]
