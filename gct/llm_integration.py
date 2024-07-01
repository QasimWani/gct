import os
import sys
import ast
import anthropic
import json
import logging
from typing import Dict, List, Tuple
import graphviz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gct import api
from gct.network import Node, Graph

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Anthropic client
try:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    logger.info("Anthropic client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {e}")
    sys.exit(1)

def generate_parse_prompt(file_content: str) -> str:
    return f"""Analyze the following Python file and extract information about its structure and semantic components. Provide the output in a specific JSON format.

    Python file content:
    <python_file>
    {file_content}
    </python_file>

    Your task:
    1. Identify all classes, their methods, and standalone functions.
    2. Identify the main semantic components of the program.
    3. Map methods and functions to these semantic components.

    Provide your analysis in the following JSON format:

    {{
        "classes_and_functions": {{
            "ClassName": {{
                "type": "class",
                "methods": ["method1", "method2", ...],
                "nested_classes": {{
                    "NestedClassName": {{
                        "methods": ["nestedMethod1", "nestedMethod2", ...],
                        "nested_classes": null
                    }}
                }}
            }},
            "FunctionName": {{
                "type": "function",
                "methods": null,
                "nested_classes": null
            }}
        }},
        "semantic_components": {{
            "ComponentName1": ["ClassName.method1", "FunctionName", ...],
            "ComponentName2": ["ClassName.method2", ...],
            ...
        }}
    }}

    Guidelines:
    - Include all public methods, including built-in methods like __init__ if explicitly defined.
    - For standalone functions, set "methods" and "nested_classes" to null.
    - If there are no nested classes, set "nested_classes" to null.
    - Ensure every method or function is mapped to at least one semantic component.
    - Use descriptive names for semantic components that reflect their role in the program.

    Provide only the JSON output without any additional explanation."""

def generate_unmapped_methods_prompt(unmapped_methods: List[str], file_content: str) -> str:
    return f"""You are tasked with categorizing unmapped methods from a Python file into appropriate semantic components. Here are the unmapped methods:

    {', '.join(unmapped_methods)}

    Please analyze the following Python file content and suggest appropriate semantic components for these methods. If a new semantic component is needed, feel free to create one.

    Python file content:
    <python_file>
    {file_content}
    </python_file>

    Provide your response in the following JSON format:

    {{
        "semantic_components": {{
            "ComponentName1": ["Method1", "Method2"],
            "ComponentName2": ["Method3"],
            ...
        }}
    }}

    Ensure that every unmapped method is assigned to at least one semantic component. If a method's purpose is unclear, you can assign it to a "Miscellaneous" component.
    """

def get_claude_response(prompt: str) -> str:
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        logger.info("Received response from Claude.")
        response = message.content[0].text
        return response
    except Exception as e:
        logger.error(f"Failed to get response from Claude: {e}")
        return ""

def verify_structure(parsed_structure: Dict, file_content: str) -> Tuple[Dict, List[str]]:
    logger.info("Verifying structure against AST...")
    tree = ast.parse(file_content)
    verified_structure = {
        "classes": {},
        "semantic_components": {}
    }

    all_methods = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            verified_structure["classes"][class_name] = {"methods": [], "nested_classes": {}}
            
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    verified_structure["classes"][class_name]["methods"].append(method_name)
                    all_methods.add(f"{class_name}.{method_name}")
                elif isinstance(item, ast.ClassDef):
                    nested_class_name = item.name
                    verified_structure["classes"][class_name]["nested_classes"][nested_class_name] = {"methods": []}
                    for nested_item in item.body:
                        if isinstance(nested_item, ast.FunctionDef):
                            nested_method_name = nested_item.name
                            verified_structure["classes"][class_name]["nested_classes"][nested_class_name]["methods"].append(nested_method_name)
                            all_methods.add(f"{class_name}.{nested_class_name}.{nested_method_name}")

    # Verify and prune semantic components
    for component, methods in parsed_structure["semantic_components"].items():
        verified_methods = [method for method in methods if method in all_methods]
        if verified_methods:
            verified_structure["semantic_components"][component] = verified_methods

    # Check if all methods are mapped to at least one semantic component
    mapped_methods = set()
    for methods in verified_structure["semantic_components"].values():
        mapped_methods.update(methods)

    unmapped_methods = list(all_methods - mapped_methods)
    if unmapped_methods:
        logger.warning(f"The following methods are not mapped to any semantic component: {unmapped_methods}")

    logger.info("Structure verification completed.")
    return verified_structure, unmapped_methods

