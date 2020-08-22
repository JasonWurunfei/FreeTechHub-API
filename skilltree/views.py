from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import viewsets
from . import serializers

from .models import (
    Node, NodeToNode, SkillTree,
    LightNode, ModifyRequest
)

from .treeHandler import SkillTreeHandler


class SkilltreeView(APIView):

    def get(self, request, tree_id, format=None):
        tree_handler = SkillTreeHandler(tree_id)
        return Response(tree_handler.get_tree(), status.HTTP_200_OK)

    def post(self, request, tree_id, format=None):
        tree_handler = SkillTreeHandler(tree_id)
        modify_queue = request.data['modify_queue']
        print(modify_queue)
        tree_handler.read_modify(modify_queue)
        print(tree_handler.modify_queue)
        tree_handler.commit()
        return Response(tree_handler.get_tree(), status.HTTP_202_ACCEPTED)


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = serializers.NodeSerializer


class NodeToNodeViewSet(viewsets.ModelViewSet):
    queryset = NodeToNode.objects.all()
    serializer_class = serializers.NodeToNodeSerializer


class SkillTreeViewSet(viewsets.ModelViewSet):
    queryset = SkillTree.objects.all()
    serializer_class = serializers.SkillTreeSerializer


class LightNodeViewSet(viewsets.ModelViewSet):
    queryset = LightNode.objects.all()
    serializer_class = serializers.LightNodeSerializer


class ModifyRequestViewSet(viewsets.ModelViewSet):
    queryset = ModifyRequest.objects.all()
    serializer_class = serializers.ModifyRequestSerializer
