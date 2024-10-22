Supported SHT libraries and their installation
==============================================

`SHTns <https://users.isterre.fr/nschaeff/SHTns/>`_
------------------------------------------------------

SHTns is a high performance library for Spherical Harmonic Transform written
in C, aimed at numerical simulation (fluid flows, mhd, ...) in spherical
geometries. It scales using OpenMP, SIMD, and with beta-support for CUDA. It
is probably the fastest implementation for moderately sized grids.

``SHTns`` uses a simple GNU Autotools based installation procedure::

    hg clone https://foss.heptapod.net/nschaeff/shtns
    cd shtns
    hg update v3.3.1
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


.. note::

  Due to lack of documentation it is hard (not impossible) to implement
  an API bridge. The development of libsharp seems to have resumed recently
  and it looks promising. Now it uses pybind11:
  https://gitlab.mpcdf.mpg.de/mtr/libsharp/

The new library `pysharp` can be installed as follows::

  git clone https://gitlab.mpcdf.mpg.de/mtr/libsharp
  cd libsharp
  autoreconf -i
  CC=mpicc CFLAGS="-DUSE_MPI -std=c99 -O3 -march=native -ffast-math" ./configure
  make- j

  # Install
  cd python
  LDFLAGS="-L../.libs/" python setup.py install
  export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(realpath ../.libs)"
