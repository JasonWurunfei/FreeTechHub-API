from django.http import Http404
from . import serializers
from .models import (
    Node, NodeToNode, SkillTree,
    LightNode, ModifyRequest
)

class Modify:
    NodeToNode_class = NodeToNode
    Node_class = Node

    def __init__(self, tree):
        self.tree = tree


class Create(Modify):
    def __init__(self, tree, targets):
        super().__init__(tree)
        self.parent = self.Node_class.objects.get(name=targets['node_name'])
        self.child, _ = self.Node_class.objects.get_or_create(name=targets['new_node_name'])
    
    def perform(self):
        self.NodeToNode_class.objects.create(
            parent=self.parent,
            child=self.child,
            beloging_tree=self.tree
        )

    def __repr__(self):
        return f"<Create: {self.child} on {self.parent}>"

class Delete(Modify):
    def __init__(self, tree, targets):
        super().__init__(tree)
        self.node = self.Node_class.objects.get(name=targets['node_name'])
    
    def recursive_delete(self, node):
        sub_ntns = self.NodeToNode_class.objects.filter(
            parent=node, beloging_tree=self.tree
        )
        if len(sub_ntns) == 0:
            self.NodeToNode_class.objects.filter(
                child=node, beloging_tree=self.tree
            ).delete()

        for ntn in sub_ntns:
            self.recursive_delete(ntn.child)
            self.NodeToNode_class.objects.filter(
                child=node, beloging_tree=self.tree
            ).delete()
    
    def perform(self):
        self.recursive_delete(self.node)

    def __repr__(self):
        return f"<Delete: {self.node}>"


class Move(Modify):
    def __init__(self, tree, targets):
        super().__init__(tree)
        self.node = self.Node_class.objects.get(name=targets['node_name'])
        self.to_node = self.Node_class.objects.get(name=targets['to_node_name'])
    
    def perform(self):
        ntns = self.NodeToNode_class.objects.filter(
            child=self.node, beloging_tree=self.tree)
        for ntn in ntns:
            ntn.parent = self.to_node
            ntn.save()

    def __repr__(self):
        return f"<Move: {self.node} to {self.to_node}>"


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
        self.modify_queue = []
    
    def query_tree(self):
        """
        get tree ORM object from the database
        """
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
                "sub_trees": sub_nodes
            }
        
        for ntn in sub_ntns:
            child_node = ntn.child
            sub_tree = self.get_serialized_tree(child_node)
            sub_nodes.append(sub_tree)
        
        return {
            "node": self.Node_serializer(node).data,
            "sub_trees": sub_nodes
        }

    def get_tree(self):
        tree_obj = self.get_tree_obj()
        root_node = tree_obj.root_node
        data = self.SkillTree_serializer(tree_obj).data
        data.update({
            "tree_structure": self.get_serialized_tree(root_node)
        })
        return data

    def modify_factory(self, modify_dict):
        """
        This factory will have different instantiation
        strategies for different modify types 
        """
        modify_map = {
            'create': Create,
            'delete': Delete,
            'move': Move
        }
        constructor = modify_map[modify_dict['type']]
        return constructor(self.get_tree_obj(), modify_dict['targets'])

    def read_modify(self, modify_dicts):
        for modify_dict in modify_dicts:
            self.modify_queue.append(self.modify_factory(modify_dict))
    
    def commit(self):
        for modify in self.modify_queue:
            modify.perform()
