from __future__ import print_function
import os, sys

def warn(message, **kwargs):
    _print_message(message, 'error', sys.stderr, **kwargs)

def info(message, **kwargs):
    _print_message(message, 'info', sys.stderr, **kwargs)

def _print_message(message, type, file, line=None, infile=None):
    message = str(message)
    if line and infile:
        message = "[{}] {} line {}: {}".format(type, infile, line, message)
    print(message, file=file)

class Path: # Heh, classpath
    PATH_BASE = os.getcwd()
    PATH_LEVELS = os.path.join(PATH_BASE, "levels")

    @staticmethod
    def resolve_path(path, type=""):
        if type == "":
            if not path.startswith(Path.PATH_BASE):
                path = os.path.join(Path.PATH_BASE, path)
            return path
        elif type == "levels":
            if not path.startswith(Path.PATH_LEVELS):
                path = os.path.join(Path.PATH_LEVELS, path)
            return path
        else:
            warn("Unknown path type: {}; ignoring".format(type))
            return ""
