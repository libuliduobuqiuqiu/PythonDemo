"""
    :Date: 2024-4-4
    :Author: linshukai
    :Description: About grpc service.
"""


from concurrent.futures import ThreadPoolExecutor

from grpc.experimental import grpc
from hello_pb2 import HelloResp

from hello_pb2_grpc import (
    SayHelloServicer,
    add_SayHelloServicer_to_server,
)


class SayHello(SayHelloServicer):
    def Hello(self, request, context):
        print(request)
        return HelloResp(msg=f"Hello, {request.name}!")


def server_run():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_SayHelloServicer_to_server(SayHello(), server)
    server.add_insecure_port("[::]:" + "50051")
    server.start()
    print("grpc server starting...")
    server.wait_for_termination()


if __name__ == "__main__":
    server_run()
