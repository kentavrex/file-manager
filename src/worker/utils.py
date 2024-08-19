from urllib.parse import unquote, urlparse


def get_path_from_url(url: str) -> str:
    """
    Converts url with args to uri without args

    https://example.domain.org/here/is/path/to/file.txt?arg1=123&arg2=qwe
    -->
    here/is/path/to/file.txt
    """
    return urlparse(unquote(url)).path[1:]
