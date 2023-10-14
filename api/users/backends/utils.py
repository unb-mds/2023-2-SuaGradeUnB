from importlib import import_module


def get_backend(backend: str) -> object | None:
    try:
        module = import_module('users.backends.' + backend)
        return getattr(module, backend.title() + 'OAuth2')
    except (ImportError, AttributeError):
        return None