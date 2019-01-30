======
|logo|
======
*efficient and easy Spherical Harmonic Transforms for Python*

|release| |pyversions| |docs| |coverage| |travis|

.. |logo| image:: https://bitbucket.org/fluiddyn/fluidsht/raw/default/doc/logo.svg
   :alt: FluidFFT

.. |release| image:: https://img.shields.io/pypi/v/fluidsht.svg
   :target: https://pypi.org/project/fluidsht/
   :alt: Latest version

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/fluidsht.svg
   :alt: Supported Python versions

.. |docs| image:: https://readthedocs.org/projects/fluidsht/badge/?version=latest
   :target: http://fluidsht.readthedocs.org
   :alt: Documentation status

.. |coverage| image:: https://codecov.io/bb/fluiddyn/fluidsht/branch/default/graph/badge.svg
   :target: https://codecov.io/bb/fluiddyn/fluidsht
   :alt: Code coverage

.. |travis| image:: https://travis-ci.org/fluiddyn/fluidsht.svg?branch=master
    :target: https://travis-ci.org/fluiddyn/fluidsht

.. |binder| image:: https://mybinder.org/badge_logo.svg
   :target: https://mybinder.org/v2/gh/fluiddyn/fluidsht/master?urlpath=lab/tree/doc/ipynb
   :alt: Binder notebook

A Python package to provide a unified API to perform `Spherical Harmonic
Transforms (SHT) <https://en.wikipedia.org/wiki/Spherical_harmonics>`_.

**Documentation**: https://fluidsht.readthedocs.io

Getting started
---------------

For a **basic installation** it should be sufficient to run::

  pip install fluidsht [--user]

You can get the source code from `Bitbucket
<https://bitbucket.org/fluiddyn/fluidsht>`__ or from `the Python
Package Index <https://pypi.org/project/fluidsht/>`__.
The development mode is often useful if you intend to modify fluidsht. From
the root directory::

  pip install -e .

Tests
-----

From the root directory::

  make tests

Or, from the root directory or any of the "test" directories::

  python -m unittest discover

How does it work?
-----------------

For the uninitiated, SHT is the spherical coordinates equivalent of FFT for
cartesian coordinates. The aim of this package is to provides Python wrapper
classes to facilitate SHT and related operators, very similar to `FluidFFT
<http://fluidfft.readthedocs.org>`_, using various libraries such as:

- `SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_

- `SHTOOLS <https://shtools.oca.eu/shtools/>`_

- `libsharp <https://github.com/Libsharp/libsharp>`_

SHTns and SHTOOLS are an OpenMP implementations while, libsharp is an MPI
implementation. All the libraries have built-in python bindings and ``SHTOOLS``
is pip installable. There are other SHT codes such as:

- `HEALPix <http://healpix.sourceforge.net/>`_ / `Healpy <https://github.com/healpy/healpy>`_

- `Rayleigh <https://github.com/geodynamics/Rayleigh>`_

- `S2HAT <http://www.apc.univ-paris7.fr/APC_CS/Recherche/Adamis/MIDAS09/software/s2hat/s2hat.html>`_

which may be pursued if needed.
