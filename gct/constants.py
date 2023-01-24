ROOT_NODE = -1
ROOT_NODE_LINENO = -1
NODE_NAMES_TO_IGNORE = {"super"}
SELF_NODE_NAME = "self"
TEMP_FOLDER = "temp"
GRAPH_FOLDER_DEFAULT_NAME = "gct_graph"
PROMPT = """
function: 
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

one sentence description: Calculates the fibonacci numbers to the n'th degree.
###
function:
def resize_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.resize(image, (512, 512))
    cv2.imwrite(image_path, image)

one sentence description: Reads an image, resizes it to (512, 512) using openCV, then saves it in the same path. 
###
function:
<function_code>

one sentence description:"""
