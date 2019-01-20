Installation and advice
=======================

Dependencies
------------

- Python >= 3.6

- a C++11 compiler (for example GCC>=4.9 or Clang)

- Numpy

  Make sure to correctly install numpy before anything.

- `Transonic <https://transonic.readthedocs.io>`_

- `Pythran <https://github.com/serge-sans-paille/pythran>`_

  We choose to use the new static Python compiler `Pythran
  <https://github.com/serge-sans-paille/pythran>`_ for some functions of the
  operators. Our microbenchmarks show that the performances are as good as what
  we are able to get with Fortran or C++!

  .. warning::

     To reach good performance, we advice to try to put in the file
     `~/.pythranrc` the lines (it seems to work well on Linux, see the `Pythran
     documentation <https://pythonhosted.org/pythran/MANUAL.html>`_):

     .. code:: bash

        [pythran]
        blas = openblas
        complex_hook = True

- Spherical harmonics libraries


.. include:: install/sht_libs.rst
