FluidSHT: efficient and easy Spherical Harmonic Transforms for Python
=====================================================================

A Python package to provide a unified API to perform `Spherical Harmonic
Transforms (SHT) <https://en.wikipedia.org/wiki/Spherical_harmonics>`_. For the
uninitiated, SHT is the spherical coordinates equivalent of FFT for cartesian
coordinates. This package provides Python wrapper classes to facilitate SHT and
related operators, very similar to `FluidFFT <http://fluidfft.readthedocs.org>`_,
using various libraries such as:

- `SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_

- `libsharp <https://github.com/Libsharp/libsharp>`_

SHTns is an OpenMP implementation while, libsharp is an MPI implementation.
Both libraries have built-in python bindings. There are other SHT codes such as:

- `HEALPix <http://healpix.sourceforge.net/>`_ / `Healpy <https://github.com/healpy/healpy>`_

- `Rayleigh <https://github.com/geodynamics/Rayleigh>`_

- `SHTOOLS <https://github.com/SHTOOLS/SHTOOLS>`_

- `S2HAT <http://www.apc.univ-paris7.fr/APC_CS/Recherche/Adamis/MIDAS09/software/s2hat/s2hat.html>`_

which may be pursued if needed.
