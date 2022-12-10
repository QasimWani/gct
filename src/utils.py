import ast

def parse_file(filename):
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename=filename)
        f.seek(0)
        return tree, f.readlines()

def get_indent_number(line:str):
    return len(line) - len(line.lstrip())

def get_end_of_function(lines:list[str], lineno:int):
    """
    Fetches the end of a function definition by comparing indentation number of the
    first line with the indentation of potential end function.
    @Parameters:
    1. lines: list[str] = relevant lines of code.
    2. lineno: int = line number (0-based indexing) where function of interest starts from.
    @Returns: line number where the function ends.
    """
    start_indent = get_indent_number(lines[lineno])
    for i in range(lineno + 1, len(lines)):
        line = lines[i]
        if get_indent_number(line) <= start_indent and line.strip():
            return i - 1
    return len(lines) - 1

def get_immediate_parent(lines:list[str], lineno:int):
    """
    Given a function, fx, find the most immediate parent node.
    In this case, most immediate parent node is the first instance where
    the indentation number is lesser than fx.
    E.g.:
    ```
    def X(): #1
        def Y(): #2
            //code #3
    ```
    In this case, if `Y` is our function of interest, the most immediate
    parent node is function `X` defined at line #1. Core logic is similar
    to `fetch_end_of_function`, except now we traverse upwards.
    @Parameters:
    1. lines: list[str] = relevant lines of code.
    2. lineno:int = line number (0-based indexing) where function of interests starts from.
    @Returns: line number of immediate parent node.
    """
    assert lineno < len(lines), "lineno out of range"
    
    if lineno < 0:
        return -1 # root node
        
    start_indent = get_indent_number(lines[lineno])

    if start_indent == 0: # at root level
        return -1
    for i in range(lineno, -1, -1):
        line = lines[i]
        if get_indent_number(line) < start_indent and line.strip():
            return i
    raise ValueError("This should never be called!")

def print_full_function(filename:str, start_lineno:int):
    """ Fetch the full context for a function at a given lineno and print it out. """
    end_lineno = get_end_of_function(filename, start_lineno)
    with open(filename, 'r') as f:
        lines = f.readlines()
        data = "".join(lines[start_lineno:end_lineno + 1])
        print(data)