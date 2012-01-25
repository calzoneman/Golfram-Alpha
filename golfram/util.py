from __future__ import print_function
import os
import sys

import golfram.config

def warn(message, **kwargs):
    """Print a message explaining a non-critical error

    >>> warn("Blah!")
    warn: Blah!
    >>> warn("ignoring duplicate declaration", file='input.txt', line=42)
    [input.txt:42] warn: ignoring duplicate declaration

    """
    _print_message(message, 'warn', **kwargs)

def info(message, **kwargs):
    """Print a message explaining normal operation

    >>> info("everything works!")
    info: everything works!

    """
    _print_message(message, 'info', **kwargs)

def error(message, **kwargs):
    """Print a message explaining a critical error

    >>> error("can't open level: {}".format('level42.py'))
    error: can't open level: level42.py

    """
    _print_message(message, 'error', **kwargs)

def _print_message(message, message_type, output_file=None, line=None,
                   file=None):
    if file:
        file = os.path.basename(file)
    if line and file:
        template = '[{file}:{line}] {type}: {message}'
    elif file:
        template = '[{file}] {type}: {message}'
    else:
        template = '{type}: {message}'
    message = template.format(type=message_type, file=file,
                              line=line, message=message)
    print(message, file=output_file)

def get_path(filename, filetype=None):
    """Return the absolute path to the file of the specified type.

    Eventually this should move to some sort of GameInstance class,
    instances of which will know the proper locations of files.

    """
    base = golfram.config.get('data_path')
    if filetype == 'level':
        path = os.path.join(base, 'levels', filename)
    elif filetype == 'tiledef':
        path = os.path.join(base, 'levels', filename)
    elif filetype == 'texture':
        path = os.path.join(base, 'levels', filename)
    else:
        path = os.path.join(base, filename)
    return path


if __name__ == '__main__':
    import doctest
    doctest.testmod()
