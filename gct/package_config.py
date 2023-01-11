import platform
import subprocess

GRAPHVIZ_INSTRUCTIONS_LINK = "https://github.com/QasimWani/gct/blob/main/README.md#step-2-skip-if-already-installed-install-graphviz-executable"
GCT_ISSUE_LINK = "https://github.com/QasimWani/gct/issues/new"


def _install_pip_package(package: str):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(["pip", "install", package])


def _is_graphviz_installed():
    """Function that checks if graphviz is installed"""
    try:
        subprocess.Popen(["dot", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print("Graphviz not installed. See instructions for graphviz:", e)
    return False


def _is_dot_installed():
    if _is_graphviz_installed():
        return

    system = platform.system()
    if system == "Windows":
        message = "Graphviz package not install. Try running 'choco install -y graphviz'. \n If the error persists, install graphviz from here: https://graphviz.org/download"
    elif system == "Darwin":  # macOS
        message = "Graphviz package not install. Try running 'brew install graphviz'. \n If the error persists, install graphviz from here: https://graphviz.org/download"
    else:  # assume Linux or other Unix-like system
        message = "Graphviz package not install. Try running 'apt-get install graphviz'. \n If the error persists, install graphviz from here: https://graphviz.org/download"

    message += f"\nFor any other errors, please post an issue (response time <= 10 minutes): {GCT_ISSUE_LINK}"
    raise Exception(message)


# Install python packages and graphviz dist. if they don't exist.
def installer():
    PACKAGES = ["argparse", "graphviz", "networkx", "platform", "requests"]
    for package in PACKAGES:
        _install_pip_package(package)

    _is_dot_installed()
