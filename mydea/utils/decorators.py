"""Utils functions for customize decorators"""

from functools import wraps

def context(f):
    """Return context  for customize decorators"""
    def _context(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info.context, *args, **kwargs)
        return wrapper
    return _context