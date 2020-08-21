from django.urls import path, include
from rest_framework import routers
from user  import views


router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('followership', views.FollowershipViewSet)
router.register('friendrequest', views.FriendRequestViewSet)
router.register('friendship', views.FriendshipViewSet)
router.register('message', views.MessageViewSet)
router.register('emailvalid',views.EmailValidViewSet)
router.register('chat', views.ChatViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('getself/', views.GetSelfView.as_view()),
    path('getfollowing/', views.FollowingshowView.as_view()),
    path('getfollower/', views.FollowershowView.as_view()),
    path('changepassword/', views.ChangePasswordView.as_view()),
    path('changeemail/', views.ChangeEmailView.as_view()),
    path('checkchangeemail/', views.CheckChangeemailView.as_view()),
    path('getrequests/<int:user_id>/', views.GetFriendRequestsView.as_view()),
    path('get_received_requests/<int:user_id>/', views.GetReceivedFriendRequestsView.as_view()),
    path('getfriends/<int:user_id>/', views.GetFriendsView.as_view()),
    path('getchat/', views.GetChatView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('validate/', views.ValidateCodeView.as_view()),
    path('send_change/', views.Send_changepassword.as_view()),
    path('resetpassword/', views.ResetPasswordView.as_view()),
    path('checkpassword/', views.CheckPasswordView.as_view()),
    path('checkrepeat/', views.CheckRepeatView.as_view()),
    path('upload/', views.UploadView.as_view()),
    path('gettags/<int:user_id>/', views.GetSelftags.as_view()),

]
