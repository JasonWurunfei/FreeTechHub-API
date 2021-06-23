from django.urls import path, include
from rest_framework import routers
from .views import TransactionViewSet
from . import views

router = routers.DefaultRouter()
router.register('transaction', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('query/<int:user_id>/', views.QueryView.as_view())
]
