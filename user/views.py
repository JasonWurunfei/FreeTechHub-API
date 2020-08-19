from .models import User
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, FollowershipSerializer
from .serializers import FriendRequestSerializer, FriendshipSerializer, EmailValidSerializer
from .models import User, Followership, FriendRequest, Friendship, MyUserManager,EmailValid
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import localtime
from django.conf import settings
import random
import datetime
import pytz
import time
import os
from collections import Counter
from blog.models import Blog
from tag.models import  Tag
from question.models import Question
from collections import Counter


# Create your views here.
def Email_Code(len=15):
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    for i in range(65, 91):
        code_list.append(chr(i))
    for i in range(97, 123):
        code_list.append(chr(i))
    myslice = random.sample(code_list, len)
    code_ = ''.join(myslice)
    return code_


def SendEmail(user,email,type):
    code1 = Email_Code()
    code2 = Email_Code()
    if type:
        emailvate = EmailValid.objects.create(onwer = user, email_address=email, value=code1, type="ForgetPassowrd")
        ret = "Your verification code is :http://localhost:8080/#/forgetpassword/{}/{}/{}".format(code1,emailvate.onwer.id,code2)
    else:
        emailvate = EmailValid.objects.create(onwer = user, email_address=email, value=code1, type="Verify")
        ret = "Your verification code is :http://localhost:8080/#/active/{}/{}".format(code1,emailvate.onwer.id)
    my_email = send_mail('Activation validation', ret, settings.DEFAULT_FROM_EMAIL, [email])


class EmailValidViewSet(viewsets.ModelViewSet):
        queryset = EmailValid.objects.all()
        serializer_class = EmailValidSerializer


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


class ChangeEmailView(APIView):
# ChangeEmail
    def post(self, request, format=None):
        data = request.data
        password = data.get('password')
        email1 = data.get('email1')
        user_ = self.request.user
        if user_.check_password(password):
            User.objects.filter(id = user_.id).update(email = email1,is_verified=False)
            user = User.objects.get(id = user_.id)
            type = False
            SendEmail(user,email1,type)
            return Response({'msg':'successful'})
        else:
            return Response({'msg':'ppppPlease enter code'})


class ResetPasswordView(APIView):
# ChangeEmail
    def post(self, request, format=None):
        data = request.data
        password = data.get('password')
        id = data.get('id')
        user = User.objects.get(id = id)
        user.set_password(password)
        user.save()
        return Response("successfully")


