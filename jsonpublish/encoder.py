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

class IJSONSettings(Interface):
    """ Marker interface"""

class SettingsRegistry(object):

    def __init__(self, settings):
        self.underlying = adapter.AdapterRegistry()
        for typ, s in settings.items():
            self.underlying.register([implementedBy(typ)], IJSONSettings, "", s)

    def lookup_settings(self, o):
        return self.underlying.lookup([providedBy(o)], IJSONSettings, "")

class IJSONSerializeable(Interface):
    """ Marker interface"""

class AdapterRegistry(object):
    """ Registry of adapters"""

    _sentinel = object()

    def __init__(self):
        self.underlying = adapter.AdapterRegistry()
        self.cache = LRUCache(500)

    def lookup_adapter(self, typ):
        """ Lookup adapter for ``typ``"""
        adapter = self.cache.get(typ, self._sentinel)
        if adapter is self._sentinel:
            adapter = self.underlying.lookup([typ], IJSONSerializeable, "")
            self.cache.put(typ, adapter)
        return adapter

    def register_adapter(self, typ, adapter=None):
        """ Register ``adapter`` for type ``typ``

        If no ``adapter`` supplied then this method returns decorator.
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

    :attr adapters:
        instance of :class:`.AdapterRegistry` which is used for serialization
        by encoder
    """

    def __init__(self, *args, **kwargs):
        if kwargs.get("adapters"):
            self.adapters = kwargs.pop("adapters")
        else:
            self.adapters = AdapterRegistry()
        if kwargs.get("settings"):
            self.settings = SettingsRegistry(kwargs.pop("settings"))
        else:
            self.settings = None
        super(JSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o, **settings):
        s = (self.settings.lookup_settings(o) if self.settings else {}) or {}
        s.update(settings)
        if proxy.isProxy(o, JSONEncoderSettingsProxy):
            s.update(o.__json_settings__)
            o = proxy.getProxiedObject(o)
        adapter = self.adapters.lookup_adapter(providedBy(o))
        if adapter is None:
            raise TypeError("%r is not JSON serializable" % o)
        return adapter(o, **s)

class JSONEncoderSettingsProxy(proxy.ProxyBase):
    """ Proxy which carries settings for adapters"""

    __slots__ = ("__json_settings__",)

    def __new__(cls, o, **settings):
        p = proxy.ProxyBase.__new__(cls, o)
        p.__json_settings__ = settings
        return p

    def __init__(self, o, **settings):
        pass

#: Create a proxy which carries JSON encoder settings
def jsonsettings(*o, **settings):
    if o:
        return JSONEncoderSettingsProxy(o[0], **settings)
    else:
        return settings