def create_gct_graph(verified_structure: Dict) -> graphviz.Digraph:
    logger.info("Creating GCT graph...")
    graph = graphviz.Digraph(comment='GCT Graph')
    graph.attr(rankdir='LR')
    
    # Add root node
    graph.node('root', 'Root')
    logger.debug("Added root node to graph.")
    
    # Add classes, methods, and nested classes
    for class_name, class_info in verified_structure["classes"].items():
        graph.node(class_name, class_name)
        graph.edge('root', class_name)
        logger.debug(f"Added class node: {class_name}")
        
        for method in class_info["methods"]:
            method_id = f"{class_name}.{method}"
            graph.node(method_id, method)
            graph.edge(class_name, method_id)
            logger.debug(f"Added method node: {method_id}")
        
        for nested_class_name, nested_class_info in class_info["nested_classes"].items():
            nested_class_id = f"{class_name}.{nested_class_name}"
            graph.node(nested_class_id, nested_class_name)
            graph.edge(class_name, nested_class_id)
            logger.debug(f"Added nested class node: {nested_class_id}")
            
            for nested_method in nested_class_info["methods"]:
                nested_method_id = f"{nested_class_id}.{nested_method}"
                graph.node(nested_method_id, nested_method)
                graph.edge(nested_class_id, nested_method_id)
                logger.debug(f"Added nested method node: {nested_method_id}")
    
    # Add semantic components and their relationships
    for component, implementations in verified_structure["semantic_components"].items():
        graph.node(component, component)
        graph.edge('root', component)
        logger.debug(f"Added semantic component node: {component}")
        
        for impl in implementations:
            graph.edge(impl, component)
            logger.debug(f"Added edge: {impl} -> {component}")
    
    logger.info("GCT graph creation completed.")
    return graph

def generate_graphs(input_files, output_dir):
    logger.info(f"Generating graphs for {len(input_files)} input files...")
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory created: {output_dir}")
    
    for input_file in input_files:
        file_name = os.path.basename(input_file)
        output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_graph")
        
        logger.info(f"Processing file: {file_name}")
        
        with open(input_file, 'r') as f:
            file_content = f.read()
        logger.debug(f"File content read: {file_name}")
        
        # First LLM call: Parse structure and semantic components
        parse_prompt = generate_parse_prompt(file_content)
        parsed_structure = get_claude_response(parse_prompt)
        if not parsed_structure:
            logger.error(f"Failed to parse structure for {file_name}. Skipping...")
            continue
        
        print("Parsed Structure (JSON):")
        print(parsed_structure)
        
        # Convert the JSON string to a Python dictionary
        try:
            parsed_structure = json.loads(parsed_structure)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON for {file_name}. Skipping...")
            continue
        
        # Verify structure against AST
        verified_structure, unmapped_methods = verify_structure(parsed_structure, file_content)
        
        if unmapped_methods:
            # Optional second LLM call: Categorize unmapped methods
            unmapped_prompt = generate_unmapped_methods_prompt(unmapped_methods, file_content)
            unmapped_categorization = get_claude_response(unmapped_prompt)
            if unmapped_categorization:
                try:
                    unmapped_categorization = json.loads(unmapped_categorization)
                    # Merge the new categorization with the existing semantic components
                    for component, methods in unmapped_categorization["semantic_components"].items():
                        if component in verified_structure["semantic_components"]:
                            verified_structure["semantic_components"][component].extend(methods)
                        else:
                            verified_structure["semantic_components"][component] = methods
                    logger.info("Unmapped methods have been categorized and added to semantic components.")
                except json.JSONDecodeError:
                    logger.error("Failed to decode JSON for unmapped methods categorization. Skipping this step.")
            else:
                logger.error("Failed to categorize unmapped methods. Skipping this step.")

        # Create GCT graph
        gct_graph = create_gct_graph(verified_structure)
        
        # Render and save the graph
        try:
            gct_graph.render(filename=output_file, format="pdf", cleanup=True)
            logger.info(f"Graph saved as {output_file}.pdf")
        except Exception as e:
            logger.error(f"Failed to render graph for {file_name}: {e}")

if __name__ == "__main__":
    logger.info("Starting GCT graph generation process...")
    
    # Define input files and output directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_files = [
        # os.path.join(base_dir, "examples", "temp", "model.py"),
        #os.path.join(base_dir, "examples", "temp", "llama3.py"),
        os.path.join(base_dir, "examples", "ambiguous_types.py"),
        os.path.join(base_dir, "examples", "complex_structure.py"),
        os.path.join(base_dir, "examples", "arithmetics.py"),
    ]
    output_dir = os.path.join(base_dir, "examples", "temp", "graphs")
    
    logger.info(f"Input files: {input_files}")
    logger.info(f"Output directory: {output_dir}")
    
    # Generate graphs
    generate_graphs(input_files, output_dir)
    
    logger.info("All graphs generated successfully!")