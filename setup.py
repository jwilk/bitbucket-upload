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
requires = ['requests==0.8.2'] + (['odict'] if under_270 else [])


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
      zip_safe=True,
      author=__author__,
      author_email=__email__,
      url='https://bitbucket.org/dahlia/bitbucket-distutils',
      license=__license__,
      install_requires=requires,
      setup_requires=requires,
      cmdclass=commands,
      entry_points={'distutils.commands': [
          'upload = bitbucket_distutils:upload'
      ]},
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: System :: Software Distribution'
      ])

