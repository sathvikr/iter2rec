import ast
import sys
import os
from converter.tail_recursion import iter2tail
from visitor.function_visitor import FunctionVisitor

def find_function(tree: ast.Module, target_name: str) -> ast.FunctionDef:
    """Find a function with the given name in the AST"""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == target_name:
            return node
    raise ValueError(f"Function '{target_name}' not found in the source file")

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <python_file> <function_name>")
        sys.exit(1)
        
    source_file = sys.argv[1]
    function_name = sys.argv[2]
    
    # Read source file
    try:
        with open(source_file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    
    # Parse source and find function
    try:
        tree = ast.parse(source)
        function_node = find_function(tree, function_name)
    except SyntaxError:
        print(f"Error: Invalid Python syntax in '{source_file}'")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Convert to tail recursive form
    tail_function = iter2tail(function_node)
    
    # Create output filename
    base, ext = os.path.splitext(source_file)
    output_file = f"{base}__tail{ext}"
    
    # Generate new source code
    new_tree = ast.Module(
        body=[tail_function],
        type_ignores=[]
    )
    
    # Write to output file
    try:
        with open(output_file, 'w') as f:
            f.write(ast.unparse(new_tree))
        print(f"Created tail recursive version in '{output_file}'")
    except IOError:
        print(f"Error: Could not write to '{output_file}'")
        sys.exit(1)

if __name__ == "__main__":
    main()

