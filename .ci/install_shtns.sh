#!/bin/bash
source doc/install/VERSIONS.sh
hg clone https://bitbucket.org/nschaeff/shtns
cd shtns
hg update ${SHTNS_VERSION}
./configure --enable-openmp --enable-python --disable-simd
make -j
python setup.py install
