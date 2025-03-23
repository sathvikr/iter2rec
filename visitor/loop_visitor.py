import ast
from ast_utils import print_ast

class LoopVisitor(ast.NodeVisitor):
    def __init__(self):
        self.loops = []

    def visit_While(self, node):
        # Store state variables
        loop_info = {
            "condition": node.test,
            "updates": []
        }
        
        loop_body_visitor = LoopBodyVisitor()
        # Visit each node in the body individually
        for stmt in node.body:
            loop_body_visitor.visit(stmt)
        loop_info["updates"] = loop_body_visitor.updates
        self.loops.append(loop_info)
        # Continue visiting the rest of the tree
        self.generic_visit(node)


class LoopBodyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.updates = []

    def visit_Assign(self, node):
        self.updates.append(node)
        self.generic_visit(node)
        
    def visit_AugAssign(self, node):
        self.updates.append(node)
        self.generic_visit(node)
