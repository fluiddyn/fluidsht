import os
import sys
from runpy import run_path
from pathlib import Path

from setuptools import setup
from setuptools.dist import Distribution

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")


def install_setup_requires():
    dist = Distribution()
    # Honor setup.cfg's options.
    dist.parse_config_files(ignore_option_errors=True)
    if dist.setup_requires:
        dist.fetch_build_eggs(dist.setup_requires)


install_setup_requires()

here = Path(__file__).parent.absolute()

try:
    from setup_build import FluidSHTBuildExt, logger
except ImportError:
    d = run_path(str(here / "setup_build.py"))
    FluidSHTBuildExt = d["FluidSHTBuildExt"]
    logger = d["logger"]


d = run_path(str(here / "fluidsht" / "_version.py"))
__version__ = d["__version__"]
__about__ = d["__about__"]


def trasonize():
    from transonic.dist import make_backend_files

    paths = ["fluidsht/sht2d/operators.py"]
    make_backend_files([here / path for path in paths])


def create_extensions():
    if "egg_info" in sys.argv:
        return []

    import numpy as np
    from transonic.dist import init_pythran_extensions

    logger.info("Running fluidsht setup.py on platform " + sys.platform)
    logger.info(__about__)

    trasonize()
    compile_arch = os.getenv("CARCH", "native")
    extensions = init_pythran_extensions(
        "fluidsht",
        include_dirs=np.get_include(),
        compile_args=("-O3", "-march={}".format(compile_arch), "-DUSE_XSIMD"),
        logger=logger,
    )
    logger.debug("Extensions: {}".format(extensions))
    return extensions


setup(
    version=__version__,
    cmdclass={"build_ext": FluidSHTBuildExt},
    ext_modules=create_extensions(),
)
