#!/usr/bin/env python

import os
from fnmatch import fnmatch

from numpy import get_include as numpy_includes
from setuptools import setup, Extension


def c_sources(parent):
    sources = []
    for root, _, files in os.walk(parent):
        for f in files:
            fn = os.path.join(root, f)
            if fnmatch(fn, '*.c'):
                sources.append(fn)
    return sources


def c_includes(parent, depth=1):
    includes = [parent]
    for root, dirs, _ in os.walk(parent):
        for d in dirs:
            dn = os.path.join(root, d)
            if len(dn.split(os.sep)) - 1 > depth:
                continue
            includes.append(dn)
    return includes


SOURCES = c_sources('src')
INCLUDES = c_includes('include') + c_includes('src') + [numpy_includes()]

# importing these extension modules is tested in `.github/workflows/build.yml`; 
# when adding new modules here, make sure to add them to the `test_command` entry there
ext_modules = [
    Extension(
        'stsci.stimage._stimage',
        sources=SOURCES,
        include_dirs=INCLUDES,
    ),
]

setup(
    ext_modules=ext_modules,
)
