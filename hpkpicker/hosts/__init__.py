"""Host adapters.  No Autodesk module is imported until a host is detected."""

from .base import NullHost


def current_host():
    """Return the adapter for the running DCC, or a safe offline adapter."""
    try:
        from .maya import MayaHost
        return MayaHost()
    except ImportError:
        pass
    try:
        from .max import MaxHost
        return MaxHost()
    except ImportError:
        return NullHost()
