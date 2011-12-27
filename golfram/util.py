from __future__ import print_function
import os
import sys

def warn(message, **kwargs):
    """Print a message explaining a non-critical error"""
    _print_message(message, 'warn', sys.stderr, **kwargs)

def info(message, **kwargs):
    """Print a message explaining normal operation"""
    _print_message(message, 'info', sys.stdout, **kwargs)

def error(message, **kwargs):
    """Print a message explaining a critical error"""
    _print_message(message, 'error', sys.stderr, **kwargs)

def _print_message(message, message_type, output_file, line=None, file=None):
    if line and file:
        template = '[{file}:{line}] {type}: {message}'
    elif file:
        template = '[{file}] {type}: {message}'
    else:
        template = '{type}: {message}'
    message = template.format(type=message_type, file=output_file, line=line,
                              message=message)
    print(message, file=output_file)

def absolute_path(filename, filetype=None):
    """Return the absolute path to the file of the specified type"""
    base = os.getcwd()
    if filetype == 'level':
        path = os.path.join(base, 'levels', filename)
    elif filetype == 'tiledef':
        path = os.path.join(base, 'levels', filename)
    else:
        path = os.path.join(base, filename)
    return path
