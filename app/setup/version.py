import sys

PYTHON_VERSION = (3, 9)

def check_python_version():
    majorVersionMatch = (sys.version_info.major == PYTHON_VERSION[0])
    minorVersionMatch = (sys.version_info.minor == PYTHON_VERSION[1])
    return majorVersionMatch and minorVersionMatch
