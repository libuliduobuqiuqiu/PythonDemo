XMLRpc简单应用示例

Server端：
```python
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
```

Client端
```
def xml_rpc_client():
    client = ServerProxy("http://127.0.0.1:9992", allow_none=True)
    client.set("name", "linshukai")
    client.set("age", 22)
    print(client.keys())
    try:
        print(client.get("name"), client.get("address"))
    except Exception as e:
        print(e)

    client.set("address", "GuangDong DongGuan")
    print(client.exists("address"))
    print(client.get("address"))
```


多进程间的Socket通信
```python
from multiprocessing.reduction import recv_handle, send_handle
import multiprocessing
import socket

def worker(in_p, out_p):
    out_p.close()

    while True:
        fd = recv_handle(in_p)

        print("Got Child FD: ", fd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as s:
            while True:
                msg = s.recv(1024)
                if not msg:
                    break
                print(f"Child recv: {msg}")
                s.send(msg)


def server(address, in_p, out_p, worker_pid):
    in_p.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    s.bind(address)
    s.listen(1)

    while True:
        client, addr = s.accept()
        print("Server: Got Connection from: ", addr)
        send_handle(out_p, client.fileno(), worker_pid)
        client.close()


if __name__ == "__main__":
    c1, c2 = multiprocessing.Pipe()
    worker_p = multiprocessing.Process(target=worker, args=(c1, c2))
    worker_p.start()

    server_p = multiprocessing.Process(target=server, args=(("", 8992), c1, c2, worker_p.pid))
    server_p.start()

    c1.close()
    c2.close()
```

理解事件驱动的I/O（作为了解）
基于事件循环，监听多个事件源（Socket套接字、文件），事件源发生事件，通知事件循环，后者调用回调函数处理事件。
通过回调函数的异步执行，程序能够高效处理多个并发事件。



