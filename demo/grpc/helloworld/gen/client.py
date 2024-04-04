"""
    :Date: 2024-4-4
    :Author: linshukai
    :Description: About grpc service client
"""


import grpc

import sys

sys.path.insert(0, "/data/PythonDemo/demo/grpc/helloworld/")

from hello_pb2 import HelloReq
from hello_pb2_grpc import SayHelloStub


def run():
    with grpc.insecure_channel("127.0.0.1:50030") as channel:
        stub = SayHelloStub(channel)
        response = stub.Hello(HelloReq(name="linshukai"))
        print(response.msg)


if __name__ == "__main__":
    run()
