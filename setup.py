import os
from runpy import run_path
from pathlib import Path

from setuptools import setup, find_packages
from fluidpythran.dist import make_pythran_files

from config import fluidsht_build_ext, make_pythran_extensions, use_pythran

f"In >=2018, you should use a Python supporting f-strings!"

here = Path(__file__).parent.absolute()

d = run_path(str(here / "fluidsht" / "_version.py"))
__version__ = d["__version__"]
__about__ = d["__about__"]

print(__about__)

paths = ["fluidsht/sht2d/operators.py"]
make_pythran_files(
    [here / path for path in paths],
    mocked_modules=("cached_property",),
)


ext_modules = []
if use_pythran:
    ext_names = []
    for root, dirs, files in os.walk("fluidsht"):
        path_dir = Path(root)
        for name in files:
            if (
                name.endswith("_pythran.py")
                or path_dir.name == "__pythran__"
                and name.endswith(".py")
            ):
                path = os.path.join(root, name)
                ext_names.append(path.replace(os.path.sep, ".").split(".py")[0])

    ext_modules += make_pythran_extensions(ext_names)

setup(
    version=__version__,
    cmdclass={"build_ext": fluidsht_build_ext},
    ext_modules=ext_modules,
)
