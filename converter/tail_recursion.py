import ast
from visitor.function_visitor import FunctionVisitor
from visitor.loop_visitor import LoopVisitor

# Convert iteration to tail recursion

def iter2tail(node):
    """
    Convert an iterative function to a tail recursive function

    Args:
        node: The function to convert
        
    Returns:
        The converted function
    """
    # Identify the loop
    # Identify the state variables relevant to the loop
    # Create a state update function
    # Identify terminating condition