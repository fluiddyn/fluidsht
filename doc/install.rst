Installation and advice
=======================

Dependencies
------------

- Python 2.7 or >= 3.4

- a C++11 compiler (for example GCC 4.9)

- Numpy

  Make sure to correctly install numpy before anything. 

  .. note::
  
     Be careful, the wheels install with `pip install numpy` can be slow. You
     might get something more efficient by compiling from source using:

     .. code:: bash

        pip install numpy --no-binary numpy
        python -c 'import numpy; numpy.test()'

- Cython

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
        complex_hook = True

- mpi4py (optional, only for mpi runs),
  
- Spherical harmonics libraries

  .. toctree::
     :maxdepth: 1

     install/sht_libs


Build/install
~~~~~~~~~~~~~

Build/install in development mode (with a virtualenv)::

  python setup.py develop

or (without virtualenv)::

  python setup.py develop --user

Of course you can also install FluidDyn with the install command ``python
setup.py install``.

After the installation, it is a good practice to run the unit tests by running
``python -m unittest discover`` from the root directory or from any of the
"test" directories (or just ``make tests`` or ``make tests_mpi``).
