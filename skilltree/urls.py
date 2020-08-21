from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('node', views.NodeViewSet)
router.register('nodetonode', views.NodeToNodeViewSet)
router.register('skilltree', views.SkillTreeViewSet)
router.register('lightnode', views.LightNodeViewSet)
router.register('modifyrequest', views.ModifyRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getskilltree/<int:tree_id>/', views.SkilltreeView.as_view()),
]
