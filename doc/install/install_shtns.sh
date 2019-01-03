#!/bin/bash
hg clone https://bitbucket.org/nschaeff/shtns
cd shtns
hg update v3.1
CC=clang ./configure --enable-openmp --enable-python
make -j
python setup.py install
