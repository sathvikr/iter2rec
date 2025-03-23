import ast
from .loop_visitor import LoopVisitor
from ast_utils import print_ast

class FunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        func_info = {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "initial_assignments": {},
            "loops": []
        }
        for stmt in node.body:
            if isinstance(stmt, ast.While):
                loop_visitor = LoopVisitor()
                loop_visitor.visit(stmt)
                func_info["loops"].extend(loop_visitor.loops)
        self.functions.append(func_info)
        self.generic_visit(node)