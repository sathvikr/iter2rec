import ast
from typing import Any

def format_ast_node(node: Any, is_top_level: bool = True) -> str:
    """
    Format an AST node or structure containing AST nodes into a readable string.
    
    Args:
        node: An AST node or structure containing AST nodes
        is_top_level: Whether this is a top-level call (for formatting)
        
    Returns:
        A formatted string representation
    """
    if isinstance(node, ast.AST):
        return ast.dump(node, indent=2)
    elif isinstance(node, (list, tuple)):
        if not node:
            return "[]"
        items = [format_ast_node(x, False) for x in node]
        separator = ",\n" if is_top_level else ", "
        return "[\n" + separator.join(items) + "\n]" if is_top_level else f"[{', '.join(items)}]"
    elif isinstance(node, dict):
        return "{" + ", ".join(f"{k}: {format_ast_node(v, False)}" for k, v in node.items()) + "}"
    else:
        return repr(node)

def print_ast(obj: Any) -> None:
    """
    Print any AST-related structure in a readable format.
    
    Args:
        obj: The object to print (AST node, list of nodes, or dict containing nodes)
    """
    print(format_ast_node(obj)) 