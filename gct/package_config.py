import platform
import subprocess

GRAPHVIZ_INSTRUCTIONS_LINK = (
    "https://github.com/QasimWani/gct/blob/main/README.md#installing-graphviz"
)
GCT_ISSUE_LINK = "https://github.com/QasimWani/gct/issues/new"


def _install_pip_package(package: str):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call(["pip", "install", package])


def _is_graphviz_installed():
    """Function that checks if graphviz is installed and if so, is dot version >= 6.0.1"""
    try:
        output = subprocess.Popen(
            ["dot", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        data = output.stderr.read()

        version = (
            data.decode("utf-8").split("graphviz version ")[1].split(" ")[0].strip()
        )
        assert version >= "6.0.1", version
        return True

    except AssertionError as e:
        message = f"Found graphviz dot version {e}. Dot version >= 6.0.1 is required. See instructions for graphviz: {GRAPHVIZ_INSTRUCTIONS_LINK}"
        raise Exception(message)

    except Exception as e:
        print("Graphviz not installed. See instructions for graphviz:", e)
    return False


def _is_dot_installed():
    # Check for correct version of graphviz, if installed.
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
    PACKAGES = ["argparse", "graphviz", "networkx", "platform"]
    for package in PACKAGES:
        _install_pip_package(package)

    _is_dot_installed()
