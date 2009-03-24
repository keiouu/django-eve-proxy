"""
Based entirely on Django's own ``setup.py``.
"""
import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
extensions_dir = os.path.join(root_dir, 'eve_proxy')
pieces = fullsplit(root_dir)
if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)

for dirpath, dirnames, filenames in os.walk(extensions_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    #if 'conf' in dirpath:
    #    print dirpath
    if '__init__.py' in filenames and not 'conf' in dirpath:
        packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

version = __import__('eve_proxy').__version__

setup(
    name = 'django-eve-proxy',
    version = version,
    description = "A Django-based EVE API proxy.",
    long_description = """django-eve-proxy transparently handles requests to
the EVE API from Python code or via HTTP. This allows developers to
provide a restricted or global EVE API HTTP proxy, or access the EVE API
via the CachedDocument python object.
See the project page for more information:
http://code.google.com/p/django-eve-proxy/""",
    author = 'Gregory Taylor',
    author_email = 'gtaylor@l11solutions.com',
    url = 'http://code.google.com/p/django-eve-proxy/',
    license = 'GPL',
    platforms = ['any'],
    packages = packages,
    data_files = data_files,
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)

