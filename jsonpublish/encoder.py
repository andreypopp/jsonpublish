""" Configurable JSON encoder for publishing Python objects"""

try:
    import simplejson as json
except ImportError:
    import json

from zope import proxy
from zope.interface import adapter
from zope.interface import Interface, providedBy, implementedBy
from repoze.lru import LRUCache

__all__ = (
    "JSONEncoder", "JSONEncoderSettingsProxy", "jsonsettings",
    "AdapterRegistry")

class IJSONSerializeable(Interface):
    """ Marker interface"""

class AdapterRegistry(object):
    """ Registry of adapters"""

    _sentinel = object()

    def __init__(self):
        self.underlying = adapter.AdapterRegistry()
        self.cache = LRUCache(500)

    def lookup_adapter(self, typ):
        adapter = self.cache.get(typ, self._sentinel)
        if adapter is self._sentinel:
            adapter = self.underlying.lookup([typ], IJSONSerializeable, "")
            self.cache.put(typ, adapter)
        return adapter

    def register_adapter(self, typ, adapter=None):
        """ Register `adapter` for type `typ`

        If no `adapter` supplied then this method returns decorator.
        """
        if adapter is None:
            def decorator(adapter):
                self.register_adapter_impl(typ, adapter)
                return adapter
            return decorator
        return self.register_adapter_impl(typ, adapter)

    def register_adapter_impl(self, typ, adapter):
        self.underlying.register(
            [implementedBy(typ)], IJSONSerializeable, "", adapter)
        self.cache.clear()


class JSONEncoder(json.JSONEncoder):
    """ Configurable JSON encoder

    It serializes object by consulting adapter registry. Registry can be
    modified by accessing `adapters` attribute of encoder which is of type
    `AdapterRegistry`.
    """

    def __init__(self, *args, **kwargs):
        if "adapters" in kwargs:
            self.adapters = kwargs.pop("adapters")
        else:
            self.adapters = AdapterRegistry()
        super(JSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o, **settings):
        if proxy.isProxy(o, JSONEncoderSettingsProxy):
            o, settings = proxy.getProxiedObject(o), o.__json_settings__
        adapter = self.adapters.lookup_adapter(providedBy(o))
        if adapter is None:
            raise TypeError("%r is not JSON serializable" % o)
        return adapter(o, **settings)

class JSONEncoderSettingsProxy(proxy.ProxyBase):
    """ Proxy which carries settings for adapters"""

    __slots__ = ("__json_settings__",)

    def __new__(cls, o, **settings):
        p = proxy.ProxyBase.__new__(cls, o)
        p.__json_settings__ = settings
        return p

    def __init__(self, o, **settings):
        pass

jsonsettings = JSONEncoderSettingsProxy
