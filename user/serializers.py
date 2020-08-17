from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import (User, Followership,
                     FriendRequest, Friendship,
                     EmailValid, Chat, Message)


class FollowershipSerializer(ModelSerializer):
    class Meta:
        model = Followership
        fields = '__all__'


class EmailValidSerializer(ModelSerializer):
    class Meta:
        model = EmailValid
        fields = '__all__'


class UserSerializer(ModelSerializer):
    following_users = FollowershipSerializer(many=True, required=False)
    follower_users =  FollowershipSerializer(many=True, required=False)
    class Meta:
        model = User
        exclude = ['password']
        extra_kwargs = {
            'last_login'        : {'read_only': True},
            'is_superuser'      : {'read_only': True},
            'date_joined'       : {'read_only': True},
            'is_active'         : {'read_only': True},
            'is_admin'          : {'read_only': True},
            'is_authorized'     : {'read_only': True},
            'balance'           : {'read_only': True},
            'groups'            : {'read_only': True},
            'user_permissions'  : {'read_only': True},
        }


class FriendRequestSerializer(serializers.ModelSerializer):
    sender_instance    = UserSerializer(read_only=True)
    receiver_instance  = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendshipSerializer(serializers.ModelSerializer):
    friend_instance_1 = UserSerializer(read_only=True)
    friend_instance_2 = UserSerializer(read_only=True)
    class Meta:
        model = Friendship
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ['id', 'user1', 'user2', 'messages']
