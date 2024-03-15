# coding: utf-8
"""
    :author: linshukai
    :description: About Rpc Example
"""

from xmlrpc.server import SimpleXMLRPCServer


class KeyValueServer:
    _rpc_methods = ["get", "set", "delete", "exists", "keys"]

    def __init__(self, address):
        self._data = {}
        self._srv = SimpleXMLRPCServer(address, allow_none=True)

        for method in self._rpc_methods:
            self._srv.register_function(getattr(self, method))

    def get(self, name):
        return self._data[name]

    def set(self, name, value):
        self._data[name] = value

    def delete(self, name):
        del self._data[name]

    def exists(self, name):
        return name in self._data

    def keys(self):
        return list(self._data)

    def serve_forever(self):
        self._srv.serve_forever()


if __name__ == "__main__":
   ks = KeyValueServer(("", 9992))
   ks.serve_forever()