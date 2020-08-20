from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .models import Transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.models import User

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [
        IsAuthenticated,
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def create(self, request, *args, **kwargs):
        data = {
            "amount": request.data['amount'],
            "transaction_type": request.data['transaction_type'],
            "description": request.data['description'],
            "user": request.data['user']
        }

        if request.data.get('csrfmiddlewaretoken') is not None:
            data.update({'csrfmiddlewaretoken': request.data['csrfmiddlewaretoken']})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        if request.data['transaction_type'] == "PBQ":
            user = User.objects.get(id=request.data['user'])
            new_balance = user.balance-int(request.data['amount'])
            user.balance = new_balance
            user.save()
        elif request.data['transaction_type'] == "B":
            user = User.objects.get(id=request.data['user'])
            new_balance = user.balance+int(request.data['amount'])
            user.balance = new_balance
            user.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 
 
class QueryView(APIView):
    """
    This view should return a list of all the transactions which 
    are belong to the requesting user.
    """
    def get(self, request, user_id, format=None, **kwargs):
        transactions = Transaction.objects.filter(user = user_id)
        user_related_content = {}
        user_related_content['transactions'] = [TransactionSerializer(transaction).data for transaction in transactions]
        return Response(user_related_content)
