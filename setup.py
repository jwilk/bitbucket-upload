import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from bitbucket_distutils import __author__, __email__, __license__, __version__

under_270 = sys.version_info < (2, 7, 0)


setup(name='bitbucket-distutils',
      version=__version__,
      py_modules=['bitbucket_distutils'],
      author=__author__,
      author_email=__email__,
      license=__license__,
      install_requires=['requests'] + (['odict'] if under_270 else []))

