from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.db import models
from blog.models import Blog
from question.models import Answer
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        verbose_name='user name',
        max_length=30,
        unique=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    balance = models.IntegerField(default=0, blank=True)
    major   = models.CharField(max_length=30, blank=True, default='')
    grade   = models.CharField(max_length=20, blank=True, default='')
    bio     = models.TextField(blank=True, default='')
    avatar  = ProcessedImageField(upload_to='media/',
                                  default='/avatar/default.png',
                                  verbose_name='avatar',
                                  #图片将处理成100 x 100的尺寸
                                  processors=[ResizeToFill(100,100)],)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def totallikes(self):
        all_blogs = Blog.objects.filter(owner=self)
        num = 0
        for blog in all_blogs:
            num +=blog.view_num
        return num

    @property
    def totalviews(self):
        all_blogs = Blog.objects.filter(owner=self)
        num = 0
        for blog in all_blogs:
            num +=blog.like_num

        return num


class Followership(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='following_users',
                                  on_delete=models.CASCADE)

    follower = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='follower_users',
                                 on_delete=models.CASCADE)


class FriendRequest(models.Model):
    sender          = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name="sent_request",
                                        on_delete=models.CASCADE,null=True)

    receiver        = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name="received_request",
                                        on_delete=models.CASCADE,null=True)

    datetime        = models.DateTimeField(auto_now_add=True)
    note            = models.TextField(null=True)

    STATES_CHOICES = [
        ('A', 'approved'),
        ('D', 'denied'),
        ('C', 'canceled'),
        ('W', 'waiting')
    ]

    state = models.CharField(
        max_length=1,
        choices=STATES_CHOICES,
        default='W',
        blank=True
    )

    @property
    def sender_instance(self):
        return self.sender

    @property
    def receiver_instance(self):
        return self.receiver


class Friendship(models.Model):
    friend_1 = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="friendship_1",
                                 on_delete=models.CASCADE,
                                 null=True)

    friend_2 = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name="friendship_2",
                                 on_delete=models.CASCADE,
                                 null=True)

    @property
    def friend_instance_1(self):
        return self.friend_1

    @property
    def friend_instance_2(self):
        return self.friend_2


class Chat(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="chat_user1",
                              on_delete=models.CASCADE)

    user2 = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="chat_user2",
                              on_delete=models.CASCADE)


class Message(models.Model):
    belonging_chat  = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    content         = models.CharField(max_length=256)
    datetime        = models.DateTimeField(auto_now_add=True)

    sender          = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name="messageSender",
                                        on_delete=models.CASCADE)


class EmailValid(models.Model):
    onwer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     related_name='onwer',
                                     on_delete=models.CASCADE,null=True)
    value = models.CharField(max_length=32)
    email_address = models.CharField(max_length=32)
    type = models.TextField(null=True)
    time = models.DateTimeField(auto_now_add=True)