from websocket.middleware import live_sockects
from rest_framework import status
from asgiref.sync import async_to_sync
class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    """
    Create a FriendRequest instance and notice the receiver if
    he or she is online
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        socket = live_sockects.get_socket(int(request.data['receiver']))

        if socket != None:
            async_to_sync(socket.send_json)({"type": "request"})

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    Update a FriendRequest instance and meanwhile setup a friendship.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # override part
        # if the update is state = approved, setup new friendship
        if request.data['state'] == "A":
            Friendship.objects.create(
                friend_1=instance.sender,
                friend_2=instance.receiver
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer


class GetFriendRequestsView(APIView):

    def get(self, request, user_id, format=None):
        requests = FriendRequest.objects.filter(sender_id=user_id).exclude(state="C")
        data = FriendRequestSerializer(requests, many=True).data
        return Response(data)

class GetReceivedFriendRequestsView(APIView):

    def get(self, request, user_id, format=None):
        requests = FriendRequest.objects.filter(receiver_id=user_id, state="W")
        data = FriendRequestSerializer(requests, many=True).data
        return Response(data)


class GetFriendsView(APIView):

    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

        # because this user could be friend_1 or friend_2 of some
        # Friendship, therefore we are getting all the relavent.
        relavent_friendships_1 = Friendship.objects.filter(friend_1=user)
        relavent_friendships_2 = Friendship.objects.filter(friend_2=user)
        relavent_friendships = relavent_friendships_1 | relavent_friendships_2

        serialized_friends = []
        for friendship in relavent_friendships:
            if friendship.friend_1 == user:
                # if user is friend_1 in a friendship
                # then friend_2 is this user's friend.
                serialized_friends.append(
                    UserSerializer(friendship.friend_2).data
                )
            else:
                serialized_friends.append(
                    UserSerializer(friendship.friend_1).data
                )

        return Response(serialized_friends)


# Chat system
from asgiref.sync import sync_to_async
from .models import Chat, Message
from .serializers import MessageSerializer, ChatSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer


class GetChatView(APIView):

    def get(self, request, format=None, **kwargs):
        sender   = self.request.query_params.get('sender', None)
        receiver = self.request.query_params.get('receiver', None)

        try:
            chat = Chat.objects.get(user1_id=sender,
                                    user2_id=receiver)

        except Chat.DoesNotExist:
            chat, _ = Chat.objects.get_or_create(user1_id=receiver,
                                                 user2_id=sender)

        return Response(ChatSerializer(chat).data)


async def WebsocketView(socket, live_sockects):
    await socket.accept()
    sender_id = None

    while True:
        message = await socket.receive_json()

        # socket.receive_json() will return None if the massage
        # if the message is to disconnect.
        if message == None:
            live_sockects.checkout(socket)
            break

        sender_id = message['sender_id']
        if message.get('register') == True:
            live_sockects.register(sender_id, socket)
            continue

        receiver_id = message['receiver_id']
        try:
            chat = await sync_to_async(
                Chat.objects.get
            )(user1_id=sender_id, user2_id=receiver_id)

        except Chat.DoesNotExist:
            chat, _ = await sync_to_async(
                Chat.objects.get_or_create
            )(user1_id=receiver_id, user2_id=sender_id)

        msg = await sync_to_async(Message.objects.create)(
            belonging_chat=chat,
            content=message['message'],
            sender_id=sender_id,
        )

        msg = MessageSerializer(msg).data
        msg.update({"type": "message", "receiver": receiver_id})
        await socket.send_json(msg)

        # live_sockects.get_socket will return None if
        # not find a match user in the list
        receiver_socket = live_sockects.get_socket(receiver_id)
        # if receiver_socket == None means the receiver
        # is not online or at message page
        if receiver_socket != None:
            await receiver_socket.send_json(msg)


class Email_codeView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if email:
            type=False
            user_ = User.objects.create_user(username,email,password)
            SendEmail(user_,email,type)
            # code = Email_Code()
            # emailvate = EmailValid.objects.create(onwer = user_, email_address=email,value=code)
            # ret = "Your verification code is :http://localhost:8080/#/active/{}/{}".format(code,emailvate.onwer.id)
            # my_email = send_mail('Activation validation', ret, settings.DEFAULT_FROM_EMAIL, [email])
            return Response({'msg':'Please enter code'})
        else:
            return Response({'msg':'ppppPlease enter code'})


class RegisterView(APIView):
    def post(self, request, format=None):
        code = request.data.get('code')
        user_id = request.data.get('user_id')
        email_obj = EmailValid.objects.filter(onwer = user_id).last()
        if(email_obj.value == code):
            now = datetime.datetime.now()+datetime.timedelta(minutes=-5)
            now = now.replace(tzinfo=pytz.timezone('UTC'))
            T1 = now.strftime("%Y-%m-%d-%H-%M-%S")
            T2 = localtime(email_obj.time.replace(tzinfo=pytz.timezone('Asia/Shanghai')))
            T2 = T2.strftime("%Y-%m-%d-%H-%M-%S")
            T1 = [int(e) for e in T1.split('-')]
            T2 = [int(e) for e in T2.split('-')]
            print(now)
            print(email_obj.time)
            if T1 < T2:
                user = User.objects.get(id = user_id, email=email_obj.email_address)
                user.is_verified = True
                user.save()
                return Response("successful")
            else:
                return Response("timeout")
        else:

            return Response("wrong code")


class Send_changepassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        user = User.objects.get(email = email)
        if user !='':
            type = True
            SendEmail(user,email,type)
            return Response("successful")
        else:
            return Response("error")


class CheckUsernameView(APIView):
    def get(self, request, format=None):
        name = request.query_params.get('username')
        count = User.objects.filter(username=username).count()
        if count > 0:
            return Response('False')
        else:
            return Response('True')


class UploadView(APIView):
    def post(self, request, format=None):
        url = "/avatar/"
        user_ = self.request.user
        file_obj=request.FILES.get("file")
        print(type(file_obj))
        name=file_obj.name.rsplit(".")[1]
        img_name = int(time.time())
        dir = os.path.join(os.path.join(settings.BASE_DIR, 'avatar/avatar'),str(img_name)+'.'+name)
        destination = open(dir,'wb+')
        for chunk in file_obj.chunks():
            destination.write(chunk)
        User.objects.filter(id = user_.id).update(avatar = url + str(img_name)+'.'+name )
        return Response('True')


class GetSelftags(APIView):
    def get(self, request, format=None):
        blogs = Blog.objects.filter(owner = self.request.user.id)
        questions = Question.objects.filter(owner = self.request.user.id)
        Btags = []
        Qtags = []
        Bdata = []
        Qdata = []
        for blog in blogs:
            all_tags = Tag.objects.filter(content_type=6,object_id=blog.id )
            for all_tag in all_tags:
                Btags.append(all_tag.tag_name)
        for question in questions:
            all_tags = Tag.objects.filter(content_type=17,object_id=question.id)
            for all_tag in all_tags:
                Qtags.append(all_tag.tag_name)
        Bstatistics = dict(Counter(Btags))
        Qstatistics = dict(Counter(Qtags))
        for k,v in Bstatistics.items():
            Bdata.append({'name': k, 'value': v})
        for k,v in Qstatistics.items():
            Qdata.append({'name': k, 'value': v})
        return Response({'Qdata':Qdata,'Bdata':Bdata})
