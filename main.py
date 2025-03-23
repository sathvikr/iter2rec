import ast
from visitor.function_visitor import FunctionVisitor
from ast_utils import print_ast

prog = open("test/factorial.py").read()

tree = ast.parse(prog)

function_visitor = FunctionVisitor()
function_visitor.visit(tree)

print_ast(function_visitor.functions)


