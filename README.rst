FluidSHT: efficient and easy Spherical Harmonic Transforms for Python
=====================================================================

A Python package to provide a unified API to perform `Spherical Harmonic
Transforms (SHT) <https://en.wikipedia.org/wiki/Spherical_harmonics>`_. 


Getting started
---------------

For a **basic installation** it should be sufficient to run::

  pip install fluiddyn [--user]

You can get the source code from `Bitbucket
<https://bitbucket.org/fluiddyn/fluidsht>`__ or from `the Python
Package Index <https://pypi.python.org/pypi/fluidsht/>`__.
The development mode is often useful if you intend to modify fluidsht . From
the root directory::

  pip install -e .

How does it work?
-----------------

For the uninitiated, SHT is the spherical coordinates equivalent of FFT for
cartesian coordinates. This package provides Python wrapper classes to
facilitate SHT and related operators, very similar to `FluidFFT
<http://fluidfft.readthedocs.org>`_, using various libraries such as:

- `SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_

- `SHTOOLS <https://https://shtools.oca.eu/shtools/>`_

- `libsharp <https://github.com/Libsharp/libsharp>`_

SHTns and SHTOOLS are an OpenMP implementations while, libsharp is an MPI
implementation. All the libraries have built-in python bindings and ``SHTOOLS``
is pip installable. There are other SHT codes such as:

- `HEALPix <http://healpix.sourceforge.net/>`_ / `Healpy <https://github.com/healpy/healpy>`_

- `Rayleigh <https://github.com/geodynamics/Rayleigh>`_

- `SHTOOLS <https://github.com/SHTOOLS/SHTOOLS>`_

- `S2HAT <http://www.apc.univ-paris7.fr/APC_CS/Recherche/Adamis/MIDAS09/software/s2hat/s2hat.html>`_

which may be pursued if needed.
