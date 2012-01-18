""" jsonpublish package"""

from jsonpublish.encoder import JSONEncoder, AdapterRegistry, jsonsettings

__all__ = ("dumps", "register_adapter", "jsonsettings")

_global_adapters = AdapterRegistry()
_default_encoder = JSONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    encoding='utf-8',
    default=None,
    adapters=_global_adapters,
)

register_adapter = _global_adapters.register_adapter

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, indent=None, separators=None,
        encoding='utf-8', default=None, use_decimal=True,
        namedtuple_as_object=True,
        tuple_as_array=True,
        **kw):
    """ Serialize `obj` using globally configured JSON encoder"""
    if (not skipkeys and ensure_ascii and
        check_circular and allow_nan
        and indent is None and separators is None and
        encoding == 'utf-8' and default is None and use_decimal
        and namedtuple_as_object and tuple_as_array and not kw):
        return _default_encoder.encode(obj)
    return JSONEncoder(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, encoding=encoding, default=default,
        use_decimal=use_decimal,
        namedtuple_as_object=namedtuple_as_object,
        tuple_as_array=tuple_as_array, adapters=_global_adapters,
        **kw).encode(obj)
