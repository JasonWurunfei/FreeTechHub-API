from rest_framework import serializers
from .models import (
    Node, NodeToNode, SkillTree,
    LightNode, ModifyRequest
)

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class NodeToNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeToNode
        fields = "__all__"


class SkillTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTree
        fields = [
            'id', 'name', 'is_under_changing',
            'last_modified', 'root_node',
            'agree_num', 'disagree_num'
        ]


class LightNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LightNode
        fields = "__all__"


class ModifyRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifyRequest
        fields = [
            'id', 'modify_reason', 'datetime',
            'new_tree_root', 'target_tree', 'owner',
            'agree_num', 'disagree_num'
        ]
