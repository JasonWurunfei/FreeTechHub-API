from .models import User
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, FollowershipSerializer
from .serializers import FriendRequestSerializer, FriendshipSerializer
from .models import User, Followership, FriendRequest, Friendship
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class GetSelfView(APIView):
    """
    get the request user model
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class FollowershipViewSet(viewsets.ModelViewSet):
    queryset = Followership.objects.all()
    serializer_class = FollowershipSerializer
    permission_classes = [
            IsAuthenticated,
        ]


class FollowershowView(APIView):
    renderer_classes = [JSONRenderer]

# Gets a list of follower for the relevant user
    def get(self, request, format=None):
        response = {'status': 100, 'data': None}
        user = self.request.user
        followers = Followership.objects.filter(following_id=user.id)
        followerList = []
        for follower in followers:
            followerList.append({'follower_name':follower.follower.username,
            'user_bio':follower.follower.bio,'id':follower.follower.pk})
        response['data'] = followerList
        return JsonResponse(response, safe=False)


class FollowingshowView(APIView):
    renderer_classes = [JSONRenderer]

# Gets a list of following for the relevant user
    def get(self, request, format=None):
        response = {'status': 100, 'data': None}
        user = self.request.user
        followings = Followership.objects.filter(follower_id=user.id)

        followingList = []
        for following in followings:
            followingList.append({'following_id':following.id,
            'following_name':following.following.username,
            'user_bio':following.following.bio,'id':following.following.pk})
        response['data'] = followingList
        return JsonResponse(response, safe=False)


class ChangePasswordView(APIView):
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer]

    # ChangePassword
    def post(self, request, format=None):
        response = {'status': 100, 'data': None}
        data = request.data
        old_password = data.get('oldpassword')
        new_password = data.get('newpassword1')
        user = self.request.user
        if user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            context = {
                "status": 100,
                "msg": "successful"
            }
        else:
            context = {
                "status": 500,
                "msg": "error"
            }
        response['data'] = context
        return JsonResponse(response, safe=False)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer


class GetRequestView(APIView):

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id)
        all_requests = FriendRequest.objects.filter(to_user_id=request.user.id,
        is_cancel=False)
        all_related_request = {}
        all_related_request['request'] = [FriendRequestSerializer(request).data for request in all_requests]
        return Response(all_related_request)


class GetFriendView(APIView):

    def get(self, request, format=None):
        user = User.objects.filter(id=request.user.id)
        all_friend1lists = Friendship.objects.filter(friend_1=request.user.id)
        all_friend2lists = Friendship.objects.filter(friend_2=request.user.id)
        all_friendlists = all_friend1lists | all_friend2lists
        all_related_friendlists = []

        #  Gets a list of friends for the relevant user
        for all_friendlist in all_friendlists:
            if(all_friendlist.friend_1.id == request.user.id):
                all_related_friendlists.append({
                'all_friendlist':FriendshipSerializer(all_friendlist).data,
                 'related_user':UserSerializer(all_friendlist.friend_2).data})
            else:
                all_related_friendlists.append({
                'all_friendlist':FriendshipSerializer(all_friendlist).data,
                'related_user':UserSerializer(all_friendlist.friend_1).data})

        return Response(all_related_friendlists)
