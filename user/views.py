from .models import User
from .serializers import UserSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserSerializer,FollowershipSerializer
from .models import User, Followership
from django.http import JsonResponse
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
    def get(self, request, format=None):
        response = {'status': 100, 'data': None}
        user = self.request.user
        followers = Followership.objects.filter(following_id=user.id)
        followerList = []
        for follower in followers:
            followerList.append({'follower_name':follower.follower.username,'user_bio':follower.follower.bio})
        response['data'] = followerList
        return JsonResponse(response, safe=False)


class FollowingshowView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, format=None):
        response = {'status': 100, 'data': None}
        user = self.request.user
        followings = Followership.objects.filter(follower_id=user.id)

        followingList = []
        for following in followings:
            followingList.append({'following_id':following.id,'following_name':following.following.username,'user_bio':following.following.bio})
        response['data'] = followingList
        return JsonResponse(response, safe=False)
