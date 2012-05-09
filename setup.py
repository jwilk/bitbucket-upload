from __future__ import with_statement
import sys
import os.path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from bitbucket_distutils import (__author__, __email__, __license__,
                                 __version__, commands)

under_270 = sys.version_info < (2, 7, 0)


def readme():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
            return f.read()
    except (IOError, OSError):
        return ''


setup(name='bitbucket-distutils',
      description='Distribute/setuptools/distutils command for Bitbucket. '
                  'You can use Bitbucket downloads instead of PyPI downloads '
                  'for release.',
      version=__version__,
      long_description=readme(),
      py_modules=['bitbucket_distutils'],
      author=__author__,
      author_email=__email__,
      license=__license__,
      install_requires=['requests==0.10.8'] + (['odict'] if under_270 else []),
      cmdclass=commands)

