Supported SHT libraries and their installation
==============================================

SHTns
-----
*`SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_ SHTns is a high
performance library for Spherical Harmonic Transform written in C, aimed at
numerical simulation (fluid flows, mhd, ...) in spherical geometries.*

It scales using OpenMP, and is probably the fastest implementation for
moderately sized grids.

SHT libraries depend on an FFTW installation. To know how to install see the
relevant `fluidfft
documentation<https://fluidfft.readthedocs.io/en/latest/install/fft_libs.html>`.
``SHTns`` uses a simple GNU Autotools based installation procedure, with a
``./configure``, ``make`` and ``make install`` step. If you have setup ``spack``
as suggested above , this can be done easily::

    spack install shtns+openmp+python
    module load shtns
