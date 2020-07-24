from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TransactionSerializer
from .models import Transaction
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrReadOnly

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = [
    #     IsAuthenticated,
    #     IsAuthenticatedOrReadOnly,
    #     IsOwnerOrReadOnly
    # ]
