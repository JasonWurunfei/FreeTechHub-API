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


class SkillTreeHandler:

    Node_class = Node
    SkillTree_class = SkillTree
    NodeToNode_class = NodeToNode

    Node_serializer = serializers.NodeSerializer
    SkillTree_serializer = serializers.SkillTreeSerializer
    NodeToNode_serializer = serializers.NodeToNodeSerializer

    def __init__(self, tree_id):
        self.tree_id = tree_id
        self.tree_obj = None
    
    def query_tree(self):
        try:
            skilltree = self.SkillTree_class.objects.get(id=self.tree_id)
        except self.SkillTree_class.DoesNotExist:
            raise Http404
        
        self.tree_obj = skilltree
        return skilltree

    def query_sub_ntn(self, node):
        """
        'ntn' stands for node_to_node. this method will
        return all the node_to_nodes where the input node
        is parent in this tree.
        """
        sub_ntn = self.NodeToNode_class.objects.filter(
                                parent=node,
                                beloging_tree_id=self.tree_id
                            )
        return sub_ntn

    def get_tree_obj(self):
        if self.tree_obj is None:
            tree_obj = self.query_tree()
            return tree_obj
        return self.tree_obj

    def get_serialized_tree(self, node):
        sub_ntns = self.query_sub_ntn(node)
        sub_nodes = []
        if len(sub_ntns) == 0:
            return {
                "node": self.Node_serializer(node).data,
                "sub_nodes": sub_nodes
            }
        
        for ntn in sub_ntns:
            child_node = ntn.child
            sub_tree = self.get_serialized_tree(child_node)
            sub_nodes.append(sub_tree)
        
        return {
            "node": self.Node_serializer(node).data,
            "sub_nodes": sub_nodes
        }


class SkilltreeView(APIView):

    def get(self, request, tree_id, format=None):
        tree_handler = SkillTreeHandler(tree_id)
        tree_obj = tree_handler.get_tree_obj()
        return Response(tree_handler.get_serialized_tree(tree_obj.root_node))

    def post(self, request, tree_id, format=None):
        pass


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
