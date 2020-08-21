from django.contrib import admin
from .models import (
    Node, NodeToNode, SkillTree,
    LightNode, ModifyRequest
)

admin.site.register(Node)
admin.site.register(NodeToNode)
admin.site.register(SkillTree)
admin.site.register(LightNode)
admin.site.register(ModifyRequest)
