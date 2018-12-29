import os
import sys
import numpy as np
from setuptools.command.build_ext import build_ext
from distutils.sysconfig import get_config_var

try:
    from pythran.dist import PythranExtension

    use_pythran = True
except ImportError:
    use_pythran = False

try:
    # pythran > 0.8.6
    from pythran.dist import PythranBuildExt, PythranExtension

    class fluidsht_build_ext(build_ext, PythranBuildExt):
        def build_extension(self, ext):
            if isinstance(ext, PythranExtension):
                PythranBuildExt.build_extension(self, ext)
            else:
                build_ext.build_extension(self, ext)

except ImportError:
    fluidsht_build_ext = build_ext

try:
    import colorlog as logging

    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.ColoredFormatter("%(log_color)s%(levelname)s: %(message)s")
    )
except ImportError:
    import logging

    handler = logging.StreamHandler()


logger = logging.getLogger("fluidsim")
logger.addHandler(handler)
logger.setLevel(20)


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


def make_pythran_extensions(modules):
    exclude_pythran = tuple()
    if len(exclude_pythran) > 0:
        logger.info(
            "Pythran files in the packages "
            + str(exclude_pythran)
            + " will not be built."
        )
    develop = sys.argv[-1] == "develop"
    extensions = []
    for mod in modules:
        package = mod.rsplit(".", 1)[0]
        if any(package == excluded for excluded in exclude_pythran):
            continue
        base_file = mod.replace(".", os.path.sep)
        py_file = base_file + ".py"
        # warning: does not work on Windows
        suffix = get_config_var("EXT_SUFFIX") or ".so"
        bin_file = base_file + suffix
        logger.info(
            "make_pythran_extension: {} -> {} ".format(
                py_file, os.path.basename(bin_file)
            )
        )
        if (
            not develop
            or not os.path.exists(bin_file)
            or modification_date(bin_file) < modification_date(py_file)
        ):
            pext = PythranExtension(mod, [py_file], extra_compile_args=["-O3"])
            pext.include_dirs.append(np.get_include())
            # bug pythran extension...
            compile_arch = os.getenv("CARCH", "native")
            pext.extra_compile_args.extend(
                ["-O3", "-march={}".format(compile_arch), "-DUSE_XSIMD"]
            )
            # pext.extra_link_args.extend(['-fopenmp'])
            extensions.append(pext)

    if not extensions:
        logger.info(f"Skipping Pythran compilation for extensions {modules}")
    return extensions
