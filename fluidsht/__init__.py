"""FluidSHT: Spherical Harmonics Transform API
===============================================

The sht and related `operators` classes are in the subpackages

.. autosummary::
   :toctree:

   sht2d

This root module provides two helper functions to import sht classes and
create sht objects:

.. autofunction:: import_sht_class

.. autofunction:: create_sht_object

"""
from importlib import import_module as _import_module
from fluidsht._version import __version__, __about__

__all__ = ["__version__", "__about__", "import_sht_class", "create_sht_object"]


def import_sht_class(method, raise_import_error=True):
    """Import a sht class.

    Parameters
    ----------

    method : str
      Name of module or string characterizing a method. It has to correspond to
      a module of fluidsht. The first part "fluidsht." of the module "path" can
      be omitted.

    raise_import_error : {True}, False

      If raise_import_error == False and if there is an import error, the
      function handles the error and returns None.

    Returns
    -------

    The corresponding SHT class.

    """
    if method.startswith("sht2d.") or method.startswith("sht3d."):
        method = "fluidsht." + method

    if not method.startswith("fluidsht."):
        raise ValueError(
            "not method.startswith('fluidsht.')\nmethod = {}".format(method)
        )

    try:
        mod = _import_module(method)
    except ImportError:
        if raise_import_error:
            raise ImportError(method)
        else:
            print("ImportError:", method)
            return None

    return mod.SHTclass


def create_sht_object(
    method, n0=None, n1=None, n2=None, lmax=15, norm=None, grid_type="gaussian"
):
    """Helper for creating sht objects.

    Parameters
    ----------

    method : str
      Name of module or string characterizing a method. It has to correspond to
      a module of fluidsht. The first part "fluidsht." of the module "path" can
      be omitted.

    n0, n1, n2 : int
      Dimensions of the real space array (in sequential).

    lmax : int
      Truncation degree

    norm : str
      Normalization factor

    grid_type : str
      Grid to sample from.

    Returns
    -------

    The corresponding SHT object.


    """

    cls = import_sht_class(method)

    str_module = cls.__module__

    if n2 is None and str_module.startswith("fluidsht.sht3d."):
        raise ValueError("Arguments incompatible")
    elif n2 is not None and str_module.startswith("fluidsht.sht2d."):
        raise ValueError("Arguments incompatible")

    if n2 is None:
        return cls(n0, n1, lmax, norm=norm, grid_type=grid_type)
    else:
        raise NotImplementedError
        # return cls(n0, n1, n2, lmax, norm=flags, flags=flags)
