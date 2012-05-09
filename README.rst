bitbucket-distutils
===================

Intro
-----

Distribute_/setuptools_/distutils_ command for Bitbucket_. You can use
Bitbucket downloads instead of PyPI_ downloads for release.

To use this, follow the instruction.

.. _Distribute: http://packages.python.org/distribute/
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. _distutils: http://docs.python.org/library/distutils.html
.. _Bitbucket: https://bitbucket.org/
.. _PyPI: http://pypi.python.org/


Instruction
-----------

First of all your software must be packaged within the standard distribution
way: use distutils_, Distribute_ or setuptools_.  This package contains
an extension command for that.  Insert the following lines into the head of
your ``setup.py`` file::

    try:
        from bitbucket_distutils import commands
    except ImportError:
        commands = {}

and then, pass the ``commands`` dictionary into your ``setup()`` function's
``cmdclass`` parameter and specify ``setup_requires`` parameter::

    setup(name='YourPackageName',
          version='1.2.3',
          ...,
          setup_requires=['bitbucket-distutils'],
          cmdclass=commands)

Now there will be the overwritten ``upload`` command for your ``setup.py``::

    $ python setup.py upload --help
    Common commands: (see '--help-commands' for more)

    ...

    Options for 'upload' command:
      --bb-repository (-R)  Bitbucket repository name e.g. user/reponame
      --bb-username (-u)    Bitbucket username
      --bb-password (-p)    Bitbucket password

    ...

As you can see there are ``--bb-``-prefixed options for the command.
If ``-u``/``--bb-username`` and ``--p``/``--bb-password`` are not present,
it shows the prompt.  ``-R``/``--bb-repository`` is required.


Upload
------

Upload is very easy::

    $ python setup.py sdist upload -R user/reponame register

By explained:

``sdist``
    Makes the source distribution file.  If your package name is
    ``YourPackageName`` and its version is ``1.2.3``, and then its file name
    becomes ``YourPackageName-1.2.3.tar.gz``.

``upload -R user/reponame``
    Uploads the built source distribution file into your Bitbucket repository.
    It does not mean that it will be version-controlled, but it will be simply
    uploaded to its downloads page.

``register``
    Using the Bitbucket download URL registers the package of this version
    into PyPI.
    The URL of PyPI page will be http://pypi.python.org/YourPackageName/1.2.3


Defaulting options
------------------

You can make default values for these options by specifying in the ``setup.cfg``
configuration file.  For example, if you want to default ``--bb-repository``,
make ``setup.cfg`` file like (hyphens becomes underscores)::

    [upload]
    bb_repository = user/reponame

You can make a shorthand alias as well::

    [aliases]
    release = sdist upload register


Author and license
------------------

It is distributed under Public Domain.  Just do what you want to do with this.
Written by `Hong Minhee`__.

You can checkout the source code from its `Bitbucket Mercurial repository`__::

    $ hg clone https://bitbucket.org/dahlia/bitbucket-distutils

If you found a bug, please report it to the `issue tracker`__.

__ http://dahlia.kr/
__ https://bitbucket.org/dahlia/bitbucket-distutils
__ https://bitbucket.org/dahlia/bitbucket-distutils/issues
