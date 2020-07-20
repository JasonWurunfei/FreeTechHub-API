from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "last_login", "is_superuser","first_name","last_name","date_joined","username","email","date_of_birth","is_active","is_admin","is_authorized","balance","major","grade",
            "bio","avatar","groups","user_permissions"
        ]
