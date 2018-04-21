"""
=======
Helpers
=======
Useful helper methods that frequently used in this project
"""
import os

def prop2pair(cls, out='tuple', startswith_only=None):
    """
    Iterates over each property of the cls and prepare the key-value pair

    :param cls: Class to be interated over
    :param str out: Output format either `tuple` or `dict`
    :param str startswith_only: Consider only properties that starts with this value
    :return tuple,dict:
    """
    if startswith_only is not None:
        d = {getattr(cls, prop): prop.replace('_', ' ').title() for prop in dir(cls)
             if prop.startswith(startswith_only) is True}
    else:
        d = {getattr(cls, prop): prop.replace('_', ' ').title() for prop in dir(cls)
             if prop.startswith('_') is False}

    if out == 'tuple':
        d = d.items()

    if out == 'array':
        d = [dict(key=pn[0], value=pn[1]) for pn in d.items()]

    if out == 'list':
        d = [pn[0] for pn in d.items()]

    return d

