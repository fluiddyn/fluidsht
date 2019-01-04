Supported SHT libraries and their installation
==============================================

`SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_
------------------------------------------------------

SHTns is a high performance library for Spherical Harmonic Transform written
in C, aimed at numerical simulation (fluid flows, mhd, ...) in spherical
geometries. It scales using OpenMP, SIMD, and with beta-support for CUDA. It
is probably the fastest implementation for moderately sized grids.

``SHTns`` uses a simple GNU Autotools based installation procedure::

    hg clone https://bitbucket.org/nschaeff/shtns
    cd shtns
    hg update v3.1
    ./configure --enable-openmp --enable-python
    make
    python setup.py install

.. note::

    ``SHTns`` depend on an ``FFTW`` installation. To install ``FFTW`` see the
    relevant `FluidFFT documentation
    <https://fluidfft.readthedocs.io/en/latest/install/fft_libs.html>`_.

If you have setup ``spack``, follow the instructions in the 
`fluiddyn/spack-packages <https://github.com/fluiddyn/spack-packages>`_
repo and the above can be done as follows (needs improvement)::

    spack install shtns+openmp+python
    module load shtns

`SHTOOLS <https://shtools.oca.eu/shtools/>`__
---------------------------------------------

.. warning::

   API not implemented yet!

Simply install as::

    pip install pyshtools


`Libsharp <https://github.com/Libsharp/libsharp>`__
---------------------------------------------------

.. warning::

   API not implemented yet!

Libsharp has an MPI implementation to perform SHT analysis and synthesis.
Installation is possible as::

    pip install mpi4py numpy cython
    git clone https://github.com/Libsharp/libsharp
    cd libsharp
    autoconf
    ./configure --enable-pic
    make -j

    # Run tests - optional
    pip install nose
    make pytest

    # Install
    cd python
    LIBSHARP=../auto python setup.py install

However due to lack of documentation it is hard (not impossible) to implement
an API bridge.
