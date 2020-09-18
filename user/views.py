from .models import User
from django.core.mail import send_mail
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, FollowershipSerializer
from .serializers import FriendRequestSerializer, FriendshipSerializer, ValidationRequestSerializer
from .models import User, Followership, FriendRequest, Friendship, MyUserManager, ValidationRequest
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import localtime
from django.conf import settings
from blog.models import Blog
from tag.models import  Tag
from collections import Counter
from django.db.utils import IntegrityError
from question.models import Question, Answer
from django.contrib.contenttypes.models import ContentType
import string
import datetime
import random
import pytz
import time
import os


from rest_framework.pagination import PageNumberPagination
class ChatPagination(PageNumberPagination):
    page_size = 4 # 表示每页的默认显示数量
    page_size_query_param = 'page_size' # 表示url中每页数量参数
    page_query_param = 'p' # 表示url中的页码参数
    max_page_size = 100  # 表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃


# Create your views here.
class ValidationRequestViewSet(viewsets.ModelViewSet):
        queryset = ValidationRequest.objects.all()
        serializer_class = ValidationRequestSerializer


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


class FollowershipListView(APIView):

    def get(self, request, user_id, format=None):

        followings = []
        following_followerships = Followership.objects.filter(follower_id=user_id)
        for followership in following_followerships:
            followings.append(UserSerializer(followership.following).data)

        followers = []
        follower_followerships = Followership.objects.filter(following_id=user_id)
        for followership in follower_followerships:
            followers.append(UserSerializer(followership.follower).data)

        content = {
            "followings": followings,     # users that this user follows
            "followers": followers,     # users that follow this user
        }
        return Response(content)


class UnfollowView(APIView):

    """
    this view is used to delete a followership to unfollow
    """
    def post(self, request, format=None):
        following_id = request.data['following_id']
        follower_id = request.data['follower_id']

        try:
            followership = Followership.objects.get(
                follower_id=follower_id, following_id=following_id
            )
        except Followership.DoesNotExist:
            raise Http404

        followership.delete()
        return Response("followership deleted", status.HTTP_200_OK)


class FollowershipCheckView(APIView):
    """
    this view is check if a user is followed another user
    """
    def get(self, request, follower_id, following_id, format=None):
        try:
            followership = Followership.objects.get(
                                follower_id=follower_id,
                                following_id=following_id
                            )
        except Followership.DoesNotExist:
            return Response(False, status.HTTP_200_OK)
        return Response(True, status.HTTP_200_OK)


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


#yy's function
def judge(tags):
    data = []
    tag_count = []
    count = dict(sorted(dict(Counter(tags)).items(), key=lambda item:item[1],reverse=True))
    if 0< len(tags) < 6:
        for k,v in count.items():
            tag_count.append({'name': k, 'value': v})
    elif len(tags) == 0:
        tag_count.append({'name': "none", 'value': 0})
    else:
        others = 0
        for k,v in count.items():
            data.append({'name': k, 'value': v})
        for i in data[6:]:
            others += i['value']
        tag_count = data[0:5]
        tag_count.append({'name': "others", 'value': others})
    return tag_count


def generateKey(length):
    char_set = string.ascii_letters + string.digits
    letters = random.sample(char_set, length)
    keys = "".join(letters)
    return keys

from django.conf import settings
def send_email(user, email, request_type):
    code = generateKey(20)
    if request_type == "forget_password":
        emailvate = ValidationRequest.objects.create(owner=user, email=email, code=code, request_type="ForgetPassowrd")
        ret = f"Your verification code is :http://{settings.FRONT_DOMAIN}/#/forgetpassword/{code}/{emailvate.owner.id}/"
    elif request_type == "register":
        emailvate = ValidationRequest.objects.create(owner=user, email=email, code=code, request_type="Verify")
        ret = f"Your verification code is :http://{settings.FRONT_DOMAIN}/#/active/{code}/{emailvate.owner.id}"
    elif request_type == "change_email":
        emailvate = ValidationRequest.objects.create(owner=user, email=email, code=code, request_type="Verify")
        ret = f"Your verification code is :http://{settings.FRONT_DOMAIN}/#/active/{code}/{emailvate.owner.id}/{email}"
    my_email = send_mail('Activation validation', ret, settings.DEFAULT_FROM_EMAIL, [email])


