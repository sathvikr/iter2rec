import ast
from visitor.function_visitor import FunctionVisitor
from visitor.loop_visitor import LoopVisitor
from ast_utils import print_ast

def set_locations(node: ast.AST, start_lineno: int = 1, col_offset: int = 0) -> ast.AST:
    """Set source location information for an AST node and its children"""
    current_line = start_lineno
    
    def _set_location(node: ast.AST, lineno: int, col_offset: int) -> int:
        """Set location for a node and its children, return next available line number"""
        if not isinstance(node, ast.AST):
            return lineno
            
        node.lineno = lineno
        node.col_offset = col_offset
        next_line = lineno + 1
        
        # Handle list fields specially to maintain contiguous line numbers
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    next_line = _set_location(item, next_line, col_offset)
            elif isinstance(value, ast.AST):
                next_line = _set_location(value, next_line, col_offset)
        
        return next_line
    
    _set_location(node, start_lineno, col_offset)
    return node

def create_loop_function(state_vars: list[ast.AST], tcond: ast.AST) -> ast.FunctionDef:
    """Create the inner loop function for tail recursion"""
    loop_args = [ast.arg(arg=var.target.id, annotation=None) for var in state_vars]
    
    # Create function with all nodes on consecutive lines
    loop_func = ast.FunctionDef(
        name='loop',
        args=ast.arguments(
            posonlyargs=[],
            args=loop_args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            vararg=None,
            kwarg=None
        ),
        body=[
            create_termination_check(state_vars, tcond),
            create_recursive_call(state_vars)
        ],
        decorator_list=[]
    )
    return set_locations(loop_func, start_lineno=2, col_offset=4)

def create_termination_check(state_vars: list[ast.AST], tcond: ast.AST) -> ast.If:
    """Create the termination condition check"""
    if_node = ast.If(
        test=ast.UnaryOp(
            op=ast.Not(),
            operand=tcond
        ),
        body=[
            ast.Return(
                value=ast.Name(id=state_vars[0].target.id, ctx=ast.Load())
            )
        ],
        orelse=[]
    )
    return set_locations(if_node, start_lineno=1, col_offset=8)

def create_recursive_call(state_vars: list[ast.AST]) -> ast.Return:
    """Create the recursive function call with updated arguments"""
    return_node = ast.Return(
        value=ast.Call(
            func=ast.Name(id='loop', ctx=ast.Load()),
            args=[
                update.value for update in state_vars
            ],
            keywords=[]
        )
    )
    return set_locations(return_node, start_lineno=1, col_offset=8)

def create_outer_function(node: ast.FunctionDef, state_vars: list[ast.AST], loop_func: ast.FunctionDef) -> ast.FunctionDef:
    """Create the outer function that wraps the recursive loop"""
    outer_func = ast.FunctionDef(
        name=node.name,
        args=node.args,
        body=[
            loop_func,
            create_initial_call(node, state_vars)
        ],
        decorator_list=[]
    )
    return set_locations(outer_func, start_lineno=1, col_offset=0)

def create_initial_call(node: ast.FunctionDef, state_vars: list[ast.AST]) -> ast.Return:
    """Create the initial call to the loop function"""
    state_var_names = [var.target.id for var in state_vars]
    return_node = ast.Return(
        value=ast.Call(
            func=ast.Name(id='loop', ctx=ast.Load()),
            args=[
                ast.Name(id=arg.arg, ctx=ast.Load()) if arg.arg in state_var_names
                else ast.Constant(value=1)
                for arg in node.args.args
            ],
            keywords=[]
        )
    )
    return set_locations(return_node, start_lineno=1, col_offset=4)

def extract_loop_info(node: ast.FunctionDef) -> tuple[list[ast.AST], ast.AST]:
    """Extract loop information from the function"""
    function_visitor = FunctionVisitor()
    function_visitor.visit(node)
    func_info = function_visitor.functions[0]
    loop = func_info["loops"][0]
    
    # Get updates directly as a list
    state_vars = [update for update in loop["updates"] 
                 if isinstance(update, (ast.Assign, ast.AugAssign)) 
                 and isinstance(update.target, ast.Name)]
    tcond = loop["condition"]
    
    return state_vars, tcond

def iter2tail(node: ast.FunctionDef) -> ast.FunctionDef:
    """
    Convert an iterative function to a tail recursive function

    Args:
        node: The function to convert

    Returns:
        The converted function
    """
    assert isinstance(node, ast.FunctionDef)
    
    # Extract loop information
    state_vars, tcond = extract_loop_info(node)
    
    # Create the inner loop function with proper indentation
    loop_func = create_loop_function(state_vars, tcond)
    
    # Create outer function with __tail suffix
    node.name = f"{node.name}__tail"
    return create_outer_function(node, state_vars, loop_func)
