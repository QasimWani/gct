""" 
Wrapper around api.py to run GCT on any file/URL.
"""
import sys

sys.path.append("../gct")

import gct.api as api
from gct.url import fetch_valid_url
import argparse
from gct.constants import TEMP_FOLDER, GRAPH_FOLDER_DEFAULT_NAME
from gct import __version__

parser = argparse.ArgumentParser()
parser.add_argument(
    "--input",
    "-i",
    type=str,
    required=True,
    help="File path or URL to visualize",
)

parser.add_argument(
    "--destination_folder",
    "-d",
    type=str,
    default=f"{TEMP_FOLDER}",
    help="Folder path to save resulting GCT graph to",
)

parser.add_argument(
    "--version",
    "-v",
    action="version",
    version=f"GCT version: {__version__}",
)


def main():
    args = parser.parse_args()

    # Download file if URL is valid
    status = fetch_valid_url(args.input)
    path = status["url"]
    if not status["valid"]:
        path = args.input

    graph, _ = api.run(path)

    api.render(
        graph,
        file_path=f"{args.destination_folder}/{GRAPH_FOLDER_DEFAULT_NAME}",
        output_format="pdf",
    )


if __name__ == "__main__":
    main()
