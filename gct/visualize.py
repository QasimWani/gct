""" 
Wrapper around api.py to run GCT on any file/URL.
"""
import sys

sys.path.append("../gct")

import gct.api as api
import argparse
from constants import TEMP_FOLDER, GRAPH_FOLDER_DEFAULT_NAME


parser = argparse.ArgumentParser()
parser.add_argument(
    "--resource",
    type=str,
    default="https://raw.githubusercontent.com/QasimWani/gct/main/examples/arithmetics.py",
    help="Path to the file/URL to visualize",
)

parser.add_argument(
    "--save_to_folder",
    type=str,
    default=f"{TEMP_FOLDER}",
    help="Folder path to save resulting GCT graph to",
)

if __name__ == "__main__":
    args = parser.parse_args()
    graph, code = api.run(args.resource)
    api.render(
        graph,
        file_path=f"{args.save_to_folder}/{GRAPH_FOLDER_DEFAULT_NAME}",
        output_format="pdf",
    )
