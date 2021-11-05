import _imp
import os
import sys
import struct
from distutils.spawn import find_executable

so_ext = _imp.extension_suffixes()[0]

mybase = os.path.dirname(os.path.dirname(__file__))

# FIXME: The compiler-specific values should be exported from the build,
# perhaps via a special __pypy__._sysconfigdata module?

pydot = '%d.%d' % sys.version_info[:2]

build_time_vars = {
    'ABIFLAGS': '',
    # SOABI is PEP 3149 compliant, but CPython3 has so_ext.split('.')[1]
    # ("ABI tag"-"platform tag") where this is ABI tag only. Wheel 0.34.2
    # depends on this value, so don't make it CPython compliant without
    # checking wheel: it uses pep425tags.get_abi_tag with special handling
    # for CPython
    "SOABI": '-'.join(so_ext.split('.')[1].split('-')[:2]),
    "SO": so_ext,  # deprecated in Python 3, for backward compatibility
    'MULTIARCH': sys.implementation._multiarch,
    'CC': "cc -pthread",
    'CXX': "c++ -pthread",
    'OPT': "-DNDEBUG -O2",
    'CFLAGS': "-DNDEBUG -O2",
    'CCSHARED': "-fPIC",
    'LDSHARED': "cc -pthread -shared",
    'EXT_SUFFIX': so_ext,
    'SHLIB_SUFFIX': ".so",
    'AR': "ar",
    'ARFLAGS': "rc",
    'EXE': "",
    # This should point to where the libpypy3-c.so file lives, on CPython
    # it points to "mybase/lib". But that would require rethinking the PyPy
    # packaging process which copies pypy3 and libpypy3-c.so to the
    # "mybase/bin" directory. Only when making a portable build (the default
    # for the linux buildbots) is there even a "mybase/lib" created, even so
    # the mybase/bin layout is left untouched.
    'LIBDIR': os.path.join(mybase, 'bin'),
    'LDLIBRARY': 'libpypy3-c.so',
    'VERSION': pydot,
    'LDVERSION': pydot,
    'Py_DEBUG': 0,  # cpyext never uses this
    'Py_ENABLE_SHARED': 0,  # if 1, will add python so to link like -lpython3.7
    'SIZEOF_VOID_P': struct.calcsize("P"),
}
if sys.platform == 'win32':
    build_time_vars['INCLUDEPY'] = os.path.join(mybase, 'include')
else:
    build_time_vars['INCLUDEPY'] = os.path.join(mybase, 'include', 'pypy' + pydot)

if find_executable("gcc"):
    build_time_vars.update({
        "CC": "gcc -pthread",
        "GNULD": "yes",
        "LDSHARED": "gcc -pthread -shared",
    })
    if find_executable("g++"):
        build_time_vars["CXX"] = "g++ -pthread"

if sys.platform[:6] == "darwin":
    # Fix this if we ever get M1 support
    arch = 'x86_64'
    build_time_vars['CC'] += ' -arch %s' % (arch,)
    build_time_vars['LDSHARED'] = build_time_vars['CC'] + ' -shared -undefined dynamic_lookup'
    build_time_vars['LDLIBRARY'] = 'libpypy3-c.dylib'
    if "CXX" in build_time_vars:
        build_time_vars['CXX'] += ' -arch %s' % (arch,)
    build_time_vars['MACOSX_DEPLOYMENT_TARGET'] = '10.7'

