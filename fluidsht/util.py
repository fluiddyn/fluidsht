from collections import namedtuple


def make_namedtuple_from_module(module, pattern, typename, field_names):
    """Make a namedtuple instance from module containing various attributes.

    Parameters
    ----------

    module : module

    pattern : str

    typename : str

    field_names : iterable

    Returns
    -------
    New namedtuple type instantiated

    """
    field_values = []
    for name in field_names:
        attr = pattern.format(name)
        try:
            # attribute as is
            value = getattr(module, attr)
        except AttributeError:
            # uppercase attribute
            value = getattr(module, attr.upper())

        field_values.append(value)

    NamedTuple = namedtuple(typename, field_names)
    return NamedTuple(*field_values)
