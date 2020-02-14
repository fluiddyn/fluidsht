#!/bin/bash
source ./VERSIONS.sh
hg clone https://foss.heptapod.net/nschaeff/shtns
cd shtns
hg update ${SHTNS_VERSION}
./configure --enable-openmp --enable-python
make -j
python setup.py install