class CheckPasswordView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        password = request.data.get('password')
        if user.check_password(password):
            return Response("successfully", status=status.HTTP_200_OK)
        else:
            return Response('false', status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    #ChangePassword
    def post(self, request, format=None):
        old_password = request.data.get('oldpassword')
        new_password = request.data.get('newpassword')
        user = self.request.user
        if user.check_password(old_password):
            request.user.set_password(new_password)
            request.user.save()
            return Response("successfully", status=status.HTTP_200_OK)
        else:
            return Response('false', status=status.HTTP_404_NOT_FOUND)


class CheckChangeemailView(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')
        user = self.request.user
        user = User.objects.exclude(id = user.id)
        count = user.filter(email=email).count()
        return Response({"count":count})


class ChangeEmailView(APIView):
# ChangeEmail
    def post(self, request, format=None):
        data = request.data
        password = data.get('password')
        email = data.get('email')
        user = self.request.user
        if user.check_password(password):
            user = User.objects.get(id = user.id)
            request_type = 'change_email'
            send_email(user,email,request_type)
            return Response('true',status=status.HTTP_200_OK)
        else:
            return Response('false',status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
# ResetPassword
    def post(self, request, format=None):
        data = request.data
        password = data.get('password')
        id = data.get('id')
        user = User.objects.get(id = id)
        user.set_password(password)
        user.save()
        return Response("successfully", status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        request_type = "register"
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return Response(IntegrityError.message, status=status.HTTP_400_BAD_REQUEST)
        send_email(user, email, request_type)
        return Response('true', status=status.HTTP_200_OK)


class ValidateCodeView(APIView):
    def post(self, request, format=None):
        code = request.data.get('code')
        user_id = request.data.get('user_id')
        request_type = request.data.get('type')
        latest_request = ValidationRequest.objects.filter(owner_id=user_id).last()
        user = User.objects.filter(id=user_id)
        user_ = User.objects.get(id=user_id)
        if request_type == "validate":
            if latest_request.is_valid(code):
                user.update(is_verified = True)
                return Response('true', status=status.HTTP_200_OK)
            else:
                return Response('false')

        elif request_type == "change_email":
            email = request.data.get('email')
            if latest_request.is_valid(code):
                user.update(email=email)
                return Response('true', status=status.HTTP_200_OK)
            else:
                return Response('false')

        elif request_type == "resend_register":
            email = latest_request.email
            request_type = "register"
            send_email(user_, email, request_type)
            return Response('true', status=status.HTTP_200_OK)

        elif request_type == "resend_change_email":
            email = latest_request.email
            request_type = "change_email"
            send_email(user_, email, request_type)
            return Response('true', status=status.HTTP_200_OK)


class SendChangePassword(APIView):
    # Send changepassword validate email
    def post(self, request, format=None):
        email = request.data.get('email')
        user = User.objects.get(email=email)
        request_type = "forget_password"
        send_email(user, email, request_type)
        return Response("successful", status=status.HTTP_200_OK)


class CheckRepeatView(APIView):
    # Whether the user name and email are duplicate
    def post(self, request, format=None):
        request_type = request.data.get('type')
        value = request.data.get('value')
        if request_type == "username" :
            count = User.objects.filter(username=value).count()
        elif request_type == "email":
            count = User.objects.filter(email=value).count()
        return Response({"count":count})


class UploadAvatatrView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        img = request.FILES.get("file")
        extension = img.name.rsplit(".")[1]

        # form the image name
        img_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + \
                   str(user.id) + '.' + extension

        # write the actual image into disk
        img_path = os.path.join(settings.AVATAR_DIR, img_name)
        destination = open(img_path, 'wb+')
        for chunk in img.chunks():
            destination.write(chunk)
        destination.close()
        
        # update img path in the database
        User.objects.filter(id=user.id).update(
            avatar=os.path.join("avatar", img_name))
        return Response('True')


class GetSelftags(APIView):
    def get(self, request, user_id, format=None):
        answer_count = Answer.objects.filter(owner_id=user_id).count()
        accept_count = Answer.objects.filter(owner_id=user_id, status=True).count()
        acceptance_rate = 0 if accept_count == 0 else '{:.2%}'.format(accept_count/answer_count)
        blogs = Blog.objects.filter(owner_id=user_id)
        questions = Question.objects.filter(owner_id=user_id)
        blog_type = ContentType.objects.get(
                        app_label="blog", model="blog")
        question_type = ContentType.objects.get(
                            app_label="question", model="question")
        Btags = []
        Qtags = []
        Bdata = []
        Qdata = []
        for blog in blogs:
            tags = Tag.objects.filter(content_type=blog_type,object_id=blog.id)
            for tag in tags:
                Btags.append(tag.tag_name)
        for question in questions:
            tags = Tag.objects.filter(content_type=question_type,object_id=question.id)
            for tag in tags:
                Qtags.append(tag.tag_name)
        Bdata = judge(Btags)
        Qdata = judge(Qtags)
        return Response({'Qdata': Qdata, 'Bdata': Bdata, 'acceptance_rate': acceptance_rate})

class GetActivityTable(APIView):
    def get(self, request, user_id, format=None):
        results = []
        begin = datetime.date(2020,1,1)
        end = datetime.date(2020,12,31)
        for i in range((end - begin).days + 1):
            daily_score = {}
            day = begin + datetime.timedelta(days=i)
            blog_count = Blog.objects.filter(owner_id=user_id, date__date=day).count()
            question_count = Question.objects.filter(owner_id=user_id, date__date=day).count()
            answer_count = Answer.objects.filter(owner_id=user_id, time__date=day).count()
            activity_score = blog_count*10 + question_count*5 + answer_count*2
            if activity_score != 0:
                daily_score["date"] = day
                daily_score["score"] = activity_score
                results.append(daily_score)
        return Response(results)

