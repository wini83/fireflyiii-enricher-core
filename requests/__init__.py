class RequestException(Exception):
    """Placeholder for requests' RequestException."""


def get(*_args, **_kwargs):
    raise NotImplementedError


def post(*_args, **_kwargs):
    raise NotImplementedError


def put(*_args, **_kwargs):
    raise NotImplementedError
