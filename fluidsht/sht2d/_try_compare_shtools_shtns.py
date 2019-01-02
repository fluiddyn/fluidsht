from fluidsht import OperatorsSphereHarmo2D
from fluidsht.sht2d._try_with_shtools import SHT2DWithSHTOOLS
from time import time

lmax = 15
nlat = lmax + 1
nlon = 2*lmax + 1

oper = OperatorsSphereHarmo2D(nlat, nlon, lmax)
optools = SHT2DWithSHTOOLS(nlat, nlon, lmax)

spat = oper.create_array_spat_random()
print("shapeX =", oper.shapeX)
print("shapeK =", oper.shapeK)
print("l_idx.shape=", oper.opsht.l_idx.shape, "= \n" ,  oper.opsht.l_idx)

# print("zeros=\n", optools._grid_coeffs[0])
# print("weights=\n", optools._grid_coeffs[1])

print("-----------")
print("spat max =", spat.max(), "sum =", spat.sum())

tstart = time()
sh_ns = oper.sht(spat)
spat_ns = oper.isht(sh_ns)
tend = time()
print("Time taken for sht and isht by shtns =", tend - tstart)

tstart = time()
sh_tools = optools.sht(spat)
spat_tools = optools.isht(sh_tools)
tend = time()
print("Time taken for sht and isht by shtools=", tend - tstart)

print()
print("spat by shtns max =", spat_ns.max(), "sum =", spat_ns.sum())
print("spat by shttools max =", spat_tools.max(), "sum =", spat_tools.sum())
