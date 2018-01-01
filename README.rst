FluidSHT: efficient and easy Spherical Harmonic Transforms for Python
====================================================================

A Python package to provide a unified API to perform `Spherical Harmonic
Transforms (SHT) <https://en.wikipedia.org/wiki/Spherical_harmonics>`_. For the
uninitiated, SHT is the spherical coordinates equivalent of FFT for cartesian
coordinates. This package provides Python wrapper classes to facilitate SHT and
related operators, very similar to `FluidFFT <http://fluidfft.readthedocs.org>`_,
using various libraries such as:

- `SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_

- `libsharp <https://github.com/Libsharp/libsharp>`_

SHTns is an OpenMP implementation while, libsharp is an MPI implementation.
Both libraries have built-in python bindings. There are other from-the-scratch
SHT codes such as `Rayleigh <https://github.com/geodynamics/Rayleigh>`_ which
may be pursued if needed.