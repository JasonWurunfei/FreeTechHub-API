from rest_framework.serializers import ModelSerializer
from .models import Transaction
from user.serializers import UserSerializer

class TransactionSerializer(ModelSerializer):
    user_instance = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "user", "user_instance",
                "amount", "time", "transaction_type", "description"]
