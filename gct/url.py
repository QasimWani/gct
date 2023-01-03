""" Ported from gct-server """
import urllib.request


def fetch_valid_url(url: str):
    """Make sure valid URL. Parses github URLs to raw githubusercontent URLs."""
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
    try:
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        print(e)
        return False
