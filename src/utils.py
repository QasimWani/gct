import ast

def parse_file(filename):
    with open(filename) as f:
        return ast.parse(f.read(), filename=filename)

def get_indent_number(line:str):
    return len(line) - len(line.lstrip())

def get_end_of_function(filename:str, lineno:int):
    """
    Fetches the end of a function definition by comparing indentation number of the
    first line with the indentation of potential end function.
    @Parameters:
    1. filename: str = file containing function.
    2. lineno: int = line number (0-based indexing) where function of interest starts from.
    @Returns: line number where the function ends.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        start_indent = get_indent_number(lines[lineno])
        for i in range(lineno + 1, len(lines)):
            line = lines[i]
            if get_indent_number(line) <= start_indent and line.strip():
                return i - 1
        return len(lines) - 1

def get_immediate_parent(filename:str, lineno:int):
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
    1. filename: str = file containing function.
    2. lineno:int = line number (0-based indexing) where function of interests starts from.
    @Returns: line number of immediate parent node.
    """

    with open(filename, 'r') as f:
        lines = f.readlines()
        start_indent = get_indent_number(lines[lineno])
        if start_indent == 0: # at root level
            return -1
        
        for i in range(lineno, -1, -1):
            line = lines[i]
            if get_indent_number(line) < start_indent and line.strip():
                return i
        raise ValueError("This should never be called!")

def fetch_full_function(filename:str, start_lineno:int):
    end_lineno = get_end_of_function(filename, start_lineno)
    with open(filename, 'r') as f:
        lines = f.readlines()
        data = "".join(lines[start_lineno:end_lineno + 1])
        print(data)
        
# filename = "test/arithmetics.py"
# start_lineno = 26

# fetch_full_function(filename, start_lineno)
# parent_lineno = get_immediate_parent(filename, start_lineno)
# fetch_full_function(filename, parent_lineno)
# end_lineno = get_end_of_function(filename, start_lineno)