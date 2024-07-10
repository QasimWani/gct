""" Ported from gct-server """
import urllib.request


def fetch_valid_url(url: str):
    """
    Verify if the provided url is valid. Converts github URLs to raw githubusercontent URLs.
    @Parameters:
    1. url: str = url to be validated.
    @Returns: An dictionary with the following keys:
        1. valid: bool = True if url is valid, False otherwise.
        2. url: str = url if url is valid (and converted to githubusercontent
        url if provided github url), None otherwise.
    """
    status = {"valid": False, "url": None}
    if url is None or len(url.strip()) == 0 or not url.startswith("http"):
        return status

    # Handle github raw URL.
    host = urllib.request.urlparse(url).hostname
    if host.startswith("raw.githubusercontent.com"):
        # Try to open the URL.
        status["valid"] = try_open_url(url)
        status["url"] = url
        return status
    if host.startswith("github.com"):
        # Try to open the URL.
        is_valid = try_open_url(url)
        if not is_valid:
            status["url"] = url
            return status
        # Convert to raw githubusercontent URL.
        url = url.replace("github.com", "raw.githubusercontent.com")
        url = url.replace("/blob/", "/")
        status["valid"] = try_open_url(url)
        status["url"] = url
        return status
    else:
        status["valid"] = try_open_url(url)
        status["url"] = url
        return status


def try_open_url(url: str):
    """
    Try to open the specified url.
    @Parameters:
    1. url: str = url to be opened.
    @Returns: True is url is successfully opened, False otherwise.
    """
    try:
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        print(e)
        return False
