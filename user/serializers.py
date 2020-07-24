from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
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
