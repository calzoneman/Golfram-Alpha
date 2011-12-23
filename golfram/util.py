import sys

def warn(message, **kwargs):
    _print_message(message, 'error', sys.stderr, **kwargs)

def info(message, **kwargs):
    _print_message(message, 'info', sys.stderr, **kwargs)

def _print_message(message, type, file, *, line=None):
    message = str(message)
    if line:
        message = "[type] {}: {}".format(line, message)
    print(message, file=file)
