""" jsonpublish package"""

try:
    import simplejson as json
except ImportError:
    import json

from zope import proxy
from zope.interface import adapter
from zope.interface import Interface, providedBy, implementedBy
from repoze.lru import lru_cache

__all__ = (
    "JSONEncoder", "JSONEncoderSettingsProxy", "jsonsettings",
    "register_adapter", "dumps")

class IJSONSerializeable(Interface):
    """ Marker interface"""

class JSONEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        if "_adapters" in kwargs:
            self._adapters = kwargs.pop("_adapters")
        else:
            self._adapters = adapter.AdapterRegistry()
        super(Encoder, self).__init__(*args, **kwargs)

    def register_adapter(self, typ, adapter):
        register_adapter(typ, adapters, adapters=self._adapters)

    @lru_cache(500)
    def _lookup_adapter(self, typ):
        return self._adapters.lookup([typ], IJSONSerializeable, '')

    def default(self, o, **settings):
        if proxy.isProxy(o, JSONEncoderSettingsProxy):
            o, settings = proxy.getProxiedObject(o), o.__json_settings__
        adapter = self._lookup_adapter(providedBy(o))
        return adapter(o, **settings)

class JSONEncoderSettingsProxy(proxy.ProxyBase):

    __slots__ = ("__json_settings__",)

    def __new__(cls, o, **settings):
        p = proxy.ProxyBase.__new__(cls, o)
        p.__json_settings__ = settings
        return p

    def __init__(self, o, **settings):
        pass

jsonsettings = JSONEncoderSettingsProxy

_global_adapters = adapter.AdapterRegistry()

def register_adapter(typ, adapter, adapters=_global_adapters):
    adapters.register([implementedBy(typ)], IJSONSerializeable, '', adapter)

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, indent=None, separators=None,
        encoding='utf-8', default=None, use_decimal=True,
        namedtuple_as_object=True,
        tuple_as_array=True,
        **kw):
    return JSONEncoder(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, encoding=encoding, default=default,
        use_decimal=use_decimal,
        namedtuple_as_object=namedtuple_as_object,
        tuple_as_array=tuple_as_array, _adapters=_global_adapters,
        **kw).encode(obj)
