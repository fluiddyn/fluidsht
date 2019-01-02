#!/bin/bash
hg clone https://bitbucket.org/nschaeff/shtns
cd shtns
hg update v3.1
./configure --enable-openmp --enable-python
make
python setup.py install
